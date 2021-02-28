# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm
from glumpy.transforms import TrackballPan, Position

vertex = """
#version 120
uniform float linewidth;
uniform float antialias;
attribute vec4  fg_color;
attribute vec4  bg_color;
attribute float radius;
attribute vec3  position;
varying float v_pointsize;
varying float v_radius;
varying float v_z;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
void main (void)
{
    v_radius = radius;
    v_fg_color = fg_color;
    v_bg_color = bg_color;
    gl_Position = <transform>;
    v_z = gl_Position.z;
    gl_PointSize = 2 * (v_radius + linewidth + 1.5*antialias);
}
"""

fragment = """
#version 120
uniform float linewidth;
uniform float antialias;
varying float v_radius;
varying float v_z;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
float marker(vec2 P, float size)
{
   const float SQRT_2 = 1.4142135623730951;
   float x = SQRT_2/2 * (P.x - P.y);
   float y = SQRT_2/2 * (P.x + P.y);
   float r1 = max(abs(x)- size/2, abs(y)- size/10);
   float r2 = max(abs(y)- size/2, abs(x)- size/10);
   float r3 = max(abs(P.x)- size/2, abs(P.y)- size/10);
   float r4 = max(abs(P.y)- size/2, abs(P.x)- size/10);
   return min( min(r1,r2), min(r3,r4));
}
void main()
{
    float r = (v_radius + linewidth + 1.5*antialias);
    float t = linewidth/2.0 - antialias;
    float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5)) * 2 * r - v_radius;
  //  float signed_distance = marker((gl_PointCoord.xy - vec2(0.5,0.5))*r*2, 2*v_radius);

    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    vec2 p = (gl_PointCoord.xy - vec2(0.5, 0.5)) * 2;
    float len_p = length(p);
    // gl_FragDepth = 0.5 * v_z  + 0.5* (len_p);
    vec3 normal = normalize(vec3(p.xy, 1.0 - len_p));
    vec3 direction = normalize(vec3(1.0, 1.0, 1.0));
    float diffuse = max(0.0, dot(direction, normal));
    float specular = pow(diffuse, 24.0);
    vec4 bg_color = vec4(max(diffuse*v_bg_color.rgb, specular*vec3(1.0)), 1);

    // Inside shape
    if( signed_distance < 0 ) {
        // Fully within linestroke
        if( border_distance < 0 ) {
             gl_FragColor = v_fg_color;
        } else {
            gl_FragColor = mix(bg_color, v_fg_color, alpha);
        }
    // Outside shape
    } else {
        discard;
        // Fully within linestroke
        if( border_distance < 0 ) {
            gl_FragColor = v_fg_color;
        } else if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            gl_FragColor = vec4(v_fg_color.rgb, v_fg_color.a * alpha);
        } else {
            discard;
        }
    }
}
"""

theta, phi = 0,0
window = app.Window(width=800, height=800, color=(1,1,1,1))


n = 100
program = gloo.Program(vertex, fragment, count=n)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)

program['position'] = 0.35 * np.random.randn(n,3)
program['radius']   = 5 * np.ones(n) #np.random.uniform(5,10,n)
program['fg_color'] = 0,0,0,1
colors = np.random.uniform(0.75, 1.00, (n, 4))
colors[:,3] = 1
program['bg_color'] = colors
program['linewidth'] = 0.0
program['antialias'] = 0.0


# create an instance of the TrackballPan object.
trackball = TrackballPan(Position("position"), znear=3, zfar=10, distance=5)
program['transform'] = trackball

trackball.aspect = 1
# rotation around the X axis
trackball.phi = 0
# rotation around the Y axis
trackball.theta = 0
trackball.zoom = 50


@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

@window.event
def on_key_press(symbol, modifiers):
    pass
    # if (symbol == app.window.key.RIGHT):
    #     trackball.view_x += 0.1
    # elif (symbol ==  app.window.key.LEFT):
    #     trackball.view_x -= 0.1
    # elif (symbol == app.window.key.UP):
    #     trackball.view_y += 0.1
    # elif (symbol == app.window.key.DOWN):
    #     trackball.view_y -= 0.1


# @window.event
# def on_mouse_scroll(mouse_x, mouse_y, scroll_dx, scroll_dy):
#     view = np.array(program['view']).reshape(4,4)
#     glm.translate(view, 0, 0, scroll_dy)
#     program['view'] = view

    # old_zoom_size = zoom_size
    # zoom_size += 0.01 * scroll_dy
    # V["radius"] *= zoom_size / old_zoom_size

    # draw_offset += -0.01 * scroll_dx


@window.event
def on_character(character):
    if (character in '+='):
        program['radius'] += 0.5
    elif (character in "-_"):
        program['radius']  -= 0.5
    # if (character in "dD"):
    #     trackball.view_x += 0.1
    # elif (character in "aA"):
    #     trackball.view_x -= 0.1
    # elif (character in "wW"):
    #     trackball.view_y += 0.1
    # elif (character in "sS"):
    #     trackball.view_y -= 0.1
    # elif (character in " eE"):
    #     trackball.zoom += 1
    # elif (character in "qQ"):
    #     trackball.zoom -= 1

    # view = np.array(program['view']).reshape(4,4)
    # glm.translate(view, *amount_to_translate)
    # program['view'] = view
    

    # global stepsize, frame_idx, draw_offset
    # if (character == "r"):
    #     frame_idx = 0
    #     stepsize = 0
    # elif (character in ".>"):
    #     frame_idx += 1
    # elif (character in ",<"):
    #     frame_idx -= 1
    # elif (character == "R"):
    #     draw_offset = 0
    # elif (character in  ["+", "="] ):
    #     V["radius"] *= 1.1
    # elif (character in ["-", "_"]):
    #     V["radius"] *= 1/1.1
    # elif (character in "dD"):
    #     draw_offset += 0.1
    # elif (character in "aA"):
    #     draw_offset -= 0.1

window.attach(program["transform"])

gl.glEnable(gl.GL_DEPTH_TEST)
app.run()