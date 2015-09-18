# -*- coding: utf-8 -*-
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Fluid with obstacles.
https://www.shadertoy.com/view/lllGDl
"""

from glumpy import app, gl, gloo

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
varying vec2 fragCoord;
uniform float iGlobalTime;
uniform vec2 iMouse;

#define STEP_COUNT 10

//these are the field movers
vec2 swirl(vec2 uv, vec2 center, float strength, float eyeWall) {
    vec2 d = uv - center;
    return vec2(d.y, -d.x)/(dot(d,d)/strength+eyeWall);
}
vec2 spray(vec2 uv, vec2 center, vec2 dir, float strength, float eyeWall){
    vec2 d = uv - center;
    return vec2(d.x, d.y)/(dot(d,d)/strength+eyeWall)*dot(d,dir);
}
vec2 drain(vec2 uv, vec2 center, float strength, float eyeWall){
    vec2 d = uv - center;
    return -vec2(d.x, d.y)/(dot(d,d)/strength+eyeWall);
}
//DE is used to define barriors
float Tube(vec2 pa, vec2 ba){
    return length(pa-ba*clamp(dot(pa,ba)/dot(ba,ba),0.0,1.0));
}
float DE(vec2 p){
    p+=vec2(0.5);
    return min(length(p),Tube(p-vec2(1.0),vec2(0.4,0.2)));
}
vec2 ReflectOffSurf(vec2 p, vec2 r){
    float d=max(DE(p),0.001);
    vec2 v=vec2(d,0.0);
    vec2 N=normalize(vec2(DE(p+v.xy)-DE(p-v.xy),DE(p+v.yx)-DE(p-v.yx)));
    d=clamp(sqrt(d)*1.1,0.0,1.0);
    r=mix(reflect(r,N)*clamp(0.5-0.5*dot(r,N),0.0,1.0),r*d,d);
    return r;
}
vec2 field(vec2 uv) {
    vec2 mouse = (iMouse.x == 0. && iMouse.y==0.) ? vec2(-0.15,-0.1) : iMouse.xy;
    mouse*=3.0;
    vec2 p=
        swirl(uv, mouse,1.5,0.25)
        +spray(uv,-mouse,vec2(-1.0,0.5),0.5,0.1)
        +drain(uv,mouse,0.5,0.75)
    ;
    p=ReflectOffSurf(uv,p);
    return p;
}

//just basic clouds from perlin noise
float rand(vec2 co){return fract(sin(dot(co,vec2(12.9898,78.233)))*43758.5453);}
float noyz(vec2 co){
    vec2 d=smoothstep(0.0,1.0,fract(co));
    co=floor(co);
    const vec2 v=vec2(1.0,0.0);
    return mix(mix(rand(co),rand(co+v.xy),d.x),
        mix(rand(co+v.yx),rand(co+v.xx),d.x),d.y);
}
float clouds( in vec2 q, in float tm )
{
    float f=0.0,a=0.6;
    for(int i=0;i<5;i++){
            f+= a*noyz( q+tm );
        q = q*2.03;
        a = a*0.5;
    }
    return f;
}

float getPattern(vec2 uv) {
    //this can be any pattern but moving patterns work best
    float w=clouds(uv*5.0, iGlobalTime*0.5);
    return w;
}

vec2 calcNext(vec2 uv, float t) {
    t /= float(STEP_COUNT);
    for(int i = 0; i < STEP_COUNT; ++i) {
        uv -= field(uv)*t;
    }
    return uv;
}

vec3 heatmap(float h){
    return mix(vec3(0.1,0.2,0.4),vec3(2.0,1.5-h,0.5)/(1.0+h),h);
}

vec3 Fluid(vec2 uv, float t) {
    float t1 = t*0.5;
    float t2 = t1 + 0.5;
    vec2 uv1 = calcNext(uv, t1);
    vec2 uv2 = calcNext(uv, t2);
    float c1 = getPattern(uv1);
    float c2 = getPattern(uv2);
    float c=mix(c2,c1,t);
    float f=1.5-0.5*abs(t-0.5);
    c=pow(c,f)*f;//correcting the contrast/brightness when sliding
    float h=mix(length(uv-uv2),length(uv-uv1),t);
    return 2.0*c*heatmap(clamp(h*0.5,0.0,1.0));//blue means slow, red = fast
}

void main()
{
    vec2 uv = fragCoord;
    uv*=3.0;
    float t = fract(iGlobalTime);
    vec3 c = Fluid(uv,t);//draws fluid
    float d=DE(uv);//get distance to objects
    c=mix(vec3(1.0-10.0*d*d),c,smoothstep(0.2,0.25,d));//mix in objects
    gl_FragColor = vec4(c,1.0);
}

'''

program = gloo.Program(vertex, fragment, count=4)
program['a_position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
program['iGlobalTime'] = 0.0

window = app.Window(width=900, height=900)


@window.event
def on_draw(dt):
    window.clear()
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    program.draw(gl.GL_TRIANGLE_STRIP)
    program['iGlobalTime'] += dt


@window.event
def on_mouse_press(x, y, button):
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    program["iMouse"] = 2 * x / w - 1, 1 - 2 * y / h


@window.timer(1 / 5.0)
def timer(dt):
    window.set_title("time:{:5.1f}\tfps:{:3.1f}".format(program['iGlobalTime'][0], window.fps).encode())


app.run()
