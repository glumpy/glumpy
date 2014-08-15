#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import datetime
import numpy as np
from glumpy import app, gl, gloo
from glumpy.ext.ffmpeg_reader import FFMPEG_VideoReader

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
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

reader = FFMPEG_VideoReader("ImaginaryForces.mp4")
width,height = reader.infos["video_size"]
duration = reader.infos["duration"]

time = 0
window = app.Window(2*width, 2*height)

@window.event
def on_draw(dt):
    global time
    window.clear()
    time = np.mod(time+dt, duration)
    program['texture'][...] = reader.get_frame(time)
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture'] = np.zeros((height,width,3), dtype=np.uint8)
app.run()
