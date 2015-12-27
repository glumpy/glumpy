# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
import numpy as np
import glumpy.gl as gl
import glumpy.gloo as gloo
from glumpy.log import log


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
uniform sampler2D original;
uniform sampler2D filtered;
uniform vec2 texsize;
varying vec2 v_texcoord;
void main()
{
    gl_FragColor = <filter>;
}
"""


class Filter(object):
    """ Post-processing filter """

    def __init__(self, width, height, *args):

        # We need 3 framebuffers:
        # 1 is used to store original rendering
        # 2 & 3 are used for ping-pong rendering
        #  -> gives 2 as input, render in 3
        #  -> gives 3 as input, render in 2
        #  -> ...
        self._framebuffers = []
        for i in range(3):
            depth = gloo.DepthBuffer(width, height)
            # depth = np.zeros((height,width),np.float32).view(gloo.DepthTexture)
            color = np.zeros((height,width,3),np.float32).view(gloo.Texture2D)
            framebuffer = gloo.FrameBuffer(color=color, depth=depth)
            self._framebuffers.append(framebuffer)

        # Build filter programs
        self._build_programs(*args)
        self._viewport = 0, 0, width, height


    def _build_programs(self, *args):
        """ Build all filter programs """

        index = 0
        self._programs = []

        # We add an extra do-nothing program for unfiltered rendering because
        # it will be rendered at original viewport size and we want all filters
        # to use the same framebuffer size.
        args = list(args) + ["texture2D(filtered, v_texcoord)"]

        for i,code in enumerate(args):
            if not isinstance(code,gloo.Snippet):
                snippet = gloo.Snippet(code)
            else:
                snippet = code
            program = gloo.Program(vertex, fragment, count=4)
            program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
            program['texcoord'] = [(0, 0), (0, 1), (1, 0), (1, 1)]
            program['original'] = self._framebuffers[0].color[0]
            program['original'].interpolation = gl.GL_LINEAR
            program['filtered'] = self._framebuffers[index].color[0]
            program['filtered'].interpolation = gl.GL_LINEAR
            program['texsize'] = self.width, self.height
            if i < len(args)-1:
                original_snippet = snippet
                # Walk through snippet arguments to fill last one
                while len(snippet.args) > 0:
                    if len(snippet.args) > 1:
                        raise ValueError("Filter snippet cannot have more than 1 argument")
                    elif not isinstance(snippet.args[0], gloo.Snippet):
                        raise ValueError("Filter snippet argument must be a Snippet")
                    else:
                        snippet = snippet.args[0]
                snippet._args = "original", "filtered", "v_texcoord", "texsize"
                program['filter'] = original_snippet
            else:
                program['filter'] = code
            self._programs.append(program)
            index = (index+1)%2


    @property
    def width(self):
        return self._framebuffers[0].width


    @property
    def height(self):
        return self._framebuffers[0].height


    @property
    def viewport(self):
        return self._viewport


    @viewport.setter
    def viewport(self, xywh):
        (x, y, width, height) = xywh
        self._viewport = x, y, width, height


    def __getitem__(self, name):
        for program in self._programs:
            snippet = program["filter"]
            if isinstance(snippet, gloo.Snippet) and name in snippet.globals.keys():
                return snippet[name]
            if name in program.keys():
                return program[name]
        raise IndexError("Unknown uniform or attribute")

    def __setitem__(self, name, value):
        for program in self._programs:
            snippet = program["filter"]
            if isinstance(snippet, gloo.Snippet) and name in snippet.globals.keys():
                snippet[name] = value
                return
            if name in program.keys():
                program[name] = value
                return
        raise IndexError("Unknown uniform or attribute")


    def __enter__(self):
        # Save viewport for final rendering
        self._viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)

        # Prepare framebuffer for "original" rendering
        gl.glViewport(0, 0, self.width, self.height)
        self._framebuffers[0].activate()


    def __exit__(self, type, value, traceback):
        # Done with "original" rendering
        self._framebuffers[0].deactivate()

        # Actual filtering starts here
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDisable(gl.GL_DEPTH_TEST)

        # Apply all filters using ping-pong framebuffers
        index = 0
        for i in range(len(self._programs)-1):
            program = self._programs[i]
            if i == 0: # special case for first rendering
                program['filtered'] = self._framebuffers[0].color[0]
            else:
                program['filtered'] = self._framebuffers[1+index].color[0]
            index = (index + 1) % 2 # ping-pong
            self._framebuffers[index+1].activate()
            self._programs[i].draw(gl.GL_TRIANGLE_STRIP)
            self._framebuffers[index+1].deactivate()

        # Final rendering (no transformation) at original viewport size
        program = self._programs[-1]
        program['filtered'] = self._framebuffers[index+1].color[0]
        gl.glViewport( *self._viewport )
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDisable(gl.GL_DEPTH_TEST)
        program.draw(gl.GL_TRIANGLE_STRIP)
