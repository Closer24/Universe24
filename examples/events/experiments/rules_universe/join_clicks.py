"""THE READER OF WORLD (d), THE JOIN AND THE PARTING: the world of `lay_out_join.py` run headless through the engine's own functions with the event lines observed, and the reading of THE CLICK JOINS AND PARTS against the expectation file beside the world: THE COUNTS (GAMEBOARD), each body's held count at its Node every interval, read from the loop's block after the count's line, the first interval a count changes and the interval a count falls under the edge (the smaller dissolved) against `dissolution_intervals`; THE MOVES (GAMEBOARD), the quanta the count's line moved between the two bodies, interval by interval, from the counts' differences: a transfer is one count down and the other up by the same quanta (the total kept), a click between the bodies; a relay is the count's line laying a count anew from the record's form (THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD; the total not kept) and is no click; the first transfer's interval against `first_click_interval`, the relays counted apart; THE RECORDS (HOST), the records alive at the end against `records_at_the_end`; THE LEVELS (GAMEBOARD), the matter level at both Nodes and the support along the run from the declared readings; THE RECORD (GAMEBOARD), each body's count over the last period of the run and its period from the level's sign changes at its Node, against Cheshbon's table from the generator run as Rule3 in integers (the amplitude b, the count D bar and the period P per body, the clocks' ratio; 15:43 Israel time, the Closer 15:47). Nothing here replays a rule; no number of a run enters a test. The run of (d): `PYTHONPATH=src python tools/run_inputs.py --out runs/join --jobs 2 <join.json> <part.json>` (the reversible rows of the expectation files), then `PYTHONPATH=src python examples/events/experiments/rules_universe/join_clicks.py --table <join.json> <part.json>`; the reading is written beside the world as `<name>.clicks.json` and `--table` prints the algebra / engine / difference table for #1325."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world


def counts_of(simulation: DetectorLawSimulation) -> list[int]:
    """Each body's held count summed over its Nodes, read from the loop's block (GAMEBOARD)."""
    found = []
    for block in simulation.blocks:
        counts = getattr(block, "counts", None)
        if counts is None:
            found.append(sum(int(c) for c in (block.definition.counts or ())))
        else:
            found.append(int(counts.sum()))
    return found


def period_of(levels: list[int]) -> float | None:
    """The period in intervals from the sign changes of the level at a Node (two changes per period), None under two changes."""
    signs = [(v > 0) - (v < 0) for v in levels if v != 0]
    changes = sum(1 for a, b in zip(signs, signs[1:], strict=False) if a != b)
    return None if changes < 2 else round(2 * (len(levels) - 1) / changes, 2)


def within(value: float | None, low: float, high: float, band: float) -> str:
    """MATCH where the value lies in [low - band, high + band], MISS otherwise or where there is no value."""
    return "MISS" if value is None else ("MATCH" if low - band <= value <= high + band else "MISS")


def record_reading(
    counts: list[list[int]], levels: dict[str, list[int]], record: dict[str, Any] | None
) -> dict[str, Any]:
    """THE RECORD (GAMEBOARD): each body's count over the last period of the run (the mean of the held counts over the last P intervals, P from the level's sign changes at its Node, else the last ten) and its period, against Cheshbon's table (D bar, P, the clocks' ratio); an expectation without the table reads the numbers alone."""
    names = ["small", "deep"]
    read: dict[str, Any] = {}
    periods: list[float | None] = []
    for number, name in enumerate(names):
        series = list(levels.values())[number] if number < len(levels) else []
        period = period_of(series)
        window = int(round(period)) if period else 10
        recent = [c[number] for c in counts[-window:]]
        mean = round(sum(recent) / len(recent), 2) if recent else None
        periods.append(period)
        read[name] = {
            "count_over_the_last_period": mean,
            "period_intervals": period,
            "count_at_the_end": counts[-1][number],
        }
        if record is not None:
            expected = record["bodies"][name]
            read[name]["expected"] = {
                "amplitude_b": expected["amplitude_b"],
                "record_count": expected["record_count"],
                "period": expected["period"],
            }
            read[name]["count_verdict"] = within(mean, *expected["record_count"], 1.0)
            read[name]["period_verdict"] = within(period, *expected["period"], 1.0)
    ratio = round(periods[1] / periods[0], 3) if periods[0] and periods[1] else None
    read["clock_ratio_deep_over_small"] = ratio
    if record is not None:
        low, _mid, high = record["clock_ratio_deep_over_small"]
        read["expected_clock_ratio"] = record["clock_ratio_deep_over_small"]
        read["ratio_verdict"] = within(ratio, low, high, 0.0)
    return {"label": "GAMEBOARD", **read}


def breathing_reading(
    counts: list[list[int]], levels: dict[str, list[int]], blind: dict[str, Any]
) -> dict[str, Any] | None:
    """THE HIERARCHY IS RECURSIVE (GAMEBOARD): the breathing period of the pair's total count (the sign changes of the total about its mean over the run) against Cheshbon's P_2, and its ratio to the pixel's period (from the level's sign changes at the first body's Node) against the band; None where the expectation carries no such number."""
    if "pair_breathing_period_intervals" not in blind:
        return None
    totals = [sum(c) for c in counts]
    mean = sum(totals) / len(totals)
    pair_period = period_of([round((t - mean) * 2) for t in totals])
    pixel_period = period_of(next(iter(levels.values()), []))
    ratio = round(pair_period / pixel_period, 2) if pair_period and pixel_period else None
    low, high = blind["period_ratio_band"]
    return {
        "label": "GAMEBOARD",
        "name": blind.get("name", "THE HIERARCHY IS RECURSIVE"),
        "pair_total_start_end": [totals[0], totals[-1]],
        "pair_breathing_period_intervals": pair_period,
        "expected_pair_breathing_period_intervals": blind["pair_breathing_period_intervals"],
        "pixel_period_intervals": pixel_period,
        "expected_pixel_period_intervals": blind["pixel_period_intervals"],
        "period_ratio_pair_over_pixel": ratio,
        "expected_period_ratio": [low, blind["period_ratio_pair_over_pixel"], high],
        "verdict": within(ratio, low, high, 0.0),
    }


