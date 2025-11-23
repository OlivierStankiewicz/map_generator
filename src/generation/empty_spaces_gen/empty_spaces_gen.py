from typing import List, Tuple, Optional
from classes.Objects.Objects import Objects
import math
import random

from classes.tile.Tile import TerrainType

class EmptySpacesGenerator:
    """
    Encapsulates the empty-space / road mask generation.
    Use generate() to produce a 2D boolean mask (height x width).

    Tunables:
    - extra_edge_prob: probability to add a non-MST edge (deterministic per-edge).
    - extra_edge_k: consider up to k nearest neighbors per point as extra edge candidates.
    - road widths are chosen deterministically between 1 and 4.
    """
    def __init__(
        self,
        size: int,
        terrain_map: List[List[TerrainType]],
        objects: List[Objects],
        reserve_radius: int = 1,
        extra_edge_prob: float = 0.12,
        extra_edge_k: int = 3
    ) -> None:            
        self.height = size
        self.width = size
        self.terrain_map = terrain_map
        self.objects = objects
        self.reserve_radius = reserve_radius
        self.extra_edge_prob = max(0.0, min(1.0, extra_edge_prob))
        self.extra_edge_k = max(0, extra_edge_k)
        self.avoid_terrain = {TerrainType.WATER, TerrainType.ROCK}

    def in_bounds(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_walkable_cell(self, y: int, x: int) -> bool:
        return self.in_bounds(y, x) and (self.terrain_map[y][x] not in self.avoid_terrain)

    def reserve_cell(self, mask: List[List[bool]], y: int, x: int, width: Optional[int] = None) -> None:
        """
        Reserve a square area centered at (y,x). 'width' is half-size (0 => single cell).
        If width is None, fall back to self.reserve_radius.
        """
        w = self.reserve_radius if width is None else max(0, int(width))
        for dy in range(-w, w + 1):
            for dx in range(-w, w + 1):
                ny, nx = y + dy, x + dx
                if self.in_bounds(ny, nx) and (self.terrain_map[ny][nx] not in self.avoid_terrain):
                    mask[ny][nx] = True

    def deterministic_rand(self, a: Tuple[int,int], b: Tuple[int,int]) -> float:
        # deterministic pseudorandom in [-1,1] based on coords
        seed = (a[0] * 73856093) ^ (a[1] * 19349663) ^ (b[0] * 83492791) ^ (b[1] * 6700417)
        r = random.Random(seed)
        return r.uniform(-1.0, 1.0)

    def deterministic_width_for_edge(self, a: Tuple[int,int], b: Tuple[int,int]) -> int:
        """
        Deterministically choose a width between 1 and 4 (inclusive) for an edge.
        """
        # low, high = 1, 2
        # r = self.deterministic_rand(a, b)  # [-1,1]
        # frac = (r + 1.0) / 2.0  # [0,1]
        # # map to integer in [low, high]
        # val = low + int(frac * (high - low + 1))
        # return max(low, min(high, val))
        return 0
        
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
            # attempt to snap, but allow a slightly larger search to increase success
            found = self.find_nearest_walkable(gy, gx, max_r=3)
            if found is not None:
                cells.append(found)
        # remove duplicates while preserving order
        seen = set()
        out: List[Tuple[int,int]] = []
        for c in cells:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return out

    def _add_extra_edges(self, edges: List[Tuple[Tuple[int,int], Tuple[int,int]]], pts: List[Tuple[int,int]]) -> None:
        """
        Add a small number of extra edges (non-MST) between nearby points to increase passability.
        Selection is deterministic per-edge using deterministic_rand and self.extra_edge_prob.
        We consider up to extra_edge_k nearest neighbors per point and add edges with low probability.
        """
        n = len(pts)
        if n <= 1 or self.extra_edge_k <= 0 or self.extra_edge_prob <= 0.0:
            return

        # existing edge set for quick lookup (undirected)
        existing = set()
        for a, b in edges:
            if a <= b:
                existing.add((a, b))
            else:
                existing.add((b, a))

        # compute neighbors for each point
        for i, p in enumerate(pts):
            # distances to others
            dists = []
            py, px = p
            for j, q in enumerate(pts):
                if i == j:
                    continue
                qy, qx = q
                d2 = (py - qy) ** 2 + (px - qx) ** 2
                dists.append((d2, j))
            dists.sort(key=lambda t: t[0])
            # consider up to k nearest neighbors
            for _, j in dists[:self.extra_edge_k]:
                a = p
                b = pts[j]
                edge_key = (a, b) if a <= b else (b, a)
                if edge_key in existing:
                    continue
                # deterministic chance
                r = self.deterministic_rand(a, b)
                frac = (r + 1.0) / 2.0
                if frac < self.extra_edge_prob:
                    # add this extra edge
                    edges.append((a, b))
                    existing.add(edge_key)
                    # keep degree moderate: if too many edges added overall, stop early
                    # (small guard: break if edges exceed 2*n)
                    if len(existing) > 2 * n:
                        return

    def generate_empty_spaces(self) -> List[List[bool]]:
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

        # reserve entries using deterministic width 1..4
        for py, px in entry_points:
            ew = self.deterministic_width_for_edge((py, px), (py, px))
            self.reserve_cell(mask, py, px, width=ew)

        n = len(entry_points)
        if n <= 1:
            return mask

        pts = entry_points
        # build Euclidean MST (Prim)
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

        # add a few extra edges between nearby points (deterministic)
        self._add_extra_edges(edges, pts)

        # draw each edge as a curved road and reserve cells (width 1..4 deterministic per-edge)
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
            px_dir = -vy / length
            py_dir = vx / length
            sign = self.deterministic_rand(a, b)
            magnitude = length * curvature * sign
            control = (my + py_dir * magnitude, mx + px_dir * magnitude)
            raster_cells = self.rasterize_quadratic(a, control, b)

            edge_w = self.deterministic_width_for_edge(a, b)  # width between 1 and 4
            for cy, cx in raster_cells:
                self.reserve_cell(mask, cy, cx, width=edge_w)

        return mask
