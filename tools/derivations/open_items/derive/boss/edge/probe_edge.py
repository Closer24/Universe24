"""Clock: the edge's probe, on the Node-clock's own load and act in whole numbers: the velocity's tooth on the edge
between the two slots, measured for the 24, the mirror and the run back, the momentum, the still clock, the fixed point
of the 00 slot, the even-count rule's cost, and the click's books, each with its "no" mutant.
Algebra: the engine's carry is the one division; the centred split (edge_lib.split) is two carries and lit().
Board: a cube of side 3, 18 rows at 27 sites, 486 gears; the 00 slot standing, rising and falling by whole counts.
Clicks: section 8 reads the carry of an area at a key, the click's algebra, with no click on the board (G5).

Run: <t24b>/.venv/bin/python -I probe_edge.py > probe_edge.txt
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402

import edge_lib as E  # noqa: E402
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402

ROUNDS = 40
SEED = 6
GRIP = E.grip_of(E.universe())  # the example universe's den Gamma^2: the Mesh unit and the fine teeth's pitch at J = 0
# the lays, (a00, b00) counts of the 00 slot: W = 6 grips + a00, moving by a00 - b00 a round; D = W(b) + W(a) is odd
# exactly where a00 + b00 is odd
LAYS = [
    (3 * GRIP, 3 * GRIP),
    (4 * GRIP, 3 * GRIP),
    (4 * GRIP, 3 * GRIP - 1),
    (4 * GRIP, 2 * GRIP),
    (40 * GRIP, 41 * GRIP),
    (40 * GRIP, 41 * GRIP + 1),
    (120 * GRIP, 123 * GRIP),
]
MUTANT_LAYS = (LAYS[0], LAYS[1], LAYS[4])


def compact(held):
    """A per-round list printed whole where it varies and summed where it does not."""
    if len(set(held)) == 1:
        return f"{held[0]} at every one of the {len(held)} rounds"
    return str(held)


def built_state(s):
    """The lay read as the act as built's state: the tooth |t|, at most 5 grips, within every W of at least 6 grips."""
    return State(s.a, s.b, abs(s.r), s.rd)


def even(x):
    """1 where x is even, by one carry."""
    _, rest = carry(x, 2, 0)
    return int(rest == 0)


def grips(x):
    return E.in_grips(int(x), GRIP)


def tidy(xs):
    """A row list for the report: each entry as it is below a grip, else in grips or grips^2."""
    return "[" + ", ".join(E.tidy(x, GRIP) for x in xs) + "]"


def section_1():
    print("1. The split at the dial 2 D, centred, the edge taken even")
    window = range(-300, 301)
    misses_bij = misses_neg = 0
    ties = misses_up = misses_floor = 0
    for d in range(1, 13):
        m = 2 * d
        seen = set()
        for n in window:
            q, s = E.split(n, m)
            ok = (abs(s) < d) or (abs(s) == d and even(q))
            if q * m + s != n or not ok or (q, s) in seen:
                misses_bij += 1
            seen.add((q, s))
            qn, sn = E.split(-n, m)
            if (qn, sn) != (-q, -s):
                misses_neg += 1
            if abs(s) == d:
                ties += 1
            qu, su = E.split_up(n, m)
            qun, sun = E.split_up(-n, m)
            if (qun, sun) != (-qu, -su):
                misses_up += 1
            qf, sf = E.split_floor(n, m)
            qfn, sfn = E.split_floor(-n, m)
            if (qfn, sfn) != (-qf, -sf):
                misses_floor += 1
    print(f"   n in [-300, 300], D in [1, 12] (dials 2 D from 2 to 24), {len(window) * 12} cases:")
    print(f"   n = q 2D + s with |s| <= D, the edge |s| = D only at an even q, each pair once: {misses_bij} misses;")
    print(f"   split(-n) = (-q, -s), a sign flip a negation: {misses_neg} misses; ties (|s| = D) among the cases: {ties}.")
    print(f"   The mutant, the tie taken upward (the plain carry from the half): {misses_up} misses of the negation,")
    print(f"   exactly the ties; the mutant, the plain carry (s in [0, 2D)): {misses_floor} misses.")
    print()


