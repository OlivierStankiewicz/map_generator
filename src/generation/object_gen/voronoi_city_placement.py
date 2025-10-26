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
from voronoi import VoronoiRegion, generate_voronoi_regions

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
        
        Cities can be placed near map edges - minimum distance only applies between cities.
        """
        seeds = []
        max_attempts = num_cities * 100  # More attempts for better results
        attempts = 0
        
        # Small margin from edges to avoid placement exactly on border
        edge_margin = 3  # Just enough to avoid edge artifacts
        
        # print(f"Generating {num_cities} cities with min distance {min_distance}...")
        
        while len(seeds) < num_cities and attempts < max_attempts:
            # Generate candidate position - prefer edges for better distribution
            x, y = self.generate_edge_preferred_position(edge_margin)
            
            # Check distance to existing seeds
            valid = True
            for sx, sy in seeds:
                distance = math.sqrt((x - sx)**2 + (y - sy)**2)
                if distance < min_distance:
                    valid = False
                    break
            
            if valid:
                seeds.append((x, y))
                # print(f"  Placed city {len(seeds)} at ({x}, {y})")
            
            attempts += 1
            
            # Progress indicator for long searches
            # if attempts % (num_cities * 10) == 0:
            #     print(f"  Attempt {attempts}/{max_attempts}, placed {len(seeds)}/{num_cities}")
        
        # If we couldn't place all cities with min_distance
        # if len(seeds) < num_cities:
        #     print(f"Warning: Could only place {len(seeds)}/{num_cities} cities with distance {min_distance}")
        #     print(f"Consider reducing city count or minimum distance")
        
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
        region1_tiles = set(region1.tiles)
        region2_tiles = set(region2.tiles)
        
        # Check all tiles of region1 for adjacency to region2
        for x, y in region1.tiles:
            # Check 4-connected neighbors
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in region2_tiles:
                    # This point is on the boundary
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
    
    def _recalculate_voronoi(self, regions: List[VoronoiRegion]) -> List[VoronoiRegion]:
        """Recalculate Voronoi diagram with current seed positions."""
        # Clear existing tiles
        for region in regions:
            region.tiles = []
            region.neighbors = set()
        
        # Reassign tiles to closest seeds
        for y in range(self.map_height):
            for x in range(self.map_width):
                closest_region = min(
                    regions, 
                    key=lambda r: (r.seed_x - x)**2 + (r.seed_y - y)**2
                )
                closest_region.tiles.append((x, y))
        
        # Recalculate neighbors
        self._find_neighbors(regions)
        
        return regions
    
    def _find_neighbors(self, regions: List[VoronoiRegion]):
        """Find neighboring regions for each region."""
        # Create ownership map
        ownership = {}
        for region in regions:
            for x, y in region.tiles:
                ownership[(x, y)] = region
        
        # Find neighbors by checking adjacent tiles
        for region in regions:
            for x, y in region.tiles:
                for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in ownership:
                        neighbor = ownership[(nx, ny)]
                        if neighbor != region:
                            region.neighbors.add(neighbor)
    
    def place_cities_with_voronoi(self, 
                                 player_cities: int, 
                                 neutral_cities: int,
                                 min_distance: int = 20,
                                 max_attempts: int = 3,
                                 max_attempts_per_attempt: int = 10,
                                 return_edges: bool = False,
                                 return_tile_centers: bool = True,
                                 include_region_boundaries: bool = False) -> VoronoiResult:
        """
        Main function to place cities using Voronoi diagrams with distance constraints.
        
        Args:
            player_cities: Number of player cities
            neutral_cities: Number of neutral cities  
            min_distance: Minimum distance between cities (default 20)
            max_attempts: Number of attempts if placement fails
            return_edges: Whether to calculate and return Voronoi edges
        
        Returns:
            VoronoiResult: Cities with their Voronoi regions, safety radii, and optionally edges
        """
        total_cities = player_cities + neutral_cities
        
        # Validate if this many cities can fit
        can_fit, message, max_recommended = True, "", total_cities  # self.validate_city_count(total_cities, min_distance)
        # print(f"City count validation: {message}")
        
        if not can_fit:
            # print(f"Reducing city count from {total_cities} to {max_recommended}")
            # Proportionally reduce both types
            ratio = max_recommended / total_cities
            player_cities = max(1, int(player_cities * ratio))
            neutral_cities = max(0, max_recommended - player_cities)
            total_cities = player_cities + neutral_cities
            # print(f"New counts: {player_cities} players + {neutral_cities} neutrals = {total_cities} total")
        
        best_cities = None
        best_min_distance = 0
        
        for attempt in range(max_attempts):
            for at in range(max_attempts_per_attempt):
                print(f"\n--- Attempt {attempt + 1}/{max_attempts} ---")
                print(f"--- Attempt per attempt {at + 1}/{max_attempts_per_attempt} ---")
                
                # Try with current min_distance, reduce if needed
                current_min_distance = max(15, min_distance - attempt * 5)
                # print(f"Trying with minimum distance: {current_min_distance}")
                
                # Step 1: Generate seeds with minimum distance
                seeds = self.generate_seeds_with_minimum_distance(total_cities, current_min_distance)
                
                if len(seeds) < total_cities:
                    # print(f"Failed to place all cities, continuing with {len(seeds)}")
                    continue
                
                # Step 2: Create initial Voronoi regions
                regions = []
                for i, (x, y) in enumerate(seeds):
                    region = VoronoiRegion(x, y)
                    regions.append(region)
                
                # Assign tiles to regions
                regions = self._recalculate_voronoi(regions)
                
                # Step 3: Apply Lloyd's relaxation for better distribution
                regions = self.lloyd_relaxation(regions, iterations=2)  # Fewer iterations to preserve distances
                
                # Step 4: Calculate safety radii and create city objects
                cities = []
                for i, region in enumerate(regions):
                    safety_radius, region_area = self.calculate_region_properties(region)

                    is_player = i < player_cities
                    player_id = i if is_player else None

                    # City coordinates: optionally return tile centers (float)
                    cx = region.seed_x + (0.5 if return_tile_centers else 0)
                    cy = region.seed_y + (0.5 if return_tile_centers else 0)

                    region_boundary = None
                    if include_region_boundaries:
                        region_boundary = self._region_boundary_polygon(region)

                    city = CityWithVoronoi(
                        x=cx,
                        y=cy,
                        is_player_city=is_player,
                        player_id=player_id,
                        voronoi_region=region,
                        safety_radius=safety_radius,
                        region_area=region_area,
                        region_boundary=region_boundary
                    )
                    cities.append(city)
                
                # Validate actual distances achieved
                actual_min_distance = self._calculate_minimum_distance(cities)
                print(f"Achieved minimum distance: {actual_min_distance:.1f}")
                
                if actual_min_distance >= current_min_distance * 0.8:  # Allow 20% tolerance
                    if actual_min_distance > best_min_distance:
                        best_cities = cities
                        best_min_distance = actual_min_distance
                        # print(f"New best result: {actual_min_distance:.1f}")
                        
                    if actual_min_distance >= min_distance * 0.9:  # Good enough
                        break
        
        if best_cities is None:
            raise RuntimeError(f"Could not place {total_cities} cities with minimum distance {min_distance}")
        
        # Calculate edges if requested
        edges = []
        if return_edges:
            # print("Calculating Voronoi edges...")
            regions = [city.voronoi_region for city in best_cities]
            edges = self.calculate_voronoi_edges(regions)
            # print(f"Found {len(edges)} edges between regions")
        
        print(f"\nFinal result: {len(best_cities)} cities with min distance {best_min_distance:.1f}")
        return VoronoiResult(
            cities=best_cities,
            edges=edges,
            min_distance_achieved=best_min_distance
        )
    
    def _calculate_minimum_distance(self, cities: List[CityWithVoronoi]) -> float:
        """Calculate minimum distance between any two cities."""
        min_distance = float('inf')
        for i, city1 in enumerate(cities):
            for city2 in cities[i+1:]:
                distance = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
                min_distance = min(min_distance, distance)
        return min_distance
    
    def validate_placement(self, cities: List[CityWithVoronoi]) -> Tuple[bool, List[str]]:
        """
        Validate that city placement meets safety requirements.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_problems)
        """
        problems = []
        
        for i, city1 in enumerate(cities):
            # Check if city is within map bounds with safety margin
            if (city1.x - city1.safety_radius < 0 or 
                city1.x + city1.safety_radius >= self.map_width or
                city1.y - city1.safety_radius < 0 or 
                city1.y + city1.safety_radius >= self.map_height):
                problems.append(f"City {i} safety zone extends beyond map boundaries")
            
            # Check distances to other cities
            for j, city2 in enumerate(cities[i+1:], i+1):
                distance = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
                required_distance = city1.safety_radius + city2.safety_radius
                
                if distance < required_distance:
                    problems.append(
                        f"Cities {i} and {j} safety zones overlap "
                        f"(distance: {distance:.1f}, required: {required_distance})"
                    )
        
        return len(problems) == 0, problems


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
