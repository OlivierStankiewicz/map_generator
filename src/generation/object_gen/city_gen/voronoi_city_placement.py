"""
City placement using Voronoi diagrams with safety rings.
Uses existing Voronoi implementation to create natural city distribution.
"""

import math
from typing import List, Tuple, Dict, Optional

# Import the existing Voronoi implementation
from generation.pcg_algorithms.voronoi import VoronoiRegion
from generation.object_gen.city_gen.VoronoiCityPlacer import *


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
                                 ) -> Dict[int, List[Tuple[int, int]]]:
    """
    Generate external boundaries for entire city areas (all 3 fields together).
    
    Args:
        all_regions: List of all Voronoi regions
        city_to_fields: Mapping city_id -> list of fields
        
    Returns:
        Dict[city_id, List[boundary_points]] - external boundaries for each city
    """
    city_boundaries = {}
    
    for city_id, fields_list in city_to_fields.items():
        # Collect all tiles belonging to this city
        city_tiles = set()
        
        for field_id in fields_list:
            # Find region with this ID
            region = next((r for r in all_regions if r.region_id == field_id), None)
            if region:
                city_tiles.update(region.tiles)
        
        # Now find external edges of this area
        boundary_tiles = []
        
        for tile_x, tile_y in city_tiles:
            # Check if tile is on edge (has neighbor not belonging to city)
            is_boundary = False
            
            # Check all 8 neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                        
                    neighbor_x, neighbor_y = tile_x + dx, tile_y + dy
                    
                    # If neighbor is outside map or doesn't belong to this city
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
    Returns list of tiles belonging to a given Voronoi region.

    Can find region by `region_id` or by seed position `seed` (x, y).

    Args:
        all_regions: list of previously generated `VoronoiRegion` objects
        region_id: optional region ID (field.region_id)
        seed: optional tuple (x, y) of region seed position

    Returns:
        List of (x, y) tuples of tiles belonging to the region. Returns empty list if region not found.
    """
    if region_id is None and seed is None:
        raise ValueError("Must provide either region_id or seed=(x,y)")

    for region in all_regions:
        if region_id is not None and getattr(region, 'region_id', None) == region_id:
            return list(region.tiles) if getattr(region, 'tiles', None) else []

        if seed is not None and (getattr(region, 'seed_x', None), getattr(region, 'seed_y', None)) == seed:
            return list(region.tiles) if getattr(region, 'tiles', None) else []

    return []

def generate_city_positions_with_fields(map_size: int, num_of_player_cities: int, num_of_neutral_cities: int,
                                       min_distance: int, total_regions: int, reserved_tiles: set[tuple[int, int]]):
    """
    Generate city positions and all Voronoi regions, where each city has 3 fields.
    
    Args:
        map_format: Map size
        num_of_player_cities: Number of player cities  
        num_of_neutral_cities: Number of neutral cities
        min_distance: Minimum distance between cities
        total_regions: Total number of regions to generate
        
    Returns:
        dict: Contains 'cities', 'all_regions', 'city_to_fields'
    """

    placer = VoronoiCityPlacer(map_size)

    # Step 1: Generate all Voronoi regions
    all_regions, region_min_distance, total_regions = placer.generate_step_1(min_distance, reserved_tiles, total_regions)

    # Step 2: Select city positions from generated regions
    total_cities, city_regions = placer.generate_step_2(num_of_player_cities, num_of_neutral_cities, all_regions)

    # Step 3: Assign each city 3 fields (regions) - must form connected component of adjacent regions
    city_to_fields = placer.generate_step_3(region_min_distance, reserved_tiles, total_cities, city_regions, all_regions)
    
    # Krok 4: Utworz obiekty miast
    cities = placer.generate_step_4(city_regions, num_of_player_cities, all_regions, city_to_fields, min_distance)
    
    # Step 5: Create information about all fields (regions)
    fields_info = placer.generate_step_5(city_to_fields, all_regions)
    
    # Generate boundaries for entire city areas
    city_boundaries = generate_city_area_boundaries(all_regions, city_to_fields)

    return {
        "cities": cities,
        "all_regions": all_regions, 
        "city_to_fields": city_to_fields,
        "fields_info": fields_info,
        "city_boundaries": city_boundaries
    }