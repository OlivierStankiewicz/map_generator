from typing import List, Dict, Tuple

from classes.tile.Tile import TerrainType
from generation.tile_gen.tile_gen import SpriteType, SpriteTypeRock, get_terrain_type_sprite_type_range
from generation.map_gen.sprite_type_dict import dirt_based_terrain_sprite_mappings
from generation.map_gen.sprite_type_water import water_sprite_mappings
from generation.map_gen.sprite_type_dirt import dirt_sprite_mappings
from generation.map_gen.sprite_type_rock import rock_sprite_mappings

sprite_type_dict: Dict[str, Tuple[SpriteType, bool, bool]]

from random import randint

def print_map(terrain_map: List[List[TerrainType]]):
    """
    Print the terrain map in a readable format.
    """
    height = len(terrain_map)
    width = len(terrain_map[0]) if height > 0 else 0

    # print column headers
    header = "    " + " ".join(f"{x:2}" for x in range(width))
    print(header)
    print("   " + "-" * (3 * width))

    for y, row in enumerate(terrain_map):
        row_str = " ".join(t.name[0] if t else '.' for t in row)
        print(f"{y:2} | {row_str}")
        
def smooth_map(terrain_map: List[List[TerrainType]]) -> List[List[TerrainType]]:
    """
    Smooth terrain borders by majority voting among neighbors.
    """
    height = len(terrain_map)
    width = len(terrain_map[0])
    
    # print_map(terrain_map)
    
    def in_bounds(y: int, x: int) -> bool:
        """
        Check if (y, x) is within map bounds.
        """
        return 0 <= y < height and 0 <= x < width
    
    def is_part_of_valid_block(y, x, terr_map: List[List[TerrainType]]) -> bool:
        """
        Check if the tile at (y, x) is part of a 2x2 block of the same terrain type.
        """
        candidates = [
            [(y, x), (y+1, x), (y, x+1), (y+1, x+1)],  # top-left
            [(y, x), (y-1, x), (y, x+1), (y-1, x+1)],  # bottom-left
            [(y, x), (y+1, x), (y, x-1), (y+1, x-1)],  # top-right
            [(y, x), (y-1, x), (y, x-1), (y-1, x-1)],  # bottom-right
        ]
        terrain_type = terr_map[y][x]
        for block in candidates:
            # check if all coordinates are in bounds
            if not all(in_bounds(yy, xx) for yy, xx in block):
                continue
            
            if all(terr_map[yy][xx] == terrain_type for yy, xx in block):
                return True
            
        return False
    
    def get_corner(y: int, x: int, terr_map: List[List[TerrainType]]) -> Dict[str, List[Tuple[int, int]]] | None:
        """
        Check if the tile at (y, x) is in a corner position. If yes, return its coordinates, else None.
        """
        corners = [
            {"different": [(y-1, x-1), (y, x-1), (y+1, x-1), (y+1, x), (y+1, x+1)], "same": [(y-1, x), (y-1, x+1), (y, x+1)]}, # left and upper edge
            {"different": [(y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1)], "same": [(y, x-1), (y-1, x-1), (y-1, x)]}, # right and upper edge
            {"different": [(y+1, x-1), (y, x-1), (y-1, x-1), (y-1, x), (y-1, x+1)], "same": [(y+1, x), (y+1, x+1), (y, x+1)]}, # left and bottom edge
            {"different": [(y+1, x+1), (y, x+1), (y-1, x+1), (y-1, x), (y-1, x-1)], "same": [(y, x-1), (y+1, x-1), (y+1, x)]}  # right and bottom edge
        ]
        
        terrain = terr_map[y][x]
        for corner in corners:
            same_coords = corner["same"]
            diff_coords = corner["different"]
            
            # check if all coordinates are in bounds
            if not all(in_bounds(yy, xx) for yy, xx in same_coords + diff_coords):
                continue
            
            # all "same" must equal candidate
            if not all(terr_map[yy][xx] == terrain for yy, xx in same_coords):
                continue
            
            # all "different" must be != candidate, but also be of the same type
            diff_types = {terr_map[yy][xx] for yy, xx in diff_coords}
            if len(diff_types) == 1 and terrain not in diff_types:
                return corner
            
        return None
                    
    new_map = [[terrain_map[y][x] for x in range(width)] for y in range(height)]
    
    for y in range(height):
        for x in range(width):
            corner = get_corner(y, x, new_map)
            if corner is None:
                continue
            
            old_terrain = new_map[y][x]
            # set new terrain
            sy, sx = corner["different"][0]
            new_terrain = new_map[sy][sx]
            new_map[y][x] = new_terrain
            
            same_coords = corner["same"]
            for dy, dx in same_coords:
                if not is_part_of_valid_block(dy, dx, new_map):
                    new_map[y][x] = old_terrain # revert to the previous terrain type if change would break a valid block
                    break
                    
    return new_map

