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
    """

    def __init__(self, *args, **kwargs):

        code = library.get("transforms/projection.glsl")

        self.aspect    = Transform._get_kwarg("aspect", kwargs) or None
        self.xinvert   = Transform._get_kwarg("xinvert", kwargs) or False
        self.yinvert   = Transform._get_kwarg("yinvert", kwargs) or False
        self.znear     = Transform._get_kwarg("znear", kwargs) or -1000
        self.zfar      = Transform._get_kwarg("znear", kwargs) or +1000
        self.normalize = Transform._get_kwarg("normalize", kwargs) or False
        Transform.__init__(self, code, *args, **kwargs)


    def on_resize(self, width, height):
        # Compute new Projection
        xmin, xmax = 0, width
        ymin, ymax = 0, height
        if self.normalize:
            xmin, xmax = -1, +1
            ymin, ymax = -1, +1
        if self.xinvert:
            xmin, xmax = xmax, xmin
        if self.yinvert:
            ymin, ymax = ymax, ymin

        aspect = self.aspect
        if aspect is not None:
            if aspect > 1.0:
                xmin *= (aspect*width)//height
                xmax *= (aspect*width)//height
            else:
                ymin /= (aspect*width)//height
                ymax /= (aspect*width)//height

        znear, zfar = self.znear, self.zfar
        self["projection"] = glm.ortho(xmin, xmax, ymin, ymax, znear, zfar)

        # Propagate event to children
        Transform.on_resize(self, width, height)
