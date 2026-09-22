"""The readings of the moving detector, a cart with a click (docs/designs/
moving_detector/DESIGN.md; `examples/events/moving_detector/`), from the
clock-stamped clicks alone, compared with the pins of `expectations.json`,
written before any run.

Usage: `PYTHONPATH=src python tools/moving_detector_readings.py <runs root>
[--register examples/events/moving_detector/expectations.json]
[--expectations <path>] [--capability]`. The root holds the runs
`tools/run_series.py` wrote (`<root>/<world>/run/`), told apart by the model
of their record (`beam-moving-detector-<name>-v1`). A record without the
key `clock_stamp` is refused: nothing here reads the tick.

Two kinds of line ([the register](../docs/EXPERIMENTS.md), "Two kinds of
readings"). DETECTOR, the cart's own record: at every click its own count
(`clock`, its self-creations), its Node and the ordinal the packet brought
(`record` mod 2^32, the emitter's count at the emission); from the lamp's
rows `k_AB` (the cart's counts apart over the lamp's ordinals apart, over
the window), the least step (the Node's change against the counts between
clicks, the pace over the window); from the returned pulses (the post's
number on them, the cart's own ordinal in `record`) the round trip (the
cart's counts apart between two returns over its ordinals apart between
the births they carry) and the radar velocity (`x_D = c (n_r - n_e) / 2`
Links, `t_D = (n_r + n_e) / 2` counts, `delta x_D / delta t_D` in Nodes per
count); and the post's own record (its `rerelease` lines: its `clock`, the
cart's ordinals in its rows) `k_BA`. GAMEBOARD, labelled and never pinned:
the tick of every line, the `step` lines' gaps (the counts between hops,
the drive's pattern), the final `age` of the cart against the intervals.
A reading outside its pin is printed with its numbers and never moved.
`--capability` prints the consecutive clicks themselves (the count, the
Node, the ordinal, the differences: the Outside step of record 803) and
says of each pin "read" or "not read" only, nothing inside or outside
(step 4 of the design, the owner's word of record 824). With `--register`
the run blocks (the source sha256, the digests, the readings) are written
under `runs` of the expectations file, the pins untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "moving_detector" / "expectations.json"
PREFIX = "beam-moving-detector-"
ORDINAL_MASK = (1 << 32) - 1


@dataclass
class Click:
    count: int
    node: int
    ordinal: int
    tick: int


@dataclass
class Reading:
    name: str
    folder: Path
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    fingerprint: str
    hypotheses: list[str]
    digests: dict[str, str]
    cart: int
    lamp: int
    post: int | None
    lamp_clicks: list[Click] = field(default_factory=list)
    returns: list[Click] = field(default_factory=list)
    post_lines: list[Click] = field(default_factory=list)
    step_ticks: list[int] = field(default_factory=list)
    final_age: int = 0


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    if not record.get("clock_stamp"):
        raise SystemExit(f"{folder}: the record carries no clock stamp; nothing here reads the tick")
    roles: dict[str, int] = {}
    for number, entry in record["numbers"].items():
        roles[str(entry["family"])] = int(number)
    cart, lamp, post = roles["cart"], roles["source"], roles.get("post")
    model = str(record["model"])
    reading = Reading(
        name=model[len(PREFIX) : -len("-v1")].replace("-", "_"),
        folder=folder,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=int(record["completed_ticks"]),
        elapsed=float(record["elapsed_seconds"]),
        fingerprint=str(record["source_sha256"]),
        hypotheses=list(record["hypotheses"]),
        digests={
            "state_sha256": digest(folder / "state.json"),
            "audit_sha256": hashlib.sha256(
                json.dumps(record.get("audit", [])).encode("utf-8")
            ).hexdigest(),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        cart=cart,
        lamp=lamp,
        post=post,
    )
    for entry in record["measured"]:
        if int(entry["number"]) == cart:
            reading.final_age = int(entry["age"])
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if '"clock"' not in text and '"step"' not in text:
                continue
            event = json.loads(text)
            kind = event["event"]
            if kind == "step":
                reading.step_ticks.append(int(event["tick"]))
            elif kind == "click" and event.get("measured") == cart and "record" in event:
                click = Click(
                    int(event["clock"]),
                    int(event["node"][0]),
                    int(event["record"]) & ORDINAL_MASK,
                    int(event["tick"]),
                )
                if int(event["number"]) == lamp:
                    reading.lamp_clicks.append(click)
                elif post is not None and int(event["number"]) == post:
                    if int(event["record"]) >> 32 != cart:
                        raise SystemExit(f"{folder}: a return not born at the cart: {text.strip()}")
                    reading.returns.append(click)
            elif kind == "rerelease" and post is not None and event.get("measured") == post:
                for row in event.get("rows", []):
                    identity = int(row[0])
                    if identity >> 32 == cart:
                        reading.post_lines.append(
                            Click(int(event["clock"]), 1, identity & ORDINAL_MASK, int(event["tick"]))
                        )
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        if path.parent.name == "resolved_view":
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if str(record.get("model", "")).startswith(PREFIX):
            found.append(read_run(path.parent))
    return found


def ratio_over(clicks: list[Click], from_count: int) -> tuple[Fraction | None, int]:
    """The counts apart over the ordinals apart from the first click at or
    after `from_count` to the last, and the window's length in counts."""
    window = [click for click in clicks if click.count >= from_count]
    if len(window) < 2 or window[-1].ordinal == window[0].ordinal:
        return None, 0
    first, last = window[0], window[-1]
    return Fraction(last.count - first.count, last.ordinal - first.ordinal), last.count - first.count


