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
from glumpy.gloo.buffer import VertexBuffer
from glumpy.graphics.collection.array_list import ArrayList


class Item(object):
    """
    An item represent an object within a collection and is created on demand
    when accessing a specific object of the collection.
    """

    def __init__(self, parent, key, vertices):
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
        """

        self._parent   = parent
        self._vertices = vertices


    @property
    def vertices(self):
        return self._vertices


    @vertices.setter
    def vertices(self, data):
        data = np.array(data)
        self._vertices[...] = data


    def __getitem__(self, key):
        """ Get a specific uniform value """
        return self._vertices[key]


    def __setitem__(self, key, value):
        """ Set a specific uniform value """

        self._vertices[key] = value

    def __str__(self):
        return "Item (%s)" % (self._vertices)



class Collection(object):
    """
    A collection is a container for several objects having the same vertex
    structure (vtype).

    Parameters
    ----------

    vtype: np.dtype
        Vertices data type
    """

    def __init__(self, vtype):

        vtype = np.dtype(vtype)
        if vtype.names is None:
            raise ValueError("vtype must be a structured dtype")
        self._vertices = ArrayList(dtype=vtype)
        self._vbuffer = None


    @property
    def vertices(self):
        """ Vertices buffer """

        return self._vertices


    def __len__(self):
        """ x.__len__() <==> len(x) """

        return len(self._vertices)


    def __getitem__(self, key):
        """ x.__getitem__(y) <==> x[y] """

        if key in self._vertices.dtype.names:
            return self._vertices[key]
        else:
            return Item(self, key, self._vertices[key])


    def __setitem__(self, key, data):
        """ """

        # Setting vertices field at once
        if key in self._vertices.dtype.names:
            self._vertices.data[key] = data

        # Setting individual item
        else:
            del self[key]
            self.insert(key, data)


    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """

        del self._vertices[key]


    def insert(self, index, vertices, itemsize=None):
        """
        Parameters
        ----------

        index : int
            Index before which to insert data

        vertices : numpy array
            An array whose dtype is compatible with self.vertices.dtype

        itemsize:  int or 1-D array
            If `itemsize is an integer, N, the array will be divided into
            elements of size N. If such partition is not possible, an error is
            raised.

            If `itemsize` is 1-D array, the array will be divided into elements
            whose succesive sizes will be picked from itemsize.  If the sum of
            itemsize values is different from array size, an error is raised.
        """

        # Make sure vertices is of the right dtype
        vtype = self._vertices.dtype
        vertices = np.array(vertices,copy=False).astype(vtype).ravel()

        # Check index
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("Collection insertion index out of range")

        # Inserting
        if index < len(self._vertices):
            vstart = self._vertices._items[index][0]
        # Appending
        else:
            vstart = self._vertices.size

        # Inserting one item
        if itemsize is None:
            self._vertices.insert(index,vertices)

        # No item size specified
        if itemsize is None:
            v_itemcount = 1
            v_itemsize = np.ones(1,dtype=int)*vertices.size

        # Vertices size specified
        if type(itemsize) is int:
            v_itemcount = vertices.size // itemsize
            v_itemsize = itemsize*np.ones(v_itemcount,dtype=int)

        # Vertices have different size
        else:
            itemsize = np.array(itemsize, copy=False)
            v_itemsize = itemsize[:,0]

        # Sanity check
        if (vertices.size % v_itemsize.sum()) != 0:
            raise ValueError("Cannot partition vertices data as requested")

        self._vertices.insert(index, vertices, v_itemsize)


    def append(self, vertices, itemsize=None):
        """

        Parameters
        ----------

        vertices : numpy array
            An array whose dtype is compatible with self.vertices.dtype

        itemsize: int, tuple or 1-D array
            If `itemsize is an integer, N, the array will be divided
            into elements of size N. If such partition is not possible,
            an error is raised.

            If `itemsize` is 1-D array, the array will be divided into
            elements whose succesive sizes will be picked from itemsize.
            If the sum of itemsize values is different from array size,
            an error is raised.

        """
        self.insert(len(self), vertices, itemsize)
