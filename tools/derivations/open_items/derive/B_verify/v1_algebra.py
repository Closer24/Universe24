"""Verifier B: the draft's algebra re-derived with integers only, no engine, no code of the draft.

Run: python3 -I v1_algebra.py
Every part prints PASS or FAIL with its counts; each mutation must print FAIL (a probe that cannot fail proves nothing).
The engine's formulas are transcribed from the source by hand (rates.py, stretch/__init__.py, rule3.py, acts.py,
clock.turnover, tick.end_teeth); nothing is imported from the repository or from S/derive/B.
"""

import random

OUT = []


def say(*parts):
    line = " ".join(str(p) for p in parts)
    print(line, flush=True)
    OUT.append(line)


# ---------------------------------------------------------------- the carry (acts.carry, transcribed)
def carry(total, teeth, fine, going=1):
    flip = (lambda r: teeth - 1 - r) if going == -1 else (lambda r: r)
    carried = total + flip(fine)
    q = carried // teeth
    return q, flip(carried - teeth * q)


def rounded(n, d):
    """rates.rounded: half up on the magnitude, the sign after (d > 0)."""
    if n >= 0:
        return (n + n + d) // (d + d)
    return -((-n - n + d) // (d + d))


# ---------------------------------------------------------------- the rate table (the law's chain of carries)
TABLES = {}


def table(gamma, depth_hollow, depth_hill):
    """p0(c) for c in [-depth_hill, depth_hollow]: N_0 = Gamma^3, r_0 = Gamma div 2;
    hollows N(c+1) Gamma + r(c+1) = N(c)(Gamma - 1) + r(c); hills N(c-1)(Gamma-1) + r = N(c) Gamma + r(c)."""
    key = (gamma, depth_hollow, depth_hill)
    if key in TABLES:
        return TABLES[key]
    rate = {}
    n, r = gamma ** 3, gamma // 2
    for c in range(0, depth_hollow + 1):
        rate[c] = rounded(n, gamma * gamma)
        n, r = divmod(n * (gamma - 1) + r, gamma)
    n, r = gamma ** 3, (gamma - 1) // 2
    for c in range(0, -depth_hill - 1, -1):
        if c < 0:
            rate[c] = rounded(n, gamma * gamma)
        n, r = divmod(n * gamma + r, gamma - 1)
    TABLES[key] = rate
    return rate


def mesh_rate(gamma, p0):
    return rounded(p0 * p0, gamma)


def stretch_of(gamma, p0):
    """ceil(Gamma^5 / p0^4)."""
    return (gamma ** 5 + p0 ** 4 - 1) // p0 ** 4


def load_of(gamma, rate, x, low, high):
    """the largest a in [low, high] with Gamma^5 <= X p0(a)^4, by a plain scan from the top (no search shortcut)."""
    for a in range(high, low - 1, -1):
        if gamma ** 5 <= x * rate[a] ** 4:
            return a
    return None


def mesh_unit(gamma):
    g = 1
    while 2 * g * g * (2 * gamma - 1) <= gamma * gamma:
        g += 1
    return g


def mesh_factor(gamma, g, t):
    return (g * g * (gamma - t) ** 2 + (gamma * gamma) // 2) // (gamma * gamma)


def part1_rates():
    say("== 1. the rate table, the load reading, the floor's stretch (claims 1, 6)")
    for gamma in (1000, 6000):
        rate = table(gamma, 8 * gamma, gamma)
        stopped = next(c for c in range(0, 8 * gamma) if mesh_rate(gamma, rate[c]) == 0)
        zero = next((c for c in range(0, 8 * gamma) if rate[c] == 0), None)
        xf_head = stretch_of(gamma, rate[-gamma])
        say(f"Gamma {gamma}: X(0) = {stretch_of(gamma, rate[0])}, X_f head = X(-Gamma) = {xf_head},"
            f" stopped load {stopped} (rate {rate[stopped]}, X {stretch_of(gamma, rate[stopped])}), rate 0 at {zero}")
        # c >= 0 exactly where X >= Gamma, scanned over every X from the head's floor to 3 Gamma
        lo, hi = xf_head, 3 * gamma
        bad = 0
        for x in range(lo, hi + 1):
            c = load_of(gamma, rate, x, -gamma, 40)
            if (c >= 0) != (x >= gamma):
                bad += 1
        say(f"  c >= 0 iff X >= Gamma over X in [{lo}, {hi}]: {'PASS' if bad == 0 else 'FAIL'} ({bad} mismatches);"
            f" load_of(Gamma - 1) = {load_of(gamma, rate, gamma - 1, -gamma, 40)}, load_of(Gamma) = {load_of(gamma, rate, gamma, -gamma, 40)}")
        mono = all(rate[c + 1] <= rate[c] for c in range(-gamma, 8 * gamma))
        say(f"  p0 non-increasing on [-Gamma, 8 Gamma]: {'PASS' if mono else 'FAIL'}")


# ---------------------------------------------------------------- claims 1 and 2: the floor's invariant, the end teeth
def turn_tick(xm, x, xp, stopped, xf):
    """law 4 as clock.turnover reads it: x0 the held before, x1 the held now, x2 the now after the restore."""
    x0, x1, x2 = xm, x, (x if stopped else xp)
    top = (x0 <= x1 and x2 <= x1 and (x0 < x1 or x2 < x1)) or x0 < xf or x2 < xf
    if top:
        return (x0, x1), True          # (now, before) = (X-, X): the two notches exchanged
    if stopped:
        return (x1, x0), False         # restored
    return (x2, x1), False


def adversary(rng, gamma, xm, x):
    pick = rng.randrange(9)
    if pick == 0:
        return gamma - 1
    if pick == 1:
        return gamma
    if pick == 2:
        return -x - rng.randrange(0, 3)            # through the bottom within the tick
    if pick == 3:
        return 0
    if pick == 4:
        return x + rng.randrange(-x, x + 1)        # within one stretch of the start
    if pick == 5:
        return rng.randrange(-10 ** 30, 10 ** 30)
    if pick == 6:
        return x - rng.randrange(0, 2 * gamma)
    if pick == 7:
        return xm
    return x + rng.randrange(0, 10 ** 6)


def et3(half, xm, x, xp, stopped, xf):
    f = 1 if (xm < xf or xp < xf or stopped) else 0
    return half * (x + xp + f * (xm - xp)), f


def et3_signflip(half, xm, x, xp, stopped, xf):
    f = 1 if (xm < xf or xp < xf or stopped) else 0
    return half * (x + xp + f * (xp - xm)), f


def et3_factor(half, xm, x, xp, stopped, xf):
    f = 1 if (xm < xf or xp < xf or stopped) else 0
    return half * (x + xp + f * (x - xp)), f


def head_end_teeth(half, xm, x, xp):
    w = half * (x + xp)
    return w if w > 0 else half * (xm + x)


def part2_floor(floor_shift, et_form, label, clocks=400, ticks=400, seed=11):
    gamma, half = 1000, 3
    rng = random.Random(seed)
    xf = gamma - floor_shift
    state = [(gamma, gamma)] * clocks                  # (now, before): the setting at the full rate, both slots
    p_bad = load_bad = pos_bad = match_bad = fallback = discarded = 0
    rate = table(gamma, 40, gamma)
    for _ in range(ticks):
        new = []
        for (x, xm) in state:
            if min(x, xm) < gamma:
                p_bad += 1
            if load_of(gamma, rate, x, -gamma, 40) < 0:
                load_bad += 1
            xp = adversary(rng, gamma, xm, x)
            stopped = rng.randrange(50) == 0
            w, f = et_form(half, xm, x, xp, stopped, xf)
            discarded += f
            if w <= 0:
                pos_bad += 1
            head = head_end_teeth(half, xm, x, xp)
            if half * (x + xp) <= 0:
                fallback += 1
                if not f:
                    match_bad += 1                     # a fallback outside the discarded clocks
            if (not f) and w != half * (x + xp):
                match_bad += 1
            if half * (x + xp) <= 0 and w != head:
                match_bad += 1
            (nx, nb), _turned = turn_tick(xm, x, xp, stopped, xf)
            new.append((nx, nb))
        state = new
    ok = p_bad == 0 and load_bad == 0 and pos_bad == 0 and match_bad == 0
    say(f"  {label}: tick boundaries with a slot below Gamma {p_bad}, tick-start loads below 0 {load_bad},"
        f" end teeth <= 0 {pos_bad}, mismatches with the head's teeth {match_bad};"
        f" head fallbacks {fallback}, discarded clock-ticks {discarded} of {clocks * ticks}: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- claim 3: F2 above Gamma
def part3_upper():
    say("== 3. F2 above Gamma: Q = mesh_factor(t) (1 div (1 + t div Gamma)) against mesh_factor(min(max(t, 0), Gamma))")
    total = same = 0
    for gamma in list(range(2, 120)) + [1000, 6000, 23057]:
        g = mesh_unit(gamma)
        for t in range(0, 6 * gamma + 1):
            total += 1
            same += mesh_factor(gamma, g, t) * (1 // (1 + t // gamma)) == mesh_factor(gamma, g, min(max(t, 0), gamma))
    say(f"  exhaustive t in [0, 6 Gamma] at Gamma 2..119, 1000, 6000, 23057: {same} of {total} equal:"
        f" {'PASS' if same == total else 'FAIL'}")
    rng = random.Random(5)
    agree = 0
    for _ in range(20000):
        gamma = rng.randrange(2, 10 ** 12)
        g = rng.randrange(1, gamma)
        t = rng.randrange(0, 10 ** 40)
        agree += mesh_factor(gamma, g, t) * (1 // (1 + t // gamma)) == mesh_factor(gamma, g, min(t, gamma))
    say(f"  random Gamma < 10^12, any G < Gamma, t < 10^40: {agree} of 20000 equal: {'PASS' if agree == 20000 else 'FAIL'}")
    gamma, g = 1000, mesh_unit(1000)
    zero_div = sum(1 for t in range(-gamma, 0) if 1 + t // gamma == 0)
    minus = sorted({1 // (1 + t // gamma) for t in range(-5 * gamma, -gamma)})
    say(f"  below 0 at Gamma 1000: 1 + t div Gamma = 0 at {zero_div} of {gamma} tensions in [-Gamma, -1] (no factor);"
        f" e takes {minus} for t < -Gamma")
    # mutations of the indicator: where must the cut stand?
    def passes(cut_of):
        return all(
            mesh_factor(gamma, g, t) * (1 // (1 + t // cut_of)) == mesh_factor(gamma, g, min(t, gamma))
            for t in range(0, 6 * gamma + 1)
        )
    above = [d for d in range(1, 201) if passes(gamma + d)]
    below = [d for d in range(1, 201) if passes(gamma - d)]
    say(f"  MUTATION k = t div (Gamma + d), d in 1..200: passes at {len(above)} values, d = {above[:1]}..{above[-1:]}"
        f" ({'the cut is not pinned' if above else 'caught'})")
    say(f"  MUTATION k = t div (Gamma - d), d in 1..200: passes at {len(below)} values, d = {below[:1]}..{below[-1:]}")
    m2 = sum(mesh_factor(gamma, g, t) * (1 // (2 + t // gamma)) == mesh_factor(gamma, g, min(t, gamma)) for t in range(0, 6 * gamma + 1))
    say(f"  MUTATION e = 1 div (2 + k): {m2} of {6 * gamma + 1} equal: {'FAIL (caught)' if m2 < 6 * gamma + 1 else 'PASS (not caught)'}")
    zero_band = [t for t in range(0, 2 * gamma) if mesh_factor(gamma, g, t) == 0]
    say(f"  the head's factor is 0 already at t in [{zero_band[0]}, {zero_band[-1]}] (the rounding), G = {g}")


# ---------------------------------------------------------------- claim 4: the light's hold below 0
def hold_sign(gamma, g, tens, upper=False, lower=False):
    """S / (2 rim Gamma^2) = 6 G^2 - SUM_j Q_j at p_i = Gamma, two meshes per axis at the clock's own tension."""
    s = 6 * g * g
    for t in tens:
        tt = t
        if lower:
            tt = max(tt, 0)
        if upper:
            tt = min(tt, gamma)
        s -= 2 * mesh_factor(gamma, g, tt)
    return s


def part4_cone():
    say("== 4. F2 below 0: the light's hold S at the full rate with traceless tensions")
    gamma = 1000
    g = mesh_unit(gamma)
    R = 400
    nonzero = exc = exc_up = 0
    worst = 0
    exact_bad = 0
    for tx in range(-R, R + 1):
        for ty in range(-R, R + 1):
            tz = -tx - ty
            if tx == ty == 0:
                continue
            nonzero += 1
            if hold_sign(gamma, g, (tx, ty, tz)) >= 0:
                exc += 1
                worst = max(worst, tx * tx + ty * ty + tz * tz)
            if hold_sign(gamma, g, (tx, ty, tz), upper=True) >= 0:
                exc_up += 1
            # the exact (unrounded) form: 6 Gamma^2 - 2 SUM (Gamma - t_a)^2 = -2 SUM t_a^2
            lhs = 6 * gamma ** 2 - 2 * sum((gamma - t) ** 2 for t in (tx, ty, tz))
            if lhs != -2 * (tx * tx + ty * ty + tz * tz) or lhs >= 0:
                exact_bad += 1
    say(f"  exact identity 6 Gamma^2 - 2 SUM (Gamma - t_a)^2 = -2 SUM t_a^2 < 0, |t_x|,|t_y| <= {R}:"
        f" {nonzero - exact_bad} of {nonzero}: {'PASS' if exact_bad == 0 else 'FAIL'}")
    say(f"  with the head's rounding of Q: nonzero traceless tensions with S >= 0: {exc} of {nonzero};"
        f" largest SUM t_a^2 among them {worst} -> 'S < 0 at any nonzero tension' is"
        f" {'TRUE' if exc == 0 else 'FALSE on the integers (true above the rounding band)'}")
    examples = [(1, -1, 0), (1, 1, -2), (2, -1, -1), (3, -2, -1), (5, 5, -10)]
    say("  examples (t_x, t_y, t_z) -> 6 G^2 - SUM Q: " + ", ".join(f"{e} -> {hold_sign(gamma, g, e)}" for e in examples))
    say(f"  with the upper clamp kept (the lower struck): nonzero traceless tensions with S >= 0: {exc_up} of {nonzero}")
    # both clamps: S >= 0 for every tension, traceless or not, and through the rounding
    rng = random.Random(9)
    both_bad = 0
    for _ in range(200000):
        tens = tuple(rng.randrange(-5 * gamma, 5 * gamma) for _ in range(3))
        if hold_sign(gamma, g, tens, upper=True, lower=True) < 0:
            both_bad += 1
    say(f"  with both clamps: S < 0 at {both_bad} of 200000 random tensions: {'PASS' if both_bad == 0 else 'FAIL'}")
    # MUTATION: the lemma with one mesh per axis (the factor 2 dropped) must fail
    m_bad = sum(1 for tx in range(-50, 51) for ty in range(-50, 51)
                if 6 * gamma ** 2 - sum((gamma - t) ** 2 for t in (tx, ty, -tx - ty)) != -2 * (tx * tx + ty * ty + (tx + ty) ** 2))
    say(f"  MUTATION one mesh per axis: the identity fails at {m_bad} of {101 * 101}: {'FAIL (caught)' if m_bad else 'not caught'}")
    m_tr = sum(1 for t in range(1, 200) if 6 * gamma ** 2 - 2 * 3 * (gamma - t) ** 2 > 0)
    say(f"  MUTATION a trace (t, t, t), t in 1..199: S_exact > 0 at {m_tr} of 199: {'FAIL (caught)' if m_tr else 'not caught'}")


# ---------------------------------------------------------------- claim 5: F1's quotient
def part5_drive():
    say("== 5. F1: N / H with N = 4 X (F t rim Gamma^2 - sigma p0^2) p0, H = X t rim Gamma^4 key")
    rng = random.Random(7)
    ok = mut = xfree = cond = 0
    n = 20000
    for _ in range(n):
        x, f, t, rim = rng.randrange(1, 10 ** 12), rng.randrange(-10 ** 15, 10 ** 15), rng.randrange(1, 100), rng.randrange(1, 10 ** 17)
        gamma, key, p0, sig = rng.randrange(2, 10 ** 4), rng.randrange(1, 10 ** 6), rng.randrange(0, 10 ** 4), rng.randrange(-10 ** 25, 10 ** 25)
        N = 4 * x * (f * t * rim * gamma ** 2 - sig * p0 ** 2) * p0
        H = x * t * rim * gamma ** 4 * key
        A = 4 * f * p0 * t * rim * gamma ** 2 - 4 * sig * p0 ** 3
        B = t * rim * gamma ** 4 * key
        ok += N * B == H * A
        A2 = 4 * f * p0 * t * rim * gamma ** 2 - 4 * sig * p0 ** 2          # the brake's power changed
        mut += N * B == H * A2
        x2 = rng.randrange(1, 10 ** 12)
        N2 = 4 * x2 * (f * t * rim * gamma ** 2 - sig * p0 ** 2) * p0
        H2 = x2 * t * rim * gamma ** 4 * key
        xfree += N * H2 == N2 * H
        # at the full rate: |N| <= H iff 4 |F t rim - sigma| <= Gamma key t rim
        Nf = 4 * x * (f * t * rim * gamma ** 2 - sig * gamma ** 2) * gamma
        cond += (abs(Nf) <= H) == (4 * abs(f * t * rim - sig) <= gamma * key * t * rim)
    say(f"  N B = H A (the claimed form): {ok} of {n}: {'PASS' if ok == n else 'FAIL'}; X cancels: {xfree} of {n};"
        f" the full-rate condition: {cond} of {n}")
    say(f"  MUTATION the brake at p0^2: {mut} of {n} equal: {'FAIL (caught)' if mut < n else 'not caught'}")


# ---------------------------------------------------------------- claim 6: the stopped clock's own grips
def part6_zero():
    say("== 6. R10: the grips R_j = 2 pinion p_i^2 Q_j at the mesh rate 0")
    rng = random.Random(3)
    nz = 0
    for _ in range(100000):
        q, pinion = rng.randrange(-10 ** 9, 10 ** 9), rng.randrange(0, 10 ** 17)
        nz += (0 * 0 + 0 * 0) * q * pinion != 0
    say(f"  nonzero grips at p_i = 0 over 100000 random (Q, pinion): {nz}: {'PASS' if nz == 0 else 'FAIL'}")
    rate = table(1000, 8000, 1000)
    pi = [c for c in range(0, 8000) if mesh_rate(1000, rate[c]) == 0][:1]
    say(f"  at Gamma 1000 the mesh rate is 0 from the load {pi[0]} on, where the rate p0 is {rate[pi[0]]} (not 0):"
        f" the clock's own spring 12 (rim - pinion) p0^2 G^2 stays, so its gears are not frozen by the zero")


# ---------------------------------------------------------------- claim 7: the held load's reaction and its source
def part7_held():
    say("== 7. the held load: reaction over source = key (p0(c)^2 - p0(c + w)^2) / (2 w p0(c)^2), the bang's calibre")
    gamma, key, w = 1000, 36000, 2          # universe_bang.json: node_clock, quantum_action, the held row's weight
    rate = table(gamma, 4000, gamma)
    for c in (0, 10, 100, 1000, 3000):
        num = key * (rate[c] ** 2 - rate[c + w] ** 2)
        den = 2 * w * rate[c] ** 2
        q, r = divmod(num, den)
        say(f"  load {c}: p0 {rate[c]}, p0(c + w) {rate[c + w]}, ratio {q} + {r}/{den} (~ {num * 1000 // den / 1000})")
    say(f"  key div Gamma = {key // gamma} remainder {key % gamma}")
    # the exact exponential: the ratio is the same at every load
    num = key * (gamma ** (2 * w) - (gamma - 1) ** (2 * w))
    den = 2 * w * gamma ** (2 * w)
    say(f"  the exact exponential p0 = Gamma (1 - 1/Gamma)^c: ratio {num // den} + {num % den}/{den} at every load"
        f" (~ {num * 10000 // den / 10000}); the rise with the load is the table's rounding")


def part7_toy():
    """A toy with the two couplings of one weight: T a'' = -(D0 - beta phi) a, T phi'' = -K phi + s a^2.
    With s = (beta / 2) / lam the Lagrangian whose held part is weighted lam gives exactly these equations, so
    E_lam = T/2 a'^2 + (D0 - beta phi) a^2 / 2 + lam (T/2 phi'^2 + K phi^2 / 2) is kept and E_1 is not.
    Integers: fixed point at the scale 2^120, the Stormer-Verlet step (symplectic: its error is bounded, O(1/T)).
    omega_phi = 2 omega_a, so the light parametric resonance moves the energy between the two."""
    say("== 7b. toy: the source the reaction over lam; which energy is kept?")
    S = 1 << 120
    T, D0, K = 10000, 25, 100

    def run(lam_dyn, lam_read, beta, ticks=120000):
        a, phi, va, vphi = S, 0, 0, 0

        def force(a, phi):
            fa = -((D0 * S - beta * phi) * a // S)
            fphi = -K * phi + (beta * a * a // S) // (2 * lam_dyn)
            return fa, fphi

        def energy(a, phi, va, vphi, lam):
            kin_a = T * va * va // (2 * S)
            pot_a = (D0 * S - beta * phi) * (a * a // S) // (2 * S)
            held = T * vphi * vphi // (2 * S) + K * phi * phi // (2 * S)
            return kin_a + pot_a + lam * held, held

        fa, fp = force(a, phi)
        e0, _ = energy(a, phi, va, vphi, lam_read)
        dev, held_max = 0, 0
        for _ in range(ticks):
            va += fa // (2 * T)
            vphi += fp // (2 * T)
            a += va
            phi += vphi
            fa, fp = force(a, phi)
            va += fa // (2 * T)
            vphi += fp // (2 * T)
            e, held = energy(a, phi, va, vphi, lam_read)
            dev = max(dev, abs(e - e0))
            held_max = max(held_max, held)
        return dev * 10 ** 6 // e0, held_max * lam_dyn * 10 ** 6 // e0

    for lam_dyn, lam_read, beta, what in ((36, 36, 72, "source = reaction / 36, E read with the held part x 36"),
                                          (36, 1, 72, "source = reaction / 36, E read with every part x 1 (the draft's reading)"),
                                          (1, 1, 2, "control: source = reaction (beta 2), E read x 1"),
                                          (1, 36, 2, "control: source = reaction (beta 2), E read with the held part x 36")):
        dev, held = run(lam_dyn, lam_read, beta)
        say(f"  {what}: largest |E - E(0)| / E(0) = {dev} ppm (the held part reached {held} ppm of E(0) in weighted terms)")


# ---------------------------------------------------------------- claim 8: the release's identities
def part8_release():
    say("== 8. the release: u_h = pinion div rim, c_h = 1 - u_h, the kick, the merged recoil")
    i1 = i1n = 0
    for rim in range(1, 301):
        for pinion in range(0, rim + 1):
            i1n += 1
            i1 += (1 - pinion // rim) == min(rim - pinion, 1)
    neg = [(p, 13, 1 - p // 13, min(13 - p, 1)) for p in (-13, -12, -5, -1)]
    negbad = sum(1 for rim in range(1, 301) for pinion in range(-rim, 0) if (1 - pinion // rim) != min(rim - pinion, 1))
    say(f"  I1 on 0 <= pinion <= rim <= 300: {i1} of {i1n}: {'PASS' if i1 == i1n else 'FAIL'}")
    say(f"  I1 on -rim <= pinion < 0 (the loader refuses only pinion >= rim): fails at {negbad} of {sum(range(1, 301))};"
        f" (pinion, rim, 1 - pinion div rim, min(rim - pinion, 1)) = {neg}")
    rng = random.Random(1)
    i2 = m2 = 0
    for _ in range(100000):
        W = rng.randrange(1, 10 ** 30)
        p, q = rng.randrange(-10 ** 40, 10 ** 40), rng.randrange(-10 ** 9, 10 ** 9)
        mid = W // 2
        lhs = divmod(p + W * q + mid, W)
        a0, r0 = divmod(p + mid, W)
        i2 += lhs == (a0 + q, r0)
        m2 += divmod(p + W * q + 1 + mid, W) == (a0 + q, r0)
    say(f"  I2 the advance after the carry = the kick W+ q before it: {i2} of 100000: {'PASS' if i2 == 100000 else 'FAIL'};"
        f" MUTATION kick W+ q + 1: {m2} of 100000 equal: {'FAIL (caught)' if m2 < 100000 else 'not caught'}")
    i3 = m3 = 0
    for _ in range(100000):
        T = rng.randrange(1, 10 ** 20)
        r0 = rng.randrange(0, T)
        n1, n2 = rng.randrange(-10 ** 30, 10 ** 30), rng.randrange(-10 ** 30, 10 ** 30)
        good = bad = True
        for going in (1, -1):
            q1, r1 = carry(n1, T, r0, going)
            q2, r2 = carry(n2, T, r1, going)
            Q, R = carry(n1 + n2, T, r0, going)
            good &= (Q, R) == (q1 + q2, r2)
            q2b, r2b = carry(n2, T, r0, going)              # the remainder not carried between the two drives
            bad &= (Q, R) == (q1 + q2b, r2b)
        i3 += good
        m3 += bad
    say(f"  I3 two drives at one teeth = one drive of the sum, at +1 and -1: {i3} of 100000: {'PASS' if i3 == 100000 else 'FAIL'};"
        f" MUTATION the remainder not carried: {m3} of 100000 equal: {'FAIL (caught)' if m3 < 100000 else 'not caught'}")
    z = all(carry(0, T, r, g) == (0, r) for T in (1, 2, 7, 36000) for r in range(0, T) for g in (1, -1))
    say(f"  the carry of 0 at the key leaves its remainder (u_h = 0), at +1 and -1: {'PASS' if z else 'FAIL'}")


if __name__ == "__main__":
    part1_rates()
    say("== 1/2. the floor's invariant P(t) and the end teeth, law 4's trigger on adversarial raw outputs X+")
    part2_floor(0, et3, "X_f = Gamma, ET3")
    part2_floor(1, et3, "MUTATION X_f = Gamma - 1, ET3")
    part2_floor(0, et3_signflip, "MUTATION ET3 with f (X+ - X-)")
    part2_floor(0, et3_factor, "MUTATION ET3 with f (X - X+)")
    part3_upper()
    part4_cone()
    part5_drive()
    part6_zero()
    part7_held()
    part7_toy()
    part8_release()