def section_2():
    print("2. The 24 on moving clocks, 40 rounds (tick^n(turned s) = turned(tick^n s), of the 24 turns)")
    print("   The edge act's turn: rows and sites by the turn, the tooth of a flipped row negated; the act as built's:")
    print("   the tooth of a flipped row reflected in the teeth of the round that kept it (the before slot's).")
    results = {}
    for a00, b00 in LAYS:
        layout, s0, trains = E.board(a00, b00, seed=SEED)
        r00 = E.row_00(trains)
        turns = E.twenty_four(trains)
        states, broke = E.forward(E.edge_tick, E.edge_promise, layout, s0, ROUNDS)
        wa, wb, d = E.dials(layout, states[0].a, states[0].b)
        wa_end, _, d_end = E.dials(layout, states[-1].a, states[-1].b)
        parities = sorted({1 - even(x) for st in states for x in E.dials(layout, st.a, st.b)[2][0]})
        held = [E.holds_edge(layout, states, p, site) for (_, p, site) in turns]
        per_round = [sum(h[n] for h in held) for n in range(len(states) - 1)]
        results[(a00, b00)] = per_round
        print(f"   Lay {E.lay_name(a00, b00, GRIP)}: {s0.a.size} gears ({s0.a.shape[0]} rows x {s0.a.shape[1]} sites); W from"
              f" {grips(wa[0, 0])} to {grips(wa_end[0, 0])} on the rows that read the 00 slot (the 00 row's own teeth at rest,"
              f" {grips(wa[r00, 0])}), D from {grips(d[0, 0])} to {grips(d_end[0, 0])}, D's parities {parities} (0 even, 1 odd),"
              f" the counts reach {E.bits(states)} bits, the edge's promise held at every round (broke: {broke}).")
        print(f"     edge act: {compact(per_round)}")
        if (a00, b00) in MUTANT_LAYS:
            layout_b, s0b, _ = E.board(a00, b00, seed=SEED, cut=False)
            stb, brb = E.forward(step.tick, E.built_promise, layout_b, built_state(s0b), ROUNDS)
            heldb = [E.holds_in_dial(layout_b, stb, p, site, step.tick, E.built_dial) for (_, p, site) in turns]
            print(f"     the act as built (the loader's lay): {compact([sum(h[n] for h in heldb) for n in range(len(stb) - 1)])}"
                  f"{'' if brb is None else f'; its promise breaks before round {brb + 1}'}")
            heldn = [E.holds_edge(layout, states, p, site, negate=False) for (_, p, site) in turns]
            print(f"     mutant, the edge act with the tooth moved and not negated: {compact([sum(h[n] for h in heldn) for n in range(ROUNDS)])}")
            tick_floor = lambda lay, st: E.edge_tick(lay, st, E.split_floor)  # noqa: E731
            s0f = State(s0.a, s0.b, abs(s0.r), s0.rd)
            stf, brf = E.forward(tick_floor, lambda lay, st: True, layout, s0f, ROUNDS)
            heldf_neg = [E.holds_edge(layout, stf, p, site, tick=tick_floor) for (_, p, site) in turns]
            heldf_dial = [E.holds_in_dial(layout, stf, p, site, tick_floor, E.edge_dial) for (_, p, site) in turns]
            print(f"     mutant, the plain carry on the edge's dial (s in [0, 2D)) with the negation: {compact([sum(h[n] for h in heldf_neg) for n in range(ROUNDS)])}")
            print(f"     the same plain carry with the flip 2D - 1 - s in the dial the tooth lives on (2 D_in): {compact([sum(h[n] for h in heldf_dial) for n in range(ROUNDS)])}"
                  " (the plain carry's flip is its own dial's, 2 D_out, which is not the tooth's where the clock moves)")
            tick_up = lambda lay, st: E.edge_tick(lay, st, E.split_up)  # noqa: E731
            stu, _ = E.forward(tick_up, lambda lay, st: True, layout, s0, ROUNDS)
            heldu = [E.holds_edge(layout, stu, p, site, tick=tick_up) for (_, p, site) in turns]
            ties = []
            for n in range(1, len(stu)):
                _, _, dn = E.dials(layout, stu[n].a, stu[n].b)
                ties.append(int((abs(stu[n].r) == dn).sum()))
            print(f"     mutant, the tie taken upward: {compact([sum(h[n] for h in heldu) for n in range(ROUNDS)])};"
                  f" teeth standing on the edge of their dial per round: {ties if len(set(ties)) > 1 else compact(ties)}")
    print()
    return results


