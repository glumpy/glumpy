# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.transforms import Position, LogScale, LinearScale
from glumpy.transforms import PolarProjection
from glumpy.transforms import HammerProjection
from glumpy.transforms import TransverseMercatorProjection

vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = position;
} """
fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
     vec2 uv = <projection.inverse(v_texcoord)>;
     gl_FragColor = texture2D(texture, <scale(uv)>.xy);
} """


window = app.Window(800,800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texture'] = data.get("earth.jpg")
program['texture'].interpolation = gl.GL_LINEAR


# Polar projection
# ----------------
# program['projection'] = PolarProjection(
#     # This translates texture coordinates to cartesian coordinates
#     LinearScale('.x', name = 'x', domain=(-1, 1), range=(-1,1), call="forward", clamp=True),
#     LinearScale('.y', name = 'y', domain=(-1, 1), range=(-1,1), call="forward", clamp=True))
# program['scale'] = Position(
#     # This translates cartesian coordinates (polar domains) to texture coordinates
#     # LogScale('.x', name = 'x', domain=(-1,0), range=(0,1), clamp=True),
#     LinearScale('.x', name = 'x', domain=(0.2, 1.0),     range=(0,1), clamp=True),
#     LinearScale('.y', name = 'y', domain=(0.0, 2*np.pi), range=(0,1), clamp=True))


# Hammer projection
# -----------------
# program['projection'] = HammerProjection(
#     # This translates texture coordinates to cartesian coordinates
#     LinearScale('.x', name = 'x', domain=(-1, 1), range=(-3.0,3.0), call="forward", clamp=True),
#     LinearScale('.y', name = 'y', domain=(+1,-1), range=(-2.0,2.0), call="forward", clamp=True))

# program['scale'] = Position(
#     # This translates cartesian coordinates (hammer domains) to texture coordinates
#     LinearScale('.x', name = 'x', domain=(-np.pi,   np.pi),   range=(0,1), clamp=True),
#     LinearScale('.y', name = 'y', domain=(-np.pi/2, np.pi/2), range=(0,1), clamp=True))
# window.set_size(800,500)


# Transverse Mercator projection
# ------------------------------
program['projection'] = TransverseMercatorProjection(
    # This translates texture coordinates to cartesian coordinates
    LinearScale('.x', name='x', domain=(-1,+1), range=(-1.5,1.5), call="forward", clamp=True),
    LinearScale('.y', name='y', domain=(+1,-1), range=(-2.4,2.4), call="forward", clamp=True))

program['scale'] = Position(
    # This translates cartesian coordinates (mercator domains) to texture coordinates
    LinearScale('.x', name = 'x', domain=(-np.pi,   np.pi),   range=(0,1), clamp=True),
    LinearScale('.y', name = 'y', domain=(-np.pi/2, np.pi/2), range=(0,1), clamp=True))
window.set_size(500,800)



@window.event
def on_mouse_scroll(x, y, dx, dy):
    xdomain = program['projection']['x']['domain']
    ydomain = program['projection']['y']['domain']
    if dy < 0:
        xdomain *= .9
        ydomain *= .9
    elif dy > 0:
        xdomain *= 1.1
        ydomain *= 1.1
    program['projection']['x']['domain'] = xdomain
    program['projection']['y']['domain'] = ydomain


app.run()
