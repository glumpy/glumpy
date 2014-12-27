// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

/* ---------------------------------------------------------
   Compute antialiased fragment color for an outlined shape.

   Parameters:
   -----------

   distance : signed distance to border (in pixels)
   linewidth: Stroke line width (in pixels)
   antialias: Stroke antialiased area (in pixels)
   stroke:    Stroke color
   fill:      Fill color

   Return:
   -------
   Fragment color (vec4)

   --------------------------------------------------------- */

/*
.. Antialias area ........................... y = linewidth/2 - antialias/2

============================================= y = linewidth/2

.. Antialias area ........................... y = linewidth/2 - antialias/2


-- Actual line ------------------------------ y = 0


.. Antialias area ........................... y = linewidth/2 - antialias/2

============================================= y = linewidth/2

.. Antialias area ........................... y = linewidth/2 + antialias/2

*/
vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias/2.0;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else
        frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
    return frag_color;
}
