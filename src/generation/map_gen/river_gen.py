import random
from typing import List
from classes.tile.Tile import TerrainType, RiverType
from generation.pcg_algorithms.random_walk import random_walk_paths


def generate_rivers(tiles: List[List[TerrainType]]) -> List[List[RiverType]]:
    """
    Generate rivers using a generic random-walk PCG algorithm.
    Rivers grow until they hit water/rock or stop randomly.
    Generates 2–4 rivers by default.
    """
    height = len(tiles)
    width = len(tiles[0]) if height > 0 else 0

    river_map = [[RiverType.NONE for _ in range(width)] for _ in range(height)]

    def is_valid_start(y: int, x: int) -> bool:
        return tiles[y][x] not in (TerrainType.WATER, TerrainType.ROCK)

    def is_valid_step(y: int, x: int) -> bool:
        return tiles[y][x] != TerrainType.ROCK

    def should_stop(y: int, x: int) -> bool:
        return tiles[y][x] == TerrainType.WATER or random.random() < 0.05

    num_rivers = random.randint(2, 4)

    river_paths = random_walk_paths(
        width=width,
        height=height,
        num_paths=num_rivers,
        is_valid_start=is_valid_start,
        is_valid_step=is_valid_step,
        should_stop=should_stop,
    )
    
    print(f"Generated {len(river_paths)} rivers.")
    print(river_paths)

    for path in river_paths:
        river_type = RiverType(random.randint(1, 4)) # Random river type between 1 and 4
        for y, x in path:
            river_map[y][x] = river_type

    return river_map