def table(report: dict[str, Any]) -> str:
    """The algebra / engine / difference table of one world for #1325, in Markdown: the blind number, the run's number and the difference per row; a refused run shows the refusal."""
    rows = [
        ("world", report["world"], "", ""),
        ("verdict", "LAWFUL", report["verdict"], report["refusal"] or ""),
    ]
    record = report["5_the_record"]
    for name in ("small", "deep"):
        body = record[name]
        expected = body.get("expected")
        if expected:
            rows.append(
                (
                    f"count of the {name} (D bar over the period)",
                    f"{expected['record_count'][0]} to {expected['record_count'][1]} (b = {expected['amplitude_b']})",
                    str(body["count_over_the_last_period"]),
                    body["count_verdict"],
                )
            )
            rows.append(
                (
                    f"period of the {name} (intervals)",
                    f"{expected['period'][0]} to {expected['period'][1]}",
                    str(body["period_intervals"]),
                    body["period_verdict"],
                )
            )
    if "expected_clock_ratio" in record:
        low, mid, high = record["expected_clock_ratio"]
        rows.append(
            (
                "clocks' ratio deep / small",
                f"{mid} ({low} to {high})",
                str(record["clock_ratio_deep_over_small"]),
                record["ratio_verdict"],
            )
        )
    breathing = report.get("6_the_hierarchy")
    if breathing:
        low, mid, high = breathing["expected_period_ratio"]
        rows.append(
            (
                "the pair's breathing period / the pixel's period (THE HIERARCHY IS RECURSIVE)",
                f"{breathing['expected_pair_breathing_period_intervals']} / {breathing['expected_pixel_period_intervals']} = {mid} ({low} to {high})",
                f"{breathing['pair_breathing_period_intervals']} / {breathing['pixel_period_intervals']} = {breathing['period_ratio_pair_over_pixel']}",
                breathing["verdict"],
            )
        )
    counts, moves, records = report["1_the_counts"], report["2_the_moves"], report["3_the_records"]
    rows.append(
        (
            "first click (interval; the first transfer between the bodies)",
            str(moves["expected_first_click_interval"]),
            str(moves["first_move_interval"]),
            moves["verdict"],
        )
    )
    rows.append(
        (
            "transfers / relays of the count (the relays are no clicks)",
            "",
            f"{moves['count_of_transfers']} / {moves['count_of_relays']} (the first relay at {moves['first_relay_interval']})",
            "",
        )
    )
    rows.append(
        (
            "the smaller under the edge (interval)",
            str(counts["expected_dissolution_intervals"]),
            str(counts["under_the_edge_at"]),
            counts["verdict"],
        )
    )
    rows.append(
        (
            "records at the end",
            str(records["expected"]),
            str(records["alive_at_the_end"]),
            records["verdict"],
        )
    )
    rows.append(("clicks at the faces (not counted)", "", str(records["clicks_at_the_faces"]), ""))
    lines = ["| row | the algebra (blind) | the engine | the difference |", "| --- | --- | --- | --- |"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    return "\n".join(lines)


def read(world_path: Path) -> dict[str, Any]:
    """The reading against the expectation file beside the world."""
    blind = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))["blind"]
    world = load_world(world_path)
    lines: list[dict[str, Any]] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    readings = Readings(world.readings)
    readings.read(simulation)
    counts = [counts_of(simulation)]
    refusal = None
    for _ in range(world.ticks):
        try:
            simulation.step()
        except (RuntimeError, ValueError) as stop:
            refusal = f"at interval {simulation.tick + 1}: {stop}"
            break
        readings.read(simulation)
        counts.append(counts_of(simulation))
    moves = [
        {
            "interval": i,
            "left": counts[i][0] - counts[i - 1][0],
            "right": counts[i][1] - counts[i - 1][1],
        }
        for i in range(1, len(counts))
        if counts[i] != counts[i - 1]
    ]
    for move in moves:  # THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD: a count changes either by a transfer between the two bodies (one down, the other up by the same quanta, the total kept) or by the count's line laying the count anew from the record's form (the total not kept); only a transfer is a click between the bodies
        transfer = move["left"] + move["right"] == 0 and move["left"] != 0
        move["kind"] = "transfer" if transfer else "relay"
    transfers = [m for m in moves if m["kind"] == "transfer"]
    relays = [m for m in moves if m["kind"] == "relay"]
    edge = float(
        blind["edge_quanta_per_node"]
    )  # the fraction of Gamma as Cheshbon gives it; a count below it is dissolved
    first_move = transfers[0]["interval"] if transfers else None
    under_edge = next((i for i, c in enumerate(counts) if min(c) < edge), None)
    events: dict[str, int] = {}
    for line in lines:
        events[line.get("event", "?")] = events.get(line.get("event", "?"), 0) + 1
    face_clicks = sum(1 for g in simulation.layer.gathers if g["chosen"] and g["chosen"][0][0] == "face")
    dissolution = blind["dissolution_intervals"]  # None where the bodies part: no dissolution expected
    levels = {
        r["name"]: [int(line["level"]) for line in r["lines"]]
        for r in readings.output()
        if r["kind"] == "level"
    }
    report = {
        "world": world_path.name,
        "kind": "WORLD (d), THE CLICK JOINS AND PARTS: the counts, the moves and the records against the expectation",
        "verdict": "LAWFUL" if refusal is None else "REFUSED IN THE RUN",
        "refusal": refusal,
        "ticks_run": simulation.tick,
        "1_the_counts": {
            "label": "GAMEBOARD",
            "start": counts[0],
            "end": counts[-1],
            "every_10": [(i, c) for i, c in enumerate(counts) if i % 10 == 0],
            "edge": edge,
            "under_the_edge_at": under_edge,
            "expected_dissolution_intervals": dissolution,
            "verdict": (
                ("MATCH" if under_edge is None else "MISS")
                if dissolution is None
                else (
                    "MISS"
                    if under_edge is None
                    else ("MATCH" if dissolution[0] <= under_edge <= dissolution[1] else "MISS")
                )
            ),
        },
        "2_the_moves": {
            "label": "GAMEBOARD",
            "moves": moves[:40],
            "count_of_transfers": len(transfers),
            "quanta_transferred": sum(abs(m["left"]) for m in transfers),
            "count_of_relays": len(relays),
            "first_relay_interval": relays[0]["interval"] if relays else None,
            "first_move_interval": first_move,
            "expected_first_click_interval": blind["first_click_interval"],
            "verdict": "MATCH" if first_move == blind["first_click_interval"] else "MISS",
        },
        "3_the_records": {
            "label": "HOST",
            "alive_at_the_end": len(simulation.records),
            "expected": blind["records_at_the_end"],
            "verdict": "MATCH" if len(simulation.records) == blind["records_at_the_end"] else "MISS",
            "event_lines": events,
            "clicks_at_the_faces": face_clicks,
            "faces": "a click at an open face is no click and is not counted (Cheshbon 14:55, the Closer 15:02)",
        },
        "5_the_record": record_reading(counts, levels, blind.get("record")),
        "6_the_hierarchy": breathing_reading(counts, levels, blind),
        "4_the_levels": {
            "label": "GAMEBOARD",
            "readings": {
                r["name"]: [
                    (line["interval"], line.get("level", line.get("support", line.get("total"))))
                    for line in r["lines"]
                ][:12]
                for r in readings.output()
                if r["kind"] in ("level", "support", "total")
            },
        },
    }
    world_path.with_name(f"{world_path.stem}.clicks.json").write_text(
        json.dumps(report, indent=1) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    arguments = sys.argv[1:]
    as_table = "--table" in arguments
    for argument in (a for a in arguments if a != "--table"):
        report = read(Path(argument).resolve())
        if as_table:
            print(table(report))
            continue
        shown = dict(report)
        shown["1_the_counts"] = {k: v for k, v in report["1_the_counts"].items() if k != "every_10"}
        shown["2_the_moves"] = {**report["2_the_moves"], "moves": report["2_the_moves"]["moves"][:8]}
        print(json.dumps(shown, indent=1))


if __name__ == "__main__":
    main()
