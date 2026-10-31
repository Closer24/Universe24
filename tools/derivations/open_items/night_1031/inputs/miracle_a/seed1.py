"""MIRACLE_A, the seed: one quartic gear, V(x) = s x^2 + c x^4, its polarized step and its McMillan invariant.
The integers are the pair world's own, read from its files: W the teeth at rest (6 den Gamma^2), s the spring, c the
tie's factor hold x f (f = rest div Gamma); D = 2W the edge's dial at rest. The lay: a count of the setting's gears
laid at rest (now = before), named by its train on the command line (the giver's 14, the held hand's 1).
The step, polarized (V_d(y, z) = s (y^2 + z^2) + 2 c y^2 z^2, V_d(z, z) = 2V), in the act's form:
  2 (D + kappa(z)) (z+ - z) = 2 (D + kappa(z)) (z - z-) + 4 J(z),  kappa(z) = 2 s + 4 c z^2,  J(z) = -2 s z - 4 c z^3,
which is McMillan's z+ + z- = 2 W z / (W + s + 2 c z^2), keeping exactly the whole polynomial
  E4(x, y) = 2 D (y - x)^2 + 4 s (x^2 + y^2) + 8 c x^2 y^2 = 4 (W + s) [x^2 + y^2 - 2 mu x y + beta x^2 y^2].
Three forms, round by round:
  unreduced: the exact rational as the act would hold it with no loop, z = Z / Q per slot, Z+ = 2 W Z Q Q- - Z- e,
             Q+ = e Q-, e = (W + s) Q^2 + 2 c Z^2 (the count and tooth of z are carry(Z, Q)); its E4 kept as
             H(n) (Q0 Q1)^2 = H(0) (Q- Q)^2, H the homogenized E4;
  reduced:   the same rationals reduced by Euclid's carries (the least any exact form holds; a reading's loop);
  whole:     the act's own carry, (count, tooth) on the round's dial d(a) = D + kappa(a), n = 2 d (a - b) + t + 4 J(a),
             split at d (n = 2 d q + t+, -d <= t+ < d), a+ = a + q; mirrored (b, a, -1 - t).
The run back of each form is the same step on the mirrored end state alone. Usage:
python -I seed1.py <universe> <piece> <setting> <train> [whole=N] [exact=N] [reduced=N]"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qrat  # noqa: E402  (puts the tree on the path)
from qrat import R, bits, count_tooth, over  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine.step import split  # noqa: E402
from tensor24.runner.load import teeth  # noqa: E402
from tensor24.runner.files import star  # noqa: E402

args = [a for a in sys.argv[1:] if "=" not in a]
opts = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
universe, piece, setting = (json.loads(Path(p).read_text(encoding="utf-8")) for p in args[:3])
train = args[3]
names = [t["name"] for t in universe["trains"]]
spokes = star(len(piece["shape"]))
senses, _ = carry(len(spokes), len(piece["shape"]), 0)
_, rest = teeth(universe, spokes)
W = rest
D = senses * W
s = universe["chosen"]["spring"]
f, _ = carry(rest, universe["integers"]["full_rate"], 0)
c = universe["chosen"]["hold"] * f
laid = [g for g in setting["gears"] if g[0] == names.index(train) and g[1] == 0][0]
x_now, x_before = laid[3], laid[4]
print(f"seed: W {W}, D {D}, s {s}, c {c}; laid at the {train}'s count {x_now} now, {x_before} before")


def E4(x, y):
    return senses * D * (y - x) * (y - x) + 4 * s * (x * x + y * y) + 8 * c * x * x * y * y


def H(X, P, Y, Q):
    """E4 homogenized: E4(X / P, Y / Q) P^2 Q^2."""
    return senses * D * (Y * P - X * Q) ** 2 + 4 * s * (X * X * Q * Q + Y * Y * P * P) + 8 * c * X * X * Y * Y


# ---- whole: the act's carry on (count, tooth), the round's dial at the middle count ----
def d_of(a):
    return D + senses * s + 4 * c * a * a


def J(a):
    return -senses * s * a - 4 * c * a * a * a


def tick_whole(st):
    a, b, t = st
    d = d_of(a)
    n = senses * (d * (a - b) + senses * J(a)) + t
    q, t1 = split(n, d, senses)
    return (a + q, a, t1)


def mirror_whole(st):
    a, b, t = st
    return (b, a, -1 - t)


nw = int(opts.get("whole", 0))
if nw:
    st0 = (x_now, x_before, 0)
    st, e0 = st0, E4(x_before, x_now)
    lo, hi, first, wide, out = e0, e0, None, 0, 0
    for n in range(1, nw + 1):
        a_prev = st[0]
        st = tick_whole(st)
        e = E4(st[1], st[0])
        lo, hi = min(lo, e), max(hi, e)
        first = first if first is not None or e == e0 else (n, e - e0)
        wide = max(wide, int(abs(st[0])).bit_length())
        # the tooth was written on d(a_prev); the next round reads it on d(st[0]): inside both windows?
        dn = d_of(st[0])
        inside = -dn <= st[2] < dn
        out = out if out or inside else n
        if n % 250 == 0:
            print(f"whole round {n}: count {st[0]}, E4 {e} ({e - e0:+d} from the lay); widest {wide} bits", flush=True)
    print(f"whole: E4 at the lay {e0}; over {nw} rounds from {lo} to {hi}; first change {first}; widest count {wide} bits")
    print(f"whole: first round whose tooth falls outside the next round's window: {out or 'none'}")
    # the run back from the end state alone, and the longest prefix that runs back
    def back(end, k):
        y = mirror_whole(end)
        for _ in range(k):
            y = tick_whole(y)
        return mirror_whole(y)
    print(f"whole: run back from the end state alone over {nw} rounds:", back(st, nw) == st0)
    lo_ok, hi_bad, prefix = 0, None, [st0]
    for _ in range(nw):
        prefix.append(tick_whole(prefix[-1]))
    for k in range(1, nw + 1):
        if back(prefix[k], k) != st0:
            hi_bad = k
            break
    print(f"whole: the run back is exact over every prefix of 1 to {(hi_bad or nw + 1) - 1} rounds; first failing prefix {hi_bad}")

# ---- unreduced exact: z = Z / Q per slot, the act's exact form with no loop ----
nx = int(opts.get("exact", 0))
if nx:
    Zb, Qb, Z, Q = x_before, 1, x_now, 1
    h0, q0 = H(Zb, Qb, Z, Q), (Qb * Q) ** 2
    past = None
    for n in range(1, nx + 1):
        e = (W + s) * Q * Q + senses * c * Z * Z
        Zn, Qn = senses * W * Z * Q * Qb - Zb * e, e * Qb
        Zb, Qb, Z, Q = Z, Q, Zn, Qn
        kept = H(Zb, Qb, Z, Q) * q0 == h0 * (Qb * Q) ** 2
        cnt, tooth = carry(Z, Q, 0)
        wide = max(int(abs(Z)).bit_length(), Q.bit_length())
        past = past or (n if wide > universe["integers"]["width"] else None)
        print(f"unreduced round {n}: E4 kept {kept}; Z {int(abs(Z)).bit_length()} bits, Q {Q.bit_length()} bits; count {cnt}", flush=True)
    print(f"unreduced: the width {universe['integers']['width']} first passed at round {past}")
    # the run back from the end state alone: the same step on the swapped pair
    Ze, Qe, Zf, Qf = Z, Q, Zb, Qb  # mirrored: now = the end's before, before = the end's now
    Zb2, Qb2, Z2, Q2 = Ze, Qe, Zf, Qf
    for _ in range(nx):
        e = (W + s) * Q2 * Q2 + senses * c * Z2 * Z2
        Zn, Qn = senses * W * Z2 * Q2 * Qb2 - Zb2 * e, e * Qb2
        Zb2, Qb2, Z2, Q2 = Z2, Q2, Zn, Qn
    # mirrored back: now = Zb2/Qb2 should be x_now's slot, before = Z2/Q2 the before's
    same_value = (Zb2 == x_now * Qb2) and (Z2 == x_before * Q2)
    c1, t1 = carry(Zb2, Qb2, 0)
    print(f"unreduced: run back from the end state alone over {nx} rounds: the rationals {same_value}; "
          f"the counts and teeth {(c1, t1) == (x_now, 0)}; the dials back to 1: {Qb2 == 1 and Q2 == 1} "
          f"(now's dial {Qb2.bit_length()} bits)")

# ---- reduced exact: the least an exact form holds ----
nr = int(opts.get("reduced", 0))
if nr:
    zb, z = R(x_before), R(x_now)
    e0 = E4(zb, z)
    hist, past = [], None
    for n in range(1, nr + 1):
        zn = over(senses * W * z, (W + s) + senses * c * z * z) - zb
        zb, z = z, zn
        kept = E4(zb, z) == e0
        w = max(bits(zb), bits(z))
        hist.append(w)
        past = past or (n if w > universe["integers"]["width"] else None)
        d2 = hist[-1] - 2 * hist[-2] + hist[-3] if len(hist) > 2 else "-"
        print(f"reduced round {n}: E4 kept {kept}; widest {w} bits; second difference {d2}; count {count_tooth(z)[0]}", flush=True)
    print(f"reduced: the width {universe['integers']['width']} first passed at round {past}")
    yb, y = z, zb
    for _ in range(nr):
        yn = over(senses * W * y, (W + s) + senses * c * y * y) - yb
        yb, y = y, yn
    print(f"reduced: run back from the end state alone over {nr} rounds:", yb == R(x_now) and y == R(x_before))
