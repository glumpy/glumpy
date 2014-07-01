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



class PanZoom(object):
    """ A pan zoom transform  """

    def __init__(self):
        self.tr_scale     = gp.transforms.LinearScale()
        self.tr_translate = gp.transforms.Translate()
        self.tr_all       = self.tr_translate + self.tr_scale
        self._scale       = np.array([1.,1.,1.])
        self._translate   = np.array([0.,0.,0.])

    @property
    def code(self):
        return self.tr_all.code

    def attach(self, program):
        self.tr_all.attach(program)

    def on_resize(self, width, height):
        self._width, self._height = float(width), float(height)
        ratio = self._width/self._height
        if ratio > 1.0:
            self._aspect = 1.0/ratio, 1.0, 1.0
        else:
            self._aspect = 1.0, ratio/1.0, 1.0
        self.tr_scale.scale = self._scale * self._aspect

    def on_mouse_scroll(self, x, y, dx, dy):
        x = x/(self._width/2) - 1
        y = 1 - y/(self._height/2)
        s = np.minimum(np.maximum(self._scale*(1+dy/100), 0.1), 100)
        t = self._translate
        t[0] = x - s[0] * (x - t[0]) / self._scale[0]
        t[1] = y - s[1] * (y - t[1]) / self._scale[1]
        self._scale = s
        self._translate = t
        self.tr_scale.scale = self._scale * self._aspect
        self.tr_translate.translate = t

    def on_mouse_drag(self, x, y, dx, dy, button):
        dx /= self._width/2
        dy /= self._height/2
        self._translate += (dx,-dy,0) #/self._scale
        self.tr_translate.translate = self._translate


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


transform = PanZoom()
program = gp.gloo.Program(transform.code + vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture'] = np.array(Image.open("lena.png"))
transform.attach(program)
window.attach(transform)

gp.run()
