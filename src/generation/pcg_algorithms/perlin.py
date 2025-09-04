import math
import random

# Permutation table (doubled to avoid overflow)
p = [i for i in range(256)]
random.shuffle(p)
p = p * 2

def fade(t):
    """6t^5 - 15t^4 + 10t^3 smoothing"""
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    """Linear interpolation"""
    return a + t * (b - a)

def grad(hash, x, y):
    """Gradient function"""
    h = hash & 3
    if h == 0: return  x + y
    if h == 1: return -x + y
    if h == 2: return  x - y
    return -x - y

def perlin(x, y):
    """
    2D Perlin noise for point (x, y).
    Returns value in range [-1, 1].
    """

    # Find unit square
    X = int(math.floor(x)) & 255
    Y = int(math.floor(y)) & 255

    # Relative coords inside square
    xf = x - math.floor(x)
    yf = y - math.floor(y)

    # Fade curves for x and y
    u = fade(xf)
    v = fade(yf)

    # Hash coordinates of the square’s corners
    aa = p[p[X] + Y]
    ab = p[p[X] + Y + 1]
    ba = p[p[X + 1] + Y]
    bb = p[p[X + 1] + Y + 1]

    # Add blended results from all corners
    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)
    return lerp(x1, x2, v)
