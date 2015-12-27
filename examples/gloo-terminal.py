# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import glumpy
import numpy as np
from glumpy import app, gl, gloo, glm

vertex = """
#version 120

// Uniforms
// --------
uniform sampler2D tex_data;
uniform vec2 tex_size;
uniform float char_width;
uniform float char_height;
uniform float rows;
uniform float cols;
uniform float scale;
uniform vec4 foreground;
uniform vec4 background;
uniform vec2 selection;
uniform mat4 projection;

// Attributes
// ----------
attribute float pindex;
attribute float gindex;

// Varyings
// --------
varying vec2 v_texcoord;
varying vec4 v_foreground;
varying vec4 v_background;

// Main
// ----
void main (void)
{
    // Compute char position from pindex
    float x = mod(pindex, cols);
    float y = floor(pindex/cols);
    vec2 P = (vec2(x,y) * vec2(char_width, char_height)) * scale;
    P += vec2(char_height, char_height)*scale/2.0;
    P += vec2(2.0, 2.0);
    gl_Position = projection*vec4(P, 0.0, 1.0);
    gl_PointSize = char_height * scale;

    // Compute color (selection)
    if( (pindex >= selection.x) && (pindex < selection.y))
        v_background = vec4(v_foreground.rgb, 0.1);
    else
        v_background = background;

    // Compute glyph tex coord from gindex
    float n = tex_size.x/char_width;
    x = 0.5 +  mod(gindex, n) * char_width;
    y = 0.5 + floor(gindex/n) * char_height;
    v_texcoord = vec2(x/tex_size.x, y/tex_size.y);
}
"""

fragment = """
#version 120

// Uniforms
// --------
uniform sampler2D tex_data;
uniform vec2 tex_size;
uniform float char_width;
uniform float char_height;
uniform float rows;
uniform float cols;
uniform float scale;
uniform vec2 selection;
uniform vec4 foreground;


// Varyings
// --------
varying vec2 v_texcoord;
varying vec4 v_background;


// Main
// ----
void main(void)
{
    vec2 uv = floor(gl_PointCoord.xy * char_height);
    if(uv.x > (char_width-1.0)) discard;
    if(uv.y > (char_height-1.0)) discard;

    float v = texture2D(tex_data, v_texcoord+uv/tex_size).r;
    gl_FragColor = v * foreground + (1.0-v) * v_background.a;
}
"""


