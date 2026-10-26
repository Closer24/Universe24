"""fr1 (one_node_bh1.py of H-Frozen-Node-1 with the head's emitter; the flag FR1_RELEASE from the environment): the one-Node test on the engine. bh1: the one-Node black-hole test on the engine (the symmetric ride, the default since the fold): the centre of the 3-cube fed to a
content (the frozen content by default) as tests/test_the_node.py feeds it, N intervals forward with every reading at the centre and
at its six neighbours (the valve), then N intervals back compared bit for bit (the run back).

Usage: one_node_bh1.py <src dir> <world.json> <content> <intervals> [form]
  <src dir>  the engine's src folder to import (e5src: the engine unchanged; e5flag: bh1's flagged copy)
  form       none (the letter) | identity | write  (set on the flagged copy's interval module; refused on the engine's own src)
Prints per interval (the first 12, then every tenth, then the last): the centre's X (bits), content, clock p0, Link pace, the velocity
v = X_now - X_before, the write's quotient q on the time line (X_post less the rotate's own output, read exactly from S, w and r),
the neighbours' max content and X bits, the count of frozen Nodes (the Link pace 0) on the board, the Links held at the wall, the max
transient bits so far and the state's bits; then the clicks at the centre and the run back's count.
"""
import copy
import json
import sys

import numpy as np


def main(argv):
    sys.set_int_max_str_digits(0)
    src, world_path, content, intervals = argv[1], argv[2], int(argv[3]), int(argv[4])
    form = argv[5] if len(argv) > 5 else "none"
    sys.path.insert(0, src)
    from event_universe import interval as interval_module
    from event_universe.core import paces
    from event_universe.features import volume
    from event_universe.loader.world import load_world
    from event_universe.node import Node
    from event_universe.rows import CARRIER, PLANE

    if form != "none":
        try:
            from event_universe import bh1_flag
        except ImportError:
            raise SystemExit("the form %r needs the flagged copy (bh1_flag.FORM); refused on %s" % (form, src))
        bh1_flag.FORM = form
    del interval_module
    universe, world = load_world(world_path)
    node = Node(universe, world)
    centre = tuple(x // 2 for x in node.shape)
    carrier = node.row(CARRIER).lines[0]
    level = int(np.asarray(volume.volume_of(node.gamma, np.array([content], dtype=object)), dtype=object).reshape(-1)[0])
    carrier.now[centre] = level
    carrier.before[centre] = level
    if len(argv) > 7:  # bh1: the Node fed with a velocity, its before slot at another content (the dynamically frozen Node)
        carrier.before[centre] = int(np.asarray(volume.volume_of(node.gamma, np.array([int(argv[7])], dtype=object)), dtype=object).reshape(-1)[0])
    node.ride_walls()
    light = node.emitter().lines[0]  # fr1: the head names the gap-0 row node.emitter()
    light.now[centre] = 4 * int(light.now[centre])
    frozen_edge = paces.frozen_content(node.gamma)
    print("world", world_path, "cube", node.cube, "den", node.den, "Gamma", node.gamma, "G", node.G, "form", form)
    print("centre", centre, "fed to the content", content, "X", level, "bits", level.bit_length(), "before at", int(carrier.before[centre]), "; the frozen content", frozen_edge,
          "; clock there", paces.clock(node.gamma, frozen_edge), "; w bits", node.w.bit_length())
    cube = node.cube
    neighbours = []
    for a in range(3):
        for s in (1, -1):
            n = list(centre)
            n[a] = (n[a] + s) % cube
            neighbours.append(tuple(n))
    hashes = []
    rows = []
    print("i | X bits | content | p0 | pace | v | q (write quotient) | rim max content | rim X bits | frozen | held | transient bits | state bits | turned at centre")
    for t in range(intervals):
        hashes.append(node.state_hash())
        x_now, x_before, r = int(carrier.now[centre]), int(carrier.before[centre]), int(carrier.rem[centre])
        c = node.content()
        c_centre = int(c[centre])
        p0 = int(paces.clock(node.gamma, c_centre))
        pace = int(paces.link_pace(node.gamma, c_centre))
        rule = node.rule_of(node.row(CARRIER), c, node.link_factors())
        s_centre = int(np.asarray(rule.self_coefficient)[centre])
        reaches = [int(np.asarray(x)[centre]) for x in rule.reaches]
        arrivals = sum(rr * int(carrier.now[n]) for rr, n in zip(reaches, neighbours))
        x_rot = (s_centre * x_now - node.w * x_before + arrivals + r) // node.w
        node.step()
        carrier = node.row(CARRIER).lines[0]
        x_post = int(carrier.now[centre])
        q = x_post - x_rot
        c_after = node.content()
        rim_c = max(int(c_after[n]) for n in neighbours)
        rim_x = max(int(carrier.now[n]) for n in neighbours)
        pace_board = np.asarray(paces.link_pace_of(node.gamma, c_after), dtype=object)
        frozen = int(sum(1 for p in pace_board.reshape(-1) if int(p) == 0))
        held = int(sum(1 for f in node.link_factors()[0::2] for v in f.reshape(-1) if int(v) == 0))
        _n, bits = node.census()
        row = (node.interval, x_post.bit_length(), c_centre, p0, pace, x_now - x_before, q, rim_c, rim_x.bit_length(), frozen, held,
               node.max_transient, bits, bool(node.turned[centre]))
        rows.append(row)
        if t < 12 or (t + 1) % 10 == 0 or t == intervals - 1:
            print(" ".join(str(v) for v in row))
    own = [e for e in node.log if tuple(e["node"]) == centre and e["event"] in ("birth", "credit")]
    ends = [e for e in node.log if e["event"] == "birth" and centre in (tuple(e["minus"]), tuple(e["plus"]))]
    print("clicks at the centre:", len(own), "; births with a child at the centre:", len(ends), "; counts:", node.counts)
    print("X at the centre at the end:", int(carrier.now[centre]), "bits", int(carrier.now[centre]).bit_length(),
          "; content", int(node.content()[centre]), "; max transient bits", node.max_transient, "; state bits", bits)
    exact = 0
    for k in range(intervals):
        node.step_back()
        exact += node.state_hash() == hashes[intervals - 1 - k]
    print("run back:", exact, "of", intervals)
    json.dump({"rows": rows, "run_back": [exact, intervals], "counts": node.counts}, open(argv[6] if len(argv) > 6 else "/dev/null", "w"))


if __name__ == "__main__":
    main(sys.argv)
