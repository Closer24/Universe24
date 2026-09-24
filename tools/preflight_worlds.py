"""The pre-GO check of the world files: LOAD every world RUN_LIST.md names, run none.

The model owner's rule (2026-09-24, through the Boss at 04:30Z): nothing runs before it
is checked and approved. This tool does the engine's half of the preflight at the GO
without a run: for every world file named in a run list (`docs/designs/detector_law/
RUN_LIST.md` by default; the backticked `*.json` names in its tables, a brace group such
as `bell_{a0b0,a0b1}.json` expanded), it resolves the file under `examples/events/`
(a path as written, or a bare name searched under that tree), decodes and parses it
with the runner's own loader (`world_loading.load_world`), runs the massive worlds'
margin rule as the runner does before its first interval (`check_margins`,
`profile_check`, printed as GAMEBOARD computations) and constructs the world's engine
(`DetectorLawSimulation` under `detector_law`, `NatureBeamSimulation` otherwise) with no
interval stepped. It prints one line per world: LOADED (the engine, the shape, the
ticks, the families and the measured events), REFUSED (the loader's or the engine's
message) or MISSING (a name the list carries and the tree does not: a world still to
write), and exits 1 when any world is refused; a missing world is reported, not a
failure (`--strict` makes it one). Nothing here runs a rule or reads a record.

    PYTHONPATH=src python tools/preflight_worlds.py
    PYTHONPATH=src python tools/preflight_worlds.py --list docs/designs/detector_law/RUN_LIST.md --root examples/events
    PYTHONPATH=src python tools/preflight_worlds.py examples/events/massive_record/layer_pin_k3_14.json
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from event_universe.diagnostics.massive_record_margin import check_margins, profile_check
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.engine import NatureBeamSimulation
from event_universe.world_loading import load_world

DEFAULT_LIST = Path("docs/designs/detector_law/RUN_LIST.md")
DEFAULT_ROOT = Path("examples/events")
NAME = re.compile(r"`([A-Za-z0-9_./{},-]*\.json)`")
BRACE = re.compile(r"\{([^{}]*)\}")


def expand(name: str) -> list[str]:
    """The names a brace group stands for: `a_{x,y}.json` is `a_x.json` and `a_y.json`;
    several groups multiply."""
    groups = BRACE.findall(name)
    if not groups:
        return [name]
    template = BRACE.sub("{}", name)
    return [template.format(*choice) for choice in product(*(group.split(",") for group in groups))]


def listed(text: str) -> list[str]:
    """Every world file name the list's text carries, in order, once each."""
    names: list[str] = []
    for found in NAME.findall(text):
        for name in expand(found):
            if name not in names and name != "expectations.json":
                names.append(name)
    return names


def resolve(name: str, root: Path) -> Path | None:
    """The file a listed name means: the path as written (relative to the checkout or to
    the root), else the one file of that base name under the root; None when none."""
    for candidate in (Path(name), root / name):
        if candidate.is_file():
            return candidate
    matches = sorted(path for path in root.rglob(Path(name).name) if path.is_file())
    if len(matches) == 1:
        return matches[0]
    return None


@dataclass(frozen=True)
class Outcome:
    name: str
    status: str  # LOADED, REFUSED or MISSING
    detail: str


def load_one(path: Path) -> Outcome:
    """Load one world file and construct its engine without stepping it."""
    try:
        loaded = load_world(path.read_bytes(), base_dir=path.parent)
        world = loaded.world
        notes: list[str] = []
        if world.massive_record:
            for reading in check_margins(world):
                notes.extend(reading.lines())
                check = profile_check(world, reading.number)
                if check is not None:
                    notes.append(
                        f"seed (GAMEBOARD): block {reading.number}: the profile against the mode at "
                        f"the amplitude {check[1]}, the largest deviation {check[0]} units"
                    )
        engine = "detector_law" if world.detector_law else "rays"
        if world.detector_law:
            DetectorLawSimulation(world)
        else:
            NatureBeamSimulation(world)
    except Exception as error:  # noqa: BLE001 - every refusal is reported, none hidden
        return Outcome(str(path), "REFUSED", f"{type(error).__name__}: {error}")
    detail = (
        f"{engine}; shape {list(world.shape)}; ticks {world.ticks}; families "
        f"{[family.name for family in world.families]}; measured {len(world.measured)}"
    )
    if notes:
        detail += "; " + " | ".join(notes)
    return Outcome(str(path), "LOADED", detail)


def preflight(names: list[str], root: Path) -> list[Outcome]:
    outcomes: list[Outcome] = []
    for name in names:
        path = resolve(name, root)
        if path is None:
            outcomes.append(Outcome(name, "MISSING", "no such file under the root (a world to write)"))
        else:
            outcomes.append(load_one(path))
    return outcomes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("worlds", nargs="*", help="world files to load (none: the list's)")
    parser.add_argument("--list", type=Path, default=DEFAULT_LIST, help="the run list (RUN_LIST.md)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="the worlds' tree")
    parser.add_argument("--strict", action="store_true", help="a missing world fails too")
    args = parser.parse_args(argv)
    names = args.worlds or listed(args.list.read_text(encoding="utf-8"))
    outcomes = preflight(names, args.root)
    for outcome in outcomes:
        print(f"{outcome.status:8} {outcome.name}: {outcome.detail}")
    counts = {
        status: sum(1 for o in outcomes if o.status == status)
        for status in ("LOADED", "REFUSED", "MISSING")
    }
    print(
        f"loaded {counts['LOADED']}, refused {counts['REFUSED']}, missing {counts['MISSING']}; no world run"
    )
    failed = counts["REFUSED"] + (counts["MISSING"] if args.strict else 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
