# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, glm, gl

vertex = """
    attribute vec2 a_texcoord;
    attribute vec2 a_position;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
        v_texcoord = a_texcoord;
    } """

fragment = """
    uniform vec2  u_size;
    uniform vec2  u_translate;
    uniform float u_scale;
    uniform vec4  u_grid_color;
    uniform float u_grid_thickness;
    uniform float u_grid_antialias;

    varying vec2 v_texcoord;

    float
    distance_to_line(vec2 P1, vec2 P2, vec2 P3)
    {
        float u = (P3.x-P1.x)*(P2.x-P1.x) + (P3.y-P1.y)*(P2.y - P1.y);
        u /= (P2.x-P1.x)*(P2.x-P1.x) + (P2.y-P1.y)*(P2.y-P1.y);
        vec2 P = P1 + u*(P2-P1);
        return sqrt( (P.x-P3.x)*(P.x-P3.x) +(P.y-P3.y)*(P.y-P3.y) );
    }

    void main()
    {
        float R = 16.0*u_scale;
        float S = 1.5*R;
        float W = 2.0*R;
        float H = sqrt(3.0)*R;

        float i,j;
        float x = v_texcoord.x * u_size.x - u_translate.x;
        float y = v_texcoord.y * u_size.y - u_translate.y;

        i = floor(x/S);
        j = floor((y - mod(i,2.0)*H/2.0)/H );
        float cy0 = j*H + H/2. *(1.0 + mod(i,2.0));
        float cx0 = i*S + W/2.;

        i = floor(x/S) - 1.;
        j = floor((y - mod(i,2.0)*H/2.0)/H );
        float cy1 = j*H + H/2. *(1.0 + mod(i,2.0));
        float cx1 = i*S + W/2.;

        float t = u_grid_thickness/2.0-u_grid_antialias;
        float radius = R*.85;

        float X = abs(x-cx0);
        float Y = abs(y-cy0);
        float d0 = abs(Y-H/2.);
        float d1 = distance_to_line( vec2(W/4.,H/2.), vec2(W/2., 0.0), vec2(X,Y));
        if (X > (W-S))
        {
            d0=2.*d1;
        }


        float temp=y; y=x; x=temp;
        x = (x - H/2.) / H;
        float t1 = y / R;
        float t2 = floor(x + t1);
        float r = floor((floor(t1 - x) + t2) / 3.);
        float q = floor((floor(2. * x + 1.) + t2) / 3.) - r;
        r = floor(r);
        q = floor(q);
        vec4 color = vec4(min(q/10.0,1.0), min(r/10.0,1.0), 0.0, 1.0);

        float d = min(d0,d1)-t;
        if( d < 0.0 )
        {
            gl_FragColor = u_grid_color;
        }
        else
        {
            float alpha = d/u_grid_antialias;
            alpha = exp(-alpha*alpha);
            //gl_FragColor = vec4(u_grid_color.rgb, alpha) + (1.-alpha)*color;
            gl_FragColor = vec4(u_grid_color.rgb, alpha);
        }

    }
"""


window = app.Window(width=512, height=512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    program['u_size'] = width, height

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    translate = [translate[0] + dx, translate[1] - dy]
    program['u_translate'] = translate

@window.event
def on_mouse_scroll(x, y, dx, dy):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y

    s = min(max(0.25, scale + .01 * dy * scale), 200)
    translate[0] = x - s * (x - translate[0]) / scale
    translate[1] = y - s * (y - translate[1]) / scale
    translate = [translate[0], translate[1]]
    scale = s
    program['u_translate'] = translate
    program['u_scale'] = scale


program = gloo.Program(vertex, fragment, count=4)
program['a_position'] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
program['a_texcoord'] = ( 0, 0), ( 0,+1), (+1, 0), (+1,+1)
program['u_grid_color'] = 0,0,0,1
program['u_grid_thickness'] = 1
program['u_grid_antialias'] = 1
program['u_translate'] = 0,0
program['u_scale'] = 1.0
program['u_size'] = 512,512
translate = [0, 0]
scale = 1

app.run()
