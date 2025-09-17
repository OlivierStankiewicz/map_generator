from typing import List, Dict, Tuple

from classes.tile.Tile import TerrainType

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