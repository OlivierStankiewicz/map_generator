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

    #* Step 1: Generate all Voronoi regions
    all_regions, region_min_distance = placer.generate_step_1(min_distance, reserved_tiles, total_regions)

    #* Step 2: Select city positions from generated regions
    total_cities, selected, city_regions = placer.generate_step_2(num_of_player_cities, num_of_neutral_cities, all_regions)

    # Step 3: Assign each city 3 fields (regions) - must form connected component of adjacent regions
    # If for any city we can't find 3 adjacent fields, repeat entire generation process
    max_regen_attempts = 50
    city_to_fields = None

    for _ in range(max_regen_attempts):
        # Reset assignments
        used_regions = set()
        candidate_city_to_fields: Dict[int, List[int]] = {}
        failure = False

        # For each city try to find connected component of size >= 3
        for i, city_region in enumerate(city_regions):
            # List of candidates for main region: first preferred, then other regions sorted by distance
            candidates = [city_region] + [r for r in sorted(all_regions, key=lambda r: placer.distance(r, city_region)) if r.region_id not in used_regions and r.region_id != city_region.region_id]

            found = False
            for cand in candidates:
                if cand.region_id in used_regions:
                    continue

                # BFS through graph of adjacent regions (skip already used regions)
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

                # If component has at least 3 regions, select two closest to candidate
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
                # No connected component found for this city in this round - mark failure and repeat entire generation
                failure = True
                break

        if not failure:
            city_to_fields = candidate_city_to_fields
            break

        # If failed, repeat region generation (randomize new points)
        # print(f"Failed to assign connected fields for all cities - repeating generation ({regen+1}/{max_regen_attempts})")
        # Regenerate region seeds and remap tiles
        all_region_seeds = placer.generate_seeds_with_minimum_distance(total_regions, region_min_distance, reserved_tiles)
        if len(all_region_seeds) < total_regions:
            # print(f"Warning: Could only generate {len(all_region_seeds)}/{total_regions} regions during retry")
            total_regions = len(all_region_seeds)

        all_regions = []
        for i_s, (sx, sy) in enumerate(all_region_seeds):
            region = VoronoiRegion(sx, sy)
            region.region_id = i_s + 1
            all_regions.append(region)

        # Assign tiles to new regions
        for y in range(map_size):
            for x in range(map_size):
                closest_region = min(all_regions, key=lambda r: (r.seed_x - x) ** 2 + (r.seed_y - y) ** 2)
                if (x, y) not in reserved_tiles:
                    closest_region.tiles.append((x, y))

        # Select new city points (maximizing distances)
        selected = placer.select_regions_max_min_dist(all_regions, n=num_of_player_cities + num_of_neutral_cities)
        city_regions = [region for region in selected[:total_cities]]

    if city_to_fields is None:
        raise Exception(f"Failed to assign 3 adjacent fields for each city after {max_regen_attempts} attempts")

    # Wypisz przypisania pol do miast
    # for i, assigned in city_to_fields.items():
        # print(f"  Miasto {i+1}: pola {assigned}")
        # print(f"  Miasto {i+1}: pola ({all_regions[assigned[0] - 1].seed_x}, {all_regions[assigned[0] - 1].seed_y}), "
        #       f"({all_regions[assigned[1] - 1].seed_x}, {all_regions[assigned[1] - 1].seed_y}), "
        #       f"({all_regions[assigned[2] - 1].seed_x}, {all_regions[assigned[2] - 1].seed_y})")
    
    # Krok 4: Utworz obiekty miast
    cities: CityWithVoronoi = []
    for i, city_region in enumerate(city_regions):
        is_player = i < num_of_player_cities
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
    
    # Step 5: Create information about all fields (regions)
    fields_info = []
    city_regions_ids = set()  # IDs of regions occupied by cities
    for fields_list in city_to_fields.values():
        city_regions_ids.update(fields_list)
    
    for region in all_regions:
        # Calculate region centroid
        centroid = placer._calculate_region_centroid(region)
        
        # Calculate region edges
        boundary = placer._region_boundary_polygon(region)
        
        # Rasterize edges to discrete grid points
        boundary_raster = placer._rasterize_boundary_edges(boundary)
        
        # Check if region is assigned to a city
        assigned_city = None
        for city_id, fields_list in city_to_fields.items():
            if region.region_id in fields_list:
                assigned_city = city_id + 1  # +1 because city_id starts from 0
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
    
    # Sort fields by ID for better readability
    fields_info.sort(key=lambda f: f.field_id)
    
    # Generate boundaries for entire city areas
    city_boundaries = generate_city_area_boundaries(all_regions, city_to_fields, placer)
    
    # print(f"Generated {len(cities)} cities with {len(all_regions)} regions")
    # print(f"Field assignments to cities:")
    for i, fields in city_to_fields.items():
        city_type = "Gracz" if i < num_of_player_cities else "Neutralne"
        boundary_count = len(city_boundaries.get(i, []))
        # print(f"  City {i+1} ({city_type}): fields {fields}, boundary {boundary_count} points")
    
    return {
        "cities": cities,
        "all_regions": all_regions, 
        "city_to_fields": city_to_fields,
        "fields_info": fields_info,
        "city_boundaries": city_boundaries
    }