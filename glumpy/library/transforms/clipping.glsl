// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
uniform vec4 local_viewport;
uniform vec4 global_viewport;

#ifdef __VERTEX_SHADER__
void transform(void)
{
    vec4 position = gl_Position;

    float w = local_viewport.z / global_viewport.z;
    float h = local_viewport.w / global_viewport.w;
    float x = 2.0*(local_viewport.x / global_viewport.z) - 1.0 + w;
    float y = 2.0*(local_viewport.y / global_viewport.w) - 1.0 + h;

    gl_Position = vec4((x + w*position.x/position.w)*position.w,
                       (y + h*position.y/position.w)*position.w,
                       position.z, position.w);
}
#endif

#ifdef __FRAGMENT_SHADER__
void clipping(void)
{
    vec2 position = gl_FragCoord.xy;
         if( position.x < (local_viewport.x))                  discard;
    else if( position.x > (local_viewport.x+local_viewport.z)) discard;
    else if( position.y < (local_viewport.y))                  discard;
    else if( position.y > (local_viewport.y+local_viewport.w)) discard;
}
#endif
