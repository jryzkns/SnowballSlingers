def colorstr2triple( color_str ):
    r, g, b = color_str[ :2 ], color_str[ 2:4 ], color_str[ 4: ]
    return ( int( r, 16 ), int( g, 16 ), int( b, 16 ) )
