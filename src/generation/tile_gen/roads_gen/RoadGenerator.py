import random
import heapq
import math
from math import sqrt
from typing import List, Tuple, Optional

from classes.tile.Tile import TerrainType, RoadType


class RoadGenerator:
    """
    Encapsulates the empty-space / road mask generation.
    Use generate() to produce a 2D boolean mask (height x width).
    """
    def __init__(
        self,
        size: int,
        terrain_map: List[List[TerrainType]],
        entry_points: List[Tuple[int,int]],
        occupied_tiles_excluding_landscape: List[List[bool]],
        occupied_tiles_excluding_actionable: List[List[bool]],
        reserve_radius: int = 1
    ) -> None:
        self.width = size
        self.height = size
        self.terrain_map = terrain_map
        self.entry_points = entry_points
        self.occupied_tiles_excluding_landscape = occupied_tiles_excluding_landscape
        self.occupied_tiles_excluding_actionable = occupied_tiles_excluding_actionable
        self.reserve_radius = reserve_radius
        self.restricted_terrain = {TerrainType.WATER, TerrainType.ROCK}
        
        # self.entry_points: List[Tuple[int,int]] = []
        # grid marking of road tiles (RoadType or None)
        self.paths: List[List[RoadType | None]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.shipyard_positions: List[Tuple[int, int]] = []

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable_cell(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and (not self.occupied_tiles_excluding_actionable[y][x])
    
    def can_place_shipyard(self, center_x: int, center_y: int, path_tiles: set[Tuple[int, int]]) -> bool:
        if not (1 <= center_x < self.width - 1 and 1 <= center_y < self.height - 1):
            return False
        
        for dx in [-1, 0, 1]:
            x = center_x + dx
            y = center_y
            if (x, y) not in path_tiles and self.occupied_tiles_excluding_landscape[y][x]:
                return False
        
        has_water_access = False
        for dx in [-1, 0, 1]:
            x = center_x + dx
            if self.in_bounds(x, center_y - 1):
                if self.terrain_map[center_y - 1][x] == TerrainType.WATER:
                    has_water_access = True
                    break
            if self.in_bounds(x, center_y + 1):
                if self.terrain_map[center_y + 1][x] == TerrainType.WATER:
                    has_water_access = True
                    break
        
        return has_water_access
    
    def find_shipyard_placement(self, reference_x: int, reference_y: int, path_tiles: set[Tuple[int, int]], max_search_radius: int = 10) -> Optional[Tuple[int, int]]:
        visited = set()
        queue = [(reference_x, reference_y, 0)]
        visited.add((reference_x, reference_y))
        
        while queue:
            x, y, dist = queue.pop(0)
            
            if dist > max_search_radius:
                break
            
            if self.can_place_shipyard(x, y, path_tiles):
                return (x, y)
            
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))
        
        return None
    
    def _a_star_with_costs(self, start: Tuple[int,int], goal: Tuple[int,int], cost_map: List[List[float]]) -> List[Tuple[int,int]]:
        """A* search using a precomputed per-cell cost_map.

        Returns path as list of (x, y) or empty list if none found.
        """
        if start == goal:
            return [start]

        def heuristic(a: Tuple[int,int], b: Tuple[int,int]) -> int:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_heap: List[Tuple[float, Tuple[int,int]]] = []
        heapq.heappush(open_heap, (heuristic(start, goal), start))
        g_score = {start: 0.0}
        came_from = {}

        # closed set of expanded nodes — prevents re-processing the same node
        closed: set = set()

        # local references for speed inside the loop
        neigh_offsets = [(-1,0),(1,0),(0,-1),(0,1)]
        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in closed:
                continue

            cx, cy = current
            if current == goal: # reached neighbor of goal
                path = [current]
                while path[-1] in came_from:
                    path.append(came_from[path[-1]])
                path.append(start)
                path.reverse()
                return path

            closed.add(current)

            for dx, dy in neigh_offsets:
                nx, ny = cx + dx, cy + dy
                neighbor = (nx, ny)

                # quick bounds + walkable check
                if not self.is_walkable_cell(nx, ny):
                    continue

                # if neighbor already expanded, skip
                if neighbor in closed:
                    continue

                tentative_g = g_score[current] + cost_map[ny][nx]
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (f, neighbor))

        return []

    def find_varied_path(self, start: Tuple[int,int], goal: Tuple[int,int], attempts: int = 6, noise: float = 0.8, curvature_weight: float = 0.5, seed: Optional[int] = None) -> List[Tuple[int,int]]:
        """Find varied path by running A* with randomized per-cell costs multiple times.

        Returns one chosen path (may be more curved / longer than the shortest).
        """
        if start == goal:
            return [start]

        base_seed = seed if seed is not None else (start[0]*73856093 ^ start[1]*19349663 ^ goal[0]*83492791 ^ goal[1]*6700417)
        master_rng = random.Random(base_seed)

        found_paths: List[List[Tuple[int,int]]] = []
        for _ in range(attempts):
            attempt_seed = master_rng.randrange(1 << 30)
            arng = random.Random(attempt_seed)
            # build noise-based cost map
            cost_map: List[List[float]] = [[1.0 + arng.random() * noise for _ in range(self.width)] for _ in range(self.height)]
            path = self._a_star_with_costs(start, goal, cost_map)
            if path:
                found_paths.append(path)

        if not found_paths:
            return []

        # scoring: length + curvature*weight
        def score_path(p: List[Tuple[int,int]]) -> float:
            L = len(p)
            total_angle = 0.0
            if L >= 3:
                prev = p[0]
                cur = p[1]
                prev_ang = math.atan2(cur[1]-prev[1], cur[0]-prev[0])
                for i in range(2, L):
                    nxt = p[i]
                    ang = math.atan2(nxt[1]-cur[1], nxt[0]-cur[0])
                    total_angle += abs(ang - prev_ang)
                    prev_ang = ang
                    prev, cur = cur, nxt
            return L + curvature_weight * total_angle

        shortest_len = min(len(p) for p in found_paths)
        candidates = [p for p in found_paths if len(p) <= shortest_len * 4]
        if not candidates:
            candidates = found_paths

        best = max(candidates, key=score_path)
        return best
    
    def get_paths_endpoints_with_mst(self, points: List[Tuple[int, int]]) -> List[Tuple[Tuple[int,int], Tuple[int,int]]]:
        """
        Return list of edges connecting all points with minimal total distance using MST (Prim's algorithm).
        """
        adj_list = [[] for _ in points]

        for i, (x1, y1) in enumerate(points):
            for j, (x2, y2) in enumerate(points):
                if x1!=x2 or y1!=y2:
                    adj_list[i].append((j, sqrt((x1-x2)**2 + (y1-y2)**2)))

        if not points:
            return []

        visited = {0}
        paths_endpoints: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        
        edge_heap = []
        for other_node_idx, edge_len in adj_list[0]:
            heapq.heappush(edge_heap, (edge_len, 0, other_node_idx)) # change order to sort by edge_len

        while len(visited) < len(points):
            edge_len, node_idx, other_node_idx = heapq.heappop(edge_heap)
            if other_node_idx not in visited:
                visited.add(other_node_idx)
                paths_endpoints.append((points[node_idx], points[other_node_idx]))
                for on, e in adj_list[other_node_idx]:
                    heapq.heappush(edge_heap, (e, other_node_idx, on))

        return paths_endpoints
    
    def generate(self) -> List[List[RoadType | None]]:

        if len(self.entry_points) < 2:
            print(f"Not enough entry points to generate roads: {self.entry_points}")
            return self.paths

        print(f"Entry points (x,y): {self.entry_points}")
        paths_endpoints = self.get_paths_endpoints_with_mst(self.entry_points)

        # For each MST edge, compute a varied path and mark it in the grid
        for a, b in paths_endpoints:
            road_type = random.choice(list(RoadType))
            # road_type = RoadType.GRAVEL #! useful for testing, if you think a road didn't generate, use this!
            path = self.find_varied_path(a, b, attempts=6, noise=0.8, curvature_weight=0.5)
            print(f"Generated road path from {a} to {b}, path: {path}")
            if not path:
                continue
            
            path_tiles = set(path)
            
            in_water_section = False
            
            for i, (x, y) in enumerate(path):
                if self.is_walkable_cell(x, y):
                    self.occupied_tiles_excluding_landscape[y][x] = True
                    
                    current_is_water = self.terrain_map[y][x] == TerrainType.WATER
                    
                    if current_is_water and not in_water_section:
                        if i > 0:
                            prev_x, prev_y = path[i-1]
                            if self.terrain_map[prev_y][prev_x] != TerrainType.WATER:
                                shipyard_pos = self.find_shipyard_placement(prev_x, prev_y, path_tiles)
                                if shipyard_pos:
                                    if shipyard_pos not in self.shipyard_positions:
                                        self.shipyard_positions.append(shipyard_pos)
                                        # print(f"  Found shipyard placement at {shipyard_pos} for entering water from ({prev_x},{prev_y})")
                                else:
                                    print(f"  WARNING: Could not find shipyard placement near ({prev_x},{prev_y}) for water entry")
                        in_water_section = True
                    
                    elif not current_is_water and in_water_section:
                        shipyard_pos = self.find_shipyard_placement(x, y, path_tiles)
                        if shipyard_pos:
                            if shipyard_pos not in self.shipyard_positions:
                                self.shipyard_positions.append(shipyard_pos)
                                # print(f"  Found shipyard placement at {shipyard_pos} for exiting water at ({x},{y})")
                        else:
                            print(f"  WARNING: Could not find shipyard placement near ({x},{y}) for water exit")
                        in_water_section = False
                    
                    if self.terrain_map[y][x] in self.restricted_terrain:
                        self.paths[y][x] = RoadType.NONE
                    else: self.paths[y][x] = road_type

        return self.paths
        