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
  5. mutants (a wrong perp, a wrong conjugate, the plus sign) fail;
  6. line 102 (Sofer's law check, 6467734998, item 3): the four parts are law 6 on the pair's composite state Psi laid
     at the fitting, sigma_ab = N(<phi_A^a (x) phi_B^b, Psi>). Law 6 on one hand is the same overlap (6a); the 24 fix
     k epsilon alone among the two-spinors (6b), and on it the rule is the closure's det form part for part (6c); the
     same rule with other states laid gives other numbers, the T1 states theirs and every product |S| <= 2 (6d); no
     state laid signals (6e); the A1 state's odds stand under the 24 and a T1 state's turn with it (6f); a mutant fails (6g).
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


def overlap2(u, v, psi):
    """Law 6's overlap on two hands: <u (x) v, Psi> = sum_ij conj(u_i) conj(v_j) Psi_ij, Psi a 2 x 2 Gaussian tensor."""
    total = g(0)
    for i in range(2):
        for j in range(2):
            total = add(total, mul(mul(conj(u[i]), conj(v[j])), psi[i][j]))
    return total


def mat_mul(m, n):
    return [[add(mul(m[i][0], n[0][j]), mul(m[i][1], n[1][j])) for j in range(2)] for i in range(2)]


def transpose(m):
    return [[m[0][0], m[1][0]], [m[0][1], m[1][1]]]


def dagger(m):
    return [[conj(m[0][0]), conj(m[1][0])], [conj(m[0][1]), conj(m[1][1])]]


def mat_det(m):
    return add(mul(m[0][0], m[1][1]), neg(mul(m[0][1], m[1][0])))


def act(m, phi):
    return (
        add(mul(m[0][0], phi[0]), mul(m[0][1], phi[1])),
        add(mul(m[1][0], phi[0]), mul(m[1][1], phi[1])),
    )


def reading(phi):
    """(rho, S) of a twin pair."""
    c = mul(conj(phi[0]), phi[1])
    return norm(phi[0]) + norm(phi[1]), (2 * c[0], 2 * c[1], norm(phi[0]) - norm(phi[1]))


def senses(phi, perp_of=perp):
    return {1: phi, -1: perp_of(phi)}


def fitting_split(fa, fb, perp_of=perp, det_of=det, psi=None):
    """The four parts at the fitting: sigma_ab = N(det[fa^a, fb^b]); with a composite state Psi laid at the fitting,
    law 6 on the two hands: sigma_ab = N(<fa^a (x) fb^b, Psi>)."""
    sa, sb = senses(fa, perp_of), senses(fb, perp_of)
    if psi is not None:
        return {(a, b): norm(overlap2(sa[a], sb[b], psi)) for a in (1, -1) for b in (1, -1)}
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


def run(fa_at_fit, fb_at_fit, fa_click, fb_click, perp_of=perp, det_of=det, psi=None):
    """The fitting splits against the frames standing there; the children carry the taken senses; the far
    detectors (frames fa_click, fb_click) click. Returns E as an exact fraction, the whole-click count, and A's odds."""
    sizes = fitting_split(fa_at_fit, fb_at_fit, perp_of, det_of, psi)
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


# Part 6 (line 102): the composite state, its kinds, and the 24 on it.

# The 24's generators lifted to 2O, Gaussian matrices with a scale (draft D, P9): a quarter turn about z, a quarter
# turn about x, a third of a turn about (1, 1, 1); det 2, 2 and 4. The first and the third generate the 24.
GENERATORS = {
    "a quarter turn about z": [[g(1, -1), g(0)], [g(0), g(1, 1)]],
    "a quarter turn about x": [[g(1), g(0, -1)], [g(0, -1), g(1)]],
    "a third of a turn about (1, 1, 1)": [[g(1, -1), g(-1, -1)], [g(1, -1), g(1, 1)]],
}

EPS = [[g(0), g(1)], [g(-1), g(0)]]  # the product table's A1 row, epsilon (the singlet)
T1 = {  # its T1 rows, (n . sigma) epsilon, symmetric
    "x": [[g(-1), g(0)], [g(0), g(1)]],
    "y": [[g(0, 1), g(0)], [g(0), g(0, 1)]],
    "z": [[g(0), g(1)], [g(1), g(0)]],
}
AXES = {
    "z": ((g(1), g(0)), (g(0), g(1))),
    "x": ((g(1), g(1)), (g(1), g(-1))),
    "y": ((g(1), g(0, 1)), (g(1), g(0, -1))),
}


def scale(k, m):
    return [[mul(k, m[i][j]) for j in range(2)] for i in range(2)]


def mat_add(m, n):
    return [[add(m[i][j], n[i][j]) for j in range(2)] for i in range(2)]


def outer(u, v):
    """The product state u (x) v: Psi_ij = u_i v_j."""
    return [[mul(u[i], v[j]) for j in range(2)] for i in range(2)]


def turned_spinor_law(m, psi):
    """Two spinor indices turned by M: M Psi M^T - det(M) Psi (zero where Psi is A1)."""
    return mat_add(mat_mul(mat_mul(m, psi), transpose(m)), scale(neg(mat_det(m)), psi))


def turned_conjugate_law(m, psi):
    """The mutant: the second index turned as a conjugate spinor, M Psi M^dagger - det(M) Psi."""
    return mat_add(mat_mul(mat_mul(m, psi), dagger(m)), scale(neg(mat_det(m)), psi))


def rank(rows):
    rows = [[Fraction(x) for x in r] for r in rows]
    rk = 0
    for c in range(len(rows[0])):
        piv = next((r for r in range(rk, len(rows)) if rows[r][c] != 0), None)
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for r in range(len(rows)):
            if r != rk and rows[r][c] != 0:
                f = rows[r][c] / rows[rk][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[rk], strict=True)]
        rk += 1
    return rk


