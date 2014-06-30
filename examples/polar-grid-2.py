#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo

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
    #version 120

    const float M_PI = 3.14159265358979323846;

    float
    compute_alpha(float d, float width, float antialias)
    {
        d -= width/2.0 - antialias;
        if( d < 0.0 )
        {
            return 1.0;
        }
        else
        {
            float alpha = d/antialias;
            return exp(-alpha*alpha);
        }
    }

    uniform vec2      u_viewport;
    uniform vec2      u_translate;
    uniform float     u_scale;
    uniform vec2      u_xlim;
    uniform vec2      u_ylim;
    uniform float     u_antialias;
    uniform float     u_major_grid_width;
    uniform float     u_minor_grid_width;
    uniform vec4      u_major_grid_color;
    uniform vec4      u_minor_grid_color;
    uniform sampler2D u_grid;

    varying vec2 v_texcoord;
    void main()
    {
        vec2 P = (v_texcoord - 2*(u_translate/u_viewport.x)) /u_scale;
        float radius = u_viewport.x/2.0 * u_scale;

        // Normalized y limits
        float ymin = u_ylim.x / u_ylim.y;
        float ymax = 1.0;

        // Normalized rho over[0,1]
        float rho = length(P);

        // Epsilon is used for ensuring at least linewidth outsize main area
        float epsilon = (u_major_grid_width/2.0 + u_antialias)/radius;
        if( (rho < ymin-epsilon) || (rho > ymax+epsilon) )
        {
            discard;
        }

        bool outside = false;

        // Angle check
        float theta = atan(P.y,P.x);
        if( theta < 0)
            theta = 2*M_PI+theta;

        // If we are very close to the upper limit (2pi), we take theta
        // complement such as to get the right distance from texture.
        epsilon = 1 * M_PI/180.0;
        if (theta > (2*M_PI - epsilon))
        {
            theta = 2*M_PI - theta;
//            outside = true;
        }


        epsilon = 1 * M_PI/180.0;
        if ( (theta < (u_xlim.x-epsilon)) || (theta > (u_xlim.y+epsilon)) )
        {
            discard;
        }

        // Renormalized rho over [ymin,ymax]
        float u = (rho - ymin) / (ymax-ymin);

        // Get nearest normalized major line
        float t = texture2D(u_grid, vec2(u,0.5)).x;
        t = (t - u_ylim.x) / (u_ylim.y - u_ylim.x);
        float My = abs(u-t) * (1.0-ymin) * radius;

        // Get nearest normalized minor line
        t = texture2D(u_grid, vec2(u,0.5)).y;
        t = (t - u_ylim.x) / (u_ylim.y - u_ylim.x);
        float my = abs(u-t) * (1.0-ymin) * radius;


        t = theta/(2*M_PI);
        float Tx = 2*M_PI*(texture2D(u_grid, vec2(t,0.5)).z/360000.0 - 1.0);
        float tx = 2*M_PI*(texture2D(u_grid, vec2(t,0.5)).w/360000.0 - 1.0);
        float Mx = abs(sin(theta-Tx) * (rho * radius));
        float mx = abs(sin(theta-tx) * (rho * radius));

        float M = My;
        float m = my;

        if( (rho < ymin) && (rho > ymax) )
        {
            M = My;
            m = my;
        }

        // This test avoid circular lines to go outside limits
        // The external area is reserved for antaliasing start or ending lines
        else if ( ((theta < u_xlim.x) || (theta > u_xlim.y)) || outside )
        {
            M = Mx;
            m = mx;
        }

        // This test avoid straight lines to go outside limits
        // The external area is reserved for antaliasing inner or outer circle
        else if( (rho >= ymin) && (rho <= ymax) )
        {
            M = min(Mx,My);
            m = min(mx,my);
        }


        vec4 color = u_major_grid_color;
        float alpha1 = compute_alpha( M, u_major_grid_width, u_antialias);
        float alpha2 = compute_alpha( m, u_minor_grid_width, u_antialias);
        float alpha  = alpha1;
        if( alpha2 > alpha1*1.5 )
        {
            alpha = alpha2;
            color = u_minor_grid_color;
        }
        gl_FragColor = vec4(color.xyz, alpha*color.a);

    }
    """


def find_closest(A, target):
    # A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A) - 1)
    left = A[idx - 1]
    right = A[idx]
    idx -= target - left < right - target
    return idx

def find_closest_direct(I, start, end, count):
    Q = (I-start)/(end-start)*count
    mid = ((Q[1:]+Q[:-1]+1)/2).astype(np.int)
    boundary = np.zeros(count, np.int)
    boundary[mid] = 1
    return np.add.accumulate(boundary)

def update_grid(w, h):

    n = Z.shape[1]

    ymin, ymax = ylim
    t1 = major_grid[0]
    t2 = minor_grid[0]

    I1 = np.linspace(ymin, ymax, (ymax-ymin)/t1+1, endpoint=True)
    Z[..., 0] = I1[find_closest_direct(I1, start=ymin, end=ymax, count=n)]

    I2 = np.linspace(ymin, ymax, (ymax-ymin)/t2+1, endpoint=True)
    Z[..., 1] = I2[find_closest_direct(I2, start=ymin, end=ymax, count=n)]

    xmin, xmax = 0,360000
    t1 = major_grid[1]*1000
    t2 = minor_grid[1]*1000

    I3 = np.linspace(xmin, xmax, (xmax-xmin)/t1, endpoint=False)
    Z[..., 2] = I3[find_closest_direct(I3, start=xmin, end=xmax, count=n)]

    I4 = np.linspace(xmin, xmax, (xmax-xmin)/t2, endpoint=False)
    Z[..., 3] = I4[find_closest_direct(I4, start=xmin, end=xmax, count=n)]

    program['u_grid'][...] = Z
    program['u_viewport'] = w, h



window = app.Window(width=1024, height=1024)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    update_grid(width, height)

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    translate = [translate[0] + dx, translate[1] - dy]
    program['u_translate'] = translate
    update_grid(w, h)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y

    x -= w/2
    y -= h/2

    s = min(max(0.25, scale + .01 * dy * scale), 200)
    translate[0] = x - s * (x - translate[0]) / scale
    translate[1] = y - s * (y - translate[1]) / scale
    translate = [translate[0], translate[1]]
    scale = s
    program['u_translate'] = translate
    program['u_scale'] = scale
    update_grid(w, h)


program = gloo.Program(vertex, fragment, 4)
program['a_position'] = (-1, -1), (-1, +1), (+1, -1), (+1, +1)
program['a_texcoord'] = (-1, -1), (-1, +1), (+1, -1), (+1, +1)
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5

scale = 1
translate = [0,0]
xlim = 0*np.pi/180.0, 360*np.pi/180.0
ylim = 1,3

major_grid = np.array([1.00,  30.0])
minor_grid = np.array([0.10,   3.0])

program['u_xlim'] = xlim
program['u_ylim'] = ylim
program['u_scale'] = scale
program['u_translate'] = translate


program['u_antialias'] = 1.0
program['u_viewport'] = window.width, window.height
Z = np.zeros((1, 2 * 1024, 4), dtype=np.float32)
program['u_grid'] = Z
program['u_grid'].interpolation = gl.GL_NEAREST


gl.glClearColor(1, 1, 1, 1)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

app.run()
