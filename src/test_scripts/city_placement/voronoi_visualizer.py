"""
ASCII visualization for Voronoi-based city placement.
Shows Voronoi regions, cities, and safety zones.
"""

import math
from voronoi_city_placement import VoronoiCityPlacer, CityWithVoronoi


def create_voronoi_ascii_map(cities, map_width, map_height, scale=2):
    """
    Create ASCII map showing Voronoi regions and cities.
    
    Legend:
    - Numbers/Letters = City centers (0-9 for players, A-Z for neutrals)
    - Different ASCII chars = Different Voronoi regions
    - ? = Safety zone boundaries
    """
    ascii_width = map_width // scale
    ascii_height = map_height // scale
    
    # Initialize map
    ascii_map = [['.' for _ in range(ascii_width)] for _ in range(ascii_height)]
    region_chars = "????????????????????"
    
    # Mark Voronoi regions
    for city_idx, city in enumerate(cities):
        region_char = region_chars[city_idx % len(region_chars)]
        
        # Mark all tiles in this Voronoi region
        for tile_x, tile_y in city.voronoi_region.tiles:
            ascii_x = tile_x // scale
            ascii_y = tile_y // scale
            if 0 <= ascii_x < ascii_width and 0 <= ascii_y < ascii_height:
                ascii_map[ascii_y][ascii_x] = region_char
    
    # Mark safety zones (rough circles)
    for city_idx, city in enumerate(cities):
        center_x = city.x // scale
        center_y = city.y // scale
        radius = city.safety_radius // scale
        
        # Draw safety circle
        for y in range(max(0, center_y - radius), min(ascii_height, center_y + radius + 1)):
            for x in range(max(0, center_x - radius), min(ascii_width, center_x + radius + 1)):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                if abs(distance - radius) < 0.7:  # Circle boundary
                    ascii_map[y][x] = '?'
    
    # Mark city centers
    neutral_counter = 0
    for city_idx, city in enumerate(cities):
        center_x = city.x // scale
        center_y = city.y // scale
        
        if 0 <= center_x < ascii_width and 0 <= center_y < ascii_height:
            if city.is_player_city:
                ascii_map[center_y][center_x] = str(city.player_id) if city.player_id < 10 else 'P'
            else:
                ascii_map[center_y][center_x] = chr(ord('A') + neutral_counter) if neutral_counter < 26 else 'N'
                neutral_counter += 1
    
    return ascii_map


