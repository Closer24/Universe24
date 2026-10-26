"""The one-Node test of H-Click-And-Rule3-One-Algebra-2 (under 15 s): (1) Rule3's time reversal is the slot exchange conjugated by the
remainder's mirror, bit for bit on 2000 random lines; (2) at one Node of the 3-cube the exact take moves the now slot alone toward the
before, the before and the remainder unmoved, and its moved level against Rule3 at -1 on the taken line (a_{-2}) is read, not assumed;
(3) the click's lay conjugated by the slot exchange is the lay on the other slot with the Wronskian negated (the sense exchanged), and not
the undo, which is the lay negated; the lay with no direction (both slots alike) writes the Wronskian 0."""
import os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tests"))
import numpy as np
from laws import node_of
from event_universe.core.rule3 import mirrored, rule3
from event_universe.links import cross
from event_universe.take import at_node, lay, neighbour, take_at

CENTRE = (1, 1, 1)


def test_rule3_reversal_is_slot_exchange_conjugated_by_the_mirror() -> None:
    random.seed(5)
    den, gamma = 1021, 1000
    w = 6 * den * gamma * gamma
    for _ in range(2000):
        now, before, r = random.randint(-10**6, 10**6), random.randint(-10**6, 10**6), random.randint(0, w - 1)
        mass, flux = random.randint(0, w), random.randint(-10 * w, 10 * w)
        nxt, r2 = rule3(flux, mass, w, now, before, r, 1)
        assert rule3(flux, mass, w, now, nxt, r2, -1) == (before, r)
        q, rr = rule3(flux, mass, w, now, nxt, mirrored(r2, w, 1), 1)
        assert (q, mirrored(rr, w, 1)) == (before, r)
        assert rule3(flux, mass, w, now, nxt, r2, 1) != (before, r) or (flux + mass) % w == 0


def test_the_take_moves_the_now_slot_alone_toward_the_before() -> None:
    node = node_of("world_node.json")
    for _ in range(4):
        node.step()
    rec = node.records().index(node.emitter())
    row = node.records()[rec]
    re = row.lines[0]
    re.now[CENTRE], re.before[CENTRE] = 1227, 920
    rem_was, im_was = int(re.rem[CENTRE]), (int(row.lines[1].now[CENTRE]), int(row.lines[1].before[CENTRE]))
    rule = node.rule(row.pair, node.content(), node.link_factors())
    got = take_at(node, CENTRE, node.units[rec], rule, 1, rec)
    assert got is not None
    levels, fall, now, before, k = got
    t = 1 if before > now else -1
    assert (now, before) == (1227, 920) and 1 <= levels <= abs(now - before)
    assert int(re.now[CENTRE]) == now + t * levels and int(re.before[CENTRE]) == before
    assert int(re.rem[CENTRE]) == rem_was
    assert (int(row.lines[1].now[CENTRE]), int(row.lines[1].before[CENTRE])) == im_was
    w, own, mass = int(rule.wall), at_node(rule.self_coefficient, CENTRE), at_node(rule.mass, CENTRE)
    flux = sum(at_node(reach, CENTRE) * (int(re.before[neighbour(node, CENTRE, p)]) - before) for p, reach in enumerate(rule.reaches))
    a_m2, _ = rule3(flux, mass, w, before, now, rem_was, -1)
    print("take", dict(levels=levels, moved=now + t * levels, a_m2=a_m2, equal=now + t * levels == a_m2))


def test_the_lay_conjugated_by_the_slot_exchange_is_the_lay_on_the_other_slot() -> None:
    node = node_of("world_node.json")
    s = next(k for k, r in enumerate(node.records()) if r.lines and len(r.lines) == 2 and r is not node.emitter())
    re, im = node.records()[s].lines
    A, B, sense = node.A, node.B, 1
    lay(node, s, CENTRE, (A, 0, 0, sense * B), 1)
    W = int(cross(re.now[CENTRE], im.now[CENTRE], re.before[CENTRE], im.before[CENTRE]))
    assert W == A * sense * B
    lay(node, s, CENTRE, (A, 0, 0, sense * B), -1)
    for z in (re, im):
        z.now[CENTRE], z.before[CENTRE] = z.before[CENTRE], z.now[CENTRE]
    lay(node, s, CENTRE, (A, 0, 0, sense * B), 1)
    for z in (re, im):
        z.now[CENTRE], z.before[CENTRE] = z.before[CENTRE], z.now[CENTRE]
    W_T = int(cross(re.now[CENTRE], im.now[CENTRE], re.before[CENTRE], im.before[CENTRE]))
    assert (int(re.now[CENTRE]), int(re.before[CENTRE]), int(im.now[CENTRE]), int(im.before[CENTRE])) == (0, A, sense * B, 0)
    assert W_T == -W
    lay(node, s, CENTRE, (0, A, sense * B, 0), -1)
    lay(node, s, CENTRE, (A, A, sense * B, sense * B), 1)
    assert int(cross(re.now[CENTRE], im.now[CENTRE], re.before[CENTRE], im.before[CENTRE])) == 0
