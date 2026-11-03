"""Tiny drawing kit: 100x100 unit canvas, grayscale shading, bold outlines."""
import math
from PIL import Image, ImageDraw

W, K = 255, 18
G1, G2, G3, G4, G5 = 238, 208, 168, 124, 78
S = 10  # px per unit while drawing (supersampled), result resized to 512


class C:
    def __init__(self):
        self.im = Image.new("L", (100 * S, 100 * S), 255)
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def E(self, cx, cy, rx, ry=None, f=W, o=K, w=1.4):
        ry = rx if ry is None else ry
        bb = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        self.d.ellipse(bb, fill=f, outline=o, width=int(w * S) if o is not None else 0)

    def P(self, pts, f=W, o=K, w=1.4, smooth=False, closed=True):
        if smooth:
            pts = spline(pts, closed)
        if f is not None and closed:
            self.d.polygon(self._p(pts), fill=f)
        if o is not None:
            seq = pts + ([pts[0]] if closed else [])
            self.L(seq, w, o)

    def L(self, pts, w=1.6, c=K, smooth=False):
        if smooth:
            pts = spline(pts, False)
        px = self._p(pts)
        self.d.line(px, fill=c, width=int(w * S), joint="curve")
        r = w * S / 2
        for x, y in (px[0], px[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=c)

    def R(self, x, y, w, h, f=W, o=K, lw=1.4, r=0):
        bb = [x * S, y * S, (x + w) * S, (y + h) * S]
        if r:
            self.d.rounded_rectangle(bb, r * S, fill=f, outline=o, width=int(lw * S) if o is not None else 0)
        else:
            self.d.rectangle(bb, fill=f, outline=o, width=int(lw * S) if o is not None else 0)

    def A(self, cx, cy, rx, ry, a0, a1, w=1.6, c=K):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
               for a in frange(a0, a1, 4)]
        self.L(pts, w, c)

    def dot(self, x, y, r=1.0, c=K):
        self.E(x, y, r, r, f=c, o=None)

    def eye(self, x, y, r=2.2):
        self.E(x, y, r, r, f=W, o=K, w=0.7)
        self.E(x + r * 0.15, y, r * 0.55, r * 0.55, f=K, o=None)
        self.E(x + r * 0.35, y - r * 0.3, r * 0.2, r * 0.2, f=W, o=None)

    def save(self, path):
        self.im.resize((512, 512), Image.LANCZOS).convert("RGB").save(path)


def frange(a, b, step):
    out = []
    n = max(2, int(abs(b - a) / step) + 1)
    for i in range(n + 1):
        out.append(a + (b - a) * i / n)
    return out


def spline(pts, closed=True, n=10):
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(P[-2])
    return out


def ground(c, y=88, x0=8, x1=92):
    c.L([(x0, y), (x1, y)], 1.2, G4)
