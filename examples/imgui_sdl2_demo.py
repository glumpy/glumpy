# -*- coding: utf-8 -*-

from glumpy import app

import OpenGL.GL as gl

from sdl2 import *

import imgui
from imgui.integrations.sdl2 import SDL2Renderer

# Download https://raw.githubusercontent.com/pyimgui/pyimgui/master/doc/examples/testwindow.py put in same directory uncomment line 13 and 32
#from testwindow import show_test_window

config = app.configuration.Configuration()
config.profile = "core"
config.major_version = 4
config.minor_version = 1
app.use("sdl2")


window = app.Window(width=800, height=800, color=(1,1,1,1), title=b"Imgui_Sdl2_Demo", config=config)

imgui.create_context() 
imguiRenderer = SDL2Renderer(window._native_window) 

@window.event
def on_draw(dt):

    imgui.new_frame()

    #show_test_window()

    imgui.begin("Custom window", True)
    imgui.text("Bar")
    imgui.text_colored("Eggs", 0.2, 1., 0.)
    imgui.end()
    gl.glClearColor(1., 1., 1., 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    imguiRenderer.render(imgui.get_draw_data())

app.run()
