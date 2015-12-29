# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import library
from . transform import Transform


class Viewport(Transform):
    """
    Viewport transform

    :param bool transform:
        Whether to enforce viewport transformation. Default is true.

    :param nool clipping: 
        Whether to enforce viewport clipping. Default is true.

    :param tuple viewport:
        Viewport (x,y,w,h) in absolute window coordinates. Default is None.


    The viewport transform allows to restrict the display of a scene to a local
    viewport.

    The transform is connected to the following events:

      * ``on_attach``: Transform initialization
      * ``on_resize``: Tranform update to maintain aspect

    **Usage example**:

      .. code:: python

         vertex = '''
         attribute vec2 position;
         void main()
         {
             ... 
             gl_Position = vec4(position,0,1);
             <viewport.transform>;
         } '''

         fragment = '''
         void main()
         {
             <viewport.clipping>;
             ...
             gl_FragColor = vec4(1,0,0,1);
         } '''
 
         window = app.Window(400,400)
         ...
         program = Program(vertex, fragment)
         program["viewport"] = transforms.Viewport(viewport=(10,10,390,390))
         window.attach(program["viewport"])
         ...
    """

    aliases = { "clipping"  : "viewport_clipping",
                "transform" : "viewport_transform",
                "local"     : "viewport_local",
                "extents"   : "viewport_local",
                "global"    : "viewport_global" }

    def __init__(self, code=None, *args, **kwargs):
        if code is None:
            code = library.get("transforms/viewport.glsl")

        self._global = 0,0,512,512
        self._local = Transform._get_kwarg("viewport", kwargs) or None
        self._clipping = Transform._get_kwarg("clipping", kwargs) or True
        self._transform = Transform._get_kwarg("transform", kwargs) or True

        Transform.__init__(self, code, *args, **kwargs)



    @property
    def extents(self):
        """ Viewport extents as (x,y,w,h) (absolute coordinates) """

        return self._local


    @extents.setter
    def extents(self, value):
        """ Viewport extents as (x,y,w,h) (absolute coordinates) """

        self._local = value
        if self.is_attached:
            if self._local is None:
                self["local"] = self._global
            else:
                self["local"] = self._local
            self["clipping"] = self._clipping
            self["transform"] = self._transform


    @property
    def clipping(self):
        """ Whether to enforce viewport clipping """

        return self._clipping


    @clipping.setter
    def clipping(self, value):
        """ Whether to enforce viewport clipping """

        self._clipping = value
        if self.is_attached:
            self["clipping"] = self._clipping


    @property
    def transform(self):
        """ Whether to enforce viewport transform """

        return self._transform


    @transform.setter
    def transform(self, value):
        """ Whether to enforce viewport transform """

        self._transform = value
        if self.is_attached:
            self["transform"] = self._transform



    def on_attach(self, program):
        self["global"] = self._global
        if self._local is None:
            self["local"] = self._global
        else:
            self["local"] = self._local
        self["clipping"] = self._clipping
        self["transform"] = self._transform


    def on_resize(self, width, height):
        self._global = 0, 0, width, height
        self["global"] = self._global
        if self._local is None:
            self["local"] = self._global

        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)
