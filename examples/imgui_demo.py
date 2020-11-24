# -*- coding: utf-8 -*-
"""

imgui_demo.py

A glumpy demo using imgui. 

The demo is structured as follows: 
    * there are 3 classes:
        * ImGuiPlayer implements the main rendering loop; it is design to 
          play "Apps"
        * ImGuiPlayerApp is the abstract base class of Render "Apps"
        * DemoApp is the concrete demo application
    * everything is kept in one file for convenience, in a real application, 
      this may be split up for clarity

Authors: 
      github user mlviz
      Ivo Ihrke

"""

import os
from   typing import List
import numpy as np

from   glumpy.app import configuration
from   glumpy import app, gloo, gl

import OpenGL.GL as gl
import glfw

import imgui
from   imgui.integrations.glfw import GlfwRenderer

#------------------------------------------------------------------------------
#--------------------- abstract base class ------------------------------------
#------------------------------------------------------------------------------
class ImGuiPlayerApp:
    
    def __init__( self, name, window_size ):
        pass
    
    def initialize_program( self ):
        pass
    
    def key_callback( self, window, key, scancode, action, mods):
        pass
        
    def mouse_cursor_pos_callback( self, window, xpos, ypos ):
        pass
    
    def mouse_button_callback( self, window, button, action, mods ):
        pass
    
    def mouse_scroll_callback( self, window, xoffset, yoffset ):
        pass
        
    def window_size_callback( self, window, width, height ):
        gl.glViewport(0, 0, width, height);

    def on_draw(self):
        pass

    def menu(self):
        pass

#------------------------------------------------------------------------------
#---------------------------- demo app ----------------------------------------
#------------------------------------------------------------------------------

