# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from . transform import Transform
from glumpy import gl, glm, library


class PVMProjection(Transform):
    """
    Perspective projection is an approximate representation, on a flat surface
    of an image as it is seen by the eye. The two most characteristic features
    of perspective are that objects are smaller as their distance from the
    observer increases; and that they are subject to foreshortening, meaning
    that an object's dimensions along the line of sight are shorter than its
    dimensions across the line of sight.

    :param float distance:
       Distance of the camera to the origin. Default is 5.

    :param bool fovy: 
       Field of view along y axis. Default is 40.

    :param int znear: 
       Z near clipping place. Default is 2.

    :param int zfar: 
       Z far clipping place. Default is 100.
    """

    
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/pvm.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._fovy = 40
        self._znear, self._zfar = 2.0, 100.0
        self._view = np.eye(4, dtype=np.float32)
        self._model = np.eye(4, dtype=np.float32)
        self._projection = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -5)

    def on_attach(self, program):
        self["view"] = self._view
        self["model"] = self._model
        self["projection"] = self._projection

    def on_resize(self, width, height):
        fovy = self._fovy
        aspect = width / float(height)
        znear, zfar = self._znear, self._zfar
        self['projection'] = glm.perspective(fovy, aspect, znear, zfar)
