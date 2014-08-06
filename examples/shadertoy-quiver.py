#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo

vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
// 2D vector field visualization by Matthias Reitinger, @mreitinger
// Based on "2D vector field visualization by Morgan McGuire, http://casual-effects.com", https://www.shadertoy.com/view/4s23DG

const float ARROW_TILE_SIZE = 32.0;

uniform vec2 iResolution;
uniform float iGlobalTime;
uniform float scale;


// Computes the center pixel of the tile containing pixel pos
vec2 arrowTileCenterCoord(vec2 pos) {
	return (floor(pos / ARROW_TILE_SIZE) + 0.5) * ARROW_TILE_SIZE;
}

// Computes the signed distance from a line segment
float line(vec2 p, vec2 p1, vec2 p2) {
	vec2 center = (p1 + p2) * 0.5;
	float len = length(p2 - p1);
	vec2 dir = (p2 - p1) / len;
	vec2 rel_p = p - center;
	float dist1 = abs(dot(rel_p, vec2(dir.y, -dir.x)));
	float dist2 = abs(dot(rel_p, dir)) - 0.5*len;
	return max(dist1, dist2);
}

// v = field sampled at arrowTileCenterCoord(p), scaled by the length
// desired in pixels for arrows
// Returns a signed distance from the arrow
float arrow(vec2 p, vec2 v) {
	// Make everything relative to the center, which may be fractional
	p -= arrowTileCenterCoord(p);

	float mag_v = length(v), mag_p = length(p);

	if (mag_v > 0.0) {
		// Non-zero velocity case
		vec2 dir_v = v / mag_v;

		// We can't draw arrows larger than the tile radius, so clamp magnitude.
		// Enforce a minimum length to help see direction
		mag_v = clamp(mag_v, 5.0, ARROW_TILE_SIZE * 0.5);

		// Arrow tip location
		v = dir_v * mag_v;

		// Signed distance from shaft
		float shaft = line(p, v, -v);
		// Signed distance from head
		float head = min(line(p, v, 0.4*v + 0.2*vec2(-v.y, v.x)),
		                 line(p, v, 0.4*v + 0.2*vec2(v.y, -v.x)));

		return min(shaft, head);
	} else {
		// Signed distance from the center point
		return mag_p;
	}
}

/////////////////////////////////////////////////////////////////////

// The vector field; use your own function or texture
vec2 field(vec2 pos) {
//	return 2.0 * texture2D(iChannel1, mod(pos, 2.0 * iChannelResolution[1].xy) * 0.5 / iChannelResolution[1].xy).xy - 1.0;
//	return 2.0 * texture2D(iChannel0, (pos + vec2(iGlobalTime * 100.0, 0.0)) / iChannelResolution[0].xy).xy - 1.0;
//	return vec2(0.0, 0.0);
	return vec2(cos(pos.x * 0.01 + pos.y * 0.01) + cos(pos.y * 0.005 + iGlobalTime), 2.0 * cos(pos.y * 0.01  + iGlobalTime * 0.3)) * 0.5;
//	return vec2(cos(pos.x * 0.017 + cos(pos.y * 0.004 + iGlobalTime * 0.1) * 6.28 * 4.0) * 3.0, cos(6.28 * cos(pos.y * 0.01 + pos.x * 0.007)));
}

void main(void) {
    float scale = 0.5;
    vec2 P = gl_FragCoord.xy * scale;

	float arrow_dist =
          arrow(P, field(arrowTileCenterCoord(P)) * ARROW_TILE_SIZE * 0.4 / scale);

	vec4 arrow_col = vec4(0, 0, 0, clamp(arrow_dist, 0.0, 1.0));
	vec4 field_col = vec4(1,1,1,1); //vec4(field(gl_FragCoord.xy) * 0.5 + 0.5, 0.5, 1.0);
	gl_FragColor = mix(arrow_col, field_col, arrow_col.a);
}
"""


window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    program.draw(gl.GL_TRIANGLE_STRIP)
    program["iGlobalTime"] += dt

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scale = program["scale"]
    program["scale"] = min(max(1, scale + .01 * dy * scale), 100)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program["iGlobalTime"] = 0
program["scale"] = 10

gl.glClearColor(1,1,1,1)
app.run()