def radar_velocity(returns: list[Click], from_count: int, c: Fraction) -> tuple[Fraction | None, int]:
    """`delta x_D / delta t_D` over the window, `x_D = c (n_r - n_e) / 2`,
    `t_D = (n_r + n_e) / 2`, Nodes per count."""
    window = [click for click in returns if click.count >= from_count]
    if len(window) < 2:
        return None, 0
    first, last = window[0], window[-1]
    dx = c * ((last.count - last.ordinal) - (first.count - first.ordinal)) / 2
    dt = Fraction((last.count + last.ordinal) - (first.count + first.ordinal), 2)
    return (dx / dt if dt else None), last.count - first.count


def compare(value: Fraction | None, pin: Fraction, window: int, capability: bool) -> str:
    if value is None:
        return "NOT READ"
    if capability:
        return "read"
    tolerance = Fraction(2, window) if window else Fraction(0)
    return "inside" if abs(value - pin) <= tolerance else "OUTSIDE"


def lines(
    reading: Reading, pin: dict[str, object], c: Fraction, capability: bool
) -> tuple[list[str], int, int, int, dict[str, object]]:
    out: list[str] = []
    failed = inside = outside = 0
    block: dict[str, object] = {}

    def tally(verdict: str) -> None:
        nonlocal inside, outside
        if verdict == "inside":
            inside += 1
        elif verdict == "OUTSIDE":
            outside += 1

    out.append(
        f"{reading.name}: {reading.ticks} intervals, {reading.elapsed:.2f} s, {reading.hypotheses}"
    )
    if not reading.completed or not reading.balanced:
        failed += 1
        out.append("  RECORD CHECK FAILED: not completed or the books unbalanced")
    windows = dict(pin["windows"])  # type: ignore[arg-type]
    one_way = int(dict(windows["one_way"])["from_count"])  # type: ignore[arg-type]
    round_trip_from = int(dict(windows["round_trip_and_radar"])["from_count"])  # type: ignore[arg-type]
    if capability:
        out.append(
            "  DETECTOR the cart's consecutive clicks of the lamp's rows (its count, its Node, the ordinal read; then the differences, the Outside step of record 803):"
        )
        previous = None
        shown = 0
        for click in reading.lamp_clicks:
            if previous is None:
                out.append(
                    f"    count {click.count} at Node x = {click.node}, the ordinal {click.ordinal}"
                )
            else:
                out.append(
                    f"    count {click.count} at Node x = {click.node}, the ordinal {click.ordinal}: "
                    f"+{click.count - previous.count} counts, {click.node - previous.node:+d} Node, "
                    f"+{click.ordinal - previous.ordinal} ordinals"
                )
            previous = click
            shown += 1
            if shown >= 40:
                out.append(f"    ... {len(reading.lamp_clicks) - shown} more clicks")
                break
    # k_AB
    k_ab, window = ratio_over(reading.lamp_clicks, one_way)
    pin_k_ab = Fraction(str(dict(pin["k_AB"])["fraction"]))  # type: ignore[arg-type]
    verdict = compare(k_ab, pin_k_ab, window, capability)
    tally(verdict)
    out.append(
        f"  DETECTOR k_AB = the cart's counts apart over the lamp's ordinals apart, from its count {one_way}: "
        f"{float(k_ab) if k_ab is not None else 'none'} over {window} counts ({len(reading.lamp_clicks)} clicks); "
        f"the pin {pin_k_ab} = {float(pin_k_ab):.4f}: {verdict}"
    )
    block["k_AB"] = {
        "value": None if k_ab is None else float(k_ab),
        "window": window,
        "verdict": verdict,
    }
    # the least step
    least = dict(pin["least_step"])  # type: ignore[arg-type]
    allowed = list(least["consecutive_clicks_of_the_lamp_rows"])  # type: ignore[arg-type]
    changes = Counter()
    per_count = True
    for before, after in zip(reading.lamp_clicks, reading.lamp_clicks[1:], strict=False):
        delta_node = after.node - before.node
        changes[delta_node] += 1
        if abs(delta_node) > after.count - before.count:
            per_count = False
    in_set = all(change in allowed for change in changes)
    verdict_step = (
        "NOT READ"
        if not changes
        else ("read" if capability else ("inside" if per_count and in_set else "OUTSIDE"))
    )
    tally(verdict_step)
    out.append(
        f"  DETECTOR the least step: the Node's change between consecutive clicks of the lamp's rows {dict(sorted(changes.items()))}, "
        f"at most one per count {'holds' if per_count else 'FAILS'}; the pin: changes in {allowed}, abs(delta node) <= delta count: {verdict_step}"
    )
    pace_value = None
    pace_window = [click for click in reading.lamp_clicks if click.count >= one_way]
    if len(pace_window) >= 2 and pace_window[-1].count > pace_window[0].count:
        pace_value = Fraction(
            pace_window[-1].node - pace_window[0].node, pace_window[-1].count - pace_window[0].count
        )
    pin_pace = Fraction(str(dict(least["pace_over_the_window"])["fraction"]))  # type: ignore[arg-type]
    verdict_pace = compare(
        pace_value,
        pin_pace,
        pace_window[-1].count - pace_window[0].count if len(pace_window) >= 2 else 0,
        capability,
    )
    tally(verdict_pace)
    out.append(
        f"  DETECTOR the pace over the window, Nodes per count: {float(pace_value) if pace_value is not None else 'none'}; "
        f"the pin {pin_pace} = {float(pin_pace):.4f}: {verdict_pace}"
    )
    block["least_step"] = {
        "changes": {str(k): v for k, v in sorted(changes.items())},
        "per_count": per_count,
        "verdict": verdict_step,
        "pace": None if pace_value is None else float(pace_value),
        "pace_verdict": verdict_pace,
    }
    if reading.post is not None and "k_BA" in pin:
        k_ba, window_ba = ratio_over(reading.post_lines, one_way)
        pin_k_ba = Fraction(str(dict(pin["k_BA"])["fraction"]))  # type: ignore[arg-type]
        verdict = compare(k_ba, pin_k_ba, window_ba, capability)
        tally(verdict)
        out.append(
            f"  DETECTOR k_BA = the post's counts apart over the cart's ordinals apart, from its count {one_way}: "
            f"{float(k_ba) if k_ba is not None else 'none'} over {window_ba} counts ({len(reading.post_lines)} rows); "
            f"the pin {pin_k_ba} = {float(pin_k_ba):.4f}: {verdict}"
        )
        block["k_BA"] = {
            "value": None if k_ba is None else float(k_ba),
            "window": window_ba,
            "verdict": verdict,
        }
        ratio = None if k_ab is None or k_ba is None else k_ba / k_ab
        pin_ratio = Fraction(str(dict(pin["ratio_k_BA_over_k_AB"])["fraction"]))  # type: ignore[arg-type]
        verdict = compare(ratio, pin_ratio, min(window, window_ba), capability)
        tally(verdict)
        out.append(
            f"  DETECTOR the ratio k_BA / k_AB (two detectors' counts, carries r_R / r_D^2): "
            f"{float(ratio) if ratio is not None else 'none'}; the law's pin {pin_ratio} = {float(pin_ratio):.4f} "
            f"(the comparison, Lorentz's one symmetric factor: 1): {verdict}"
        )
        block["ratio_k_BA_over_k_AB"] = {
            "value": None if ratio is None else float(ratio),
            "verdict": verdict,
        }
        round_trip, window_rt = ratio_over(reading.returns, round_trip_from)
        pin_rt = Fraction(str(dict(pin["round_trip"])["fraction"]))  # type: ignore[arg-type]
        verdict = compare(round_trip, pin_rt, window_rt, capability)
        tally(verdict)
        out.append(
            f"  DETECTOR the round trip = the cart's counts apart between two returns over its ordinals apart, from its count {round_trip_from}: "
            f"{float(round_trip) if round_trip is not None else 'none'} over {window_rt} counts ({len(reading.returns)} returns); "
            f"the pin {pin_rt} = {float(pin_rt):.4f} (r cancels): {verdict}"
        )
        block["round_trip"] = {
            "value": None if round_trip is None else float(round_trip),
            "window": window_rt,
            "verdict": verdict,
        }
        radar, window_radar = radar_velocity(reading.returns, round_trip_from, c)
        pin_radar = Fraction(str(dict(pin["radar_velocity"])["fraction"]))  # type: ignore[arg-type]
        verdict = compare(radar, pin_radar, window_radar, capability)
        tally(verdict)
        out.append(
            f"  DETECTOR the radar velocity of the post, delta x_D / delta t_D in Nodes per count: "
            f"{float(radar) if radar is not None else 'none'} over {window_radar} counts; the pin {pin_radar} = {float(pin_radar):.4f}: {verdict}"
        )
        block["radar_velocity"] = {
            "value": None if radar is None else float(radar),
            "window": window_radar,
            "verdict": verdict,
        }
    gaps = Counter(b - a for a, b in zip(reading.step_ticks, reading.step_ticks[1:], strict=False))
    out.append(
        f"  GAMEBOARD the step lines: {len(reading.step_ticks)} hops, the intervals between hops {dict(sorted(gaps.items()))} "
        f"(the drive's pattern; the design's closed form {list(dict(least['counts_between_hops'])['values'])}); "  # type: ignore[arg-type]
        f"the cart's final age {reading.final_age} against {reading.ticks} intervals; every line's tick, read by nothing above"
    )
    block["gameboard"] = {
        "hops": len(reading.step_ticks),
        "gaps": {str(k): v for k, v in sorted(gaps.items())},
        "final_age": reading.final_age,
    }
    return out, failed, inside, outside, block


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="The runs' root (tools/run_series.py --out)")
    parser.add_argument("--register", type=Path, help="Write the run blocks into this expectations file")
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    parser.add_argument(
        "--capability", action="store_true", help="print the consecutive clicks; read / not read only"
    )
    args = parser.parse_args()
    expected = json.loads(args.expectations.read_text(encoding="utf-8"))
    c = Fraction(str(expected["c"]["fraction"]))
    runs = find_runs(args.root)
    if not runs:
        print(f"no moving-detector runs under {args.root}", file=sys.stderr)
        return 2
    failed = inside = outside = 0
    blocks: dict[str, object] = {}
    for reading in runs:
        pin = expected["worlds"].get(reading.name)
        if pin is None:
            print(f"{reading.name}: no pin in {args.expectations}", file=sys.stderr)
            return 2
        out, f, i, o, block = lines(reading, pin, c, args.capability)
        failed, inside, outside = failed + f, inside + i, outside + o
        print("\n".join(out))
        blocks[reading.name] = {
            "source_sha256": reading.fingerprint,
            "completed_ticks": reading.ticks,
            "elapsed_seconds": round(reading.elapsed, 3),
            "hypotheses": reading.hypotheses,
            **reading.digests,
            "clicks_of_the_lamp_rows": len(reading.lamp_clicks),
            "returns": len(reading.returns),
            "readings": block,
            "mode": "capability, read / not read only" if args.capability else "the pins compared",
        }
    if args.capability:
        print(
            f"{failed} record checks failed; the pins compared as read / not read only, nothing inside or outside"
        )
    else:
        print(
            f"{failed} record checks failed, {inside} readings inside, {outside} outside, nothing moved"
        )
    if args.register:
        document = json.loads(args.register.read_text(encoding="utf-8"))
        document.setdefault("runs", {}).update(blocks)
        args.register.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(f"registered {len(blocks)} runs in {args.register}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
