from random import randint
from classes.tile.Tile import RoadType
from generation.tile_gen.tile_gen import get_road_sprite_type_range
from generation.tile_gen.roads_gen.road_sprite_dict import road_sprite_mappings

class RoadSpriteHandler():
    def choose_sprite(self, road_map, x, y) -> tuple[int, bool, bool]:
        neighbors = self._get_neighbors(road_map, x, y)
        neighbors_string = self.convert_neighbors_to_string(neighbors)
        if neighbors_string not in road_sprite_mappings:
            print("No matching road sprite type for neighbors string:", neighbors_string, "at position:", (x, y))
            return 1, False, False
        
        sprite_type, x_road_flip, y_road_flip = road_sprite_mappings[neighbors_string]
        
        allowed_sprite_ranges = get_road_sprite_type_range(sprite_type)
        return randint(allowed_sprite_ranges[0], allowed_sprite_ranges[1]), x_road_flip, y_road_flip
                
    def _get_neighbors(self, road_map: list[list[RoadType | None]], x: int, y: int) -> list[list[RoadType | None]]:
        """
        Get the 3x3 grid of neighbors around the tile at (x, y). Handles out-of-bounds by duplicating edge tiles.
            Parameters:
                road_map: 2D list of RoadType | None representing the map.
                x: X coordinate of the tile.
                y: Y coordinate of the tile.
            Returns:
                a 3x3 list of RoadType representing the neighbors.
        """
        neighbors = [[None for _ in range(3)] for _ in range(3)]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(road_map) and 0 <= nx < len(road_map[0]):
                    neighbors[dy + 1][dx + 1] = road_map[ny][nx]

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
    
    def convert_neighbors_to_string(self, neighbors: list[list[RoadType | None]]) -> str:
        """
        Convert the 3x3 neighbor grid to a string representation.
            Parameters:
                neighbors: 3x3 list of RoadType | None representing the neighbors.
            Returns:
                A string representation of the neighbors.
        """
        result = ""
        for row in neighbors:
            for road in row:
                if road == neighbors[1][1]:
                    result += "N"
                else:
                    result += "A"
            result += "\n"
        result = result.strip()
        return result