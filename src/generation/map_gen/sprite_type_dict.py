from generation.tile_gen.tile_gen import SpriteType

# Auto-generated tile pattern dictionary builder

from enum import Enum
from typing import Dict

# Assume SpriteType enum is defined elsewhere and imported when using this module.

_raw_definitions = r"""
SAND_OUTER_CORNER
X N N
X N N
X X X

N N X
N N X
X X X

X X X
N N X
N N X

X X X
X N N
X N N
*****************
SAND_EDGE_VERTICAL
N N X
N N X
N N X

X N N
X N N
X N N
*****************
SAND_EDGE_HORIZONTAL
X X X
N N N
N N N

N N N
N N N
X X X
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

N N N
X N N
X X N

N X X
N N X
N N N

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
X N N
X N N
A Y Y

A N N
X N N
X Y Y

X Y Y
X N N
A N N

A Y Y
X N N
X N N

N N X
N N X
Y Y A

N N A
N N X
Y Y X

Y Y X
N N X
N N A

Y Y A
N N X
N N X
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

def _serialize(block):
    return ''.join(block).replace(' ', '')

def build_patterns() -> Dict[str, SpriteType]:
    patterns: Dict[str, SpriteType] = {}
    current_type = None
    buffer = []

    for line in _raw_definitions.splitlines():
        line = line.strip()
        if not line:
            continue
        if line == "*****************":
            continue
        if all(c.isupper() or c == '_' for c in line) and ' ' not in line:
            current_type = getattr(SpriteType, line)
            continue
        parts = line.split()
        if len(parts) == 3:
            buffer.append(''.join(parts))
            if len(buffer) == 3:
                key = ''.join(buffer)
                patterns[key] = current_type
                buffer = []
    return patterns

patterns = build_patterns()