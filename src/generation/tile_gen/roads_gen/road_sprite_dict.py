'''
N - NATIVE (SAME TYPE AS MIDDLE)
A - ALL OTHER ROAD TYPES (INCLUDING NO ROAD)
'''

from generation.tile_gen.tile_gen import RoadSpriteType

road_sprite_mappings = {
    # CORNER - lower and right middle as N, upper middle, upper right, left middle and lower left as A
    
    "AAA\nANN\nANA": (RoadSpriteType.CORNER, False, False),
    "AAA\nANN\nANN": (RoadSpriteType.CORNER, False, False),
    "NAA\nANN\nANA": (RoadSpriteType.CORNER, False, False),
    "NAA\nANN\nANN": (RoadSpriteType.CORNER, False, False),

    "AAA\nNNA\nANA": (RoadSpriteType.CORNER, True, False),
    "AAA\nNNA\nNNA": (RoadSpriteType.CORNER, True, False),
    "AAN\nNNA\nANA": (RoadSpriteType.CORNER, True, False),
    "AAN\nNNA\nNNA": (RoadSpriteType.CORNER, True, False),

    "ANA\nANN\nAAA": (RoadSpriteType.CORNER, False, True),
    "ANN\nANN\nAAA": (RoadSpriteType.CORNER, False, True),
    "ANA\nANN\nNAA": (RoadSpriteType.CORNER, False, True),
    "ANN\nANN\nNAA": (RoadSpriteType.CORNER, False, True),

    "ANA\nNNA\nAAA": (RoadSpriteType.CORNER, True, True),
    "NNA\nNNA\nAAA": (RoadSpriteType.CORNER, True, True),
    "ANA\nNNA\nAAN": (RoadSpriteType.CORNER, True, True),
    "NNA\nNNA\nAAN": (RoadSpriteType.CORNER, True, True),
    
    # FLATTENED_CORNER
    
    # 3 tiles might change: upper left, lower left, lower right
    "AAN\nANN\nANA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "AAN\nANN\nANN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "AAN\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "AAN\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAN\nANN\nANA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAN\nANN\nANN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAN\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAN\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    
    # 3 tiles might change: upper left, upper right, lower right
    "AAA\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    # "AAN\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "AAA\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    # "AAN\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAA\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    "NAA\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    # "NAN\nANN\nNNA": (RoadSpriteType.FLATTENED_CORNER, False, False),
    # "NAN\nANN\nNNN": (RoadSpriteType.FLATTENED_CORNER, False, False),
    
    "NAA\nNNA\nANA": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAA\nNNA\nNNA": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAA\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAA\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAN\nNNA\nANA": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAN\nNNA\nNNA": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAN\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "NAN\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    
    "AAA\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    # "NAA\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "AAA\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    # "NAA\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "AAN\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    "AAN\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    # "NAN\nNNA\nANN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    # "NAN\nNNA\nNNN": (RoadSpriteType.FLATTENED_CORNER, True, False),
    
    "ANA\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "ANN\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNA\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNN\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "ANA\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "ANN\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNA\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNN\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    
    "NNA\nANN\nAAA": (RoadSpriteType.FLATTENED_CORNER, False, True),
    # "NNA\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNN\nANN\nAAA": (RoadSpriteType.FLATTENED_CORNER, False, True),
    # "NNN\nANN\nAAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNA\nANN\nNAA": (RoadSpriteType.FLATTENED_CORNER, False, True),
    "NNN\nANN\nNAA": (RoadSpriteType.FLATTENED_CORNER, False, True),
    # "NNA\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    # "NNN\nANN\nNAN": (RoadSpriteType.FLATTENED_CORNER, False, True),
    
    "ANA\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNA\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "ANN\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNN\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "ANA\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNA\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "ANN\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNN\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    
    "ANN\nNNA\nAAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    # "ANN\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNN\nNNA\nAAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    # "NNN\nNNA\nNAA": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "ANN\nNNA\nAAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    "NNN\nNNA\nAAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    # "ANN\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    # "NNN\nNNA\nNAN": (RoadSpriteType.FLATTENED_CORNER, True, True),
    
    # ONE_WAY_CROSSING_VERTICAL - always middle column as N, left middle as A, right middle as N (or the other way round)
    
    # upper corners as A
    "ANA\nANN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANA\nANN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANA\nANN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANA\nANN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    # upper left = A, upper right = N
    "ANN\nANN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANN\nANN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANN\nANN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "ANN\nANN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    # upper left = N, upper right = A
    "NNA\nANN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNA\nANN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNA\nANN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNA\nANN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    # upper corners as N
    "NNN\nANN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNN\nANN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNN\nANN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    "NNN\nANN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, False, False),
    
    # mirrored
    "ANA\nNNA\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANA\nNNA\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANA\nNNA\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANA\nNNA\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    
    "ANN\nNNA\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANN\nNNA\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANN\nNNA\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "ANN\nNNA\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),

    "NNA\nNNA\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNA\nNNA\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNA\nNNA\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNA\nNNA\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    
    "NNN\nNNA\nANA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNN\nNNA\nANN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNN\nNNA\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),
    "NNN\nNNA\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_VERTICAL, True, False),

    # ONE_WAY_CROSSING_HORIZONTAL - middle row as N, upper middle as A, lower middle as N (or the other way round)
    
    # upper corners as A
    "AAA\nNNN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAA\nNNN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAA\nNNN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAA\nNNN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    # upper left = A, upper right = N
    "AAN\nNNN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAN\nNNN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAN\nNNN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "AAN\nNNN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    # upper left = N, upper right = A
    "NAA\nNNN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAA\nNNN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAA\nNNN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAA\nNNN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    # upper corners as N
    "NAN\nNNN\nANA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAN\nNNN\nANN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAN\nNNN\nNNA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    "NAN\nNNN\nNNN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, False),
    
    # mirrored
    "ANA\nNNN\nAAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANA\nNNN\nNAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANA\nNNN\nAAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANA\nNNN\nNAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    
    "ANN\nNNN\nAAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANN\nNNN\nAAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANN\nNNN\nNAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "ANN\nNNN\nNAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    
    "NNA\nNNN\nAAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNA\nNNN\nAAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNA\nNNN\nNAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNA\nNNN\nNAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    
    "NNN\nNNN\nAAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNN\nNNN\nAAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNN\nNNN\nNAA": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    "NNN\nNNN\nNAN": (RoadSpriteType.ONE_WAY_CROSSING_HORIZONTAL, False, True),
    
    # VERTICAL - always middle column as N, left and right middle as A
    
    # upper corners as A
    "ANA\nANA\nANA": (RoadSpriteType.VERTICAL, False, False),
    "ANA\nANA\nNNA": (RoadSpriteType.VERTICAL, False, False),
    "ANA\nANA\nANN": (RoadSpriteType.VERTICAL, False, False),
    "ANA\nANA\nNNN": (RoadSpriteType.VERTICAL, False, False),
    # upper left = A, upper right = N
    "ANN\nANA\nANA": (RoadSpriteType.VERTICAL, False, False),
    "ANN\nANA\nANN": (RoadSpriteType.VERTICAL, False, False),
    "ANN\nANA\nNNA": (RoadSpriteType.VERTICAL, False, False),
    "ANN\nANA\nNNN": (RoadSpriteType.VERTICAL, False, False),
    # upper left = N, upper right = A
    "NNA\nANA\nANA": (RoadSpriteType.VERTICAL, False, False),
    "NNA\nANA\nANN": (RoadSpriteType.VERTICAL, False, False),
    "NNA\nANA\nNNA": (RoadSpriteType.VERTICAL, False, False),
    "NNA\nANA\nNNN": (RoadSpriteType.VERTICAL, False, False),
    # upper corners as N
    "NNN\nANA\nANA": (RoadSpriteType.VERTICAL, False, False),
    "NNN\nANA\nANN": (RoadSpriteType.VERTICAL, False, False),
    "NNN\nANA\nNNA": (RoadSpriteType.VERTICAL, False, False),
    "NNN\nANA\nNNN": (RoadSpriteType.VERTICAL, False, False),
    
    # HORIZONTAL - always middle row as N, upper and lower middle as A
    
    # upper corners as A
    "AAA\nNNN\nAAA": (RoadSpriteType.HORIZONTAL, False, False),
    "AAA\nNNN\nNAA": (RoadSpriteType.HORIZONTAL, False, False),
    "AAA\nNNN\nAAN": (RoadSpriteType.HORIZONTAL, False, False),
    "AAA\nNNN\nNAN": (RoadSpriteType.HORIZONTAL, False, False),
    # upper left = A, upper right = N
    "AAN\nNNN\nAAA": (RoadSpriteType.HORIZONTAL, False, False),
    "AAN\nNNN\nAAN": (RoadSpriteType.HORIZONTAL, False, False),
    "AAN\nNNN\nNAA": (RoadSpriteType.HORIZONTAL, False, False),
    "AAN\nNNN\nNAN": (RoadSpriteType.HORIZONTAL, False, False),
    # upper left = N, upper right = A
    "NAA\nNNN\nAAA": (RoadSpriteType.HORIZONTAL, False, False),
    "NAA\nNNN\nAAN": (RoadSpriteType.HORIZONTAL, False, False),
    "NAA\nNNN\nNAA": (RoadSpriteType.HORIZONTAL, False, False),
    "NAA\nNNN\nNAN": (RoadSpriteType.HORIZONTAL, False, False),
    # upper corners as N
    "NAN\nNNN\nAAA": (RoadSpriteType.HORIZONTAL, False, False),
    "NAN\nNNN\nAAN": (RoadSpriteType.HORIZONTAL, False, False),
    "NAN\nNNN\nNAA": (RoadSpriteType.HORIZONTAL, False, False),
    "NAN\nNNN\nNAN": (RoadSpriteType.HORIZONTAL, False, False),
    
    # VERTICAL_END - middle left and right as A

    # upper corners as A
    "AAA\nANA\nANA": (RoadSpriteType.VERTICAL_END, False, False),
    "AAA\nANA\nNNA": (RoadSpriteType.VERTICAL_END, False, False),
    "AAA\nANA\nANN": (RoadSpriteType.VERTICAL_END, False, False),
    "AAA\nANA\nNNN": (RoadSpriteType.VERTICAL_END, False, False),
    # upper left = A, upper right = N
    "AAN\nANA\nANA": (RoadSpriteType.VERTICAL_END, False, False),
    "AAN\nANA\nANN": (RoadSpriteType.VERTICAL_END, False, False),
    "AAN\nANA\nNNA": (RoadSpriteType.VERTICAL_END, False, False),
    "AAN\nANA\nNNN": (RoadSpriteType.VERTICAL_END, False, False),
    # upper left = N, upper right = A
    "NAA\nANA\nANA": (RoadSpriteType.VERTICAL_END, False, False),
    "NAA\nANA\nANN": (RoadSpriteType.VERTICAL_END, False, False),
    "NAA\nANA\nNNA": (RoadSpriteType.VERTICAL_END, False, False),
    "NAA\nANA\nNNN": (RoadSpriteType.VERTICAL_END, False, False),
    # upper corners as N
    "NAN\nANA\nANA": (RoadSpriteType.VERTICAL_END, False, False),
    "NAN\nANA\nANN": (RoadSpriteType.VERTICAL_END, False, False),
    "NAN\nANA\nNNA": (RoadSpriteType.VERTICAL_END, False, False),
    "NAN\nANA\nNNN": (RoadSpriteType.VERTICAL_END, False, False),
    
    # mirrored
    "ANA\nANA\nAAA": (RoadSpriteType.VERTICAL_END, False, True),
    "ANN\nANA\nAAA": (RoadSpriteType.VERTICAL_END, False, True),
    "NNA\nANA\nAAA": (RoadSpriteType.VERTICAL_END, False, True),
    "NNN\nANA\nAAA": (RoadSpriteType.VERTICAL_END, False, True),

    "ANA\nANA\nNAA": (RoadSpriteType.VERTICAL_END, False, True),
    "NNA\nANA\nNAA": (RoadSpriteType.VERTICAL_END, False, True),
    "ANN\nANA\nNAA": (RoadSpriteType.VERTICAL_END, False, True),
    "NNN\nANA\nNAA": (RoadSpriteType.VERTICAL_END, False, True),

    "ANA\nANA\nAAN": (RoadSpriteType.VERTICAL_END, False, True),
    "NNA\nANA\nAAN": (RoadSpriteType.VERTICAL_END, False, True),
    "ANN\nANA\nAAN": (RoadSpriteType.VERTICAL_END, False, True),
    "NNN\nANA\nAAN": (RoadSpriteType.VERTICAL_END, False, True),

    "ANA\nANA\nNAN": (RoadSpriteType.VERTICAL_END, False, True),
    "NNA\nANA\nNAN": (RoadSpriteType.VERTICAL_END, False, True),
    "ANN\nANA\nNAN": (RoadSpriteType.VERTICAL_END, False, True),
    "NNN\nANA\nNAN": (RoadSpriteType.VERTICAL_END, False, True),
    
    # HORIZONTAL_END - middle top and bottom as A
    
    # first 4: upper corners as A
    "AAA\nANN\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANN\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANN\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANN\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper left = A, upper right = N
    "AAN\nANN\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANN\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANN\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANN\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper left = N, upper right = A
    "NAA\nANN\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANN\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANN\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANN\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper corners as N
    "NAN\nANN\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANN\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANN\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANN\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    
    # mirrored
    "AAA\nNNA\nAAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAA\nNNA\nAAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "AAN\nNNA\nAAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAN\nNNA\nAAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    
    "AAA\nNNA\nNAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "AAN\nNNA\nNAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAA\nNNA\nNAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAN\nNNA\nNAA": (RoadSpriteType.HORIZONTAL_END, True, False),
    
    "AAA\nNNA\nAAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAA\nNNA\nAAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "AAN\nNNA\nAAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAN\nNNA\nAAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    
    "AAA\nNNA\nNAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAA\nNNA\nNAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "AAN\nNNA\nNAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    "NAN\nNNA\nNAN": (RoadSpriteType.HORIZONTAL_END, True, False),
    
    # TWO_WAY_CROSSING - middle row and middle column as N
    
    "ANA\nNNN\nANA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANA\nNNN\nANN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANA\nNNN\nNNA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANA\nNNN\nNNN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    
    "ANN\nNNN\nANA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANN\nNNN\nANN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANN\nNNN\nNNA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "ANN\nNNN\nNNN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    
    "NNA\nNNN\nANA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNA\nNNN\nNNA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNA\nNNN\nANN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNA\nNNN\nNNN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    
    "NNN\nNNN\nANA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNN\nNNN\nNNA": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNN\nNNN\nANN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    "NNN\nNNN\nNNN": (RoadSpriteType.TWO_WAY_CROSSING, False, False),
    
    
    # SPECIAL CASE - singular road (HORIZONTAL_END)
    
    "AAA\nANA\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANA\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANA\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAA\nANA\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper left = A, upper right = N
    "AAN\nANA\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANA\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANA\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "AAN\nANA\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper left = N, upper right = A
    "NAA\nANA\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANA\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANA\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAA\nANA\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    # upper corners as N
    "NAN\nANA\nAAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANA\nAAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANA\nNAA": (RoadSpriteType.HORIZONTAL_END, False, False),
    "NAN\nANA\nNAN": (RoadSpriteType.HORIZONTAL_END, False, False),
    
}