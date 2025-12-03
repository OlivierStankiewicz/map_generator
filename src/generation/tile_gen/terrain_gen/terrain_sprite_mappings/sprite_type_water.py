from generation.tile_gen.tile_gen import TerrainSpriteType

# N - Native terrain (water)
# A - every other terrain

water_sprite_mappings = {
    # CENTER
    "NNN\nNNN\nNNN": (TerrainSpriteType.CENTER, False, False),
    
    # SAND_OUTER_CORNER
    "AAA\nANN\nANN": (TerrainSpriteType.SAND_OUTER_CORNER, False, False),
    "AAA\nNNA\nNNA": (TerrainSpriteType.SAND_OUTER_CORNER, True, False),
    "ANN\nANN\nAAA": (TerrainSpriteType.SAND_OUTER_CORNER, False, True),
    "NNA\nNNA\nAAA": (TerrainSpriteType.SAND_OUTER_CORNER, True, True),
    
    "NAA\nANN\nANN": (TerrainSpriteType.SAND_OUTER_CORNER, False, False),
    "AAN\nNNA\nNNA": (TerrainSpriteType.SAND_OUTER_CORNER, True, False),
    "ANN\nANN\nNAA": (TerrainSpriteType.SAND_OUTER_CORNER, False, True),
    "NNA\nNNA\nAAN": (TerrainSpriteType.SAND_OUTER_CORNER, True, True),
    
    # SAND_EDGE_VERTICAL
    "ANN\nANN\nANN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNA": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "NNN\nANN\nANN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNN\nNNA\nNNA": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "ANN\nANN\nNNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "YNN\nANN\nANN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNY\nNNA\nNNA": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    "ANN\nANN\nYNN": (TerrainSpriteType.SAND_EDGE_VERTICAL, False, False),
    "NNA\nNNA\nNNY": (TerrainSpriteType.SAND_EDGE_VERTICAL, True, False),
    
    # SAND_EDGE_HORIZONTAL
    "AAA\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nAAA": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "AAN\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nAAN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NAA\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "NNN\nNNN\nNAA": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nYAA": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "NNN\nNNN\nAAY": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, True),
    "YAA\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    "AAY\nNNN\nNNN": (TerrainSpriteType.SAND_EDGE_HORIZONTAL, False, False),
    
    # SAND_INNER_CORNER_NEXT_TO_HALF_WATER
    "NNN\nNNN\nNNA": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NNN\nNNN\nANN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNA\nNNN\nNNN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "ANN\nNNN\nNNN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "ANN\nNNN\nNNA": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, True, True), # special case for half water
    "NNA\nNNN\nANN": (TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER, False, True),
    
    # SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
    "AAN\nANN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nNAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "AAA\nANN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "AAA\nNNA\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nAAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
    
    "AAN\nANN\nANN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "ANN\nANN\nAAN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNA\nNNA\nNAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "AAY\nANN\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "YAA\nNNA\nNNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "NNN\nANN\nAAY": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNN\nNNA\nYAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),

    "AAN\nANN\nYNN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, False),
    "NAA\nNNA\nNNY": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, False),
    "YNN\nANN\nAAN": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, False, True),
    "NNY\nNNA\nNAA": (TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER, True, True),
}