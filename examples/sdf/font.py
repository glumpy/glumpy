# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from freetype import *
from scipy.ndimage.interpolation import zoom

from sdf import compute_sdf
from glumpy.gloo.atlas import Atlas



class Glyph:
    '''
    A glyph gathers information relative to the size/offset/advance and texture
    coordinates of a single character. It is generally built automatically by a
    Font.
    '''

    def __init__(self, charcode, shape, offset, advance, texcoords):
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
        self.shape = shape
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


# -----------------------------------------------------------------------------
class Font:

    _atlas = None

    def __init__(self, filename):

        self._hires_size = 256
        self._lowres_size = 48

        self.filename = filename
        self.glyphs = {}
        face = Face( self.filename )
        face.set_char_size(self._lowres_size*64)
        metrics = face.size
        self.ascender  = metrics.ascender/64.0
        self.descender = metrics.descender/64.0
        self.height    = metrics.height/64.0
        self.linegap   = (self.height - self.ascender + self.descender)


    @property
    def atlas(self):
        if Font._atlas is None:
            Font._atlas = np.zeros((1024,1024),np.float32).view(Atlas)
            # Font._atlas = np.zeros((512,512),np.uint8).view(Atlas)
        return Font._atlas


    def __getitem__(self, charcode):
        if charcode not in self.glyphs.keys():
            self.load('%c' % charcode)
        return self.glyphs[charcode]

    def load_glyph(self, face, charcode, hires_size=512, lowres_size=32, padding=0.125):
        face.set_char_size( hires_size*64 )
        face.load_char(charcode, FT_LOAD_RENDER | FT_LOAD_NO_HINTING | FT_LOAD_NO_AUTOHINT);

        bitmap = face.glyph.bitmap
        width  = face.glyph.bitmap.width
        height = face.glyph.bitmap.rows
        pitch  = face.glyph.bitmap.pitch

        # Get glyph into a numpy array
        G = np.array(bitmap.buffer).reshape(height,pitch)
        G = G[:,:width].astype(np.ubyte)

        # Pad high resolution glyph with a blank border and normalize values
        # between 0 and 1
        hires_width  = (1+2*padding)*width
        hires_height = (1+2*padding)*height
        hires_data = np.zeros( (hires_height,hires_width), np.double)
        ox,oy = padding*width, padding*height
        hires_data[oy:oy+height, ox:ox+width] = G/255.0

       # Compute distance field at high resolution
        compute_sdf(hires_data)

       # Scale down glyph to low resoltion size
        ratio = lowres_size/float(hires_size)
        lowres_data = 1 - zoom(hires_data, ratio, cval=1.0)

       # Compute information at low resolution size
        # size   = ( lowres_data.shape[1], lowres_data.shape[0] )
        offset = ( (face.glyph.bitmap_left - padding*width) * ratio,
                   (face.glyph.bitmap_top + padding*height) * ratio )
        advance = ( (face.glyph.advance.x/64.0)*ratio,
                    (face.glyph.advance.y/64.0)*ratio )
        return lowres_data, offset, advance


    def load(self, charcodes = ''):
        face = Face( self.filename )

        for charcode in charcodes:
            if charcode in self.glyphs.keys():
                continue

            data,offset,advance = self.load_glyph(
                face, charcode, self._hires_size, self._lowres_size)

            h,w = data.shape
            region = self.atlas.allocate( (h+2,w+2) )
            if region is None:
                log.warn("Cannot store glyph '%c'" % charcode)
                continue
            x,y,_,_ = region
            x,y = x+1, y+1
            self.atlas[y:y+h,x:x+w] = data.reshape(h,w,1)

            u0     = (x +     0.0)/float(self.atlas.width)
            v0     = (y +     0.0)/float(self.atlas.height)
            u1     = (x + w - 0.0)/float(self.atlas.width)
            v1     = (y + h - 0.0)/float(self.atlas.height)
            texcoords = (u0,v0,u1,v1)
            glyph = Glyph(charcode, data.shape, offset, advance, texcoords)
            self.glyphs[charcode] = glyph

            # Generate kerning (for reference size)
            face.set_char_size( self._lowres_size*64 )
            for g in self.glyphs.values():
                kerning = face.get_kerning(g.charcode, charcode, mode=FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    glyph.kerning[g.charcode] = kerning.x/64.0
                kerning = face.get_kerning(charcode, g.charcode, mode=FT_KERNING_UNFITTED)
                if kerning.x != 0:
                    g.kerning[charcode] = kerning.x/64.0
