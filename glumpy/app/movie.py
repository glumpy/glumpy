# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Dzhelil S. Rufat
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
A module for reading and writing movies.
"""
import contextlib
import numpy as np

from glumpy import gl
from glumpy.ext.ffmpeg_writer import FFMPEG_VideoWriter


@contextlib.contextmanager
def record(window, filename, fps):
    '''
    Record an animated window to a movie file.

    :param window: window that is being recorded.
    :param filename: name of the file to write the movie to.
    :param fps: framerate at which to record.
    '''

    writer = FFMPEG_VideoWriter(filename, (window.width, window.height), fps=fps)
    fbuffer = np.zeros((window.height, window.width, 3), dtype=np.uint8)

    # Function to write one frame
    def write_frame(writer):
        gl.glReadPixels(0, 0, window.width, window.height,
                        gl.GL_RGB, gl.GL_UNSIGNED_BYTE, fbuffer)
        writer.write_frame(np.flipud(fbuffer))

    # Modify the on_draw event handler to also write a
    # movie frame every time it is called
    old_on_draw = window.get_handler('on_draw')
    @window.event
    def on_draw(dt):
        old_on_draw(dt)
        write_frame(writer)

    yield

    writer.close()
