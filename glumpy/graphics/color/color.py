#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import colors as _colors
from glumpy.log import log


class Color(object):

    def __init__(self, color=None):
        if isinstance(color, np.ndarray):
            self._rgba = np.clip(color,0,1)
        else:
            self._rgba = np.zeros(4,dtype=np.float32)
            self._rgba[...] = Color.parse(color)


    @classmethod
    def parse(cls, color):
        if color is None:
            return

        if isinstance(color, str):
            # Named color
            if color[0] != '#':
                color = color.lower().strip()
                color = color.replace(' ','')
                color = color.replace('-','')
                color = _colors.get(color)

            if color[0] != '#':
                log.warn("Unknown color name : %s" % color)
                return 0,0,0,1

            # Hexadecimal color
            color = color[1:]
            if len(color) == 3:
                color += 'f'
            if len(color) == 4:
                color = ''.join([color[i] for i in [0,0,1,1,2,2,3,3]])
            if len(color) == 6:
                color += 'ff'
            return [ord(c)/255.0 for c in color.decode('hex')]


        # Tuple/list/array color
        elif isinstance(color, (list, tuple, np.ndarray)):
            return np.clip(color, 0, 1)

        # Unknown format
        else:
            log.warn("Unknown color format : %s" % color)
            return 0,0,0,1


    def __array__(self, dtype):
        if np.issubdtype(dtype, np.integer):
            return self.RGBA.astype(dtype)
        else:
            return self.rgba.astype(dtype)

    def __int__(self):
        R,G,B,A = self.RGBA
        return  A+256*(B+256*(G+256*R))

    def hex(self):
        R,G,B,A = self.RGBA
        h = hex(A+256*(B+256*(G+256*R)))
        return "#" + h[2:-1]

    def __repr__(self):
        r,g,b,a = self.rgba
        return "Color(%g,%g,%g,%g)" % (r,g,b,a)

    @property
    def red(self):
        return self._rgba[0]

    @property
    def green(self):
        return self._rgba[1]

    @property
    def blue(self):
        return self._rgba[2]

    @property
    def alpha(self):
        return self._rgba[3]

    @property
    def rgba(self):
        return self._rgba

    @property
    def rgb(self):
        return self._rgba[:3]

    @property
    def RGBA(self):
        return np.round((self._rgba*255)).astype(int)

    @property
    def RGB(self):
        return np.round((self._rgba[:3]*255)).astype(int)



class Colors(object):
    def __init__(self, colors=[], count=0):

        if isinstance(colors, str):
            if colors[0] != '#':
                colors = _colors.get(colors)
            if isinstance(colors, str):
                colors = [colors]

        if len(colors) > 0:
            n = len(colors)
            self._data = np.zeros((n,4),dtype=np.float32)
            for i in range(n):
                self._data[i] = Color(colors[i]).rgba

        elif count > 0:
            self._data = np.zeros((count,4),dtype=np.float32)

        else:
            log.warn("Colors must be declared with a list or a color count")
            self._data = np.zeros((1,4),dtype=np.float32)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return Color(self._data[key])

    def __setitem__(self, key, value):
        self._data[key] = Color.parse(value)

    def __array__(self, dtype):
        if np.issubdtype(dtype, np.integer):
            return self.RGBA.astype(dtype)
        else:
            return self.rgba.astype(dtype)

    @property
    def RGBA(self):
        return np.round((self._data*255)).astype(int)

    @property
    def RGB(self):
        return np.round((self._data[:,:3]*255)).astype(int)

    @property
    def rgba(self):
        return self._data

    @property
    def rgb(self):
        return self._data[:,:3]




# -----------------------------------------------------------------------------
if __name__ == '__main__':

    #print Color(1,1,1,1)
    print Color("material:red:50")
    print Colors("material:red:*").rgba

    print Colors("material:red:*").hsv

    # colors = Colors(['red', 'lime', 'blue'])
    # print colors.rgba
    # print

    # # Affects an integer array
    # Z = np.zeros((3,4),dtype = int)
    # Z[...] = color
    # print Z
    # print

    # Z = np.zeros((3,4),dtype = int)
    # Z[...] = colors
    # print Z