def invariant_dim(law):
    """The real dimension of the two-spinors Psi with law(M, Psi) = 0 for every generator M (exact elimination)."""
    basis = []
    for i, j in product(range(2), range(2)):
        for unit in (g(1), g(0, 1)):
            b = [[g(0), g(0)], [g(0), g(0)]]
            b[i][j] = unit
            basis.append(b)
    rows = []
    for m in GENERATORS.values():
        images = [[x for i in range(2) for j in range(2) for x in law(m, b)[i][j]] for b in basis]
        rows.extend([images[k][e] for k in range(8)] for e in range(8))
    return 8 - rank(rows)


def odds(fa, fb, psi):
    sizes = fitting_split(fa, fb, psi=psi)
    room = sum(sizes.values())
    return tuple(Fraction(sizes[k], room) for k in sorted(sizes))


def s_of(psi, settings=None):
    settings = settings or SETTINGS
    e, whole_all, a_odds = {}, True, {}
    for sa, sb in product(("a", "a'"), ("b", "b'")):
        fa, fb = settings[sa], settings[sb]
        ex, whole, room, a_up = run(fa, fb, fa, fb, psi=psi)
        e[(sa, sb)] = ex
        whole_all = whole_all and whole == room
        a_odds[(sa, sb)] = a_up
    no_signal = all(a_odds[(x, "b")] == a_odds[(x, "b'")] for x in ("a", "a'"))
    return chsh(e), e, whole_all, no_signal


