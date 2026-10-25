"""Hand r5 (2026-10-25), part (b): a riding remainder at a wall symmetric in the Node's two levels, on a ring toy with one
light line and one volume time line per Node, integers only.

Two forms of the ride, each with the fifth act (the swap at the weak maximum of the Node's own volume, the levels
exchanged and every remainder complemented at its wall):

R: R4's form A (the engine under U24_RIDES=2/3): the light divides at w X_now, its remainder born at w X_before, the
   half-wall move (w (X_now - X_before)) div 2; the volume's write sourced by the two-level form of the pair the step leaves,
   [w (next^2 + now^2) - S next now - next SUM R m] div w; the order forward light then volume, backward volume then light;
   the light's remainder complemented at the mean wall (w div 2)(X0 + X1) (R3's mend).
S: the symmetric ride derived here: the light's momentum P = W (a_now - a_before) + r with W = (w div 2)(X_before + X_now),
   the wall of the half interval the momentum lives on, symmetric in the two levels; the kick P_c_out = P_c_in + X_now F
   (P_c = P - W div 2, the half wall's centring); the volume's write sourced by the momenta before the division,
   u_in u_out + [a SUM R (a - m)] div w with u = round(Q / (2 w X_now)), Q = 2 P_c + 1 (the odd rounding, exactly odd since
   Q is odd and 2 w X_now even: never a half); the volume steps (one division at its wall E); then the light divides once
   at W_out = (w div 2)(X_now + X_next). Backward: the light's numerator from the post-state at W_out, the kick back, the
   same source, the volume back, the light's division at W_in. The light's remainder complemented at its own wall W.

Measured: (1) the step's bijection on random states (G(F(S)) = S); (2) M = swap o step an involution, M(M(S)) = S, on
random states; (3) a run of N intervals on the ring with single-Node tops, the per-step inverse from every true post-state
by the former reading (the triple (Y.before, Z.before, Z.now), rule B) and by the forward act on the swapped state
(rule A): matches, misses and false tops; (4) the chained run back; (5) the widest integer. Output symmetric_ride.json."""

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 12  # the ring
W_LIGHT = 24 * 1021  # w, divisible by 4 (the engine's w = 6 den Gamma^2 G^2 is, Gamma even)
R = W_LIGHT // 3  # the massless reach at the vacuum's paces, R / w = 1 / 3
S_SELF = 2 * W_LIGHT - 2 * R  # the self coefficient of the massless ring line (D = 0)
E = 1 << 16  # the volume line's wall
KAPPA = E // 40  # the volume's restoring term (its own oscillation)
X_BASE = 1000
GAIN = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def top(x0, x1, x2):
    return x0 <= x1 and x2 <= x1 and (x0 < x1 or x2 < x1)


def links(a, i):
    return a[(i - 1) % N] + a[(i + 1) % N]


def force(a, i):
    return R * (links(a, i) - 2 * a[i])


def odd_round(q, d):
    """round(q / d) to the nearest, q odd and d even (never a half): (2 q + d) div (2 d)."""
    return (2 * q + d) // (2 * d)


def pot(a, i):
    return (a[i] * R * (2 * a[i] - links(a, i))) // W_LIGHT


# a state: (a, b, r, X, Xb, rho), each a list over the ring; a = light now, b = light before, r = its remainder;
# X = volume now, Xb = volume before, rho = the volume line's remainder at E


def vol_forward(X, Xb, rho, src):
    num = E * (2 * X - Xb) + GAIN * src - KAPPA * (X - X_BASE) + rho
    return num // E, num % E


