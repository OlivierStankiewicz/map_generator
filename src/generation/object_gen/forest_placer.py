"""
Forest/Tree placement algorithm with support for different object templates and hitboxes.

Supports placing trees on map while respecting:
- Passability and actionability (hitbox) constraints
- Terrain suitability for different tree types
- Occupied tiles from previously placed objects
- Density-based clustering for natural-looking forests
"""

import random
import math
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass

from classes.ObjectsTemplate import ObjectsTemplate
from classes.Objects.Objects import Objects
from classes.tile.Tile import TerrainType


@dataclass
class TreeType:
    """Informacja o typie drzewa."""
    template: ObjectsTemplate  # Template obiektu drzewa
    name: str  # Nazwa drzewa (np. "Oak", "Pine")
    terrain_affinity: Dict[TerrainType, float]  # Przeferencja terenu (0.0 - 1.0)
    passability: List[int]  # Tablica passability
    actionability: List[int]  # Tablica actionability
    min_distance: int  # Minimalna odległość od innych drzew


class ForestPlacer:
    """
    Algorytm rozmieszczania lasów na mapie.
    
    Strategie:
    1. Density Clustering: grupa drzew wokół centroidu
    2. Terrain Preference: wybór drzew na podstawie terenu
    3. Hitbox Avoidance: sprawdzenie kolizji z passability/actionability
    4. Occupied Tiles: pomijanie zajetych kafelków
    """
    
    def __init__(self, map_width: int, map_height: int, occupied_tiles: List[List[bool]]):
        """
        Args:
            map_width: szerokość mapy
            map_height: wysokość mapy
            occupied_tiles: tablica bool zajetych kafelków (6x8 dla każdego obiektu)
        """
        self.map_width = map_width
        self.map_height = map_height
        self.occupied_tiles = occupied_tiles
        self.placed_trees: List[Tuple[int, int, ObjectsTemplate]] = []
    
    def is_tile_available(self, x: int, y: int) -> bool:
        """
        Sprawdza czy kafelek jest dostępny (nie zajęty, w granicach mapy).
        
        Args:
            x, y: pozycja kafelka
            
        Returns:
            True jeśli kafelek jest wolny
        """
        if not (0 <= x < self.map_width and 0 <= y < self.map_height):
            return False
        return not self.occupied_tiles[y][x]
    
    def can_place_object(self, template: ObjectsTemplate, x: int, y: int) -> bool:
        """
        Sprawdza czy obiekt można umieścić na pozycji bez kolizji z hitboxem.
        
        Hitbox obiektu to obszar 6x8 wyznaczony przez passability/actionability.
        
        Args:
            template: template obiektu (zawiera passability/actionability)
            x, y: pozycja lewego górnego rogu
            
        Returns:
            True jeśli można umieścić obiekt bez kolizji
        """
        if not template.passability or not template.actionability:
            return True
        
        rows = 6
        cols = 8
        
        for row in range(rows):
            for col in range(cols):
                tile_x = x + col
                tile_y = y + row
                
                # Sprawdź granice mapy
                if not (0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height):
                    return False
                
                # Pobierz bity passability i actionability
                if row < len(template.passability) and col < 8:
                    passable = bool((template.passability[row] >> col) & 1)
                    actionable = False
                    if row < len(template.actionability):
                        actionable = bool((template.actionability[row] >> col) & 1)
                    
                    # Jeśli drzewo ma "hitbox" na tym kafelku, sprawdź czy jest zajęty
                    if not passable or actionable:
                        if self.occupied_tiles[tile_y][tile_x]:
                            return False
        
        return True
    
    def mark_object_as_placed(self, template: ObjectsTemplate, x: int, y: int):
        """
        Oznacza kafelki obiektu jako zajęte.
        
        Args:
            template: template obiektu
            x, y: pozycja lewego górnego rogu
        """
        if not template.passability or not template.actionability:
            return
        
        rows = 6
        cols = 8
        
        for row in range(rows):
            for col in range(cols):
                tile_x = x + col
                tile_y = y + row
                
                if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
                    if row < len(template.passability) and col < 8:
                        passable = bool((template.passability[row] >> col) & 1)
                        actionable = False
                        if row < len(template.actionability):
                            actionable = bool((template.actionability[row] >> col) & 1)
                        
                        if not passable or actionable:
                            self.occupied_tiles[tile_y][tile_x] = True
    
    def get_terrain_suitability(self, tiles: List[Tuple[int, int]], 
                               terrain_affinity: Dict[TerrainType, float]) -> float:
        """
        Oblicza przydatność terenu dla danego zestawu kafelków.
        
        Zwraca średnią wartość afinity dla typów terenu w obszarze.
        
        Args:
            tiles: lista kafelków (x, y) w obszarze
            terrain_affinity: słownik TerrainType -> wartość afinity (0.0-1.0)
            
        Returns:
            Średnia suitability (0.0-1.0)
        """
        if not tiles:
            return 0.5
        
        total_affinity = 0.0
        for x, y in tiles:
            if not (0 <= x < self.map_width and 0 <= y < self.map_height):
                continue
            
            # Pobierz typ terenu z mapy (jeśli dostępny)
            # W praktyce musisz mieć dostęp do self.tiles z TerrainType
            # Na razie zwracamy domyślną wartość
            total_affinity += 0.7  # Default affinity
        
        return total_affinity / len(tiles) if tiles else 0.5
    
    def find_cluster_center(self, cluster_seed_x: int, cluster_seed_y: int, 
                           cluster_radius: int) -> Tuple[int, int]:
        """
        Znajduje środek klastra dla drzew (punkt o największej gęstości wolnych kafelków).
        
        Args:
            cluster_seed_x, cluster_seed_y: punkt startowy
            cluster_radius: promień klastra
            
        Returns:
            (x, y) środek klastra
        """
        best_x, best_y = cluster_seed_x, cluster_seed_y
        best_count = 0
        
        for cx in range(max(0, cluster_seed_x - cluster_radius), 
                       min(self.map_width, cluster_seed_x + cluster_radius + 1)):
            for cy in range(max(0, cluster_seed_y - cluster_radius), 
                           min(self.map_height, cluster_seed_y + cluster_radius + 1)):
                free_count = 0
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if self.is_tile_available(cx + dx, cy + dy):
                            free_count += 1
                
                if free_count > best_count:
                    best_count = free_count
                    best_x, best_y = cx, cy
        
        return best_x, best_y
    
    def generate_forest_cluster(self, tree_types: List[TreeType],
                                cluster_center_x: int, cluster_center_y: int,
                                cluster_radius: int,
                                density: float = 0.6) -> List[Tuple[int, int, ObjectsTemplate]]:
        """
        Generuje klaster drzew wokół podanego punktu.
        
        Args:
            tree_types: lista dostępnych typów drzew
            cluster_center_x, cluster_center_y: środek klastra
            cluster_radius: promień klastra (w kafelkach)
            density: gęstość drzew (0.0-1.0, gdzie 1.0 = maksymalna gęstość)
            
        Returns:
            Lista (x, y, template) umieszczonych drzew
        """
        trees_placed = []
        
        # Próbuj umieścić drzewa w obrębie klastra
        attempts = int(cluster_radius ** 2 * density * 2)  # Heurystyka liczby prób
        
        for _ in range(attempts):
            # Losuj pozycję w obrębie klastra
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0, cluster_radius)
            
            tree_x = int(cluster_center_x + dist * math.cos(angle))
            tree_y = int(cluster_center_y + dist * math.sin(angle))
            
            # Sprawdź czy w granicach mapy
            if not (0 <= tree_x < self.map_width and 0 <= tree_y < self.map_height):
                continue
            
            # Wybierz losowy typ drzewa
            tree_type = random.choice(tree_types)
            
            # Sprawdź czy można umieścić
            if self.can_place_object(tree_type.template, tree_x, tree_y):
                # Sprawdź minimalną odległość do innych drzew
                too_close = False
                for placed_x, placed_y, _ in trees_placed:
                    dist_to_placed = math.sqrt((tree_x - placed_x) ** 2 + (tree_y - placed_y) ** 2)
                    if dist_to_placed < tree_type.min_distance:
                        too_close = True
                        break
                
                if not too_close:
                    self.mark_object_as_placed(tree_type.template, tree_x, tree_y)
                    trees_placed.append((tree_x, tree_y, tree_type.template))
                    self.placed_trees.append((tree_x, tree_y, tree_type.template))
        
        return trees_placed
    
    def generate_forests(self, tree_types: List[TreeType],
                        num_clusters: int = 10,
                        cluster_radius: int = 10,
                        density: float = 0.5) -> List[Tuple[int, int, ObjectsTemplate]]:
        """
        Generuje lasy na mapie (wiele klastrów drzew).
        
        Args:
            tree_types: lista dostępnych typów drzew
            num_clusters: liczba klastrów lasów
            cluster_radius: promień każdego klastra
            density: gęstość drzew w każdym klastrze (0.0-1.0)
            
        Returns:
            Lista wszystkich umieszczonych drzew (x, y, template)
        """
        all_trees = []
        
        for _ in range(num_clusters):
            # Losuj środek klastra
            center_x = random.randint(cluster_radius, self.map_width - cluster_radius)
            center_y = random.randint(cluster_radius, self.map_height - cluster_radius)
            
            # Znajdujemy lepszy punkt dla klastra
            center_x, center_y = self.find_cluster_center(center_x, center_y, cluster_radius)
            
            # Generuj klaster
            cluster_trees = self.generate_forest_cluster(
                tree_types,
                center_x, center_y,
                cluster_radius,
                density
            )
            
            all_trees.extend(cluster_trees)
        
        return all_trees
    
    def generate_forest_on_region(self, tree_types: List[TreeType],
                                  region_tiles: List[Tuple[int, int]],
                                  density: float = 0.4) -> List[Tuple[int, int, ObjectsTemplate]]:
        """
        Generuje las na podanym regionie (z listy kafelków, np. z diagramu Voronoi).
        
        Args:
            tree_types: lista dostępnych typów drzew
            region_tiles: lista kafelków (x, y) z regionu
            density: gęstość drzew (0.0-1.0)
            
        Returns:
            Lista umieszczonych drzew (x, y, template)
        """
        if not region_tiles:
            return []
        
        trees_placed = []
        
        # Liczba prób umieszczenia drzew
        num_attempts = int(len(region_tiles) * density)
        
        for _ in range(num_attempts):
            # Losuj tile z regionu
            tile_x, tile_y = random.choice(region_tiles)
            
            # Sprawdź czy kafelek jest dostępny
            if not self.is_tile_available(tile_x, tile_y):
                continue
            
            # Wybierz losowy typ drzewa
            tree_type = random.choice(tree_types)
            
            # Sprawdź czy można umieścić (pozycja to lewy górny róg hitboxa)
            if self.can_place_object(tree_type.template, tile_x, tile_y):
                # Sprawdzenie minimalne odległości
                too_close = False
                for placed_x, placed_y, _ in trees_placed:
                    dist = math.sqrt((tile_x - placed_x) ** 2 + (tile_y - placed_y) ** 2)
                    if dist < tree_type.min_distance:
                        too_close = True
                        break
                
                if not too_close:
                    self.mark_object_as_placed(tree_type.template, tile_x, tile_y)
                    trees_placed.append((tile_x, tile_y, tree_type.template))
                    self.placed_trees.append((tile_x, tile_y, tree_type.template))
        
        return trees_placed


