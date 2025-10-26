# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Test dla nowej funkcjonalnosci krawedzi Voronoi.
"""

from voronoi_city_placement import quick_city_placement, VoronoiCityPlacer

def test_simple_edges():
    """Prosty test pokazujacy jak uzyskac krawedzie Voronoi."""
    print("=== PROSTY TEST KRAWEDZI VORONOI ===\n")
    
    # Test z mniejsz� map� dla �atwiejszej wizualizacji
    result, success, problems = quick_city_placement(
        map_width=72,
        map_height=72,
        player_cities=5,
        neutral_cities=3,
        min_distance=25,
        include_edges=True  # Wlaczamy obliczanie krawedzi
    )
    
    if not success:
        print(f"Blad: {problems}")
        return
    
    print(f"Sukces! Umieszczono {len(result.cities)} miast")
    print(f"Minimalna odleglosc: {result.min_distance_achieved:.1f}")
    print(f"Liczba krawedzi: {len(result.edges)}")
    
    print(f"\nPOZYCJE MIAST:")
    for i, city in enumerate(result.cities):
        city_type = f"Gracz {city.player_id}" if city.is_player_city else f"Neutralne {i - sum(1 for c in result.cities[:i] if c.is_player_city) + 1}"
        print(f"  {city_type}: ({city.x:2d}, {city.y:2d}) - Region: {city.region_area:4d} pol")
    
    print(f"\nKRAWEDZIE VORONOI:")
    for i, edge in enumerate(result.edges, 1):
        seed1 = edge.region1_seed
        seed2 = edge.region2_seed
        print(f"  Krawedz {i:2d}: ({seed1[0]:2d},{seed1[1]:2d}) <-> ({seed2[0]:2d},{seed2[1]:2d}) | Dlugosc: {edge.length:.0f} punktow")
    
    # Analiza polaczen
    print(f"\nANALIZA POLACZEN:")
    connections = {}
    for edge in result.edges:
        seed1, seed2 = edge.region1_seed, edge.region2_seed
        connections[seed1] = connections.get(seed1, 0) + 1
        connections[seed2] = connections.get(seed2, 0) + 1
    
    for city in result.cities:
        seed = (city.x, city.y)
        city_type = f"Gracz {city.player_id}" if city.is_player_city else "Neutralne"
        neighbor_count = connections.get(seed, 0)
        print(f"  {city_type} ({city.x:2d},{city.y:2d}): {neighbor_count} sasiadow")
    
    return result

def test_edge_visualization():
    """Test z wizualizacja ASCII pokazujaca krawedzie."""
    print(f"\n=== WIZUALIZACJA KRAWEDZI ===\n")
    
    # Mala mapa dla latwej wizualizacji
    placer = VoronoiCityPlacer(50, 30)
    result = placer.place_cities_with_voronoi(
        player_cities=3,
        neutral_cities=1, 
        min_distance=10,
        return_edges=True
    )
    
    print(f"Mapa 50x30, miasta: {len(result.cities)}, krawedzie: {len(result.edges)}")
    
    # Prosty ASCII art
    grid = [['.' for _ in range(50)] for _ in range(30)]
    
    # Oznacz miasta
    for i, city in enumerate(result.cities):
        if 0 <= city.x < 50 and 0 <= city.y < 30:
            grid[city.y][city.x] = str(i)
    
    # Pokaz mape
    print("Mapa (cyfry = miasta, . = puste pole):")
    for row in grid:
        print(''.join(row))
    
    # Pokaz krawedzie
    print(f"\nKrawedzie miedzy miastami:")
    for i, edge in enumerate(result.edges, 1):
        # Znajdz miasta dla tych pozycji
        city1 = next(c for c in result.cities if (c.x, c.y) == edge.region1_seed)
        city2 = next(c for c in result.cities if (c.x, c.y) == edge.region2_seed)
        city1_idx = result.cities.index(city1)
        city2_idx = result.cities.index(city2)
        
        print(f"  {i}: Miasto {city1_idx} <-> Miasto {city2_idx} (dlugosc: {edge.length:.0f})")

if __name__ == "__main__":
    # Uruchom testy
    result = test_simple_edges()
    test_edge_visualization()
    
    print(f"\nGOTOWE! Teraz masz dostep do krawedzi grafu Voronoi.")
    print(f"Uzyj: result, success, problems = quick_city_placement(..., include_edges=True)")
    print(f"Wynik zawiera: result.cities, result.edges, result.min_distance_achieved")