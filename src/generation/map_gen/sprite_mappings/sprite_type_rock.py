from generation.tile_gen.tile_gen import SpriteType

# N - Native terrain (rock)
# A - any other terrain

rock_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (SpriteType.CENTER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER
    "AAA\nANN\nANN": (SpriteType.UPPER_LEFT_OUTER_CORNER, False, False),
    "NAA\nANN\nANN": (SpriteType.UPPER_LEFT_OUTER_CORNER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER
    "AAA\nNNA\nNNA": (SpriteType.UPPER_RIGHT_OUTER_CORNER, False, False),
    "AAN\nNNA\nNNA": (SpriteType.UPPER_RIGHT_OUTER_CORNER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER
    "ANN\nANN\nAAA": (SpriteType.LOWER_LEFT_OUTER_CORNER, False, False),
    "ANN\nANN\nNAA": (SpriteType.LOWER_LEFT_OUTER_CORNER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER
    "NNA\nNNA\nAAA": (SpriteType.LOWER_RIGHT_OUTER_CORNER, False, False),
    "NNA\nNNA\nAAN": (SpriteType.LOWER_RIGHT_OUTER_CORNER, False, False),
    
    # LEFT_VERTICAL
    "ANN\nANN\nANN": (SpriteType.LEFT_VERTICAL, False, False),
    "NNN\nANN\nANN": (SpriteType.LEFT_VERTICAL, False, False),
    "ANN\nANN\nNNN": (SpriteType.LEFT_VERTICAL, False, False),
    
    # RIGHT_VERTICAL
    "NNA\nNNA\nNNA": (SpriteType.RIGHT_VERTICAL, False, False),
    "NNN\nNNA\nNNA": (SpriteType.RIGHT_VERTICAL, False, False),
    "NNA\nNNA\nNNN": (SpriteType.RIGHT_VERTICAL, False, False),
    
    # UPPER_HORIZONTAL
    "AAA\nNNN\nNNN": (SpriteType.UPPER_HORIZONTAL, False, False),
    "AAN\nNNN\nNNN": (SpriteType.UPPER_HORIZONTAL, False, False),
    "NAA\nNNN\nNNN": (SpriteType.UPPER_HORIZONTAL, False, False),
    
    # LOWER_HORIZONTAL
    "NNN\nNNN\nAAA": (SpriteType.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nNAA": (SpriteType.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nAAN": (SpriteType.LOWER_HORIZONTAL, False, False),
    
    # UPPER_LEFT_INNER_CORNER
    # "NNN\nNNN\nNNA": (SpriteType.UPPER_LEFT_INNER_CORNER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER
    # "NNN\nNNN\nANN": (SpriteType.UPPER_RIGHT_INNER_CORNER, False, False),
    
    # LOWER_LEFT_INNER_CORNER
    # "NNA\nNNN\nNNN": (SpriteType.LOWER_LEFT_INNER_CORNER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER
    # "ANN\nNNN\nNNN": (SpriteType.LOWER_RIGHT_INNER_CORNER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nANN\nNNN": (SpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "AAN\nANN\nNNN": (SpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "AAN\nANN\nANN": (SpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nNNA\nNNN": (SpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNN": (SpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "NAA\nNNA\nNNA": (SpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nANN\nAAA": (SpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nANN\nAAN": (SpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "ANN\nANN\nAAN": (SpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNA\nAAA": (SpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNA\nNAA": (SpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNA\nNNA\nNAA": (SpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNA": (SpriteType.UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nANN": (SpriteType.UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNA\nNNN\nNNN": (SpriteType.LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    "ANN\nNNN\nNNN": (SpriteType.LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
}