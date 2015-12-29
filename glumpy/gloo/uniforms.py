# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
"""
import sys
import math
import numpy as np
from operator import mul
from functools import reduce
from glumpy.log import log
from . texture import Texture2D


def dtype_reduce(dtype, level=0, depth=0):
    """
    Try to reduce dtype up to a given level when it is possible

    dtype =  [ ('vertex',  [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]),
               ('normal',  [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]),
               ('color',   [('r', 'f4'), ('g', 'f4'), ('b', 'f4'), ('a', 'f4')])]

    level 0: ['color,vertex,normal,', 10, 'float32']
    level 1: [['color', 4, 'float32']
              ['normal', 3, 'float32']
              ['vertex', 3, 'float32']]
    """
    dtype = np.dtype(dtype)
    fields = dtype.fields

    # No fields
    if fields is None:
        if dtype.shape:
            count = reduce(mul, dtype.shape)
        else:
            count = 1
        size = dtype.itemsize/count
        if dtype.subdtype:
            name = str( dtype.subdtype[0] )
        else:
            name = str( dtype )
        return ['', count, name]
    else:
        items = []
        name = ''
        # Get reduced fields
        for key,value in fields.items():
            l = dtype_reduce(value[0], level, depth+1)
            if type(l[0]) is str:
                items.append( [key, l[1], l[2]] )
            else:
                items.append( l )
            name += key+','

        # Check if we can reduce item list
        ctype = None
        count = 0
        for i,item in enumerate(items):
            # One item is a list, we cannot reduce
            if type(item[0]) is not str:
                return items
            else:
                if i==0:
                    ctype = item[2]
                    count += item[1]
                else:
                    if item[2] != ctype:
                        return items
                    count += item[1]
        if depth >= level:
            return [name, count, ctype]
        else:
            return items



class Uniforms(Texture2D):
    """
    Uniforms data texture holder.

    This class is used in conjunction with collections in order to store a
    number of uniforms in a texture such that each vertices can retrieve a
    specific group of uniforms. The data type can be structured but must be
    reduceable to n x np.float32. Note that you don't need to manipulate
    directly this function, it is done automagically in collections.

    .. note::
 
       The code needed to retrieve a specific item is given from the ``code``
       function and is generated specifically for the actual data type.

    :param int size: Number of items to be stored in the texture
    :param numpy.dtype dtype: Item data type (must be reduceable to n x np.float32)
    """

    def __init__(self, size, dtype):
        """ Initialization """

        # Check dtype is made of float32 only
        dtype = eval(str(np.dtype(dtype)))
        rtype = dtype_reduce(dtype)
        if type(rtype[0]) is not str or rtype[2] != 'float32':
            raise RuntimeError("Uniform type cannot be reduced to float32 only")

        # True dtype (the one given in args)
        self._original_dtype = np.dtype(dtype)

        # Equivalent float count
        self._original_count = rtype[1]

        # Make dtype a multiple of 4 floats
        count = 4*(rtype[1]//4)
        if rtype[1] % 4:
            count += 4
        if (count - rtype[1]) > 0:
            dtype.append(('unused', '<f4', count - rtype[1]))

        # Complete dtype, multiple of 4 floats
        self._complete_dtype = dtype

        # Equivalent float count
        self._complete_count = count

        # max_texsize = gl.glGetInteger(gl.GL_MAX_TEXTURE_SIZE)
        max_texsize = 512
        width = max_texsize
        height = 1 + size//width

        cols = max_texsize//(count/4)
        rows = size // cols
        if size % cols: rows += 1

        Texture2D.__init__(self, shape=(rows,cols,4), dtype=np.float32,
                           resizeable=False, store=True)
        data = self._data.ravel()
        self._typed_data = data.view(self._complete_dtype)
        self._size = size


    def __setitem__(self, key, value):
        """ x.__getitem__(y) <==> x[y] """


        if self.base is not None and not self._valid:
            raise ValueError("This uniforms view has been invalited")

        size = self._size
        if isinstance(key, int):
            if key < 0:
                key += size
            if key < 0 or key > size:
                raise IndexError("Uniforms assignment index out of range")
            start, stop = key, key + 1
        elif isinstance(key, slice):
            start, stop, step = key.indices(size)
            if step != 1:
                raise ValueError("Cannot access non-contiguous uniforms data")
            if stop < start:
                start, stop = stop, start
        elif key == Ellipsis:
            start = 0
            stop = size
        else:
            raise TypeError("Uniforms indices must be integers")


        # First we set item using the typed data
        shape = self._typed_data[start:stop].shape
        dtype = self._original_dtype
        data = self._typed_data
        # data[start:stop] = np.array(value, dtype=dtype).reshape(shape)
        data[start:stop] = np.array(value, dtype=dtype)


        # Second, we tell texture where to update
        count  = self._complete_count
        start = np.unravel_index(start*count, self.shape)
        stop = np.unravel_index(stop*count, self.shape)
        if start[0] == stop[0]:
            start = start[:2]
            stop  = stop[:2]
        else:
            start = start[0], 0
            stop  = stop[0], self.shape[1]-1

        offset = start[0], start[1], 0
        data = self._data[start[0]:stop[0]+1,start[1]:stop[1]]
        self.set_data(data=data, offset=offset, copy=False)



    def code(self, prefix="u_"):
        """
        Generate the GLSL code needed to retrieve fake uniform values from a texture.
        The generated uniform names can be prefixed with the given prefix.
        """

        dtype = np.dtype(self._original_dtype)
        _dtype = dtype_reduce(dtype, level=1)

        header = """uniform sampler2D u_uniforms;\n"""

        # Header generation (easy)
        types = { 1 : 'float', 2 : 'vec2 ', 3 : 'vec3 ',
                  4 : 'vec4 ', 9 : 'mat3 ', 16 : 'mat4 '}
        for name,count,_ in _dtype:
            header += "varying %s %s%s;\n" % (types[count],prefix,name)


        # Body generation (not so easy)
        rows, cols = self.shape[0], self.shape[1]
        count = self._complete_count

        body = """\nvoid fetch_uniforms(float index) {
        float rows   = %.1f;
        float cols   = %.1f;
        float count  = %.1f;
        int index_x  = int(mod(index, (floor(cols/(count/4.0))))) * int(count/4.0);
        int index_y  = int(floor(index / (floor(cols/(count/4.0)))));
        float size_x = cols - 1.0;
        float size_y = rows - 1.0;
        float ty     = 0.0;
        if (size_y > 0.0)
            ty = float(index_y)/size_y;
        int i = index_x;
        vec4 _uniform;\n""" % (rows, cols, count)


        _dtype = {name: count for name,count,_ in _dtype}
        store = 0
        # Be very careful with utype name order (_utype.keys is wrong)
        for name in dtype.names:
            count, shift =_dtype[name], 0
            while count:
                if store == 0:
                    body += "\n    _uniform = texture2D(u_uniforms, vec2(float(i++)/size_x,ty));\n"
                    store = 4
                if   store == 4: a = "xyzw"
                elif store == 3: a = "yzw"
                elif store == 2: a = "zw"
                elif store == 1: a = "w"
                if shift == 0:   b = "xyzw"
                elif shift == 1: b = "yzw"
                elif shift == 2: b = "zw"
                elif shift == 3: b = "w"

                i = min(min(len(b), count), len(a))
                body += "    %s%s.%s = _uniforms.%s;\n" % (prefix,name,b[:i],a[:i])
                count -= i
                shift += i
                store -= i

        body += """}"""
        return header + body
