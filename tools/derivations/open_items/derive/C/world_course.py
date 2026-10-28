"""Draft C: the stretch's least and largest at every tick of any world file, on a source tree (the drive as the tree has
it), with the births and the turnovers: a reading of how the drive moves a world that is not alike at every Node-clock.
Usage: python -I world_course.py <root> <world> <ticks>"""
import sys

root, world, ticks = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402

calibre, piece = world_of(world)
clock = Clock(calibre, piece)
X = clock.train(REGULATOR).gears[0].now
print(f"{world} on {root.rsplit('/', 2)[-2]}/{root.rsplit('/', 1)[-1]}: seed X {int(X.min())}..{int(X.max())}, Node-clocks {X.size}")
for at in range(1, ticks + 1):
    clock.tick()
    X = clock.train(REGULATOR).gears[0].now
    print(f"  {at}: X {int(X.min())}..{int(X.max())}, turned over {int(clock.turned_over.sum())}, births so far {clock.counts['births']}")