def section_3():
    print("3. The mirror as its own inverse, and the run back (untick(tick s) = s at every round; the whole rewind)")
    for a00, b00 in [LAYS[1], LAYS[2], LAYS[4], LAYS[5], LAYS[6], LAYS[0]]:
        layout, s0, trains = E.board(a00, b00, seed=SEED)
        states, _ = E.forward(E.edge_tick, E.edge_promise, layout, s0, ROUNDS)
        ran = len(states) - 1
        twice = sum(0 if E.same(E.edge_mirror(layout, E.edge_mirror(layout, st)), st) else 1 for st in states)
        back = [int(E.same(E.edge_untick(layout, states[n + 1]), states[n])) for n in range(ran)]
        end = states[-1]
        for _ in range(ran):
            end = E.edge_untick(layout, end)
        rewound = E.same(end, states[0])
        mutant = [int(E.same(E.edge_untick(layout, states[n + 1], mirror=E.edge_mirror_unnegated), states[n])) for n in range(ran)]
        print(f"   Lay {E.lay_name(a00, b00, GRIP)}: edge act: mirror(mirror s) = s at {len(states) - twice} of {len(states)} states;"
              f" untick(tick s) = s in {sum(back)} of {ran} rounds; the {ran} rounds rewound to the start bit for bit: {rewound};")
        print(f"     mutant, the mirror with the tooth kept and not negated: untick(tick s) = s in {sum(mutant)} of {ran} rounds.")
        # the floor form on the edge: the plain carry at 2 D_out, the mirror's flip in the dial the tooth lives on
        tick_floor = lambda lay, st: E.edge_tick(lay, st, E.split_floor)  # noqa: E731

        def mirror_floor(lay, st):
            _, _, d = E.dials(lay, st.a, st.b)
            _, _, _, teeth = lay.gearing
            return State(st.b, st.a, flip(st.r, 2 * d), flip(st.rd, teeth))

        s0f = State(s0.a, s0.b, abs(s0.r), s0.rd)
        stf = [s0f]
        for _ in range(ran):
            stf.append(tick_floor(layout, stf[-1]))
        backf = [int(E.same(mirror_floor(layout, tick_floor(layout, mirror_floor(layout, stf[n + 1]))), stf[n])) for n in range(ran)]
        print(f"     mutant, the plain carry on the edge's dial with the flip 2D - 1 - s: untick(tick s) = s in {sum(backf)} of {ran} rounds.")
        layout_b, s0b, _ = E.board(a00, b00, seed=SEED, cut=False)
        sb = built_state(s0b)
        stb = [sb]
        for _ in range(ROUNDS):
            stb.append(step.tick(layout_b, stb[-1]))
        backb = [int(E.same(step.untick(layout_b, stb[n + 1]), stb[n])) for n in range(ROUNDS)]
        twiceb = sum(int((step.mirror(layout_b, step.mirror(layout_b, st)).r != st.r).sum()) for st in stb)
        promise_broke = next((n for n, st in enumerate(stb) if not E.built_promise(layout_b, st)), None)
        print(f"     the act as built, no promise asked: untick(tick s) = s in {sum(backb)} of {ROUNDS} rounds; mirror(mirror s) moves"
              f" the tooth at {twiceb} gear-states of {len(stb) * sb.a.size} (by W(a) - W(b)); its promise first breaks at round {promise_broke}.")
    print()


