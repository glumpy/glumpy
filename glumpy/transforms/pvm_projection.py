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

    The transform is connected to the following events:

      * ``on_attach``: Transform initialization
      * ``on_resize``: Recompute projection matrix

    **Usage example**

      .. code:: python

         vertex = '''
         attribute vec3 position;
         attribute vec4 color;
         void main()
         {
             v_color = color;
             gl_Position = <transform>;
         } '''

         fragment = '''
         varying vec4 v_color;
         void main()
         {
             gl_FragColor = v_color;
         } '''

         window = app.Window()

         @window.event
         def on_draw(dt):
             global phi, theta
             window.clear()
             cube.draw(gl.GL_TRIANGLES, I)

             theta += 0.5 # degrees
             phi += 0.5 # degrees
             model = np.eye(4, dtype=np.float32)
             glm.rotate(model, theta, 0, 0, 1)
             glm.rotate(model, phi, 0, 1, 0)
             cube['transform']['model'] = model

         V, I, O = colorcube()
         cube = gloo.Program(vertex, fragment)
         cube.bind(V)
         cube['transform'] = PVMProjection(Position("position"))
         window.attach(cube['transform'])

         phi, theta = 0, 0
         app.run()
    
    
    """

    
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/pvm.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._width     = None
        self._height    = None
        self._distance = Transform._get_kwarg("distance", kwargs) or 5
        self._fovy     = Transform._get_kwarg("fovy", kwargs) or 40
        self._znear    = Transform._get_kwarg("znear", kwargs) or 2.0
        self._zfar     = Transform._get_kwarg("znear", kwargs) or 100.0
        self._view = np.eye(4, dtype=np.float32)
        self._model = np.eye(4, dtype=np.float32)
        self._projection = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -self._distance)


    @property
    def view(self):
        """ View matrix """

        return self._view

    @property
    def model(self):
        """ Model matrix """

        return self._model

    @property
    def projection(self):
        """ Projection matrix """

        return self._projection

    @property
    def distance(self):
        """ Distance of the camera to the origin """

        return self._distance

    @distance.setter
    def distance(self, value):
        """ Distance of the camera to the origin """

        if value > 1:
            self._distance = value
            self._view = np.eye(4, dtype=np.float32)
            glm.translate(self._view, 0, 0, -self._distance)
            self["view"] = self._view

    @property
    def fovy(self):
        """ Field of view along y axis """

        return self._fovy

    @fovy.setter
    def fovy(self, value):
        """ Field of view along y axis """

        if 0 < fovy < 90:
            self._fovy = value
            self._build_projection()

    @property
    def znear(self):
        """ Z near clipping place """

        return self._znear

    @znear.setter
    def znear(self, value):
        """ Z near clipping place """

        if value < self._zfar:
            self._znear = value
            self._build_projection()

        
    @property
    def zfar(self):
        """ Z far clipping place """
        return self._znear

    @zfar.setter
    def zfar(self, value):
        """ Z near clipping place """

        if value > self._znear:
            self._zfar = value
            self._build_projection()

    def on_attach(self, program):
        self["view"] = self._view
        self["model"] = self._model
        self["projection"] = self._projection


    def on_resize(self, width, height):
        self._width  = width
        self._height = height

        # Build projection matrix
        self._build_projection()
        
        # Propagate event to children
        Transform.on_resize(self, width, height)
        
    def _build_projection(self):
        # We need to have caught at least one resize event
        if self._width is None: return

        aspect = self._width / float(self._height)
        self['projection'] = glm.perspective(self.fovy, aspect,
                                             self._znear, self._zfar)
