# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo
from glumpy.geometry import colorcube
from glumpy.transforms import TrackballPan, Position

import imgui
from imgui.integrations.glfw import GlfwRenderer


vertex = """

uniform vec4 u_color;
attribute vec3 position;
attribute vec4 color;
varying vec4 v_color;

void main()
{
    v_color = u_color * color;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""


app.use("pyglfw")  # Required for ImGui integration
window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

# Build cube data
V, I, O = colorcube()
vertices = V.view(gloo.VertexBuffer)
faces    = I.view(gloo.IndexBuffer)
outline  = O.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(vertices)

# create an instance of the TrackballPan object.
trackball = TrackballPan(Position("position"), znear=3, zfar=10, distance=5)
cube['transform'] = trackball

trackball.aspect = 1
# rotation around the X axis
trackball.phi = 0
# rotation around the Y axis
trackball.theta = 0
trackball.zoom = 50


@window.event
def on_draw(dt):
    # GUI
    imguiRenderer.process_inputs()
    imgui.new_frame()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked, selected = imgui.menu_item("Quit", 'ESC', False, True)
            if clicked:
                exit(0)
            imgui.end_menu()

        imgui.end_main_menu_bar()

    imgui.begin('Cube')
    changed, zoom = imgui.slider_float('zoom', trackball.zoom, 15, 90)
    if changed: trackball.zoom = zoom
    imgui.end()

    imgui.end_frame()
    imgui.render()


    window.clear()

    # Filled cube
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    cube['u_color'] = 1, 1, 1, 1
    cube.draw(gl.GL_TRIANGLES, faces)

    # Outlined cube
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    cube['u_color'] = 0, 0, 0, 1
    cube.draw(gl.GL_LINES, outline)
    gl.glDepthMask(gl.GL_TRUE)

    imguiRenderer.render(imgui.get_draw_data())


window.attach(cube['transform'])


# ImGui
imgui.create_context()
imguiRenderer = GlfwRenderer(window._native_window, attach_callbacks=False)


# OpenGL
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


# Run
app.run()






# Finish ImGui
#imguiRenderer.shutdown()