def section_4():
    print("4. The momentum in the edge's teeth: per row P = SUM over the sites of 2 D_in (a - b) + t, in half-teeth")
    for a00, b00 in [LAYS[1], LAYS[4], LAYS[0]]:
        layout, s0, trains = E.board(a00, b00, seed=SEED)
        states, _ = E.forward(E.edge_tick, E.edge_promise, layout, s0, ROUNDS)
        rows = s0.a.shape[0]
        misses_books = misses_zero = 0
        for n in range(ROUNDS):
            p0, _ = E.row_books_edge(layout, states[n])
            p1, _ = E.row_books_edge(layout, states[n + 1])
            push = E.pushes_sum(layout, states[n])
            misses_books += int((p1 - p0 != 4 * push).sum())
            misses_zero += int((push != 0).sum())
        p_first, s_first = E.row_books_edge(layout, states[0])
        p_last, s_last = E.row_books_edge(layout, states[-1])
        dp = (p_last - p_first).tolist()
        _, _, d_first = E.dials(layout, states[0].a, states[0].b)
        _, _, d_last = E.dials(layout, states[-1].a, states[-1].b)
        print(f"   Lay {E.lay_name(a00, b00, GRIP)}: P_(t+1) - P_t = 4 SUM push: {misses_books} misses over {rows} rows x {ROUNDS} rounds;"
              f" SUM push = 0 (the Meshes' pull alike from both ends, J = 0): {misses_zero} misses;")
        print(f"     P_40 - P_0 per row: {tidy(dp)};")
        print(f"     S_0 per row (S the sum of a - b): {tidy(s_first.tolist())}")
        print(f"     S_40 per row: {tidy(s_last.tolist())}")
        print(f"     (P kept exactly; S re-split at the dial, D from {grips(d_first[0, 0])} to {grips(d_last[0, 0])}: S ~ (P - SUM t) over 2 D, the"
              f" velocities fall as the clock rises and rise as it falls, no drift);")
        layout_b, s0b, _ = E.board(a00, b00, seed=SEED, cut=False)
        stb = [built_state(s0b)]
        for _ in range(ROUNDS):
            stb.append(step.tick(layout_b, stb[-1]))
        missb = 0
        for n in range(ROUNDS):
            pb0, sb0, _ = E.row_books_built(layout_b, stb[n])
            pb1, sb1, _ = E.row_books_built(layout_b, stb[n + 1])
            w0 = step.teeth(layout_b, stb[n])[:, 0]
            w1 = step.teeth(layout_b, stb[n + 1])[:, 0]
            missb += int((pb1 - pb0 != (w1 - w0) * sb1).sum())
        pb_first, sb_first, _ = E.row_books_built(layout_b, stb[0])
        pb_last, sb_last, _ = E.row_books_built(layout_b, stb[-1])
        print(f"     the act as built: P = W S + R, P_(t+1) - P_t = dW x S_(t+1): {missb} misses; P_40 - P_0 per row:"
              f" {tidy((pb_last - pb_first).tolist())}; S_40 - S_0 per row: {tidy((sb_last - sb_first).tolist())}")
    layout, s0, trains = E.board(*LAYS[1], seed=SEED)
    sprung = E.with_spring(layout, 0, 1)
    states, broke = E.forward(E.edge_tick, E.edge_promise, sprung, s0, 12)
    misses = nonzero = 0
    for n in range(len(states) - 1):
        p0, _ = E.row_books_edge(sprung, states[n])
        p1, _ = E.row_books_edge(sprung, states[n + 1])
        push = E.pushes_sum(sprung, states[n])
        misses += int((p1 - p0 != 4 * push).sum())
        nonzero += int((push != 0).sum())
    back = sum(int(E.same(E.edge_untick(sprung, states[n + 1]), states[n])) for n in range(len(states) - 1))
    print(f"   Mutant, a spring f = 1 on the light train's first row, A1 (its push -2 a, summing to -2 SUM a, not 0), rising by 1 grip, {len(states) - 1} rounds,"
          f" {E.bits(states)} bits: P_(t+1) - P_t = 4 SUM push in every row and round ({misses} misses), SUM push not 0 in"
          f" {nonzero} row-rounds: the books close, P moves by exactly 4 x the pushes' sum; run back exact in {back} of {len(states) - 1}.")
    print()


