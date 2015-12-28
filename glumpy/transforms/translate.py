# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import library
from glumpy.transforms.transform import Transform


class Translate(Transform):
    """
    Translation transform

    :param 3-tuple translate:
       Translation vector. Default is (0,0,0).

    The transform is connected to the following events:

      * ``on_attach``: Transform initialization

    **Usage example**:

      .. code:: python

         vertex = '''
         attribute vec2 position;
         void main()
         {
             gl_Position = <transform>;
         } '''

         ...
         window = app.Window(width=800, height=800)
         program = gloo.Program(vertex, fragment, count=4)
         ...
         program['transform'] = Translate("position", translate=(0,0,0))
         window.attach(program['transform'])
         ...
    """

    aliases = { "translate" : "translate_translate" }


    def __init__(self, *args, **kwargs):
        code = library.get("transforms/translate.glsl")
        Transform.__init__(self, code, *args, **kwargs)
        self.translate = Transform._get_kwarg("translate", kwargs) or (0,0,0)


    @property
    def translate(self):
        """ Translate vector """

        return self._translate


    @translate.setter
    def translate(self, value):
        """ Translate vector """

        self._translate = np.asarray(value,dtype=np.float32)
        if self.is_attached:
            self["translate"] = self._translate


    def on_attach(self, program):
        self["translate"] = self._translate
