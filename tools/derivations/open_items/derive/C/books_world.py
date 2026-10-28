"""Draft C: the books of the head's own click on any world file, the drive untouched (a control for the open books met
under the declared curvature): at every click phase, the board's wind lost against the chimes' booked plus the remainder's
rise (test_the_record's form); the open phases listed with their births (mergers or fittings).
Usage: python -I books_world.py <root> <world> <ticks> [<quanta>]"""
import json
import sys

root, world, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3])
quanta = int(sys.argv[4]) if len(sys.argv) > 4 else None
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe import click, hands, readings  # noqa: E402
from event_universe.clock import Clock  # noqa: E402

calibre, piece = world_of(world)
piece = json.loads(json.dumps(piece))
if quanta is not None:
    piece["seed"][0]["quanta"] = quanta
clicked = click.click
phases, opened, mergers = 0, [], 0


def board(clock):
    reads = [readings.gearing_of(clock, r, clock.start_load, clock.start_factors) for r in clock.hands()]
    return sum(int(hands.wind(clock, r.gears, g).sum()) for r, g in zip(clock.hands(), reads, strict=True))


def booked(clock, starts, held, going=1, note=None):
    global phases, mergers
    wind, slack, log_from = board(clock), int(clock.slack.sum()), len(clock.log)
    clicked(clock, starts, held, going, note)
    new = clock.log[log_from:]
    chimes = sum(int(e["booked"]) for e in new if e["event"] == "credit")
    gap = wind - board(clock) - chimes - int(clock.slack.sum()) + slack
    phases += 1
    merged = sum(1 for e in new if e["event"] == "birth" and "takes" in e)
    mergers += merged
    if gap:
        opened.append((clock.ticks, gap, merged, sum(1 for e in new if e["event"] == "birth")))


click.click = booked
clock = Clock(calibre, piece)
for _ in range(ticks):
    clock.tick()
print(f"{world} quanta {quanta} ticks {ticks}: books closed at {phases - len(opened)} of {phases} phases; mergers {mergers}; births {clock.counts['births']}")
for row in opened:
    print(f"  open at tick {row[0]} by {row[1]}: mergers {row[2]} of births {row[3]}")
