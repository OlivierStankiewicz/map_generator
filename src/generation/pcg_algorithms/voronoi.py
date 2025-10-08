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

def voronoi(terrain_weights: Dict[TerrainType, int], height: int, width: int, alpha: int = 5) -> List[List[TerrainType]]:
    """
    Generate a Voronoi map with specified dimensions and number of regions.
    Useful info: http://pcg.wikidot.com/pcg-algorithm:voronoi-diagram
    """
    num_of_regions = sum(weight * alpha for weight in terrain_weights.values())
    regions = generate_voronoi_regions(n=num_of_regions, height=height, width=width)

    sorted_terrains = sorted(terrain_weights.items(), key=lambda kv: kv[1])
    regions_for_terrain = {terrain: [] for terrain in terrain_weights} # list for storing current regions assigned to each terrain

    # phase 1: pick initial seed regions for each terrain type
    
    def pick_seed(terrain: TerrainType, target_size: int) -> VoronoiRegion:
        """
        Pick initial seed region for a terrain, provided chosen region has enough neighbors.
        """
        seed = random.choice([r for r in regions if r.terrain_type is None])
        # ensure the chosen region has enough neighbors
        while len(seed.neighbors) < target_size:
            seed = random.choice(regions)
        seed.terrain_type = terrain
        seed.iteration = 1
        regions_for_terrain[terrain].append(seed)
        
        return seed
    
    seeds = {terrain: pick_seed(terrain, weight) for terrain, weight in terrain_weights.items()}
    
    # phase 2: expand from the seeds, assigning terrain types to neighboring regions
    
    def choose_initial_regions_next_to_seed(seed: VoronoiRegion, terrain: TerrainType, weight: int):
        """
        Grow a terrain outward from its seed region.
        """
        region = seed
        for _ in range(weight - 1):
            empty_neighbors = [n for n in region.neighbors if n.terrain_type is None]
            if not empty_neighbors:
                return
            region = random.choice(empty_neighbors)
            region.terrain_type = terrain
            region.iteration = 1
            regions_for_terrain[terrain].append(region)
    
    def get_oldest_region(terrain: TerrainType) -> List[VoronoiRegion]:
        """
        Return the oldest region of a given terrain type (the one with the highest iteration)
        that still has neighbors with unassigned terrain.
        """
        candidates = [
            r for r in regions_for_terrain[terrain]
            if any(n.terrain_type is None for n in r.neighbors)
        ]
        if not candidates:
            return []
        max_iter = max(r.iteration for r in candidates)
        return [r for r in candidates if r.iteration == max_iter]
    
    def expand_terrain(terrain: TerrainType, weight: int):
        """
        Expand terrain from its frontier into unassigned neighbors.
        """
        frontier = get_oldest_region(terrain)
        for _ in range(weight):
            if not frontier:
                return
            region = random.choice(frontier)
            frontier.remove(region)

            empty_neighbors = [n for n in region.neighbors if n.terrain_type is None]
            if not empty_neighbors:
                continue

            new_region = random.choice(empty_neighbors)
            new_region.terrain_type = terrain
            new_region.iteration = region.iteration + 1
            regions_for_terrain[terrain].append(new_region)
            
    for i in range(alpha):
        # repeat alpha iterations for each terrain type    
        for terrain, weight in sorted_terrains:
            if i == 0:
                choose_initial_regions_next_to_seed(seeds[terrain], terrain, weight)
            else:
                expand_terrain(terrain, weight)        
            
        print(f"After iteration {i + 1}:")
        for terrain, regs in regions_for_terrain.items():
                print(f"{terrain.name}: {len(regs)} regions")

    # phase 3: fill the remaining unassigned regions
    
    def assign_unassigned_regions():
        """
        Assign leftover regions based on neighbor majority or terrain weights.
        """
        unassigned = [r for r in regions if r.terrain_type is None]
        unassigned.sort(
            key=lambda r: sum(1 for n in r.neighbors if n.terrain_type),
            reverse=True
        )
        for region in unassigned:
            neighbors = [n for n in region.neighbors if n.terrain_type]
            if neighbors:
                # pick neighbor with highest terrain weight
                best_neighbor = max(neighbors, key=lambda n: terrain_weights[n.terrain_type])
                region.terrain_type = best_neighbor.terrain_type
            else:
                # fallback: assign terrain with the highest weight
                region.terrain_type = max(terrain_weights, key=terrain_weights.get)

    assign_unassigned_regions()
    
    # phase 4: build final map
    
    voronoi_map = [[None for _ in range(width)] for _ in range(height)]
    for region in regions:
        for x, y in region.tiles:
            voronoi_map[y][x] = region.terrain_type

    return voronoi_map
