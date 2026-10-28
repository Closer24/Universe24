"""Probe: Bell through the cone (the owner's word of 2026-10-28, 11:3x UTC), pure Gaussian integers, every draw counted.

The route: the detectors' frames stand in the fitting's past cone (the detectors already entangled with
the pair through their common past), so the pair's one click of a split happens at the fitting, at the
two ends of one Mesh (draft D, part 2: four parts, sigma_ab = N(det[phi_A^a, phi_B^b])), against both
frames. Each child carries its taken sense, phi_A^a or phi_B^b, to its detector, one Mesh a tick. The
far clicks are then clicks of a whole: the part along the other sense has size 0, so each detector reads
the answer the fitting drew, at any tick, however far apart the two clicks are.

Checked here, exactly (no sampling: every draw number c in [0, room) is counted):
  1. the joint odds are the singlet's, E = -m_A . m_B / (rho_A rho_B), and S = -82/29 at draft D's settings;
  2. each far click is a click of a whole (the other part's size is 0);
  3. no signalling: A's odds do not move with B's frame;
  4. the control: where the frames at the fitting are not the detectors' (a setting changed after the
     fitting, outside the cone), the same rule gives |S| <= 2 (Bell's theorem holds);
  5. mutants (a wrong perp, a wrong conjugate, the plus sign) fail.
"""

from fractions import Fraction
from itertools import product


def conj(z):
    return (z[0], -z[1])


def mul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def add(z, w):
    return (z[0] + w[0], z[1] + w[1])


def neg(z):
    return (-z[0], -z[1])


def norm(z):
    return z[0] * z[0] + z[1] * z[1]


def g(x, y=0):
    return (x, y)


def perp(phi):
    """The other sense of a twin pair: (-conj(phi2), conj(phi1)) (draft D, P3)."""
    return (neg(conj(phi[1])), conj(phi[0]))


def det(u, v):
    """The A1 part of two twin pairs (the product table's singlet row)."""
    return add(mul(u[0], v[1]), neg(mul(u[1], v[0])))


def overlap(phi, psi):
    return add(mul(conj(phi[0]), psi[0]), mul(conj(phi[1]), psi[1]))


def reading(phi):
    """(rho, S) of a twin pair."""
    c = mul(conj(phi[0]), phi[1])
    return norm(phi[0]) + norm(phi[1]), (2 * c[0], 2 * c[1], norm(phi[0]) - norm(phi[1]))


def senses(phi, perp_of=perp):
    return {1: phi, -1: perp_of(phi)}


def fitting_split(fa, fb, perp_of=perp, det_of=det):
    """The four parts at the fitting: sigma_ab = N(det[fa^a, fb^b])."""
    sa, sb = senses(fa, perp_of), senses(fb, perp_of)
    return {(a, b): norm(det_of(sa[a], sb[b])) for a in (1, -1) for b in (1, -1)}


def pick_all(sizes):
    """Every draw number c in [0, room), room = the parts' sum: Rule3 picks the part whose running sum passes c.
    Returns the count of draws per part (exact odds)."""
    room = sum(sizes.values())
    counts = {k: 0 for k in sizes}
    order = list(sizes)
    for c in range(room):
        t, run = c, 0
        for k in order:
            run += sizes[k]
            if t < run:
                counts[k] += 1
                break
    return counts, room


def far_click(detector, child, perp_of=perp):
    """The detector's own click of the child: two parts, the overlaps with its two senses. A click of a whole
    where one part is 0; returns (answer, the other part's size)."""
    up, down = norm(overlap(detector, child)), norm(overlap(perp_of(detector), child))
    if down == 0:
        return 1, down
    if up == 0:
        return -1, up
    return None, min(up, down)


def run(fa_at_fit, fb_at_fit, fa_click, fb_click, perp_of=perp, det_of=det):
    """The fitting splits against the frames standing there; the children carry the taken senses; the far
    detectors (frames fa_click, fb_click) click. Returns E as an exact fraction, the whole-click count, and A's odds."""
    sizes = fitting_split(fa_at_fit, fb_at_fit, perp_of, det_of)
    counts, room = pick_all(sizes)
    total, corr, whole, a_up = 0, Fraction(0), 0, Fraction(0)
    for (a, b), n in counts.items():
        if not n:
            continue
        child_a = senses(fa_at_fit, perp_of)[a]
        child_b = senses(fb_at_fit, perp_of)[b]
        ra, _ = far_click(fa_click, child_a, perp_of)
        rb, _ = far_click(fb_click, child_b, perp_of)
        total += n
        if ra is not None and rb is not None:
            whole += n
            corr += n * ra * rb
            a_up += n * (ra == 1)
            continue
        # not a click of a whole: each far detector splits the child by its own two sizes (law 6, local),
        # independently at the two ends; the branch keeps its n draws
        pa = {1: norm(overlap(fa_click, child_a)), -1: norm(overlap(perp_of(fa_click), child_a))}
        pb = {1: norm(overlap(fb_click, child_b)), -1: norm(overlap(perp_of(fb_click), child_b))}
        sa_, sb_ = sum(pa.values()), sum(pb.values())
        corr += n * Fraction(sum(x * y * pa[x] * pb[y] for x, y in product((1, -1), (1, -1))), sa_ * sb_)
        a_up += n * Fraction(pa[1], sa_)
    return corr / total, whole, room, a_up / total


