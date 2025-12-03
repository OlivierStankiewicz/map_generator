from generation.tile_gen.tile_gen import TerrainSpriteType

# N - Native terrain (rock)
# A - any other terrain

rock_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (TerrainSpriteType.CENTER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER
    "AAA\nANN\nANN": (TerrainSpriteType.UPPER_LEFT_OUTER_CORNER, False, False),
    "NAA\nANN\nANN": (TerrainSpriteType.UPPER_LEFT_OUTER_CORNER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER
    "AAA\nNNA\nNNA": (TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER, False, False),
    "AAN\nNNA\nNNA": (TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER
    "ANN\nANN\nAAA": (TerrainSpriteType.LOWER_LEFT_OUTER_CORNER, False, False),
    "ANN\nANN\nNAA": (TerrainSpriteType.LOWER_LEFT_OUTER_CORNER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER
    "NNA\nNNA\nAAA": (TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER, False, False),
    "NNA\nNNA\nAAN": (TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER, False, False),
    
    # LEFT_VERTICAL
    "ANN\nANN\nANN": (TerrainSpriteType.LEFT_VERTICAL, False, False),
    "NNN\nANN\nANN": (TerrainSpriteType.LEFT_VERTICAL, False, False),
    "ANN\nANN\nNNN": (TerrainSpriteType.LEFT_VERTICAL, False, False),
    
    # RIGHT_VERTICAL
    "NNA\nNNA\nNNA": (TerrainSpriteType.RIGHT_VERTICAL, False, False),
    "NNN\nNNA\nNNA": (TerrainSpriteType.RIGHT_VERTICAL, False, False),
    "NNA\nNNA\nNNN": (TerrainSpriteType.RIGHT_VERTICAL, False, False),
    
    # UPPER_HORIZONTAL
    "AAA\nNNN\nNNN": (TerrainSpriteType.UPPER_HORIZONTAL, False, False),
    "AAN\nNNN\nNNN": (TerrainSpriteType.UPPER_HORIZONTAL, False, False),
    "NAA\nNNN\nNNN": (TerrainSpriteType.UPPER_HORIZONTAL, False, False),
    
    # LOWER_HORIZONTAL
    "NNN\nNNN\nAAA": (TerrainSpriteType.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nNAA": (TerrainSpriteType.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nAAN": (TerrainSpriteType.LOWER_HORIZONTAL, False, False),
    
    # UPPER_LEFT_INNER_CORNER
    # "NNN\nNNN\nNNA": (TerrainSpriteType.UPPER_LEFT_INNER_CORNER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER
    # "NNN\nNNN\nANN": (TerrainSpriteType.UPPER_RIGHT_INNER_CORNER, False, False),
    
    # LOWER_LEFT_INNER_CORNER
    # "NNA\nNNN\nNNN": (TerrainSpriteType.LOWER_LEFT_INNER_CORNER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER
    # "ANN\nNNN\nNNN": (TerrainSpriteType.LOWER_RIGHT_INNER_CORNER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nANN\nNNN": (TerrainSpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "AAN\nANN\nNNN": (TerrainSpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "AAN\nANN\nANN": (TerrainSpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nNNA\nNNN": (TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNN": (TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "NAA\nNNA\nNNA": (TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nANN\nAAA": (TerrainSpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nANN\nAAN": (TerrainSpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "ANN\nANN\nAAN": (TerrainSpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNA\nAAA": (TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNA\nNAA": (TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNA\nNNA\nNAA": (TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNA": (TerrainSpriteType.UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nANN": (TerrainSpriteType.UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNA\nNNN\nNNN": (TerrainSpriteType.LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    "ANN\nNNN\nNNN": (TerrainSpriteType.LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
}