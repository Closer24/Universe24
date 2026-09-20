"""Read the amplitude law's world from a run's register: replay the apparatus's
Port events of `events.jsonl` (the births, the clicks, the reads and the
re-emissions at the sets, the splits, the cancels) through the layer
(`event_universe.events.amplitude.Layer`) and print the world's list of
clicks, the gathers, labelled DETECTOR, with the GameBoard's lines (the
splits and the cancels) labelled GAMEBOARD; with `--check` the replayed
list is compared with `run.json`'s `world` (the design's acceptance test 10:
the register's replay equals the run's world), the clicks per set are
counted and the process exits 1 on a difference.

    python tools/amplitude_path.py RUN_DIR [--check] [--quiet]

The register carries everything the layer read at run time: the `birth`
lines (the record, its u, labels, arms and units), the `click` lines of
the sets, the faces and the border (the record, branch, multiplicity,
amount, phase and, at a rotated set, the window and turn), the `read` and
`rerelease` lines at `sum` sets (the rows taken: record, branch,
multiplicity, amount, phase, arrival), the `split` lines (the units
absorbed and born, the rebirth flag and the entry's phase), the `gate`
lines (the survivor and the records joined), the `rotate` lines, the
`cancel` lines and the `gather` lines the layer wrote. The layer is built as the
engine built it (`NatureBeamSimulation(world).layer`, no interval run) so
that its sets carry the run's names and order; the completions are taken
at the two points of the interval where the engine takes them (after the
clicks of step 4, before the self-creations; and at the interval's end,
after the merge).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world  # noqa: E402
from event_universe.events.amplitude import Layer  # noqa: E402
from event_universe.events.world import FACE_NAMES, LIFETIME_NAME  # noqa: E402

DETECTOR, GAMEBOARD = "DETECTOR", "GAMEBOARD"


def sets_by_number(layer: Layer) -> dict[int, int]:
    """The layer's set index per measured event's number."""
    found: dict[int, int] = {}
    for set_index, key in enumerate(layer.keys):
        if key[0] == "set":
            for number in layer.sets[key[1]].numbers:
                found[number] = set_index
    return found


def set_index_of(layer: Layer, by_number: dict[int, int], line: dict[str, Any]) -> int:
    """The layer's index of the set a line names: a detector by name, an
    undeclared set by its measured event's number, a face, the border."""
    detector = line.get("detector")
    if detector is None:
        return int(by_number[int(line["measured"])])
    name = str(detector)
    if name in FACE_NAMES:
        return int(layer.face_index[FACE_NAMES.index(name)])
    if name == LIFETIME_NAME:
        assert layer.border_index is not None
        return int(layer.border_index)
    return int(layer.names.index(name))


def is_sum(layer: Layer, set_index: int) -> bool:
    key = layer.keys[set_index]
    return bool(key[0] == "set" and layer.sets[key[1]].sum)


