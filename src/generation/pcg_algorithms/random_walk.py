import random
from typing import List, Tuple, Callable, Optional


def random_walk_paths(
    width: int,
    height: int,
    num_paths: int = 3,
    min_length: int = 20,
    max_length: int = 60,
    is_valid_start: Optional[Callable[[int, int], bool]] = None,
    is_valid_step: Optional[Callable[[int, int], bool]] = None,
    should_stop: Optional[Callable[[int, int], bool]] = None,
) -> List[List[Tuple[int, int]]]:
    """
    Generate multiple random walk paths.
    Generic PCG algorithm usable for rivers and roads.
    http://pcg.wikidot.com/pcg-algorithm:random-walk

    Parameters:
        width, height: map dimensions.
        num_paths: number of paths to generate.
        min_length, max_length: path length range.
        is_valid_start(y, x): function to validate starting cell.
        is_valid_step(y, x): function to validate continuation cell.
        should_stop(y, x): function that decides when to stop early.

    Returns:
        List of paths, each being a list of (y, x) coordinates.
    """

    def in_bounds(y: int, x: int) -> bool:
        return 0 <= y < height and 0 <= x < width

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    paths: List[List[Tuple[int, int]]] = []

    for _ in range(num_paths):
        # pick a valid random start
        for _ in range(50):
            y, x = random.randint(0, height - 1), random.randint(0, width - 1)
            if is_valid_start is None or is_valid_start(y, x):
                break
        else:
            continue  # no valid start found

        path = [(y, x)]
        length_limit = random.randint(min_length, max_length)

        for _ in range(length_limit):
            dy, dx = random.choice(directions)
            ny, nx = y + dy, x + dx

            if not in_bounds(ny, nx):
                break
            if is_valid_step and not is_valid_step(ny, nx):
                break
            if should_stop and should_stop(ny, nx):
                break
            if (ny, nx) in path:
                break

            path.append((ny, nx))
            y, x = ny, nx

        paths.append(path)

    return paths
