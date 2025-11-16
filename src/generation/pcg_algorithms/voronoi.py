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

class VoronoiMapGenerator:
    def __init__(self, height: int, width: int, terrain_weights: Dict[TerrainType, int], alpha: int = 5):
        self.height = height
        self.width = width
        self.terrain_weights = terrain_weights
        self.alpha = alpha
        
        self.regions: List[VoronoiRegion] = []
        # 2D array to track which regions are tiles assigned to
        self.ownership: List[List[VoronoiRegion]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        # map of terrain types and their assigned regions
        self.regions_for_terrain: Dict[TerrainType, List[VoronoiRegion]] = {}
    
    def find_neighbors(self):
        """
        Identify neighboring Voronoi regions based on tile adjacency.
        """
        def valid_neighbors(x: int, y: int):
            directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    yield nx, ny
        
        def add_neighbors(region: VoronoiRegion, neighbors: List[Tuple[int, int]]):
            for nx, ny in neighbors:
                neighbor = self.ownership[ny][nx]
                if neighbor is not region:
                    region.neighbors.add(neighbor)
        
        for y in range(self.height):
            for x in range(self.width):
                region = self.ownership[y][x]
                neighbors = valid_neighbors(x, y)
                add_neighbors(region, neighbors)

    def generate_voronoi_regions(self, n: int):
        """
        Generate Voronoi regions within a grid of given height and width.
        """
        for _ in range(n):
            sx = random.randint(0, self.width - 1)
            sy = random.randint(0, self.height - 1)
            self.regions.append(VoronoiRegion(sx, sy))
        
        for y in range(self.height):
            for x in range(self.width):
                closest_region = min(self.regions, key=lambda r, x=x, y=y: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
                closest_region.tiles.append((x, y))
                self.ownership[y][x] = closest_region

        self.find_neighbors()

    def pick_seed(self, terrain: TerrainType) -> VoronoiRegion:
        """
        Pick initial seed region for a terrain, provided chosen region has enough neighbors.
        """
        candidates = [r for r in self.regions if r.terrain_type is None]
        seed = max(candidates, key=lambda r: sum(1 for _ in r.neighbors))
        seed.terrain_type = terrain
        seed.iteration = 1
        self.regions_for_terrain[terrain].append(seed)

        return seed

    def choose_initial_regions_next_to_seed(self, seed: VoronoiRegion, terrain_type: TerrainType, weight: int):
        """
        Grow a terrain outward from its seed region.
        """
        region = seed
        for _ in range(weight - 1):
            empty_neighbors = [n for n in region.neighbors if n.terrain_type is None]
            if not empty_neighbors:
                return
            region = random.choice(empty_neighbors)
            region.terrain_type = terrain_type
            region.iteration = 1
            self.regions_for_terrain[terrain_type].append(region)

    def expand_terrain(self, terrain_type: TerrainType, weight: int):
        """
        Expand terrain from its entire frontier (all unassigned neighbors of the
        current territory) into unassigned neighbors. Frontier is updated as we grow.
        """
        # Build initial frontier: all unassigned neighbors of any region of this terrain
        frontier: Set[VoronoiRegion] = set()
        for r in self.regions_for_terrain[terrain_type]:
            for n in r.neighbors:
                if n.terrain_type is None:
                    frontier.add(n)

        for _ in range(weight):
            if not frontier:
                return

            # Pick one frontier cell to claim
            new_region = random.choice(tuple(frontier))
            frontier.remove(new_region)

            new_region.terrain_type = terrain_type
            new_region.iteration = 1 + max(
                (nbr.iteration for nbr in new_region.neighbors if nbr.terrain_type == terrain_type),
                default=0
            )
            self.regions_for_terrain[terrain_type].append(new_region)

            # Update frontier with new_region's unassigned neighbors
            for n in new_region.neighbors:
                if n.terrain_type is None:
                    frontier.add(n)
            
    def assign_unassigned_regions(self):
        """
        Assign leftover regions based on neighbor majority or terrain weights.
        """
        unassigned = [r for r in self.regions if r.terrain_type is None]
        unassigned.sort(
            key=lambda r: sum(1 for n in r.neighbors if n.terrain_type),
            reverse=True
        )
        for region in unassigned:
            neighbors = [n for n in region.neighbors if n.terrain_type]
            if neighbors:
                # pick neighbor with highest terrain weight
                best_neighbor = max(neighbors, key=lambda n: self.terrain_weights[n.terrain_type])
                region.terrain_type = best_neighbor.terrain_type
            else:
                # fallback: assign terrain with the highest weight
                region.terrain_type = max(self.terrain_weights, key=self.terrain_weights.get)

    def generate_map(self) -> List[List[TerrainType]]:
        """
        Generate a Voronoi map with specified dimensions and number of regions.
        Useful info: http://pcg.wikidot.com/pcg-algorithm:voronoi-diagram
        """
        num_of_regions = sum(weight * self.alpha for weight in self.terrain_weights.values())
        self.generate_voronoi_regions(n=num_of_regions)

        sorted_terrains = sorted(self.terrain_weights.items(), key=lambda kv: kv[1])
        self.regions_for_terrain = {terrain: [] for terrain, _ in sorted_terrains} # list for storing current regions assigned to each terrain

        # phase 1: pick initial seed regions for each terrain type
        seeds = {terrain: self.pick_seed(terrain) for terrain in self.terrain_weights}

        # phase 2: expand from the seeds, assigning terrain types to neighboring regions
        for i in range(self.alpha):
            # repeat alpha iterations for each terrain type
            for terrain, weight in sorted_terrains:
                if i == 0:
                    self.choose_initial_regions_next_to_seed(seed=seeds[terrain], terrain_type=terrain, weight=weight)
                else:
                    self.expand_terrain(terrain_type=terrain, weight=weight)
            print(f"After iteration {i + 1}:")
            for terrain, regs in self.regions_for_terrain.items():
                    print(f"{terrain.name}: {len(regs)} regions")

        # phase 3: fill the remaining unassigned regions
        self.assign_unassigned_regions()

        # phase 4: build final map
        voronoi_map = [[None for _ in range(self.width)] for _ in range(self.height)]
        for region in self.regions:
            for x, y in region.tiles:
                voronoi_map[y][x] = region.terrain_type

        return voronoi_map