def part6():
    print("6. line 102: the four parts are law 6 on the pair's composite state Psi laid at the fitting,")
    print(
        "   sigma_ab = N(<phi_A^a (x) phi_B^b, Psi>); the rule reads Psi, and the frames enter as in every click"
    )

    # 6a. law 6 on one hand is the same overlap: N(<phi^+-, psi>) = (rho_d rho +- m . S) / 2 (Fierz; the plan's K6)
    box = [g(x, y) for x in range(-2, 3) for y in range(-2, 3)]
    spinors = [(p, q) for p in box for q in box if norm(p) + norm(q)]
    bad = checked = 0
    for phi in spinors:
        rd, m = reading(phi)
        for psi in spinors:
            r, s = reading(psi)
            dot = m[0] * s[0] + m[1] * s[1] + m[2] * s[2]
            checked += 1
            bad += (
                2 * norm(overlap(phi, psi)) != rd * r + dot
                or 2 * norm(overlap(perp(phi), psi)) != rd * r - dot
            )
    print(
        f"   6a. law 6 on one hand is the overlap's size, 2 N(<phi^+-, psi>) = rho_d rho +- m . S: "
        f"{checked - bad} of {checked} pairs (the components in [-2, 2] + [-2, 2] i)"
    )

    # 6b. the kinds: the two-spinors left fixed by the 24 (lifted to 2O), by exact elimination
    dim = invariant_dim(turned_spinor_law)
    fixed = all(turned_spinor_law(m, EPS) == [[g(0), g(0)], [g(0), g(0)]] for m in GENERATORS.values())
    print(
        f"   6b. the two-spinors with M Psi M^T = det(M) Psi under the three generators: real dimension {dim}; "
        f"epsilon among them: {fixed}; so the A1 part is k epsilon alone, and the symmetric part (T1) holds none"
    )
    zero = [[g(0), g(0)], [g(0), g(0)]]
    moved = all(any(turned_spinor_law(m, T1[n]) != zero for m in GENERATORS.values()) for n in "xyz")
    print(f"       no T1 row is fixed by all three generators: {moved}")

    # 6c. the rule on k epsilon is the closure's det form, part for part
    agree = total = 0
    for k in (g(1), g(2, 1)):
        for sa, sb in product(("a", "a'"), ("b", "b'")):
            s_a, s_b = senses(SETTINGS[sa]), senses(SETTINGS[sb])
            for a, b in product((1, -1), (1, -1)):
                total += 1
                agree += norm(overlap2(s_a[a], s_b[b], scale(k, EPS))) == norm(k) * norm(
                    det(s_a[a], s_b[b])
                )
    print(
        f"   6c. on Psi = k epsilon (k = 1 and k = 2 + i) the rule's parts equal N(k) N(det[phi_A^a, phi_B^b]): "
        f"{agree} of {total}"
    )

    # 6d. the rule reads Psi: the same frames, other states laid at the fitting, other numbers
    print("   6d. the same rule and the same frames, with other states laid at the fitting:")
    states = [
        ("A1, k = 1 (the singlet)", EPS),
        ("A1, k = 2 + i", scale(g(2, 1), EPS)),
        ("T1 along x", T1["x"]),
        ("T1 along y", T1["y"]),
        ("T1 along z (the closure's plus-sign mutant)", T1["z"]),
        ("A1 beside T1 z (= 2 z+ (x) z-, a product)", mat_add(EPS, T1["z"])),
        ("a product, z+ (x) z-", outer(*AXES["z"])),
        ("a product, x+ (x) x-", outer(*AXES["x"])),
        ("a product, y+ (x) y-", outer(*AXES["y"])),
    ]
    for label, psi in states:
        s, _, whole_all, no_signal = s_of(psi)
        print(
            f"       {label}: S = {s} ({'|S| <= 2' if abs(s) <= 2 else '|S| above 2'}); "
            f"every far click whole: {whole_all}; no signalling: {no_signal}"
        )
    mix = {}
    for up, down in AXES.values():
        for chi_a, chi_b in ((up, down), (down, up)):
            _, e, _, _ = s_of(outer(chi_a, chi_b))
            for key, val in e.items():
                mix[key] = mix.get(key, Fraction(0)) + val / 6
    print(
        f"       the six Spoke directions, chi(n) (x) chi(-n), each a sixth (the owner's 'from the twins' state', "
        f"draft D's P10): S = {chsh(mix)}"
    )

    # 6e. no signalling for every laid state: A's four-part marginal never moves with B's frame
    entries = [g(0), g(1), g(-1), g(0, 1), g(1, 1), g(2, -1)]
    frames = [SETTINGS["b"], SETTINGS["b'"], (g(5), g(0, 2)), (g(1), g(1, 1))]
    moved = states_checked = 0
    for p, q, r, s in product(entries, repeat=4):
        psi = [[p, q], [r, s]]
        if not any(norm(x) for x in (p, q, r, s)):
            continue
        states_checked += 1
        for fa in (SETTINGS["a"], SETTINGS["a'"], (g(1), g(0, 1))):
            marg = set()
            for fb in frames:
                o = odds(fa, fb, psi)  # sorted keys: (-1, -1), (-1, 1), (1, -1), (1, 1)
                marg.add((o[0] + o[1], o[2] + o[3]))
            moved += len(marg) != 1
    print(
        f"   6e. no signalling for every state laid: A's odds move with B's frame in {moved} of "
        f"{states_checked * 3} (state, A frame) cases, B over four frames"
    )

    # 6f. the 24 on the composite: the A1 state's odds stand under every generator; a T1 state's turn with it
    inv = cov_ok = t1_moves = 0
    cases = 0
    for m in GENERATORS.values():
        for sa, sb in product(("a", "a'"), ("b", "b'")):
            fa, fb = SETTINGS[sa], SETTINGS[sb]
            cases += 1
            inv += odds(act(m, fa), act(m, fb), EPS) == odds(fa, fb, EPS)
            for n in "xyz":
                turned = mat_mul(mat_mul(m, T1[n]), transpose(m))
                cov_ok += odds(act(m, fa), act(m, fb), turned) == odds(fa, fb, T1[n])
                t1_moves += odds(act(m, fa), act(m, fb), T1[n]) != odds(fa, fb, T1[n])
    print(
        f"   6f. the 24: A1's four odds stand with both frames turned, {inv} of {cases}; a T1 state's stand when it turns "
        f"too, {cov_ok} of {3 * cases}; they move when it does not, {t1_moves} of {3 * cases}"
    )

    # 6g. mutants of part 6
    dim_mut = invariant_dim(turned_conjugate_law)
    identity = [[g(1), g(0)], [g(0), g(1)]]
    s_mut, _, _, _ = s_of(identity)
    print(
        f"   6g. mutant, the second index turned as a conjugate spinor (M Psi M^dagger): the fixed two-spinors have "
        f"real dimension {dim_mut}, the identity among them "
        f"{all(turned_conjugate_law(m, identity) == [[g(0), g(0)], [g(0), g(0)]] for m in GENERATORS.values())}; "
        f"laid at the fitting it gives S = {s_mut} ({'fails as it must' if s_mut != Fraction(-82, 29) else 'does not fail'})"
    )


