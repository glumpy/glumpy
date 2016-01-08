// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------

#ifndef __GEO_POSITION_STRUCT__
#define __GEO_POSITION_STRUCT__
struct GeoPosition
{
    float longitude;
    float latitude;
    bool frozen;   // Prevent further transformation if true
};
#endif
