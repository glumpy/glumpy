//------------------------------------------------------------------------------
//
// author: thomas diewald
// web:    http://thomasdiewald.com
// date:   22.03.2013
//
// WebGL vertex shader: "PixelVoronoiKdTree_frag.glsl"
// for creating a pixel-based voronoi diagram.
// distance to nearest neighbor affects pixel-shading.
// nearest neighbor search is done by traversing a kd-tree.
// the output of this shader is a "distance-map" saved to the alpha-channel.
//
// note: the OpenGL version is much faster and also much simpler!
// webgl has a view annoying restrictions:
//     loops: no while loop, all and everything must be constant
//     arrays: only accessed by constants
//     vector components: access only per constant
//     no bitwise operators
//     precision highp int is limited from -2^16 to 2^16
//     chrome: it seems, that chrome needs more time than firefox to load (or verify??) a shader.
//
//      ... and so on ...
//
// something to remember: using uniforms as buffers offers much more
// flexibility and is a lot faster, than using textures. But since uniforms are
// very limited in size, this only works for a small number of points.
//
// update: arithemtic expressions are used instead if bitwise-ops.
//         index-pointer-based iterative nearest-neighbor-search
//
//------------------------------------------------------------------------------
#version 120
// precision mediump float;
// precision highp int;

// Bit-Shifting
#define SHIFT_15 0x8000
#define SHIFT_08 0x0100
#define SHIFT_01 0x0002

// RS_XX= Right Shift by XX, LS_XX = Left shift by XX
#define RS_15(i) ( (i) / SHIFT_15 )
#define LS_15(i) ( (i) * SHIFT_15 )
#define RS_08(i) ( (i) / SHIFT_08 )
#define LS_08(i) ( (i) * SHIFT_08 )
#define RS_01(i) ( (i) / SHIFT_01 )
#define LS_01(i) ( (i) * SHIFT_01 )

// node index pointer
#define P(i) ( RS_01(i)   ) // parent node
#define L(i) ( LS_01(i)   ) // left child
#define R(i) ( LS_01(i)+1 ) // right child

#define POINT_PREC 0.1 // for scale point coords



varying vec2 v_texcoord;  // fragment position, unnormalized

uniform sampler2D kdtree;
uniform vec2      kdtree_size;

vec2 VEC2_KDTREE_SIZE_INV = 1.0 / (kdtree_size); // precompute textcoord scaling
int  tex_kdtree_width     = int(kdtree_size.x);  // integer-size for texture look up (to get texture row)

struct Node{      // Kd-Tree Node
  vec2 pnt;       // node point
  int  leaf, dim; // leaf, split-dimension
};

struct NN{    // Nearest Neighbor. (really just "dis" is needed!)
  vec2  pnt;  // pixel position, unnormalized!
  float dis;  // init Float.MAX_VALUE;
};



// Kd-Tree Node - texture look up
void getNode(const int n_idx, inout Node node){

  // re-create node: encoding of 32bit rgba:
  //
  //                    bit-pos    24 16  8  0
  //                       rgba    RR GG BB AA
  //   point_y/dim/point_x/leaf    YY DY XX LX ( reversed in .rgba texture )
  //  rebuilt(swizzled) version    LX XX DY YY ( .abgr )

  // 1) tex-coords: s,t
  int t = n_idx/tex_kdtree_width;
  int s = n_idx - t*tex_kdtree_width;
  vec2 st = (vec2(s,t)+0.5) * VEC2_KDTREE_SIZE_INV;

  // 2) texture look-up of rgba normalized float values.
  //    mult with 255 and convert to int, to get original bytes.
  //    if dot(lx_xx_dy_yy,lx_xx_dy_yy) == 0, then node is "non existing".
  ivec4 lx_xx_dy_yy = ivec4(texture2D(kdtree, st).abgr * 255.0); // .abgr !!!

  // 3) shift .rb 8 bytes to the left and merge with .ga
  ivec2 lxxx_dyyy = LS_08( lx_xx_dy_yy.rb ) + lx_xx_dy_yy.ga;

  // 4) extract leaf and dim, which both are saved in the last bit. so shift right by 15.
  ivec2 ld = RS_15( lxxx_dyyy ); // x=leaf, y=dim

  // 5) subtract leaf/dim bits to get x/y coordinates (still integer and scaled)
  ivec2 xy = lxxx_dyyy - LS_15( ld );

  // 6) apply reconstructed values to the node
  node.leaf  = ld.x;                // 0=inter, 1=leaf,
  node.dim   = ld.y;                // dimension: 0 or 1 (for 2d-tree)
  node.pnt   = vec2(xy)*POINT_PREC; // convert x/y to float and scale back.
}


