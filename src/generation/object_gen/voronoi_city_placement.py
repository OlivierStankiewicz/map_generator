"""
City placement using Voronoi diagrams with safety rings.
Uses existing Voronoi implementation to create natural city distribution.
"""

import math
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import sys
import os

# Import the existing Voronoi implementation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pcg_algorithms')))
from voronoi import VoronoiRegion

@dataclass
class FieldInfo:
    """Informacje o polu (regionie) Voronoi."""
    field_id: int  # ID pola
    centroid: Tuple[float, float]  # Centrum pola (x, y)
    boundary: List[Tuple[float, float]]  # Krawedzie pola jako lista punktow float
    boundary_raster: List[Tuple[int, int]]  # Krawedzie jako dyskretne punkty grid'a
    area: int  # Liczba tiles w polu
    seed_position: Tuple[int, int]  # Pozycja seed'a
    assigned_to_city: Optional[int] = None  # ID miasta jesli pole jest przypisane

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
    
    def __init__(self, map_width: int, map_height: int):
        self.map_width = map_width
        self.map_height = map_height
    
    def calculate_max_cities_for_distance(self, min_distance: int) -> int:
        """
        Calculate maximum number of cities that can fit with given minimum distance.
        
        Args:
            min_distance: Minimum required distance between cities
            
        Returns:
            int: Maximum number of cities that can reasonably fit
        """
        # Area needed per city (circular packing approximation)
        area_per_city = math.pi * (min_distance / 2) ** 2
        
        # Add some padding factor for realistic placement
        padding_factor = 1.5  # 50% extra space for realistic placement
        effective_area_per_city = area_per_city * padding_factor
        
        map_area = self.map_width * self.map_height
        max_cities = int(map_area / effective_area_per_city)
        
        # Conservative estimate - reduce by 20% for edge effects
        return max(1, int(max_cities * 0.8))
    
    def validate_city_count(self, total_cities: int, min_distance: int = 20) -> Tuple[bool, str, int]:
        """
        Validate if requested number of cities can fit with minimum distance.
        
        Returns:
            Tuple[bool, str, int]: (is_valid, message, max_recommended)
        """
        max_cities = self.calculate_max_cities_for_distance(min_distance)
        
        if total_cities <= max_cities:
            return True, f"Cities should fit (max {max_cities} for distance {min_distance})", max_cities
        else:
            return False, f"Too many cities! Max {max_cities} for distance {min_distance}, requested {total_cities}", max_cities 
    
    def generate_seeds_with_minimum_distance(self, 
                                           num_cities: int, 
                                           min_distance: int) -> List[Tuple[int, int]]:
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
        
        # print(f"Generating {num_cities} cities with min distance {min_distance}...")
        
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
                
                # If this is a valid position and better than our current best
                if min_distance_to_seeds >= min_distance and min_distance_to_seeds > best_min_distance:
                    best_candidate = (x, y)
                    best_min_distance = min_distance_to_seeds
            
            if best_candidate is not None:
                seeds.append(best_candidate)
            
            attempts += 1
        
        return seeds
    
    def calculate_voronoi_edges(self, regions: List[VoronoiRegion]) -> List[VoronoiEdge]:
        """
        Calculate edges between adjacent Voronoi regions.
        
        Args:
            regions: List of Voronoi regions with neighbor information
            
        Returns:
            List[VoronoiEdge]: Edges between neighboring regions
        """
        edges = []
        processed_pairs = set()
        
        # Create region lookup by seed position
        region_by_seed = {(r.seed_x, r.seed_y): r for r in regions}
        
        for region in regions:
            region_seed = (region.seed_x, region.seed_y)
            
            for neighbor in region.neighbors:
                neighbor_seed = (neighbor.seed_x, neighbor.seed_y)
                
                # Create pair identifier (sorted to avoid duplicates)
                pair = tuple(sorted([region_seed, neighbor_seed]))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)
                
                # Find boundary points between these regions (tile coords)
                raw_boundary = self._find_boundary_points(region, neighbor)

                if raw_boundary:
                    # Convert tile coordinates to centers (float) for output
                    boundary_points = [(bx + 0.5, by + 0.5) for bx, by in raw_boundary]

                    # Calculate edge length based on raw tile points
                    edge_length = self._calculate_edge_length(raw_boundary)

                    edge = VoronoiEdge(
                        region1_seed=region_seed,
                        region2_seed=neighbor_seed,
                        boundary_points=boundary_points,
                        length=edge_length
                    )
                    edges.append(edge)
        
        return edges
    
    def _find_boundary_points(self, region1: VoronoiRegion, region2: VoronoiRegion) -> List[Tuple[int, int]]:
        """
        Find points on the boundary between two regions.
        
        Args:
            region1, region2: Two neighboring Voronoi regions
            
        Returns:
            List[Tuple[int, int]]: Boundary points
        """
        boundary_points = []

        # Work only on the connected component that contains the region seed
        comp1 = self._get_seed_connected_component(region1)
        comp2 = self._get_seed_connected_component(region2)

        # Check all tiles of region1's seed-component for adjacency to region2's seed-component
        for x, y in comp1:
            # Skip tiles on the absolute map border - we don't want outlines there
            if x == 0 or y == 0 or x == self.map_width - 1 or y == self.map_height - 1:
                continue

            # Check 4-connected neighbors
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in comp2:
                    # This point is on the boundary between the two seed-components
                    boundary_points.append((x, y))
                    break  # No need to check other neighbors for this tile

        return boundary_points

    def _calculate_edge_length(self, boundary_points: List[Tuple[int, int]]) -> float:
        """
        Calculate approximate length of an edge from its boundary points.

        Args:
            boundary_points: List of points on the boundary

        Returns:
            float: Approximate edge length
        """
        if len(boundary_points) <= 1:
            return 0.0

        # Simple approach: return number of boundary points as length
        # More sophisticated: could trace the actual boundary path
        return float(len(boundary_points))

    def _region_boundary_polygon(self, region: VoronoiRegion) -> List[Tuple[float, float]]:
        """
        Compute an ordered polygon (list of tile-center points) that approximates
        the boundary of the given region.

        Returns points as tile centers (x+0.5, y+0.5) ordered by angle around
        the region centroid.
        """
        if not region.tiles:
            return []

        tiles_set = set(region.tiles)
        boundary_tiles = []

        # Find tiles that are on the boundary (have a neighbor not in the region)
        for x, y in region.tiles:
            is_boundary = False
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
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

    def _calculate_region_centroid(self, region: VoronoiRegion) -> Tuple[float, float]:
        """
        Oblicza centroid (srodek masy) regionu na podstawie jego tiles.

        Args:
            region: Region Voronoi

        Returns:
            Tuple[float, float]: Wspolrzedne centroidu (x, y) jako tile centers
        """
        if not region.tiles:
            return (float(region.seed_x) + 0.5, float(region.seed_y) + 0.5)

        # Oblicz srednia pozycje wszystkich tiles (jako tile centers)
        sum_x = sum(x + 0.5 for x, y in region.tiles)
        sum_y = sum(y + 0.5 for x, y in region.tiles)

        centroid_x = sum_x / len(region.tiles)
        centroid_y = sum_y / len(region.tiles)

        return (centroid_x, centroid_y)

    def _rasterize_boundary_edges(self, boundary_points: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
        """
        Rasteryzuje krawedzie pola na dyskretne punkty grid'a.
        Dla kazdego segmentu krawedzi, oblicza wszystkie tiles przez ktore przechodzi.

        Args:
            boundary_points: Lista punktow krawedzi jako (x, y) float

        Returns:
            Lista unikalnych punktow grid'a (x, y) int przez ktore przechodza krawedzie
        """
        if len(boundary_points) < 2:
            return []

        raster_points = set()

        # Dla kazdego segmentu krawedzi
        for i in range(len(boundary_points)):
            start = boundary_points[i]
            end = boundary_points[(i + 1) % len(boundary_points)]  # Zamykamy polygon

            # Rasteryzuj linie od start do end uzywajac algorytmu Bresenhama
            line_points = self._bresenham_line(start[0], start[1], end[0], end[1])
            raster_points.update(line_points)

        return list(raster_points)

    def _bresenham_line(self, x0: float, y0: float, x1: float, y1: float) -> List[Tuple[int, int]]:
        """
        Algorytm Bresenhama do rasteryzacji linii.
        Zwraca wszystkie punkty grid'a przez ktore przechodzi linia.

        Args:
            x0, y0: Punkt poczatkowy (float)
            x1, y1: Punkt koncowy (float)

        Returns:
            Lista punktow grid'a (x, y) int
        """
        points = []

        # Konwertuj float na int (floor)
        ix0, iy0 = int(x0), int(y0)
        ix1, iy1 = int(x1), int(y1)

        # Sprawdz granice mapy
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

        points.append((x, y))  # Dodaj ostatni punkt

        return points

    def are_regions_adjacent(self, region1: 'VoronoiRegion', region2: 'VoronoiRegion') -> bool:
        """
        Sprawdza czy dwa regiony Voronoi sa sasiednie (maja wspolna granice).

        Args:
            region1, region2: Regiony do sprawdzenia

        Returns:
            bool: True jesli regiony sa sasiednie
        """
        if not region1.tiles or not region2.tiles:
            return False

        # Konwertuj tiles na set dla szybszego wyszukiwania
        tiles1 = set(region1.tiles)
        tiles2 = set(region2.tiles)

        # Sprawdz czy ktorykolwiek tile z region1 ma sasiada w region2
        for x, y in tiles1:
            # Sprawdz 4 sasiadow (g�ra, d�, lewo, prawo)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_x, neighbor_y = x + dx, y + dy
                if (neighbor_x, neighbor_y) in tiles2:
                    return True

        return False

    def find_adjacent_regions(self, target_region: 'VoronoiRegion', all_regions: List['VoronoiRegion'],
                              exclude_regions: set) -> List['VoronoiRegion']:
        """
        Znajdz wszystkie regiony sasiednie do podanego regionu.

        Args:
            target_region: Region dla ktorego szukamy sasiadow
            all_regions: Lista wszystkich regionow
            exclude_regions: Set ID regionow do pominiecia

        Returns:
            Lista sasiadujacych regionow
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
    
    def _calculate_edge_length(self, boundary_points: List[Tuple[int, int]]) -> float:
        """
        Calculate approximate length of an edge from its boundary points.
        
        Args:
            boundary_points: List of points on the boundary
            
        Returns:
            float: Approximate edge length
        """
        if len(boundary_points) <= 1:
            return 0.0
        
        # Simple approach: return number of boundary points as length
        # More sophisticated: could trace the actual boundary path
        return float(len(boundary_points))

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
    
    def generate_edge_preferred_position(self, edge_margin: int) -> Tuple[int, int]:
        """
        Generate position with preference for being near map edges.
        
        Args:
            edge_margin: Minimum distance from map edge
            
        Returns:
            Tuple[int, int]: (x, y) coordinates
        """
        # 40% chance to be near an edge, 60% chance anywhere
        if random.random() < 0.4:
            # Choose which edge to be near
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            
            if edge == 'top':
                x = random.randint(edge_margin, self.map_width - edge_margin)
                y = random.randint(edge_margin, min(30, self.map_height // 4))
            elif edge == 'bottom':
                x = random.randint(edge_margin, self.map_width - edge_margin)
                y = random.randint(max(self.map_height - 30, 3 * self.map_height // 4), 
                                  self.map_height - edge_margin)
            elif edge == 'left':
                x = random.randint(edge_margin, min(30, self.map_width // 4))
                y = random.randint(edge_margin, self.map_height - edge_margin)
            else:  # right
                x = random.randint(max(self.map_width - 30, 3 * self.map_width // 4), 
                                  self.map_width - edge_margin)
                y = random.randint(edge_margin, self.map_height - edge_margin)
        else:
            # Random position anywhere on map
            x = random.randint(edge_margin, self.map_width - edge_margin)
            y = random.randint(edge_margin, self.map_height - edge_margin)
            
        return x, y
    
    def calculate_region_properties(self, region: VoronoiRegion) -> Tuple[int, int]:
        """
        Calculate safety radius and area for a Voronoi region.
        
        Returns:
            Tuple[int, int]: (safety_radius, region_area)
        """
        region_area = len(region.tiles)
        
        # Find minimum distance to region border
        min_distance_to_border = float('inf')
        
        for tile_x, tile_y in region.tiles:
            # Check distance to map edges
            edge_distances = [
                tile_x,  # distance to left edge
                tile_y,  # distance to top edge
                self.map_width - 1 - tile_x,  # distance to right edge
                self.map_height - 1 - tile_y   # distance to bottom edge
            ]
            min_distance_to_border = min(min_distance_to_border, min(edge_distances))
            
            # Check distance to neighboring regions
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    check_x, check_y = tile_x + dx, tile_y + dy
                    if (0 <= check_x < self.map_width and 
                        0 <= check_y < self.map_height):
                        
                        # If this neighboring tile belongs to a different region,
                        # we're at the border
                        neighbor_region = None
                        for other_region in region.neighbors:
                            if (check_x, check_y) in other_region.tiles:
                                neighbor_region = other_region
                                break
                        
                        if neighbor_region:
                            # Distance from region center to this border point
                            center_to_border = math.sqrt(
                                (tile_x - region.seed_x)**2 + 
                                (tile_y - region.seed_y)**2
                            )
                            min_distance_to_border = min(min_distance_to_border, center_to_border)
        
        # Safety radius is a percentage of the minimum distance to border
        # Larger regions get relatively smaller safety margins
        area_factor = min(1.0, region_area / 100)  # Normalize by typical region size
        safety_radius = max(2, int(min_distance_to_border * 0.6 * area_factor))
        
        return safety_radius, region_area
    
    def lloyd_relaxation(self, regions: List[VoronoiRegion], iterations: int = 3) -> List[VoronoiRegion]:
        """
        Apply Lloyd's relaxation to improve region distribution.
        
        Moves each seed to the centroid of its region for more uniform shapes.
        """
        for iteration in range(iterations):
            # Calculate centroids and move seeds
            for region in regions:
                if region.tiles:
                    # Calculate centroid
                    sum_x = sum(x for x, y in region.tiles)
                    sum_y = sum(y for x, y in region.tiles)
                    centroid_x = sum_x / len(region.tiles)
                    centroid_y = sum_y / len(region.tiles)
                    
                    # Move seed towards centroid (but not all the way for stability)
                    move_factor = 0.7
                    new_x = int(region.seed_x + (centroid_x - region.seed_x) * move_factor)
                    new_y = int(region.seed_y + (centroid_y - region.seed_y) * move_factor)
                    
                    # Keep within bounds
                    region.seed_x = max(5, min(self.map_width - 5, new_x))
                    region.seed_y = max(5, min(self.map_height - 5, new_y))
            
            # Recalculate Voronoi diagram with new seed positions
            if iteration < iterations - 1:  # Don't recalculate on last iteration
                regions = self._recalculate_voronoi(regions)
        
        return regions
    
    def _create_voronoi_region(self, x: int, y: int, region_id: int = None) -> VoronoiRegion:
        """Create a new Voronoi region with the given seed position."""
        region = VoronoiRegion(x, y)
        if region_id is not None:
            region.region_id = region_id
        return region
    
    def _generate_regions_around_cities(self, city_positions: List[Tuple[int, int]], total_regions: int) -> List[VoronoiRegion]:
        """
        Generate additional region seeds around city positions.
        These will be used to create terrain variation.
        """
        all_seeds = []
        used_positions = set()
        
        # First add the city positions
        for x, y in city_positions:
            all_seeds.append((x, y))
            used_positions.add((x, y))
        
        # Then add additional seeds around each city
        additional_seeds_per_city = max(2, (total_regions - len(city_positions)) // len(city_positions))
        
        for city_x, city_y in city_positions:
            seeds_added = 0
            max_radius = 15  # Maximum radius to search for positions
            current_radius = 5  # Start with a smaller radius
            
            while seeds_added < additional_seeds_per_city and current_radius <= max_radius:
                # Try positions at current radius
                for attempt in range(8):  # Try 8 different angles
                    angle = 2 * math.pi * (attempt / 8)
                    dx = int(current_radius * math.cos(angle))
                    dy = int(current_radius * math.sin(angle))
                    
                    x = city_x + dx
                    y = city_y + dy
                    
                    # Ensure position is within map bounds and not already used
                    if (0 <= x < self.map_width and 0 <= y < self.map_height and 
                        (x, y) not in used_positions):
                        
                        # Check minimum distance to existing seeds
                        min_distance = min(math.sqrt((x - sx)**2 + (y - sy)**2) 
                                        for sx, sy in all_seeds)
                        
                        if min_distance >= 5:  # Minimum distance between region seeds
                            all_seeds.append((x, y))
                            used_positions.add((x, y))
                            seeds_added += 1
                            
                            if seeds_added >= additional_seeds_per_city:
                                break
                
                current_radius += 3  # Incrementally increase radius if needed
        
        # Create Voronoi regions from seeds
        regions = []
        for i, (x, y) in enumerate(all_seeds):
            region = self._create_voronoi_region(x, y, region_id=i+1)
            regions.append(region)
        
        return regions

    def generate_city_positions_with_fields(self, 
                                          player_cities: int, 
                                          neutral_cities: int,
                                          min_distance: int = 20,
                                          total_regions: int = None) -> Dict:
        """
        Generate city positions using old distance-based placement,
        but with multiple terrain regions and adjacent region selection.
        
        Args:
            player_cities: Number of player cities
            neutral_cities: Number of neutral cities
            min_distance: Minimum distance between cities
            total_regions: Total number of regions to generate (if None, will use 3x cities)
        """
        total_cities = player_cities + neutral_cities
        
        if total_regions is None:
            total_regions = total_cities * 3  # Default to 3 regions per city
        
        # Step 1: Generate city positions using distance-based placement
        city_seeds = self.generate_seeds_with_minimum_distance(total_cities, min_distance)
        
        if len(city_seeds) < total_cities:
            raise RuntimeError(f"Could not place {total_cities} cities with minimum distance {min_distance}")
        
        # Step 2: Generate additional region seeds around cities
        all_regions = self._generate_regions_around_cities(city_seeds, total_regions)
        
        # Step 3: Assign tiles to regions
        ownership = [[None for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        for y in range(self.map_height):
            for x in range(self.map_width):
                closest_region = min(all_regions, 
                                   key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
                closest_region.tiles.append((x, y))
                ownership[y][x] = closest_region
        
        # Step 4: Create city objects and assign fields
        cities = []
        city_to_fields = {}
        used_regions = set()
        
        for i, (city_x, city_y) in enumerate(city_seeds):
            # Find the region containing this city
            city_region = min(all_regions, 
                            key=lambda r: (r.seed_x - city_x) ** 2 + (r.seed_y - city_y) ** 2)
            
            # This region becomes the main field for the city
            main_region_id = city_region.region_id
            used_regions.add(main_region_id)
            
            # Find adjacent regions for additional fields
            adjacent_regions = self.find_adjacent_regions(city_region, all_regions, used_regions)
            
            # Sort adjacent regions by distance to city
            adjacent_regions.sort(key=lambda r: 
                                (r.seed_x - city_x) ** 2 + (r.seed_y - city_y) ** 2)
            
            # Select up to 2 additional fields
            selected_fields = [main_region_id]
            for adj_region in adjacent_regions[:2]:  # Take up to 2 closest adjacent regions
                selected_fields.append(adj_region.region_id)
                used_regions.add(adj_region.region_id)
            
            # Create city object
            is_player = i < player_cities
            player_id = i if is_player else None
            
            city = CityWithVoronoi(
                x=float(city_x),
                y=float(city_y),
                is_player_city=is_player,
                player_id=player_id,
                voronoi_region=city_region,
                safety_radius=min_distance // 2,
                region_area=len(city_region.tiles)
            )
            cities.append(city)
            
            # Store field assignments
            city_to_fields[i] = selected_fields
        
        # Step 5: Create detailed field information
        fields_info = []
        for region in all_regions:
            # Calculate region properties
            centroid = self._calculate_region_centroid(region)
            boundary = self._region_boundary_polygon(region)
            boundary_raster = self._rasterize_boundary_edges(boundary)
            
            # Find if region is assigned to a city
            assigned_city = None
            for city_id, fields in city_to_fields.items():
                if region.region_id in fields:
                    assigned_city = city_id + 1  # +1 for 1-based city IDs
                    break
            
            field_info = FieldInfo(
                field_id=region.region_id,
                centroid=centroid,
                boundary=boundary,
                boundary_raster=boundary_raster,
                area=len(region.tiles),
                seed_position=(region.seed_x, region.seed_y),
                assigned_to_city=assigned_city
            )
            fields_info.append(field_info)
        
        # Calculate city boundaries
        city_boundaries = self._generate_city_area_boundaries(all_regions, city_to_fields)
        
        return {
            "cities": cities,
            "all_regions": all_regions,
            "city_to_fields": city_to_fields,
            "fields_info": fields_info,
            "city_boundaries": city_boundaries
        }
    
    def _generate_city_area_boundaries(self, all_regions: List[VoronoiRegion],
                                     city_to_fields: Dict[int, List[int]]) -> Dict[int, List[Tuple[int, int]]]:
        """Generate external boundaries for each city's total area (all fields)."""
        city_boundaries = {}
        
        for city_id, field_ids in city_to_fields.items():
            # Collect all tiles belonging to this city
            city_tiles = set()
            
            for field_id in field_ids:
                region = next((r for r in all_regions if r.region_id == field_id), None)
                if region:
                    city_tiles.update(region.tiles)
            
            # Find boundary tiles (tiles with neighbors outside city area)
            boundary_tiles = []
            
            for x, y in city_tiles:
                is_boundary = False
                
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    
                    if (nx, ny) not in city_tiles:
                        is_boundary = True
                        break
                
                if is_boundary:
                    boundary_tiles.append((x, y))
            
            city_boundaries[city_id] = boundary_tiles
        
        return city_boundaries


def quick_city_placement(map_width: int, 
                        map_height: int,
                        player_cities: int, 
                        neutral_cities: int,
                        min_distance: int = 20,
                        include_edges: bool = False) -> Tuple[VoronoiResult, bool, List[str]]:
    """
    Quick function for city placement using Voronoi with distance constraints.
    
    Args:
        map_width, map_height: Map dimensions
        player_cities: Number of player cities
        neutral_cities: Number of neutral cities
        min_distance: Minimum distance between cities (default 20)
        include_edges: Whether to calculate and include Voronoi edges
    
    Returns:
        Tuple with VoronoiResult (cities + edges), success status, and any problems
    """
    placer = VoronoiCityPlacer(map_width, map_height)
    
    try:
        result = placer.place_cities_with_voronoi(player_cities, neutral_cities, min_distance, return_edges=include_edges)
        is_valid, problems = placer.validate_placement(result.cities)
        return result, is_valid, problems
    except RuntimeError as e:
        # If placement completely failed
        empty_result = VoronoiResult(cities=[], edges=[], min_distance_achieved=0.0)
        return empty_result, False, [str(e)]


def get_city_limits_for_map(map_width: int, map_height: int, min_distance: int = 20) -> Dict:
    """
    Get recommended city limits for a map size with given minimum distance.
    
    Returns:
        Dict with recommendations and limits
    """
    placer = VoronoiCityPlacer(map_width, map_height)
    max_cities = placer.calculate_max_cities_for_distance(min_distance)
    
    # Recommended distributions
    recommendations = []
    
    # Small maps
    if max_cities >= 6:
        recommendations.append({"players": 4, "neutrals": 2, "total": 6, "description": "Small competitive"})
    if max_cities >= 8:
        recommendations.append({"players": 6, "neutrals": 2, "total": 8, "description": "Medium competitive"})
    if max_cities >= 10:
        recommendations.append({"players": 8, "neutrals": 2, "total": 10, "description": "Large competitive"})
    if max_cities >= 13:
        recommendations.append({"players": 8, "neutrals": 5, "total": 13, "description": "Standard campaign"})
    if max_cities >= 16:
        recommendations.append({"players": 10, "neutrals": 6, "total": 16, "description": "Large campaign"})
    
    return {
        "map_size": f"{map_width}x{map_height}",
        "min_distance": min_distance,
        "max_cities": max_cities,
        "recommendations": recommendations,
        "area_per_city": (map_width * map_height) / max_cities if max_cities > 0 else 0
    }


def generate_city_positions(map_format: int, player_cities: int, neutral_cities: int,
                            min_distance: int):
    """Test the new edge calculation functionality."""
    print("\n=== TESTING VORONOI EDGES ===")

    # Small test case to visualize edges
    placer = VoronoiCityPlacer(map_format, map_format)
    result = placer.place_cities_with_voronoi(player_cities, neutral_cities, min_distance, return_edges=True)

    print(f"\nPlacement results:")
    print(f"Cities: {len(result.cities)}")
    print(f"Edges: {len(result.edges)}")
    print(f"Min distance: {result.min_distance_achieved:.1f}")

    print("\nCity positions:")
    for i, city in enumerate(result.cities):
        city_type = f"Player {city.player_id}" if city.is_player_city else f"Neutral {i - sum(1 for c in result.cities[:i] if c.is_player_city) + 1}"
        # city.x and city.y may be floats (tile centers)
        print(f"  {city_type}: ({city.x:5.2f}, {city.y:5.2f}) - Region size: {city.region_area}")
        if city.region_boundary is not None:
            print(f"    Boundary points: {len(city.region_boundary)}")

    print("\nVoronoi edges:")
    for i, edge in enumerate(result.edges):
        print(f"  Edge {i + 1}: {edge.region1_seed} <-> {edge.region2_seed}")
        print(f"    Boundary length: {edge.length:.1f} points")

    return result



# 72 x 72
# 25+ distance max 9
# 8 7 6 7 6 8 7 7 7 9 7 6 7 8 7 8 8 6 8 9
#
# 20+ distance max 11
# 11 10 10 11 10 11 9 11 10 10 11 11 10 10 11 9 9 11 9 10
#
# distance to place everything (13 cities) max 16,3
# 16,0 16,3 14,6 14,1 16,1 13,9 16,1 14,9 15,0 14,0 16,1 13,6 15,6 15,8 16,1 14,8 15,0 14,0 14,1 14,6


def generate_city_area_boundaries(all_regions: List[VoronoiRegion], 
                                 city_to_fields: Dict[int, List[int]], 
                                 placer: 'VoronoiCityPlacer') -> Dict[int, List[Tuple[int, int]]]:
    """
    Generate external boundaries for entire city areas (all 3 fields together).
    
    Args:
        all_regions: List of all Voronoi regions
        city_to_fields: Mapping city_id -> list of fields
        placer: Instance of VoronoiCityPlacer with helper methods
        
    Returns:
        Dict[city_id, List[boundary_points]] - external boundaries for each city
    """
    city_boundaries = {}
    
    for city_id, fields_list in city_to_fields.items():
        # Zbierz wszystkie tiles nale��ce do tego miasta
        city_tiles = set()
        
        for field_id in fields_list:
            # Znajd� region o tym ID
            region = next((r for r in all_regions if r.region_id == field_id), None)
            if region:
                city_tiles.update(region.tiles)
        
        # Teraz znajd� zewn�trzne kraw�dzie tego obszaru
        boundary_tiles = []
        
        for tile_x, tile_y in city_tiles:
            # sprawd� czy tile jest na kraw�dzi (ma s�siada nie nale��cego do miasta)
            is_boundary = False
            
            # Sprawd� wszystkich 8 s�siad�w
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                        
                    neighbor_x, neighbor_y = tile_x + dx, tile_y + dy
                    
                    # Je�li s�siad jest poza map� lub nie nale�y do tego miasta
                    if ((neighbor_x, neighbor_y) not in city_tiles):
                        is_boundary = True
                        break
                        
                if is_boundary:
                    break
            
            if is_boundary:
                boundary_tiles.append((tile_x, tile_y))
        
        city_boundaries[city_id] = boundary_tiles
    
    return city_boundaries


def get_region_tiles(all_regions: List[VoronoiRegion], region_id: Optional[int] = None, seed: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
    """
    Zwraca listę kafelków (tiles) należących do danego regionu Voronoi.

    Można znaleźć region po `region_id` lub po pozycji ziarna `seed` (x, y).

    Args:
        all_regions: lista obiektów `VoronoiRegion` wygenerowanych wcześniej
        region_id: opcjonalne ID regionu (pole.region_id)
        seed: opcjonalny tuple (x, y) pozycji ziarna regionu

    Returns:
        Lista tupli (x, y) kafelków należących do regionu. Zwraca pustą listę, jeśli nie znaleziono regionu.
    """
    if region_id is None and seed is None:
        raise ValueError("Trzeba podać albo region_id, albo seed=(x,y)")

    for region in all_regions:
        if region_id is not None and getattr(region, 'region_id', None) == region_id:
            return list(region.tiles) if getattr(region, 'tiles', None) else []

        if seed is not None and (getattr(region, 'seed_x', None), getattr(region, 'seed_y', None)) == seed:
            return list(region.tiles) if getattr(region, 'tiles', None) else []

    return []


def distance(a: VoronoiRegion, b: VoronoiRegion) -> float:
    """Odległość euklidesowa między punktami nasiennymi regionów."""
    return math.hypot(a.seed_x - b.seed_x, a.seed_y - b.seed_y)


def can_select_with_distance(regions: List[VoronoiRegion], n: int, min_dist: float) -> List[VoronoiRegion] | None:
    """Próbuje wybrać n regionów z minimalnym odstępem min_dist.
       Jeśli się uda – zwraca wybrane regiony, jeśli nie – None."""
    selected = [regions[0]]
    for region in regions[1:]:
        if all(distance(region, s) >= min_dist for s in selected):
            selected.append(region)
            if len(selected) == n:
                return selected
    return None


def select_regions_max_min_dist(all_regions: List[VoronoiRegion], n: int) -> List[VoronoiRegion]:
    """Zwraca listę n regionów o maksymalnej minimalnej odległości między punktami nasiennymi."""
    if n >= len(all_regions):
        return all_regions.copy()

    regions = sorted(all_regions, key=lambda r: (r.seed_x, r.seed_y))

    # Ustalenie maksymalnego możliwego dystansu
    max_possible = max(
        distance(a, b)
        for i, a in enumerate(regions)
        for b in regions[i + 1 :]
    )

    low, high = 0.0, max_possible
    best_dist = 0.0
    best_selection: List[VoronoiRegion] = []

    # Binary search po odległości
    while high - low > 1e-3:
        mid = (low + high) / 2
        selection = can_select_with_distance(regions, n, mid)
        if selection:
            best_dist = mid
            best_selection = selection
            low = mid
        else:
            high = mid

    return best_selection


def generate_city_positions_with_fields(map_format: int, player_cities: int, neutral_cities: int,
                                       min_distance: int, total_regions: int):
    """
    Generate city positions and all Voronoi regions, where each city has 3 fields.
    
    Args:
        map_format: Map size
        player_cities: Number of player cities  
        neutral_cities: Number of neutral cities
        min_distance: Minimum distance between cities
        total_regions: Total number of regions to generate
        
    Returns:
        dict: Contains 'cities', 'all_regions', 'city_to_fields'
    """
    print(f"\n=== GENEROWANIE {total_regions} REGIONOW DLA {player_cities + neutral_cities} MIAST ===")
    
    # Krok 1: Wygeneruj wszystkie regiony Voronoi
    print(f"Tworzenie VoronoiCityPlacer z rozmiarem mapy: {map_format}x{map_format}")
    placer = VoronoiCityPlacer(map_format, map_format)
    
    # Wygeneruj pozycje dla wszystkich region�w (nie tylko miast)
    # Zmniejszamy wymagan� odleg�o�� mi�dzy regionami, �eby zmie�ci� wi�cej
    region_min_distance = max(5, min_distance // 4)  # Znacznie mniejsza odleg�o�� dla region�w
    all_region_seeds = placer.generate_seeds_with_minimum_distance(total_regions, region_min_distance)
    
    if len(all_region_seeds) < total_regions:
        print(f"Uwaga: Udalo sie wygenerowac tylko {len(all_region_seeds)}/{total_regions} regionow")
        total_regions = len(all_region_seeds)
    
    # Wygeneruj regiony Voronoi dla wszystkich pozycjigenerate_voronoi_regions
    all_regions = []
    
    for i, (x, y) in enumerate(all_region_seeds):
        region = VoronoiRegion(x, y)
        region.region_id = i + 1  # Numeruj regiony od 1
        all_regions.append(region)
    
    # Przypisz tiles do region�w
    ownership = [[None for _ in range(map_format)] for _ in range(map_format)]
    
    for y in range(map_format):
        for x in range(map_format):
            closest_region = min(all_regions, key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
            closest_region.tiles.append((x, y))
            ownership[y][x] = closest_region
    
    # Krok 2: Wybierz pozycje miast z wygenerowanych region�w
    total_cities = player_cities + neutral_cities
    
    if total_cities > len(all_regions):
        raise Exception(f"Zbyt malo regionow ({len(all_regions)}) dla liczby miast ({total_cities})")
    
    # Wybieramy pozycje miast maksymalizujac wzajemne odleglosci
    selected = select_regions_max_min_dist(all_regions, n=player_cities + neutral_cities)
    print("Wybrane punkty:")
    for r in selected:
        print(r.seed_x, r.seed_y)

    city_regions = [region for region in selected[:total_cities]]

    # Krok 3: Przypisz kazdemu miastu 3 pola (regiony) - musza tworzyc spojny komponent sasiadujacych regionow
    # Jesli dla jakiegokolwiek miasta nie da sie znalezc 3 przylegajacych do siebie pol, powtorz caly proces generacji
    max_regen_attempts = 6
    city_to_fields = None

    for regen in range(max_regen_attempts):
        # Zresetuj przypisania
        used_regions = set()
        candidate_city_to_fields: Dict[int, List[int]] = {}
        failure = False

        # Dla kazdego miasta probujemy znalezc spojny komponent o wielkosci >= 3
        for i, city_region in enumerate(city_regions):
            # Lista kandydatow dla regionu glownym: najpierw preferowane, potem inne regiony posortowane po odleglosci
            candidates = [city_region] + [r for r in sorted(all_regions, key=lambda r: distance(r, city_region)) if r.region_id not in used_regions and r.region_id != city_region.region_id]

            found = False
            for cand in candidates:
                if cand.region_id in used_regions:
                    continue

                # BFS po grafie sasiadujacych regionow (pomijamy juz uzyte regiony)
                comp_ids = set()
                stack = [cand]
                while stack:
                    r = stack.pop()
                    if r.region_id in comp_ids or r.region_id in used_regions:
                        continue
                    comp_ids.add(r.region_id)
                    neighbours = placer.find_adjacent_regions(r, all_regions, used_regions)
                    for n in neighbours:
                        if n.region_id not in comp_ids:
                            stack.append(n)

                # Jezeli komponent ma co najmniej 3 regiony, wybierz dwa najblizsze do kandydata
                if len(comp_ids) >= 3:
                    comp_regions = [r for r in all_regions if r.region_id in comp_ids and r.region_id != cand.region_id]
                    comp_regions.sort(key=lambda r: (r.seed_x - cand.seed_x) ** 2 + (r.seed_y - cand.seed_y) ** 2)
                    additional = comp_regions[:2]
                    assigned = [cand.region_id] + [r.region_id for r in additional]
                    candidate_city_to_fields[i] = assigned
                    used_regions.update(assigned)
                    found = True
                    break

            if not found:
                # Nie znaleziono spojnego komponentu dla tego miasta w tej rundzie - oznacz porazke i powtorz cala generacje
                failure = True
                break

        if not failure:
            city_to_fields = candidate_city_to_fields
            break

        # Jesli nie udalo sie, powtorz generacje regionow (losuj inne punkty)
        print(f"Nie udalo sie przypisac spojnych pol dla wszystkich miast - powtarzam generacje ({regen+1}/{max_regen_attempts})")
        # Regeneruj ziarna regionow i przemapuj tiles
        all_region_seeds = placer.generate_seeds_with_minimum_distance(total_regions, region_min_distance)
        if len(all_region_seeds) < total_regions:
            print(f"Uwaga: Udalo sie wygenerowac tylko {len(all_region_seeds)}/{total_regions} regionow podczas powtorzenia")
            total_regions = len(all_region_seeds)

        all_regions = []
        for i_s, (sx, sy) in enumerate(all_region_seeds):
            region = VoronoiRegion(sx, sy)
            region.region_id = i_s + 1
            all_regions.append(region)

        # Przypisz tiles do nowych regionow
        for y in range(map_format):
            for x in range(map_format):
                closest_region = min(all_regions, key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
                closest_region.tiles.append((x, y))

        # Wybrac nowe punkty miast (maksymalizujac dystanse)
        selected = select_regions_max_min_dist(all_regions, n=player_cities + neutral_cities)
        city_regions = [region for region in selected[:total_cities]]

    if city_to_fields is None:
        raise Exception(f"Nie udalo sie przypisac 3 przylegajacych pol dla kazdego miasta po {max_regen_attempts} probach")

    # Wypisz przypisania pol do miast
    for i, assigned in city_to_fields.items():
        print(f"  Miasto {i+1}: pola {assigned}")
        print(f"  Miasto {i+1}: pola ({all_regions[assigned[0] - 1].seed_x}, {all_regions[assigned[0] - 1].seed_y}), "
              f"({all_regions[assigned[1] - 1].seed_x}, {all_regions[assigned[1] - 1].seed_y}), "
              f"({all_regions[assigned[2] - 1].seed_x}, {all_regions[assigned[2] - 1].seed_y})")
    
    # Krok 4: Utworz obiekty miast
    cities = []
    for i, city_region in enumerate(city_regions):
        is_player = i < player_cities
        player_id = i + 1 if is_player else None
        rest_of_tiles = []

        rest_of_tiles.extend(all_regions[city_to_fields[i][1] - 1].tiles)
        rest_of_tiles.extend(all_regions[city_to_fields[i][2] - 1].tiles)

        city_region.tiles.extend(rest_of_tiles)
        
        city = CityWithVoronoi(
            x=float(city_region.seed_x),
            y=float(city_region.seed_y),
            is_player_city=is_player,
            player_id=player_id,
            voronoi_region=city_region,
            safety_radius=min_distance // 2,
            region_area=len(city_region.tiles)
        )
        cities.append(city)
    
    # Krok 5: Utworz informacje o wszystkich polach (regionach)
    fields_info = []
    city_regions_ids = set()  # ID regionow zajmowanych przez miasta
    for fields_list in city_to_fields.values():
        city_regions_ids.update(fields_list)
    
    for region in all_regions:
        # Oblicz centroid regionu
        centroid = placer._calculate_region_centroid(region)
        
        # Oblicz krawedzie regionu
        boundary = placer._region_boundary_polygon(region)
        
        # Rasteryzuj krawedzie na dyskretne punkty grid'a
        boundary_raster = placer._rasterize_boundary_edges(boundary)
        
        # Sprawdz czy region jest przypisany do miasta
        assigned_city = None
        for city_id, fields_list in city_to_fields.items():
            if region.region_id in fields_list:
                assigned_city = city_id + 1  # +1 bo city_id zaczyna sie od 0
                break
        
        field_info = FieldInfo(
            field_id=region.region_id,
            centroid=centroid,
            boundary=boundary,
            boundary_raster=boundary_raster,
            area=len(region.tiles),
            seed_position=(region.seed_x, region.seed_y),
            assigned_to_city=assigned_city
        )
        fields_info.append(field_info)
    
    # Sortuj pola po ID dla lepszej czytelnosci
    fields_info.sort(key=lambda f: f.field_id)
    
    # Wygeneruj obram�wki dla ca�ych obszar�w miast
    city_boundaries = generate_city_area_boundaries(all_regions, city_to_fields, placer)
    
    print(f"Wygenerowano {len(cities)} miast z {len(all_regions)} regionami")
    print(f"Przypisania pol do miast:")
    for i, fields in city_to_fields.items():
        city_type = "Gracz" if i < player_cities else "Neutralne"
        boundary_count = len(city_boundaries.get(i, []))
        print(f"  Miasto {i+1} ({city_type}): pola {fields}, obramowka {boundary_count} punktow")
    
    return {
        "cities": cities,
        "all_regions": all_regions, 
        "city_to_fields": city_to_fields,
        "fields_info": fields_info,
        "city_boundaries": city_boundaries
    }