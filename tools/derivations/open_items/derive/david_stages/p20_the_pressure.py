"""David's probe for the pressure's sign: which channel sources the time gear's load c, rho + 3p or the head's rho - 3p.

usage: python3 -I p20_the_pressure.py <tensor24 worktree>/src
  (1) on the law's metric N A = 1 (N = e^Phi, A = 1 / N), a train with the cone kappa and the spring mu has the action
      L = (1/2) e^(-4 Phi) v^2 - (kappa/2) |grad phi|^2 - (mu/2) e^(-2 Phi) phi^2: 7b's gearing (W reading Y^4 ~ N^-4,
      the spring Y^2 ~ N^-2, the grip unread). Its own source of Phi, -dL/dPhi, against rho + T_ii and rho - T_ii,
      built from the stress T_ij = kappa d_i phi d_j phi + delta_ij L: exact rationals at random points, and the
      derivative by a centred difference;
  (2) a float board of the act (a+ - 2a + b = kappa L a - mu a, the doubler's hold kappa = 1/6): a light packet
      (mu = 0) and a dust packet (mu = 0.04, at rest), each at the energy 1 by the step's own conserved form; the
      board's summed source per tick, averaged over the run, for the exact form (the strides), the force form, the
      gradient form and the trace's form; light over dust;
  (3) 7a's own act (tensor24.engine.step), exact integers: row 0 the time gear, row 1 the train, J_0 from the plan's
      terms on the train's readings; the time gear's summed impulse moves by the summed J at every tick, exactly; the
      light and the dust packets at about equal energy; the run back exact through 40 ticks.
"""
import math
import random
import sys
from fractions import Fraction as Q

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

# (1) the identity ---------------------------------------------------------------------------------------------------
print("(1) the action of a train on the law's metric N A = 1, its own source of Phi:")
rng = random.Random(19)
worst_plus = worst_minus_trace = 0
for _ in range(1000):
    v, mu, kap, phi = (Q(rng.randint(-99, 99), rng.randint(1, 50)) for _ in range(4))
    kap, mu = abs(kap) + Q(1, 100), abs(mu)
    g = [Q(rng.randint(-99, 99), rng.randint(1, 50)) for _ in range(3)]
    g2 = sum(x * x for x in g)
    lag = v * v / 2 - kap * g2 / 2 - mu * phi * phi / 2
    rho = v * v / 2 + kap * g2 / 2 + mu * phi * phi / 2
    t_ii = kap * g2 + 3 * lag  # SUM_i (kappa d_i phi d_i phi + L)
    own = 2 * v * v - mu * phi * phi  # -dL/dPhi at Phi = 0, from e^(-4 Phi) and e^(-2 Phi)
    worst_plus = max(worst_plus, abs(own - (rho + t_ii)))
    trace = -rho + t_ii  # T^mu_mu
    worst_minus_trace = max(worst_minus_trace, abs((rho - t_ii) + trace))
print(f"  -dL/dPhi = 2 v^2 - mu phi^2 against rho + T_ii, exact rationals at 1,000 random points: largest miss {worst_plus}")
print(f"  rho - T_ii against minus the trace T^mu_mu: largest miss {worst_minus_trace}")


def action(p, v, kap, g2, mu, phi):
    return 0.5 * math.exp(-4 * p) * v * v - 0.5 * kap * g2 - 0.5 * mu * math.exp(-2 * p) * phi * phi


worst = 0.0
for _ in range(1000):
    v, kap, g2, mu, phi = (rng.uniform(-2, 2), rng.uniform(0.05, 1), rng.uniform(0, 3), rng.uniform(0, 1), rng.uniform(-2, 2))
    d = (action(1e-6, v, kap, g2, mu, phi) - action(-1e-6, v, kap, g2, mu, phi)) / 2e-6
    worst = max(worst, abs(-d - (2 * v * v - mu * phi * phi)))
print(f"  the derivative itself by a centred difference at 1,000 random points: largest miss {worst:.1e}")
print("  so the books' own source of the load is rho + T_ii = rho + 3p (pointwise); rho - T_ii is minus the trace")