def upscale_map(terrain_map: List[List[TerrainType]]) -> List[List[TerrainType]]:
    """
    Upscale a map so that every tile expands to a 2x2 block of the same terrain type.
    """
    print("Before upscaling:")
    print_map(terrain_map)
    height = len(terrain_map)
    width = len(terrain_map[0])
    upscaled_map = [[None for _ in range(width * 2)] for _ in range(height * 2)]

    for y in range(height):
        for x in range(width):
            terrain_type = terrain_map[y][x]
            upscaled_map[2*y][2*x] = terrain_type
            upscaled_map[2*y][2*x + 1] = terrain_type
            upscaled_map[2*y + 1][2*x] = terrain_type
            upscaled_map[2*y + 1][2*x + 1] = terrain_type

    print("After upscaling:")
    print_map(upscaled_map)
    
    return upscaled_map

def choose_sprite(terrain_map, x, y) -> Tuple[int, bool, bool]:
    """
    Choose an appropriate sprite number for the tile at (x, y) based on its neighbors.
    Returns a tuple of (
        sprite_number - number of the chosen sprite,
        x_terrain - whether the sprite needs to be flipped in x direction (flag terrain_x)
        y_terrain - whether the sprite needs to be flipped in y direction (flag terrain_y
    ).
    """
    terrain_type = terrain_map[y][x]
    sprite, x_terrain_flip, y_terrain_flip = 1, False, False
    
    # handle dirt sprites
    if terrain_type == TerrainType.DIRT:
        neighbors = get_neighbors(terrain_map, x, y)
        neighbors_string = convert_dirt_neighbors_to_string(neighbors)
        
        sand_inner_corner_conflicting = ["NNN\nNNN\nNNX", "NNN\nNNN\nXNN", "NNX\nNNN\nNNN", "XNN\nNNN\nNNN"]
        if neighbors_string in sand_inner_corner_conflicting:
            conflict_resolution = resolve_sand_inner_corner_conflict(neighbors_string, terrain_map, x, y)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
            else:
                sprite_type, x_terrain_flip, y_terrain_flip = dirt_sprite_mappings[neighbors_string]
        else:
            sprite_type, x_terrain_flip, y_terrain_flip = dirt_sprite_mappings[neighbors_string]

        allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
            sprite = randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1])
        else:
            sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])
        
        return sprite, x_terrain_flip, y_terrain_flip
    
    # handle sand sprites
    if terrain_type == TerrainType.SAND:
        sprite_type = SpriteType.CENTER
        x_terrain_flip = False
        y_terrain_flip = False
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1: # 10% chance to pick a special sprite (rare one)
            sprite = randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1])
        else:
            sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])

        return sprite, x_terrain_flip, y_terrain_flip

    # handle water sprites
    if terrain_type == TerrainType.WATER:
        neighbors = get_neighbors(terrain_map, x, y)
        neighbors_string = convert_water_neighbors_to_string(neighbors)
        
        sand_inner_corner_conflicting = ["NNN\nNNN\nNNA", "NNN\nNNN\nANN", "NNA\nNNN\nNNN", "ANN\nNNN\nNNN"]
        if neighbors_string in sand_inner_corner_conflicting:
            conflict_resolution = resolve_sand_inner_corner_conflict_water(neighbors_string, terrain_map, x, y)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
            else:
                sprite_type, x_terrain_flip, y_terrain_flip = water_sprite_mappings[neighbors_string]
        else:
            sprite_type, x_terrain_flip, y_terrain_flip = water_sprite_mappings[neighbors_string]
        
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
        sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])
        
        return sprite, x_terrain_flip, y_terrain_flip

    # handle rock sprites
    if terrain_type == TerrainType.ROCK:
        neighbors = get_neighbors(terrain_map, x, y)
        neighbors_string = convert_water_neighbors_to_string(neighbors)
       
        inner_corner_conflicting = ["NNN\nNNN\nNNA", "NNN\nNNN\nANN", "NNA\nNNN\nNNN", "ANN\nNNN\nNNN"]
        if neighbors_string in inner_corner_conflicting:
            print("Rock inner corner conflict at:", (x, y))
            conflict_resolution = resolve_sand_inner_corner_conflict_rock(neighbors_string, terrain_map, x, y)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
            else:
                sprite_type, x_terrain_flip, y_terrain_flip = rock_sprite_mappings[neighbors_string]
        else:
            sprite_type, x_terrain_flip, y_terrain_flip = rock_sprite_mappings[neighbors_string]
        
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
        sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])
        
        return sprite, x_terrain_flip, y_terrain_flip
    
    # handle dirt based terrain sprites
    neighbors = get_neighbors(terrain_map, x, y)
    neighbors_string = convert_neighbors_to_string(neighbors)

    # handle sand inner corner conflict resolution
    sand_inner_corner_conflicting = ["NNN\nNNN\nNNX", "NNN\nNNN\nXNN", "NNX\nNNN\nNNN", "XNN\nNNN\nNNN"]
    if neighbors_string in sand_inner_corner_conflicting:
        conflict_resolution = resolve_sand_inner_corner_conflict(neighbors_string, terrain_map, x, y)
        if conflict_resolution:
            sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
            allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
            if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
                sprite = randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1])
            else:
                sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])
            return sprite, x_terrain_flip, y_terrain_flip

    # handle dirt inner corner conflict resolution
    dirt_inner_corner_conflicting = ["NNN\nNNN\nNNY", "NNN\nNNN\nYNN", "NNY\nNNN\nNNN", "YNN\nNNN\nNNN"]
    if neighbors_string in dirt_inner_corner_conflicting:
        conflict_resolution = resolve_dirt_inner_corner_conflict(neighbors_string, terrain_map, x, y)
        if conflict_resolution:
            sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
            allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
            if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
                sprite = randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1])
            else:
                sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])
            return sprite, x_terrain_flip, y_terrain_flip

    # print("Neighbors string:", neighbors_string)
    if neighbors_string not in dirt_based_terrain_sprite_mappings:
        print("No matching sprite type for neighbors string:", neighbors_string, "at position:", (x, y))
        return 1, False, False

    sprite_entry = dirt_based_terrain_sprite_mappings[neighbors_string]
    sprite_type, x_terrain_flip, y_terrain_flip = sprite_entry
    
    allowed_sprite_ranges = get_terrain_type_sprite_type_range(terrain_type, sprite_type)
    if allowed_sprite_ranges["special"] and randint(1, 10) == 1: # 10% chance to pick a special sprite (rare one)
        sprite = randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1])
    else:
        sprite = randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1])

    return sprite, x_terrain_flip, y_terrain_flip

