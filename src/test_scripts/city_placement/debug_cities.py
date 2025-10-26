"""
Debug script to test city generation and see what's happening with neutral cities.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from voronoi_city_placement import VoronoiCityPlacer


def debug_city_generation():
    """Debug city generation step by step."""
    print("=== DEBUG CITY GENERATION ===")
    
    map_width, map_height = 144, 144
    player_cities, neutral_cities = 8, 5
    total_cities = player_cities + neutral_cities
    
    print(f"Map: {map_width}x{map_height}")
    print(f"Requested: {player_cities} players + {neutral_cities} neutrals = {total_cities} total")
    
    # Create placer
    placer = VoronoiCityPlacer(map_width, map_height)
    
    # Step 1: Generate seeds
    print(f"\nStep 1: Generating {total_cities} seeds...")
    seeds = placer.generate_seeds_with_minimum_distance(total_cities, 20)
    print(f"Generated {len(seeds)} seeds:")
    for i, (x, y) in enumerate(seeds):
        city_type = "Player" if i < player_cities else "Neutral"
        print(f"  {i}: {city_type} at ({x}, {y})")
    
    # Step 2: Create regions
    print(f"\nStep 2: Creating Voronoi regions...")
    from voronoi import VoronoiRegion
    regions = []
    for i, (x, y) in enumerate(seeds):
        region = VoronoiRegion(x, y)
        regions.append(region)
    
    print(f"Created {len(regions)} regions")
    
    # Step 3: Assign tiles
    print(f"\nStep 3: Assigning tiles to regions...")
    regions = placer._recalculate_voronoi(regions)
    
    for i, region in enumerate(regions):
        print(f"  Region {i}: {len(region.tiles)} tiles, seed at ({region.seed_x}, {region.seed_y})")
    
    # Step 4: Create cities
    print(f"\nStep 4: Creating city objects...")
    cities = []
    for i, region in enumerate(regions):
        safety_radius, region_area = placer.calculate_region_properties(region)
        
        is_player = i < player_cities
        player_id = i if is_player else None
        
        print(f"  City {i}: is_player={is_player}, player_id={player_id}")
        
        from voronoi_city_placement import CityWithVoronoi
        city = CityWithVoronoi(
            x=region.seed_x,
            y=region.seed_y,
            is_player_city=is_player,
            player_id=player_id,
            voronoi_region=region,
            safety_radius=safety_radius,
            region_area=region_area
        )
        cities.append(city)
    
    # Final check
    print(f"\nFinal results:")
    player_count = sum(1 for city in cities if city.is_player_city)
    neutral_count = sum(1 for city in cities if not city.is_player_city)
    
    print(f"Player cities: {player_count} (expected {player_cities})")
    print(f"Neutral cities: {neutral_count} (expected {neutral_cities})")
    print(f"Total cities: {len(cities)} (expected {total_cities})")
    
    print(f"\nCity details:")
    for i, city in enumerate(cities):
        city_type = f"Player {city.player_id}" if city.is_player_city else "Neutral"
        print(f"  {i}: {city_type} at ({city.x}, {city.y}), safety={city.safety_radius}")
    
    return cities


def test_visualization_issue():
    """Test if the issue is in visualization, not generation."""
    print(f"\n=== TESTING VISUALIZATION ===")
    
    # Generate cities normally
    placer = VoronoiCityPlacer(144, 144)
    cities = placer.place_cities_with_voronoi(8, 5)
    
    print(f"Generated {len(cities)} cities")
    
    # Check city types
    player_cities = [c for c in cities if c.is_player_city]
    neutral_cities = [c for c in cities if not c.is_player_city]
    
    print(f"Player cities: {len(player_cities)}")
    for city in player_cities:
        print(f"  Player {city.player_id}: ({city.x}, {city.y})")
    
    print(f"Neutral cities: {len(neutral_cities)}")
    for i, city in enumerate(neutral_cities):
        print(f"  Neutral {i+1}: ({city.x}, {city.y})")
    
    # Test the visualization function
    print(f"\nTesting visualization...")
    try:
        from voronoi_visualizer import create_voronoi_ascii_map
        ascii_map = create_voronoi_ascii_map(cities, 144, 144, scale=4)
        
        # Show a small portion
        print("Sample from ASCII map (first 20x20):")
        for i in range(min(20, len(ascii_map))):
            print("".join(ascii_map[i][:min(20, len(ascii_map[i]))]))
            
    except Exception as e:
        print(f"Visualization error: {e}")
    
    return cities


if __name__ == "__main__":
    cities = debug_city_generation()
    test_visualization_issue()