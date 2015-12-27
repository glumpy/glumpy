# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.transforms import Position, LogScale, LinearScale, Viewport
from glumpy.transforms import PolarProjection
from glumpy.transforms import HammerProjection
from glumpy.transforms import AzimuthalEqualAreaProjection
from glumpy.transforms import AzimuthalEquidistantProjection
from glumpy.transforms import TransverseMercatorProjection

vertex = """
attribute vec2 position;
varying vec2 v_uv;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_uv = (position + 1.0) / 2.0;
} """

fragment = """
varying vec2 v_uv;

uniform sampler2D texture; // Texture
uniform float antialias;   // Line antialias
uniform vec2  major_step;  // Major ticks step
uniform vec2  minor_step;  // Minor ticks step
uniform float major_width; // Major line width (1.50 pixel)
uniform float minor_width; // Minor line width (0.75 pixel)
uniform vec4  major_color; // Major line color
uniform vec4  minor_color; // Minor line color


// Antialias stroke alpha coeff
float stroke_alpha(float distance, float linewidth, float antialias)
{
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);
    if( border_distance > (linewidth/2.0 + antialias) )
        return 0.0;
    else if( border_distance < 0.0 )
        return 1.0;
    else
        return alpha;
}


// Compute the nearest tick from a value
float get_tick(float value, vec2 bounds, float step)
{
    float vmin = bounds.x;
    float vmax = bounds.y;

    float first_tick = floor((vmin + step/2.0)/step) * step;
    float last_tick  = floor((vmax + step/2.0)/step) * step;
    float tick = vmin + value*(vmax-vmin);
    if (tick < (vmin + (first_tick-vmin)/2.0))
        return vmin;
    if (tick > (last_tick + (vmax-last_tick)/2.0))
        return vmax;
    tick += step/2.0;
    tick = floor(tick/step)*step;
    return clamp(tick,vmin,vmax);
}

// Compute the screen distance (pixels) between P0 and P1
float screen_distance(vec2 P0, vec2 P1)
{
    return length((P0-P1) * <viewport.viewport_global>.zw);
}


void main()
{
    // <scale1>
    // vec2 T1; // Texture coordinates (domain [0,1]x[0,1])
    // vec2 P1; // Cartesian coordinates (range is free)

    // <scale2>
    // vec2 P2; // Projected coordinates (domain is dependent on projection)
    // vec2 T2; // Projected texture coordinates (range [0,1]x[0,1])

    // Get texture coordinates (-> scale1.domain)
    vec2 T1 = v_uv;

    // This scales texture coordinates into cartesian coordinates
    // scale1.domain -> scale1.range
    vec2 P1 = vec2( <scale1.x.forward(T1.x)>,
                    <scale1.y.forward(T1.y)> );

    // Actual projection (scale1.range -> scale2.domain)
    vec2 P2 = <projection.inverse(P1)>;

    // This scales projected coordinates into texture coordinates
    // scale2.domain -> scale2.range
    vec2 T2 = vec2( <scale2.x.forward(P2.x)>,
                    <scale2.y.forward(P2.y)> );

    // Test if we are within limits but we do not discard yet because we want
    // to draw border. Discarding would mean half of the exterior not drawn.
    bvec2 outside = bvec2(false);
    if ( P2.x < <scale2.x.domain>.x ) outside.x = true;
    if ( P2.x > <scale2.x.domain>.y ) outside.x = true;
    if ( P2.y < <scale2.y.domain>.x ) outside.y = true;
    if ( P2.y > <scale2.y.domain>.y ) outside.y = true;

    float tick;
    vec2 P;

    // Compute major x tick
    tick = get_tick(T2.x, <scale2.x.domain>, major_step.x);
    P = <projection.forward(vec2(tick,P2.y))>.xy;
    P = vec2( <scale1.x.inverse(P.x)>, <scale1.y.inverse(P.y)> );
    float Mx = screen_distance(T1, P);

    // Compute major y tick
    tick = get_tick(T2.y, <scale2.y.domain>, major_step.y);
    P = <projection.forward(vec2(P2.x,tick))>.xy;
    P = vec2( <scale1.x.inverse(P.x)>, <scale1.y.inverse(P.y)> );
    float My = screen_distance(T1, P);

    // Compute minor x tick
    tick = get_tick(T2.x, <scale2.x.domain>, minor_step.x);
    P = <projection.forward(vec2(tick,P2.y))>.xy;
    P = vec2( <scale1.x.inverse(P.x)>, <scale1.y.inverse(P.y)> );
    float mx = screen_distance(T1, P);

    // Compute minor y tick
    tick = get_tick(T2.y, <scale2.y.domain>, minor_step.y);
    P = <projection.forward(vec2(P2.x,tick))>.xy;
    P = vec2( <scale1.x.inverse(P.x)>, <scale1.y.inverse(P.y)> );
    float my = screen_distance(T1, P);

    float M = min(Mx,My);
    float m = min(mx,my);


    // Here we take care of "finishing" the border lines
    if( outside.x && outside.y ) {
        if (Mx > 0.5*(major_width + antialias)) {
            discard;
        } else if (My > 0.5*(major_width + antialias)) {
            discard;
        } else {
            M = max(Mx,My);
        }
    } else if( outside.x ) {
        if (Mx > 0.5*(major_width + antialias)) {
            discard;
        } else {
            M = m = Mx;
        }
    } else if( outside.y ) {
        if (My > 0.5*(major_width + antialias)) {
            discard;
        } else {
            M = m = My;
        }
    }

    // Mix major/minor colors to get dominant color
    vec4 color = major_color;
    float alpha1 = stroke_alpha( M, major_width, antialias);
    float alpha2 = stroke_alpha( m, minor_width, antialias);
    float alpha  = alpha1;
    if( alpha2 > alpha1*1.5 )
    {
        alpha = alpha2;
        color = minor_color;
    }

    // For the same price you could project a texture
    if( outside.x || outside.y ) {
        gl_FragColor = vec4(color.rgb, color.a*alpha);
    } else {
        vec4 texcolor = texture2D(texture, T2);
        gl_FragColor = mix(texcolor, color, color.a*alpha);
    }
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
program['major_width'] = 2.0
program['minor_width'] = 1.0
program['major_color'] = 0, 0, 0, 1
program['minor_color'] = 0, 0, 0, 1
program['antialias'] = 1.0
program['viewport'] = Viewport()


# Polar projection
# ----------------

# # This scales texture coordinates into cartesian coordinates
# program['scale1'] = Position(
#     LinearScale(name = 'x', domain=(0,1), range=(-5.1,5.1), discard=False, clamp=False),
#     LinearScale(name = 'y', domain=(0,1), range=(-5.1,5.1), discard=False, clamp=False))

# # Actual projection
# program['projection'] = PolarProjection()
# program['major_step'] = 1.00, np.pi/6
# program['minor_step'] = 0.25, np.pi/60

# # This scales projected coordinates into texture coordinates
# program['scale2'] = Position(
#    LinearScale(name = 'x', domain=(0.0, 5.0),     range=(0,1), discard=False, clamp=False),
#    LinearScale(name = 'y', domain=(0.0, 2*np.pi), range=(0,1), discard=False, clamp=False))


# Transverse Mercator projection
# ------------------------------
# This scales texture coordinates into cartesian coordinates
program['scale1'] = Position(
    LinearScale(name = 'x', domain=(0,1), range=(-1.5,1.5),
                discard=False, clamp=False),
    LinearScale(name = 'y', domain=(1,0), range=(-2.3,2.3),
                discard=False, clamp=False))

# Actual projection
program['projection'] = TransverseMercatorProjection()

program['major_step'] = np.array([ 1.00, 0.50]) * np.pi/ 6.0
program['minor_step'] = np.array([ 1.00, 0.50]) * np.pi/30.0

# This scales projected coordinates into texture coordinates
program['scale2'] = Position(
    LinearScale(name = 'x', domain=(-np.pi, np.pi), range=(0,1),
                discard=False, clamp=False),
    LinearScale(name = 'y', domain=(-np.pi/2, np.pi/2), range=(0,1),
                discard=False, clamp=False))
window.set_size(500,800)



# Azimuthal equidistant
# ---------------------
# This scales texture coordinates into cartesian coordinates
# program['scale1'] = Position(
#     LinearScale(name = 'x', domain=(0,1), range=(-3.,3.),
#                 discard=False, clamp=False),
#     LinearScale(name = 'y', domain=(1,0), range=(-3.,3.),
#                 discard=False, clamp=False))

# # Actual projection
# # program['projection'] = AzimuthalEqualAreaProjection()
# program['projection'] = AzimuthalEquidistantProjection()
# program['major_step'] = np.array([ 1.0, 1.0]) * np.pi/6.0
# program['minor_step'] = np.array([ 1.0, 1.0]) * np.pi/18.0

# # This scales projected coordinates into texture coordinates
# program['scale2'] = Position(
#     LinearScale(name = 'x', domain=(-np.pi, np.pi), range=(0,1),
#                 discard=False, clamp=False),
#     LinearScale(name = 'y', domain=(-np.pi/2, np.pi/2), range=(0,1),
#                 discard=False, clamp=False))
# window.set_size(800,800)



@window.event
def on_mouse_scroll(x, y, dx, dy):
    vmin, vmax = program['scale2']['y']['domain']
    if dy > 0:
        if vmin > -np.pi/2:
            vmin -= 0.05
        else:
            vmax -= 0.05
    elif dy < 0:
        if vmax < np.pi/2:
            vmax += 0.05
        else:
            vmin += 0.05

    vmin = min(max(vmin,-np.pi/2),0)
    vmax = max(min(vmax,+np.pi/2),0)
    program['scale2']['y']['domain'] = vmin, vmax

window.attach(program["viewport"])
app.run()
