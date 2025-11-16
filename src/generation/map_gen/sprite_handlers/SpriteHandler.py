from classes.tile.Tile import TerrainType
from generation.tile_gen.tile_gen import SpriteType
from abc import ABC, abstractmethod

class SpriteHandler(ABC):
    @abstractmethod
    def choose_sprite(self, terrain_map: list[list[TerrainType]], x: int, y: int) -> tuple[int, bool, bool]:
        """
        Choose a sprite and its rotation for the tile at (x, y) based on its terrain type and neighbors.
            Parameters:
                terrain_map: 2D list of TerrainType representing the map.
                x: X coordinate of the tile.
                y: Y coordinate of the tile.
            Returns:
                a tuple of (sprite_number, x_terrain_flip, y_terrain_flip).
        """
        pass

    def _get_neighbors(self, terrain_map: list[list[TerrainType]], x: int, y: int) -> list[list[TerrainType]]:
        """
        Get the 3x3 grid of neighbors around the tile at (x, y). Handles out-of-bounds by duplicating edge tiles.
            Parameters:
                terrain_map: 2D list of TerrainType representing the map.
                x: X coordinate of the tile.
                y: Y coordinate of the tile.
            Returns:
                a 3x3 list of TerrainType representing the neighbors.
        """
        neighbors = [[None for _ in range(3)] for _ in range(3)]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(terrain_map) and 0 <= nx < len(terrain_map[0]):
                    neighbors[dy + 1][dx + 1] = terrain_map[ny][nx]

        rows = neighbors
        cols = list(zip(*rows))
        
        empty_col, empty_row = None, None
        for i in range(3):
            if all(tile is None for tile in rows[i]):
                empty_row = i
            if all(tile is None for tile in cols[i]):
                empty_col = i
        if empty_row is not None:
            neighbors[empty_row] = neighbors[1]
        if empty_col is not None:
            for i in range(3):
                neighbors[i][empty_col] = neighbors[i][1]
        
        return neighbors
    
    def _resolve_inner_corner_conflict(self, neighbors_string: str, terrain_map: list[list[TerrainType]], x, y, neighbor_to_sprite_map: list[tuple[str, SpriteType, bool, bool]]) -> tuple[SpriteType, bool, bool] | None:
        """
        Resolve inner corner conflicts based on extended neighbor checks.
            Parameters:
                neighbors_string: The string representation of the 3x3 neighbor grid.
                terrain_map: 2D list of TerrainType representing the map.
                x: X coordinate of the tile.
                y: Y coordinate of the tile.
                neighbor_to_sprite_map: List of tuples mapping neighbor strings to sprite types and flips.
            Returns:
                A tuple of (sprite_type, x_terrain_flip, y_terrain_flip) if a resolution is found, else None.
        """
        if len(neighbor_to_sprite_map) != 4 or len(neighbor_to_sprite_map[0]) != 4:
            return None

        if neighbors_string == neighbor_to_sprite_map[0][0] and y < len(terrain_map) - 2 and x < len(terrain_map[0]) - 2:
            if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
                return neighbor_to_sprite_map[0][1:]
                
        elif neighbors_string == neighbor_to_sprite_map[1][0] and y < len(terrain_map) - 2 and x > 1:
            if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
                return neighbor_to_sprite_map[1][1:]

        elif neighbors_string == neighbor_to_sprite_map[2][0] and y > 1 and x < len(terrain_map[0]) - 2:
            if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
                return neighbor_to_sprite_map[2][1:]
        
        elif neighbors_string == neighbor_to_sprite_map[3][0] and y > 1 and x > 1:
            if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
                return neighbor_to_sprite_map[3][1:]
        
        return None
    
    def convert_neighbors_to_string(self, neighbors: list[list[TerrainType]]) -> str:
        """
        Convert the 3x3 neighbor grid to a string representation.
            Parameters:
                neighbors: 3x3 list of TerrainType representing the neighbors.
            Returns:
                A string representation of the neighbors.
        """
        result = ""
        for row in neighbors:
            for terrain in row:
                if terrain == neighbors[1][1]:
                    result += "N"
                else:
                    result += "A"
            result += "\n"
        result = result.strip()
        return result