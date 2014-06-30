#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from collection import Collection


# Vertices dtype
vtype = [('position', 'f4', 2)]

# Uniforms dtype
utype = [('color',    'f4', 3)]

# Inidces dtype
itype = np.uint32

# Creates empty collection
C = Collection(vtype, utype, itype)

# Add one item (4 vertices, 6 indices, 1 uniform)
vertices = np.zeros(4, dtype=vtype)
indices  = [0,1,2,0,2,3]
uniforms = np.zeros(1, dtype=utype)
C.append(vertices, indices, uniforms)

# Add another item
# In such case, indices are updated such that they point to the right
# set of vertices within the global buffer
C.append(vertices, indices, uniforms)

# Each item can be manipulated individually
print C[0].vertices
print C[0].indices
print C[0].uniforms

# or globally:
C['position'] = 0
C['color'] = 0,0,1


# How to render ?
# C.vertices must be bound to a vertex buffer
# C.indices must be bound to an element vertex buffer
# C.uniforms must be upload as a texture with shape C.u_shape[:2]
#
# C.u_shape must be bound to u_uniforms_shape within shader
# Code from util.generate_shader() must prepended to vertex shader code