void updateMinDis(inout NN nn, const Node node){
  nn.dis = min( nn.dis, distance(node.pnt, nn.pnt) );
}

float planeDistance(const NN nn, const Node node){
  vec2 d = nn.pnt-node.pnt;
  return (node.dim == 0) ? d.x : d.y; // normal distance to plane, in split-dimension
//  return mix(d.x, d.y, float(node.dim)); // recommended ?!?
}

//
// NEAREST NEIGHBOR SEARCH
//
// general algorithm:
// 1) while traversing down, always choose half-space [HS] the point is in
// 2) while traversing back, check if current min distance is greater
//    than normal distance to split plane. if so, check the other HS too.
//
// instead of using a stack, i use an index-pointer-based iterating process
// by checking/modifying a bit-mask (... 2^depth) to avoid checking the same
// HS again and again (endless recursion). This is BY FAR! the best solution
// when using GLSL-ES 1.0, in GLSL a stackbased solution is probably better.
void getNearestNeighbor(inout NN nn){

  Node node;
  bool down  = true;
  int  n_idx = 1; // 1 = root
  int  depth = 1; // current depth (power of 2 --> bit indicates depth)
  int  dcode = 0; // depth-bits inidicate checked HalfSpaces

  for(int i = 0; i < 500; i++){                    // constant loop (GL ES)

    getNode(n_idx, node);                          // get node from texture
    float pd = planeDistance(nn, node);            // normal dist to split plane

    if(down){                                      // if traversing down
      if( down = (node.leaf == 0) ){               //   if not leaf
        depth = LS_01(depth);                      //     incr depth (go down)
        n_idx = (pd < 0.0) ? L(n_idx) : R(n_idx);  //     get child
      } else {                                     //   else (=leaf)
        updateMinDis(nn, node);                    //     update min distance
        depth = RS_01(depth);                      //     decr depth (go up now)
        n_idx = P(n_idx);                          //     get parent
      }
    } else {                                       // else (=undwinding)
      if(down = ((dcode < depth) &&                //   if not checked yet
                 (abs(pd) < nn.dis)))              //   AND overlapping
      {                                            //     --> check (other) HS
        dcode += depth;                            //     set depth-bit
        depth  = LS_01(depth);                     //     incr depth (go down)
        n_idx  = (pd < 0.0) ? R(n_idx) : L(n_idx); //     get (other) child
      } else {                                     //   else (=undwinding)
        dcode -= (dcode < depth) ? 0 : depth;      //     clear depth-bit
        depth  = RS_01(depth);                     //     decr depth (go up)
        n_idx  = P(n_idx);                         //     get parent
      }
    }

    if(depth == 0) break; // THIS is the end of the nearest neighbor search.
  }
}


//------------------------------------------------------------------------------
// MAIN
//------------------------------------------------------------------------------
void main(void){
  NN nn = NN(v_texcoord, 50000000.0); // init nearest neighbor values
  getNearestNeighbor(nn);              // kd-tree nearest neighbor search

  float d = nn.dis;
  // if (d < 15.0) discard;
  gl_FragColor.rgb = vec3(nn.dis/100.0);
}