def chsh(e):
    return e[("a", "b")] + e[("a", "b'")] + e[("a'", "b")] - e[("a'", "b'")]


SETTINGS = {
    "a": (g(1), g(0)),        # z, rho 1
    "a'": (g(1), g(1)),       # x, rho 2
    "b": (g(5), g(2)),        # (20, 0, 21), rho 29
    "b'": (g(5), g(-2)),      # (-20, 0, 21), rho 29
}


def main():
    print("1-3. the frames in the fitting's cone: the fitting splits against the detectors' own frames")
    e, whole_all, signal = {}, True, []
    for sa, sb in product(("a", "a'"), ("b", "b'")):
        fa, fb = SETTINGS[sa], SETTINGS[sb]
        ex, whole, room, a_up = run(fa, fb, fa, fb)
        e[(sa, sb)] = ex
        whole_all = whole_all and whole == room
        signal.append((sa, sb, a_up))
        ra, ma = reading(fa)
        rb, mb = reading(fb)
        singlet = Fraction(-(ma[0] * mb[0] + ma[1] * mb[1] + ma[2] * mb[2]), ra * rb)
        print(f"   {sa:2s} {sb:2s}: E = {str(ex):>7s} (the singlet {str(singlet):>7s}, {'equal' if ex == singlet else 'APART'}); "
              f"far clicks of a whole {whole} of {room}; A up {a_up}")
    s = chsh(e)
    print(f"   S = {s} = {float(s):.4f}; S^2 = {s * s} ({'above 4, at most 8' if 4 < s * s <= 8 else 'NOT in the band'})")
    print(f"   every far click a click of a whole: {whole_all}")
    print(f"   no signalling: A's odds per setting pair {[(x, y, str(p)) for x, y, p in signal]}")

    print("4. the control: the frames at the fitting are not the detectors' (B's setting changed after the fitting)")
    e2 = {}
    for sa, sb in product(("a", "a'"), ("b", "b'")):
        fa, fb = SETTINGS[sa], SETTINGS[sb]
        # B's detector turns to the other B setting after the fitting: the fitting saw the other frame
        fb_seen = SETTINGS["b'" if sb == "b" else "b"]
        ex, whole, room, a_up = run(fa, fb_seen, fa, fb)
        e2[(sa, sb)] = ex
        print(f"   {sa:2s} {sb:2s}: E = {str(ex):>8s}")
    s2 = chsh(e2)
    print(f"   S = {s2} = {float(s2):.4f}; |S| <= 2: {abs(s2) <= 2}")

    print("5. mutants (each must move S off the singlet's -82/29)")
    mutants = {
        "perp without the sign": lambda phi: (conj(phi[1]), conj(phi[0])),
        "perp without the conjugates": lambda phi: (neg(phi[1]), phi[0]),
    }
    for name, p in mutants.items():
        e3 = {}
        for sa, sb in product(("a", "a'"), ("b", "b'")):
            fa, fb = SETTINGS[sa], SETTINGS[sb]
            e3[(sa, sb)] = run(fa, fb, fa, fb, perp_of=p)[0]
        s3 = chsh(e3)
        print(f"   {name}: S = {s3} ({'FAILS as it must' if s3 != s else 'DOES NOT FAIL'})")
    complex_settings = {
        "a": (g(1), g(0)),        # z
        "a'": (g(1), g(0, 1)),    # y, rho 2
        "b": (g(5), g(0, 2)),     # (0, 20, 21), rho 29
        "b'": (g(5), g(0, -2)),   # (0, -20, 21), rho 29
    }
    for label, p in (("the frames off the real plane (y and z): the head's perp", perp),
                     ("the frames off the real plane: perp without the conjugates", mutants["perp without the conjugates"])):
        e5 = {}
        for sa, sb in product(("a", "a'"), ("b", "b'")):
            fa, fb = complex_settings[sa], complex_settings[sb]
            e5[(sa, sb)] = run(fa, fb, fa, fb, perp_of=p)[0]
        s5 = chsh(e5)
        print(f"   {label}: S = {s5}")
    plus = lambda u, v: add(mul(u[0], v[1]), mul(u[1], v[0]))
    e4 = {}
    for sa, sb in product(("a", "a'"), ("b", "b'")):
        fa, fb = SETTINGS[sa], SETTINGS[sb]
        e4[(sa, sb)] = run(fa, fb, fa, fb, det_of=plus)[0]
    s4 = chsh(e4)
    print(f"   the plus sign in det: S = {s4} ({'FAILS as it must' if s4 != s else 'DOES NOT FAIL'})")


if __name__ == "__main__":
    main()
