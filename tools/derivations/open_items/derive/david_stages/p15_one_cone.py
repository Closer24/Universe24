"""David's probe for the owner's question of 01:3x UTC: does one light cone for every train follow from the tensor act?

usage: python3 -I p15_one_cone.py
The one formula at the vacuum, for one train on the cube: a+ + a- = (2 - d - 6 g) a + g SUM_j a_j, with d = D / w the
spring and g = R / w the grip of each Spoke. Two grips:
  the head's, which carries the train's pinion: g = (pinion / rim) / 3 and d = 2 (1 - pinion / rim), so that
      cos w = (pinion / rim) (1/3) SUM_a cos k_a;
  one grip per Mesh for every train, the light's g_L, the spring the same: cos w = cos w0 - g_L SUM_a (1 - cos k_a).
For each, at the rest beat w0 (cos w0 = pinion / rim): the cone each train reads at long waves, c^2 = w0 / (w''(0)),
read as w'' at k -> 0 along an axis; the rest energy against m c^2 with light's c, E0 / (m c_L^2) = w0 w''(0) / c_L^2
(m = 1 / w''(0) in the lattice's units); and whether the step stays a turn (|cos w| <= 1) over the whole Brillouin
zone, with light at the edge (g_L = 1/3) and at the owner's way (a) for item (g) (g_L = 1/6). Floats; no engine run.
"""
import math


def head(w0, k):
    return math.cos(w0) * sum(math.cos(x) for x in k) / 3


def per_mesh(w0, g, k):
    return math.cos(w0) - g * sum(1 - math.cos(x) for x in k)


def curvature(cosine, h=1e-4):
    """w''(0) along an axis from cos w(k): w(k) = acos(cos w(k)), a central second difference."""
    w = [math.acos(max(-1.0, min(1.0, cosine((x, 0.0, 0.0))))) for x in (-h, 0.0, h)]
    return (w[0] - 2 * w[1] + w[2]) / (h * h)


def stable(cosine, n=24):
    grid = [math.pi * (i / n) for i in range(n + 1)]
    return all(-1 - 1e-12 <= cosine((a, b, c)) <= 1 + 1e-12 for a in grid for b in grid for c in grid)


print("the train's cone against light's, c^2 / c_L^2 = E0 / (m c_L^2), at the rest beat w0 (1 is one cone, and E0 = m c^2):")
for degrees in (2, 10, 30, 48.19, 60, 80):
    w0 = math.radians(degrees)
    h2 = curvature(lambda k: head(w0, k))
    m2 = curvature(lambda k: per_mesh(w0, 1 / 6, k))
    print(f"  {degrees:6.2f} deg: the head's grip {w0 * h2 / (1 / 3):7.4f}; one grip per Mesh {w0 * m2 / (1 / 6):7.4f}")
print("the step a turn over the whole zone:")
for name, cosine in (
    ("the head's grip", lambda w0: (lambda k: head(w0, k))),
    ("one grip per Mesh, light at the edge (g_L = 1/3)", lambda w0: (lambda k: per_mesh(w0, 1 / 3, k))),
    ("one grip per Mesh, light at way (a) (g_L = 1/6)", lambda w0: (lambda k: per_mesh(w0, 1 / 6, k))),
):
    held = [d for d in (0, 2, 10, 30, 60, 80, 90) if stable(cosine(math.radians(d)))]
    print(f"  {name}: a turn at the rest beats {held} (deg)")
print("in closed form: the head's E0/(m c_L^2) = w0 / tan w0, one grip per Mesh w0 / sin w0; both go to 1 as w0 -> 0")
