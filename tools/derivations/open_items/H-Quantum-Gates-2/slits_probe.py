"""The two slits' probe on the board and in the clicks (hand qg2): the world stepped by the engine's own Node, the gap-0 plane's form (re_now^2 + im_now^2) read per Node at every interval and summed over x and z into the profile along y; the births and the refusals of the log by their y offset from the centre. Integers only.

Usage: python slits_probe.py <world.json> [intervals]"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "src"))
import numpy as np  # noqa: E402

from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import PLANE  # noqa: E402

THOUSAND = 1000


def share_profile(node):
    """The gap-0 record's share (the conserved form's share, the click premise's measure) in units of its quantum, summed over x and z per y."""
    row = node.row(PLANE, gap=0)
    rec = node.records().index(row)
    rule = node.rule(row.pair, node.content(), node.link_factors())
    sh = node.share(row.lines, rule)
    unit = node.units[rec]
    standing = [int(sum(1 for x in sh[:, y, :].reshape(-1) if int(x) >= unit)) for y in range(node.cube)]
    return [int(sum(int(x) for x in sh[:, y, :].reshape(-1)) * THOUSAND // unit) for y in range(node.cube)], standing


def profile(node):
    row = node.row(PLANE, gap=0)
    re, im = row.lines
    form = re.now * re.now + im.now * im.now
    return [int(sum(int(x) for x in form[:, y, :].reshape(-1))) for y in range(node.cube)]


def parity_split(prof, centre, cube):
    even = odd = 0
    for y, v in enumerate(prof):
        off = (y - centre) % cube
        off = min(off, cube - off)
        if off % 2:
            odd += v
        else:
            even += v
    return even, odd


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    intervals = int(argv[2]) if len(argv) > 2 else int(world["intervals"])
    node = Node(universe, world)
    centre = node.cube // 2
    lays = [e for e in node.log if e["event"] == "lay"]
    refused_state = [e for e in node.log if e["event"] == "refused"]
    print(json.dumps({"lays": len(lays), "refused at the lay": len(refused_state), "lay lines": lays}))
    prof0 = profile(node)
    print(json.dumps({"i": 0, "profile along y (gap-0 form summed over x, z)": prof0}))
    sh, st = share_profile(node)
    print(json.dumps({"i": 0, "share along y (thousandths of a quantum, summed over x, z)": sh, "Nodes standing at a whole quantum per y": st}))
    seen = len(node.log)
    gap0 = node.records().index(node.row(PLANE, gap=0))
    for t in range(intervals):
        node.step()
        prof = profile(node)
        even, odd = parity_split(prof, centre, node.cube)
        total = even + odd
        meetings = [e for e in node.log[seen:] if e["event"] in ("birth", "refused") and e.get("row", gap0) == gap0 and e.get("cause") != "stop"]
        seen = len(node.log)
        m_even = m_odd = 0
        for e in meetings:
            off = (e["node"][1] - centre) % node.cube
            off = min(off, node.cube - off)
            if off % 2:
                m_odd += 1
            else:
                m_even += 1
        print(json.dumps({"i": node.interval, "profile y": prof, "odd offsets' share of the form (thousandths)": (odd * THOUSAND) // total if total else None, "meetings of the gap-0 row this interval at even / odd y offsets": [m_even, m_odd], "gap-0 record": gap0, "births": node.counts["births"], "met": node.counts["met"]}))
    births = [e for e in node.log if e["event"] == "birth"]
    refused = [e for e in node.log if e["event"] == "refused" and e["i"] > 0]
    by_y = Counter((b["node"][1] - centre) for b in births)
    ref_y = Counter((e["node"][1] - centre) for e in refused)
    ref_cause = Counter(e["cause"] for e in refused)
    odd_births = sum(n for off, n in by_y.items() if off % 2)
    print(json.dumps({"births by y offset": dict(sorted(by_y.items())), "births at odd offsets": odd_births, "births": len(births), "refusals by y offset": dict(sorted(ref_y.items())), "refusals by cause": dict(ref_cause), "counts": {k: str(v) for k, v in node.counts.items()}}))


if __name__ == "__main__":
    main(sys.argv)
