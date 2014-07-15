# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
A collection is a (virtual) container for several objects having the same
vertex structure (vtype) and same uniforms type (utype). A collection allows to
manipulate objects individually but they can be rendered at once (single call).
Each object can have its own set of uniforms provided they are a combination of
floats.
"""
import math
import numpy as np

from glumpy.gloo.program import Program
from glumpy.gloo.texture import Texture2D
from glumpy.gloo.buffer import VertexBuffer, IndexBuffer
from glumpy.gloo.shader import VertexShader, FragmentShader
from glumpy.graphics.collection.array_list import ArrayList
from glumpy.graphics.collection.util import dtype_reduce, fetchcode


class Item(object):
    """
    An item represent an object within a collection and is created on demand
    when accessing a specific object of the collection.
    """

    # ---------------------------------
    def __init__(self, parent, key, vertices, indices, uniforms):
        """
        Create an item from an existing collection.

        Parameters
        ----------

        parent : Collection
            Collection this item belongs to

        key : int
            Collection index of this item

        vertices: array-like
            Vertices of the item

        indices: array-like
            Indices of the item

        uniforms: array-like
            Uniform parameters of the item
        """

        self._parent   = parent
        self._key      = key
        self._vertices = vertices
        self._indices  = indices
        self._uniforms  = uniforms


    @property
    def vertices(self):
        return self._vertices


    @vertices.setter
    def vertices(self, data):
        self._vertices[...] = np.array(data)


    @property
    def indices(self):
        return self._indices


    @indices.setter
    def indices(self, data):
        if self._indices is None:
            raise ValueError("Item has no indices")
        start = self._parent.vertices._items[self._key][0]
        self._indices[...] = np.array(data) + start


    @property
    def uniforms(self):
        return self._uniforms


    @uniforms.setter
    def uniforms(self, data):
        if self._uniforms is None:
            raise ValueError("Item has no associated uniform")
        self._uniforms[...] = data


    def __getitem__(self, key):
        """ Get a specific uniforms value """

        if key in self._vertices.dtype.names:
            return self._vertices[key]
        elif key in self._uniforms.dtype.names:
            return self._uniforms[key]
        else:
            raise IndexError("Unknown key ('%s')" % key)


    def __setitem__(self, key, value):
        """ Set a specific uniforms value """

        if key in self._vertices.dtype.names:
            self._vertices[key] = value
        elif key in self._uniforms.dtype.names:
            self._uniforms[key] = value
        else:
            raise IndexError("Unknown key")


    def __str__(self):
        return "Item (%s, %s, %s)" % (self._vertices, self._indices, self._uniforms)





class Collection(object):
    """
    A collection is a container for several objects having the same vertex
    structure (vtype) and same uniforms type (utype). A collection allows to
    manipulate objects individually but they can be rendered at once (single
    call). Each object can have its own set of uniforms provided they are a
    combination of floats.
    """

    def __init__(self, vtype, utype=None, itype=None, vertex=None, fragment=None):
        """

        Parameters
        ----------

        vtype: np.dtype
            Vertices data type

        utype: np.dtype
            Uniforms data type

        itype: np.dtype
            Indices data type
        """

        self._vbuffer = None
        self._ibuffer = None
        self._utexture = None
        self._vertex = vertex
        self._fragment = fragment
        self._program = None


        # Vertices and type (mandatory)
        self._vertices       = None
        self._vertices_dtype = None

        # Vertex indices and type (optional)
        self._v_indices       = None
        self._v_indices_dtype = None

        # Uniforms and type (optional)
        self._uniforms       = None
        self._uniforms_dtype = None

        # Make sure types are np.dtype (or None)
        vtype = np.dtype(vtype) if vtype is not None else None
        itype = np.dtype(itype) if itype is not None else None
        utype = np.dtype(utype) if utype is not None else None

        # Vertices type (mandatory)
        # -------------------------
        if vtype.names is None:
            raise ValueError("vtype must be a structured dtype")

        # Indices type (optional)
        # -----------------------
        if itype is not None:
            if itype not in [np.uint8, np.uint16, np.uint32]:
                raise ValueError("itype must be unsigned integer or None")
            self._v_indices = ArrayList(dtype=itype)
            self._v_indices_dtype = itype

        # Uniforms type (optional)
        # -------------------------
        if utype is not None:
            if utype.names is None:
                raise ValueError("utype must be a structured dtype")

            # Convert types to lists (in case they were already dtypes) such that
            # we can append new fields
            vtype = eval(str(np.dtype(vtype)))
            # We add a uniform index to access uniform data
            vtype.append( ('a_index', 'f4') )
            vtype = np.dtype(vtype)

            # Check utype is made of float32 only
            utype = eval(str(np.dtype(utype)))
            r_utype = dtype_reduce(utype)
            if type(r_utype[0]) is not str or r_utype[2] != 'float32':
                raise RuntimeError("utype cannot be reduced to float32 only")

            # Make utype divisible by 4
            count = int(math.pow(2, math.ceil(math.log(r_utype[1], 2))))
            if (count - r_utype[1]) > 0:
                utype.append(('unused', 'f4', count-r_utype[1]))

            self._uniforms       = ArrayList(dtype=utype)
            self._uniforms_dtype = utype
            self._uniforms_rtype = np.dtype([("all", np.float32, count)])

        # Last since utype may add a new field in vtype (a_index)
        self._vertices = ArrayList(dtype=vtype)
        self._vertices_dtype = vtype



    @property
    def vertices(self):
        """ Vertices buffer """

        return self._vertices.data


    @property
    def indices(self):
        """ Indices buffer """

        return self._v_indices.data


    @property
    def uniforms(self):
        """ Uniforms buffer """

        return self._uniforms.data


    def __len__(self):
        """ """
        return len(self._vertices)


    def __getitem__(self, key):
        """ """

        V, I, U = self._vertices, self._v_indices, self._uniforms

        # Getting field
        # -------------
        if isinstance(key, str):
            if key in V.dtype.names:
                return V[key]
            elif U is not None and key in U.dtype.names:
                return U[key]
            else:
                raise IndexError("Unknonw field name ('%s')" % key)

        # Getting individual item
        # -----------------------
        elif isinstance(key, int):
            vertices = V[key]
            indices  = I[key] if I is not None else None
            uniform  = U[key] if U is not None else None
            return Item(self, key, vertices, indices, uniform)

        # Error
        # -----
        else:
            raise IndexError("Cannot get more than one item")


    def __setitem__(self, key, data):
        """ """

        # Setting field
        # -------------
        if isinstance(key, str):
            # Setting vertices field at once
            if key in self._vertices_dtype.names:
                self._vertices.data[key] = data

            # Setting uniforms field at once
            elif key in self._uniforms_dtype.names:
                self._uniforms.data[key] = data
            else:
                raise IndexError("Unknonw field name ('%s')" % key)

        # Setting individual item
        # -----------------------
        elif isinstance(key, int):
            vertices, indices, uniforms = data
            del self[key]
            self.insert(key, vertices, indices, uniforms)

        # Setting individual item
        # -----------------------
        else:
            raise IndexError("Cannot set more than one item")



    def __delitem__(self, index):
        """ x.__delitem__(y) <==> del x[y] """

        # Deleting one item
        # -----------------
        if isinstance(index, int):
            if index < 0:
                index += len(self)
            if index < 0 or index > len(self):
                raise IndexError("Collection deletion index out of range")
            istart, istop = index, index+1

        # Deleting several items
        # ----------------------
        elif isinstance(index, slice):
            istart, istop, _ = index.indices(len(self))
            if istart > istop:
                istart, istop = istop,istart
            if istart == istop:
                return

        # Deleting everything
        # -------------------
        elif index is Ellipsis:
            istart, istop = 0, len(self)

        # Error
        # -----
        else:
            raise TypeError("Collection deletion indices must be integers")

        vsize = len(self._vertices[index])
        if self._v_indices is not None:
            del self._v_indices[index]
            self._v_indices[index] -= vsize
        del self._vertices[index]
        if self._uniforms is not None:
            del self._uniforms[index]

        # Update a_index at once
        if self._uniforms is not None:
            I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
            self._vertices['a_index'] = I.astype(np.float32)

    def insert(self, index, vertices, uniforms=None, indices=None, itemsize=None):
        """
        Parameters
        ----------

        index : int
            Index before which to insert data

        vertices : numpy array
            An array whose dtype is compatible with self.vertices.dtype

        indices : numpy array
            An array whose dtype is compatible with self.indices.dtype All
            index values must be between 0 and len(vertices)

        uniforms: int or numpy array
            An array whose dtype is int or is compatible with
            self.uniforms.dtype

        itemsize:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided into
            elements of size N. If such partition is not possible, an error is
            raised.

            If `itemsize` is 1-D array, the array will be divided into elements
            whose succesive sizes will be picked from itemsize.  If the sum of
            itemsize values is different from array size, an error is raised.
        """

        vtype = self._vertices.dtype
        vertices = np.array(vertices,copy=False).astype(vtype).ravel()

        # Sanity checks
        # -------------
        if indices is not None and self._v_indices is None:
            raise RuntimeError("Collection has been created without indices")
        elif indices is None and self._v_indices is not None:
            indices = np.arange(len(vertices), dtype=self._v_indices_dtype)
            #raise RuntimeError("Items must be provided with indices")

        if uniforms is not None and self._uniforms is None:
            raise RuntimeError("Collection has been created without uniforms")
        elif uniforms is None and self._uniforms is not None:
            raise RuntimeError("Items must be provided with uniforms")

        if indices is not None:
            itype = self._v_indices.dtype
            indices = np.array(indices,copy=False).astype(itype).ravel()

        if uniforms is not None:
            utype = self._uniforms.dtype
            uniforms = np.array(uniforms,copy=False).astype(utype).ravel()


        # Check index
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("Collection insertion index out of range")

        # Inserting
        if index < len(self._vertices):
            vstart = self._vertices._items[index][0]
            if self._v_indices is not None:
                istart = self._v_indices._items[index][0]
            if self._uniforms is not None:
                ustart = self._uniforms._items[index][0]
        # Appending
        else:
            vstart = self._vertices.size
            if self._v_indices is not None:
                istart = self._v_indices.size
            if self._uniforms is not None:
                ustart = self._uniforms.size

        # Updating indices
        if self._v_indices is not None:
            self._v_indices._data[istart:] += len(vertices)
            indices += vstart

        # Inserting one item
        if itemsize is None:
            self._vertices.insert(index,vertices)
            if self._v_indices is not None:
                self._v_indices.insert(index,indices)
            if self._uniforms is not None:
                if uniforms is not None:
                    self._uniforms.insert(index,uniforms)
                else:
                    U = np.zeros(1,dtype=self._uniforms.dtype)
                    self._uniforms.insert(index,U)

            # Update a_index at once
            if self._uniforms is not None:
                I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
                self._vertices['a_index'] = I.astype(np.float32)

            self._build_buffers()
            return


        # No item size specified
        if itemsize is None:
            v_itemcount = 1
            v_itemsize = np.ones(1,dtype=int)*vertices.size
            if indices is not None:
                i_itemcount = 1
                i_itemsize = np.ones(1,dtype=int)*indices.size

        # Vertices size specified but no indices size
        if type(itemsize) is int:
            v_itemcount = vertices.size // itemsize
            v_itemsize = itemsize*np.ones(v_itemcount,dtype=int)
            if indices is not None:
                i_itemcount = v_itemcount
                i_itemsize = len(indices)*np.ones(i_itemcount,dtype=int)
                indices = np.resize(indices, len(indices)*i_itemcount)

        # Vertices and indices size specified
        elif isinstance(itemsize, tuple):
            v_itemsize = itemsize[0]
            v_itemcount = vertices.size // v_itemsize
            v_itemsize = v_itemsize*np.ones(v_itemcount,dtype=int)

            if indices is not None:
                i_itemsize = itemsize[1]
                i_itemcount = indices.size // i_itemsize
                i_itemsize = i_itemsize*np.ones(i_itemcount, dtype=int)

        # Vertices have different size
        else:
            itemsize = np.array(itemsize, copy=False)
            v_itemsize = itemsize[:,0]
            i_itemsize = itemsize[:,1]

        # Sanity check
        if (vertices.size % v_itemsize.sum()) != 0:
            raise ValueError("Cannot partition vertices data as requested")

        if indices is not None:
            if (indices.size % i_itemsize.sum()) != 0:
                raise ValueError("Cannot partition indices data as requested")
            if v_itemcount != i_itemcount:
                raise ValueError("Vertices/Indices item size not compatible")

        self._vertices.insert(index, vertices, v_itemsize)

        if self._v_indices is not None:
            I = np.repeat(v_itemsize.cumsum(),i_itemsize)
            indices[i_itemsize[0]:] += I[:-i_itemsize[0]]
            self._v_indices.insert(index, indices, i_itemsize)

        if self._uniforms is not None:
            if uniforms is None:
                U = np.zeros(v_itemcount,dtype=self._uniforms.dtype)
                self._uniforms.insert(index,U, itemsize=1)
            else:
                if len(uniforms) != v_itemcount:
                    if len(uniforms) == 1:
                        U = np.resize(uniforms, v_itemcount)
                        self._uniforms.insert(index, U, itemsize=1)
                    else:
                        raise ValueError("Vertices/Uniforms item number not compatible")
                else:
                    self._uniforms.insert(index, uniforms, itemsize=1)

        # Update a_index at once
        if self._uniforms is not None:
            I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
            self._vertices['a_index'] = I.astype(np.float32)

        self._build_buffers()


    def _build_program(self):
        """ """

        if self._program is not None:
            return self._program

        vert, frag = self._vertex, self._fragment
        if notisinstance(vert, VertexShader):
            vert = VertexShader(vert)
        code = fetchcode(self._uniforms_dtype)
        code += self._vertex._code
        vert = VertexShader(code)
        self._program = Program(vert, frag)
        self._build_buffers()



    def _build_buffers(self):
        """ """

        # Explicit deletion of buffers & texture from GPU memory
        if self._vbuffer is not None:
            self._vbuffer._delete()
        if self._utexture is not None:
            self._utexture._delete()
        if self._ibuffer is not None:
            self._ibuffer._delete()

        self._vbuffer = self._vertices.data.view(VertexBuffer)

        if self._v_indices is not None:
            self._ibuffer = self._v_indices.data.view(IndexBuffer)

        if self._uniforms is not None:
            # max_texsize = gl.glGetInteger(gl.GL_MAX_TEXTURE_SIZE)
            texture = self._uniforms.data.view(np.float32)
            rowsize = min(4096, texture.size//4)

            count = self._uniforms_rtype[0].shape[0]
            cols = rowsize//(count/4)
            rows = (len(self) // cols)
            # rows = (len(self) // cols)+1
            shape = rows, cols*(count/4), count
            texture = texture.reshape(shape)

            self._utexture = texture.view(Texture2D)

        if self._program:
            self._program.bind(self._v_buffer)
            if self._uniforms is not None:
                self._program["u_uniforms"] = self._utexture
                self._program["u_uniforms_shape"] = shape


    def append(self, vertices, uniforms=None, indices=None, itemsize=None):
        """

        Parameters
        ----------

        vertices : numpy array
            An array whose dtype is compatible with self.vertices.dtype

        indices : numpy array
            An array whose dtype is compatible with self.indices.dtype
            All index values must be between 0 and len(vertices)

        uniforms: numpy array
            An array whose dtype is compatible with self.uniforms.dtype

        itemsize: int, tuple or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.

        """
        self.insert(len(self), vertices, uniforms, indices, itemsize)


if __name__ == '__main__':
    vtype = [('position', 'f4', 2)]
    utype = [('color', 'f4', 3)]
    itype = np.uint32

    C = Collection(vtype, utype, itype)
    for i in range(4):
        V = np.zeros(i+1,vtype)
        I = np.arange(i+1)
        V['position'] = i
        U = np.zeros(1,utype)
        U['color'] = i
        C.append(V, U, I)


    for i in range(4):
        print C[i]
    print
    del C[:3]
    print C[0]

#    print C.program
