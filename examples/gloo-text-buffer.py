#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm

vertex = """
#version 120

// Uniforms
// --------
uniform mat4 projection;
uniform vec2 position;
uniform vec2 selection;
uniform vec2 size;
uniform float scale;

// Attributes
// ----------
attribute vec2 colrow;
attribute vec4 foreground;
attribute vec4 background;
attribute vec4 bytes_0123, bytes_4567;
attribute vec2 bytes_89;

// Varyings
// --------
varying vec4 v_foreground, v_background;
varying vec4 v_bytes_0123, v_bytes_4567;
varying vec2 v_bytes_89;

void main (void)
{
    float index = colrow.y * size.y + colrow.x;

    vec2 P = (position + colrow * vec2(6.0,13.0)) * scale;
    gl_Position = projection*vec4(P, 0.0, 1.0);
    gl_PointSize = 13.0 * scale;

    v_foreground = foreground;
    if( (index >= selection.x) && (index < selection.y)) {
        v_background = vec4(v_foreground.rgb, 0.1);
    } else {
        v_background = background;
    }
    v_bytes_0123 = bytes_0123;
    v_bytes_4567 = bytes_4567;
    v_bytes_89   = bytes_89;
}
"""

fragment = """
#version 120

float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}

// Varyings
// --------
varying vec4 v_foreground, v_background;
varying vec4 v_bytes_0123, v_bytes_4567;
varying vec2 v_bytes_89;

void main(void)
{
    vec2 uv = floor(gl_PointCoord.xy * 13.0);
    if(uv.x > 5.0) discard;
    if(uv.y > 12.0) discard;
    float index = floor( (uv.y*6.0+uv.x)/8.0 );
    float offset = floor( mod(uv.y*6.0+uv.x,8.0));
    float byte = segment(0.0,1.0,index) * v_bytes_0123.x
               + segment(1.0,2.0,index) * v_bytes_0123.y
               + segment(2.0,3.0,index) * v_bytes_0123.z
               + segment(3.0,4.0,index) * v_bytes_0123.w
               + segment(4.0,5.0,index) * v_bytes_4567.x
               + segment(5.0,6.0,index) * v_bytes_4567.y
               + segment(6.0,7.0,index) * v_bytes_4567.z
               + segment(7.0,8.0,index) * v_bytes_4567.w
               + segment(8.0,9.0,index) * v_bytes_89.x
               + segment(9.0,10.0,index)* v_bytes_89.y;

    // Logical AND test
    if( floor(mod(byte / (128.0/pow(2.0,offset)), 2.0)) > 0.0 )
        gl_FragColor = v_foreground;
    else if( v_background.a > 0.0 )
        gl_FragColor = v_background;
    else
        discard;
}
"""


