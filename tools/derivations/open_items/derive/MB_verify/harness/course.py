"""Draft C's harness: the one big bang world (tests/worlds/world_bang.json on universe_bang.json) run on a source tree,
the drive chosen by name, the course read at every tick: the stretch X at every Node-clock (its least and largest), the
whole-board turnovers (all 64 Node-clocks in one tick, the bangs), the local turnovers, the fittings (births), the clicks
whose books close (the board's wind lost equals the chimes' booked plus the remainder's rise, test_the_record's form),
and the rewind (n ticks forward and n back, the state bit for bit).
Usage: python -I course.py <root> <drive> <quanta> <ticks> [<rewind> [<trace>|- [<rewind_from>]]]
  <root>   the source tree (its src and tests are put first on sys.path)
  <drive>  pure (the tree's own carry) | head (the head's carry copied in drives.py) | nocap | any drive of drives.py
"""
import sys
import json
import time

root, drive_name, quanta, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rewind_n = int(sys.argv[5]) if len(sys.argv) > 5 else 20
trace_out = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != "-" else None
rewind_from = int(sys.argv[7]) if len(sys.argv) > 7 else 0
import os

here = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path[:0] = [root + "/src", root, here]

from tests.laws import world_of, run_back_exact, state_of  # noqa: E402
import hashlib  # noqa: E402
from event_universe import click, hands, readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from event_universe.features import stretch as stretch_feature  # noqa: E402

if drive_name != "pure":
    import drives  # noqa: E402

    drives.install(T, drive_name)

calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece))
piece["seed"][0]["quanta"] = quanta

books = []
open_books = []
clicked = click.click


def board(clock):
    reads = [readings.gearing_of(clock, r, clock.start_load, clock.start_factors) for r in clock.hands()]
    return sum(int(hands.wind(clock, r.gears, g).sum()) for r, g in zip(clock.hands(), reads, strict=True))


def booked(clock, starts, held, going=1, note=None):
    if going != 1:
        return clicked(clock, starts, held, going, note)
    wind, slack, log_from = board(clock), int(clock.slack.sum()), len(clock.log)
    clicked(clock, starts, held, going, note)
    new = clock.log[log_from:]
    chimes = sum(int(e["booked"]) for e in new if e["event"] == "credit")
    clicks = sum(1 for e in new if e["event"] in ("credit", "birth"))
    after = board(clock)
    closed = wind - after == chimes + int(clock.slack.sum()) - slack
    books.append((closed, clicks))
    if not closed:
        kinds = {}
        for e in new:
            kinds[e["event"]] = kinds.get(e["event"], 0) + 1
        open_books.append((clock.ticks, wind - after - chimes - int(clock.slack.sum()) + slack, int(clock.turned_over.sum()), kinds))


def make_clock():
    found = Clock(calibre, piece)
    if drive_name != "pure" and hasattr(drives, "PREPARE") and drive_name in drives.PREPARE:
        drives.PREPARE[drive_name](found)
    return found


click.click = booked
t0 = time.time()
clock = make_clock()
size = 1
for n in clock.size:
    size *= n
X0 = clock.train(REGULATOR).gears[0].now
line = [("seed", int(X0.min()), int(X0.max()))]
whole, local = [], 0
fell, rose_sites, kept = 0, 0, None
stopped_ticks, whole_at_stop = 0, []
for at in range(1, ticks + 1):
    gear = clock.train(REGULATOR).gears[0]
    held_now, held_before = gear.now.copy(), gear.before.copy()
    stopped = readings.stopped_of(clock, stretch_feature.load_of(clock.full_rate, gear.now))
    stopped_ticks += int(stopped.sum())
    clock.tick()
    X = clock.train(REGULATOR).gears[0].now
    still = ~clock.turned_over
    fell += int(((X - held_now < held_now - held_before) & still).sum())
    rose_sites += int(still.sum())
    turned = int(clock.turned_over.sum())
    if turned == size:
        whole.append(at)
        if bool(stopped.all()):
            whole_at_stop.append(at)
    elif turned:
        local += turned
    line.append((at, int(X.min()), int(X.max()), turned))
births = clock.counts["births"]
print(f"tree {root.rsplit('/', 2)[-2] + '/' + root.rsplit('/', 1)[-1]}  drive {drive_name}  quanta {quanta}  ticks {ticks}")
print(f"seed X {line[0][1]}..{line[0][2]}")
print("tick: X least..largest [turned over]")
for row in line[1:]:
    at, lo, hi, turned = row
    print(f"  {at}: {lo}..{hi}" + (f" [{turned}]" if turned else ""))
print(f"whole-board turnovers (bangs): {len(whole)} at ticks {whole}")
print(f"local turnovers (Node-clocks): {local}")
print(f"whole-board turnovers with every Node-clock stopped at the tick's start (the rate chain's zero): {len(whole_at_stop)} at {whole_at_stop}; stopped Node-clock ticks {stopped_ticks}")
print(f"the first difference fell (X+ - X < X - X-) at {fell} of {rose_sites} Node-clock ticks not turned over")
print(f"births (fittings and mergers): {births}; chimes {clock.counts['body_clicks']}")
closed = sum(1 for c, _ in books if c)
print(f"books: closed at {closed} of {len(books)} clicks' phases, clicks among them {sum(k for _, k in books)}")
for row in open_books:
    print(f"  books open at tick {row[0]}: the wind lost less the booked and the remainder's rise {row[1]}, turned over {row[2]}, events {row[3]}")
print(f"largest |X|: {max(max(abs(r[1]), abs(r[2])) for r in line)}")
if trace_out and drive_name != "pure":
    with open(trace_out, "w") as f:
        for row in drives.TRACE:
            f.write(json.dumps(row) + "\n")
print("state hash", hashlib.sha256(state_of(clock).encode()).hexdigest()[:16])
click.click = clicked
if rewind_n:
    start = make_clock()
    for _ in range(rewind_from):
        start.tick()
    print(f"rewind from tick {rewind_from}: {run_back_exact(start, rewind_n)} of {rewind_n}")
print(f"seconds {time.time() - t0:.1f}")