def replay(run: Path, quiet: bool = True) -> tuple[Layer, list[dict[str, Any]]]:
    """Replay the run's register through a fresh layer; returns the layer
    and the gathers it wrote."""
    world = parse_nature_beam_world(json.loads((run / "initialization.json").read_text("utf-8")))
    if not world.amplitude:
        raise SystemExit(f"{run}: the world does not declare the key `amplitude`")
    simulation = NatureBeamSimulation(world)
    layer = simulation.layer
    assert layer is not None
    family_index = {name: index for index, name in enumerate(layer.families)}
    by_number = sets_by_number(layer)
    tick = 0
    completed_before_creations = False

    def complete() -> None:
        for live in layer.complete(tick):
            gather = live.gather
            assert gather is not None
            if not quiet:
                print(DETECTOR, json.dumps(gather))

    with (run / "events.jsonl").open(encoding="utf-8") as stream:
        for raw in stream:
            line = json.loads(raw)
            event = line.get("event")
            line_tick = int(line.get("tick", tick))
            if line_tick != tick:
                tick = line_tick
                completed_before_creations = False
            if event in ("split", "birth", "gather") and not completed_before_creations:
                # The engine completes the records after the clicks of
                # step 4 and before the self-creations (a chosen re-emitter
                # then re-creates a new record), and again after the merge:
                # a `gather` line marks either completion.
                complete()
                completed_before_creations = event != "gather"
            if event == "birth":
                labels = {int(label): int(weight) for label, weight in line["labels"]}
                layer.birth(
                    tick,
                    int(line["record"]),
                    family_index[str(line["family"])],
                    int(line["u"]),
                    labels,
                    int(line["arms"]),
                    int(line["units"]),
                )
            elif event == "click":
                record = int(line.get("record", 0))
                if record:
                    rotation = None
                    if "turn" in line:
                        rotation = (int(line["window"]), int(line["turn"]))
                    node = line["node"]
                    layer.end(
                        tick,
                        set_index_of(layer, by_number, line),
                        record,
                        int(line["branch"]),
                        int(line["multiplicity"]),
                        int(line["amount"]),
                        int(line["phase"]),
                        rotation=rotation,
                        node=(int(node[0]), int(node[1]), int(node[2])),
                        content=int(line["content"]),
                        momentum=[int(v) for v in line.get("momentum", line.get("push", []))],
                    )
            elif event in ("read", "rerelease"):
                set_index = set_index_of(layer, by_number, line)
                if is_sum(layer, set_index):
                    rotation = None
                    if "turn" in line:
                        rotation = (int(line["window"]), int(line["turn"]))
                    node = line["node"]
                    for record, branch, multiplicity, amount, phase, _ in line.get("rows", []):
                        if record:
                            layer.end(
                                tick,
                                set_index,
                                int(record),
                                int(branch),
                                int(multiplicity),
                                int(amount),
                                int(phase),
                                absorbed=event == "rerelease",
                                rotation=rotation,
                                node=(int(node[0]), int(node[1]), int(node[2])),
                            )
            elif event == "split":
                record = int(line["record"])
                set_index = by_number[int(line["measured"])]
                if not quiet:
                    print(GAMEBOARD, json.dumps(line))
                if line.get("rebirth"):
                    # One birth per rebirth, every row's units by its split.
                    if layer.resolve(record) is None:
                        layer.birth(
                            tick, record, family_index[str(line["family"])], int(line["u"]), {0: 1}, 1, 0
                        )
                    layer.split(record, 0, int(line["born"]))
                else:
                    absorbed = 0 if is_sum(layer, set_index) else int(line["absorbed"])
                    layer.split(record, absorbed, int(line["born"]))
            elif event == "gate":
                # The gate's join: the records named join the survivor (the
                # rows' relabelling is the GameBoard's; the layer's labels,
                # arms and live count follow).
                if not quiet:
                    print(GAMEBOARD, json.dumps(line))
                layer.join(
                    tick,
                    int(line["survivor"]),
                    [int(other) for other in line["joined"]],
                    {
                        int(identity): {int(label) for label in labels}
                        for identity, labels in line["present"]
                    },
                )
            elif event == "rotate":
                # The rotation's amounts: w becomes w C' + w S' per row, the
                # live count following.
                if not quiet:
                    print(GAMEBOARD, json.dumps(line))
                for record, absorbed, born in line.get("records", []):
                    layer.split(int(record), int(absorbed), int(born))
                for record in sorted({int(item[0]) for item in line.get("records", [])}):
                    layer.rotate(record, int(line["bit"]))
            elif event == "cancel":
                if not quiet:
                    print(GAMEBOARD, json.dumps(line))
                layer.cancel(int(line["record"]), int(line["amount"]))
            elif event == "step":
                complete()
                completed_before_creations = False
    return layer, list(layer.gathers)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("run", type=Path, help="A run directory of the amplitude law")
    parser.add_argument("--check", action="store_true", help="Compare with run.json's world")
    parser.add_argument("--quiet", action="store_true", help="Print the summary only")
    args = parser.parse_args()
    layer, gathers = replay(args.run, quiet=args.quiet)
    counts = Counter(str(g["chosen"][0][0]) if g["chosen"] else "none" for g in gathers)
    print(
        f"{DETECTOR} gathers {len(gathers)}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    )
    print(f"{GAMEBOARD} open records {layer.report()['open']}")
    if args.check:
        world = json.loads((args.run / "run.json").read_text("utf-8")).get("world")
        if world != gathers:
            print(
                f"the replay differs from run.json's world ({len(gathers)} against {len(world or [])})"
            )
            raise SystemExit(1)
        print(f"{DETECTOR} the replay equals run.json's world")


if __name__ == "__main__":
    main()
