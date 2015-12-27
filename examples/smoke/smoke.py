# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Porting of the Fluid demo by Philip Prideout (c) 2010
# Originals sources and explanation on http://prideout.net/blog/?p=58
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, data

# Constants
# -------------------------------------
CellSize               = 1.25
ViewportWidth          = 512
ViewportHeight         = 512
GridWidth              = 512
GridHeight             = 512
SplatRadius            = GridWidth / 8.0
AmbientTemperature     = -1.0
ImpulseTemperature     = 10.0
ImpulseDensity         = 1.0
NumJacobiIterations    = 40
TimeStep               = 0.125
SmokeBuoyancy          = 1.00
SmokeWeight            = 0.05
GradientScale          = 1.125 / CellSize
TemperatureDissipation = 0.99
VelocityDissipation    = 0.99
DensityDissipation     = 0.9995
ImpulsePosition        = GridWidth/2, -int(SplatRadius/2)
PositionSlot           = 0


window = app.Window(ViewportWidth, ViewportHeight)


class Surface(object):
    def __init__(self, width, height, depth, interpolation=gl.GL_NEAREST):
        self.texture = np.zeros((height,width,depth), np.float32).view(gloo.TextureFloat2D)
        self.texture.interpolation = interpolation
        self.framebuffer = gloo.FrameBuffer(color=self.texture)
        self.clear()

    def clear(self):
        self.activate()
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.deactivate()

    def activate(self):
        self.framebuffer.activate()

    def deactivate(self):
        self.framebuffer.deactivate()

class Slab(object):
    def __init__(self, width, height, depth, interpolation=gl.GL_NEAREST):
        self.Ping = Surface(width, height, depth, interpolation)
        self.Pong = Surface(width, height, depth, interpolation)

    def swap(self):
        self.Ping, self.Pong = self.Pong, self.Ping