def get_neighbors(terrain_map: List[List[TerrainType]], x: int, y: int) -> List[List[TerrainType]]:
    """
    Get the 3x3 grid of neighbors around the tile at (x, y).
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

def convert_neighbors_to_string(neighbors: list[list[TerrainType]]) -> str:
    sand_group = {TerrainType.SAND, TerrainType.ROCK, TerrainType.WATER}

    result = ""
    for row in neighbors:
        for terrain in row:
            if terrain == neighbors[1][1]:
                result += "N"
            elif terrain in sand_group:
                result += "X"
            else:
                result += "Y"
        result += "\n"
    result = result.strip()
    return result

def convert_water_neighbors_to_string(neighbors: list[list[TerrainType]]) -> str:
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

def convert_dirt_neighbors_to_string(neighbors: list[list[TerrainType]]) -> str:
    sand_group = {TerrainType.SAND, TerrainType.ROCK, TerrainType.WATER}
    result = ""
    for row in neighbors:
        for terrain in row:
            if terrain in sand_group:
                result += "X"
            else:
                result += "N"
        result += "\n"
    result = result.strip()
    return result

def resolve_sand_inner_corner_conflict(neighbors_string: str, terrain_map: list[list[TerrainType]], x, y) -> tuple[SpriteType, bool, bool] | None:
    if neighbors_string == "NNN\nNNN\nNNX" and y < len(terrain_map) - 2 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, False, False
            
    elif neighbors_string == "NNN\nNNN\nXNN" and y < len(terrain_map) - 2 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, True, False

    elif neighbors_string == "NNX\nNNN\nNNN" and y > 1 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, False, True
    
    elif neighbors_string == "XNN\nNNN\nNNN" and y > 1 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, True, True

    return None

def resolve_sand_inner_corner_conflict_water(neighbors_string: str, terrain_map: list[list[TerrainType]], x, y) -> tuple[SpriteType, bool, bool] | None:
    if neighbors_string == "NNN\nNNN\nNNA" and y < len(terrain_map) - 2 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, False, False
            
    elif neighbors_string == "NNN\nNNN\nANN" and y < len(terrain_map) - 2 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, True, False

    elif neighbors_string == "NNA\nNNN\nNNN" and y > 1 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, False, True
    
    elif neighbors_string == "ANN\nNNN\nNNN" and y > 1 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.SAND_INNER_CORNER, True, True

    return None

def resolve_sand_inner_corner_conflict_rock(neighbors_string: str, terrain_map: list[list[TerrainType]], x, y) -> tuple[SpriteType, bool, bool] | None:
    if neighbors_string == "NNN\nNNN\nNNA" and y < len(terrain_map) - 2 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            print("Resolved to UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER")
            return SpriteTypeRock.UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False
            
    elif neighbors_string == "NNN\nNNN\nANN" and y < len(terrain_map) - 2 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            print("Resolved to UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER")
            return SpriteTypeRock.UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False

    elif neighbors_string == "NNA\nNNN\nNNN" and y > 1 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            print("Resolved to LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER")
            return SpriteTypeRock.LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False
    
    elif neighbors_string == "ANN\nNNN\nNNN" and y > 1 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            print("Resolved to LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER")
            return SpriteTypeRock.LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER, False, False
    return None

def resolve_dirt_inner_corner_conflict(neighbors_string: str, terrain_map: list[list[TerrainType]], x, y) -> tuple[SpriteType, bool, bool] | None:
    if neighbors_string == "NNN\nNNN\nNNY" and y < len(terrain_map) - 2 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.DIRT_INNER_CORNER, False, False
            
    elif neighbors_string == "NNN\nNNN\nYNN" and y < len(terrain_map) - 2 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y+2][x] == terrain_map[y][x]:
            return SpriteType.DIRT_INNER_CORNER, True, False

    elif neighbors_string == "NNY\nNNN\nNNN" and y > 1 and x < len(terrain_map[0]) - 2:
        if terrain_map[y][x+2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.DIRT_INNER_CORNER, False, True
    
    elif neighbors_string == "YNN\nNNN\nNNN" and y > 1 and x > 1:
        if terrain_map[y][x-2] == terrain_map[y][x] and terrain_map[y-2][x] == terrain_map[y][x]:
            return SpriteType.DIRT_INNER_CORNER, True, True

    return None