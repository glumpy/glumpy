# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import library
from . transform import Transform


class Position(Transform):
    """
    Generic position transform

    The position transform is a convenient transform that takes any positional
    format and transform it in a vec4 format. It wotks thanks to GLSL function
    overloading.

    **Usage example**:

      .. code:: python

         vertex = '''
         attribute vec2 position;
         void main()
         {
             ... 
             gl_Position = <transform>;
         } '''

         fragment = ...
 
         window = app.Window(400,400)
         ...
         program = Program(vertex, fragment)
         program["transform"] = Position("position")
         # or program["transform"] = Position("position.y","position.x")
         # or program["transform"] = Position("vec2(position.y,position.x"))
         ...
    """
    
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/position.glsl")
        Transform.__init__(self, code, *args, **kwargs)
