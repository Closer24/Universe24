"""Verifier's driver: one massive hand laid at rest at every Node-clock (the fourth form, `sea`, sense 1), no light
laid, on the verifier's engine copy; the course of the time gear under a mode (derived: GR's (V); R: GR's 00 equation,
X'' = X'^2/(2X) - (kappa/3) X (4K - 2V), the seed's constraint residual kept as curvature with no number stored),
its whole-board turnovers, the books, the rewind (the head's helper; mode R's velocity term is not exactly
invertible, so a failed rewind there is expected).
Usage: python -I vrun_sea.py <root> <mode> <pinion> <quanta> <ticks> [every=n] [rewind=n]"""
import sys, json, hashlib
root, mode, pinion, quanta, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
opts = dict(kv.split("=", 1) for kv in sys.argv[6:])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of, run_back_exact, state_of  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
rim = calibre["integers"]["den"]
calibre["rows"] = [{"shape": 2, "pair": [pinion, rim]}]
piece["seed"] = [{"lay": "sea", "row": 1, "quanta": quanta, "sense": 1}]
T.VERIFY.update(mode=mode, sign=1, gw=4, vw=6, spring=False, restore=True, log=[])
c = Clock(calibre, piece)
size = c.size[0] ** 3
xs, whole, local = [int(c.train(REGULATOR).gears[0].now.min())], [], 0
for t in range(1, ticks + 1):
    c.tick()
    x = c.train(REGULATOR).gears[0].now
    n = int(c.turned_over.sum())
    if n == size:
        whole.append(t)
    else:
        local += n
    xs.append((int(x.min()), int(x.max())))
r0 = T.VERIFY["log"][0]
print(f"mode {mode} pinion/rim {pinion / rim:.4f} quanta {quanta}: seed forms {r0['forms']}, K0 {r0['kin']}, V0 {r0['spr'] // c.teeth}; 4K0 - 2V0 {4 * r0['kin'] - 2 * (r0['spr'] // c.teeth)}")
every = int(opts.get("every", 10))
print("  X: " + "  ".join(f"t{t}:{v[0]}" + ("" if v[0] == v[1] else f"..{v[1]}") for t, v in enumerate(xs) if t and (t % every == 0 or t in whole)))
print(f"  whole-board turnovers {len(whole)} at {whole[:40]}{' ...' if len(whole) > 40 else ''}; local {local}; births {c.counts['births']}")
print("  state hash", hashlib.sha256(state_of(c).encode()).hexdigest()[:16])
if int(opts.get("rewind", 0)):
    T.VERIFY["log"] = None
    print(f"  rewind from 0: {run_back_exact(Clock(calibre, piece), int(opts['rewind']))} of {opts['rewind']}")
