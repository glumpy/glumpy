# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import unittest

import glumpy.gl as gl
from glumpy.gloo.shader import VertexShader, FragmentShader


# -----------------------------------------------------------------------------
class VertexShaderTest(unittest.TestCase):

    def test_init(self):
        shader = VertexShader()
        assert shader._target == gl.GL_VERTEX_SHADER


# -----------------------------------------------------------------------------
class FragmentShaderTest(unittest.TestCase):

    def test_init(self):
        shader = FragmentShader()
        assert shader._target == gl.GL_FRAGMENT_SHADER


# -----------------------------------------------------------------------------
class ShaderTest(unittest.TestCase):

    def test_init(self):
        shader = VertexShader()
        assert shader._handle == -1
        assert shader.code is None
        assert shader.source is None

    def test_sourcecode(self):
        code = "/* Code */"
        shader = VertexShader(code)
        assert shader.code == code
        assert shader.source == "<string>"

    def test_empty_build(self):
        shader = VertexShader()
        #with self.assertRaises(RuntimeError):
        #    shader.activate()
        self.assertRaises(RuntimeError, shader.activate)

    def test_delete_no_context(self):
        shader = VertexShader()
        shader.delete()

    def test_uniform_float(self):
        shader = VertexShader("uniform float color;")
        assert shader.uniforms == [("color", gl.GL_FLOAT)]

    def test_uniform_vec4(self):
        shader = VertexShader("uniform vec4 color;")
        assert shader.uniforms == [("color", gl.GL_FLOAT_VEC4)]

    def test_uniform_array(self):
        shader = VertexShader("uniform float color[2];")
        assert shader.uniforms == [("color[0]", gl.GL_FLOAT),
                                   ("color[1]", gl.GL_FLOAT)]

    def test_attribute_float(self):
        shader = VertexShader("attribute float color;")
        assert shader.attributes == [("color", gl.GL_FLOAT)]

    def test_attribute_vec4(self):
        shader = VertexShader("attribute vec4 color;")
        assert shader.attributes == [("color", gl.GL_FLOAT_VEC4)]


if __name__ == "__main__":
    unittest.main()
