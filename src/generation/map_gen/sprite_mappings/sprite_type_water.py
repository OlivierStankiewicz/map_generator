from generation.tile_gen.tile_gen import SpriteType

# N - Native terrain (water)
# A - every other terrain

water_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (SpriteType.CENTER, False, False),
    
    # SAND_OUTER_CORNER
    "AAA\nANN\nANN": (SpriteType.SAND_OUTER_CORNER, False, False),
    "AAA\nNNA\nNNA": (SpriteType.SAND_OUTER_CORNER, True, False),
    "ANN\nANN\nAAA": (SpriteType.SAND_OUTER_CORNER, False, True),
    "NNA\nNNA\nAAA": (SpriteType.SAND_OUTER_CORNER, True, True),
    
    "NAA\nANN\nANN": (SpriteType.SAND_OUTER_CORNER, False, False),
    "AAN\nNNA\nNNA": (SpriteType.SAND_OUTER_CORNER, True, False),
    "ANN\nANN\nNAA": (SpriteType.SAND_OUTER_CORNER, False, True),
    "NNA\nNNA\nAAN": (SpriteType.SAND_OUTER_CORNER, True, True),
    
    # SAND_EDGE_VERTICAL
    "ANN\nANN\nANN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNA": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "NNN\nANN\nANN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNN\nNNA\nNNA": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "ANN\nANN\nNNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNN": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "YNN\nANN\nANN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNY\nNNA\nNNA": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    "ANN\nANN\nYNN": (SpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNY": (SpriteType.SAND_EDGE_VERTICAL, True, False),
    
    # SAND_EDGE_HORIZONTAL
    "AAA\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nAAA": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "AAN\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nAAN": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NAA\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNAA": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nYAA": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nAAY": (SpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "YAA\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "AAY\nNNN\nNNN": (SpriteType.SAND_EDGE_HORIZONTAL, False, False),
    
    # SAND_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNA": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nANN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNA\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "ANN\nNNN\nNNN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "ANN\nNNN\nNNA": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True), # special case for half water
    "NNA\nNNN\nANN": (SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    
    # SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAN\nANN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nNAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "AAA\nANN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "AAA\nNNA\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nAAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "AAN\nANN\nANN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "ANN\nANN\nAAN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNA\nNNA\nNAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "AAY\nANN\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YAA\nNNA\nNNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAY": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nYAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "AAN\nANN\nYNN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNY": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nANN\nAAN": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNA\nNAA": (SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
}