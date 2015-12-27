# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.geometry import primitives
from glumpy.graphics.filter import Filter
from glumpy import gl, app, glm, gloo, data


cube_vertex = """
uniform mat4 model, view, projection;
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


pixelate = Filter(512, 512, """
uniform float level;
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    vec2 uv = (texcoord * level);
    uv = (uv - fract(uv)) / level;
    return texture2D(filtered, uv);
} """)
pixelate["level"] = 256.0


window = app.Window(1024,1024)

@window.event
def on_draw(dt):
    global phi, theta

    with pixelate:
        window.clear()
        gl.glEnable(gl.GL_DEPTH_TEST)
        cube.draw(gl.GL_TRIANGLES, faces)
    theta += 0.5
    phi += 0.5
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)
    pixelate.viewport = 0, 0, width, height


@window.event
def on_mouse_scroll(x, y, dx, dy):
    p = pixelate["level"]
    pixelate["level"] = min(max(8, p + .01 * dy * p), 512)


# Build cube data
vertices, faces = primitives.cube()
cube = gloo.Program(cube_vertex, cube_fragment)
cube.bind(vertices)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -3)
cube['view'] = view
cube['model'] = np.eye(4, dtype=np.float32)
cube['texture'] = data.checkerboard()
phi, theta = 0, 0
app.run()
