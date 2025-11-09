from generation.tile_gen.tile_gen import SpriteType

# Auto-generated tile pattern dictionary builder

from typing import Dict, Tuple

# Assume SpriteType enum is defined elsewhere and imported when using this module.
dirt_based_terrain_types_patterns = {
    # SAND_OUTER_CORNER
    r"""
    XXX
    XNN
    XNN
    """
    : (SpriteType.DIRT_OUTER_CORNER, False, False),
    r"""
    XXX
    NNX
    NNX
    """
    : (SpriteType.DIRT_OUTER_CORNER, False, True),
    r"""
    XNN
    XNN
    XXX
    """
    : (SpriteType.DIRT_OUTER_CORNER, True, False),
    r"""
    NNX
    NNX
    XXX
    """
    : (SpriteType.DIRT_OUTER_CORNER, True, True),
    
    
}

_raw_definitions = r"""
SAND_OUTER_CORNER
X X X
X N N
X N N
x: 0, y: 0

X X X
N N X
N N X
x: 0, y: 1

X N N
X N N
X X X
x: 1, y: 0

N N X
N N X
X X X
x: 1, y: 1
*****************
SAND_EDGE_VERTICAL
N N X
N N X
N N X
x: 0, y: 0

X N N
X N N
X N N
x: 0, y: 1
*****************
SAND_EDGE_HORIZONTAL
X X X
N N N
N N N
x: 0, y: 1

N N N
N N N
X X X
x: 0, y: 1
*****************
SAND_INNER_CORNER
N N N
N N N
N N X

X N N
N N N
N N N

N N X
N N N
N N N

N N N
N N N
X N N
*****************
SAND_OUTER_CORNER_NEXT_TO_HALF_WATER
X X N
X N N
N N N

N X X
N N X
N N N

N N N
X N N
X X N

N N N
N N X
N X X
*****************
SAND_CONNECTOR
X N N
N N N
N N X

N N X
N N N
X N N
*****************
CENTER
N N N
N N N
N N N
*****************
SAND
N N X
X N N
X X N

N X X
N N X
X N N

X N N
N N X
N X X

X X N
X N N
N N X
*****************
DIRT_OUTER_CORNER
Y N N
Y N N
Y Y Y

Y Y Y
Y Y Y
Y Y Y

Y Y Y
N N Y
N N Y

Y Y Y
Y N N
Y N N
*****************
DIRT_EDGE_VERTICAL
N N Y
N N Y
N N Y

Y N N
Y N N
Y N N
*****************
DIRT_EDGE_HORIZONTAL
Y Y Y
N N N
N N N

N N N
N N N
Y Y Y
*****************
DIRT_INNER_CORNER
N N N
N N N
N N Y

Y N N
N N N
N N N

N N Y
N N N
N N N

N N N
N N N
Y N N
*****************
DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER
Y Y N
Y N N
N N N

N N N
Y N N
Y Y N

N Y Y
N N Y
N N N

N N N
N N Y
N Y Y
*****************
DIRT_CONNECTOR
Y N N
N N N
N N Y

N N Y
N N N
Y N N
*****************
DIRT
N N Y
Y N N
Y Y N

N Y Y
N N Y
Y N N

Y N N
N N Y
N Y Y

Y Y N
Y N N
N N Y
*****************
MIXED_CONNECTOR
X N N
N N N
N N Y

Y N N
N N N
N N X

N N X
N N N
Y N N

N N Y
N N N
X N N
*****************
MIXED_OUTER_CORNER_VERTICAL_SAND
N N X
N N X
Y Y A

X N N
X N N
A Y Y

Y Y A
N N X
N N X

A Y Y
X N N
X N N

# case 2

N N A
N N X
Y Y X

A N N
X N N
X Y Y

Y Y X
N N X
N N A

X Y Y
X N N
A N N
*****************
MIXED_OUTER_CORNER_HORIZONTAL_SAND
N N Y
N N Y
X X A

N N Y
N N Y
A X X

Y N N
Y N N
X X A

Y N N
Y N N
A X X

X X A
N N Y
N N Y

A X X
N N Y
N N Y

X X A
Y N N
Y N N

A X X
Y N N
Y N N
*****************
MIXED_EDGE_VERTICAL
N N X
N N X
N N Y

N N Y
N N X
N N X

X N N
X N N
Y N N

Y N N
X N N
X N N
*****************
MIXED_EDGE_HORIZONTAL
X X Y
N N N
N N N

Y X X
N N N
N N N

N N N
N N N
X X Y

N N N
N N N
Y X X
*****************
MIXED_OUTER_CORNER_VERTICAL_DIRT
N N Y
N N Y
X N N

N N N
N N Y
X Y Y

N N Y
N N Y
X Y Y

Y N N
Y N N
N N X

N N N
Y N N
Y Y X

Y N N
Y N N
Y Y X

X N N
N N Y
N N Y

X Y Y
N N Y
N N N

X Y Y
N N Y
N N Y

N N X
Y N N
Y N N

Y Y X
Y N N
N N N

Y Y X
Y N N
Y N N
*****************
MIXED_OUTER_CORNER_HORIZONTAL_DIRT
Y Y N
N N N
N N X

N Y Y
N N Y
N N X

Y Y Y
N N Y
N N X

N N X
N N N
Y Y N

N N X
N N Y
N N Y

N N X
N N Y
Y Y Y

N Y Y
N N N
X N N

Y Y N
Y N N
X N N

Y Y Y
Y N N
X N N

X N N
N N N
N Y Y

X N N
Y N N
Y Y N

X N N
Y N N
Y Y Y
*****************
MIXED_INNER_CORNER_NEXT_TO_HALF_WATER
N N X
Y N N
Y Y N

X N N
N N Y
N Y Y

Y Y N
Y N N
N N X

N Y Y
N N Y
X N N
*****************
MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER
X X N
X N N
N N Y

N X X
N N X
Y N N

N N Y
X N N
X X N

Y N N
N N X
N X X
*****************
MIXED_CONNECTOR_BETWEEN_HALF_WATERS
N N X
N N Y
X Y Y

X N N
Y N N
Y Y X

X Y Y
N N Y
N N X

Y Y X
Y N N
X N N
*****************
MIXED_OUTER_CORNER_DIAGONAL_SAND
N N X
N N X
X X Y

X N N
X N N
Y X X

X X Y
N N X
N N X

Y X X
X N N
X N N
"""