SETTINGS = {
    "a": (g(1), g(0)),  # z, rho 1
    "a'": (g(1), g(1)),  # x, rho 2
    "b": (g(5), g(2)),  # (20, 0, 21), rho 29
    "b'": (g(5), g(-2)),  # (-20, 0, 21), rho 29
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
        print(
            f"   {sa:2s} {sb:2s}: E = {str(ex):>7s} (the singlet {str(singlet):>7s}, {'equal' if ex == singlet else 'apart'}); "
            f"far clicks of a whole {whole} of {room}; A up {a_up}"
        )
    s = chsh(e)
    print(
        f"   S = {s} = {float(s):.4f}; S^2 = {s * s} ({'above 4, at most 8' if 4 < s * s <= 8 else 'not in the band'})"
    )
    print(f"   every far click a click of a whole: {whole_all}")
    print(f"   no signalling: A's odds per setting pair {[(x, y, str(p)) for x, y, p in signal]}")

    print(
        "4. the control: the frames at the fitting are not the detectors' (B's setting changed after the fitting)"
    )
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
        print(f"   {name}: S = {s3} ({'fails as it must' if s3 != s else 'does not fail'})")
    complex_settings = {
        "a": (g(1), g(0)),  # z
        "a'": (g(1), g(0, 1)),  # y, rho 2
        "b": (g(5), g(0, 2)),  # (0, 20, 21), rho 29
        "b'": (g(5), g(0, -2)),  # (0, -20, 21), rho 29
    }
    for label, p in (
        ("the frames off the real plane (y and z): the head's perp", perp),
        (
            "the frames off the real plane: perp without the conjugates",
            mutants["perp without the conjugates"],
        ),
    ):
        e5 = {}
        for sa, sb in product(("a", "a'"), ("b", "b'")):
            fa, fb = complex_settings[sa], complex_settings[sb]
            e5[(sa, sb)] = run(fa, fb, fa, fb, perp_of=p)[0]
        s5 = chsh(e5)
        print(f"   {label}: S = {s5}")

    def plus(u, v):
        return add(mul(u[0], v[1]), mul(u[1], v[0]))

    e4 = {}
    for sa, sb in product(("a", "a'"), ("b", "b'")):
        fa, fb = SETTINGS[sa], SETTINGS[sb]
        e4[(sa, sb)] = run(fa, fb, fa, fb, det_of=plus)[0]
    s4 = chsh(e4)
    print(f"   the plus sign in det: S = {s4} ({'fails as it must' if s4 != s else 'does not fail'})")

    part6()


if __name__ == "__main__":
    main()
