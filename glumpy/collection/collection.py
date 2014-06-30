#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
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
from util import dtype_reduce
from array_list import ArrayList


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


    def _get_vertices(self):
        return self._vertices
    def _set_vertices(self, data):
        data = np.array(data)
        self._vertices[...] = data
    vertices = property(_get_vertices, _set_vertices)


    def _get_indices(self):
        return self._indices
    def _set_indices(self, data):
        data = np.array(data)
        # assert 0 <= data.min() <= data.max() < len(self._vertices)
        start = self._parent.vertices._items[self._key][0]
        self._indices[...] = data + start
    indices = property(_get_indices, _set_indices)


    def _get_uniforms(self):
        return self._uniforms
    def _set_uniforms(self, data):
        self._uniforms[...] = data
    uniforms = property(_get_uniforms, _set_uniforms)


    def __getitem__(self, key):
        """ Get a specific uniform value """
        return self._uniforms[key]


    def __setitem__(self, key, value):
        """ Set a specific uniform value """
        self._uniforms[key] = value


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

    def __init__(self, vtype, utype, itype=np.uint32 ):
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

        vtype = np.dtype(vtype)
        if vtype.names is None:
            raise ValueError("vtype must be a structured dtype")

        utype = np.dtype(utype)
        if utype.names is None:
            raise ValueError("utype must be a structured dtype")

        itype = np.dtype(itype)
        if itype not in [np.uint8, np.uint16, np.uint32]:
            raise ValueError("itype must be unsigned integer or None")

        # Convert types to lists (in case they were already dtypes) such that
        # we can append new fields
        #vtype = eval(str(np.dtype(vtype)))
        # We add a uniform index to access uniform data
        #vtype.append( ('a_index', 'f4') )
        #vtype = np.dtype(vtype)

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

        # Create relevant array lists
        self._vertices = ArrayList(dtype=vtype)
        self._indices = ArrayList(dtype=itype)
        self._uniforms = ArrayList(dtype=utype)


    @property
    def u_shape(self):
        """ Uniform texture shape """
        # max_texsize = gl.glGetInteger(gl.GL_MAX_TEXTURE_SIZE)
        max_texsize = 4096
        cols = max_texsize//(self._u_float_count/4)
        rows = (len(self) // cols)+1
        return rows, cols*(self._u_float_count/4), self._u_float_count


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

    @property
    def u_indices(self):
        """ Uniform texture indices """

        return np.repeat(np.arange(len(self)), self._vertices.itemsize)



    def __len__(self):
        """ """
        return len(self._vertices)



    def __getitem__(self, key):
        """ """

        V, U, I = self._vertices, self._uniforms, self._indices
        if V.dtype.names and key in V.dtype.names:
            return V[key]
        elif U.dtype.names and key in U.dtype.names:
            return U[key]
        else:
            return Item(self, key, V[key], I[key], U[key])



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
        # I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
        # self._vertices['a_index'] = I


    def insert(self, index, vertices, indices, uniforms=None, itemsize=None):
        """

        Parameters
        ----------

        index : int
            Index before which to insert data

        vertices : numpy array
            An array whose dtype is compatible with self.vertices.dtype

        indices : numpy array
            An array whose dtype is compatible with self.indices.dtype
            All index values must be between 0 and len(vertices)

        uniforms: numpy array
            An array whose dtype is compatible with self.uniforms.dtype

        itemsize:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.
        """

        # Make sure vertices/indices/uniforms are of the right dtype

        vtype = self._vertices.dtype
        vertices = np.array(vertices,copy=False).astype(vtype).ravel()

        itype = self._indices.dtype
        indices  = np.array(indices,copy=False).astype(itype).ravel()

        utype = self._uniforms.dtype
        if uniforms is not None:
            uniforms = np.array(uniforms,copy=False).astype(utype).ravel()

        # Check index
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("Collection insertion index out of range")

        # Inserting
        if index < len(self._vertices):
            vstart = self._vertices._items[index][0]
            istart = self._indices._items[index][0]
            ustart = self._uniforms._items[index][0]
        # Appending
        else:
            vstart = self._vertices.size
            istart = self._indices.size
            ustart = self._uniforms.size

        # Updating indices
        self._indices._data[istart:] += len(vertices)
        indices += vstart

        # Inserting one item
        if itemsize is None:
            #self._vertices[index:]['a_index'] += 1
            #vertices['a_index'] = index
            self._vertices.insert(index,vertices)
            self._indices.insert(index,indices)
            if uniforms is not None:
                self._uniforms.insert(index,uniforms)
            else:
                U = np.zeros(1,dtype=self._uniforms.dtype)
                self._uniforms.insert(index,U)

            # Update a_index at once
            # I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
            # self._vertices['a_index'] = I
            return

        # No item size specified
        if itemsize is None:
            v_itemcount = 1
            v_itemsize = np.ones(1,dtype=int)*vertices.size
            i_itemcount = 1
            i_itemsize = np.ones(1,dtype=int)*indices.size

        # Vertices size specified but no indices size
        if type(itemsize) is int:
            v_itemcount = vertices.size // itemsize
            v_itemsize = itemsize*np.ones(v_itemcount,dtype=int)

            i_itemcount = v_itemcount
            i_itemsize = len(indices)*np.ones(i_itemcount,dtype=int)
            indices = np.resize(indices, len(indices)*i_itemcount)

        # Vertices and indices size specified
        elif isinstance(itemsize, tuple):
            v_itemsize = itemsize[0]
            v_itemcount = vertices.size // v_itemsize
            v_itemsize = v_itemsize*np.ones(v_itemcount,dtype=int)

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
        if (indices.size % i_itemsize.sum()) != 0:
            raise ValueError("Cannot partition indices data as requested")
        if v_itemcount != i_itemcount:
            raise ValueError("Vertices/Indices item size not compatible")

        I = np.repeat(v_itemsize.cumsum(),i_itemsize)
        indices[i_itemsize[0]:] += I[:-i_itemsize[0]]
        self._vertices.insert(index, vertices, v_itemsize)
        self._indices.insert(index, indices, i_itemsize)
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
        I = np.repeat(np.arange(len(self)), self._vertices.itemsize)
        self._vertices['a_index'] = I



    def append(self, vertices, indices, uniforms=None, itemsize=None):
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



# if __name__ == '__main__':

#     vtype = [('position', 'f4', 2)]
#     utype = [('color',    'f4', 3)]
#     itype = np.uint32

#     vertices = np.zeros(4, dtype=vtype)
#     indices  = [0,1,2,0,2,3]
#     uniforms = np.zeros(1, dtype=utype)

#     C = Collection(vtype, utype, itype)
#     C.append(vertices, indices, uniforms)
#     C.append(vertices, indices, uniforms)
#     C.append(vertices, indices, uniforms)
#     del C[0]

#     print C[1].vertices
#     print C[1].indices
#     C[1]["color"] = 1,2,3
#     print C[1].uniforms
