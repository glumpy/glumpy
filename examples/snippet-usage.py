# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import gloo

transform_1 = gloo.Snippet("""
uniform float scale;
float forward(float x) { return scale*x; }
float inverse(float x) { return scale*x; }
""")

transform_2 = gloo.Snippet("""
uniform float scale;
float forward(float x) { return scale*x; }
float inverse(float x) { return scale*x; }
""")

transform_3 = gloo.Snippet("""
vec2 compose(float x, float y) { return vec2(x,y); }
vec2 compose(vec2 xy) { return xy; }
""")

code= """
uniform float scale;

void main(void)
{
    // ---
    float scale_t1 = <transform_1.scale>;
    float scale_t2 = <transform_6.scale>;

    // ---
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

    // ---
    // Compose snippet with specific field affectation
    <transform_7>;

    // Compose snippet with generic field affectation
    // Note yet done
    <transform_8(H)>;

    <transform_8.x.scale>;
    <transform_8.y.scale>;
} """

program = gloo.Program(code,"void main(){}")
program["transform_1"] = transform_1("A")
program["transform_2"] = "forward"
program["transform_3"] = transform_1()
program["transform_4"] = transform_1("D")
program["transform_5"] = transform_1(transform_2("E"))
program["transform_6"] = transform_2("F", scale="aliased_scale")
program["transform_7"] = transform_3(transform_1("G.x"), transform_2("G.y"))
program["transform_8"] = transform_3(transform_1('.x', name='x'),
                                     transform_2('.y', name='y'))
print(program.vertex.code)


# Make sure that if snippet code has been already included in another program
# it is nonetheless included in the new program
code= """
void main(void)
{
    // Argument must be given through snippet
    <transform>;
}
"""
program = gloo.Program(code, "void main(){}")
program["transform"] = transform_1("A")
#print program.vertex.code
