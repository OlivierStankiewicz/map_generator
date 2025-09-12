from typing import List, Tuple, Set, Dict
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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

def find_neighbors(ownership: List[List[VoronoiRegion]], height: int, width: int):
    """
    Identify neighboring Voronoi regions based on tile adjacency.
    """
    def valid_neighbors(x: int, y: int):
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                yield nx, ny
    
    def add_neighbors(region: VoronoiRegion, neighbors: List[Tuple[int, int]]):
        for nx, ny in neighbors:
            neighbor = ownership[ny][nx]
            if neighbor is not region:
                region.neighbors.add(neighbor)
    
    for y in range(height):
        for x in range(width):
            region = ownership[y][x]
            neighbors = valid_neighbors(x, y)
            add_neighbors(region, neighbors)

def generate_voronoi_regions(n: int, height: int, width: int) -> List[VoronoiRegion]:
    """
    Generate Voronoi regions within a grid of given height and width.
    """
    regions = []
    for _ in range(n):
        sx = random.randint(0, width - 1)
        sy = random.randint(0, height - 1)
        regions.append(VoronoiRegion(sx, sy))

    # 2D array to track which regions are tiles assigned to
    ownership = [[None for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            closest_region = min(regions, key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
            closest_region.tiles.append((x, y))
            ownership[y][x] = closest_region
    
    find_neighbors(height=height, width=width, ownership=ownership)

    return regions

def voronoi(terrain_values: Dict[TerrainType, int], height: int, width: int, alpha: int = 5) -> List[List[TerrainType]]:
    """
    Generate a Voronoi map with specified dimensions and number of regions.
    Useful info: http://pcg.wikidot.com/pcg-algorithm:voronoi-diagram
    """
    num_of_regions = sum(value * alpha for value in terrain_values.values())
    regions = generate_voronoi_regions(n=num_of_regions, height=height, width=width)
    # print(f"Num of tiles: {sum([len(r.tiles) for r in regions])}")

    sorted_terrains = sorted(terrain_values.items(), key=lambda kv: kv[1])
    
    regions_for_terrain = {terrain: [] for terrain in terrain_values} # list for storing current regions assigned to each terrain

    def print_regions_for_terrain():
        for terrain, regions in regions_for_terrain.items():
            print(f"{terrain.name}: {len(regions)} regions")

    def set_initial_seeds() -> Dict[TerrainType, VoronoiRegion]:
        seeds = {}
        for terrain, value in terrain_values.items():
            seed = random.choice([r for r in regions if r.terrain_type is None])
            # ensure the chosen region has enough neighbors
            while len(seed.neighbors) < value:
                seed = random.choice(regions)
            seed.terrain_type = terrain
            regions_for_terrain[terrain].append(seed)
            seeds[terrain] = seed

        return seeds
    
    initial_seeds = set_initial_seeds()
    for i in range(alpha):
        # repeat alpha iterations for each terrain type    
        for terrain, value in sorted_terrains:
            if i == 0:
                # pick one region at random with enough neighbors
                region = initial_seeds[terrain]
                region.iteration = 1
                
                # assign terrain type to neighboring regions
                for _ in range(value - 1):
                    neighbors_with_no_terrain = [n for n in region.neighbors if n.terrain_type is None]
                    if not neighbors_with_no_terrain:
                        break
                    region = random.choice(neighbors_with_no_terrain)
                    region.terrain_type = terrain
                    region.iteration = 1
                    regions_for_terrain[terrain].append(region)
            else:
                def get_oldest_regions_list():
                    """Return a list of the oldest regions with neighbors with no terrain assigned yet for the current terrain type."""
                    regions_with_empty_neighbors = [
                        r for r in regions_for_terrain[terrain]
                        if any(n.terrain_type is None for n in r.neighbors)
                    ]
                    if not regions_with_empty_neighbors:
                        return []
                    max_iter = max(r.iteration for r in regions_with_empty_neighbors)
                    return [r for r in regions_with_empty_neighbors if r.iteration == max_iter]
                                    
                oldest_regions = get_oldest_regions_list()
                # assign given terrain type to the {value} of regions 
                for _ in range(value):
                    if not oldest_regions:
                        break
                    # pick one at random from the oldest regions (with max iterations)
                    oldest = random.choice(oldest_regions)
                    oldest_regions.remove(oldest)
                    
                    neighbors_with_no_terrain = [n for n in oldest.neighbors if n.terrain_type is None]
                    if not neighbors_with_no_terrain:
                        continue
                    
                    new_region = random.choice(neighbors_with_no_terrain)
                    new_region.terrain_type = terrain
                    new_region.iteration = oldest.iteration + 1
                    regions_for_terrain[terrain].append(new_region)

        print(f"After iteration {i + 1}:")
        print_regions_for_terrain()

    # assign any unassigned regions to the terrain type with the highest value
    unassigned = [r for r in regions if r.terrain_type is None]
    # sort by number of neighbors that already have terrain, descending
    unassigned.sort(key=lambda r: sum(1 for n in r.neighbors if n.terrain_type is not None), reverse=True)
    for region in unassigned:
        assigned_neighbors = [n for n in region.neighbors if n.terrain_type is not None]
        if assigned_neighbors:
            # pick neighbor with highest terrain value
            best_neighbor = max(assigned_neighbors, key=lambda n: terrain_values[n.terrain_type])
            region.terrain_type = best_neighbor.terrain_type
        else:
            # fallback: assign terrain with the highest value
            region.terrain_type = max(terrain_values.items(), key=lambda kv: kv[1])[0]
    
    # build final map
    voronoi_map = [[None for _ in range(width)] for _ in range(height)]
    for region in regions:
        for x, y in region.tiles:
            voronoi_map[y][x] = region.terrain_type

    return voronoi_map

def main():
    from classes.tile.Tile import TerrainType
    terrain_values = {
        TerrainType.WATER: 1,
        TerrainType.GRASS: 3,
        TerrainType.SAND: 2,
        TerrainType.DIRT: 3,
    }
    voronoi_map = voronoi(terrain_values, 36, 36)
    for row in voronoi_map:
        print(" ".join(t.name[0] if t else '.' for t in row))

if __name__ == "__main__":
    main()