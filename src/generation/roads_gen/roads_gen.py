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
        objects: List,
        # entry_points: List[Tuple[int,int]],
        occupied_tiles: List[List[bool]],
        reserve_radius: int = 1
    ) -> None:
        self.width = size
        self.height = size
        self.terrain_map = terrain_map
        self.objects = objects 
        # self.entry_points = entry_points
        self.occupied_tiles = occupied_tiles
        self.reserve_radius = reserve_radius
        self.avoid_terrain = {TerrainType.WATER, TerrainType.ROCK}
        
        self.entry_points: List[Tuple[int,int]] = []
        # grid marking of road tiles (RoadType or None)
        self.paths: List[List[RoadType | None]] = [[None for _ in range(self.width)] for _ in range(self.height)]
        # list of found path coordinate lists
        self.paths_list: List[List[Tuple[int,int]]] = []

    def in_bounds(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_walkable_cell(self, y: int, x: int) -> bool:
        return self.in_bounds(y, x) and (self.terrain_map[y][x] not in self.avoid_terrain) # and (not self.occupied_tiles[y][x])

    def _a_star_with_costs(self, start: Tuple[int,int], goal: Tuple[int,int], cost_map: List[List[float]]) -> List[Tuple[int,int]]:
        """A* search using a precomputed per-cell `cost_map`.

        Returns path as list of (y,x) or empty list if none found.
        """
        if start == goal:
            return [start]

        def heuristic(a: Tuple[int,int], b: Tuple[int,int]) -> int:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_heap: List[Tuple[float, Tuple[int,int]]] = []
        heapq.heappush(open_heap, (heuristic(start, goal), start))
        g_score = {start: 0.0}
        came_from = {}

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current == goal:
                # reconstruct
                path = [current]
                while path[-1] in came_from:
                    path.append(came_from[path[-1]])
                path.reverse()
                return path

            cy, cx = current
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = cy + dy, cx + dx
                neighbor = (ny, nx)
                if not self.is_walkable_cell(ny, nx):
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
                prev_ang = math.atan2(cur[0]-prev[0], cur[1]-prev[1])
                for i in range(2, L):
                    nxt = p[i]
                    ang = math.atan2(nxt[0]-cur[0], nxt[1]-cur[1])
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
    
    def get_paths_endpoints_with_mst(self, points: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """
        Return list of edges connecting all points with minimal total distance using MST (Prim's algorithm).
        """
        adj_list = [[] for _ in points]

        for i, (x1, y1) in enumerate(points):
            for j, (x2, y2) in enumerate(points):
                if x1!=x2 or y1!=y2:
                    adj_list[i].append((j, sqrt((x1-x2)**2 + (y1-y2)**2)))

        visited = {0}
        paths_endpoints: List[List[Tuple[int, int]]] = []
        
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
        # collect entry points
        self.entry_points = []
        for obj in self.objects:
            self.entry_points.append((obj.y, obj.x))

        # build MST edges between entry points
        print(f"Entry points: {self.entry_points}")
        paths_endpoints = self.get_paths_endpoints_with_mst(self.entry_points)

        # For each MST edge, compute a varied path and mark it in the grid
        for a, b in paths_endpoints:
            path = self.find_varied_path(a, b, attempts=6, noise=0.8, curvature_weight=0.5)
            print(f"Generated road path from {a} to {b}, path: {path}")
            if not path:
                continue
            self.paths_list.append(path)
            for y, x in path:
                if self.is_walkable_cell(y, x):
                    self.paths[y][x] = RoadType.GRAVEL

        return self.paths
        