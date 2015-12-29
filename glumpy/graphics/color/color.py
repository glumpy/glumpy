# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from . import colors as _colors
from glumpy.log import log


class Color(object):
    """
    A Color represent a color using four normalized channels (red, green, blue
    and alpha).  Alpha encodes the transparency of the color, with 0 being
    fully transparent and 1 being fully opaque.

    A color can be declared using several different formats:

      color = Color()
      color = Color( "#123", alpha=1)
      color = Color( "#123456" )
      color = Color( "#123456ff" )
      color = Color( (1,1,1) )
      color = Color( (1,1,1,1) )
      color = Color( "0.5" )
      color = Color( "red" )
      color = Color( "svg:aqua" )
      color = Color( "material:red:500")

    Note
    ----

    You can directly affect a color into a numpy array knowing that depending
    on the type of the array (integer or real), the copied value will be
    unnormalized or normalized.

    Z = np.zeros((1,4),dtype = int)
    Z[0] = Color("white")
    # Z[0] is 255,255,255,255

    Z = np.zeros((1,4),dtype = float)
    Z[0] = Color("white)
    # Z[0] is 1,1,1,1

    """

    def __init__(self, color=None, alpha=None):
        """ Color initialization

        Parameters
        ----------

        color : str, tuple or ndarray
           Color description

        alpha : float
           Alpha channel
        """

        if isinstance(color, np.ndarray):
            self._rgba = np.clip(color,0,1)
        else:
            self._rgba = np.ones(4,dtype=np.float32)*(0,0,0,1)
            self._rgba[...] = Color.parse(color, alpha)


    @classmethod
    def parse(cls, color, alpha ):
        """ Color parsing """

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
            r,g,b,a = [c/255.0 for c in bytearray.fromhex(color)]
            if alpha is not None:
                a  = alpha
            return r,g,b,a



        # Tuple/list/array color
        elif isinstance(color, (list, tuple, np.ndarray)):
            color = np.clip(color, 0, 1)
            if alpha is not None:
                color[3] = alpha
            return color

        # Unknown format
        else:
            log.warn("Unknown color format : %s" % color)
            return 0,0,0,1


    def __array__(self, dtype):
        """ Array interface """

        if np.issubdtype(dtype, np.integer):
            return self.RGBA.astype(dtype)
        else:
            return self.rgba.astype(dtype)


    def __int__(self):
        """ Integer code """

        R,G,B,A = self.RGBA
        return  A+256*(B+256*(G+256*R))


    def hex(self):
        """ Hexadecimal representation of the color """

        R,G,B,A = self.RGBA
        h = hex(int(self))
        return "#" + h[2:-1]


    def __repr__(self):
        """ x.__repr__() <==> repr(x) """

        r,g,b,a = self.rgba
        return "Color(%g,%g,%g,%g)" % (r,g,b,a)


    @property
    def red(self):
        """ Normalized red channel """

        return self._rgba[0]


    @property
    def green(self):
        """ Normalized green channel """

        return self._rgba[1]


    @property
    def blue(self):
        """ Normalized blue channel """

        return self._rgba[2]


    @property
    def alpha(self):
        """ Normalized alpha channel """

        return self._rgba[3]


    @property
    def rgba(self):
        """ Normalized r,g,b,a channels """

        return self._rgba

    @property
    def rgb(self):
        """ Normalized r,g,b channels """

        return self._rgba[:3]

    @property
    def RGBA(self):
        """ r,g,b,a channels """

        return np.round((self._rgba*255)).astype(int)


    @property
    def RGB(self):
        """ r,g,b,a channels """

        return np.round((self._rgba[:3]*255)).astype(int)



class Colors(object):
    """
    Colors represent several color stacked into a numpy array. It it
    initialized from either a list of color names (or values) or from the
    number of colors.
    """

    def __init__(self, colors=[], count=0, alpha=None):
        """ Colors initialization

        Parameters
        ----------

        colors : list
            List of color names or values

        count : int
            Number of colors

        alpha : float
           Alpha channels
        """

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

        if alpha is not None:
            self._data[:,3] = alpha


    def __len__(self):
        """ Number of colors """

        return len(self._data)


    def __getitem__(self, key):
        """ Access a specific color """

        return Color(self._data[key])


    def __setitem__(self, key, value):
        """ Set a specific color """

        self._data[key] = Color.parse(value)


    def __array__(self, dtype):
        """ Array interface """

        if np.issubdtype(dtype, np.integer):
            return self.RGBA.astype(dtype)
        else:
            return self.rgba.astype(dtype)


    @property
    def RGBA(self):
        """ r,g,b,a channels """

        return np.round((self._data*255)).astype(int)


    @property
    def RGB(self):
        """ r,g,b channels """

        return np.round((self._data[:,:3]*255)).astype(int)


    @property
    def rgba(self):
        """ Normalized r,g,b,a channels """

        return self._data


    @property
    def rgb(self):
        """ Normalized r,g,b channels """

        return self._data[:,:3]



    @property
    def red(self):
        """ Normalized red channels """

        return self._rgba[:,0]


    @property
    def green(self):
        """ Normalized green channels """

        return self._rgba[:,1]


    @property
    def blue(self):
        """ Normalized blue channels """

        return self._rgba[:,2]


    @property
    def alpha(self):
        """ Normalized alpha channels """

        return self._rgba[:,3]



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    #print Color(1,1,1,1)
    print(Color("material:red:50"))
    print(Color("material:red:50").rgba)
    print(Color("material:red:50").hsv)

    print(Colors("material:red:*").rgba)
    # print Colors("material:red:*").hsv

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
