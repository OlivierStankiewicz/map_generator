# -*- coding: utf-8 -*-
"""
Test large distance city placement with visualization.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from voronoi_city_placement import quick_city_placement, get_city_limits_for_map
from voronoi_visualizer import create_voronoi_ascii_map, print_voronoi_map, analyze_voronoi_placement
import math


def test_large_distance_placement():
    """Test city placement with large minimum distances."""
    print("=== TESTING LARGE DISTANCE CITY PLACEMENT ===")
    
    # Test case: 144x144 map with 25+ distance
    map_width, map_height = 144, 144
    min_distance = 25
    
    # Check what's possible
    limits = get_city_limits_for_map(map_width, map_height, min_distance)
    print(f"Map {map_width}x{map_height} with min distance {min_distance}:")
    print(f"Max cities: {limits['max_cities']}")
    print(f"Area per city: {limits['area_per_city']:.0f} tiles")
    
    print("\nRecommended configurations:")
    for rec in limits['recommendations']:
        print(f"  - {rec['players']} players + {rec['neutrals']} neutrals ({rec['description']})")
    
    # Try a good configuration
    players, neutrals = 6, 3
    print(f"\nTesting {players} players + {neutrals} neutrals with min distance {min_distance}:")
    
    cities, success, problems = quick_city_placement(
        map_width, map_height, players, neutrals, min_distance
    )
    
    if success:
        print(f"? Success! Placed {len(cities)} cities")
        
        # Calculate actual minimum distance
        min_actual = float('inf')
        for i, city1 in enumerate(cities):
            for city2 in cities[i+1:]:
                dist = math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)
                min_actual = min(min_actual, dist)
        
        print(f"Achieved minimum distance: {min_actual:.1f}")
        
        # Show detailed analysis
        analyze_voronoi_placement(cities, map_width, map_height)
        
        # Show coordinates
        print(f"\n=== CITY COORDINATES ===")
        print("Player cities:")
        for city in cities:
            if city.is_player_city:
                print(f"  Player {city.player_id}: ({city.x:3d}, {city.y:3d}) safety={city.safety_radius:2d}")
        
        print("Neutral cities:")
        neutral_count = 0
        for city in cities:
            if not city.is_player_city:
                neutral_count += 1
                print(f"  Neutral {neutral_count}: ({city.x:3d}, {city.y:3d}) safety={city.safety_radius:2d}")
        
        # Create visualization
        ascii_map = create_voronoi_ascii_map(cities, map_width, map_height, scale=2)
        print_voronoi_map(ascii_map, f"Cities with {min_actual:.1f}+ distance (scale 1:2)")
        
        return cities
    else:
        print(f"? Failed: {problems}")
        return None


def test_different_distances():
    """Test different minimum distances to show the trade-offs."""
    print(f"\n=== DISTANCE TRADE-OFF ANALYSIS ===")
    
    map_size = 144
    test_distances = [15, 20, 25, 30, 35]
    
    print(f"Map: {map_size}x{map_size}")
    print("Distance | Max Cities | Example Config")
    print("-" * 40)
    
    for dist in test_distances:
        limits = get_city_limits_for_map(map_size, map_size, dist)
        max_cities = limits['max_cities']
        
        # Find best recommendation that fits
        best_rec = None
        for rec in limits['recommendations']:
            if rec['total'] <= max_cities:
                best_rec = rec
        
        if best_rec:
            config = f"{best_rec['players']}P + {best_rec['neutrals']}N"
        else:
            config = "Too few cities"
        
        print(f"{dist:8d} | {max_cities:10d} | {config}")
    
    print(f"\nConclusion:")
    print(f"- Distance 20-25: Good balance for most maps")
    print(f"- Distance 30+: Requires fewer cities or larger maps")
    print(f"- Consider 200x200+ maps for many cities with large distances")


if __name__ == "__main__":
    cities = test_large_distance_placement()
    test_different_distances()
    
    # Show quick recommendations
    print(f"\n=== QUICK RECOMMENDATIONS ===")
    print(f"For 144x144 maps:")
    print(f"  - Distance 20: Up to 8 players + 5 neutrals")
    print(f"  - Distance 25: Up to 6 players + 3 neutrals") 
    print(f"  - Distance 30: Up to 4 players + 2 neutrals")
    print(f"")
    print(f"For 200x200 maps:")
    print(f"  - Distance 20: Up to 15 players + 10 neutrals")
    print(f"  - Distance 25: Up to 12 players + 8 neutrals")
    print(f"  - Distance 30: Up to 9 players + 6 neutrals")