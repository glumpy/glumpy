# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np

from glumpy import gl
from glumpy.shaders import get_file, get_code
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection
from glumpy.gloo.program import Program, VertexBuffer, IndexBuffer



class GlyphCollection(Collection):
    """ """

    # This cannot be changed (shader code depends on it)
    dtypes = [ ('position',  np.float32, 2),
               ('texcoord',  np.float32, 2),
               ('color',     np.float32, 4) ]

    # Default variable scopes
    scopes = { 'position'   : '!local',
               'texcoord'   : '!local',
               'color'      : 'shared' }

    # Default variable values
    defaults = { 'position' : (0,0),
                 'texcoord' : (0,0),
                 'color'    : (0,0,0,1) }


    def __init__(self, **kwargs):
        """ """

        # Extend dtypes with user argument
        dtypes = list(GlyphCollection.dtypes)
        if "dtypes" in kwargs.keys():
            dtypes.extend(kwargs.get("dtypes", []))
            del kwargs["dtypes"]
        scopes = dict(GlyphCollection.scopes)

        # Initialize collection
        Collection.__init__(self, dtypes, scopes, itype=np.uint32, **kwargs)

        # Set draw mode
        self._mode = gl.GL_TRIANGLES

        # Build program
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        vertex += get_code('sdf-glyph.vert')
        fragment = ""
        fragment += get_code("spatial-filters.frag")
        fragment += get_code('sdf-glyph.frag')

        self._program = Program(vertex, fragment)
        for name in self._uniforms.keys():
            self._uniforms[name] = GlyphCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]
        self._build_buffers()



    def append(self, text, font, anchor_x='center', anchor_y='center', **kwargs):
        """ """

        defaults = GlyphCollection.defaults
        V,I = self.bake(text, font, anchor_x, anchor_y)

        reserved = ["a_uniform_index", "position", "texcoord"]
        for name in self.vtype.names:
            if name not in reserved:
                if name in kwargs.keys() or name in defaults.keys():
                    V[name] = kwargs.get(name, defaults[name])

        if self.utype:
            U = np.zeros(1, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    if name in kwargs.keys() or name in defaults.keys():
                        U[name] = kwargs.get(name, defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, indices=I ,uniforms=U)


    def bake(self, text, font, anchor_x='center', anchor_y='center'):
        """ """

        n = len(text) - text.count('\n')
        indices = np.zeros((n,6), dtype=self.itype)
        vertices = np.zeros((n,4), dtype=self.vtype)

        # Current line start index
        start = 0
        # Pen position
        pen = [0,0]
        # Previous glyph
        prev = None
        # Lines (as start/end index and width (pixels)
        lines = []
        # Maximum text width and total height
        text_width, text_height = 0, 0

        index = 0
        for charcode in text:

            # Line feed
            if charcode == '\n':
                prev = None
                lines.append( ((start, index), pen[0]) )
                start = index
                text_width = max(text_width,pen[0])
                pen[1] -= font.height
                pen[0] = 0
                # Actual glyph
            else:
                glyph = font[charcode]
                kerning = glyph.get_kerning(prev)
                x0 = pen[0] + glyph.offset[0] + kerning
                y0 = pen[1] + glyph.offset[1]
                x1 = x0 + glyph.shape[1]
                y1 = y0 - glyph.shape[0]
                u0, v0, u1, v1 = glyph.texcoords
                vertices[index]['position'] = (x0,y0),(x0,y1),(x1,y1),(x1,y0)
                vertices[index]['texcoord'] = (u0,v0),(u0,v1),(u1,v1),(u1,v0)
                indices[index] = index*4
                indices[index] += 0,1,2, 0,2,3
                pen[0] = pen[0]+glyph.advance[0] + kerning
                pen[1] = pen[1]+glyph.advance[1]
                prev = charcode
                index += 1

        lines.append( ((start, index+1), pen[0]) )
        text_height = (len(lines)-1)*font.height
        text_width = max(text_width,pen[0])

        # Adjusting each line
        for ((start, end), width) in lines:
            if anchor_x == 'right':
                dx = -width/1.0
            elif anchor_x == 'center':
                dx = -width/2.0
            else:
                dx = 0
            vertices[start:end]['position'] += dx,0

        # Adjusting whole label
        if anchor_y == 'top':
            dy = - (font.ascender + font.descender)
        elif anchor_y == 'center':
            dy = (text_height - (font.descender + font.ascender))/2
        elif anchor_y == 'bottom':
            dy = -font.descender + text_height
        else:
            dy = 0
        vertices['position'] += 0, dy

        vertices = vertices.ravel()
        indices  = indices.ravel()

        return vertices.view(VertexBuffer), indices.view(IndexBuffer)
