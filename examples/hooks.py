#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import glumpy
import glumpy.gloo as gloo

vertex = gloo.VertexShader(
"""
attribute vec2 position;
void main()
{
    gl_Position = <transform>;
}
""")

fragment = gloo.FragmentShader(
"""
void main()
{
    gl_FragColor = <color>;
}
""")

uniforms = gloo.Snippet(
"""
uniform vec3 translate;
""")

position2D = gloo.Snippet(
"""
vec4 position2D(vec2 position)
{
    return vec4(position, 0.0, 1.0);
}
""")

translate = gloo.Snippet(
"""
vec4 translate(vec4 position, vec3 translate)
{
    return vec4(position.xyz+translate, 1.0);
}
""")

#print translate(position2D("position"), translate="offset").code
window = glumpy.Window()

program = gloo.Program(vertex, fragment)
program["transform"] = uniforms() + translate(position2D("position"), "translate")
program["transform"]["translate"] = 1
program["translate"] = 1
program["color"] = "vec4(0,0,0,1)"
print program._verts[0].code

program = gloo.Program(vertex, fragment)
program["transform"] = uniforms(translate="offset") \
                     + translate(position2D("position"), "offset")
# program["transform"]["offset"] = 1
program["offset"] = 1
program["color"] = "vec4(0,0,0,1)"
print program._verts[0].code
