# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.geometry import primitives
from glumpy.graphics.filter import Filter
from glumpy import gl, app, glm, gloo, data


cube_vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
attribute vec3 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
    v_texcoord = texcoord;
}
"""

cube_fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    float r = texture2D(texture, v_texcoord).r;
    gl_FragColor = vec4(vec3(r),1.0);
}
"""



window = app.Window(1024,1024)

# See http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/
VBlur = gloo.Snippet("""
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    return 0.2270270270 *  texture2D( filtered, texcoord)
         + 0.3162162162 * (texture2D( filtered, texcoord + vec2(0.0, 1.3846153846)/texsize) +
                           texture2D( filtered, texcoord - vec2(0.0, 1.3846153846)/texsize) )
         + 0.0702702703 * (texture2D( filtered, texcoord + vec2(0.0, 3.2307692308)/texsize) +
                           texture2D( filtered, texcoord - vec2(0.0, 3.2307692308)/texsize) );
}""")

HBlur = gloo.Snippet("""
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    return 0.2270270270 *  texture2D( filtered, texcoord)
         + 0.3162162162 * (texture2D( filtered, texcoord + vec2(1.3846153846, 0.0)/texsize) +
                           texture2D( filtered, texcoord - vec2(1.3846153846, 0.0)/texsize) )
         + 0.0702702703 * (texture2D( filtered, texcoord + vec2(3.2307692308, 0.0)/texsize) +
                           texture2D( filtered, texcoord - vec2(3.2307692308, 0.0)/texsize) );
}""")
GaussianBlur = Filter(512, 512, VBlur, HBlur)



@window.event
def on_draw(dt):
    global phi, theta

    with GaussianBlur:
        window.clear()
        gl.glEnable(gl.GL_DEPTH_TEST)
        cube.draw(gl.GL_TRIANGLES, faces)

    theta += 0.5 # degrees
    phi += 0.5 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)


vertices, faces = primitives.cube()
cube = gloo.Program(cube_vertex, cube_fragment)
cube.bind(vertices)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -3)
cube['view'] = view
cube['model'] = np.eye(4, dtype=np.float32)
cube['texture'] = data.checkerboard()
phi, theta = 0, 0

# Run
app.run()
