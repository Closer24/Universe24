"""The reading of the phase of a one-qubit world of (k) from its two exits' clicks (ALGEBRA.md #the-rows-against-nature (l) and (k)): the runner's output beside the world (`<world>.output.json`, tools/run_inputs.py) carries the verdict and every click with its detector; this tool counts the clicks per exit, the share at the cross exit with the draw's band, and the phase the row's form gives for that share, cos^2 (Delta / 2) = share / (4 s (1 - s)) with s the splitter's share of the expectation file, and prints the table the experiments of record print, the algebra (blind, the expectation file's numbers under Cheshbon's name) against the engine (the output's) and the difference, one row per number; a refused run prints its refusal with the interval and the gate's name in place of the engine's numbers. The books it can read from the output alone: the clicks per detector and the records alive at the end (the labels left on the GameBoard); the quanta given and the labels ended at a face are the event lines' (examples/events/experiments/bell_books.py). Nothing here is compared with nature, and no rule is replayed: the cosine lives in the expectation's form alone. Run from the repository root: python examples/events/experiments/quantum_computer/exits.py <world.json> <world.output.json>; the table is printed and the reading written beside the output as <name>.exits.json."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

EXITS = ("cross_exit", "straight_exit")
SPLITTER_SHARE = 0.5  # s of the row's form, the expectation's: one half at Cheshbon's count by bisection


def clicks_per_exit(output: dict[str, Any]) -> dict[str, int]:
    """The clicks per detector from the output's click lines, the measurement."""
    counts = dict.fromkeys(EXITS, 0)
    for click in output.get("clicks", []):
        name = click.get("detector")
        if name in counts:
            counts[name] += 1
    return counts


def phase_of(share: float, splitter_share: float = SPLITTER_SHARE) -> float | None:
    """Delta from the cross exit's share by the row's form, 4 s (1 - s) cos^2 (Delta / 2); None where the share exceeds the form's top."""
    top = 4 * splitter_share * (1 - splitter_share)
    if top <= 0 or share > top:
        return None
    return 2 * math.acos(math.sqrt(share / top))


def number(value: float | int | None, places: int = 4) -> str:
    """A number for the table, or a dash where there is none."""
    if value is None:
        return "-"
    return str(value) if isinstance(value, int) else f"{value:.{places}f}"


def difference(blind: float | int | None, engine: float | int | None) -> str:
    """The engine's number less the algebra's, or a dash where either is missing."""
    if blind is None or engine is None:
        return "-"
    return number(engine - blind)


def table(reading: dict[str, Any]) -> str:
    """The table of the experiments of record: one row per number, the algebra (blind), the engine and the difference; a refused run carries its refusal in the engine's column."""
    blind, engine = reading["algebra"], reading["engine"]
    rows: list[tuple[str, str, str, str]] = []
    if reading["verdict"] != "LAWFUL":
        rows.append(("verdict", "LAWFUL", f"{reading['verdict']}: {reading['refusal']}", "-"))
    for name in ("cross_share", "straight_share", "phase_radians"):
        rows.append(
            (
                name.replace("_", " "),
                number(blind.get(name)),
                number(engine.get(name)),
                difference(blind.get(name), engine.get(name)),
            )
        )
    rows.append(
        (
            "cross share band (algebra: Cheshbon's; engine: the draw's)",
            number(blind.get("cross_share_band")),
            number(engine.get("cross_share_band")),
            "-",
        )
    )
    for name in EXITS:
        rows.append((f"clicks at the {name.replace('_', ' ')}", "-", number(engine.get(name)), "-"))
    rows.append(("records alive at the end (GAMEBOARD)", "-", number(engine.get("records_alive")), "-"))
    lines = ["| row | the algebra (blind) | the engine | the difference |", "| --- | --- | --- | --- |"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    return "\n".join(lines)


def report(world: dict[str, Any], output: dict[str, Any], expectation: dict[str, Any]) -> dict[str, Any]:
    """The run's numbers beside the expectation's forms: the clicks per exit (DETECTOR), the cross share with the draw's band, the phase by the form, the records alive at the end (GAMEBOARD), and the giver's stock as the quanta the run could give."""
    blind_section = expectation.get("blind_expectation", {})
    shares = blind_section.get("shares", {})
    band = blind_section.get("cross_share_band")
    algebra = {
        "cross_share": shares.get("cross_exit"),
        "straight_share": shares.get("straight_exit"),
        "phase_radians": blind_section.get("gate_phase_radians"),
        "cross_share_band": None if band is None else (band[1] - band[0]) / 2,
    }
    counts = clicks_per_exit(output)
    total = sum(counts.values())
    share = counts["cross_exit"] / total if total else None
    draw = math.sqrt(share * (1 - share) / total) if total and share is not None else None
    engine = {
        **counts,
        "cross_share": share,
        "straight_share": None if share is None else 1 - share,
        "phase_radians": None if share is None else phase_of(share),
        "cross_share_band": draw,
        "records_alive": output.get("records_alive"),
    }
    giver = world["measured"][0]
    return {
        "verdict": output.get("verdict"),
        "refusal": output.get("reason"),
        "algebra": algebra,
        "engine": engine,
        "DETECTOR": {"clicks_per_exit": counts, "clicks": total},
        "GAMEBOARD": {
            "records_alive_at_the_end": output.get("records_alive"),
            "quanta_the_giver_could_give": giver.get("stocks", {}).get("charge"),
        },
        "row": "the clicks per exit are the measurement; the engine's band is the draw's, sqrt(p (1 - p) / n); the phase is the row's form read backward and no reading of the GameBoard; the quanta given and the labels ended at a face are read from the event lines, not from this output",
    }


def main(argv: list[str]) -> None:
    world_path, output_path = Path(argv[1]), Path(argv[2])
    world = json.loads(world_path.read_text(encoding="utf-8"))
    output = json.loads(output_path.read_text(encoding="utf-8"))
    expectation = json.loads(world_path.with_suffix(".expectation.json").read_text(encoding="utf-8"))
    result = report(world, output, expectation)
    print(f"{world_path.stem}: {result['verdict']}")
    print(table(result))
    output_path.with_suffix(".exits.json").write_text(
        json.dumps(result, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main(sys.argv)
