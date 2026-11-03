"""Shared helpers for the hard-mode pictures (simple, naive cartoons)."""
from lib import *
import math

D = {}
def reg(D_):
    def word(fn):
        D_[fn.__name__.upper()] = fn
        return fn
    return word

def petals(c, cx, cy, n, dist, rx, ry, f=G1, rot=0):
    """n ellipse petals around a centre; ry is along the radial direction."""
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        px, py = cx + dist * math.cos(a), cy + dist * math.sin(a)
        # draw petal as polygon ellipse rotated
        pts = []
        for t in range(0, 360, 20):
            u, v = rx * math.cos(math.radians(t)), ry * math.sin(math.radians(t))
            pts.append((px + v * math.cos(a) - u * math.sin(a), py + v * math.sin(a) + u * math.cos(a)))
        c.P(pts, f=f, w=1.1)

def stem(c, x, y0, y1, w=2.2):
    c.L([(x, y0), (x, y1)], w, G5)

def leaf(c, x, y, dx, dy, f=G3):
    c.P([(x, y), (x + dx * .5, y + dy - 6), (x + dx, y + dy), (x + dx * .5 + 4, y + dy * .4)], f=f, smooth=True)

def star(c, cx, cy, r, f=G1, n=5):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * .45
        a = math.radians(-90 + 180 * i / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    c.P(pts, f=f, w=1.2)

def note(c, x, y, f=K):
    c.E(x, y, 3.4, 2.5, f=f, o=K, w=.6)
    c.L([(x + 3.2, y), (x + 3.2, y - 14)], 1.2)

def table_top(c, y=70):
    c.R(10, y, 80, 5, f=G3, r=1)
    c.L([(18, y + 5), (18, 90)], 2.4, G5); c.L([(82, y + 5), (82, 90)], 2.4, G5)
