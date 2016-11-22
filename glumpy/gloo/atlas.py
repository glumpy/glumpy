# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
A Texture atlas allows to group multiple small data regions into a larger
texture.

The algorithm is based on the article by Jukka Jylänki : "A Thousand Ways
to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin
Packing", February 27, 2010. More precisely, this is an implementation of
the Skyline Bottom-Left algorithm based on C++ sources provided by Jukka
Jylänki at: http://clb.demon.fi/files/RectangleBinPack/

Example usage:
--------------
"""
import sys
from glumpy.log import log
from . texture import Texture2D


class Atlas(Texture2D):
    """ Texture Atlas (two dimensional)

    Parameters

    data : ndarray
        Texture data (optional)

    shape : tuple of integers
        Texture shape (optional)

    dtype : dtype
        Texture data type (optional)

    store : bool
        Specify whether this object stores a reference to the data,
        allowing the data to be updated regardless of striding. Note
        that modifying the data after passing it here might result in
        undesired behavior, unless a copy is given. Default True.

    format : ENUM
        The format of the texture: GL_LUMINANCE, ALPHA, GL_LUMINANCE_ALPHA,
        or GL_RGB, GL_RGBA. If not given the format is chosen automatically
        based on the number of channels. When the data has one channel,
        GL_LUMINANCE is assumed.
    """


    def __init__(self):
        Texture2D.__init__(self)
        self.nodes  = [(0,0,self.width),]
        self.used   = 0


    def allocate(self, shape):
        """
        Allocate a new region of given shape.

        Parameters
        ----------

        shape : (int,int)
            Shape of region  as (heigth, width)

        Return
        ------
            Texture2D or None
        """

        height, width = shape
        best_height = sys.maxsize
        best_index = -1
        best_width = sys.maxsize
        region = 0, 0, width, height

        for i in range(len(self.nodes)):
            y = self._fit(i, width, height)
            if y >= 0:
                node = self.nodes[i]
                if (y+height < best_height or
                    (y+height == best_height and node[2] < best_width)):
                    best_height = y+height
                    best_index = i
                    best_width = node[2]
                    region = node[0], y, width, height

        if best_index == -1:
            log.warn("No enough free space in atlas")
            return None

        node = region[0], region[1]+height, width
        self.nodes.insert(best_index, node)

        i = best_index+1
        while i < len(self.nodes):
            node = self.nodes[i]
            prev_node = self.nodes[i-1]
            if node[0] < prev_node[0]+prev_node[2]:
                shrink = prev_node[0]+prev_node[2] - node[0]
                x,y,w = self.nodes[i]
                self.nodes[i] = x+shrink, y, w-shrink
                if self.nodes[i][2] <= 0:
                    del self.nodes[i]
                    i -= 1
                else:
                    break
            else:
                break
            i += 1

        self._merge()
        self.used += width*height
        x,y,width,height = region
        return region
        # return self[y:y+height, x:x+width]
        # return self[x:x+width, y:y+height]



    def _fit(self, index, width, height):
        """
        Test if region (width,height) fit into self.nodes[index]

        Parameters
        ----------

        index : int
            Index of the internal node to be tested

        width : int
            Width or the region to be tested

        height : int
            Height or the region to be tested
        """

        node = self.nodes[index]
        x,y = node[0], node[1]
        width_left = width

        if x+width > self.width:
            return -1

        i = index
        while width_left > 0:
            node = self.nodes[i]
            y = max(y, node[1])
            if y+height > self.height:
                return -1
            width_left -= node[2]
            i += 1
        return y


    def _merge(self):
        """ Merge nodes. """

        i = 0
        while i < len(self.nodes)-1:
            node = self.nodes[i]
            next_node = self.nodes[i+1]
            if node[1] == next_node[1]:
                self.nodes[i] = node[0], node[1], node[2]+next_node[2]
                del self.nodes[i+1]
            else:
                i += 1
