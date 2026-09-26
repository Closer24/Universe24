"""Item 51's proof: the old engine (d8ce79bd, the worktree wt_old) on the old world files and
the new engine (wt_ec) on the regenerated files give the same rows, the same lines and the
same held levels at every interval. Argument: the world's relative path under examples/events,
the intervals."""

import json
import sys
from pathlib import Path

import numpy as np

S = Path("/tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad")


def engine(root: Path):
    sys.path.insert(0, str(root / "src"))
    for name in list(sys.modules):
        if name.startswith("event_universe"):
            del sys.modules[name]
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.events.world import parse_nature_beam_world

    sys.path.pop(0)
    return DetectorLawSimulation, parse_nature_beam_world


def run(root: Path, world: Path, ticks: int, new: bool):
    Sim, parse = engine(root)
    lines: list[dict] = []
    document = json.loads(world.read_text())
    sim = Sim(parse(document), observer=lines.append)
    snapshots = []
    for _ in range(ticks):
        sim.step()
        rows = {
            int(k): (v.now.copy(), v.before.copy(), v.remainder.copy()) for k, v in sim.records.items()
        }
        if new:
            held = {sim.families[f].held: r.now.copy() for f, r in sim.held_records.items()}
        else:
            held = {"content": sim.clock_record.now.copy(), "charge": sim.charge_record.now.copy()}
        # item 59: the held quanta keyed by family name (the families file reorders the list)
        quanta = [
            {
                RENAME.get(sim.families[f].name, sim.families[f].name): q
                for f, q in enumerate(row)
                if q != 0
            }
            for row in sim.held
        ]
        snapshots.append((rows, held, quanta))
    return snapshots, lines


rel, ticks = sys.argv[1], int(sys.argv[2])
# an optional third argument old=new renames a family of the old file (the point emitter's
# seat family is "point" in the families file, "matter" in the old inline list)
RENAME = dict(pair.split("=") for pair in sys.argv[3:])
old_snap, old_lines = run(
    S / "wt_old", S / "wt_old" / "examples" / "events" / rel, ticks, True
)  # item 57: both heads past item 51
new_snap, new_lines = run(S / "wt_ec", S / "wt_ec" / "examples" / "events" / rel, ticks, True)
bad = 0
for t, ((ro, ho, qo), (rn, hn, qn)) in enumerate(zip(old_snap, new_snap, strict=True), 1):
    if sorted(ro) != sorted(rn):
        print("interval", t, "records differ", sorted(ro), sorted(rn))
        bad += 1
        break
    for k in ro:
        for a, b, what in zip(ro[k], rn[k], ("now", "before", "remainder"), strict=True):
            if not np.array_equal(a, b):
                print("interval", t, "record", k, what, "differs")
                bad += 1
    for source in ho:
        if not np.array_equal(ho[source], hn[source]):
            print("interval", t, "held", source, "differs")
            bad += 1
    if qo != qn:
        print("interval", t, "held quanta differ")
        bad += 1
    if bad > 5:
        break
    if bad and t >= 1 and "first_bad" not in dir():
        first_bad = t


def strip(line):
    return {
        k: (RENAME.get(v, v) if k == "family" else v) for k, v in line.items() if k not in ("input",)
    }


same_lines = [strip(a) for a in old_lines] == [strip(b) for b in new_lines]
print("first differing interval", first_bad) if "first_bad" in dir() else None
print(
    f"{rel}: {ticks} intervals, {len(old_lines)} lines; rows and held levels {'BIT FOR BIT' if bad == 0 else 'DIFFER'}; lines {'identical' if same_lines else 'DIFFER'}"
)
if not same_lines:
    for a, b in zip(old_lines, new_lines, strict=False):
        if strip(a) != strip(b):
            print(
                "first differing line:",
                {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)},
            )
            break
