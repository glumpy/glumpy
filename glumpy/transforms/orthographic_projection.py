# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import glm, library
from . transform import Transform

class OrthographicProjection(Transform):
    """
    Orthographic projection (or orthogonal projection) is a means of
    representing a three-dimensional object in two dimensions. It is a form of
    parallel projection, where all the projection lines are orthogonal to the
    projection plane, resulting in every plane of the scene appearing in
    affine transformation on the viewing surface.

    :param float aspect: 
       Aspect ratio (width/height). Default is None.

    :param bool xinvert:
       Whether to invert X axis. Default is False.

    :param bool yinvert: 
       Whether to invert Y axis. Default is False.

    :param int znear: 
       Z near clipping place. Default is -1000.

    :param int zfar: 
       Z far clipping place. Default is +1000.

    :param bool normalize: 
       Whether to use normalized device coordinates. Default is False

    The transform is connected to the following events:

      * ``on_attach``: Transform initialization
      * ``on_resize``: Recompute projection matrix


    **Usage example**

      .. code:: python

         vertex = '''
         attribute vec2 position;
         void main()
         {
             gl_Position = <transform>;
         } '''
         fragment = '''
         void main()
         {
             gl_FragColor = vec4(1,0,0,1);
         } '''

         window = app.Window()
       
         @window.event
         def on_draw(dt):
             window.clear()
             quad.draw(gl.GL_TRIANGLE_STRIP)

         @window.event
         def on_resize(w, h):
             quad['position'] = [(w-100,h-100), (w-100,h), (w,h-100), (w,h)]

         quad = gloo.Program(vertex, fragment, count=4)
         quad["transform"] = OrthographicProjection(Position("position"))
         window.attach(quad["transform"])
         app.run()
    """

    def __init__(self, *args, **kwargs):

        code = library.get("transforms/projection.glsl")

        self._width     = None
        self._height    = None
        self._aspect    = Transform._get_kwarg("aspect", kwargs) or None
        self._xinvert   = Transform._get_kwarg("xinvert", kwargs) or False
        self._yinvert   = Transform._get_kwarg("yinvert", kwargs) or False
        self._znear     = Transform._get_kwarg("znear", kwargs) or -1000
        self._zfar      = Transform._get_kwarg("znear", kwargs) or +1000
        self._normalize = Transform._get_kwarg("normalize", kwargs) or False
        Transform.__init__(self, code, *args, **kwargs)

        
    @property
    def aspect(self):
        """ Aspect ratio """
        
        return self._aspect

    @aspect.setter
    def aspect(self, value):
        """ Aspect ratio """
        
        self._aspect = value
        self._build_projection()

    @property
    def normalize(self):
        """ Whether to use normalized coordinates """
        
        return self._normalize

    @normalize.setter
    def normalize(self, value):
        """ Whether to use normalized coordinates """
        
        self._normalize = value
        self._build_projection()

    @property
    def xinvert(self):
        """ Whether to invert x axis """
        
        return self._xinvert

    @xinvert.setter
    def xinvert(self, value):
        """ Whether to invert x axis """
        
        self._xinvert = value
        self._build_projection()

    @property
    def yinvert(self):
        """ Whether to invert y axis """

        return self._xinvert

    @yinvert.setter
    def yinvert(self, value):
        """ Whether to invert y axis """

        self._yinvert = value
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
        
        # Compute new Projection
        xmin, xmax = 0, self._width
        ymin, ymax = 0, self._height
        if self._normalize:
            xmin, xmax = -1, +1
            ymin, ymax = -1, +1
        if self._xinvert:
            xmin, xmax = xmax, xmin
        if self._yinvert:
            ymin, ymax = ymax, ymin

        aspect = self._aspect
        if aspect is not None:
            if aspect > 1.0:
                xmin *= (aspect*self._width)/self._height
                xmax *= (aspect*self._width)/self._height
            else:
                ymin /= (aspect*self._width)/self._height
                ymax /= (aspect*self._width)/self._height

        znear, zfar = self._znear, self._zfar
        self["projection"] = glm.ortho(xmin, xmax, ymin, ymax, znear, zfar)