class TextBuffer(object):
    """
    """

    # Load fonts
    __regular__ = np.load("6x13-regular.npy")
    __italic__  = np.load("6x13-italic.npy")
    __bold__    = np.load("6x13-bold.npy")
    __font__    = None

    def __init__(self, rows=24, cols=80, x=0, y=0, scale=2):

        # Build a font array that holds regular, italic & bold font
        # Regular:      0 to   65536-1
        # Italic :  65536 to 2*65536-1
        # Bold :  2*65536 to 3*65536-1
        if TextBuffer.__font__ is None:
            n1 = len(TextBuffer.__regular__)
            n2 = len(TextBuffer.__italic__)
            n3 = len(TextBuffer.__bold__)
            n = n1+n2+n3
            dtype = [ ("code", np.uint32,  1),
                      ("data",  np.uint8, 10) ]
            TextBuffer.__font__ = np.zeros(n, dtype)
            TextBuffer.__font__[:n1] = TextBuffer.__regular__
            TextBuffer.__font__[n1:n1+n2] = TextBuffer.__italic__
            TextBuffer.__font__[n1:n1+n2]["code"] += 1*65536
            TextBuffer.__font__[n1+n2:n1+n2+n3] = TextBuffer.__bold__
            TextBuffer.__font__[n1+n2:n1+n2+n3]["code"] += 2*65536


        self._position = x+6.5,y+6.5
        self._rows = rows
        self._cols = cols
        self._scale = int(max(scale,1))
        self._selection = None

        self._program = gloo.Program(vertex, fragment)
        self._vbuffer = np.zeros(rows*cols, [("colrow",     np.float32, 2),
                                             ("foreground", np.float32, 4),
                                             ("background", np.float32, 4),
                                             ("glyph",      np.float32,10)])
        self._vbuffer= self._vbuffer.view(gloo.VertexBuffer)
        self._program.bind(self._vbuffer.view([("colrow",     np.float32, 2),
                                               ("foreground", np.float32, 4),
                                               ("background", np.float32, 4),
                                               ("bytes_0123", np.float32, 4),
                                               ("bytes_4567", np.float32, 4),
                                               ("bytes_89",   np.float32, 2) ]))
        self._program['scale'] = self._scale
        self._program['size'] = rows, cols
        if self._selection is not None:
            self._program['selection'] = self._selection
        else:
            self._program['selection'] = -1,-1
        self._program['position'] = self._position

        # Initialize glyph position (they won't be moved individually)
        C,R = np.meshgrid(np.arange(self._cols), np.arange(self._rows))
        self._vbuffer["colrow"][...,0] = C.ravel()
        self._vbuffer["colrow"][...,1] = R.ravel()
        self._vbuffer["foreground"] = 0, 0, 0, 1
        self._vbuffer["background"] = 0, 0, 0, 0


    def on_init(self):
        gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
        gl.glEnable(gl.GL_POINT_SPRITE)


    def on_resize(self, width, height):
        self._program["projection"] = glm.ortho(0, width, height, 0, -1, +1)


    def draw(self):
        self._program.draw(gl.GL_POINTS)


    def __contains__(self, (x,y)):
        width = self._cols*self._scale*6
        height = self._rows*self._scale*13
        if 0 <= x < width and 0 <= y < height:
            return True
        return False


    @property
    def scale(self):
        """ Font scale """

        return self._scale


    @property
    def rows(self):
        """ Number of rows """

        return self._rows


    @property
    def cols(self):
        """ Number of columns """

        return self._cols

    @property
    def selection_bounds(self):
        """ Selection bounds """

        start,end = self._selection
        if end < start:
            start,end = end,start
        return max(0, start), min(self.rows*self.cols, end)


    def clear(self, start=0, end=-1):
        """
        Clear the text buffer
        """

        self._vbuffer["glyph"][start:end] = 0
        self._vbuffer["foreground"][start:end] = 0,0,0,1
        self._vbuffer["background"][start:end] = 0,0,0,0
        self.clear_selection()


    def clear_selection(self):
        """
        Clear current selection
        """

        self._selection = None
        self._program["selection"] = -1,-1


    def put(self, row, col, text, foreground, background, style):
        """ Put text at (row,col) """

        font = TextBuffer.__font__

        # Make sure argument are of the right type
        foreground = np.atleast_2d(foreground)
        background = np.atleast_2d(background)
        style = np.atleast_1d(style)

        index = row*self.cols + col

        # Decode text
        if isinstance(text, (str,unicode)):
            text = unicode(text)
            codes = np.array([ord(c) for c in text]).astype(np.uint32)
        else:
            codes = text.astype(np.uint32).ravel()

        # Crop if necessary
        n = len(codes)
        imax = self.rows*self.cols
        if index + n > imax:
            n = imax - index
            codes = codes[:n]
            style = style[:n]
            foreground = foreground[:n]
            background = background[:n]

        # Tweak code to take style into account
        codes += style*65536

        # Replace unknown glyphs with glyph 0
        codes *= np.in1d(codes, font["code"])

        # Put glyphs data into buffer
        glyphs = font["data"][np.searchsorted(font["code"], codes)]
        self._vbuffer["glyph"][index:index+n] = glyphs
        self._vbuffer["foreground"][index:index+n] = foreground
        self._vbuffer["background"][index:index+n] = background