class TextBuffer(object):
    """
    """

    def __init__(self, rows=24, cols=80, x=0, y=0, scale=2):

        # Build program first
        self._program = gloo.Program(vertex, fragment)

        # Build a font array that holds regular, italic & bold font
        # Regular:      0 to   65536-1
        # Italic :  65536 to 2*65536-1
        # Bold :  2*65536 to 3*65536-1
        regular = glumpy.data.get("6x13-regular.npy")
        italic  = glumpy.data.get("6x13-italic.npy")
        bold    = glumpy.data.get("6x13-bold.npy")
        n1 = len(regular)
        n2 = len(italic)
        n3 = len(bold)
        n = n1+n2+n3
        dtype = [ ("code", np.uint32, 1),
                  ("data", np.uint8, 10)]
        font = np.zeros(n, dtype)
        font[:n1] = regular
        font[n1:n1+n2] = italic
        font[n1:n1+n2]["code"] += 1*65536
        font[n1+n2:n1+n2+n3] = bold
        font[n1+n2:n1+n2+n3]["code"] += 2*65536

        # Build a texture out of glyph arrays (need to unpack bits)
        # This code is specific for a character size of 6x13
        n = len(font)
        G = np.unpackbits(font["data"].ravel())
        G = G.reshape(n,80)[:,:78].reshape(n,13,6)
        width, height = 6*128, 13*((n//128)+1)
        data = np.zeros((height,width), np.ubyte)
        for i in range(n):
            r = 13*(i//128)
            c = 6*(i % 128)
            data[r:r+13,c:c+6] = G[i]*255

        # Store char codes
        self._codes = font["code"]

        # Fill program uniforms
        self._program["tex_data"] = data.view(gloo.Texture2D)
        self._program["tex_data"].interpolation = gl.GL_NEAREST
        self._program["tex_data"].wrapping = gl.GL_CLAMP
        self._program["tex_size"] = width, height
        self._program["char_width"] = 6.0
        self._program["char_height"]= 13.0
        self._program["rows"] = rows
        self._program["cols"] = cols
        self._program["scale"]= int(max(1.0, scale))
        self._program["foreground"] = 0, 0, 0, 1
        self._program["background"] = 0, 0, 0, 0
        self._program['selection'] = -1,-1

        # Build vertex buffer
        self._vbuffer = np.zeros(rows*cols, [("pindex", np.float32, 1),
                                             ("gindex", np.float32, 1)])
        self._vbuffer = self._vbuffer.view(gloo.VertexBuffer)
        self._vbuffer["pindex"] = np.arange(rows*cols)
        self._vbuffer["gindex"] = 1 # index of space in our font
        self._program.bind(self._vbuffer)

        self._rows = rows
        self._cols = cols
        self._scale = int(max(scale,1))
        self._selection = None


    def on_init(self):
        gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
        gl.glEnable(gl.GL_POINT_SPRITE)

    def on_resize(self, width, height):
        self._program["projection"] = glm.ortho(0, width, height, 0, -1, +1)

    def draw(self):
        self._program.draw(gl.GL_POINTS)

    def __contains__(self, xy):
        (x,y) = xy
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

        self._vbuffer["gindex"] = 1 # index of space in our font
        self.clear_selection()


    def clear_selection(self):
        """
        Clear current selection
        """

        self._selection = None
        self._program["selection"] = -1,-1


    def put(self, row, col, text, style=0):
        """ Put text at (row,col) """

        # Make style argument is of the right type
        style = np.atleast_1d(style)
        index = row*self.cols + col

        # Decode text
        if isinstance(text, str):
            text = str(text)
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

        # Tweak code to take style into account
        codes += np.uint32(style*65536)

        # Replace unknown glyphs with glyph 0
        codes *= np.in1d(codes, self._codes)

        # Put glyphs data into buffer
        self._vbuffer["gindex"][index:index+n] = np.searchsorted(self._codes, codes)




# -----------------------------------------------------------------------------
class Console(TextBuffer):

    def __init__(self, rows=24, cols=80, x=3, y=3, scale=2, cache=1000):
        TextBuffer.__init__(self, rows, cols, x, y, scale)

        # We use a ring buffer to avoid to have to move things around
        self._buffer_start = 0
        self._buffer_end = 0
        cache = max(cache, rows)
        self._buffer = np.ones((cache+rows,cols),
                               dtype=[("code",       np.uint16,  1),
                                      ("style",      np.uint16,  1)])
        self._buffer["code"] = 32 # space
        self._scroll = -self.rows
        self._default_foreground = 0,0,0,1 # Black
        self._default_background = 0,0,0,0 # Transparent black
        self._default_style      = 0       # Regular
        self._buffer["style"]      = self._default_style



    def write(self, text="", style=None):
        """ Write at current position into the buffer and rotate buffer """

        if style is None:
            style = self._default_style

        n = len(self._buffer)
        empty = 32, 0

        # Clear line
        self._buffer[self._buffer_end] = empty

        # Write line
        self._buffer["code"][self._buffer_end,:len(text)] = [ord(c) for c in text]
        self._buffer["style"][self._buffer_end,:len(text)] = style

        # Clear line beyond row lines in case use want to have only the first
        # line on top (or else we would display buffer start)
        self._buffer[(self._buffer_end+self.rows) % n] = empty

        self._buffer_end = (self._buffer_end + 1) % n
        if self._buffer_end == self._buffer_start:
            self._buffer_start = (self._buffer_start + 1) % n

        # Update text buffer
        # V = self.view(int(self._scroll))
        # self.put(0, 0, text=V["code"])

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
        #V = self.view(int(self._scroll))
        #self.put(0, 0, text=V["code"])

        # Update selection if any
        if self._selection is not None:
            start, end = self._selection
            start -= (int(self._scroll)+self.rows)*self.cols
            end   -= (int(self._scroll)+self.rows)*self.cols
            self._program["selection"] = start, end

    def draw(self):
        V = self.view(int(self._scroll))
        self.put(0, 0, text=V["code"])
        TextBuffer.draw(self)


    def clear(self):
        TextBuffer.clear(self)
        self._buffer_start = 0
        self._buffer_end = 0
        self._buffer[...] = 32,0

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
    console = Console(24,80,scale=2)
    window = app.Window(width=console.cols*console.scale*6,
                        height=console.rows*console.scale*13,
                        color = (1,1,1,1))

    @window.event
    def on_draw(dt):
        window.clear(), console.draw()

    import codecs
    f = codecs.open("UTF-8-demo.txt", "r", "utf-8")
    # f = codecs.open("TeX.txt", "r", "utf-8")
    lines = f.readlines()
    for line in lines:
        console.write(line[:-1])

    # @window.timer(1/30.0)
    def timer(fps):
        console.clear()
        console.write("─────────────────────────────────────────────────────")
        console.write("GLUMPY 2.0 - Copyright (c) 2014 Nicolas P. Rougier")
        console.write("")
        console.write(" → Window size: %dx%d" % (window.width, window.height))
        console.write(" → Backend: %s (%s)" % (window._backend.__name__,
                                              window._backend.__version__))
        console.write(" → Console size: %dx%d" % (console.rows, console.cols))
        console.write(" → Actual FPS: %.2f frames/second  " % (app.fps()))
        console.write("───────────────────────────────────────────────────────")
        #for line in repr(window.config).split("\n"):
        #    console.write(u" "+line)
        #console.write(u"───────────────────────────────────────────────────────")

    window.attach(console)
    app.run()
