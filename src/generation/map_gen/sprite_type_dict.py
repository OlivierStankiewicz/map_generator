'''
N - NATIVE (SAME TYPE AS MIDDLE)
A - ANY TERRAIN
S - SAND
D - DIRT
W - WATER
X - SAND/ROCK/WATER
Y - DIRT/GRASS/SNOW/SWAMP/ROUGH/SUBTERRANEAN/LAVA
_! - Z WYŁĄCZENIEM NATIVE TYPE

TO WSZYSTKO JEST DLA N=GRASS
JEŚLI JEST INNE OZNACZENIE NIŻ N, TO ZNACZY ŻE NIE MOŻE BYĆ N
'''

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
    "NNN\nXNN\nXNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNN\nNNX\nNNX": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "XNN\nXNN\nNNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNN": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "YNN\nXNN\nXNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNY\nNNX\nNNX": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "NNX\nNNX\nNNY": (SpriteType.SAND_EDGE_VERTICAL, False, True),
    "XNN\nXNN\nYNN": (SpriteType.SAND_EDGE_VERTICAL, True, True),
    
    # SAND_EDGE_HORIZONTAL
    "XXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "XXN\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXN": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    
    # SAND_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNX": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nXNN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNX\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "XNN\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
    "XXN\nXNN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nNXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "XXX\nXNN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "XXX\nNNX\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nXXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "XXN\nXNN\nXNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "XNN\nXNN\nXXN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNX\nNNX\nNXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "XXY\nXNN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YXX\nNNX\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nXNN\nXXY": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNX\nYXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "XXN\nXNN\nYNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NXX\nNNX\nNNY": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nXNN\nXXN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNX\nNXX": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
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
    "YNN\nYNN\nYNN": (SpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNY\nNNY\nNNY": (SpriteType.DIRT_EDGE_VERTICAL, True, False),
    "NNN\nYNN\nYNN": (SpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNN\nNNY\nNNY": (SpriteType.DIRT_EDGE_VERTICAL, True, False),
    "YNN\nYNN\nNNN": (SpriteType.DIRT_EDGE_VERTICAL, False, False),
    "NNY\nNNY\nNNN": (SpriteType.DIRT_EDGE_VERTICAL, True, False),
    
    # DIRT_EDGE_HORIZONTAL
    "YYY\nNNN\nNNN": (SpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nYYY": (SpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    "YYN\nNNN\nNNN": (SpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nYYN": (SpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    "NYY\nNNN\nNNN": (SpriteType.DIRT_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNYY": (SpriteType.DIRT_EDGE_HORIZONTAL, False, True),
    
    # DIRT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNY": (SpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nYNN": (SpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNY\nNNN\nNNN": (SpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "YNN\nNNN\nNNN": (SpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    # DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "YYN\nYNN\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nYNN\nYYN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNY\nNYY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "YYY\nYNN\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YYY\nNNY\nNNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nYNN\nYYY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNY\nYYY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "YYN\nYNN\nYNN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NYY\nNNY\nNNY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nYNN\nYYN": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNY\nNYY": (SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

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
    "NNX\nNNX\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    "NNX\nNNX\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nYYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nYYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYY\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "YYY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    "NNY\nNNX\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "YNN\nXNN\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    "NNX\nNNX\nYYN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "XNN\nXNN\nNYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYN\nNNX\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "NYY\nXNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    "NNN\nNNX\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, False),
    "NNN\nXNN\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, False),
    "YYX\nNNX\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, False, True),
    "XYY\nXNN\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND, True, True),
    
    # MIXED_OUTER_CORNER_HORIZONTAL_SAND
    "NNY\nNNY\nXXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    "NNY\nNNY\nXXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nYXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXY\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "YXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    "NNY\nNNY\nYXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "YXX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXY\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    
    "NNY\nNNY\nXXN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nNXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXN\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "NXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),
    "NNY\nNNY\nNXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "YNN\nYNN\nXXN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "NXX\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "XXN\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),

    
    "NNN\nNNY\nXXY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, False),
    "NNN\nYNN\nYXX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, False),
    "XXY\nNNY\nNNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, False, True),
    "YXX\nYNN\nNNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND, True, True),

    "NNY\nNNY\nXXY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "YNN\nYNN\nYXX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XXY\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "YXX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    # MIXED_EDGE_VERTICAL
    "NNY\nNNY\nNNX": (SpriteType.MIXED_EDGE_VERTICAL, False, False),
    "YNN\nYNN\nXNN": (SpriteType.MIXED_EDGE_VERTICAL, True, False),
    "NNX\nNNY\nNNY": (SpriteType.MIXED_EDGE_VERTICAL, False, True),
    "XNN\nYNN\nYNN": (SpriteType.MIXED_EDGE_VERTICAL, True, True),

    "NNY\nNNY\nNNX": (SpriteType.MIXED_EDGE_VERTICAL, False, False),
    "YNN\nYNN\nXNN": (SpriteType.MIXED_EDGE_VERTICAL, True, False),
    "NNX\nNNY\nNNY": (SpriteType.MIXED_EDGE_VERTICAL, False, True),
    "XNN\nYNN\nYNN": (SpriteType.MIXED_EDGE_VERTICAL, True, True),

    # MIXED_EDGE_HORIZONTAL
    "NNN\nNNN\nYXX": (SpriteType.MIXED_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXY": (SpriteType.MIXED_EDGE_HORIZONTAL, True, False),
    "YXX\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, False, True),
    "XXY\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, True, True),

    "NNN\nNNN\nYYX": (SpriteType.MIXED_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXYY": (SpriteType.MIXED_EDGE_HORIZONTAL, True, False),
    "YYX\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, False, True),
    "XYY\nNNN\nNNN": (SpriteType.MIXED_EDGE_HORIZONTAL, True, True),
    
    # MIXED_OUTER_CORNER_VERTICAL_DIRT
    "NNY\nNNY\nXNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "YNN\nYNN\nNNX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XNN\nNNY\nNNY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "NNX\nYNN\nYNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    "NNN\nNNY\nXYY": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, False),
    "NNN\nYNN\nYYX": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, False),
    "XYY\nNNY\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, False, True),
    "YYX\nYNN\nNNN": (SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT, True, True),
    
    # MIXED_OUTER_CORNER_HORIZONTAL_DIRT
    "NNX\nNNN\nYYN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nNNN\nNYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYN\nNNN\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "NYY\nNNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
    "NNX\nNNY\nYYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "YYY\nNNY\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YYY\nYNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),

    "NNX\nNNY\nNYY": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, False),
    "XNN\nYNN\nYYN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, False),
    "NYY\nNNY\nNNX": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, False, True),
    "YYN\nYNN\nXNN": (SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT, True, True),
    
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