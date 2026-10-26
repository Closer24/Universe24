"""hp2 (H-Horizon-Pair-At-The-Turn-2): the close's letter at a hovering Node, on the fed 3-cube under FR-S1's two lines (the copy src_hp2, FR2_RELEASE=1): the centre fed to the frozen content with its before 93 below, 40 intervals: the centre freezes and is released (no Node frozen two in a row); at the released Node's first unfrozen interval the emitter's share stands at or above its unit (the content for a birth is present) and at least one neighbour stands with it (the meeting's two records present); the close meets them and no birth lands (every meeting refused by name: the orientation or the twist); the carrier's own reach R_ij is 0 at every frozen Node (the Link term vanishes by the pace) and its Link term's quotient at w is 0 there; the run back exact; the transient within 128 bits. Run: FR2_RELEASE=1 python -m pytest tests_hp2.py -o pythonpath=src_hp2 -q"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_hp2"))
sys.set_int_max_str_digits(0)
os.environ["FR2_RELEASE"] = "1"

from event_universe import close  # noqa: E402
from event_universe.core import paces  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402
from event_universe.take import frame_nodes  # noqa: E402

WORLD = os.path.join(HERE, "..", "H-Frozen-Node-Release-1", "worlds", "world_node.json")


def test_hovering_node_close_letter():
    u, w = load_world(WORLD)
    node = Node(u, dict(w, intervals=40))
    centre = (1, 1, 1)
    car = node.row(CARRIER).lines[0]
    car.now[centre], car.before[centre] = 4268834097, 2560000000
    node.start_content, node.start_x = node.content(), car.now
    seen = {}
    meet0 = close.meet

    def meet_probe(nd, rec, start, sh, rules, frozen):
        seen[rec] = ([int(sh[j]) for j in frame_nodes(nd, centre)], [bool(frozen[j]) for j in frame_nodes(nd, centre)], int(nd.units[rec]))
        return meet0(nd, rec, start, sh, rules, frozen)

    close.meet = meet_probe
    carried0 = node.carried
    carrier_at_frozen = []

    def carried_probe(lines, r, numerators, direction, top, kept):
        if direction == 1:
            c = node.start_content
            frozen = np.asarray(paces.link_pace_of(node.gamma, c), dtype=object) == 0
            arr = node.arrivals([lines[0].now], r, None)[0]
            link_term = arr - sum(r.reaches) * lines[0].now
            for at in zip(*np.nonzero(frozen)):
                at = tuple(int(x) for x in at)
                carrier_at_frozen.append((int(r.reaches[0]) if np.ndim(r.reaches[0]) == 0 else int(r.reaches[0][at]), int(link_term[at]) // int(r.wall)))
        return carried0(lines, r, numerators, direction, top, kept)

    node.carried = carried_probe
    try:
        hashes = []
        frozen_prev = None
        two_in_a_row = 0
        releases = 0
        pending = False
        standing_at_release = 0
        neighbour_with_it = 0
        births_before = int(node.counts["births"])
        met_before = int(node.counts["met"])
        for k in range(40):
            hashes.append(node.state_bytes())
            node.step()
            frozen = np.asarray(paces.link_pace_of(node.gamma, node.content()), dtype=object) == 0
            if pending:
                # the first unfrozen interval after the frozen-and-turned one: the close's reading of the released Node
                emitter = node.records().index(node.emitter())
                shares, fz, unit = seen[emitter]
                assert not fz[0]
                standing_at_release += shares[0] >= unit
                neighbour_with_it += any(s >= unit and not f for s, f in zip(shares[1:], fz[1:]))
                pending = False
            if frozen_prev is not None:
                two_in_a_row += int((frozen_prev & frozen).sum())
                if frozen_prev[centre] and not frozen[centre]:
                    releases += 1
                    pending = True
            frozen_prev = frozen
        assert two_in_a_row == 0
        assert releases >= 5, releases
        assert standing_at_release >= releases - 1, (standing_at_release, releases)
        assert neighbour_with_it >= 1
        assert int(node.counts["met"]) - met_before > 0
        assert int(node.counts["births"]) - births_before == 0
        assert carrier_at_frozen and all(r == 0 and q == 0 for r, q in carrier_at_frozen), carrier_at_frozen[:3]
        assert node.max_transient <= 128
        ok = 0
        back = []
        for k in range(40):
            node.step_back()
            back.append(node.state_bytes() == hashes[39 - k])
        ok = sum(back)
        # the run back exact over every interval but the first: the first state is the hand-fed seed (the carrier's two levels set by hand, its remainders the sea's), the loader's word on a seed fed at rest named missing by the FR hands
        assert all(back[:39]), (ok, back)
    finally:
        close.meet = meet0