def section_5():
    print("5. On a still clock, the act as built, state for state (t = 4 r + 2 - D, D = 2 W: the centre of the tooth's cell)")
    print("   Both acts on one layout, the clocks' read cut acyclic (the 00 row's own teeth at rest; on this still lay the cut")
    print("   changes no count of the act as built, measured below).")
    for a00 in (3 * GRIP, 4 * GRIP):
        layout, s0, trains = E.board(a00, a00, seed=SEED)
        layout_b, s0b, _ = E.board(a00, a00, seed=SEED, cut=False)
        sb = built_state(s0b)
        se = E.to_edge(layout, sb)
        stb, ste, stl = [sb], [se], [sb]
        misses = ties = 0
        for n in range(ROUNDS):
            stb.append(step.tick(layout, stb[-1]))
            stl.append(step.tick(layout_b, stl[-1]))
            ste.append(E.edge_tick(layout, ste[-1]))
            _, _, d = E.dials(layout, ste[-1].a, ste[-1].b)
            ties += int((abs(ste[-1].r) == d).sum())
            misses += 0 if E.same(E.to_edge(layout, stb[-1]), ste[-1]) else 1
        cut_same = sum(int(bool((x.a == y.a).all() and (x.b == y.b).all())) for x, y in zip(stb, stl, strict=True))
        # the mirror: (iii)'s flip corresponds to the negation
        mm = sum(0 if E.same(E.to_edge(layout, step.mirror(layout, st)), E.edge_mirror(layout, E.to_edge(layout, st))) else 1 for st in stb)
        # the mutant: the cell's lower edge instead of its centre
        _, _, d0 = E.dials(layout, sb.a, sb.b)
        off = State(sb.a, sb.b, 4 * sb.r - d0, sb.rd)
        off1 = E.edge_tick(layout, off)
        da, _ = E.differing(off1, E.to_edge(layout, stb[1]))
        print(f"   Standing at W = {grips(6 * GRIP + a00)} (D = {grips(12 * GRIP + 2 * a00)}), {ROUNDS} rounds: the two acts' states correspond at {ROUNDS - misses}"
              f" of {ROUNDS} rounds (a and b equal, t = 4 r + 2 - D), {ties} teeth on the dial's edge; (iii)'s flip W - 1 - r maps"
              f" to the negation of t at {len(stb) - mm} of {len(stb)} states; the act as built on the loader's lay and on the cut"
              f" agree in a and b at {cut_same} of {len(stb)} states;")
        print(f"     mutant, the tooth laid at the cell's lower edge, t = 4 r - D: the now slot departs at {da} gears of {sb.a.size} after one round.")
    print()