def print_voronoi_map(ascii_map, title="Voronoi City Placement"):
    """Print the ASCII map with coordinates and legend."""
    print(f"\n=== {title} ===")
    
    width = len(ascii_map[0])
    height = len(ascii_map)
    
    # Column headers
    print("     " + "".join([str(i//10) if i >= 10 else " " for i in range(0, width, 5)]))
    print("     " + "".join([str(i%10) for i in range(0, width, 5)]))
    print("    +" + "-" * width)
    
    # Map rows
    for i, row in enumerate(ascii_map):
        if i % 5 == 0:
            print(f"{i:3d} |" + "".join(row))
        else:
            print("    |" + "".join(row))
    
    print("\nLegend:")
    print("  0-9     = Player cities (number = player ID)")
    print("  A-Z     = Neutral cities")
    print("  ?       = Safety zone boundary")
    print("  ????... = Voronoi regions (each city's territory)")
    print("  .       = Empty space")


def analyze_voronoi_placement(cities, map_width, map_height):
    """Analyze and report statistics about Voronoi placement."""
    print(f"\n=== VORONOI ANALYSIS ===")
    print(f"Map: {map_width}x{map_height} = {map_width * map_height:,} tiles")
    
    player_cities = [c for c in cities if c.is_player_city]
    neutral_cities = [c for c in cities if not c.is_player_city]
    
    print(f"Cities: {len(player_cities)} players + {len(neutral_cities)} neutrals = {len(cities)} total")
    
    # Region size statistics
    total_area = sum(c.region_area for c in cities)
    print(f"Total region area: {total_area:,} tiles ({total_area/(map_width*map_height)*100:.1f}% of map)")
    
    if player_cities:
        player_areas = [c.region_area for c in player_cities]
        player_radii = [c.safety_radius for c in player_cities]
        print(f"\nPlayer cities:")
        print(f"  Region areas: min={min(player_areas)}, max={max(player_areas)}, avg={sum(player_areas)/len(player_areas):.0f}")
        print(f"  Safety radii: min={min(player_radii)}, max={max(player_radii)}, avg={sum(player_radii)/len(player_radii):.1f}")
    
    if neutral_cities:
        neutral_areas = [c.region_area for c in neutral_cities]
        neutral_radii = [c.safety_radius for c in neutral_cities]
        print(f"\nNeutral cities:")
        print(f"  Region areas: min={min(neutral_areas)}, max={max(neutral_areas)}, avg={sum(neutral_areas)/len(neutral_areas):.0f}")
        print(f"  Safety radii: min={min(neutral_radii)}, max={max(neutral_radii)}, avg={sum(neutral_radii)/len(neutral_radii):.1f}")
    
    # Distance analysis
    distances = []
    for i, city1 in enumerate(cities):
        for city2 in cities[i+1:]:
            dist = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
            distances.append(dist)
    
    if distances:
        print(f"\nCity distances:")
        print(f"  Minimum: {min(distances):.1f}")
        print(f"  Maximum: {max(distances):.1f}")
        print(f"  Average: {sum(distances)/len(distances):.1f}")
    
    # Safety zone coverage
    total_safety_area = sum(math.pi * c.safety_radius**2 for c in cities)
    print(f"\nSafety zones:")
    print(f"  Total safety area: {total_safety_area:.0f} tiles ({total_safety_area/(map_width*map_height)*100:.1f}% of map)")
    
    # Check for overlapping safety zones
    overlaps = 0
    for i, city1 in enumerate(cities):
        for city2 in cities[i+1:]:
            distance = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
            required_distance = city1.safety_radius + city2.safety_radius
            if distance < required_distance:
                overlaps += 1
    
    print(f"  Overlapping safety zones: {overlaps}")


def demo_voronoi_city_placement():
    """Complete demo of Voronoi city placement with visualization."""
    print("=== VORONOI CITY PLACEMENT DEMO ===")
    
    # Test case: Standard Heroes 3 map
    map_width, map_height = 144, 144
    player_cities, neutral_cities = 8, 5
    
    print(f"\nGenerating cities for {map_width}x{map_height} map...")
    print(f"Cities: {player_cities} players + {neutral_cities} neutrals")
    
    # Create placer and generate cities
    placer = VoronoiCityPlacer(map_width, map_height)
    cities = placer.place_cities_with_voronoi(player_cities, neutral_cities)
    
    # Validate placement
    is_valid, problems = placer.validate_placement(cities)
    print(f"\nValidation: {'? PASSED' if is_valid else '? FAILED'}")
    if problems:
        print("Issues found:")
        for problem in problems:
            print(f"  - {problem}")
    
    # Show detailed analysis
    analyze_voronoi_placement(cities, map_width, map_height)
    
    # Show city coordinates
    print(f"\n=== CITY COORDINATES ===")
    print("Player cities:")
    for city in cities:
        if city.is_player_city:
            print(f"  Player {city.player_id}: ({city.x:3d}, {city.y:3d}) "
                  f"safety={city.safety_radius:2d}, area={city.region_area:4d}")
    
    print("Neutral cities:")
    neutral_count = 0
    for city in cities:
        if not city.is_player_city:
            neutral_count += 1
            print(f"  Neutral {neutral_count}: ({city.x:3d}, {city.y:3d}) "
                  f"safety={city.safety_radius:2d}, area={city.region_area:4d}")
    
    # Create ASCII visualization
    ascii_map = create_voronoi_ascii_map(cities, map_width, map_height, scale=2)
    print_voronoi_map(ascii_map, f"Map {map_width}x{map_height} (scale 1:2)")
    
    return cities


def compare_voronoi_vs_grid():
    """Compare Voronoi approach with regular grid placement."""
    print("\n" + "="*60)
    print("COMPARISON: VORONOI vs REGULAR GRID")
    print("="*60)
    
    map_size = 144
    players, neutrals = 8, 5
    
    print(f"\nTest case: {map_size}x{map_size} map, {players} players + {neutrals} neutrals")
    
    # Voronoi approach
    print(f"\n--- VORONOI APPROACH ---")
    placer = VoronoiCityPlacer(map_size, map_size)
    voronoi_cities = placer.place_cities_with_voronoi(players, neutrals)
    
    voronoi_distances = []
    for i, city1 in enumerate(voronoi_cities):
        for city2 in voronoi_cities[i+1:]:
            dist = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
            voronoi_distances.append(dist)
    
    voronoi_min_dist = min(voronoi_distances)
    voronoi_avg_dist = sum(voronoi_distances) / len(voronoi_distances)
    voronoi_safety_avg = sum(c.safety_radius for c in voronoi_cities) / len(voronoi_cities)
    
    print(f"Min distance: {voronoi_min_dist:.1f}")
    print(f"Avg distance: {voronoi_avg_dist:.1f}")
    print(f"Avg safety radius: {voronoi_safety_avg:.1f}")
    print("Advantages: Natural territories, adaptive radii, no overlaps by design")
    
    # Regular grid approach (theoretical)
    print(f"\n--- REGULAR GRID APPROACH ---")
    total_cities = players + neutrals
    grid_size = math.ceil(math.sqrt(total_cities))
    cell_size = map_size / grid_size
    grid_min_dist = cell_size
    grid_avg_dist = cell_size * 1.4  # Approximate
    
    # Theoretical uniform safety radius
    area_per_city = (map_size * map_size) / total_cities
    uniform_radius = math.sqrt(area_per_city / math.pi) * 0.6
    
    print(f"Min distance: {grid_min_dist:.1f}")
    print(f"Avg distance: {grid_avg_dist:.1f}")
    print(f"Uniform safety radius: {uniform_radius:.1f}")
    print("Advantages: Predictable, uniform distribution, simple calculation")
    
    print(f"\nConclusion:")
    print(f"- Voronoi gives more natural, varied territories")
    print(f"- Grid gives more predictable, uniform layout")
    print(f"- Voronoi better for organic feel, Grid better for balanced gameplay")


if __name__ == "__main__":
    # Run the demo
    cities = demo_voronoi_city_placement()
    
    # Run comparison
    compare_voronoi_vs_grid()