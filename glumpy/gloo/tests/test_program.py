# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import unittest

import glumpy.gl as gl
from glumpy.gloo.program import Program
from glumpy.gloo.shader import VertexShader, FragmentShader


class ProgramTest(unittest.TestCase):

    def test_init(self):
        program = Program()
        assert program._handle == -1
        assert program.shaders == []

    def test_delete_no_context(self):
        program = Program()
        program.delete()

    def test_init_from_string(self):
        program = Program("A", "B")
        assert len(program.shaders) == 2
        assert program.shaders[0].code == "A"
        assert program.shaders[1].code == "B"

    def test_init_from_shader(self):
        program = Program(VertexShader("A"), FragmentShader("B"))
        assert len(program.shaders) == 2
        assert program.shaders[0].code == "A"
        assert program.shaders[1].code == "B"

    def test_unique_shader(self):
        vert = VertexShader("A")
        frag = FragmentShader("B")
        program = Program([vert, vert], [frag, frag, frag])
        assert len(program.shaders) == 2

    def test_uniform(self):
        vert = VertexShader("uniform float A;")
        frag = FragmentShader("uniform float A; uniform vec4 B;")
        program = Program(vert, frag)
        assert ("A", gl.GL_FLOAT) in program.all_uniforms
        assert ("B", gl.GL_FLOAT_VEC4) in program.all_uniforms
        assert len(program.all_uniforms) == 2

    def test_attributes(self):
        vert = VertexShader("attribute float A;")
        frag = FragmentShader("")
        program = Program(vert, frag)
        assert program.all_attributes == [("A", gl.GL_FLOAT)]

    def test_attach(self):
        vert = VertexShader("A")
        frag = FragmentShader("B")
        program = Program(vert)
        program.attach(frag)
        assert len(program.shaders) == 2
        assert program.shaders[0].code == "A"
        assert program.shaders[1].code == "B"

    def test_detach(self):
        vert = VertexShader("A")
        frag = FragmentShader("B")
        program = Program(vert, frag)
        program.detach(frag)
        assert len(program.shaders) == 1
        assert program.shaders[0].code == "A"

    def test_failed_build(self):
        vert = VertexShader("A")
        frag = FragmentShader("B")

        program = Program(verts=vert)
        self.assertRaises(ValueError, program.activate)

        program = Program(frags=frag)
        self.assertRaises(ValueError, program.activate)

    def test_setitem(self):
        vert = VertexShader("")
        frag = FragmentShader("")

        program = Program(vert, frag)
        self.assertRaises(ValueError, program.__setitem__, "A", 1)


if __name__ == "__main__":
    unittest.main()
