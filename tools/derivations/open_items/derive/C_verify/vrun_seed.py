"""Verifier's driver for other seeds of the light (the cycle lay's sixteen digits p1 and cz): the light-only world (no
gapped row) at a quanta, a mode of the verifier's engine copy, the course's turnovers. Usage:
python -I vrun_seed.py <root> <mode> <quanta> <ticks> <p1>(16 digits, or 'plan') CZ [key=value ...]"""
import sys, json
root, mode, quanta, ticks, p1, cz = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6])
opts = dict(kv.split("=", 1) for kv in sys.argv[7:])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import tick as T, click  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
calibre["rows"] = []
piece["seed"][0]["quanta"] = quanta
if p1 != "plan":
    piece["seed"][0]["p1"] = [int(ch) for ch in p1]
piece["seed"][0]["cz"] = cz
T.VERIFY.update(mode=mode, sign=1, gw=4, vw=6, spring=bool(int(opts.get("spring", 0))), restore=True, log=[])
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
log = T.VERIFY["log"]
print(f"mode {mode} quanta {quanta} p1 {p1} cz {cz}: seed forms {log[0]['forms']}, K0 {log[0]['kin']}, (pot - spr) {log[0]['pot'] - log[0]['spr']}")
every = int(opts.get("every", 10))
print("  X: " + "  ".join(f"t{t}:{v[0]}" + ("" if v[0] == v[1] else f"..{v[1]}") for t, v in enumerate(xs) if t and (t % every == 0 or t in whole)))
print(f"  whole-board turnovers {len(whole)} at {whole[:30]}{' ...' if len(whole) > 30 else ''}; local {local}")