def vol_back(X, Xn, rho2, src):
    v = E * (2 * X - Xn) + GAIN * src - KAPPA * (X - X_BASE) - rho2
    xb = -((-v) // E)
    return xb, E * xb - v


def step(form, s):
    a, b, r, X, Xb, rho = s
    na, nr, nX, nrho = [0] * N, [0] * N, [0] * N, [0] * N
    for i in range(N):
        f = force(a, i)
        if form == "R":
            move = (W_LIGHT * (X[i] - Xb[i])) // 2
            num = X[i] * f + W_LIGHT * X[i] * a[i] + W_LIGHT * Xb[i] * (a[i] - b[i]) + move + r[i]
            na[i], nr[i] = num // (W_LIGHT * X[i]), num % (W_LIGHT * X[i])
            src = (W_LIGHT * (na[i] ** 2 + a[i] ** 2) - S_SELF * na[i] * a[i] - na[i] * R * links(a, i)) // W_LIGHT
            nX[i], nrho[i] = vol_forward(X[i], Xb[i], rho[i], src)
        else:
            w_in = (W_LIGHT // 2) * (Xb[i] + X[i])
            p_in = w_in * (a[i] - b[i]) + r[i] - w_in // 2
            p_out = p_in + X[i] * f
            d = 2 * W_LIGHT * X[i]
            src = odd_round(2 * p_in + 1, d) * odd_round(2 * p_out + 1, d) + pot(a, i)
            nX[i], nrho[i] = vol_forward(X[i], Xb[i], rho[i], src)
            w_out = (W_LIGHT // 2) * (X[i] + nX[i])
            v, nr[i] = divmod(p_out + w_out // 2, w_out)
            na[i] = a[i] + v
    return (na, list(a), nr, nX, list(X), nrho)


def inverse(form, z):
    """The step back from a post-state z = (next, now, r', X_next, X_now, rho'), the acts in the reverse order."""
    n, a, r2, Xn, X, rho2 = z
    b, r, Xb, rho = [0] * N, [0] * N, [0] * N, [0] * N
    for i in range(N):
        f = force(a, i)
        if form == "R":
            src = (W_LIGHT * (n[i] ** 2 + a[i] ** 2) - S_SELF * n[i] * a[i] - n[i] * R * links(a, i)) // W_LIGHT
            Xb[i], rho[i] = vol_back(X[i], Xn[i], rho2[i], src)
            move = (W_LIGHT * (X[i] - Xb[i])) // 2
            u = X[i] * f + W_LIGHT * X[i] * a[i] + W_LIGHT * Xb[i] * a[i] + move - W_LIGHT * X[i] * n[i] - r2[i]
            wall = W_LIGHT * Xb[i]
            b[i] = -((-u) // wall)
            r[i] = wall * b[i] - u
        else:
            w_out = (W_LIGHT // 2) * (X[i] + Xn[i])
            p_out = w_out * (n[i] - a[i]) + r2[i] - w_out // 2
            p_in = p_out - X[i] * f
            d = 2 * W_LIGHT * X[i]
            src = odd_round(2 * p_in + 1, d) * odd_round(2 * p_out + 1, d) + pot(a, i)
            Xb[i], rho[i] = vol_back(X[i], Xn[i], rho2[i], src)
            w_in = (W_LIGHT // 2) * (Xb[i] + X[i])
            v, r[i] = divmod(p_in + w_in // 2, w_in)
            b[i] = a[i] - v
    return (list(a), b, r, list(X), Xb, rho)


def swap_wall(form, x_before, x_now):
    return (W_LIGHT // 2) * (x_before + x_now)  # R: R3's mean wall; S: the remainder's own wall, the same expression


def swapped(form, s, mask):
    a, b, r, X, Xb, rho = s
    out = [list(v) for v in s]
    for i in range(N):
        if mask[i]:
            out[0][i], out[1][i] = b[i], a[i]
            out[2][i] = swap_wall(form, Xb[i], X[i]) - 1 - r[i]
            out[3][i], out[4][i] = Xb[i], X[i]
            out[5][i] = E - 1 - rho[i]
    return tuple(out)


def interval(form, s):
    """The five acts' map: the step, and where the Node's own volume reads a weak maximum, the swap of the pre-state."""
    z = step(form, s)
    mask = [top(s[4][i], s[3][i], z[3][i]) for i in range(N)]
    sw = swapped(form, s, mask)
    out = tuple([sw[k][i] if mask[i] else z[k][i] for i in range(N)] for k in range(6))
    return out, mask


def back(form, z, rule):
    """One interval back: rule B, the triple (Y.before, Z.before, Z.now) of the engine's inverse Y; rule A, the forward
    act on the swapped state (the candidate tau Z, its own step's triple)."""
    y = inverse(form, z)
    if rule == "B":
        mask = [top(y[4][i], z[4][i], z[3][i]) for i in range(N)]
    else:
        cand = swapped(form, z, [True] * N)
        f = step(form, cand)
        mask = [top(cand[4][i], cand[3][i], f[3][i]) for i in range(N)]
    sw = swapped(form, z, mask)
    return tuple([sw[k][i] if mask[i] else y[k][i] for i in range(N)] for k in range(6)), mask


def random_state(rng, levels):
    X = [rng.randint(400, 3000) for _ in range(N)]
    Xb = [x + rng.randint(-200, 200) for x in X]
    a = [rng.randint(-levels, levels) for _ in range(N)]
    b = [rng.randint(-levels, levels) for _ in range(N)]
    r = [rng.randrange(W_LIGHT * Xb[i]) if True else 0 for i in range(N)]
    rho = [rng.randrange(E) for _ in range(N)]
    return (a, b, r, X, Xb, rho)


def random_state_s(rng, levels):
    a, b, _r, X, Xb, rho = random_state(rng, levels)
    r = [rng.randrange((W_LIGHT // 2) * (Xb[i] + X[i])) for i in range(N)]
    return (a, b, r, X, Xb, rho)


def widest(s):
    return max(abs(int(v)).bit_length() for part in s for v in part)


def lay(form, amplitude):
    a = [amplitude if i % 4 == 0 else (-amplitude if i % 4 == 2 else 0) for i in range(N)]
    a[0] = 2 * amplitude  # one antinode larger: its Node's volume tops alone
    b = [0] * N
    X, Xb = [X_BASE] * N, [X_BASE] * N
    if form == "R":
        r = [(W_LIGHT * X_BASE) // 2] * N
    else:
        r = [((W_LIGHT // 2) * 2 * X_BASE) // 2] * N
    return (a, b, r, X, Xb, [E // 2] * N)


def run(form, amplitude, intervals):
    s = lay(form, amplitude)
    states, masks, bits = [s], [None], widest(s)
    single, singles_big = 0, 0
    for _ in range(intervals):
        s, mask = interval(form, s)
        states.append(s)
        masks.append(mask)
        bits = max(bits, widest(s))
        if sum(mask) == 1:
            single += 1
            i = mask.index(True)
            pre = states[-2]
            if abs(pre[0][i] - pre[1][i]) >= 50:
                singles_big += 1
    found = {"form": form, "amplitude": amplitude, "intervals": intervals, "turned_nodes": sum(sum(m) for m in masks[1:]), "single_node_turn_intervals": single, "single_node_turns_with_light_velocity_50_or_more": singles_big, "X_range": [min(min(st[3]) for st in states), max(max(st[3]) for st in states)], "widest_bits": bits}
    for rule in ("B", "A"):
        matched, misses, false = 0, 0, 0
        for t in range(intervals, 0, -1):
            pre, m = back(form, states[t], rule)
            matched += pre == tuple(list(v) for v in states[t - 1])
            truth = masks[t]
            misses += sum(1 for i in range(N) if truth[i] and not m[i])
            false += sum(1 for i in range(N) if m[i] and not truth[i])
        chained, z, first = 0, states[-1], None
        for t in range(intervals, 0, -1):
            z, _m = back(form, z, rule)
            ok = z == tuple(list(v) for v in states[t - 1])
            chained += ok
            if not ok and first is None:
                first = t
                z = states[t - 1]  # reset to the truth to count the later steps
        found[f"rule_{rule}"] = {"per_step_matched": matched, "misses": misses, "false_tops": false, "chained_matched_with_resets": chained, "first_unmatched": first}
    return found


if __name__ == "__main__":
    rng = random.Random(20261025)
    found = {"gain": GAIN, "w": W_LIGHT, "R": R, "E": E, "kappa": KAPPA, "ring": N}
    for form, maker in (("R", random_state), ("S", random_state_s)):
        bij, invol, cases = 0, 0, 20000 // N
        for _ in range(cases):
            s = maker(rng, 3000)
            if inverse(form, step(form, s)) == s:
                bij += 1
            m1 = swapped(form, step(form, s), [True] * N)
            m2 = swapped(form, step(form, m1), [True] * N)
            if m2 == s:
                invol += 1
        found[f"random_{form}"] = {"boards": cases, "nodes_per_board": N, "step_bijection_boards": bij, "M_involution_boards": invol}
    amplitudes = [int(a) for a in sys.argv[2:]] or [300, 1200]
    for form in ("R", "S"):
        for amplitude in amplitudes:
            try:
                found[f"run_{form}_{amplitude}"] = run(form, amplitude, 300)
            except ZeroDivisionError:
                found[f"run_{form}_{amplitude}"] = "the volume reached 0 at a Node (a wall of 0): the run ends, named"
    tag = "" if not sys.argv[2:] else "_A" + "_".join(sys.argv[2:])
    out = HERE / f"symmetric_ride_g{GAIN}{tag}.json"
    out.write_text(json.dumps(found, indent=1), encoding="utf-8")
    print(json.dumps(found, indent=1))
