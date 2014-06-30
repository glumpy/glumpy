# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.log import log
from glumpy.ext import freetype
from glumpy.gloo.atlas import Atlas


# Default texture atlas
__atlas__ = None


class TextureFont:

    def __init__(self, filename, size, atlas = None):
        '''
        Initialize font

        Parameters:
        -----------

        atlas: Atlas
            Texture atlas where glyph texture will be stored

        filename: str
            Font filename

        size : float
            Font size
        '''
        global __atlas__

        if atlas is not None:
            self.atlas = atlas
        else:
            if __atlas__ is None:
                __atlas__ = np.zeros((512,512,3), dtype=np.ubyte).view(Atlas)
                #__atlas__ = Atlas(data, store=False)
            self.atlas = __atlas__

        self.filename = filename
        self.size = size
        self.glyphs = {}
        face = freetype.Face(self.filename)
        face.set_char_size( int(self.size*64))
        metrics = face.size
        self.ascender  = metrics.ascender/64.0
        self.descender = metrics.descender/64.0
        self.height    = metrics.height/64.0
        self.linegap   = self.height - self.ascender + self.descender
        self.depth     = 3
        freetype.set_lcd_filter(freetype.FT_LCD_FILTER_LIGHT)


    def __getitem__(self, charcode):
        '''
        x.__getitem__(y) <==> x[y]
        '''
        if charcode not in self.glyphs.keys():
            self.load('%c' % charcode)
        return self.glyphs[charcode]


    def load(self, charcodes = ''):
        '''
        Build glyphs corresponding to individual characters in charcodes.

        Parameters:
        -----------

        charcodes: [str | unicode]
            Set of characters to be represented
        '''
        face = freetype.Face( self.filename )
        pen = freetype.Vector(0,0)
        hres = 100*72
        hscale = 1.0/100

        for charcode in charcodes:
            face.set_char_size( int(self.size * 64), 0, hres, 72 )
            matrix = freetype.Matrix( int((hscale) * 0x10000L), int((0.0) * 0x10000L),
                                      int((0.0)    * 0x10000L), int((1.0) * 0x10000L) )
            face.set_transform( matrix, pen )
            if charcode in self.glyphs.keys():
                continue

            flags = freetype.FT_LOAD_RENDER | freetype.FT_LOAD_FORCE_AUTOHINT
            flags |= freetype.FT_LOAD_TARGET_LCD

            face.load_char( charcode, flags )
            bitmap = face.glyph.bitmap
            left   = face.glyph.bitmap_left
            top    = face.glyph.bitmap_top
            width  = face.glyph.bitmap.width
            rows   = face.glyph.bitmap.rows
            pitch  = face.glyph.bitmap.pitch

            w = width/3
            h = rows
            # h+1,w+1 to have a black border
            region = self.atlas.allocate( (h+1,w+1) )
            if region is None:
                log.warn("Cannot store glyph '%c'" % charcode)
                continue

            x,y,_,_ = region
            # sould be y+h+1,x+w+1 but we skip the black border
            texture = self.atlas[y:y+h,x:x+w]
            data = []
            for i in range(rows):
                data.extend(bitmap.buffer[i*pitch:i*pitch+width])
            data = np.array(data,dtype=np.ubyte).reshape(h,w,3)
            texture[...] = data

            # Build glyph
            size   = w,h
            offset = left, top
            advance= face.glyph.advance.x, face.glyph.advance.y

            u0     = (x +     0.0)/float(self.atlas.width)
            v0     = (y +     0.0)/float(self.atlas.height)
            u1     = (x + w - 0.0)/float(self.atlas.width)
            v1     = (y + h - 0.0)/float(self.atlas.height)
            texcoords = (u0,v0,u1,v1)
            glyph = TextureGlyph(charcode, size, offset, advance, texcoords)
            self.glyphs[charcode] = glyph

            # Generate kerning
            for g in self.glyphs.values():
                # 64 * 64 because of 26.6 encoding AND the transform matrix used
                # in texture_font_load_face (hres = 64)
                kerning = face.get_kerning(g.charcode, charcode,
                                           mode=freetype.FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    glyph.kerning[g.charcode] = kerning.x/(64.0*64.0)
                kerning = face.get_kerning(charcode, g.charcode,
                                           mode=freetype.FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    g.kerning[charcode] = kerning.x/(64.0*64.0)

            # High resolution advance.x calculation
            # gindex = face.get_char_index( charcode )
            # a = face.get_advance(gindex, FT_LOAD_RENDER | FT_LOAD_TARGET_LCD)/(64*72)
            # glyph.advance = a, glyph.advance[1]


class TextureGlyph:
    '''
    A texture glyph gathers information relative to the size/offset/advance and
    texture coordinates of a single character. It is generally built
    automatically by a TextureFont.
    '''

    def __init__(self, charcode, size, offset, advance, texcoords):
        '''
        Build a new texture glyph

        Parameter:
        ----------

        charcode : char
            Represented character

        size: tuple of 2 ints
            Glyph size in pixels

        offset: tuple of 2 floats
            Glyph offset relatively to anchor point

        advance: tuple of 2 floats
            Glyph advance

        texcoords: tuple of 4 floats
            Texture coordinates of bottom-left and top-right corner
        '''
        self.charcode = charcode
        self.size = size
        self.offset = offset
        self.advance = advance
        self.texcoords = texcoords
        self.kerning = {}


    def get_kerning(self, charcode):
        ''' Get kerning information

        Parameters:
        -----------

        charcode: char
            Character preceding this glyph
        '''
        if charcode in self.kerning.keys():
            return self.kerning[charcode]
        else:
            return 0