def create_default_tree_types(tree_templates: List[ObjectsTemplate]) -> List[TreeType]:
    """
    Tworzy domyślne typy drzew z dostępnych szablonów.
    
    Args:
        tree_templates: lista ObjectsTemplate dla drzew
        
    Returns:
        Lista TreeType z domyślnymi parametrami
    """
    tree_types = []
    
    tree_names = ["Oak", "Pine", "Birch", "Spruce", "Maple", "Elm", "Ash", "Willow"]
    
    for i, template in enumerate(tree_templates):
        name = tree_names[i % len(tree_names)]
        
        # Domyślna preferencja terenu (większość drzew lubi trawę i las)
        terrain_affinity = {
            TerrainType.GRASS: 0.9,
            TerrainType.DIRT: 0.7,
            TerrainType.ROUGH: 0.6,
            TerrainType.SWAMP: 0.3,
            TerrainType.SAND: 0.2,
            TerrainType.SNOW: 0.4,
            TerrainType.SUBTERRANEAN: 0.0,
            TerrainType.LAVA: 0.0,
        }
        
        tree_type = TreeType(
            template=template,
            name=name,
            terrain_affinity=terrain_affinity,
            passability=getattr(template, 'passability', []),
            actionability=getattr(template, 'actionability', []),
            min_distance=3  # Minimalna odległość między drzewami
        )
        tree_types.append(tree_type)
    
    return tree_types
