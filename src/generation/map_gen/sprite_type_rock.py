from generation.tile_gen.tile_gen import SpriteTypeRock

# N - Native terrain (rock)
# A - any other terrain

rock_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (SpriteTypeRock.CENTER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER
    "AAA\nANN\nANN": (SpriteTypeRock.UPPER_LEFT_OUTER_CORNER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER
    "AAA\nNNA\nNNA": (SpriteTypeRock.UPPER_RIGHT_OUTER_CORNER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER
    "ANN\nANN\nAAA": (SpriteTypeRock.LOWER_LEFT_OUTER_CORNER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER
    "NNA\nNNA\nAAA": (SpriteTypeRock.LOWER_RIGHT_OUTER_CORNER, False, False),
    
    # LEFT_VERTICAL
    "ANN\nANN\nANN": (SpriteTypeRock.LEFT_VERTICAL, False, False),
    "NNN\nANN\nANN": (SpriteTypeRock.LEFT_VERTICAL, False, False),
    "ANN\nANN\nNNN": (SpriteTypeRock.LEFT_VERTICAL, False, False),
    
    # RIGHT_VERTICAL
    "NNA\nNNA\nNNA": (SpriteTypeRock.RIGHT_VERTICAL, False, False),
    "NNN\nNNA\nNNA": (SpriteTypeRock.RIGHT_VERTICAL, False, False),
    "NNA\nNNA\nNNN": (SpriteTypeRock.RIGHT_VERTICAL, False, False),
    
    # UPPER_HORIZONTAL
    "AAA\nNNN\nNNN": (SpriteTypeRock.UPPER_HORIZONTAL, False, False),
    "AAN\nNNN\nNNN": (SpriteTypeRock.UPPER_HORIZONTAL, False, False),
    "NAA\nNNN\nNNN": (SpriteTypeRock.UPPER_HORIZONTAL, False, False),
    
    # LOWER_HORIZONTAL
    "NNN\nNNN\nAAA": (SpriteTypeRock.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nNAA": (SpriteTypeRock.LOWER_HORIZONTAL, False, False),
    "NNN\nNNN\nAAN": (SpriteTypeRock.LOWER_HORIZONTAL, False, False),
    
    # UPPER_LEFT_INNER_CORNER
    "NNN\nNNN\nNNA": (SpriteTypeRock.UPPER_LEFT_INNER_CORNER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER
    "NNN\nNNN\nANN": (SpriteTypeRock.UPPER_RIGHT_INNER_CORNER, False, False),
    
    # LOWER_LEFT_INNER_CORNER
    "NNA\nNNN\nNNN": (SpriteTypeRock.LOWER_LEFT_INNER_CORNER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER
    "ANN\nNNN\nNNN": (SpriteTypeRock.LOWER_RIGHT_INNER_CORNER, False, False),
    
    # UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nANN\nNNN": (SpriteTypeRock.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "AAN\nANN\nNNN": (SpriteTypeRock.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "AAN\nANN\nANN": (SpriteTypeRock.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAA\nNNA\nNNN": (SpriteTypeRock.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNN": (SpriteTypeRock.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),    
    "NAA\nNNA\nNNA": (SpriteTypeRock.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nANN\nAAA": (SpriteTypeRock.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nANN\nAAN": (SpriteTypeRock.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "ANN\nANN\nAAN": (SpriteTypeRock.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNA\nAAA": (SpriteTypeRock.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNA\nNAA": (SpriteTypeRock.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNA\nNNA\nNAA": (SpriteTypeRock.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    # "NNN\nNNN\nNNA": (SpriteTypeRock.UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    # "NNN\nNNN\nANN": (SpriteTypeRock.UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER
    # "NNA\nNNN\nNNN": (SpriteTypeRock.LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    
    # LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER
    # "ANN\nNNN\nNNN": (SpriteTypeRock.LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
}