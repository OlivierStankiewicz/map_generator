from generation.tile_gen.tile_gen import TerrainSpriteType

# N - Native terrain (dirt) or other dirt based terrain types
# X - sand based terrain types

dirt_sprite_mappings = {
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
    
    # SAND
    "NNX\nXNN\nXXN": (TerrainSpriteType.SAND, False, False),
    "NXX\nNNX\nXNN": (TerrainSpriteType.SAND, True, False),
    "XNN\nNNX\nNXX": (TerrainSpriteType.SAND, False, True),
    "XXN\nXNN\nNNX": (TerrainSpriteType.SAND, True, True),
}