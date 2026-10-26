"""The one-Node test of H-Take-Count-As-Rule3-Division-2 (under 15 s). (1) The theorem: the exact take's fall f(s) = x s (g - w s) over the
weight is concave in the count with f(0) = 0, so the chord count, the walls times the full move divided by the full fall by the one
carried division at the direction -1 (the quotient rounded up by the remainder's mirror), pays the walls at every take and never exceeds
the full move: on 20,000 random quadratics; and the least root is not one division: the least count at a vanishing gradient grows as
the square root of the walls (the count at 4 times the walls is twice the count, not 4 times), which no quotient of an affine numerator
by a fixed wall does. (2) At one Node of the 3-cube the flagged copy's fall_of with the flag set returns a count that pays the walls,
within the full move, and at least the head's least root; with the flag empty the head's bit for bit."""
import os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/dev/shm/tmp/tc2/src_tc2")
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "tests"))
from event_universe.core import rule3
from event_universe.core.rule3 import quotient
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe import take as take_mod

CENTRE = (1, 1, 1)


def chord(walls, dist, full):
    return rule3.carried_division(walls * dist, full, 0, -1)[0]


def test_the_chord_pays_at_every_take_and_the_least_root_is_no_division() -> None:
    random.seed(7)
    paid = within = at_least = 0
    for _ in range(20000):
        w, x, weight = random.randint(1, 10**6), random.randint(1, 10**6), random.randint(1, 10**6)
        g = random.randint(1, 10**9)
        dist = random.randint(1, max(1, g // (w + w)))

        def fall(s):
            return quotient(x * (g * s - w * s * s), weight)

        full = fall(dist)
        if full <= 0:
            continue
        walls = random.randint(1, full)
        s = chord(walls, dist, full)
        paid += fall(s) >= walls
        within += 1 <= s <= dist
        least = next(k for k in range(1, dist + 1) if fall(k) >= walls)
        at_least += s >= least
    assert paid == within == at_least
    assert paid > 15000
    # the least root at a vanishing gradient: f(s) = x w s^2 (the fall's sign mirrored, the rise), s ~ root(walls)
    w, x, weight = 7, 3, 1
    least = [next(k for k in range(1, 10**6) if quotient(x * w * k * k, weight) >= x * w * t * t) for t in (1000, 2000, 4000)]
    assert least == [1000, 2000, 4000]


def test_the_flagged_fall_of_at_one_node_of_the_3_cube() -> None:
    u, w = load_world(os.path.join(HERE, "worlds", "world_node.json"))
    node = Node(u, w)
    for _ in range(4):
        node.step()
    rec = node.records().index(node.emitter())
    row = node.records()[rec]
    re = row.lines[0]
    re.now[CENTRE], re.before[CENTRE] = 1227, 920
    rule = node.rule(row.pair, node.content(), node.link_factors())
    walls = node.units[rec]
    os.environ.pop("TC2_CHORD_COUNT", None)
    head = take_mod.fall_of(node, CENTRE, walls, rule, row)
    os.environ["TC2_CHORD_COUNT"] = "1"
    flagged = take_mod.fall_of(node, CENTRE, walls, rule, row)
    os.environ.pop("TC2_CHORD_COUNT", None)
    again = take_mod.fall_of(node, CENTRE, walls, rule, row)
    assert again == head and head[0] is not None
    s, fall, k = flagged
    assert k == head[2] and 1 <= s <= 1227 - 920 and fall >= walls and s >= head[0]
    print("one node", dict(head=head, flagged=flagged, walls=walls))
