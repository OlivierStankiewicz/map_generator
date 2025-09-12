from typing import List

from classes.tile.Tile import TerrainType

def smooth_map(terrain_map: List[List[TerrainType]], iterations: int = 2) -> List[List[TerrainType]]:
    """
    Smooth terrain borders by majority voting among neighbors.
    
    Args:
        terrain_map: 2D list of TerrainType
        iterations: number of smoothing passes
    
    Returns:
        New smoothed 2D terrain map
    """
    height = len(terrain_map)
    width = len(terrain_map[0])

    def get_neighbors(y, x):
        neighbors = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    neighbors.append(terrain_map[ny][nx])
        return neighbors

    smoothed = [[terrain_map[y][x] for x in range(width)] for y in range(height)]

    for _ in range(iterations):
        new_map = [[smoothed[y][x] for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):
                neighbors = get_neighbors(y, x)
                if not neighbors:
                    continue
                # Count majority type
                counts = {}
                for n in neighbors:
                    counts[n] = counts.get(n, 0) + 1
                majority = max(counts, key=counts.get)

                # If majority overwhelms (e.g. >5/8), replace tile
                if counts[majority] >= 5:
                    new_map[y][x] = majority
        smoothed = new_map

    return smoothed

def upscale_map(map: List[List[TerrainType]]) -> List[List[TerrainType]]:
    """
    Upscale a map so that every tile expands to a 2x2 block of the same terrain type.
    """
    height = len(map)
    width = len(map[0])
    new_height = height * 2
    new_width = width * 2
    upscaled_map = [[None for _ in range(new_width)] for _ in range(new_height)]

    for y in range(height):
        for x in range(width):
            terrain_type = map[y][x]
            upscaled_map[2*y][2*x] = terrain_type
            upscaled_map[2*y][2*x + 1] = terrain_type
            upscaled_map[2*y + 1][2*x] = terrain_type
            upscaled_map[2*y + 1][2*x + 1] = terrain_type

    return upscaled_map