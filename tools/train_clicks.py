"""The train's reader (DETECTOR, the one measurement; the advisor, #1515 comment 5907540901): a run's output read against the train world's expectation file, per quantum which groups rose and whether both halves of the screen rose, and the summary: the rises per quantum (the mean), the both-halves rate, the neither rate, the exactly-one rate, and the rises per group across the axis beside the blind row. Every number is the world's files' and the run's output's: the groups are the world's detectors whose Nodes share one coordinate on the axis the expectation names (`across`), ordered by it; the quanta are the expectation's list, each with the interval its peak reaches the slab's first Node along the beam (`peak`, the beam's axis `along`) and its window for reference; the pace is the expectation's (`pace`, [Links, intervals]); a click line at a Node and an interval belongs to the quantum whose peak passes that Node nearest in time (a rise comes while the packet's mass climbs at the Node, before its peak passes it, and the fall after, so the nearest peak names the quantum on either side); the halves are the expectation's ranges on the axis; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/train_clicks.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe.loader.keys import AXES
from event_universe.loader.world import DetectorRow
from event_universe.world_files import load_world


def placed(detectors: tuple[DetectorRow, ...], axis: int) -> list[tuple[str, int]]:
    """The groups a reading across `axis` can place: every detector of declared Nodes whose Nodes share one coordinate on that axis, with it, ordered by it."""
    found = []
    for row in detectors:
        shared = {node[axis] for node in row.positions}
        if row.body is None and len(shared) == 1:
            found.append((row.name, shared.pop()))
    return sorted(found, key=lambda group: group[1])


def nearest(peaks: list[int], pace: tuple[int, int], first: int, at: int, tick: int) -> int:
    """The quantum whose peak passes the Node at coordinate `at` along the beam nearest to `tick`: its peak reaches the slab's first Node at `peaks[k]` and moves `pace` Links per `pace` intervals, so the distance in intervals times the pace's Links is |Links x (tick - peak) - intervals x (at - first)|; the earliest of equals."""
    links, intervals = pace
    return min(
        range(len(peaks)), key=lambda k: (abs(links * (tick - peaks[k]) - intervals * (at - first)), k)
    )


def reading(world: Path, output: Path, expectation: Path) -> dict[str, object]:
    """The reading: per quantum the groups that rose (by their coordinate across the beam), its rises, the halves that rose and its rises within the file's window; the summary over the quanta; the rises per group beside the blind row."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    loaded = load_world(world)
    across, along = AXES.index(expected["across"]), AXES.index(expected["along"])
    groups = placed(loaded.detectors, across)
    names = {name: at for name, at in groups}
    first = min(node[along] for row in loaded.detectors if row.name in names for node in row.positions)
    quanta = [dict(quantum) for quantum in expected["quanta"]]
    peaks = [int(quantum["peak"]) for quantum in quanta]
    pace = (int(expected["pace"][0]), int(expected["pace"][1]))
    halves = {str(name): (int(span[0]), int(span[1])) for name, span in expected["halves"].items()}
    per_group = dict.fromkeys(names, 0)
    rose: list[dict[int, int]] = [{} for _ in quanta]
    within = [0 for _ in quanta]
    for line in lines:
        if line.get("event") != "click" or line.get("family") != expected["family"]:
            continue
        if line.get("detector") not in names:
            continue
        tick, node = int(str(line["tick"])), [int(i) for i in list(line["node"])]  # type: ignore[call-overload]
        k = nearest(peaks, pace, first, node[along], tick)
        at = names[str(line["detector"])]
        rose[k][at] = rose[k].get(at, 0) + 1
        per_group[str(line["detector"])] += 1
        for number, quantum in enumerate(quanta):
            window = quantum["window"]
            within[number] += int(window[0]) <= tick <= int(window[1])
    rows = []
    for number, quantum in enumerate(quanta):
        risen = {name: any(a <= at <= b for at in rose[number]) for name, (a, b) in halves.items()}
        rows.append(
            {
                **quantum,
                "groups": sorted(rose[number]),
                "rises": sum(rose[number].values()),
                "halves": [name for name, up in risen.items() if up],
                "within_window": within[number],
            }
        )
    counted = [sum(1 for row in rows if len(row["halves"]) == n) for n in range(len(halves) + 1)]  # type: ignore[arg-type]
    rises = [row["rises"] for row in rows]
    return {
        "verdict": "DETECTOR",
        "family": expected["family"],
        "across": expected["across"],
        "groups": [at for _name, at in groups],
        "quanta": rows,
        "rises_in_all": sum(rises),  # type: ignore[arg-type]
        "rises_per_quantum": [sum(rises), len(rows)],  # type: ignore[list-item]
        "both": [counted[-1], len(rows)],
        "neither": [counted[0], len(rows)],
        "one": [sum(counted[1:-1]), len(rows)],
        "per_group": [per_group[name] for name, _at in groups],
        "blind": expected.get("counts"),
        "blind_through": expected.get("through"),
        "blind_per_quantum": expected.get("per_quantum"),
        "nature": expected.get("nature"),
        "clicks_in_all": sum(1 for line in lines if line.get("event") == "click"),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--world", type=Path, required=True, help="the world file the run ran")
    parser.add_argument("--output", type=Path, required=True, help="the run's output file")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.output, args.expectation)))


if __name__ == "__main__":
    main()
