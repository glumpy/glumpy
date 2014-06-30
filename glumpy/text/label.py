# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy.gl as gl
import glumpy.glm as glm
import glumpy.gloo as gloo
from . texture_font import TextureFont


vertex = """
uniform mat4 u_projection;
uniform vec2 u_position;
uniform vec4 u_color;
uniform float u_offset;

attribute vec2  a_position;
attribute vec2  a_texcoord;
attribute float a_offset;

varying float v_offset;
varying vec2  v_texcoord;
void main()
{
    vec4 position = vec4(a_position+u_position,0.0,1.0);
    gl_Position = u_projection*position;
    v_texcoord = a_texcoord;
    v_offset = 3.0*(a_offset + u_offset);
}
"""

fragment = """
uniform sampler2D u_atlas;
uniform vec4      u_color;
uniform vec2      u_viewport;

varying float v_offset;
varying vec2  v_texcoord;
void main()
{
/*
   vec3 rgb = texture2D(u_atlas, v_texcoord).rgb;
   float r = rgb.r;
   float g = rgb.g;
   float b = rgb.b;
   float t = max(max(r,g),b);

   vec4 color = vec4(u_color.rgb, (r+g+b)/3.0);
   color = t*color + (1.0-t)*vec4(r,g,b, min(min(r,g),b));
   gl_FragColor = vec4(color.rgb, u_color.a*color.a);
*/

    vec4 current = texture2D(u_atlas, v_texcoord);
    vec4 previous= texture2D(u_atlas, v_texcoord+vec2(-1.0,0.0)/u_viewport);
    vec4 next    = texture2D(u_atlas, v_texcoord+vec2(+1.0,0.0)/u_viewport);

    // current = pow(current, vec4(1.0/u_gamma));
    // previous= pow(previous, vec4(1.0/u_gamma));

    float r = current.r;
    float g = current.g;
    float b = current.b;

    if( v_offset < 1.0 )
    {
        float z = v_offset;
        r = mix(current.r, previous.b, z);
        g = mix(current.g, current.r,  z);
        b = mix(current.b, current.g,  z);
    }
    else if( v_offset < 2.0 )
    {
        float z = v_offset - 1.0;
        r = mix(previous.b, previous.g, z);
        g = mix(current.r,  previous.b, z);
        b = mix(current.g,  current.r,  z);
    }
   else //if( v_offset <= 1.0 )
    {
        float z = v_offset - 2.0;
        r = mix(previous.g, previous.r, z);
        g = mix(previous.b, previous.g, z);
        b = mix(current.r,  previous.b, z);
    }

   float t = max(max(r,g),b);
   vec4 color = vec4(u_color.rgb, (r+g+b)/3.0);
   color = t*color + (1.0-t)*vec4(r,g,b, min(min(r,g),b));
   gl_FragColor = vec4( color.rgb, u_color.a*color.a);
}
"""

# Default program to display label
__program__ = None


class Label:
    """
    """

    def __init__(self, text, font, anchor_x='left', anchor_y='baseline'):

        self._font = font
        self._text = text
        self._indices = np.zeros((len(text),6),
                                 dtype=np.uint32)
        self._vertices = np.zeros((len(text),4),
                                  dtype= [('a_position', np.float32, 2),
                                          ('a_texcoord', np.float32, 2),
                                          ('a_offset',   np.float32, 1)])
        pen = [0,0]
        prev = None
        for i,charcode in enumerate(text):
            glyph = font[charcode]
            kerning = glyph.get_kerning(prev)
            x0 = pen[0] + glyph.offset[0] + kerning
            offset = x0-int(x0)
            x0 = int(x0)
            y0 = pen[1] + glyph.offset[1]
            x1 = x0 + glyph.size[0]
            y1 = y0 - glyph.size[1]
            u0, v0, u1, v1 = glyph.texcoords
            self._vertices[i]['a_position'] = (x0,y0),(x0,y1),(x1,y1),(x1,y0)
            self._vertices[i]['a_texcoord'] = (u0,v0),(u0,v1),(u1,v1),(u1,v0)
            self._vertices[i]['a_offset'] = offset
            self._indices[i] = i*4
            self._indices[i] += 0, 1, 2, 0, 2, 3
            pen[0] = pen[0]+glyph.advance[0]/64.0 + kerning
            pen[1] = pen[1]+glyph.advance[1]/64.0
            prev = charcode

        width = pen[0]-glyph.advance[0]/64.0+glyph.size[0]

        if anchor_y == 'top':
            dy = -round(font.ascender)
        elif anchor_y == 'center':
            dy = +round(-font.height/2-font.descender)
        elif anchor_y == 'bottom':
            dy = -round(font.descender)
        else:
            dy = 0

        if anchor_x == 'right':
            dx = -width/1.0
        elif anchor_x == 'center':
            dx = -width/2.0
        else:
            dx = 0
        self._vertices['a_position'] += round(dx), round(dy)
        self._indices = self._indices.view(gloo.IndexBuffer)
        self._vertices = self._vertices.view(gloo.VertexBuffer)


    def draw(self, x=0, y=0, color=(0,0,0,1)):
        global __program__

        if __program__ is None:
            __program__ = gloo.Program(vertex, fragment)

        _, _, w, h = gl.glGetInteger(gl.GL_VIEWPORT)
        program = __program__
        projection = glm.ortho(0, w, 0, h, -1, +1)
        program['u_projection'] = projection
        program['u_color'] = color
        program['u_offset'] = x-int(x)
        program['u_position'] = int(x),y
        program['u_atlas'] = self._font.atlas
        program['u_viewport'] = w,h
        program.bind(self._vertices)

        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc( gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA )
        program.draw(gl.GL_TRIANGLES, self._indices)
