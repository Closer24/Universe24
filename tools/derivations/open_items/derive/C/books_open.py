"""Draft C: where the books open under a drive (diagnostic): the course.py books reading, and at every phase that does
not close, the births and credits of the phase with their Node-clocks, the stretch there and the loads (a load below 0,
read at 0 by readings.rates_of, F5), and whether a turned-over Node-clock stands among the ends.
Usage: python -I books_open.py <root> <drive> <quanta> <ticks>"""
import json
import os
import sys

root, drive_name, quanta, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
here = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path[:0] = [root + "/src", root, here]
from tests.laws import world_of  # noqa: E402
from event_universe import click, hands, readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
import drives  # noqa: E402

if drive_name != "pure":
    drives.install(T, drive_name)
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece))
piece["seed"][0]["quanta"] = quanta
clicked = click.click


def board(clock):
    reads = [readings.gearing_of(clock, r, clock.start_load, clock.start_factors) for r in clock.hands()]
    return sum(int(hands.wind(clock, r.gears, g).sum()) for r, g in zip(clock.hands(), reads, strict=True))


def booked(clock, starts, held, going=1, note=None):
    wind, slack, log_from = board(clock), int(clock.slack.sum()), len(clock.log)
    X = clock.train(REGULATOR).gears[0].now.copy()
    load = clock.start_load.copy()
    clicked(clock, starts, held, going, note)
    new = clock.log[log_from:]
    chimes = sum(int(e["booked"]) for e in new if e["event"] == "credit")
    gap = wind - board(clock) - chimes - int(clock.slack.sum()) + slack
    if gap:
        print(f"tick {clock.ticks}: open by {gap}; turned over {int(clock.turned_over.sum())}; least load {int(load.min())}")
        for e in new:
            if e["event"] == "birth":
                ends = [tuple(e["node"])] + ([tuple(x) for x in e["clock_ends"]] if isinstance(e.get("clock_ends"), list) and e["clock_ends"] and isinstance(e["clock_ends"][0], (list, tuple)) else [])
                at = tuple(e["node"])
                print(f"   birth at {at}: merger {'takes' in e}, X {int(X[at])}, load {int(load[at])}, turned {bool(clock.turned_over[at])}, keys booked {e.get('booked')} taken {e.get('taken')} rem {e.get('remainder_was')}->{e.get('remainder')}")


click.click = booked
clock = Clock(calibre, piece)
for _ in range(ticks):
    clock.tick()
