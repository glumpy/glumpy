# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.graphics.filter import Filter

cone_vertex = """
uniform mat4 projection;
attribute vec2 translate;
attribute vec3 position;
attribute vec3 color;
varying vec3 v_color;
void main()
{
    v_color = color;
    gl_Position = projection * vec4(position.xy+translate, position.z ,1.0);
}
"""

cone_fragment = """
varying vec3 v_color;
void main()
{
    gl_FragColor = vec4(v_color.rgb, 1.0);
}
"""

borders = Filter(1024, 1024, """
const float epsilon = 1e-3;
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    vec4 center = texture2D(filtered, texcoord);
    vec4 left   = texture2D(filtered, texcoord + vec2(-1.0, 0.0)/texsize);
    vec4 right  = texture2D(filtered, texcoord + vec2(+1.0, 0.0)/texsize);
    vec4 down   = texture2D(filtered, texcoord + vec2( 0.0,-1.0)/texsize);
    vec4 up     = texture2D(filtered, texcoord + vec2( 0.0,+1.0)/texsize);
    vec4 black  = vec4(0,0,0,1);
    float level = 0.5;

    if (length(center-left) > epsilon) {
        return mix(black,right, level);
    } else if (length(center-right) > epsilon) {
        return mix(black, left, level);
    } else if (length(center-down) > epsilon) {
        return mix(black, up,  level);
    } else if (length(center-up) > epsilon) {
        return mix(black, down, level);
    }
    return center;
} """)


window = app.Window(width=1024, height=1024)

@window.event
def on_draw(dt):
    with borders:
        window.clear()
        gl.glEnable(gl.GL_DEPTH_TEST)
        cones.draw(gl.GL_TRIANGLES, I)

@window.event
def on_resize(width, height):
    cones['projection'] = glm.ortho(0, width, 0, height, -5, +500)
    borders.viewport = 0,0,width,height

@window.event
def on_mouse_motion(x,y,dx,dy):
    C["translate"][0] = x, window.height-y

def makecone(n=32, radius=1024):
    height = radius / np.tan(45 * np.pi / 180.0)
    V = np.zeros((1+n,3))
    V[0] = 0,0,0
    T = np.linspace(0,2*np.pi,n, endpoint=False)
    V[1:,0] = radius*np.cos(T)
    V[1:,1] = radius*np.sin(T)
    V[1:,2] = -height
    I  = np.repeat([[0,1,2]], n, axis=0).astype(np.uint32)
    I += np.arange(n,dtype=np.uint32).reshape(n,1)
    I[:,0] = 0
    I[-1] = 0,n,1
    return V, I.ravel()


n = 512 # number of cones (= number of points)
p = 32  # faces per cones

cones = gloo.Program(cone_vertex, cone_fragment)
C = np.zeros((n,1+p), [("translate", np.float32, 2),
                       ("position",  np.float32, 3),
                       ("color",     np.float32, 3)]).view(gloo.VertexBuffer)
I = np.zeros((n,3*p), np.uint32).view(gloo.IndexBuffer)
I += (1+p)*np.arange(n, dtype=np.uint32).reshape(n,1)
for i in range(n):
    #x,y = np.random.uniform(0,1024,2)
    x,y = np.random.normal(512,256,2)
    vertices, indices = makecone(p, radius=512)
    if i > 0:
        C["color"][i] = np.random.uniform(0.25,1.00,3)
    else:
        C["color"][0] = 1,1,0
    C["translate"][i] = x,y
    C["position"][i] = vertices
    I[i] += indices.ravel()
cones.bind(C)

app.run()