# -----------------------------------------------------------------------------
class Console(TextBuffer):

    def __init__(self, rows=24, cols=80, x=3, y=3, scale=2, cache=100):
        TextBuffer.__init__(self, rows, cols, x, y, scale)

        # We use a ring buffer to avoid to have to move things around
        self._buffer_start = 0
        self._buffer_end = 0
        cache = min(cache, rows)
        self._buffer = np.ones((cache+rows,cols),
                               dtype=[("code",       np.uint16,  1),
                                      ("style",      np.uint16,  1),
                                      ("foreground", np.float32, 4),
                                      ("background", np.float32, 4)])
        self._buffer["code"] = 32 # space
        self._scroll = -self.rows

        self._default_foreground = 0,0,0,1 # Black
        self._default_background = 0,0,0,0 # Transparent black
        self._default_style      = 0       # Regular

        self._buffer["style"]      = self._default_style
        self._buffer["foreground"] = self._default_foreground
        self._buffer["background"] = self._default_background



    def write(self, text=u"", foreground=None, background=None, style=None):
        """ Write at current position into the buffer and rotate buffer """

        # Set defaults
        if foreground is None:
            foreground = self._default_foreground
        if background is None:
            background = self._default_background
        if style is None:
            style = self._default_style

        n = len(self._buffer)
        empty = (32,0,(0,0,0,1),(0,0,0,0))

        # Clear line
        self._buffer[self._buffer_end] = empty

        # Write line
        self._buffer["code"][self._buffer_end,:len(text)] = [ord(c) for c in text]
        self._buffer["foreground"][self._buffer_end,:len(text)] = foreground
        self._buffer["background"][self._buffer_end,:len(text)] = background
        self._buffer["style"][self._buffer_end,:len(text)] = style

        # Clear line beyond row lines in case use want to have only the first
        # line on top (or else we would display buffer start)
        self._buffer[(self._buffer_end+self.rows) % n] = empty

        self._buffer_end = (self._buffer_end + 1) % n
        if self._buffer_end == self._buffer_start:
            self._buffer_start = (self._buffer_start + 1) % n
        # Update text buffer
        # self.put(0, 0, self.view(int(self._scroll))["code"])
        V = self.view(int(self._scroll))

        self.put(0, 0, text=V["code"],
                 foreground=V["foreground"], background=V["background"], style=V["style"])

        # Update selection if any
        if self._selection is not None:
            start, end = self._selection
            start += self._scroll*self.cols
            end   += self._scroll*self.cols
            if end < start:
                self._program["selection"] = end, start
            else:
                self._program["selection"] = start, end


    def on_mouse_press(self, x, y, button):
        """ Selection start point (taking scroll into account) """

        if (x,y) in self:
            x = x // ( 6*self._scale)
            y = y // (13*self._scale)
            s = (int(self._scroll)+self.rows)*self.cols

            start = y*self.cols + x
            self._selection = start+s, start+s
            self._program["selection"] = start, start


    def on_mouse_drag(self, x, y, dx, dy, button):
        """ Selection end point (taking scroll into account) """

        if self._selection is not None:
            x = x // ( 6*self._scale)
            y = y // (13*self._scale)
            s = (int(self._scroll)+self.rows)*self.cols

            start = self._selection[0]
            end = (y*self.cols+x) + s
            self._selection = start, end

            if end < start:
                self._program["selection"] = end-s, start-s
            else:
                self._program["selection"] = start-s, end-s


    def on_mouse_scroll(self, x, y, dx, dy):
        # Count how many lines have been writen so far
        if self._buffer_end > self._buffer_start:
            n = self._buffer_end
        else:
            n = len(self._buffer) - self.rows
        self._scroll = min(max(self._scroll-dy,-n),-1)

        # Update text buffer
        V = self.view(int(self._scroll))
        self.put(0, 0, text=V["code"],
                 foreground=V["foreground"], background=V["background"], style=V["style"])

        # Update selection if any
        if self._selection is not None:
            start, end = self._selection
            start -= (int(self._scroll)+self.rows)*self.cols
            end   -= (int(self._scroll)+self.rows)*self.cols
            self._program["selection"] = start, end


    def clear(self):
        TextBuffer.clear(self)
        self._buffer_start = 0
        self._buffer_end = 0
        self._buffer[...] = 32

    def view(self, index=-1):
        """ Retrieve a view of the buffer starting at index """

        # Count how many lines have been writen so far
        if self._buffer_end > self._buffer_start:
            n = self._buffer_end
        else:
            n = len(self._buffer) - self.rows

        actual_index = min(max(index, -n),-1)
        start = (self._buffer_end + actual_index) % len(self._buffer)
        stop = start + self.rows
        indices = np.mod(np.arange(start, stop), len(self._buffer))
        return self._buffer[indices].ravel()




# -----------------------------------------------------------------------------
if __name__ == '__main__':
    console = Console()
    window = app.Window(width=console.cols*console.scale*6,
                        height=console.rows*console.scale*13,
                        color = (1,1,1,1))

    @window.event
    def on_draw(dt):
        window.clear(), console.draw()

    # import codecs
    # f = codecs.open("UTF-8-demo.txt", "r", "utf-8")
    # #f = codecs.open("TeX.txt", "r", "utf-8")
    # lines = f.readlines()
    # for line in lines:
    #     console.write(line[:-1])

    @window.timer(1/30.0)
    def timer(fps):
        console.clear()
        console.write(u"──────────────────────────────────────────────────")
        console.write(u"GLUMPY 2.0 - Copyright (c) 2014 Nicolas P. Rougier")
        console.write(u"")
        console.write(u" → Window size: %dx%d" % (window.width, window.height),
                      foreground = (0,0,0,.5))
        console.write(u" → Backend: %s (%s)" % (window._backend.__name__,
                                              window._backend.__version__),
                      foreground = (0,0,0,.5))
        console.write(u" → Console size: %dx%d" % (console.rows, console.cols),
                      foreground = (0,0,0,.5))
        console.write(u" → Actual FPS: %.2f frames/second  " % (app.fps()),
                      foreground = (0,0,0,.5))
        console.write(u"──────────────────────────────────────────────────")

    window.attach(console)
    app.run()