# (2) the float board --------------------------------------------------------------------------------------------------
def lap(a):
    return sum(np.roll(a, s, ax) for ax in range(3) for s in (1, -1)) - 6 * a


def centred(a):
    return [np.roll(a, -1, ax) - np.roll(a, 1, ax) for ax in range(3)]


def run(a0, am, kap, mu, ticks):
    """The leapfrog a+ = 2 a - b + kappa L a - mu a; per tick the board's sums of each source, and the energy."""
    b, a = am, a0
    sums = {"exact": [], "force": [], "gradient": [], "mesh": [], "trace": [], "trace, pointwise": [], "forms": [],
            "centred trace": []}
    energy = []
    for _ in range(ticks):
        acc = kap * lap(a) - mu * a
        nxt = 2 * a - b + acc
        vb, vp = a - b, nxt - a
        grad2_c = sum(d * d for d in centred(a)) / 4  # |grad phi|^2 by centred differences
        grad2_m = sum((np.roll(a, -1, ax) - a) ** 2 for ax in range(3))  # by the Meshes
        sums["exact"].append(float(np.sum(vb * vb + vp * vp - mu * a * a)))  # 2 v^2 - mu phi^2, v^2 the mean of both
        sums["force"].append(float(np.sum(-2 * a * acc - mu * a * a)))  # -2 phi phi'' - mu phi^2
        sums["gradient"].append(float(np.sum(2 * kap * grad2_c + mu * a * a)))
        sums["mesh"].append(float(np.sum(2 * kap * grad2_m + mu * a * a)))
        sums["trace"].append(float(np.sum(mu * a * a)))  # the trace's channel on the time average
        sums["trace, pointwise"].append(float(np.sum(-(vb * vb + vp * vp) / 2 + kap * grad2_c + 2 * mu * a * a)))
        sums["forms"].append(float(np.sum(vb * vp - a * acc)))  # the head's forms: u_in u_out less the start times the pull
        sums["centred trace"].append(float(np.sum(4 * grad2_c)))  # the head's trace: the centred differences squared
        m = -kap * lap(nxt) + mu * nxt
        energy.append(float(0.5 * np.sum(vp * vp) + 0.5 * np.sum(a * m)))  # (1/2) v^2 + (1/2) a M a+
        b, a = a, nxt
    return {k: np.array(x) for k, x in sums.items()}, np.array(energy)


