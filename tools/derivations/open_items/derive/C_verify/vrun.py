"""Verifier's driver (derive/C_verify; integers only): the one big bang world on the verifier's own engine copy (eng/,
the head's src with the switches of eng_tick.diff.txt), or the same world with the light alone (no gapped row, so no
fitting can break the board's sameness: a pure A1 course). Reads the course: X per tick (least..largest), the
whole-board turnovers, the local ones, the falls of the first difference at the Node-clocks not turned over, the
births, the books per click phase (the board's hand wind lost = chimes booked + slack rise), the state hash and the
rewind (tests.laws.run_back_exact, the head's helper, from tick FROM).
Usage: python -I vrun.py <root> <world> <mode> <quanta> <ticks> [key=value ...]
  ROOT   an engine tree with tick.VERIFY (the verifier's copy) or any tree (MODE pure: the tree's own carry)
  WORLD  bang | light
  MODE   head | derived | pure
  keys   sign=-1  gw=3  vw=3  spring=1  restore=0  rewind=20  rewind_from=0  log=FILE  every=1"""
import sys, json, hashlib, time
root, world, mode, quanta, ticks = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
opts = dict(kv.split("=", 1) for kv in sys.argv[6:])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of, run_back_exact, state_of  # noqa: E402
from event_universe import click, hands, readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402

if mode != "pure":
    T.VERIFY.update(mode=mode, sign=int(opts.get("sign", 1)), gw=int(opts.get("gw", 4)), vw=int(opts.get("vw", 6)),
                    spring=bool(int(opts.get("spring", 1 if mode == "head" else 0))),
                    restore=bool(int(opts.get("restore", 1))), log=[] if "log" in opts else None)
calibre, piece = world_of("world_bang.json")
calibre, piece = json.loads(json.dumps(calibre)), json.loads(json.dumps(piece))
if world == "light":
    calibre["rows"] = []
piece["seed"][0]["quanta"] = quanta
clicked = click.click
books = []

def board(clock):
    reads = [readings.gearing_of(clock, r, clock.start_load, clock.start_factors) for r in clock.hands()]
    return sum(int(hands.wind(clock, r.gears, g).sum()) for r, g in zip(clock.hands(), reads, strict=True))

def booked(clock, starts, held, going=1, note=None):
    if going != 1:
        return clicked(clock, starts, held, going, note)
    before, slack, n = board(clock), int(clock.slack.sum()), len(clock.log)
    clicked(clock, starts, held, going, note)
    chimes = sum(int(e["booked"]) for e in clock.log[n:] if e["event"] == "credit")
    books.append(before - board(clock) == chimes + int(clock.slack.sum()) - slack)

click.click = booked
t0 = time.time()
clock = Clock(calibre, piece)
size = clock.size[0] ** 3
whole, local, fell, still_ticks, rows = [], 0, 0, 0, []
every = int(opts.get("every", 1))
for at in range(1, ticks + 1):
    g = clock.train(REGULATOR).gears[0]
    x1, x0 = g.now.copy(), g.before.copy()
    clock.tick()
    x2 = clock.train(REGULATOR).gears[0].now
    turned = clock.turned_over
    fell += int(((x2 - x1 < x1 - x0) & ~turned).sum())
    still_ticks += int((~turned).sum())
    n = int(turned.sum())
    if n == size:
        whole.append(at)
    else:
        local += n
    rows.append((at, int(x2.min()), int(x2.max()), n))
print(f"root {root.rsplit('/', 1)[-1]} world {world} mode {mode} quanta {quanta} ticks {ticks} opts {opts}")
for at, lo, hi, n in rows:
    if at % every == 0 or n or at <= 3:
        print(f"  {at}: {lo}..{hi}" + (f" [{n}]" if n else ""))
print(f"bangs (whole-board turnovers): {len(whole)} at {whole}")
print(f"local turnovers: {local}")
print(f"first difference fell at {fell} of {still_ticks} Node-clock ticks not turned over")
print(f"births {clock.counts['births']}; books closed {sum(books)} of {len(books)}")
print(f"largest X {max(r[2] for r in rows)}")
print("state hash", hashlib.sha256(state_of(clock).encode()).hexdigest()[:16])
click.click = clicked
if mode != "pure" and T.VERIFY["log"] is not None:
    with open(opts["log"], "w") as f:
        for row in T.VERIFY["log"]:
            f.write(json.dumps(row) + "\n")
    T.VERIFY["log"] = None
rw = int(opts.get("rewind", 0))
if rw:
    start = Clock(calibre, piece)
    for _ in range(int(opts.get("rewind_from", 0))):
        start.tick()
    print(f"rewind from tick {opts.get('rewind_from', 0)}: {run_back_exact(start, rw)} of {rw}")
print(f"seconds {time.time() - t0:.1f}")