def build_patterns() -> Dict[str, Tuple[SpriteType, bool, bool]]:
    patterns: Dict[str, Tuple[SpriteType, bool, bool]] = {}
    current_type = None

    lines = [ln.strip() for ln in _raw_definitions.splitlines()]
    import re

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or line == "*****************":
            i += 1
            continue

        # parse and get correct SpriteType from header
        if all(c.isupper() or c == '_' for c in line) and ' ' not in line:
            current_type = getattr(SpriteType, line)
            i += 1
            continue

        # try to read a 3x3 block (3 consecutive non-empty lines of 3 tokens)
        if len(line.split()) == 3:
            block_rows = [''.join(line.split())]
            j = i + 1
            while len(block_rows) < 3 and j < len(lines):
                if lines[j]:
                    parts = lines[j].split()
                    if len(parts) == 3:
                        block_rows.append(''.join(parts))
                    else:
                        break
                j += 1

            if len(block_rows) == 3:
                key = ''.join(block_rows)

                # lookahead for the required explicit flag line (e.g. "x: 0, y: 1")
                k = j
                # skip blank lines between block and flag
                while k < len(lines) and not lines[k]:
                    k += 1

                if k >= len(lines):
                    raise ValueError(f"Missing flag line after 3x3 block for sprite type {current_type} at line {i}")

                m = re.match(r'\s*x\s*:\s*([01])\s*,\s*y\s*:\s*([01])\s*$', lines[k].lower())
                if not m:
                    raise ValueError(f"Expected 'x: <0|1>, y: <0|1>' after 3x3 block for {current_type} at line {i}, got: {lines[k]!r}")

                flag_x = bool(int(m.group(1)))
                flag_y = bool(int(m.group(2)))
                j = k + 1  # consume flag line

                if current_type is None:
                    raise ValueError(f"3x3 block at line {i} is not preceded by a sprite type header")

                patterns[key] = (current_type, flag_x, flag_y)

                i = j
                continue

        i += 1

    return patterns

patterns = build_patterns()