SIDES = (192, 16, 16)
x, y, z = np.meshgrid(*(np.arange(n) for n in SIDES), indexing="ij")
KAP, TICKS = 1.0 / 6, 600
cx, cy, cz = (n / 2 for n in SIDES)
print(f"(2) the act on a float board {SIDES}, the cone kappa = 1/6, {TICKS} ticks, each packet at the energy 1:")
results = {}
k = 2 * math.pi / 24
omega = 2 * math.asin(math.sqrt(KAP) * math.sin(k / 2))  # the lattice's own light along an axis
env = lambda dx: np.exp(-((x - cx - dx) ** 2) / (2 * 20.0**2) - ((y - cy) ** 2 + (z - cz) ** 2) / (2 * 5.0**2))  # noqa: E731
vg = math.sqrt(KAP) * math.cos(k / 2) / math.sqrt(1 - KAP * math.sin(k / 2) ** 2)
light0, lightm = env(0) * np.cos(k * (x - cx)), env(-vg) * np.cos(k * (x - cx) + omega)
MU = 0.1
dust_env = np.exp(-((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) / (2 * 10.0**2))
w0 = 2 * math.asin(math.sqrt(MU) / 2)
dust0, dustm = dust_env, dust_env * math.cos(w0)
MU2 = 0.02
wide = np.exp(-((x - cx) ** 2) / (2 * 32.0**2))  # uniform across the two short sides
w2 = 2 * math.asin(math.sqrt(MU2) / 2)
cases = {"light": (light0, lightm, 0.0), "dust": (dust0, dustm, MU), "dust, wide": (wide, wide * math.cos(w2), MU2)}
for name, (a0, am, mu) in cases.items():
    sums, energy = run(a0, am, KAP, mu, TICKS)
    e = energy.mean()
    results[name] = {k2: v.mean() / e for k2, v in sums.items()}
    results[name]["_forms"], results[name]["_trace"] = sums["forms"].mean() / e, sums["centred trace"].mean() / e
    drift = (energy.max() - energy.min()) / e
    print(f"  {name}: the energy kept to {drift:.1e} of itself; the summed source per tick over the energy:")
    print("    " + ", ".join(f"{k2} {v:.4f}" for k2, v in results[name].items() if not k2.startswith("_")
                            and k2 not in ("forms", "centred trace")))
for d in ("dust", "dust, wide"):
    print(f"  light over {d} at one energy: " + ", ".join(
        f"{k2} {results['light'][k2] / results[d][k2]:.3f}" for k2 in results["light"]
        if not k2.startswith("_") and k2 not in ("forms", "centred trace")))
b = results["light"]["_trace"] / results["light"]["_forms"]  # the balance: a massless wave's forms against its trace
print(f"  the head's own variables: light's trace over its forms, the balance weight, {b:.3f} (2 / kappa = 12 for long waves)")
for sign, word in ((-1, "the head's sign, b forms - trace"), (1, "the count's sign, b forms + trace")):
    v = {n: b * r["_forms"] + sign * r["_trace"] for n, r in results.items()}
    print(f"    {word}: light {v['light']:.4f}, dust {v['dust']:.4f}, wide dust {v['dust, wide']:.4f};"
          f" light over wide dust {v['light'] / v['dust, wide']:.3f}")


# (3) 7a's own act ---------------------------------------------------------------------------------------------------
def board(shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def meshes_of(nb):
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def obj(v):
    return np.asarray(v, dtype=object)


GAMMA = 1000
SHAPE = (96, 6, 6)
nb = board(SHAPE)
N = nb.shape[1]
W1, GRIP1 = 150, 25  # the train: kappa = 25 / 150 = 1/6
# the readings' rows: plane * G + row, G = 2 (row 0 the time gear, row 1 the train); planes 0 value, 1-3 the centred
# differences, 4 the force
VAL, FORCE, GRADS = 1, 4 * 2 + 1, (1 * 2 + 1, 2 * 2 + 1, 3 * 2 + 1)


def plan_of(form, d1):
    """J_0 from the train's readings, twice the forms of (2) in the act's integers (W times the notch form)."""
    if form == "force":  # -2 a F - D a a, twice: -4 a F - 2 D a a
        terms = [(VAL, FORCE, -4), (VAL, VAL, -2 * d1)]
    elif form == "gradient":  # grip SUM (D_a a)^2 / 2 + D a a, twice
        terms = [(g, g, GRIP1) for g in GRADS] + [(VAL, VAL, 2 * d1)]
    else:  # the trace's channel: D a a, twice
        terms = [(VAL, VAL, 2 * d1)]
    first, second, factor = zip(*terms, strict=True)
    return Plan(np.array(first, np.intp), np.array(second, np.intp), obj(list(factor)), np.zeros(len(terms), np.intp))


def layout_of(plan, d1):
    grip = obj(np.vstack([np.zeros((1, 3 * N), int), np.full((1, 3 * N), GRIP1)]))
    col = lambda v0, v1: obj([[v0], [v1]])  # noqa: E731
    gearing = Gearing(col(1, W1), col(1, W1), 1, col(0, d1), 1, col(1, 1))
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, N), GAMMA)), GAMMA)


