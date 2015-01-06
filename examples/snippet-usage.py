#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import gloo

transform_1 = gloo.Snippet("""
vec2 forward(float x) { return x; }
vec2 inverse(float x) { return x; }
""")

transform_2 = gloo.Snippet("""
vec2 forward(float x) { return x; }
vec2 inverse(float x) { return x; }
""")

code= """
void main(void)
{
    // Argument must be given through snippet
    <transform_1>;

    // Argument cannot be given through snippet
    <transform_2>(B);

    // Argument can be overriden throught snippet
    <transform_3(C)>;

    // ---

    // Default function (first defined) is used
    <transform_4>;

    // Forward function is used
    <transform_5.forward>;

    // Inverse function is used
    <transform_6.inverse>;
} """

program = gloo.Program(code,"void main(){}")
program["transform_1"] = transform_1("A")
program["transform_2"] = "forward"
program["transform_3"] = transform_1()
program["transform_4"] = transform_1("D")
program["transform_5"] = transform_2("E")
program["transform_6"] = transform_2("F")
print program.vertex.code