def section_6():
    print("6. How the split learns W(a+): the 00 slot reading its own teeth")
    print("   A dial that depends on its own quotient: for the 00 row reading itself, D_out(q) = 2 W_a + q, and the")
    print("   split asks N in the cell [2 D(q) q - D(q), 2 D(q) q + D(q)] for exactly one q. Two cells in a row meet edge to")
    print("   edge exactly when their dials are equal: the next cell's floor less this cell's ceiling is (2 q + 1) (D(q+1) - D(q)),")
    print("   a gap where it is positive (q >= 0 and the dial growing) and an overlap where it is negative (q <= -1). Counted:")
    for wa in (1, 2, 3, 5, 8, 13):
        lo_q, hi_q = -2 * wa + 1, 40  # D(q) at least 1
        cells = {}
        for q in range(lo_q, hi_q + 1):
            dq = 2 * wa + q
            cells[q] = (2 * dq * q - dq, 2 * dq * q + dq)
        formula_misses = sum(
            1 for q in range(lo_q, hi_q) if cells[q + 1][0] - cells[q][1] != (2 * q + 1) * ((2 * wa + q + 1) - (2 * wa + q))
        )
        cover = {}
        for lo, hi in cells.values():
            for n in range(lo, hi + 1):
                cover[n] = cover.get(n, 0) + 1
        hull = range(min(lo for lo, _ in cells.values()), max(hi for _, hi in cells.values()) + 1)
        none = sum(1 for n in hull if cover.get(n, 0) == 0)
        twice = sum(1 for n in hull if cover.get(n, 0) >= 2)
        print(f"   W_a = {wa:2d}, q from {lo_q} to {hi_q}: the formula {formula_misses} misses; integers of the hull under no q: {none};"
              f" under two or more: {twice}; of {len(hull)}.")
    d = 9
    cover = {}
    for q in range(-30, 41):
        for n in range(2 * d * q - d, 2 * d * q + d + 1):
            cover[n] = cover.get(n, 0) + 1
    hull = range(2 * d * -30 - d, 2 * d * 40 + d + 1)
    none = sum(1 for n in hull if cover.get(n, 0) == 0)
    edges = sum(1 for n in hull if cover.get(n, 0) >= 2)
    print(f"   A dial that does not depend on q (D = 9), q from -30 to 40: under no q: {none}; under two: {edges}, every one a shared")
    print(f"   edge, which the even rule gives to one q (section 1: 0 misses). So the only lawful dial is one the quotient does not move.")
    print("   On the act: the edge act on the loader's lay (the 00 row reading itself), the second split reading the first's 00 count:")
    for a00, b00 in [LAYS[1], LAYS[4]]:
        layout, s0, trains = E.board(a00, b00, seed=SEED, cut=False)
        r00 = E.row_00(trains)
        states, _ = E.forward(E.edge_tick, lambda lay, st: True, layout, s0, 12)
        back = [int(E.same(E.edge_untick(layout, states[n + 1]), states[n])) for n in range(12)]
        rows_00 = [grips(st.a[r00, 0]) for st in states]
        print(f"     lay {E.lay_name(a00, b00, GRIP)}: untick(tick s) = s in {sum(back)} of 12 rounds; the 00 slot's count by round: {rows_00}")
        layout_c, s0c, _ = E.board(a00, b00, seed=SEED)
        statesc, _ = E.forward(E.edge_tick, E.edge_promise, layout_c, s0c, 12)
        backc = [int(E.same(E.edge_untick(layout_c, statesc[n + 1]), statesc[n])) for n in range(12)]
        print(f"     the acyclic cut (the 00 row's teeth read no row, W_00 = rest = 6 grips): untick(tick s) = s in {sum(backc)} of 12;"
              f" the 00 slot's count by round: {[grips(st.a[r00, 0]) for st in statesc]}")
    print()


def section_7():
    print("7. The even-count rule's cost: adding a whole count k to every velocity (a -> a + k, b kept) on a still clock")
    window = range(-200, 201)
    for k in (1, 2, 3, -1):
        misses = ties = 0
        for d in range(1, 13):
            m = 2 * d
            for n in window:
                q, s = E.split(n, m)
                qk, sk = E.split(n + m * k, m)
                if (qk, sk) != (q + k, s):
                    misses += 1
                if abs(s) == d:
                    ties += 1
        print(f"   k = {k:2d}: split(n + 2 D k) = (q + k, s) misses {misses} of {len(window) * 12} (n in [-200, 200], D in [1, 12]);"
              f" ties among the cases {ties}: {'every miss a tie, none else' if misses == ties else ('no miss' if misses == 0 else 'see counts')}")
    print("   The act as built: q - v = (push + r) div W, so v -> v + k gives q -> q + k at every state: covariant for every k.")
    print("   On the board, standing at W = 9 grips (D = 18 grips), the light train's first row (A1) with its a raised by k at every")
    print("   site (its velocity by k, F unchanged), the row's teeth laid (i) as drawn, (ii) so that every one of its 27 carries lands")
    print("   on the dial's edge (a tie):")
    layout, s0, trains = E.board(*LAYS[0], seed=SEED)
    layout_b, s0b, _ = E.board(*LAYS[0], seed=SEED, cut=False)
    row = 0
    # (ii): t such that N = 2 D v + 4 push + t is D mod 2 D on the row
    force, _ = step.sources(layout, s0.a)
    _, _, d0 = E.dials(layout, s0.a, s0.b)
    n_less_t = 2 * d0[row] * (s0.a[row] - s0.b[row]) + 4 * force[row]
    _, residue = carry(d0[row] - n_less_t, 2 * d0[row], 0)
    tied_t = s0.r.copy()
    tied_t[row] = residue - 2 * d0[row] * (residue > d0[row])
    tied = State(s0.a, s0.b, tied_t, s0.rd)
    for k in (1, 2, 3):
        for name, st in (("as drawn", s0), ("every carry of the row a tie", tied)):
            shifted_a = st.a.copy()
            shifted_a[row] = shifted_a[row] + k
            sh = State(shifted_a, st.b, st.r, st.rd)
            e1, e1s = E.edge_tick(layout, st), E.edge_tick(layout, sh)
            expect = e1.a.copy()
            expect[row] = expect[row] + 2 * k
            _, _, d1 = E.dials(layout, e1.a, e1.b)
            dep = int((e1s.a[row] != expect[row]).sum())
            ties = int((abs(e1.r[row]) == d1[row]).sum())
            print(f"     k = {k}, teeth {name}: ties in the row's carries {ties} of 27; the row's now slot departs from a+ + 2k at {dep} gears of 27")
        sb = built_state(s0b)
        shifted_b = sb.a.copy()
        shifted_b[row] = shifted_b[row] + k
        b1, b1s = step.tick(layout_b, sb), step.tick(layout_b, State(shifted_b, sb.b, sb.r, sb.rd))
        expect = b1.a.copy()
        expect[row] = expect[row] + 2 * k
        print(f"     k = {k}, the act as built: departs at {int((b1s.a[row] != expect[row]).sum())} gears of 27")
    print("   No line of the law asks this covariance (the law's symmetries are the cube's 24, time's reversal and locality;")
    print("   no boost of a count's velocity is a law): a property the act as built had and the edge act does not, named.")
    print()


