import math
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from generation.pcg_algorithms.voronoi import VoronoiRegion

@dataclass
class FieldInfo:
    """Information about a Voronoi field (region)."""
    field_id: int  # Field ID
    centroid: Tuple[float, float]  # Field center (x, y)
    boundary: List[Tuple[float, float]]  # Field edges as list of float points
    boundary_raster: List[Tuple[int, int]]  # Edges as discrete grid points
    area: int  # Number of tiles in field
    seed_position: Tuple[int, int]  # Seed position
    assigned_to_city: Optional[int] = None  # City ID if field is assigned

@dataclass
class VoronoiEdge:
    """Edge between two Voronoi regions."""
    region1_seed: Tuple[int, int]  # (x, y) of first region's seed
    region2_seed: Tuple[int, int]  # (x, y) of second region's seed
    boundary_points: List[Tuple[float, float]]  # List of (x, y) points on the boundary (tile centers)
    length: float  # Length of the edge


@dataclass
class CityWithVoronoi:
    """City with its Voronoi region and safety properties."""
    x: float
    y: float
    is_player_city: bool
    player_id: Optional[int]
    voronoi_region: VoronoiRegion
    safety_radius: int
    region_area: int
    region_boundary: Optional[List[Tuple[float, float]]] = None


@dataclass
class VoronoiResult:
    """Complete result of Voronoi city placement including edges."""
    cities: List[CityWithVoronoi]
    edges: List[VoronoiEdge]
    min_distance_achieved: float

