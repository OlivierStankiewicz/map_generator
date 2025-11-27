# ...existing code...
from typing import List, Tuple, Optional
from classes.Objects.Objects import Objects
import math
import random

from classes.tile.Tile import TerrainType

class EmptySpacesGenerator:
    """
    Encapsulates the empty-space / road mask generation.
    Use generate() to produce a 2D boolean mask (height x width).
    """
    def __init__(
        self,
        size: int,
        terrain_map: List[List[TerrainType]],
        objects: List[Objects],
        reserve_radius: int = 1
    ) -> None:
        self.width = size
        self.height = size
        self.terrain_map = terrain_map
        self.objects = objects
        self.reserve_radius = reserve_radius
        self.avoid_terrain = {TerrainType.WATER, TerrainType.ROCK}

    def in_bounds(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_walkable_cell(self, y: int, x: int) -> bool:
        return self.in_bounds(y, x) and (self.terrain_map[y][x] not in self.avoid_terrain)

    def reserve_cell(self, mask: List[List[bool]], y: int, x: int) -> None:
        for dy in range(-self.reserve_radius, self.reserve_radius + 1):
            for dx in range(-self.reserve_radius, self.reserve_radius + 1):
                ny, nx = y + dy, x + dx
                if self.in_bounds(ny, nx) and (self.terrain_map[ny][nx] not in self.avoid_terrain):
                    mask[ny][nx] = True

    def deterministic_rand(self, a: Tuple[int,int], b: Tuple[int,int]) -> float:
        seed = (a[0] * 73856093) ^ (a[1] * 19349663) ^ (b[0] * 83492791) ^ (b[1] * 6700417)
        r = random.Random(seed)
        return r.uniform(-1.0, 1.0)

    def find_nearest_walkable(self, yf: int, xf: int, max_r: int = 2) -> Optional[Tuple[int,int]]:
        if self.is_walkable_cell(yf, xf):
            return (yf, xf)
        for r in range(1, max_r + 1):
            for dy in range(-r, r + 1):
                dx = r - abs(dy)
                for sx in (-1, 1):
                    nx = xf + sx * dx
                    ny = yf + dy
                    if self.in_bounds(ny, nx) and self.is_walkable_cell(ny, nx):
                        return (ny, nx)
            for dx in range(-r, r + 1):
                for dy in (-r, r):
                    ny = yf + dy
                    nx = xf + dx
                    if self.in_bounds(ny, nx) and self.is_walkable_cell(ny, nx):
                        return (ny, nx)
        return None

    def rasterize_quadratic(
        self,
        p0: Tuple[int,int],
        pc: Tuple[float,float],
        p1: Tuple[int,int]
    ) -> List[Tuple[int,int]]:
        (y0, x0), (y1, x1) = p0, p1
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        samples = max(4, int(dist * 2.0))
        cells: List[Tuple[int,int]] = []
        for i in range(samples + 1):
            t = i / samples
            bx = (1 - t)**2 * x0 + 2 * (1 - t) * t * pc[1] + t**2 * x1
            by = (1 - t)**2 * y0 + 2 * (1 - t) * t * pc[0] + t**2 * y1
            gx = int(round(bx))
            gy = int(round(by))
            found = self.find_nearest_walkable(gy, gx, max_r=2)
            if found is not None:
                cells.append(found)
        seen = set()
        out: List[Tuple[int,int]] = []
        for c in cells:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return out

    def generate(self) -> List[List[bool]]:
        # collect entry points
        entry_points: List[Tuple[int,int]] = []
        for obj in self.objects:
            try:
                pt = (obj.y, obj.x)
            except Exception:
                continue
            if self.in_bounds(pt[0], pt[1]):
                entry_points.append(pt)

        mask = [[False for _ in range(self.width)] for _ in range(self.height)]
        if not entry_points:
            return mask

        for py, px in entry_points:
            self.reserve_cell(mask, py, px)

        n = len(entry_points)
        if n <= 1:
            return mask

        pts = entry_points
        in_mst = [False] * n
        min_dist = [float("inf")] * n
        parent = [-1] * n
        min_dist[0] = 0.0

        for _ in range(n):
            u = -1
            best = float("inf")
            for i in range(n):
                if not in_mst[i] and min_dist[i] < best:
                    best = min_dist[i]
                    u = i
            if u == -1:
                break
            in_mst[u] = True
            uy, ux = pts[u]
            for v in range(n):
                if in_mst[v]:
                    continue
                vy, vx = pts[v]
                d2 = (uy - vy) ** 2 + (ux - vx) ** 2
                if d2 < min_dist[v]:
                    min_dist[v] = d2
                    parent[v] = u

        edges: List[Tuple[Tuple[int,int], Tuple[int,int]]] = []
        for v in range(n):
            if parent[v] != -1:
                edges.append((pts[v], pts[parent[v]]))

        curvature = 0.18
        for a, b in edges:
            ay, ax = a
            by, bx = b
            mx = (ax + bx) / 2.0
            my = (ay + by) / 2.0
            vx = bx - ax
            vy = by - ay
            length = math.hypot(vx, vy)
            if length == 0:
                continue
            px = -vy / length
            py = vx / length
            sign = self.deterministic_rand(a, b)
            magnitude = length * curvature * sign
            control = (my + py * magnitude, mx + px * magnitude)
            raster_cells = self.rasterize_quadratic(a, control, b)
            for cy, cx in raster_cells:
                self.reserve_cell(mask, cy, cx)

        return mask