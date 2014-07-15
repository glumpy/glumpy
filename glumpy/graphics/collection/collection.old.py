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

from glumpy.gloo.texture import Texture2D
from glumpy.gloo.buffer import VertexBuffer, IndexBuffer
from glumpy.graphics.collection.util import dtype_reduce
from glumpy.graphics.collection.array_list import ArrayList


class Item(object):
    """
    An item represent an object within a collection and is created on demand
    when accessing a specific object of the collection.
    """

    # ---------------------------------
    def __init__(self, parent, key, vertices, indices, uniforms):
        """
        Create a new item from an existing collection.

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
        self._uniforms = uniforms


    @property
    def vertices(self):
        return self._vertices


    @vertices.setter
    def vertices(self, data):
        data = np.array(data)
        self._vertices[...] = data


    @property
    def indices(self):
        return self._indices


    @indices.setter
    def indices(self, data):
        if self._indices is None:
            raise ValueError("Item has no indices")
        data = np.array(data)
        start = self._parent.vertices._items[self._key][0]
        self._indices[...] = data + start


    @property
    def uniforms(self):
        return self._uniforms


    @uniforms.setter
    def uniforms(self, data):
        if self._uniforms is None:
            raise ValueError("Item has no uniforms")
        self._uniforms[...] = data


    def __getitem__(self, key):
        """ Get a specific uniform value """
        # return self._uniforms[key]

        if self._vertices.dtype.names and key in self._vertices.dtype.names:
            return self._vertices[key]
        elif self._uniforms.dtype.names and key in self._uniforms.dtype.names:
            return self._uniforms[key]
        else:
            raise IndexError("Unknown key")


    def __setitem__(self, key, value):
        """ Set a specific uniform value """
        # self._uniforms[key] = value

        if self._vertices.dtype.names and key in self._vertices.dtype.names:
            self._vertices[key] = value
        elif self._uniforms.dtype.names and key in self._uniforms.dtype.names:
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

    def __init__(self, vtype, utype=None, itype=None):
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

        # Vertices type (mandatory)
        vtype = np.dtype(vtype)
        if vtype.names is None:
            raise ValueError("vtype must be a structured dtype")

        if utype is not None:
            # Convert types to lists (in case they were already dtypes) such that
            # we can append new fields
            vtype = eval(str(np.dtype(vtype)))
            # We add a uniform index to access uniform data
            vtype.append( ('a_index', 'f4') )
            vtype = np.dtype(vtype)

        self._vertices = ArrayList(dtype=vtype)

        # Uniforms type (optional)
        if utype is not None:
            utype = np.dtype(utype)

            if utype.names is None:
                raise ValueError("utype must be a structured dtype")
            # Check utype is made of float32 only
            utype = eval(str(np.dtype(utype)))
            r_utype = dtype_reduce(utype)
            if type(r_utype[0]) is not str or r_utype[2] != 'float32':
                raise RuntimeError("Uniform type cannot be reduced to float32 only")

            # Make utype divisible by 4
            count = int(math.pow(2, math.ceil(math.log(r_utype[1], 2))))
            if (count - r_utype[1]) > 0:
                utype.append(('unused', 'f4', count-r_utype[1]))
            self._u_float_count = count
            self._uniforms = ArrayList(dtype=utype)
        else:
            self._uniforms = None

        # Indices type (optional)
        if itype is not None:
            itype = np.dtype(itype)
            if itype not in [np.uint8, np.uint16, np.uint32]:
                raise ValueError("itype must be unsigned integer or None")
            self._indices = ArrayList(dtype=itype)
        else:
            self._indices = None

        self._vbuffer = None
        self._ibuffer = None
        self._utexture = None


    @property
    def vertices(self):
        """ Vertices buffer """

        return self._vertices


    @property
    def indices(self):
        """ Indices buffer """

        return self._indices


    @property
    def uniforms(self):
        """ Uniforms buffer """

        return self._uniforms


    def __len__(self):
        """ """
        return len(self._vertices)



    def __getitem__(self, key):
        """ """

        V, U, I = self._vertices, self._uniforms, self._indices
        if V.dtype.names and key in V.dtype.names:
            return V[key]
        elif  U is not None and U.dtype.names and key in U.dtype.names:
            return U[key]
        else:
            if self._uniforms is None:
                uniforms = None
            else:
                uniforms = U[key]
            if self._indices is None:
                indices = None
            else:
                indices = I[key]
            vertices = V[key]
            return Item(self, key, vertices, indices, uniforms)



    def __setitem__(self, key, data):
        """ """

        # Setting vertices field at once
        if self._vertices.dtype.names and key in self._vertices.dtype.names:
            self._vertices.data[key] = data

        # Setting uniforms field at once
        elif self._uniforms.dtype.names and key in self._uniforms.dtype.names:
            self._uniforms.data[key] = data

        # Setting individual item
        else:
            vertices, indices, uniforms = data
            del self[key]
            self.insert(key, vertices, indices, uniforms)



    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """

        if type(key) is int:
            if key < 0:
                key += len(self)
            if key < 0 or key > len(self):
                raise IndexError("Collection deletion index out of range")
            kstart, kstop = key, key+1

        # Deleting several items
        elif type(key) is slice:
            kstart, kstop, _ = key.indices(len(self))
            if kstart > kstop:
                kstart, kstop = kstop,kstart
            if kstart == kstop:
                return
        elif key is Ellipsis:
            kstart, kstop = 0, len(self)
        # Error
        else:
            raise TypeError("Collection deletion indices must be integers")

        vsize = len(self._vertices[key])
        del self._indices[key]
        self._indices[key] -= vsize
        del self._vertices[key]
        del self._uniforms[key]

        # Update a_index at once
        if self._uniforms is not None:
            I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
            self._vertices['a_index'] = I


    def insert(self, index, vertices, indices=None, uniforms=None, itemsize=None):
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

        # Make sure vertices/indices/uniforms are of the right dtype

        vtype = self._vertices.dtype
        vertices = np.array(vertices,copy=False).astype(vtype).ravel()

        if indices is not None and self._indices is None:
            raise RuntimeError("Collection has been created without indices")

        if indices is  None and self._indices is not None:
            raise RuntimeError("Items must be provided with indices")

        if uniforms is not None and self._uniforms is None:
            raise RuntimeError("Collection has been created without uniforms")

        if uniforms is None and self._uniforms is not None:
            raise RuntimeError("Items must be provided with uniforms")

        if indices is not None:
            itype = self._indices.dtype
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
            if self._indices is not None:
                istart = self._indices._items[index][0]
            if self._uniforms is not None:
                ustart = self._uniforms._items[index][0]
        # Appending
        else:
            vstart = self._vertices.size
            if self._indices is not None:
                istart = self._indices.size
            if self._uniforms is not None:
                ustart = self._uniforms.size

        # Updating indices
        if self._indices is not None:
            self._indices._data[istart:] += len(vertices)
            indices += vstart

        # Inserting one item
        if itemsize is None:
            #self._vertices[index:]['a_index'] += 1
            #vertices['a_index'] = index
            self._vertices.insert(index,vertices)
            if self._indices is not None:
                self._indices.insert(index,indices)
            if self._uniforms is not None:
                if uniforms is not None:
                    self._uniforms.insert(index,uniforms)
                else:
                    U = np.zeros(1,dtype=self._uniforms.dtype)
                    self._uniforms.insert(index,U)

            # Update a_index at once
            if self._uniforms is not None:
                I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
                self._vertices['a_index'] = I

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

        if self._indices is not None:
            I = np.repeat(v_itemsize.cumsum(),i_itemsize)
            indices[i_itemsize[0]:] += I[:-i_itemsize[0]]
            self._indices.insert(index, indices, i_itemsize)

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
            self._vertices['a_index'] = I

        self._build_buffers()



    def _build_buffers(self):
        """ """
        if self._vbuffer is not None:
            del self._vbuffer
        self._vbuffer = self._vertices.data.view(VertexBuffer)

        if self._ibuffer is not None:
            del self._ibuffer
        if self._indices is not None:
            self._ibuffer = self._indices.data.view(IndexBuffer)

        if self._utexture is not None:
            del self._utexture
        if self._uniforms is not None:
            # max_texsize = gl.glGetInteger(gl.GL_MAX_TEXTURE_SIZE)
            texture = self._uniforms.data.view(np.float32)
            rowsize = min(4096, texture.size//4)

            count = self._u_float_count
            cols = rowsize//(count/4)
            rows = (len(self) // cols)
            # rows = (len(self) // cols)+1
            shape = rows, cols*(count/4), count

            texture = texture.reshape(shape)
            self._utexture = texture.view(Texture2D)


    def append(self, vertices, indices=None, uniforms=None, itemsize=None):
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
        self.insert(len(self), vertices, indices, uniforms, itemsize)
