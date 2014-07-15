# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
"""
import numpy as np
from glumpy.graphic.collection.util import dtype_reduce
from glumpy.graphic.collection.collection import Collection


class MarkerCollection(Collection):

    def __init__(self):
        self.vtype = np.dtype([('a_center', 'f4', 2)])
        self.utype = np.dtype([('u_color', 'f4', 4)])
        Collection.__init__(self, self.vtype, self.utype)

        shaders = os.path.join(os.path.dirname(__file__),'shaders')
        vertex_shader= os.path.join( shaders, 'circles.vert')
        fragment_shader= os.path.join( shaders, 'circles.frag')

        self.shader = Shader( open(vertex_shader).read(),
                              open(fragment_shader).read() )


    def append( self, center=(0,0) ):
        V, I = self.bake(center)
        U = np.zeros(1, self.utype)
        U['fg_color'] = 0,0,0,1
        Collection.append(self, V, I, U)


    # ---------------------------------
    def bake(self, center ):
        V = np.zeros(1, dtype=self.vtype)
        V['a_center'] = center
        return V, None


    # ---------------------------------
    def draw(self):
        if self._dirty:
            self.upload()

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)
        _,_,width,height = gl.glGetIntegerv( gl.GL_VIEWPORT )
        P = orthographic( 0, width, 0, height, -1, +1 )
        V = np.eye(4).astype( np.float32 )
        M = np.eye(4).astype( np.float32 )

        shader = self.shader
        shader.bind()
        gl.glActiveTexture( gl.GL_TEXTURE0 )
        shader.uniformi( 'u_uniforms', 0 )
        gl.glBindTexture( gl.GL_TEXTURE_2D, self._ubuffer_id )
        if self.dash_atlas:
            gl.glActiveTexture( gl.GL_TEXTURE1 )
            shader.uniformi('u_dash_atlas', 1)
            gl.glBindTexture( gl.GL_TEXTURE_2D, self.dash_atlas.texture_id )
        shader.uniform_matrixf( 'u_M', M )
        shader.uniform_matrixf( 'u_V', V )
        shader.uniform_matrixf( 'u_P', P )
        shape = self._ubuffer_shape
        shader.uniformf( 'u_uniforms_shape', shape[1]//4, shape[0])
        self._vbuffer.draw( )
        shader.unbind()