def section_8():
    print("8. The click's books on the centred split (the owner's word on the Node-clock forward and backward)")
    print("   carry(A) of an area A at a key with the tooth born at the middle: q(A) + q(-A) = 0, every key, odd or even:")
    misses_c = misses_b_odd = misses_b_even = 0
    cases = 0
    for key in range(1, 41):
        for area in range(-3 * key, 3 * key + 1):
            cases += 1
            q, s = E.split(2 * area, 2 * key)
            qn, sn = E.split(-2 * area, 2 * key)
            if q + qn != 0 or s + sn != 0:
                misses_c += 1
            k0, _ = carry(key - 1, 2, 0)
            qb, _ = carry(area, key, k0)
            qbn, _ = carry(-area, key, k0)
            if qb + qbn != 0:
                if even(key):
                    misses_b_even += 1
                else:
                    misses_b_odd += 1
    print(f"   keys 1 to 40, areas within 3 keys, {cases} cases: the centred split (the area doubled, the dial 2 key, the tooth 0):"
          f" {misses_c} misses; the act as built's birth (key - 1) div 2 with the plain carry: {misses_b_odd} misses at odd keys"
          f" and {misses_b_even} at even keys (term 11's measure 4).")
    print("   Two trains, a giver and a taker, areas A and -A each round, teeth born at 0, 6,000 rounds of areas from the")
    print("   recurrence at an even key 12 and an odd key 13: the clicks opposite and the teeth opposite in every round:")
    src = E.recurrence(11)
    for key in (12, 13):
        kg = kt = 0
        miss_q = miss_k = 0
        for _ in range(6000):
            area = E.drawn(src, -2 * key, 2 * key)
            qg, kg = E.split(2 * area + kg, 2 * key)
            qt, kt = E.split(-2 * area + kt, 2 * key)
            miss_q += int(qg + qt != 0)
            miss_k += int(kg + kt != 0)
        print(f"     key {key}: clicks not opposite in {miss_q} rounds, teeth not opposite in {miss_k} rounds")
    print()


def main():
    print("The double Node-clock's tooth on the edge: the probe, in whole numbers on the engine's own load and act")
    print(f"(the example world's universe, examples/tensor24, on a cube of side 3: the light train, A1 of two parts, and the metric")
    print(f" family, the four-vector's square; den Gamma^2 = {GRIP}, the grip at rest and the Mesh unit; rest teeth 6 grips; J = 0, T_d = 1;")
    print(f" the 00 slot's counts and the fine teeth laid in grips, the fine teeth's own pitch at J = 0)")
    print()
    section_1()
    section_2()
    section_3()
    section_4()
    section_5()
    section_6()
    section_7()
    section_8()


if __name__ == "__main__":
    main()
