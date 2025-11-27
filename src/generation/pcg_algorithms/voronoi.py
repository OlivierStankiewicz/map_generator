from typing import List, Tuple, Set
import random

from classes.tile.Tile import TerrainType

class VoronoiRegion:
    def __init__(self, seed_x: int, seed_y: int, terrain_type: TerrainType = None):
        self.seed_x = seed_x
        self.seed_y = seed_y
        self.terrain_type = terrain_type
        self.tiles: List[Tuple[int, int]] = []
        self.neighbors: Set["VoronoiRegion"] = set()
        self.iteration = 0

    def __str__(self):
        return (
            f"VoronoiRegion(seed: ({self.seed_x}, {self.seed_y}), "
            f"terrain: {self.terrain_type}, "
            f"tiles: {len(self.tiles)}, "
            f"neighbors: {len(self.neighbors)})"
        )
