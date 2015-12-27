# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app, gl, gloo, data, library
from glumpy.transforms import Trackball, Position, Position

vertex = """
uniform vec2 iResolution;
attribute vec2 texcoord;
varying vec2 v_texcoord;
varying vec2 v_size;

varying mat4 v_PVM;
void main (void)
{
    v_texcoord = texcoord;
    gl_Position = <trackball>;

    v_PVM = <trackball.trackball_projection> *
            <trackball.trackball_view> *
            <trackball.trackball_model>;
}
"""

window = app.Window(width=2*512, height=2*512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

program = gloo.Program(vertex, "./regular-grid.frag")
program["texcoord"] = (-0.5,-0.5), (-0.5, +0.5), (+0.5,-0.5), (+0.5,+0.5)
program["u_texture"] = data.get("lena.png")
program["u_texture"].interpolation = gl.GL_LINEAR
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 1.0
program['u_antialias'] = 1.0

# Polar domains
# program['u_major_grid_step'] = np.array([ 1.00, np.pi/6])
# program['u_minor_grid_step'] = np.array([ 0.25, np.pi/60])
# program['u_limits1'] = -5.1, +5.1, -5.1, +5.1
# program['u_limits2'] = 1.0, 5.0, 0*np.pi, 2*np.pi

# Cartesian domains
program['u_major_grid_step'] = np.array([ 1.00, 1.00])
program['u_minor_grid_step'] = np.array([ 0.10, 0.10])
program['u_limits1'] = -5.1, +5.1, -5.1, +5.1
program['u_limits2'] = -5.0, +5.0, -5.0, +5.0

# Hammer domains
# program['u_major_grid_step'] = np.array([ 1.00, 0.50]) * np.pi/ 6.0
# program['u_minor_grid_step'] = np.array([ 1.00, 0.50]) * np.pi/30.0
# program['u_limits1'] = -3.0, +3.0, -1.5, +1.5
# program['u_limits2'] = -np.pi, +np.pi, -np.pi/3, +np.pi/3

# program['transform'] = shaders.get("transforms/polar.glsl")
# program['transform'] = shaders.get("transforms/hammer.glsl")
program['transform_forward'] = gloo.Snippet(library.get("transforms/identity_forward.glsl"))
program['transform_inverse'] = gloo.Snippet(library.get("transforms/identity_inverse.glsl"))
program['trackball'] = Trackball(Position("texcoord"))
program['trackball'].theta = 0
program['trackball'].phi = 0
program['trackball'].zoom = 7.5

window.attach(program['trackball'])

app.run()