class DemoApp( ImGuiPlayerApp ):
    
    # ---------------------------------------------------------------------------
    # ------------------------- internal classes  -------------------------------
    # ---------------------------------------------------------------------------
        

    class UI():
        """
        This class contains the variables that are communicated 
        to the vertex and fragment programs
        """
        
        mouse_pos : np.array   = None; #mouse position; used for translating the view
        zoom  : float          = None; #zoom value
        gamma : float          = None; #contrast
        blue  : float          = None; #value of blue compponent for interaction demo 
        animate : bool         = None; #toggle animation
        speed : float          = None; #speed of animation
        theta : float          = None; #rotation angle
        
        prev_mouse : np.array = None; #previous mouse position to implement drag; maybe move to ImGuiPlayer
        
        def __init__(self):
            
            
            self.mouse_pos = np.array( [0,0] ).astype('float');
            self.zoom      = 1.0; 
            self.gamma     = 1.0;
            self.blue      = 0.0;
            self.animate   = False;
            self.speed     = 2.0 * np.pi / 100; 
            self.theta     = 0.0;
            
            self.prev_mouse = np.array( [-1, -1] ).astype('float');
    
    # ---------------------------------------------------------------------------
    # --------------------------- class variables -------------------------------
    # ---------------------------------------------------------------------------
    
    ui      : UI = None;
    quad    : gloo.Program = None;    
    
    def __init__( self ):
        
        
    
        self.ui = DemoApp.UI();

        self.quad = self.quad_init()
        

    def quad_init( self ):
        '''
        Initializes the rendering geometry (a quad) and the shader programs.
        '''
        
        
        vertex = """
            //note that this is ineffective, I keep it here as a reminder, 
            //the actual glsl version request must be made to the 
            //gloo.Program(..., version=130) constructor
            #version 130  
            
            in vec2   position; // do not use layout(location = 0) syntax; glumpy appears to use some magic
            in vec3   color;
            uniform   vec2   mouse_pos;
            uniform   float  zoom; 
            uniform   float  blue; 
            uniform   float  theta; 
            
            out vec4 frag_color;
            
            void main()
            {
                vec2 p = zoom * (position + mouse_pos);
                vec2 q = vec2( p.x * cos( theta ) + p.y * sin( theta ), -p.x * sin( theta ) + p.y * cos( theta ) );
                gl_Position = vec4( q, 0.0, 1.0);
                frag_color  = vec4( color.rg, blue, 1.0 );
            }
        """
        
        fragment = """
            //note that this is ineffective, I keep it here as a reminder, 
            //the actual glsl version request must be made to the 
            //gloo.Program(..., version=130) constructor
            #version 130
            
            uniform float   gamma;
                        
            in vec4 frag_color;                   // from vertex shader
            
            out vec4 color;  // this is the output color, going to GL_COLOR_ATTACHEMENT0

            void main()
            {                
                vec3 gamma_col = pow( frag_color.rgb, vec3(1.0/gamma) );
                color = vec4( gamma_col, 1 );
            }
        """

        
        #create a shader program for count vertices
        quad   = gloo.Program(vertex, fragment, count=4, version=130);
        
        #geometry and texure coordinates for the quad
        quad['position']  = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)];
        quad['color']  = [( 0, 0, 0), ( 1, 0, 0), ( 1, 1, 0), ( 0, 1, 0)];
        
        #initial values 
        quad['mouse_pos'] = self.ui.mouse_pos;
        quad['zoom']      = self.ui.zoom; 
        quad['gamma']     = self.ui.gamma;
        
        return quad

    # ---------------------------------------------------------------------------
    # --------------------------- class methods - gui and menu   ----------------
    # ---------------------------------------------------------------------------
    

    def key_callback( self, window, key, scancode, action, mods):
        
        
        if key == glfw.KEY_SPACE and action == glfw.RELEASE:
            self.ui.animate = not self.ui.animate;
            
        pass        
    
    def mouse_cursor_pos_callback( self, window, xpos, ypos ):
        io = imgui.get_io();
        
        mouse_pos = np.array( [xpos, ypos] ).astype('float');
            
        if io.mouse_down[0]:
            
            
            _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    
            if not np.all( self.ui.prev_mouse == np.array([-1,-1]) ):
                dmouse = self.ui.prev_mouse - mouse_pos;
        
                self.ui.mouse_pos -= np.array( [ dmouse[0]/w, -dmouse[1]/h] ) / self.ui.zoom * 2;
                self.quad["mouse_pos"] = self.ui.mouse_pos;
        
                print("mouse_pos: {}, dmouse: {}".format( mouse_pos, dmouse ) );
            
        self.ui.prev_mouse = mouse_pos;
            
        
    def mouse_button_callback( self, window, button, action, mods ):
        pass
        
    def mouse_scroll_callback( self, window, xoffset, yoffset ):
        
        self.ui.zoom += yoffset * 0.05;
        
        if self.ui.zoom < 0.1:
            self.ui.zoom = 0.1;
            
        self.quad["zoom"] = self.ui.zoom;

        
    
    def on_draw(self):
        '''
        called for every rendered frame
        '''
        
        if self.ui.animate:
            self.ui.theta += self.ui.speed;
        
            if self.ui.theta > 2.0 * np.pi:
                self.ui.theta -= 2.0 * np.pi;
            
            #move variable values to shader program
            self.quad['theta'] = self.ui.theta; 
            
        
        self.quad.draw(gl.GL_TRIANGLE_STRIP);

    def menu( self ):

        imgui.new_frame()

        #menu bar
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Ctrl+Q', False, True
                )

                if clicked_quit:
                    glfw.set_window_should_close( self.window, True );

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_test_window()

        imgui.begin("Demo window", True);
        imgui.text('ImGuiDemo');
        imgui.text_colored("* hold Left Mouse Button and drag to translate", 0.2, 1., 0.);
        imgui.text_colored("* use scroll wheel to zoom", 0.4, 1., 0.);
        imgui.text_colored("* press SPACE to toggle animation", 0.6, 1., 0.);
            
        changed, self.ui.animate = imgui.checkbox("Animate", self.ui.animate );
        changed, self.ui.gamma   = imgui.slider_float("Gamma",self.ui.gamma, 0.3, 3.3 );
        changed, self.ui.blue    = imgui.slider_float("Blue",self.ui.blue, 0.0, 1.0 );
        imgui.text("Animation Angle: {:0.2f}".format( self.ui.theta / (2.0 * np.pi) * 360.0 ) );
        changed, self.ui.speed   = imgui.slider_float("Speed",self.ui.speed, 0.0, np.pi/2.0 );
        
        #transfer changed variables to shader programs
        self.quad['blue']   = self.ui.blue;
        self.quad['gamma']  = self.ui.gamma;
        
        imgui.end()
        
