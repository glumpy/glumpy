#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from PIL import Image

import glumpy as gp
import glumpy.gl as gl



class PanZoom(gp.transforms.TranslateScale):

    def __init__(self):
        gp.transforms.TranslateScale.__init__(self)
        self.scale     = np.array([1.,1.,1.])
        self.translate = np.array([0.,0.,0.])

    def on_resize(self, width, height):
        self.width, self.height = float(width), float(height)
        ratio = self.width/self.height
        if ratio > 1.0:
            self.aspect = 1.0/ratio, 1.0, 1.0
        else:
            self.aspect = 1.0, ratio/1.0, 1.0
        self["scale"] = self.scale * self.aspect

    def on_mouse_scroll(self, x, y, dx, dy):
        x = x/(self.width/2) - 1
        y = 1 - y/(self.height/2)
        s = np.minimum(np.maximum(self.scale*(1+dy/100), 0.1), 100)
        self.translate[0] = x - s[0] * (x - self.translate[0]) / self.scale[0]
        self.translate[1] = y - s[1] * (y - self.translate[1]) / self.scale[1]
        self.scale = s
        self["scale"] = self.scale * self.aspect
        self["translate"] = self.translate

    def on_mouse_drag(self, x, y, dx, dy, button):
        self.translate += (2*dx/self.width, -2*dy/self.height,0)
        self["translate"] = self.translate

    def reset(self):
        self.scale = np.array([1.,1.,1.])
        self.translate = np.array([0.,0.,0.])
        self["scale"] = self.aspect * np.array([1.,1.,1.])
        self["translate"] = np.array([0.,0.,0.])


vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = transform(vec4(position, 0.0, 1.0));
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""

window = gp.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_key_press(key, modifiers):
    if key == gp.app.window.key.SPACE:
        transform.reset()


transform = PanZoom()
program = gp.gloo.Program(transform.code + vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture'] = np.array(Image.open("lena.png"))


transform.attach(program)
window.attach(transform)

gp.run()
