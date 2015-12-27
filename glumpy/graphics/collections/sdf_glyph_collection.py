# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from . collection import Collection
from glumpy import gl, data, library
from glumpy.graphics.text import FontManager
from glumpy.transforms import Position, Viewport



class SDFGlyphCollection(Collection):

    def __init__(self, transform=None, viewport=None, **kwargs):
        dtype = [('position',  (np.float32, 2), '!local', (0,0)),
                 ('texcoord',  (np.float32, 2), '!local', (0,0)),
                 ('origin',    (np.float32, 3), 'shared', (0,0,0)),
                 ('direction', (np.float32, 3), 'shared', (1,0,0)),
                 ('scale',     (np.float32, 1), 'shared', 0.005),
                 ('color',     (np.float32, 4), 'shared', (0,0,0,1))]

        if "vertex" in kwargs.keys():
            vertex = library.get(kwargs["vertex"])
            del kwargs["vertex"]
        else:
            vertex = library.get('collections/sdf-glyph.vert')

        if "fragment" in kwargs.keys():
            fragment = library.get(kwargs["fragment"])
            del kwargs["fragment"]
        else:
            fragment = library.get('collections/sdf-glyph.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32,
                            mode = gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment)
        program = self._programs[0]
        if transform is not None:
            program["transform"] = transform
#        else:
#            program["transform"] = Position()

        if "viewport" in program.hooks:
            if viewport is not None:
                program["viewport"] = viewport
            else:
                program["viewport"] = Viewport()


        manager = FontManager()
        atlas = manager.atlas_sdf
        self['u_kernel'] = data.get("spatial-filters.npy")
        self['atlas_data'] = atlas
        self['atlas_data'].interpolation = gl.GL_LINEAR
        self['atlas_shape'] = atlas.shape[1], atlas.shape[0]


    def append(self, text, font, anchor_x='center', anchor_y='center', **kwargs):
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
        reserved = ["collection_index", "position", "texcoord"]
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
        """ Bake a text string to be added in the collection """

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
                indices[index] += np.array([0,1,2,0,2,3], dtype=np.uint32)
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

        return vertices, indices
        # return vertices.view(VertexBuffer), indices.view(IndexBuffer)
