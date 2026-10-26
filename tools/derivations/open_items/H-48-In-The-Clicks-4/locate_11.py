"""a484, step 1's measurement: the chiral 3-cube (CB13's world) run beside one reflection to N intervals on a named src; at every interval the state compared through the image under the three carries (a48b's compare_state), and every draw's digits logged (li, slot, rem, wall, bit, reversals, rho, folded, digit, base) so the first parting draw is read digit by digit. Usage: locate_11.py <src> <worktree> <N> <reflection index in a48b's 48> <out.json>"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2] + "/tools/derivations/open_items/H-48-In-The-Clicks-2")
sys.set_int_max_str_digits(0)
from event_universe import close, take  # noqa: E402
from event_universe.core.rule3 import half, lattice, mirrored, quotient, remainder  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
import a48b_48 as A  # noqa: E402

root, n, k_img = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
universe, world = load_world(root + "/tests/worlds/world_node.json")
centres = ([1, 0, 0], [0, 2, 1], [2, 1, 0])
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in centres]
world = dict(world, shape=[3, 3, 3], intervals=n, seed=lays)
cube = 3
m = A.signed_permutations()[k_img]
det = A.det_of(m)


def wrap(node):
    node.draws = []
    original = take.read_number

    def wrapped(nd, at, rules, unit):
        nodes = take.frame_nodes(nd, at)
        is_im = nd.is_im()
        digits = []
        for li, (line, r) in enumerate(rules):
            for k, nn in enumerate(nodes):
                wl = take.at_node(line.wall, nn)
                f = lattice(wl, take.at_node(r.mass, nn), *[take.at_node(x, nn) for x in r.reaches]) if k == 0 else lattice(wl, take.at_node(r.reaches[k - 1], nn))
                rem = int(line.rem[nn])
                bit = int(rules[0][0].rem[nn])
                rev = (1 - bit) * (1 + is_im[li])
                rho = mirrored(rem, wl, rev)
                folded = min(rho, remainder(wl - rho, wl))
                digits.append({"li": li, "k": k, "node": list(nn), "rem": rem, "wall": wl, "F": f, "bit": bit, "rev": rev, "rho": rho, "folded": folded, "digit": quotient(folded, f), "base": quotient(quotient(wl, f), 2) + 1, "half": half(wl)})
        got = original(nd, at, rules, unit)
        nd.draws.append({"i": nd.interval, "node": list(at), "digits": digits, "drawn": None if got is None else list(got)})
        return got

    close.read_number = wrapped


base, img = Node(universe, world), Node(universe, A.world_image(world, m, cube))
wrap(base)
img.draws = []
turns = {x: 0 for x in np.ndindex(*base.shape)}
carries = ["ones", "twos", "parity"]
out = {"image": m.tolist(), "det": det, "state": [], "first_state": {c: None for c in carries}, "first_draw_parting": None}
for t in range(n):
    base.step()
    img.step()
    for x in np.ndindex(*base.shape):
        if base.turned[x]:
            turns[x] += 1
    bad = A.compare_state(base, img, m, cube, turns, carries)
    out["state"].append({"i": base.interval, **{c: [bad[c]["scalar"], bad[c]["odd_level"], bad[c]["odd_rem"], bad[c]["odd_wr"]] for c in carries}})
    for c in carries:
        if out["first_state"][c] is None and bad[c]["first"] is not None:
            out["first_state"][c] = {"i": base.interval, **bad[c]}
img2 = img
di = {(e["i"], tuple(e["node"])): e for e in img2.draws}
for e in base.draws:
    key = (e["i"], tuple(A.image(m, tuple(e["node"]), cube)))
    f = di.get(key)
    db = sorted((x["digit"], x["base"]) for x in e["digits"])
    dd = None if f is None else sorted((x["digit"], x["base"]) for x in f["digits"])
    if f is None or db != dd or e["drawn"] != f["drawn"]:
        parting = {"i": e["i"], "node": e["node"], "image_node": list(key[1]), "found": f is not None, "drawn_base": e["drawn"], "drawn_image": None if f is None else f["drawn"], "lines": []}
        if f is not None:
            for x in e["digits"]:
                y = next((y for y in f["digits"] if y["li"] == x["li"] and tuple(y["node"]) == tuple(A.image(m, tuple(x["node"]), cube))), None)
                if y is None or (x["digit"], x["base"]) != (y["digit"], y["base"]):
                    parting["lines"].append({"base": x, "image": y})
        out["first_draw_parting"] = parting
        break
out["births"] = [base.counts["births"], img.counts["births"]]
out["credits"] = [base.counts["body_clicks"], img.counts["body_clicks"]]
out["verdict_C"] = A.verdict(base, img, m, cube, "C")
out["draws"] = [len(base.draws), len(img2.draws)]
json.dump(out, open(sys.argv[5], "w"), default=str)
print(json.dumps({k: out[k] for k in ("image", "det", "births", "credits", "verdict_C", "draws", "first_state")}, default=str))
p = out["first_draw_parting"]
if p:
    print("first parting draw at", p["i"], p["node"], "->", p["image_node"], "drawn", p["drawn_base"], p["drawn_image"], "lines parting", len(p["lines"]))
    for ln in p["lines"][:8]:
        print(json.dumps(ln, default=str))
else:
    print("no parting draw")
for s in out["state"]:
    if any(sum(s[c]) for c in carries):
        print("state", json.dumps(s)); 