AMP = 10**6
xs = np.unravel_index(np.arange(N), SHAPE)
cx3 = [n / 2 for n in SHAPE]
k3 = 2 * math.pi / 16
om3 = 2 * math.asin(math.sqrt(1 / 6) * math.sin(k3 / 2))
vg3 = math.sqrt(1 / 6) * math.cos(k3 / 2) / math.sqrt(1 - (1 / 6) * math.sin(k3 / 2) ** 2)
env3 = lambda dx: np.exp(-((xs[0] - cx3[0] - dx) ** 2) / (2 * 12.0**2))  # noqa: E731
D_DUST = 15  # mu = 15 / 150 = 0.1
wd = 2 * math.asin(math.sqrt(D_DUST / W1) / 2)
denv = np.exp(-((xs[0] - cx3[0]) ** 2) / (2 * 10.0**2) - ((xs[1] - cx3[1]) ** 2 + (xs[2] - cx3[2]) ** 2) / (2 * 40.0**2))
D_WIDE = 3  # mu = 0.02
wenv = np.exp(-((xs[0] - cx3[0]) ** 2) / (2 * 20.0**2))
ww = 2 * math.asin(math.sqrt(D_WIDE / W1) / 2)
packets = {
    "light": (0, AMP * env3(0) * np.cos(k3 * (xs[0] - cx3[0])), AMP * env3(-vg3) * np.cos(k3 * (xs[0] - cx3[0]) + om3)),
    "dust": (D_DUST, AMP * denv, AMP * denv * math.cos(wd)),
    "wide": (D_WIDE, AMP * wenv, AMP * wenv * math.cos(ww)),
}


def energy_of(a, b, d1):
    """The step's conserved form in the train's notches (floats from the integers): (1/2) v^2 + (1/2) a M b."""
    a, b = a.astype(float), b.astype(float)
    shaped = lambda u: u.reshape(SHAPE)  # noqa: E731
    lap_b = lap(shaped(b)).ravel()
    m_b = -(GRIP1 / W1) * lap_b + (d1 / W1) * b
    return 0.5 * np.sum((a - b) ** 2) + 0.5 * np.sum(a * m_b)


print(f"(3) 7a's own act, exact integers, the board {SHAPE}, the train at W {W1} and the grip {GRIP1} (kappa 1/6):")
TICKS3 = 300
per_energy = {}
for form in ("force", "gradient", "trace"):
    for name, (d1, a1, b1) in packets.items():
        layout = layout_of(plan_of(form, d1), d1)
        a = obj(np.zeros((2, N), int))
        b = obj(np.zeros((2, N), int))
        a[1] = obj(np.rint(a1).astype(np.int64).tolist())
        b[1] = obj(np.rint(b1).astype(np.int64).tolist())
        r = obj(np.vstack([np.full((1, N), home(1, 0)), np.full((1, N), home(W1, 0))]))
        zero = obj(np.zeros((1, N), int))
        s = State(a, b, r, obj(np.zeros((2, N), int)), obj(np.zeros((2, N), int)), zero, zero, zero)
        e0 = energy_of(s.a[1], s.b[1], d1)
        p0 = lambda st: int(np.sum(1 * (st.a[0] - st.b[0]) + (st.r[0] - home(1, st.go[0]))))  # noqa: E731
        total, exact_ok, kept = 0, True, []
        for t in range(TICKS3):
            before = p0(s)
            _, j = step.sources(layout, s)
            s1, out = step.tick(layout, s, 1)
            moved = p0(s1) - before
            exact_ok &= moved == int(np.sum(j[0]))
            total += moved
            if t < 40:
                kept.append((s, s1, out))
            s = s1
        back_ok = all(all(np.array_equal(u, v) for u, v in zip(step.untick(layout, s1_, o_), s0_, strict=True))
                      for s0_, s1_, o_ in kept)
        e1 = energy_of(s.a[1], s.b[1], d1)
        per_energy[(form, name)] = total / TICKS3 / (W1 * 2 * (e0 + e1) / 2)
        print(f"  {form:8s} {name:5s}: the time gear's summed impulse moved by the summed J at every tick: {exact_ok};"
              f" run back 40 of 40: {back_ok}; the energy {e0:.4e} -> {e1:.4e}; the source per tick per energy"
              f" {per_energy[(form, name)]:.4f}")
for form in ("force", "gradient", "trace"):
    print(f"  {form}: light over dust at one energy {per_energy[(form, 'light')] / per_energy[(form, 'dust')]:.3f},"
          f" over the wide dust {per_energy[(form, 'light')] / per_energy[(form, 'wide')]:.3f}")
