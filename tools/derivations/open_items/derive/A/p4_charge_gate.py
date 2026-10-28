"""P4, the write's own charge book (formula F4) against the head's lay jam (E16) and sense jam (R1).

F4: a click of a whole writes at both ends of a Mesh only where the charge its write moves sums to 0:
      c_T * dQ_T = 0,   dQ_T = SUM over the written ends e of [ W(z_e + d_e) - W(z_e) ],
    W(z) = Im(conj(z_now) z_before), z_e the train's hand standing at e at the tick's start, d_e the write:
      a fitting:     d_e = sigma_e (A, i B), the fitted hand at its sense, so dQ_T = X_x + X_y, the cross terms
                     X_e = Im(conj(z_now) d_before) + Im(conj(d_now) z_before) with the standing hand;
      an unspringing: d_e = -z_e (the hand unwound whole), so dQ_T = -(W_x + W_y).
    The indicator [dQ = 0] = 1 + ((-dQ dQ) div (dQ dQ dQ dQ + 1)), two products and one Rule3 quotient.
The head refuses a fitting by name `lay` where the fitted hand's train already stands at an end (its wind above 0
at the tick's start) or two fitted hands of one train land at one Node-clock (click.jam), and refuses a sprung
pair by name `sense` unless its two ends' sweeps have opposite signs (click.engage, R1).
Read: every candidate fitting at the head's jam, its standing hands and dQ; every unspringing's pair sum.

argv: the head's worktree, the world file, the ticks.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
from tests.laws import world_of
from event_universe import click as C, hands
from event_universe.clock import Clock
from event_universe.meshes import coupling_of


def W(n3, n12, b3, b12):
    return n3 * b12 - n12 * b3


def zero(dq):
    """[dq = 0] in the three operations: 1 + ((-dq dq) div (dq^4 + 1))."""
    return 1 + ((-dq * dq) // (dq * dq * dq * dq + 1))


stats = Counter()
orig_jam = C.jam


def at_start(gears, where):
    three, twelve = gears
    return (int(three.now[where]), int(twelve.now[where]), int(three.before[where]), int(twelve.before[where]))


def jam(clock, fits, winds):
    starts = clock.start_gears
    kept = []
    all_hands = clock.hands()
    A, B = clock.A, clock.B
    for f in fits:
        s, rec = f.gear_ratio, f.rec
        if coupling_of(all_hands[rec]) > coupling_of(all_hands[s]):  # an unspringing (the head's `inverse`)
            t = hands.twin_of(all_hands, rec)
            w0 = W(*at_start(starts[rec], f.minus))
            w1 = W(*at_start(starts[t], f.plus))
            stats["unspringing candidates (a coupled pair into the light)"] += 1
            stats["  their ends' sweeps of opposite sign (the head's R1 passes)"] += int(w0 * w1 < 0)
            stats["  dQ = -(W_x + W_y) = 0 (F4 writes)"] += int(w0 + w1 == 0)
            continue
        t = hands.twin_of(all_hands, s)
        stats["fitting candidates at the jam (from the uncoupled giver)"] += 1
        dq = 0
        empty = True
        for where, sense, p in ((f.minus, -1, s), (f.plus, 1, t)):
            n3, n12, b3, b12 = at_start(starts[p], where)
            empty = empty and (n3, n12, b3, b12) == (0, 0, 0, 0)
            d = (sense * A, 0, 0, B)  # the fitted hand: now (sense A, 0), before (0, B)
            dq += W(n3 + d[0], n12 + d[1], b3 + d[2], b12 + d[3]) - W(n3, n12, b3, b12)
        standing = int(winds[s][f.minus]) > 0 or int(winds[t][f.plus]) > 0
        c = coupling_of(all_hands[s])
        gate = c * zero(dq) + (1 - c)
        kind = "coupled fitted train" if c else "uncoupled fitted train (light into light, SL-S3)"
        stats[f"  [{kind}] candidates"] += 1
        stats[f"  [{kind}] the head's lay jam by standing (wind above 0 at an end)"] += int(standing)
        stats[f"  [{kind}] both ends empty (no notch of the train at either end)"] += int(empty)
        stats[f"  [{kind}] F4's gate open"] += int(gate == 1)
        stats[f"  [{kind}] the head jams by standing and F4 writes (dQ = 0 with a hand standing)"] += int(standing and gate == 1)
        stats[f"  [{kind}] the head passes (no standing) and F4 refuses (dQ != 0)"] += int((not standing) and gate == 0)
        stats[f"  [{kind}] the head passes with a notch standing (wind 0, the hand not empty)"] += int((not standing) and not empty)
        if c and not standing:
            kept.append((s, f.minus, -1, t, f.plus, 1))
    # the crowd: the summed write of every kept coupled fitting at one (hand, Node-clock)
    landing = {}
    for s, mi, smi, t, pl, spl in kept:
        landing.setdefault((s, mi), []).append(smi)
        landing.setdefault((t, pl), []).append(spl)
    for (p_, where), senses in landing.items():
        if len(senses) < 2:
            continue
        n3, n12, b3, b12 = at_start(starts[p_], where)
        tot = sum(senses)
        dW = W(n3 + tot * A, n12, b3, b12 + len(senses) * B) - W(n3, n12, b3, b12)
        dq = dW - tot * A * B  # the summed write's sweep less the children's own charges
        stats["crowds: two or more coupled fitted hands of one hand at one Node-clock (the head jams them all)"] += 1
        stats["  their summed write's charge book closes (F4 open)"] += int(dq == 0)
        stats["  of them with opposite senses only (+, -)"] += int(sorted(senses) == [-1, 1])
    return orig_jam(clock, fits, winds)


C.jam = jam
calibre, piece = world_of(sys.argv[2])
clock = Clock(calibre, piece)
for _ in range(int(sys.argv[3])):
    clock.tick()
print(sys.argv[2], sys.argv[3], "ticks; births", clock.counts["births"], "lay jams", clock.counts["refused_lay"],
      "sense jams", clock.counts["refused_sense"])
for k in stats:
    print(f"  {k}: {stats[k]}")
# the indicator of zero, exhaustive on a range
bad = sum(1 for n in range(-50000, 50001) if zero(n) != int(n == 0))
print(f"  the indicator [dq = 0] = 1 + ((-dq dq) div (dq^4 + 1)) off at {bad} of 100001 integers")