def Program(fragment):
    program = gloo.Program("smoke.vert", fragment, count=4)
    program['Position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
    return program


Velocity = Slab(GridWidth, GridHeight, 2)
Density = Slab(GridWidth, GridHeight, 1, gl.GL_LINEAR)
Pressure = Slab(GridWidth, GridHeight, 1)
Temperature = Slab(GridWidth, GridHeight, 1, gl.GL_LINEAR)
Divergence = Surface(GridWidth, GridHeight, 3)
Obstacles = Surface(GridWidth, GridHeight, 3, gl.GL_LINEAR)

prog_gradient = Program("gradient.frag")
prog_jacobi = Program("jacobi.frag")
prog_advect = Program("advect.frag")
prog_divergence = Program("divergence.frag")
prog_fill = Program("fill.frag")
prog_splat = Program("splat.frag")
prog_buoyancy = Program("buoyancy.frag")
prog_visualize = Program("visualize.frag")



prog_advect["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_divergence["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_gradient["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_buoyancy["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_jacobi["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_fill["InverseSize"] = 1.0 / GridWidth, 1.0 / GridHeight
prog_advect["TimeStep"] = TimeStep
prog_jacobi["Alpha"] =  -CellSize * CellSize
prog_jacobi["InverseBeta"] = 0.25
prog_gradient["GradientScale"] = GradientScale
prog_divergence["HalfInverseCellSize"] = 0.5 / CellSize
prog_splat["Radius"] = SplatRadius
prog_splat["Point"] = ImpulsePosition
prog_buoyancy["AmbientTemperature"] = AmbientTemperature
prog_buoyancy["TimeStep"] = TimeStep
prog_buoyancy["Sigma"] = SmokeBuoyancy
prog_buoyancy["Kappa"] = SmokeWeight


def Advect(velocity, source, obstacles, dest, dissipation):
    prog_advect["Dissipation"] = dissipation
    prog_advect["VelocityTexture"] = velocity.texture
    prog_advect["SourceTexture"] = source.texture
    prog_advect["Obstacles"] = obstacles.texture
    dest.activate()
    prog_advect.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

def Jacobi(pressure, divergence, obstacles, dest):
    prog_jacobi["Pressure"] = pressure.texture
    prog_jacobi["Divergence"] = divergence.texture
    prog_jacobi["Obstacles"] = obstacles.texture
    dest.activate()
    prog_jacobi.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

def SubtractGradient(velocity, pressure, obstacles, dest):
    prog_gradient["Velocity"] = velocity.texture
    prog_gradient["Pressure"] = pressure.texture
    prog_gradient["Obstacles"] = obstacles.texture
    dest.activate()
    prog_gradient.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

def ComputeDivergence(velocity, obstacles, dest):
    prog_divergence["Obstacles"] = obstacles.texture
    prog_divergence["Velocity"] = velocity.texture
    dest.activate()
    prog_divergence.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

def ApplyImpulse(dest, position, value):
    prog_splat["FillColor"] = value,value,value
    dest.activate()
    gl.glEnable(gl.GL_BLEND)
    prog_splat.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()
    gl.glDisable(gl.GL_BLEND)

def ApplyBuoyancy(velocity, temperature, density, dest):
    prog_buoyancy["Density"] = density.texture
    prog_buoyancy["Velocity"] = velocity.texture
    prog_buoyancy["Temperature"] = temperature.texture
    dest.activate()
    prog_buoyancy.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

def ClearSurface(surface, v):
    surface.activate()
    gl.glClearColor(v, v, v, v)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    surface.deactivate()

def disc(shape=(256,256), center=(128,128), radius = 96):
    def distance(x,y):
        return np.sqrt((x-center[0])**2+(y-center[1])**2)
    D = np.fromfunction(distance,shape)
    return np.where(D<=radius,1.0,0.0).astype(np.float32)

def CreateObstacles(dest, width, height):
    dest.activate()
    gl.glViewport(0, 0, width, height)
    gl.glClearColor(0, 0, 0, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    T = np.ones((height,width,3), np.float32).view(gloo.Texture2D)

    T[+1:-1,+1:-1] = 0.0
    T[...,0] += disc(shape = (GridHeight,GridWidth),
                     center = (GridHeight/2,GridWidth/2),
                     radius = 32)
    T[...,2] += -2*disc(shape = (GridHeight,GridWidth),
                        center = (GridHeight/2,GridWidth/2),
                        radius = 32)
    prog_fill["Sampler"] = T
    prog_fill.draw(gl.GL_TRIANGLE_STRIP)
    dest.deactivate()

@window.event
def on_init():
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_BLEND)
    ClearSurface(Temperature.Ping, AmbientTemperature)
    CreateObstacles(Obstacles, GridWidth, GridHeight)

@window.event
def on_draw(dt):

    gl.glViewport(0, 0, GridWidth, GridHeight)
    gl.glDisable(gl.GL_BLEND)

    Advect(Velocity.Ping, Velocity.Ping, Obstacles, Velocity.Pong, VelocityDissipation)
    Velocity.swap()

    Advect(Velocity.Ping, Temperature.Ping, Obstacles, Temperature.Pong, TemperatureDissipation)
    Temperature.swap()

    Advect(Velocity.Ping, Density.Ping, Obstacles, Density.Pong, DensityDissipation)
    Density.swap()

    ApplyBuoyancy(Velocity.Ping, Temperature.Ping, Density.Ping, Velocity.Pong)
    Velocity.swap()

    ApplyImpulse(Temperature.Ping, ImpulsePosition, ImpulseTemperature)
    ApplyImpulse(Density.Ping, ImpulsePosition, ImpulseDensity)
    ComputeDivergence(Velocity.Ping, Obstacles, Divergence)
    ClearSurface(Pressure.Ping, 0.0)

    for i in range(NumJacobiIterations):
        Jacobi(Pressure.Ping, Divergence, Obstacles, Pressure.Pong)
        Pressure.swap()

    SubtractGradient(Velocity.Ping, Pressure.Ping, Obstacles, Velocity.Pong)
    Velocity.swap()

    gl.glViewport(0,0,window.width,window.height)
    gl.glClearColor(0, 0, 0, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    prog_visualize['u_data']   = Density.Ping.texture
    prog_visualize['u_shape']  = Density.Ping.texture.shape[1], Density.Ping.texture.shape[0]
    prog_visualize['u_kernel'] = data.get("spatial-filters.npy")
    prog_visualize["Sampler"] = Density.Ping.texture
    prog_visualize["FillColor"] = 0.95, 0.925, 1.00
    prog_visualize["Scale"] =  1.0/window.width, 1.0/window.height
    prog_visualize.draw(gl.GL_TRIANGLE_STRIP)

app.run()
