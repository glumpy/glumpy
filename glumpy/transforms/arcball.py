# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from . transform import Transform
from glumpy import gl, glm, library


class Arcball(Transform):
    """
    3D arcball transform

    :param float aspect:
       Indicate what is the aspect ratio of the object displayed. This is
       necessary to convert pixel drag move in oject space coordinates.
       Default is None.

    :param float znear:
       Near clip plane. Default is 2.

    :param float zfar: 
       Distance clip plane. Default is 1000.

    :param float theta:
       Angle (in degrees) around the z axis. Default is 0.

    :param float phi: 
       Angle (in degrees) around the x axis. Default is 0.

    :param float distance:
       Distance from the arcball to the object.  Default is 8.

    :param float zoom:
           Zoom level. Default is 35.

    The arcball transform simulates a virtual arcball (3D) that can rotate
    around the origin using intuitive mouse gestures.

    The transform is connected to the following events:

      * ``on_attach``: Transform initialization
      * ``on_resize``: Tranform update to maintain aspect
      * ``on_mouse_scroll``: Zoom in & out (user action)
      * ``on_mouse_grab``: Drag (user action)

    **Usage example**:

      .. code:: python

         vertex = '''
         attribute vec2 position;
         void main()
         {
             gl_Position = <transform>(vec4(position, 0.0, 1.0));
         } '''

         ...
         window = app.Window(width=800, height=800)
         program = gloo.Program(vertex, fragment, count=4)
         ...
         program['transform'] = Arcball(aspect=1)
         window.attach(program['transform'])
         ...
    """

    aliases = { "view"       : "arcball_view",
                "model"      : "arcball_model",
                "projection" : "arcball_projection" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        """

        code = library.get("transforms/arcball.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._aspect = Transform._get_kwarg("aspect", kwargs) or 1
        self._znear = Transform._get_kwarg("znear", kwargs) or 2.0
        self._zfar = Transform._get_kwarg("zfar", kwargs) or 1000.0
        self._theta = Transform._get_kwarg("theta", kwargs) or 0
        self._phi = Transform._get_kwarg("phi", kwargs) or 0
        self._distance = Transform._get_kwarg("distance", kwargs) or 8
        self._zoom = Transform._get_kwarg("zoom", kwargs) or 35
        self._width = 1
        self._height = 1
        self._window_aspect = 1

        self._projection = np.eye(4, dtype=np.float32)
        self._view = np.eye(4, dtype=np.float32)
        self._model = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -abs(self._distance))


    @property
    def distance(self):
        """ Distance from the trackball to the object """

        return self._distance

    @distance.setter
    def distance(self, distance):
        """ Distance from the trackball to the object """

        self._distance = abs(distance)
        self._view = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -abs(self._distance))
        self["view"] = self._view


    @property
    def theta(self):
        """ Angle (in degrees) around the z axis """

        return self._theta

    @theta.setter
    def theta(self, theta):
        """ Angle (in degrees) around the z axis """

        self._theta = theta
        model = np.eye(4, dtype=np.float32)
        glm.rotate(model, self._theta, 0, 0, 1)
        glm.rotate(model, self._phi, 1, 0, 0)
        self["model"] = model

    @property
    def phi(self):
        """ Angle (in degrees) around the x axis """

        return self._trackball.phi

    @phi.setter
    def phi(self, phi):
        """ Angle (in degrees) around the x axis """

        self._phi = phi
        model = np.eye(4, dtype=np.float32)
        glm.rotate(model, self._theta, 0, 0, 1)
        glm.rotate(model, self._phi, 1, 0, 0)
        self["model"] = model


    @property
    def zoom(self):
        """ Zoom level (aperture angle in degrees) """

        return self._zoom


    @phi.setter
    def zoom(self, value):
        """ Zoom level (aperture angle in degrees) """

        aspect = self._window_aspect * self._aspect
        self._zoom = min(max(value, 1.0), 179.0)
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)

    @property
    def aspect(self):
        """ Projection aspect """

        return self._aspect


    @aspect.setter
    def aspect(self, value):
        """ Projection aspect """

        aspect = self._window_aspect * self._aspect
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)
    

    def on_attach(self, program):
        self["view"] = self._view
        self["model"] = self._model
        self["projection"] = self._projection


    def on_resize(self, width, height):
        self._width  = float(width)
        self._height = float(height)
        self._window_aspect = self._width / self._height
        aspect = self._window_aspect * self._aspect
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)
        Transform.on_resize(self, width, height)


    def on_mouse_drag(self, x, y, dx, dy, button):
        model = np.eye(4, dtype=np.float32)
        self._theta -= dx/5.0
        self._phi += dy/5.0
        glm.rotate(model, self._theta, 0, 0, 1)
        glm.rotate(model, self._phi, 1, 0, 0)
        self["model"] = model


    def on_mouse_scroll(self, x, y, dx, dy):
        width = self._width
        height = self._height
        aspect = self._window_aspect * self._aspect
        self._zoom = min(max(self._zoom*(1-dy/100), 1.0), 179.0)
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)
