# -*- coding: utf-8 -*-
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Fast rendering of vector field (fluid for example).
Code is based on https://www.shadertoy.com/view/4llGWl#
"""

from glumpy import app, gl, gloo, data

vertex = '''
attribute vec2 a_position;
varying vec2 fragCoord;

void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
    fragCoord = a_position;
}
'''

fragment = '''
#include "math/constants.glsl"
varying vec2 fragCoord;
uniform float iGlobalTime;
uniform vec2 iMouse;
uniform sampler2D iChannel0;

#define CUBIC_INTERPOLATION
#define STEP_COUNT 10
#define RUNGE_KUTTA
//#define SHOW_GRID
#define SHOW_FIELD
//#define SHOW_SPEED_SURFACE

vec4 rot(vec2 uv, vec2 center) {
    vec2 d = uv - center;
    float l = length(d);
    return vec4(d.y, -d.x, l, l+0.01);
}

vec4 point(vec2 uv, vec2 center) {
    vec2 d = uv - center;
    float l = length(d);
    return vec4(d.x, d.y,l, l+0.01);
}

vec2 field(vec2 uv) {
	vec2 dir = vec2(1, 0);
    vec2 mouse = (iMouse.x == 0. && iMouse.y==0.) ? vec2(-0.15,-0.1) : iMouse.xy;
    vec4 rot1 = rot(uv, mouse);
    vec4 rot2 = rot(uv, vec2(-mouse.x,mouse.y));
  	//vec4 p1 = point(uv, vec2(0.2,-0.2)); // source  point - looks bad
    //vec4 p2 = point(uv, vec2(-0.2,-0.2));  // sewer

    return
      // dir // constant part
        0.5*(
        + rot1.xy/(rot1.z*rot1.z+0.1)
        - rot2.xy/(rot2.z*rot2.z+0.1)
       // + p1.xy/(p1.z*p1.z+0.1)
       //  -p2.xy/(p2.z*p2.z+0.1)
       );
}

float getColor(vec2 uv) {
    #ifdef SHOW_GRID
    	vec2 d = step(0.95, fract(uv*10.));
    	return (d.x + d.y);
	#elif defined SHOW_FIELD
	    vec2 d = step(0.9, fract(uv*10.));
	    return d.x*d.y;
	#else
	    float c= texture2D(iChannel0, .5*(uv+1.)).x;
	    return c;
    #endif
}

float sumColor = 0.;
vec2 calcNext(vec2 uv, float t) {
    t /= float(STEP_COUNT);
    for(int i = 0; i < STEP_COUNT; ++i) {
        #ifdef RUNGE_KUTTA
        	vec2 k1 = -field(uv);
        	vec2 k2 = -field(uv + k1*t/2.);
        	vec2 k3 = -field(uv + k2*t/2.);
	        vec2 k4 = -field(uv + k3*t);
    	    uv = uv + t/6.*(k1+2.*k2+2.*k2+k3);
        #else
        	uv += -field(uv)*t;
        #endif

        #ifdef SHOW_FIELD
        	sumColor += getColor(uv);
        #endif
    }

    return uv;
}

float cubic(float x, float v0,float v1, float v2,float v3)
{
	float p = (v3 - v2) - (v0 - v1);
	return p*(x*x*x) + ((v0 - v1) - p)*(x*x) + (v2 - v0)*x + v1;
}


float getColor(vec2 uv, float cf, float per) {

    float k1 = 0.5;
    float k2 = 0.;

    float t1 = per * cf/4.;
    float t2 = t1 + per/4.;
 #ifdef SHOW_FIELD
	 calcNext(uv, t1 * k1 + k2);
     float  c =sumColor;
 #else
    vec2 uv1 = calcNext(uv, t1 * k1 + k2);
    vec2 uv2 = calcNext(uv, t2 * k1 + k2);
    float c1 = getColor(uv1);
    float c2 = getColor(uv2);

    #ifdef CUBIC_INTERPOLATION
        float t3 = t2 + per/4.;
        float t4 = t3 + per/4.;
        vec2 uv3 = calcNext(uv, t3 * k1 + k2);
        vec2 uv4 = calcNext(uv, t4 * k1 + k2);
        float c3 = getColor(uv3);
        float c4 = getColor(uv4);

    	float c = cubic(cf, c4,c3,c2,c1);
	#else
    	float c = mix(c2,c1, cf);
 	#endif
 #endif
    // SHOW_FIELD
    return c;

}

void main() {

    vec2 uv = fragCoord;

    float per = 2.;

    float cf = fract(iGlobalTime / per);
    float cl = getColor(uv,cf, per);
    float l = length(field(uv));
    cl = (cl-0.8)*2.+0.8;
    vec4 c = vec4(cl);

#ifdef SHOW_SPEED_SURFACE
    float del = 0.1;
    float q = smoothstep(0.8, 1., fract(l/del));
    vec4 range = mix(vec4(0, 1, 0, 0), vec4(1, 0, 0.5, 0), l*0.4)*2.;
    c +=range*q;
#endif
   c += 0.75*vec4(1.0, 0.6, 0.2, 1.)*exp(-1./abs(l+0.1))*2.;
   c *= smoothstep(0., 1.,l)+0.2;

	gl_FragColor = c;
}

'''

program = gloo.Program(vertex, fragment, count=4)
program['a_position'] = [(-1., -1.), (-1., +1.),
                         (+1., -1.), (+1., +1.)]
program['iChannel0'] = data.checkerboard()
program['iGlobalTime'] = 0.0

window = app.Window(width=900, height=900)


@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    program['iGlobalTime'] += dt


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)


@window.event
def on_mouse_drag(x, y, dx, dy, button):
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    program["iMouse"] = 2 * x / w - 1, 1 - 2 * y / h


@window.timer(1 / 5.0)
def timer(dt):
    window.set_title("time:{:5.1f}\tfps:{:3.1f}".format(program['iGlobalTime'][0], window.fps).encode())


app.run()
