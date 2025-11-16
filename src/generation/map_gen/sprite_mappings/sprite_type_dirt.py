from generation.tile_gen.tile_gen import SpriteType

# N - Native terrain (dirt) or other dirt based terrain types
# X - sand based terrain types

dirt_sprite_mappings = {
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
    "XNN\nXNN\nYNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNX\nNNX\nNNY": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    
    # SAND_EDGE_HORIZONTAL
    "XXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "XXN\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nXXN": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nYXX": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nXXY": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "YXX\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "XXY\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    
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
    
    # SAND
    "NNX\nXNN\nXXN": (SpriteType.SAND, False, False),
    "NXX\nNNX\nXNN": (SpriteType.SAND, True, False),
    "XNN\nNNX\nNXX": (SpriteType.SAND, False, True),
    "XXN\nXNN\nNNX": (SpriteType.SAND, True, True),
}