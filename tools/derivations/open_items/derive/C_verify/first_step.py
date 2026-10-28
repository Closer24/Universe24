"""Verifier's probe (integers only): the first step from rest on the bang world, X1 against X0 (1 + 4 n / Gamma) for
the derived push and X0 (1 + (4/3) n / Gamma) for the head, at many quanta n; and the seed's split of the forms
(K, G, V over the teeth) at the Node-clock (0, 0, 0). Usage: python -I first_step.py ENGINE_ROOT [mode]"""
import sys, json
root = sys.argv[1]
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
calibre, piece0 = world_of("world_bang.json")
G, key = 1000, 36000
bad = {"derived": 0, "head": 0}
for n in [1, 2, 3, 7, 11, 50, 99, 250, 333, 500, 501, 749, 750, 751, 1000, 5000, 50000, 500000, 5000000]:
    out = {}
    for mode in ("derived", "head"):
        T.VERIFY.update(mode=mode, sign=1, gw=4, vw=6, spring=(mode == "head"), restore=True, log=[])
        piece = json.loads(json.dumps(piece0)); piece["seed"][0]["quanta"] = n
        c = Clock(calibre, piece)
        x0 = int(c.train(REGULATOR).gears[0].now.min())
        c.tick()
        x = c.train(REGULATOR).gears[0].now
        row = T.VERIFY["log"][0]
        w = c.teeth
        out[mode] = (int(x.min()), int(x.max()), row)
    xd, xh = out["derived"][0], out["head"][0]
    row = out["derived"][2]
    g0, v0, k0 = (row["pot"] - row["spr"]) // w, row["spr"] // w, row["kin"]
    want_d = x0 + (4 * n * x0) // G            # X0 (1 + 4 n / Gamma), exact here since X0 = Gamma
    want_h = x0 + (4 * n * x0 + 1) // (3 * G)  # X0 (1 + (4/3) n / Gamma) rounded
    ok_d = xd == want_d and out["derived"][0] == out["derived"][1]
    bad["derived"] += not ok_d
    print(f"n {n:>8}: G0 {g0} (n key {n * key}) V0 {v0} K0 {k0} forms {row['forms']} | derived X1 {xd} want {want_d} {'ok' if ok_d else 'DIFF'}"
          f" | head X1 {xh} vs (4/3) {want_h} {'ok' if abs(xh - want_h) <= 1 else 'DIFF'}")
print("derived first steps off X0 (1 + 4 n / Gamma):", bad["derived"])
