# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
A collection is a container for several (optionally indexed) objects having
the same vertex structure (vtype) and same uniforms type (utype). A collection
allows to manipulate objects individually and each object can have its own set
of uniforms provided they are a combination of floats.
"""
import math
import numpy as np
from glumpy import gl
from glumpy.gloo.texture import Texture2D
from glumpy.gloo.buffer import VertexBuffer, IndexBuffer
from glumpy.graphics.collection.util import dtype_reduce
from glumpy.graphics.collection.array_list import ArrayList



class Item(object):
    """
    An item represent an object within a collection and is created on demand
    when accessing a specific object of the collection.
    """

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





class BaseCollection(object):
    """
    A collection is a container for several objects having the same vertex
    structure (vtype) and same uniforms type (utype). A collection allows to
    manipulate objects individually and each object can have its own set of
    uniforms provided they are a combination of floats.

    Parameters
    ----------

    vtype: np.dtype
        Vertices data type

    utype: np.dtype or None
        Uniforms data type

    itype: np.dtype or None
        Indices data type
    """

    def __init__(self, vtype, utype=None, itype=None):

        # Vertices and type (mandatory)
        self._vertices_list = None
        self._vertices_buffer = None

        # Vertex indices and type (optional)
        self._indices_list = None
        self._indices_buffer = None

        # Uniforms and type (optional)
        self._uniforms_list = None
        self._uniforms_texture = None

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
            self._indices_list = ArrayList(dtype=itype)

        # No program yet
        self._program = None

        # We should use this line but we may not have a GL context yet
        # self._max_texture_size = gl.glGetInteger(gl.GL_MAX_TEXTURE_SIZE)
        self._max_texture_size = 1024


        # Uniforms type (optional)
        # -------------------------
        if utype is not None:
            if utype.names is None:
                raise ValueError("utype must be a structured dtype")

            # Convert types to lists (in case they were already dtypes) such that
            # we can append new fields
            vtype = eval(str(np.dtype(vtype)))
            # We add a uniform index to access uniform data
            vtype.append( ('collection_index', 'f4') )
            vtype = np.dtype(vtype)

            # Check utype is made of float32 only
            utype = eval(str(np.dtype(utype)))
            r_utype = dtype_reduce(utype)
            if type(r_utype[0]) is not str or r_utype[2] != 'float32':
                raise RuntimeError("utype cannot be reduced to float32 only")

            # Make utype divisible by 4
            count = ((r_utype[1]-1)//4+1)*4
            if (count - r_utype[1]) > 0:
                utype.append(('__unused__', 'f4', count-r_utype[1]))
            self._uniforms_list  = ArrayList(dtype=utype)
            self._uniforms_float_count = count
            self._compute_ushape(1)
            self._uniforms_list.reserve( self._ushape[1] / (count/4) )

        # Last since utype may add a new field in vtype (collecion_index)
        self._vertices_list  = ArrayList(dtype=vtype)



    def _compute_ushape(self, size=1):
        """ Compute uniform texture shape """

        texsize = self._max_texture_size
        count = self._uniforms_float_count
        cols = texsize//(count/4)
        rows = (size // cols)+1
        self._ushape = rows, cols*(count/4), count
        return self._ushape



    def _build_buffers(self):
        """ """

        if self._vertices_buffer is not None:
            self._vertices_buffer._delete()
        self._vertices_buffer = self._vertices_list.data.view(VertexBuffer)

        if self._indices_list is not None:
            if self._indices_buffer is not None:
                self._indices_buffer._delete()
            self._indices_buffer = self._indices_list.data.view(IndexBuffer)

        if self._uniforms_list is not None:
            if self._uniforms_texture is not None:
                self._uniforms_texture._delete()
            shape = self._compute_ushape(len(self))
            # We take the whole array (_data), not the data one
            texture = self._uniforms_list._data.view(np.float32)
            texture = texture.reshape(shape[0],shape[1],4)
            self._uniforms_texture = texture.view(Texture2D)
            self._uniforms_texture.interpolation =  gl.GL_NEAREST

        if self._program is not None:
            self._program.bind(self._vertices_buffer)
            if self._uniforms_list is not None:
                self._program["uniforms"] = self._uniforms_texture
                self._program["uniforms_shape"] = self._ushape



    @property
    def vtype(self):
        """ Vertices dtype """

        return self._vertices_list.dtype


    @property
    def itype(self):
        """ Indices dtype """

        if self._indices_list is not None:
            return self._indices_list.dtype
        return None


    @property
    def utype(self):
        """ Uniforms dtype """

        if self._uniforms_list is not None:
            return self._uniforms_list.dtype
        return None


    def __len__(self):
        """ """
        return len(self._vertices_list)


    def __getitem__(self, key):
        """ """

        # WARNING
        # Here we want to make sure to use buffers and texture (instead of
        # lists) since only them are aware of any external modification.

        V = self._vertices_buffer
        I = None
        U = None
        if self._indices_list is not None:
            I = self._indices_buffer
        if self._uniforms_list is not None:
            U = self._uniforms_texture.ravel().view(self.utype)

        # Getting a whole field
        if isinstance(key, str):
            # Getting a named field from vertices
            if key in V.dtype.names:
                return V[key]
            # Getting a named field from uniforms
            elif U is not None and key in U.dtype.names:
                return U[key]
            else:
                raise IndexError("Unknonw field name ('%s')" % key)

        # Getting individual item
        elif isinstance(key, int):
            vstart, vend = self._vertices_list._items[key]
            vertices = V[vstart:vend]
            indices = None
            uniforms = None
            if I is not None:
                istart, iend = self._indices_list._items[key]
                indices  = I[istart:iend]

            if U is not None:
                ustart, uend = self._uniforms_list._items[key]
                uniforms  = U[ustart:uend]

            return Item(self, key, vertices, indices, uniforms)

        # Error
        else:
            raise IndexError("Cannot get more than one item at once")


    def __setitem__(self, key, data):
        """ x.__setitem__(i, y) <==> x[i]=y """

        # WARNING
        # Here we want to make sure to use buffers and texture (instead of
        # lists) since only them are aware of any external modification.

        V = self._vertices_buffer
        I = None
        U = None
        if self._indices_list is not None:
            I = self._indices_buffer
        if self._uniforms_list is not None:
            U = self._uniforms_texture.ravel().view(self.utype)

        # Setting a whole field
        if isinstance(key, str):
            # Setting a named field in vertices
            if key in self.vtype.names:
                V[key] = data
            # Setting a named field in uniforms
            elif self.utype and key in self.utype.names:
                U[key] = data
            else:
                raise IndexError("Unknonw field name ('%s')" % key)

        # # Setting individual item
        # elif isinstance(key, int):
        #     #vstart, vend = self._vertices_list._items[key]
        #     #istart, iend = self._indices_list._items[key]
        #     #ustart, uend = self._uniforms_list._items[key]
        #     vertices, indices, uniforms = data
        #     del self[key]
        #     self.insert(key, vertices, indices, uniforms)

        else:
            raise IndexError("Cannot set more than one item")



    def __delitem__(self, index):
        """ x.__delitem__(y) <==> del x[y] """

        # WARNING
        # Here we want to make sure to use buffers and texture (instead of
        # lists) since only them are aware of any external modification.

        # Deleting one item
        if isinstance(index, int):
            if index < 0:
                index += len(self)
            if index < 0 or index > len(self):
                raise IndexError("Collection deletion index out of range")
            istart, istop = index, index+1

        # Deleting several items
        elif isinstance(index, slice):
            istart, istop, _ = index.indices(len(self))
            if istart > istop:
                istart, istop = istop,istart
            if istart == istop:
                return

        # Deleting everything
        elif index is Ellipsis:
            istart, istop = 0, len(self)

        # Error
        else:
            raise TypeError("Collection deletion indices must be integers")

        vsize = len(self._vertices_list[index])
        if self._indices_list is not None:
            del self._indices_list[index]
            self._indices_list[index] -= vsize
        del self._vertices_list[index]
        if self._uniforms_list is not None:
            del self._uniforms_list[index]

        # Update collection_index at once
        if self._uniforms_list is not None:
            I = np.repeat(np.arange(len(self)), self._vertices_list.itemsize)
            self._vertices_list['collection_index'] = I.astype(np.float32)


        # It is not strictly necessary to build new buffers each time an
        # item is deleted, but it would complexify even more this already
        # complex object.
        self._build_buffers()



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

        vtype = self.vtype
        vertices = np.array(vertices,copy=False).astype(vtype).ravel()

        # Sanity checks
        # -------------
        if indices is not None and self._indices_list is None:
            raise RuntimeError("Collection has been created without indices")
        elif indices is None and self._indices_list is not None:
            indices = np.arange(len(vertices), dtype=self.itype)
            #raise RuntimeError("Items must be provided with indices")

        if uniforms is not None and self._uniforms_list is None:
            raise RuntimeError("Collection has been created without uniforms")
        elif uniforms is None and self._uniforms_list is not None:
            raise RuntimeError("Items must be provided with uniforms")

        if indices is not None:
            itype = self.itype
            indices = np.array(indices,copy=False).astype(itype).ravel()

        if uniforms is not None:
            utype = self.utype
            uniforms = np.array(uniforms,copy=False).astype(utype).ravel()

        # Check index
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("Collection insertion index out of range")

        # Inserting
        if index < len(self._vertices_list):
            vstart = self._vertices_list._items[index][0]
            if self._indices_list is not None:
                istart = self._indices_list._items[index][0]
            if self._uniforms_list is not None:
                ustart = self._uniforms_list._items[index][0]
        # Appending
        else:
            vstart = self._vertices_list.size
            if self._indices_list is not None:
                istart = self._indices_list.size
            if self._uniforms_list is not None:
                ustart = self._uniforms_list.size

        # Updating indices
        if self._indices_list is not None:
            self._indices_list._data[istart:] += len(vertices)
            indices += vstart

        # Inserting one item
        if itemsize is None:
            self._vertices_list.insert(index,vertices)
            if self._indices_list is not None:
                self._indices_list.insert(index,indices)
            if self._uniforms_list is not None:
                if uniforms is not None:
                    self._uniforms_list.insert(index,uniforms)
                else:
                    U = np.zeros(1,dtype=self.utype)
                    self._uniforms_list.insert(index,U)

            # Update a_index at once
            if self._uniforms_list is not None:
                I = np.repeat(np.arange(len(self)), self._vertices_list.itemsize)
                self._vertices_list['collection_index'] = I.astype(np.float32)

            # It is not strictly necessary to build new buffers each time an
            # item is inserted, but it would complexify even more this already
            # complex object.
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

        self._vertices_list.insert(index, vertices, v_itemsize)

        if self._indices_list is not None:
            I = np.repeat(v_itemsize.cumsum(),i_itemsize)
            indices[i_itemsize[0]:] += I[:-i_itemsize[0]]
            self._indices_list.insert(index, indices, i_itemsize)

        if self._uniforms_list is not None:
            if uniforms is None:
                U = np.zeros(v_itemcount,dtype=self.utype)
                self._uniforms_list.insert(index,U, itemsize=1)
            else:
                if len(uniforms) != v_itemcount:
                    if len(uniforms) == 1:
                        U = np.resize(uniforms, v_itemcount)
                        self._uniforms_list.insert(index, U, itemsize=1)
                    else:
                        raise ValueError("Vertices/Uniforms item number not compatible")
                else:
                    self._uniforms_list.insert(index, uniforms, itemsize=1)

        # Update collection_index at once
        if self._uniforms_list is not None:
            I = np.repeat(np.arange(len(self)), self._vertices_list.itemsize)
            self._vertices_list['collection_index'] = I.astype(np.float32)

        # It is not strictly necessary to build new buffers each time an item
        # is inserted, but it would complexify even more this already complex
        # object.
        self._build_buffers()



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



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    vtype = [('position', 'f4', 2)]
    utype = [('color', 'f4', 3)]
    itype = np.uint32

    C = BaseCollection(vtype, utype, itype)

    for i in range(4):
        V = np.zeros(i+1,vtype)
        I = np.arange(i+1)
        V['position'] = i
        U = np.zeros(1,utype)
        U['color'] = i
        C.append(V, U, I)

    print C._vertices_buffer._pending_data
    C._vertices_buffer._pending_data = None
    print C._vertices_buffer._pending_data

#    C['position'] = -1,-1
#    print C._vertices_buffer._pending_data

    for i in range(4):
        print C[i]
    print
    del C[:3]
    print C[0]
    print C._vertices_buffer._pending_data
