"""The readings of RUNS.md (step 2 of the new rows, the New Rows Scout,
2026-09-23), read from the runner's records under a root that
`tools/run_series.py` wrote (`<root>/<world>/run/`) and compared with the
pins of `new_rows_pins.json`, written before any run and untouched here.

Usage: `PYTHONPATH=src python docs/designs/new_rows/new_rows_readings.py <runs root>`.

Every printed number is one of the kinds of PINS.md. DETECTOR: a click
line (a face's or a measured event's), a gather line's chosen cell (the
click's record of the ladder's one choice per record), a stamped count
(`clock`). GAMEBOARD: the tick of a line, a `home` line (a row of the
event's own number taken back, ENGINE.md "what comes home"), the books.
CONVERSION: a pass fraction or a ratio formed from readings. COMPUTATION:
the pins and the closed forms. The record checks (completed, the books
balanced at every tick) are printed and never repaired; a reading outside
its pin is printed with its numbers and never moved. The readings are
written to `new_rows_readings.json` beside the pins with the source
fingerprint and the digests of every run.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.trimmed_record import refuse_trimmed_record  # noqa: E402

HERE = Path(__file__).resolve().parent
PINS = HERE / "new_rows_pins.json"
OUT = HERE / "new_rows_readings.json"
ORDINAL_MASK = (1 << 32) - 1
MALUS_RECORDS = 256


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path) -> dict[str, object]:
    refuse_trimmed_record(folder)
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    events = [
        json.loads(text)
        for text in (folder / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if text.strip()
    ]
    return {
        "name": folder.parent.name,
        "model": str(record["model"]),
        "status": str(record["status"]),
        "error": record.get("error"),
        "completed_ticks": int(record["completed_ticks"]),
        "elapsed_seconds": float(record["elapsed_seconds"]),
        "balanced": bool(record["conserved_at_every_completed_tick"]),
        "source_sha256": str(record["source_sha256"]),
        "clock_stamp": bool(record.get("clock_stamp")),
        "age_bound": record.get("age_bound"),
        "hypotheses": list(record["hypotheses"]),
        "digests": {
            "state_sha256": digest(folder / "state.json"),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        "events": events,
    }


def malus_readings(
    run: dict[str, object], pin: dict[str, object]
) -> tuple[list[str], dict[str, object]]:
    """R3: the cells 0+ and 0- over the records 1 to 256 from the gather
    lines (the click's record of the one cell the ladder chose per record;
    `chosen` names the read's label at `first` and the channel at
    `second`), the u coverage, the falsifiers, the verdict against the
    integer pin, met exactly or not at all."""
    events = run["events"]  # type: ignore[index]
    gathers = [
        e
        for e in events
        if e["event"] == "gather" and 1 <= (int(e["record"]) & ORDINAL_MASK) <= MALUS_RECORDS
    ]
    cells: Counter[str] = Counter()
    labels_read: Counter[str] = Counter()
    residues: set[int] = set()
    for g in gathers:
        chosen = {name: (label, cell) for name, label, cell in g["chosen"]}
        label, _ = chosen["first"]
        _, sign = chosen["second"]
        cells[f"{label}{sign}"] += 1
        labels_read[str(label)] += 1
        residues.add(int(g["u"]))
    all_gathers = sum(1 for e in events if e["event"] == "gather")
    clicks_second = sum(1 for e in events if e["event"] == "click" and e.get("detector") == "second")
    expected = {"0+": int(pin["counts"]["0+"]), "0-": int(pin["counts"]["0-"])}  # type: ignore[index]
    read = {"0+": cells.get("0+", 0), "0-": cells.get("0-", 0)}
    other = {k: v for k, v in cells.items() if k not in expected}
    verdict = "PASS" if read == expected and not other and len(gathers) == MALUS_RECORDS else "FAIL"
    fraction = read["0+"] / MALUS_RECORDS
    lines = [
        f"  DETECTOR the cells over the records 1 to {MALUS_RECORDS} (the gather lines' chosen cell, one per record): "
        f"0+ {read['0+']}, 0- {read['0-']}{', other ' + str(other) if other else ''}; "
        f"the pin 0+ {expected['0+']}, 0- {expected['0-']} (met exactly or not at all): {verdict}",
        f"  CONVERSION the pass fraction 0+ / {MALUS_RECORDS} = {fraction:.5f} against cos^2 = {float(pin['comparison']['cos2']):.5f} "  # type: ignore[index]
        f"(the departure {fraction - float(pin['comparison']['cos2']):+.5f}; the pin's {float(pin['departure']['value']):+.5f})",  # type: ignore[index]
        f"  DETECTOR the falsifiers: a cell on label 1: {'none' if labels_read.get('1', 0) == 0 else labels_read['1']}; "
        f"the wheel's coverage {len(residues)} of 256 residues over the records 1 to 256; "
        f"{len(gathers)} of {MALUS_RECORDS} records gathered ({all_gathers} gathered in all, {clicks_second} click lines at `second`)",
        f"  GAMEBOARD the record: {run['status']}, {run['completed_ticks']} intervals, the books balanced at every tick: {run['balanced']}; "
        f"HOST {float(run['elapsed_seconds']):.2f} s",  # type: ignore[arg-type]
    ]
    block = {
        "cells": dict(cells),
        "pin": expected,
        "verdict": verdict,
        "pass_fraction": fraction,
        "cos2": float(pin["comparison"]["cos2"]),  # type: ignore[index]
        "labels_read": dict(labels_read),
        "residues_covered": len(residues),
        "records_gathered": len(gathers),
        "all_gathered": all_gathers,
        "clicks_at_second": clicks_second,
    }
    return lines, block


def sagnac_readings(
    run: dict[str, object], pin: dict[str, object]
) -> tuple[list[str], dict[str, object]]:
    """R2: what the record holds against the chain of PINS.md section 2:
    the cart's stamped click lines of its own family (step 5), the `home`
    lines (a row of the cart's own number taken back, not a click), the
    face clicks of the cart's rows (where the records ended), the first of
    them with its Node and tick, and the ratio, read if the returns are
    stamped and NOT READ otherwise. Nothing here moves the pin."""
    events = run["events"]  # type: ignore[index]
    births = [e for e in events if e["event"] == "birth"]
    homes = Counter(str(e["family"]) for e in events if e["event"] == "home")
    cart_clicks = [
        e for e in events if e["event"] == "click" and e.get("measured") == 1 and "record" in e
    ]
    stamped = [e for e in cart_clicks if "clock" in e]
    face_clicks = [
        e
        for e in events
        if e["event"] == "click" and e.get("measured") is None and e.get("family") == "cart"
    ]
    by_face: Counter[str] = Counter(str(e["detector"]) for e in face_clicks)
    by_label: Counter[str] = Counter(str(e["momentum"]) for e in face_clicks)
    first_face = min(face_clicks, key=lambda e: int(e["tick"]), default=None)
    gathers = [e for e in events if e["event"] == "gather"]
    steps = [e for e in events if e["event"] == "step"]
    ratio_read = None
    if stamped:
        # Pair the two returns of one ordinal at the cart, by the record's ordinal.
        by_ordinal: dict[int, list[int]] = {}
        for e in stamped:
            by_ordinal.setdefault(int(e["record"]) & ORDINAL_MASK, []).append(int(e["clock"]))
        births_count = {int(e["record"]) & ORDINAL_MASK: e.get("clock") for e in births}
        ratios = []
        for ordinal, counts in sorted(by_ordinal.items()):
            n0 = births_count.get(ordinal)
            if (
                len(counts) == 2
                and n0 is not None
                and int(counts[0]) >= int(pin["ratio"].get("from", 0))
            ):  # type: ignore[union-attr]
                a, b = sorted(counts)
                ratios.append((b - a) / (a + b - 2 * int(n0)))
        ratio_read = sum(ratios) / len(ratios) if ratios else None
    lines = [
        f"  GAMEBOARD the record: {run['status']}"
        + (f" ({run['error']})" if run.get("error") else "")
        + f", {run['completed_ticks']} intervals, the books balanced at every tick: {run['balanced']}, age_bound {run['age_bound']}; "
        f"{len(births)} birth lines (two rows each), {len(steps)} step lines of the cart; HOST {float(run['elapsed_seconds']):.2f} s",  # type: ignore[arg-type]
        f"  DETECTOR the cart's click lines of its own family (the chain's step 5): {len(cart_clicks)}, stamped {len(stamped)}",
        f"  GAMEBOARD the `home` lines (a row of the event's own number taken back and created again on its directions, "
        f"ENGINE.md 'what comes home'; no clock, no record on the line): {dict(homes)}",
        f"  DETECTOR the face clicks of the cart's rows (the records ending at the open y and z faces): {dict(by_face)}; "
        f"their momentum labels {dict(by_label)}; {len(gathers)} records gathered at faces",
    ]
    if first_face is not None:
        births_at = {int(e["record"]): (int(e["tick"]), int(e["node"][0])) for e in births}
        ages = [int(e["tick"]) - births_at[int(e["record"])][0] for e in face_clicks]
        displacements = [(int(e["node"][0]) - births_at[int(e["record"])][1]) % 240 for e in face_clicks]
        off_axis = Counter((int(e["node"][1]), int(e["node"][2])) for e in face_clicks)
        lines.append(
            f"  DETECTOR the first face click: tick {first_face['tick']} at the Node {first_face['node']} through {first_face['detector']}, "
            f"the label {first_face['momentum']}; the escaping rows' ages at the escape from {min(ages)} to {max(ages)} intervals "
            f"and their displacements from the birth Node along x over {len(set(displacements))} distinct values of 240 "
            f"(COMPUTATION: no one age and no one Node, so not the loop's antipode); the escapes' (y, z) {dict(off_axis)}, one Link off the axis"
        )
    if ratio_read is None:
        lines.append(
            f"  CONVERSION the ratio (n_+ - n_-) / (n_+ + n_- - 2 n_0): NOT READ (no stamped return of the cart's own rows exists in the "
            f"record); the pin {pin['ratio']['pin']['exact']} = {float(pin['ratio']['pin']['value']):.5f} stands unread, not moved"  # type: ignore[index]
        )
    else:
        lines.append(
            f"  CONVERSION the ratio (n_+ - n_-) / (n_+ + n_- - 2 n_0): {ratio_read:.5f} against the pin "
            f"{float(pin['ratio']['pin']['value']):.5f} (the band {float(pin['band']['on_the_ratio']):.4f})"  # type: ignore[index]
        )
    block = {
        "status": run["status"],
        "error": run.get("error"),
        "completed_ticks": run["completed_ticks"],
        "balanced": run["balanced"],
        "age_bound": run["age_bound"],
        "births": len(births),
        "cart_steps": len(steps),
        "cart_own_clicks": len(cart_clicks),
        "stamped_returns": len(stamped),
        "home_lines": dict(homes),
        "face_clicks": dict(by_face),
        "face_labels": dict(by_label),
        "records_gathered_at_faces": len(gathers),
        "first_face_click": None
        if first_face is None
        else {"tick": first_face["tick"], "node": first_face["node"], "face": first_face["detector"]},
        "escape_ages": None if first_face is None else [min(ages), max(ages)],
        "escape_displacements_distinct": None if first_face is None else len(set(displacements)),
        "ratio": ratio_read,
        "ratio_pin": pin["ratio"]["pin"],  # type: ignore[index]
        "verdict": "NOT READ" if ratio_read is None else "READ",
    }
    return lines, block


def main(root: Path) -> None:
    pins = json.loads(PINS.read_text(encoding="utf-8"))
    out: dict[str, object] = {"format": "new-rows-readings-v1", "runs": {}}
    lines = ["THE READINGS OF RUNS.md, BY KIND, AGAINST THE PINS AS WRITTEN (no pin moved)", ""]
    for folder in sorted(root.iterdir()):
        run_folder = folder / "run"
        if not (run_folder / "run.json").exists():
            continue
        run = read_run(run_folder)
        name = str(run["name"])
        lines.append(f"{name} ({run['model']}; the source {str(run['source_sha256'])[:16]}):")
        if name.startswith("malus_"):
            text, block = malus_readings(run, pins["R3_malus"][name])
        elif name.startswith("sagnac_"):
            text, block = sagnac_readings(run, pins["R2_sagnac"][name])
        else:
            continue
        lines.extend(text)
        lines.append("")
        block["source_sha256"] = run["source_sha256"]
        block["digests"] = run["digests"]
        block["hypotheses"] = run["hypotheses"]
        out["runs"][name] = block  # type: ignore[index]
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    (HERE / "new_rows_readings.out").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
