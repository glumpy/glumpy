# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from . collection import Collection
from glumpy import gloo, gl, library
from glumpy.graphics.text import FontManager
from glumpy.transforms import Position, Viewport


class AggGlyphCollection(Collection):

    def __init__(self, transform=None, viewport=None, **kwargs):
        dtype = [('position',  (np.float32, 2), '!local', (0, 0)),
                 ('texcoord',  (np.float32, 2), '!local', (0, 0)),
                 ('offset',    (np.float32, 1), '!local', 0),
                 ('origin',    (np.float32, 3), 'shared', (0, 0, 0)),
                 ('color',     (np.float32, 4), 'shared', (0, 0, 0, 1))]

        if "vertex" in kwargs.keys():
            vertex = kwargs["vertex"]
            del kwargs["vertex"]
        else:
            vertex = library.get('collections/agg-glyph.vert')

        if "fragment" in kwargs.keys():
            fragment = kwargs["vertex"]
            del kwargs["vertex"]
        else:
            fragment = library.get('collections/agg-glyph.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32,
                            mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment)

        program = self._programs[0]

        if transform is not None:
            program["transform"] = transform
        else:
            program["transform"] = Position()

        if "viewport" in program.hooks:
            if viewport is not None:
                program["viewport"] = viewport
            else:
                program["viewport"] = Viewport()

        manager = FontManager()
        atlas = manager.atlas_agg
        self['atlas_data'] = atlas
        self['atlas_data'].interpolation = gl.GL_LINEAR
        self['atlas_shape'] = atlas.shape[1], atlas.shape[0]

    def append(self, text, font,
               anchor_x='center', anchor_y='center', **kwargs):
        """
        Append a new text to the collection

        text : str
            Text to be appended

        font : glumpy.graphics.font.Font
            Font to be used to render text

        anchor_x : str
            Text horizontal anchor ('left', 'center', 'right')

        anchor_y : str
            Text horizontal anchor ('top', 'center', 'bottom')
        """

        V, I = self.bake(text, font, anchor_x, anchor_y)

        defaults = self._defaults
        reserved = ["collection_index", "position", "texcoord", "offset"]
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

        Collection.append(self, vertices=V, indices=I, uniforms=U)

    def bake(self, text, font, anchor_x='center', anchor_y='center'):
        """ Bake a text string to be added in the collection """

        n = len(text) - text.count('\n')
        indices = np.zeros((n, 6), dtype=self.itype)
        vertices = np.zeros((n, 4), dtype=self.vtype)

        # Current line start index
        start = 0
        # Pen position
        pen = [0, 0]
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
                lines.append(((start, index), pen[0]))
                start = index
                text_width = max(text_width, pen[0])
                pen[1] -= font.height
                pen[0] = 0
                # Actual glyph
            else:
                glyph = font[charcode]
                kerning = glyph.get_kerning(prev)
                x0 = pen[0] + glyph.offset[0] + kerning
                offset = x0-int(x0)
                x0 = int(x0)
                y0 = pen[1] + glyph.offset[1]
                x1 = x0 + glyph.shape[0]
                y1 = y0 - glyph.shape[1]
                u0, v0, u1, v1 = glyph.texcoords
                vertices[index]['position'] = ((x0, y0), (x0, y1),
                                               (x1, y1), (x1, y0))
                vertices[index]['texcoord'] = ((u0, v0), (u0, v1),
                                               (u1, v1), (u1, v0))
                vertices[index]['offset'] = offset
                indices[index] = index*4
                indices[index] += np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
                pen[0] = pen[0]+glyph.advance[0]/64. + kerning
                pen[1] = pen[1]+glyph.advance[1]/64.
                prev = charcode
                index += 1

        lines.append(((start, index+1), pen[0]))
        text_height = (len(lines)-1)*font.height
        text_width = max(text_width, pen[0])

        # Adjusting each line
        for ((start, end), width) in lines:
            if anchor_x == 'right':
                dx = -width/1.0
            elif anchor_x == 'center':
                dx = -width/2.0
            else:
                dx = 0
            vertices[start:end]['position'] += round(dx), 0

        # Adjusting whole label
        if anchor_y == 'top':
            dy = - (font.ascender + font.descender)
        elif anchor_y == 'center':
            dy = (text_height - (font.descender + font.ascender))/2
        elif anchor_y == 'bottom':
            dy = -font.descender + text_height
        else:
            dy = 0
        vertices['position'] += 0, round(dy)
        vertices = vertices.ravel()
        indices = indices.ravel()
        return vertices, indices

    def view(self, transform, viewport=None):
        """ Return a view on the collection using provided transform """

        return GlyphCollectionView(self, transform, viewport)


class GlyphCollectionView(object):

    def __init__(self, collection, transform=None, viewport=None):

        vertex = collection._vertex
        fragment = collection._fragment
        program = gloo.Program(vertex, fragment)

        if "transform" in program.hooks and transform is not None:
            program["transform"] = transform

        if "viewport" in program.hooks and viewport is not None:
            program["viewport"] = viewport

        program.bind(collection._vertices_buffer)
        for name in collection._uniforms.keys():
            program[name] = collection._uniforms[name]

        collection._programs.append(program)
        self._program = program
        self._collection = collection

    def __getitem__(self, key):
        return self._program[key]

    def __setitem__(self, key, value):
        self._program[key] = value

    def draw(self):
        program = self._program
        collection = self._collection
        mode = collection._mode

        if collection._need_update:
            collection._update()
            # self._program.bind(self._vertices_buffer)

            if collection._uniforms_list is not None:
                program["uniforms"] = collection._uniforms_texture
                program["uniforms_shape"] = collection._ushape

        atlas = collection["atlas_data"]
        program['atlas_data'] = atlas
        program['atlas_data'].interpolation = gl.GL_LINEAR
        program['atlas_shape'] = atlas.shape[1], atlas.shape[0]

        if collection._indices_list is not None:
            program.draw(mode, collection._indices_buffer)
        else:
            program.draw(mode)
