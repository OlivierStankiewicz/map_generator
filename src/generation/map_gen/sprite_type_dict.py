from generation.tile_gen.tile_gen import SpriteType

dirt_based_terrain_types_patterns = {
    # CENTER
    "NNN\nNNN\nNNN": (SpriteType.CENTER, False, False),
    
    # SAND_OUTER_CORNER
    "XXX\nXNN\nXNN": (SpriteType.SAND_OUTER_CORNER, False, False),
    "XXX\nNNX\nNNX": (SpriteType.SAND_OUTER_CORNER, True, False),
    "XNN\nXNN\nXXX": (SpriteType.SAND_OUTER_CORNER, False, True),
    "NNX\nNNX\nXXX": (SpriteType.SAND_OUTER_CORNER, True, True),
    
    # SAND_EDGE_VERTICAL
    "XNN\nXNN\nXNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNX": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    
    # SAND_EDGE_HORIZONTAL
    "XXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    
    # SAND_INNER_CORNER
    "NNN\nNNN\nNNX": (SpriteType.SAND_INNER_CORNER, False, False),
    "NNN\nNNN\nXNN": (SpriteType.SAND_INNER_CORNER, True, False),
    "NNX\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER, False, True),
    "XNN\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER, True, True),
    
    # SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
    "XXN\nXNN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nNXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # SAND_CONNECTOR
    "XNN\nNNN\nNNX": (SpriteType.SAND_CONNECTOR, False, False),
    "NNX\nNNN\nXNN": (SpriteType.SAND_CONNECTOR, True, False),
    
    # SAND
    "NNX\nXNN\nXXN": (SpriteType.SAND, False, False),
    "NXX\nNNX\nXNN": (SpriteType.SAND, True, False),
    "XNN\nNNX\nNXX": (SpriteType.SAND, False, True),
    "XXN\nXNN\nNNX": (SpriteType.SAND, True, True),
    
    # DIRT_OUTER_CORNER
    "YYY\nYNN\nYNN": (SpriteType.DIRT_OUTER_CORNER, False, False),
    "YYY\nNNY\nNNY": (SpriteType.DIRT_OUTER_CORNER, True, False),
    "YNN\nYNN\nYYY": (SpriteType.DIRT_OUTER_CORNER, False, True),
    "NNY\nNNY\nYYY": (SpriteType.DIRT_OUTER_CORNER, True, True),
    
    # DIRT_EDGE_VERTICAL
    "NNY\nNNY\nNNY": (SpriteType.DIRT_EDGE_VERTICAL, False, False),
    "YNN\nYNN\nYNN": (SpriteType.DIRT_EDGE_VERTICAL, True, False),
    
    # DIRT_EDGE_HORIZONTAL
    "YYY\nNNN\nNNN": (SpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nYYY": (SpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    
    # DIRT_INNER_CORNER
    "NNN\nNNN\nNNY": (SpriteType.DIRT_INNER_CORNER, False, False),
    "NNN\nNNN\nYNN": (SpriteType.DIRT_INNER_CORNER, True, False),
    "NNY\nNNN\nNNN": (SpriteType.DIRT_INNER_CORNER, False, True),
    "YNN\nNNN\nNNN": (SpriteType.DIRT_INNER_CORNER, True, True),
    
    # DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "YYN\nYNN\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nYNN\nYYN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNY\nNYY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    # DIRT_CONNECTOR
    "YNN\nNNN\nNNY": (SpriteType.DIRT_CONNECTOR, False, False),
    "NNY\nNNN\nYNN": (SpriteType.DIRT_CONNECTOR, True, False),
    
    # DIRT
    "NNY\nYNN\nYYN": (SpriteType.DIRT, False, False),
    "NYY\nNNY\nYNN": (SpriteType.DIRT, True, False),
    "YNN\nNNY\nNYY": (SpriteType.DIRT, False, True),
    "YYN\nYNN\nNNY": (SpriteType.DIRT, True, True),
    
    # MIXED_CONNECTOR
    "YNN\nNNN\nNNX": (SpriteType.MIXED_CONNECTOR, False, False),
    "NNY\nNNN\nXNN": (SpriteType.MIXED_CONNECTOR, True, False),
    "NNX\nNNN\nYNN": (SpriteType.MIXED_CONNECTOR, False, True),
    "XNN\nNNN\nNNY": (SpriteType.MIXED_CONNECTOR, True, True),
    
    # MIXED_OUTER_CORNER_VERTICAL_SAND
    "NNX\nNNX\nYYA": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nAYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYA\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "AYY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    "NNA\nNNX\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "ANN\nXNN\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNA": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nANN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    # MIXED_OUTER_CORNER_HORIZONTAL_SAND
    "NNY\nNNY\nXXA": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nAXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXA\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "AXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    "NNY\nNNY\nAXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXA": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "AXX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXA\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    # MIXED_EDGE_VERTICAL
    "NNY\nNNX\nNNX": (SpriteType.MIXED_EDGE_VERTICAL, False, False),
    "YNN\nXNN\nXNN": (SpriteType.MIXED_EDGE_VERTICAL, True, False),
    "NNX\nNNX\nNNY": (SpriteType.MIXED_EDGE_VERTICAL, False, True),
    "XNN\nXNN\nYNN": (SpriteType.MIXED_EDGE_VERTICAL, True, True),

    # MIXED_EDGE_HORIZONTAL
    "NNN\nNNN\nYXX": (SpriteType.MIXED_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXY": (SpriteType.MIXED_EDGE_HORIZONTAL, True, False),
    "YXX\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, False, True),
    "XXY\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, True, True),
    
    # MIXED_OUTER_CORNER_VERTICAL_DIRT
    "NNY\nNNY\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "YNN\nYNN\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XNN\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "NNX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    "NNN\nNNY\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "NNN\nYNN\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XYY\nNNY\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "YYX\nYNN\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    "NNY\nNNY\nXXY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "YNN\nYNN\nYXX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XXY\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "YXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    # MIXED_OUTER_CORNER_HORIZONTAL_DIRT
    "NNX\nNNN\nYYN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nNNN\nNYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYN\nNNN\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "NYY\nNNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    "NNX\nNNY\nYYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYY\nNNY\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YYY\nYNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    "NNX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "NNY\nNNY\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YNN\nYNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    # MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER
    "YNN\nNNX\nNXX": (SpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NXX\nNNX\nYNN": (SpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XXN\nXNN\nNNY": (SpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # MIXED_INNER_CORNER_NEXT_TO_HALF_WATER
    "YYN\nYNN\nNNX": (SpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nXNN": (SpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNX\nYYN\nYNN": (SpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XNN\nNYY\nNNY": (SpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # MIXED_CONNECTOR_BETWEEN_HALF_WATERS
    "NNX\nNNY\nXYY": (SpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, False, False),
    "XNN\nYNN\nYYX": (SpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, True, False),
    "XYY\nNNY\nNNX": (SpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, False, True),
    "YYX\nYNN\nXNN": (SpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, True, True),
    
    # MIXED_OUTER_CORNER_DIAGONAL_SAND
    "NNX\nNNX\nXXY": (SpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, False, False),
    "XNN\nXNN\nYXX": (SpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, True, False),
    "XXY\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, False, True),
    "YXX\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, True, True),
}