'''
N - NATIVE (SAME TYPE AS MIDDLE)
X - SAND/ROCK/WATER
Y - DIRT/GRASS/SNOW/SWAMP/ROUGH/SUBTERRANEAN/LAVA (DIRT BASED TYPES)
'''

from generation.tile_gen.tile_gen import TerrainSpriteType

dirt_based_terrain_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (TerrainSpriteType.CENTER, False, False),
    
    # SAND_OUTER_CORNER
    "XXX\nXNN\nXNN": (TerrainSpriteType.SAND_OUTER_CORNER, False, False),
    "XXX\nNNX\nNNX": (TerrainSpriteType.SAND_OUTER_CORNER, True, False),
    "XNN\nXNN\nXXX": (TerrainSpriteType.SAND_OUTER_CORNER, False, True),
    "NNX\nNNX\nXXX": (TerrainSpriteType.SAND_OUTER_CORNER, True, True),
    
    "YXX\nXNN\nXNN": (TerrainSpriteType.SAND_OUTER_CORNER, False, False),    
    "XXY\nNNX\nNNX": (TerrainSpriteType.SAND_OUTER_CORNER, True, False),
    "XNN\nXNN\nYXX": (TerrainSpriteType.SAND_OUTER_CORNER, False, True),
    "NNX\nNNX\nXXY": (TerrainSpriteType.SAND_OUTER_CORNER, True, True),

    "NXX\nXNN\nXNN": (TerrainSpriteType.SAND_OUTER_CORNER, False, False),
    "XXN\nNNX\nNNX": (TerrainSpriteType.SAND_OUTER_CORNER, True, False),
    "XNN\nXNN\nNXX": (TerrainSpriteType.SAND_OUTER_CORNER, False, True),
    "NNX\nNNX\nXXN": (TerrainSpriteType.SAND_OUTER_CORNER, True, True),
    
    # SAND_EDGE_VERTICAL
    "XNN\nXNN\nXNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNX": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "NNN\nXNN\nXNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNN\nNNX\nNNX": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "XNN\nXNN\nNNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "YNN\nXNN\nXNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNY\nNNX\nNNX": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "XNN\nXNN\nYNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNY": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    
    # SAND_EDGE_HORIZONTAL
    "XXX\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXX": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "XXN\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NXX\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNXX": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nYXX": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nXXY": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "YXX\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "XXY\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    
    # SAND_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNX": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nXNN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNX\nNNN\nNNN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XNN\nNNN\nNNN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
    "XXN\nXNN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nNXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "XXX\nXNN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "XXX\nNNX\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nXXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "XXN\nXNN\nXNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "XNN\nXNN\nXXN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNX\nNNX\nNXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "XXY\nXNN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YXX\nNNX\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXY": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nYXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "XXN\nXNN\nYNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNY": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nXNN\nXXN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNX\nNXX": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # SAND_CONNECTOR
    "XNN\nNNN\nNNX": (TerrainSpriteType.SAND_CONNECTOR, False, False),
    "NNX\nNNN\nXNN": (TerrainSpriteType.SAND_CONNECTOR, True, False),
    
    # SAND
    "NNX\nXNN\nXXN": (TerrainSpriteType.SAND, False, False),
    "NXX\nNNX\nXNN": (TerrainSpriteType.SAND, True, False),
    "XNN\nNNX\nNXX": (TerrainSpriteType.SAND, False, True),
    "XXN\nXNN\nNNX": (TerrainSpriteType.SAND, True, True),
    
    # DIRT_OUTER_CORNER
    "YYY\nYNN\nYNN": (TerrainSpriteType.DIRT_OUTER_CORNER, False, False),
    "YYY\nNNY\nNNY": (TerrainSpriteType.DIRT_OUTER_CORNER, True, False),
    "YNN\nYNN\nYYY": (TerrainSpriteType.DIRT_OUTER_CORNER, False, True),
    "NNY\nNNY\nYYY": (TerrainSpriteType.DIRT_OUTER_CORNER, True, True),

    "NYY\nYNN\nYNN": (TerrainSpriteType.DIRT_OUTER_CORNER, False, False),
    "YYN\nNNY\nNNY": (TerrainSpriteType.DIRT_OUTER_CORNER, True, False),
    "YNN\nYNN\nNYY": (TerrainSpriteType.DIRT_OUTER_CORNER, False, True),
    "NNY\nNNY\nYYN": (TerrainSpriteType.DIRT_OUTER_CORNER, True, True),
    
    # DIRT_EDGE_VERTICAL
    "YNN\nYNN\nYNN": (TerrainSpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNY\nNNY\nNNY": (TerrainSpriteType.DIRT_EDGE_VERTICAL, True, False),
    "NNN\nYNN\nYNN": (TerrainSpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNN\nNNY\nNNY": (TerrainSpriteType.DIRT_EDGE_VERTICAL, True, False),
    "YNN\nYNN\nNNN": (TerrainSpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNY\nNNY\nNNN": (TerrainSpriteType.DIRT_EDGE_VERTICAL, True, False),
    
    # DIRT_EDGE_HORIZONTAL
    "YYY\nNNN\nNNN": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nYYY": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    "YYN\nNNN\nNNN": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nYYN": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    "NYY\nNNN\nNNN": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNYY": (TerrainSpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    
    # DIRT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNY": (TerrainSpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nYNN": (TerrainSpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNY\nNNN\nNNN": (TerrainSpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "YNN\nNNN\nNNN": (TerrainSpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "YYN\nYNN\nNNN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nNNN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nYNN\nYYN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNY\nNYY": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "YYY\nYNN\nNNN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YYY\nNNY\nNNN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nYNN\nYYY": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNY\nYYY": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "YYN\nYNN\nYNN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nNNY": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nYNN\nYYN": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNY\nNYY": (TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    # DIRT_CONNECTOR
    "YNN\nNNN\nNNY": (TerrainSpriteType.DIRT_CONNECTOR, False, False),
    "NNY\nNNN\nYNN": (TerrainSpriteType.DIRT_CONNECTOR, True, False),
    
    # DIRT
    "NNY\nYNN\nYYN": (TerrainSpriteType.DIRT, False, False),
    "NYY\nNNY\nYNN": (TerrainSpriteType.DIRT, True, False),
    "YNN\nNNY\nNYY": (TerrainSpriteType.DIRT, False, True),
    "YYN\nYNN\nNNY": (TerrainSpriteType.DIRT, True, True),
    
    # MIXED_CONNECTOR
    "YNN\nNNN\nNNX": (TerrainSpriteType.MIXED_CONNECTOR, False, False),
    "NNY\nNNN\nXNN": (TerrainSpriteType.MIXED_CONNECTOR, True, False),
    "NNX\nNNN\nYNN": (TerrainSpriteType.MIXED_CONNECTOR, False, True),
    "XNN\nNNN\nNNY": (TerrainSpriteType.MIXED_CONNECTOR, True, True),
    
    # MIXED_OUTER_CORNER_VERTICAL_SAND
    "NNX\nNNX\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nYYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nYYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYY\nNNX\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "YYY\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNY\nNNX\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "YNN\nXNN\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nYYN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nNYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYN\nNNX\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "NYY\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNN\nNNX\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "NNN\nXNN\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nNYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nYYN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "NYY\nNNX\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "YYN\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
        
    # MIXED_OUTER_CORNER_HORIZONTAL_SAND
    "NNY\nNNY\nXXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXX\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXX\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nYXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXY\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "YXX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nYXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "YXX\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXY\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nNXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXN\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "NXX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nNXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "NXX\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXN\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),

    "NNN\nNNY\nXXY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "NNN\nYNN\nYXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXY\nNNY\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "YXX\nYNN\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nYXX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXY\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "YXX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    # MIXED_EDGE_VERTICAL
    "NNY\nNNY\nNNX": (TerrainSpriteType.MIXED_EDGE_VERTICAL, False, False),
    "YNN\nYNN\nXNN": (TerrainSpriteType.MIXED_EDGE_VERTICAL, True, False),
    "NNX\nNNY\nNNY": (TerrainSpriteType.MIXED_EDGE_VERTICAL, False, True),
    "XNN\nYNN\nYNN": (TerrainSpriteType.MIXED_EDGE_VERTICAL, True, True),

    "NNY\nNNY\nNNX": (TerrainSpriteType.MIXED_EDGE_VERTICAL, False, False),
    "YNN\nYNN\nXNN": (TerrainSpriteType.MIXED_EDGE_VERTICAL, True, False),
    "NNX\nNNY\nNNY": (TerrainSpriteType.MIXED_EDGE_VERTICAL, False, True),
    "XNN\nYNN\nYNN": (TerrainSpriteType.MIXED_EDGE_VERTICAL, True, True),

    # MIXED_EDGE_HORIZONTAL
    "NNN\nNNN\nYYX": (TerrainSpriteType.MIXED_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXYY": (TerrainSpriteType.MIXED_EDGE_HORIZONTAL, True, False),
    "YYX\nNNN\nNNN": (TerrainSpriteType.MIXED_EDGE_HORIZONTAL, False, True),
    "XYY\nNNN\nNNN": (TerrainSpriteType.MIXED_EDGE_HORIZONTAL, True, True),
    
    # MIXED_OUTER_CORNER_VERTICAL_DIRT
    "NNY\nNNY\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "YNN\nYNN\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XNN\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "NNX\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    "NNN\nNNY\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "NNN\nYNN\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XYY\nNNY\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "YYX\nYNN\nNNN": (TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    # MIXED_OUTER_CORNER_HORIZONTAL_DIRT
    "NNX\nNNN\nYYN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nNNN\nNYY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYN\nNNN\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "NYY\nNNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    "NNX\nNNY\nYYY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYYY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYY\nNNY\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YYY\nYNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),

    "NNX\nNNY\nNYY": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYYN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "NYY\nNNY\nNNX": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YYN\nYNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    # MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER
    "YNN\nNNX\nNXX": (TerrainSpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNY\nXNN\nXNN": (TerrainSpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NXX\nNNX\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XXN\nXNN\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # MIXED_INNER_CORNER_NEXT_TO_HALF_WATER
    "YYN\nYNN\nNNX": (TerrainSpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nXNN": (TerrainSpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNX\nYYN\nYNN": (TerrainSpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XNN\nNYY\nNNY": (TerrainSpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # MIXED_CONNECTOR_BETWEEN_HALF_WATERS
    "NNX\nNNY\nXYY": (TerrainSpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, False, False),
    "XNN\nYNN\nYYX": (TerrainSpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, True, False),
    "XYY\nNNY\nNNX": (TerrainSpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, False, True),
    "YYX\nYNN\nXNN": (TerrainSpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS, True, True),
    
    # MIXED_OUTER_CORNER_DIAGONAL_SAND
    "NNY\nNNY\nYYX": (TerrainSpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, False, False),
    "YNN\nYNN\nXYY": (TerrainSpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, True, False),
    "YYX\nNNY\nNNY": (TerrainSpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, False, True),
    "XYY\nYNN\nYNN": (TerrainSpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND, True, True),
}