class VoronoiCityPlacer:
    """
    City placement using Voronoi diagrams.
    
    Key advantages:
    - Natural separation of city territories
    - Adaptive safety radii based on region size
    - No overlapping territories by design
    """
    
    def __init__(self, map_size: int):
        self.map_width = map_size
        self.map_height = map_size
    
    def generate_seeds_with_minimum_distance(self, 
                                           num_cities: int, 
                                           min_distance: int,
                                           reserved_tiles: set[tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Generate city seeds using Poisson disk sampling for minimum distance.
        Enhanced version with better distance guarantees.
        
        Cities are placed to maximize distance between them.
        """
        seeds = []
        max_attempts = num_cities * 100  # More attempts for better results
        attempts = 0
        
        # Small margin from edges to avoid placement exactly on border
        edge_margin = 3  # Just enough to avoid edge artifacts
        
        # # print(f"Generating {num_cities} cities with min distance {min_distance}...")
        
        while len(seeds) < num_cities and attempts < max_attempts:
            # For each new seed, try to place it as far as possible from existing seeds
            best_candidate = None
            best_min_distance = -1
            
            # Try multiple candidate positions
            for _ in range(20):  # Number of candidates to try
                x = random.randint(edge_margin, self.map_width - edge_margin)
                y = random.randint(edge_margin, self.map_height - edge_margin)
                
                # Calculate minimum distance to existing seeds
                min_distance_to_seeds = float('inf')
                for sx, sy in seeds:
                    distance = math.sqrt((x - sx)**2 + (y - sy)**2)
                    min_distance_to_seeds = min(min_distance_to_seeds, distance)
                
                # If this is a valid position and better than our current best and not a reserved tile
                if min_distance_to_seeds >= min_distance and min_distance_to_seeds > best_min_distance and (x, y) not in reserved_tiles:
                    best_candidate = (x, y)
                    best_min_distance = min_distance_to_seeds
            
            if best_candidate is not None:
                seeds.append(best_candidate)
            
            attempts += 1
        
        return seeds

    def _calculate_region_centroid(self, region: VoronoiRegion) -> Tuple[float, float]:
        """
        Calculate the centroid (center of mass) of a region based on its tiles.

        Args:
            region: Voronoi region

        Returns:
            Tuple[float, float]: Centroid coordinates (x, y) as tile centers
        """
        if not region.tiles:
            return (float(region.seed_x) + 0.5, float(region.seed_y) + 0.5)

        # Calculate average position of all tiles (as tile centers)
        sum_x = sum(x + 0.5 for x, y in region.tiles)
        sum_y = sum(y + 0.5 for x, y in region.tiles)

        centroid_x = sum_x / len(region.tiles)
        centroid_y = sum_y / len(region.tiles)

        return (centroid_x, centroid_y)

    def _rasterize_boundary_edges(self, boundary_points: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
        """
        Rasterize field edges to discrete grid points.
        For each edge segment, calculate all tiles it passes through.

        Args:
            boundary_points: List of edge points as (x, y) float

        Returns:
            List of unique grid points (x, y) int through which edges pass
        """
        if len(boundary_points) < 2:
            return []

        raster_points = set()

        # For each edge segment
        for i in range(len(boundary_points)):
            start = boundary_points[i]
            end = boundary_points[(i + 1) % len(boundary_points)]  # Close polygon

            # Rasterize line from start to end using Bresenham's algorithm
            line_points = self._bresenham_line(start[0], start[1], end[0], end[1])
            raster_points.update(line_points)

        return list(raster_points)

    def _bresenham_line(self, x0: float, y0: float, x1: float, y1: float) -> List[Tuple[int, int]]:
        """
        Bresenham's algorithm for line rasterization.
        Returns all grid points through which the line passes.

        Args:
            x0, y0: Starting point (float)
            x1, y1: Ending point (float)

        Returns:
            List of grid points (x, y) int
        """
        points = []

        # Convert float to int (floor)
        ix0, iy0 = int(x0), int(y0)
        ix1, iy1 = int(x1), int(y1)

        # Check map bounds
        ix0 = max(0, min(self.map_width - 1, ix0))
        iy0 = max(0, min(self.map_height - 1, iy0))
        ix1 = max(0, min(self.map_width - 1, ix1))
        iy1 = max(0, min(self.map_height - 1, iy1))

        dx = abs(ix1 - ix0)
        dy = abs(iy1 - iy0)

        x, y = ix0, iy0

        sx = 1 if ix0 < ix1 else -1
        sy = 1 if iy0 < iy1 else -1

        if dx > dy:
            err = dx / 2.0
            while x != ix1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != iy1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        points.append((x, y))  # Add last point

        return points

    def are_regions_adjacent(self, region1: 'VoronoiRegion', region2: 'VoronoiRegion') -> bool:
        """
        Check if two Voronoi regions are adjacent (share a common border).

        Args:
            region1, region2: Regions to check

        Returns:
            bool: True if regions are adjacent
        """
        if not region1.tiles or not region2.tiles:
            return False

        # Convert tiles to set for faster lookup
        tiles1 = set(region1.tiles)
        tiles2 = set(region2.tiles)

        # Check if any tile from region1 has a neighbor in region2
        for x, y in tiles1:
            # Check 4 neighbors (up, down, left, right)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_x, neighbor_y = x + dx, y + dy
                if (neighbor_x, neighbor_y) in tiles2:
                    return True

        return False

    def find_adjacent_regions(self, target_region: 'VoronoiRegion', all_regions: List['VoronoiRegion'],
                              exclude_regions: set) -> List['VoronoiRegion']:
        """
        Find all regions adjacent to a given region.

        Args:
            target_region: Region for which we search for neighbors
            all_regions: List of all regions
            exclude_regions: Set of region IDs to skip

        Returns:
            List of adjacent regions
        """
        adjacent = []
        for region in all_regions:
            if (region.region_id not in exclude_regions and
                    region.region_id != target_region.region_id and
                    self.are_regions_adjacent(target_region, region)):
                adjacent.append(region)
        return adjacent

    def _get_seed_connected_component(self, region: VoronoiRegion) -> set:
        """
        Return the set of tiles that form the 4-connected component of `region.tiles`
        which contains the region seed (region.seed_x, region.seed_y).

        If seed is not in region.tiles, fallback to returning the full set of tiles.
        """
        tiles = set(region.tiles)
        seed = (region.seed_x, region.seed_y)

        if seed not in tiles:
            # seed not directly inside tiles (possible after relaxations) - try nearest tile
            # find tile with minimal distance to seed
            if not tiles:
                return set()
            best = min(tiles, key=lambda t: (t[0] - region.seed_x)**2 + (t[1] - region.seed_y)**2)
            seed = best

        # BFS/stack to gather 4-connected component
        comp = set()
        stack = [seed]
        while stack:
            tx, ty = stack.pop()
            if (tx, ty) in comp:
                continue
            if (tx, ty) not in tiles:
                continue
            comp.add((tx, ty))
            # push 4-neighbors
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = tx + dx, ty + dy
                if (nx, ny) in tiles and (nx, ny) not in comp:
                    stack.append((nx, ny))

        return comp

    def _region_boundary_polygon(self, region: VoronoiRegion) -> List[Tuple[float, float]]:
        """
        Compute an ordered polygon (list of tile-center points) that approximates
        the boundary of the given region.

        Returns points as tile centers (x+0.5, y+0.5) ordered by angle around
        the region centroid.
        """
        if not region.tiles:
            return []

        # Work on the connected component containing the region seed (exclude disconnected islands)
        comp = self._get_seed_connected_component(region)
        if not comp:
            return []

        tiles_set = comp
        boundary_tiles = []

        # Find tiles that are on the boundary (have a neighbor not in the component)
        for x, y in comp:
            # Skip absolute map edge tiles
            if x == 0 or y == 0 or x == self.map_width - 1 or y == self.map_height - 1:
                continue

            is_boundary = False
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                # If neighbor is outside bounds or not in the same component -> boundary
                if not (0 <= nx < self.map_width and 0 <= ny < self.map_height):
                    is_boundary = True
                    break
                if (nx, ny) not in tiles_set:
                    is_boundary = True
                    break
            if is_boundary:
                boundary_tiles.append((x, y))

        if not boundary_tiles:
            return []

        # Compute centroid (use tile centers)
        cx = sum(x + 0.5 for x, y in region.tiles) / len(region.tiles)
        cy = sum(y + 0.5 for x, y in region.tiles) / len(region.tiles)

        # Convert to centers and sort by angle around centroid to create a polygon
        def angle(t):
            tx, ty = t
            return math.atan2((ty + 0.5) - cy, (tx + 0.5) - cx)

        boundary_centers = [(x + 0.5, y + 0.5) for x, y in boundary_tiles]
        # sort boundary tiles by their angle around centroid
        boundary_centers.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

        return boundary_centers
    
    def select_regions_max_min_dist(self, all_regions: List[VoronoiRegion], n: int) -> List[VoronoiRegion]:
        """Returns list of n regions with maximum minimum distance between seed points."""
        if n >= len(all_regions):
            return all_regions.copy()

        regions = sorted(all_regions, key=lambda r: (r.seed_x, r.seed_y))

        # Determine maximum possible distance
        max_possible = max(
            self.distance(a, b)
            for i, a in enumerate(regions)
            for b in regions[i + 1 :]
        )

        low, high = 0.0, max_possible
        best_dist = 0.0
        best_selection: List[VoronoiRegion] = []

        # Binary search by distance
        while high - low > 1e-3:
            mid = (low + high) / 2
            selection = self.can_select_with_distance(regions, n, mid)
            if selection:
                best_dist = mid
                best_selection = selection
                low = mid
            else:
                high = mid

        return best_selection
    
    def distance(self, a: VoronoiRegion, b: VoronoiRegion) -> float:
        """Euclidean distance between region seed points."""
        return math.hypot(a.seed_x - b.seed_x, a.seed_y - b.seed_y)
    
    def can_select_with_distance(self, regions: List[VoronoiRegion], n: int, min_dist: float) -> List[VoronoiRegion] | None:
        """Tries to select n regions with minimum distance min_dist.
        If successful - returns selected regions, if not - None."""
        selected = [regions[0]]
        for region in regions[1:]:
            if all(self.distance(region, s) >= min_dist for s in selected):
                selected.append(region)
                if len(selected) == n:
                    return selected
        return None
    
    def generate_step_1(self, min_distance, reserved_tiles, total_regions):
        # Generate positions for all regions (not just cities)
        # Reduce required distance between regions to fit more
        region_min_distance = max(5, min_distance // 4)  # Much smaller distance for regions
        all_region_seeds = self.generate_seeds_with_minimum_distance(total_regions, region_min_distance, reserved_tiles)
        
        if len(all_region_seeds) < total_regions:
            # print(f"Warning: Could only generate {len(all_region_seeds)}/{total_regions} regions")
            total_regions = len(all_region_seeds)
        
        # Generate Voronoi regions for all positions
        all_regions = []
        
        for i, (x, y) in enumerate(all_region_seeds):
            region = VoronoiRegion(x, y)
            region.region_id = i + 1  # Number regions from 1
            all_regions.append(region)
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                closest_region = min(all_regions, key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
                if (x, y) not in reserved_tiles:
                    closest_region.tiles.append((x, y))

        return all_regions, region_min_distance, total_regions
    
    def generate_step_2(self, player_cities, neutral_cities, all_regions):
        total_cities = player_cities + neutral_cities
        if total_cities > len(all_regions):
            raise Exception(f"Too few regions ({len(all_regions)}) for number of cities ({total_cities})")
        
        # Select city positions maximizing mutual distances
        selected = self.select_regions_max_min_dist(all_regions, n=total_cities)
        city_regions = selected[:total_cities]

        return total_cities, selected, city_regions