#------------------------------------------------------------------------------
#------------------------ generic player class  -------------------------------
#------------------------------------------------------------------------------

class ImGuiPlayer:
    
    # ---------------------------------------------------------------------------
    # --------------------------- class variables -------------------------------
    # ---------------------------------------------------------------------------
    
    window  = None;
    impl : GlfwRenderer   = None;

    app : ImGuiPlayerApp = None;

    quit_requested : bool = None;

    def __init__( self, app : ImGuiPlayerApp ):

        self.app = app; 

        #initialize window and GUI        
        imgui.create_context();
    
        self.window = self.impl_glfw_init()
        self.impl = GlfwRenderer(self.window)

        self.quit_requested = False; 


        
    def impl_glfw_init(self):
        width, height = 1200, 1200
        window_name = "RefocusApp"
    
        
        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)
    
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    
        # the OPENGL_COMPAT_PROFILE enables the mix between pyimgui and glumpy
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    
        window = glfw.create_window( int(width), int(height), window_name, None, None );
        glfw.make_context_current( window )
    
        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)
    
        self.app.window_size_callback( window, 1200, 1200 );
    
    
        return window

    # ---------------------------------------------------------------------------
    # --------------------------- class methods - gui and menu   ----------------
    # ---------------------------------------------------------------------------
    

    def key_callback( self, window, key, scancode, action, mods):
        
        io = imgui.get_io();
        self.impl.keyboard_callback( window, key, scancode, action, mods );
        
        if io.want_capture_keyboard:
            print("imgui handles")    
        else:
            #print("processed by app: key pressed")
            
            if key == glfw.KEY_ESCAPE and action == glfw.RELEASE:
                self.quit_requested = True; 
        
            if key == glfw.KEY_Q and np.bitwise_and( mods, glfw.MOD_CONTROL ):
                self.quit_requested = True; 
        
            self.app.key_callback( window, key, scancode, action, mods );
    
    def mouse_cursor_pos_callback( self, window, xpos, ypos ):
        io = imgui.get_io();
        
        if not io.want_capture_mouse:
            self.app.mouse_cursor_pos_callback( window, xpos, ypos )    
        
    def mouse_button_callback( self, window, button, action, mods ):
        io = imgui.get_io();
        
        if io.want_capture_mouse:
            print("imgui handles")
        else:        
            self.app.mouse_button_callback( window, button, action, mods );
            
    def mouse_scroll_callback( self, window, xoffset, yoffset ):
        io = imgui.get_io();
        
        if io.want_capture_mouse:
            print("imgui handles")
        else:
            #print( "processed by app: scroll: {},{}".format( xoffset, yoffset ));
            
            self.app.mouse_scroll_callback(window, xoffset, yoffset);

        
    def window_size_callback( self, window, width, height ):
        self.app.window_size_callback(window, width, height);
        

    def run(self):
        
        glfw.set_key_callback(self.window, self.key_callback );
        glfw.set_cursor_pos_callback( self.window, self.mouse_cursor_pos_callback );
        glfw.set_mouse_button_callback( self.window, self.mouse_button_callback );
        glfw.set_scroll_callback( self.window, self.mouse_scroll_callback );
        glfw.set_window_size_callback( self.window, self.window_size_callback );
        
        while not glfw.window_should_close(self.window) and not self.quit_requested:
            self.app.on_draw();
            
            glfw.poll_events()
            self.impl.process_inputs()
    
                
            self.app.menu();
            
            gl.glClearColor(0., 0., 0.2, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
            self.app.on_draw();
    
            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)
    
        self.impl.shutdown()
        glfw.terminate()


# ---------------------------------------------------------------------------
# ---------------- main fct - run as app if used from cmd-line   ------------
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    app = DemoApp();

    player = ImGuiPlayer( app )
    
    player.run();