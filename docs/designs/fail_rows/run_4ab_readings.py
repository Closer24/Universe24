"""The readings of RUN_4AB.md (rows 4a and 4b turned by the algebra; the FAIL
Runner A, 2026-09-23), read from the runner's records and compared with the
pins of `run_4ab_pins.json`, written before any run and untouched here.

Usage: `PYTHONPATH=src python docs/designs/fail_rows/run_4ab_readings.py
<runs root>`. The root holds the runs `tools/run_series.py` wrote
(`<root>/<world>/run/`), told apart by the model of their record
(`beam-fail-rows-j4-muon-<p>-<law|key>-v1`, `beam-fail-rows-cart-k<k>-<law|key>-v1`,
and series S's `rays-hubble-stars-record-covariant-none-space-v1` for the
coasting world, whose z is read by `tools/covariant_readings.py` beside
this tool). A record without the key `clock_stamp` is refused: nothing
here reads the tick as a reading.

Every printed number is one of the kinds of RUN_4AB.md. DETECTOR: a
measured event's own count at a click (`clock`), the ordinal a row
carries (`record` mod 2^32), the row's own `age` on the click line (read
whole by the measured event), a click's Node. COMPUTATION or CONVERSION:
the ratios formed from them (the counts apart over the ordinals apart
from the window's first count, `ratio_over`, as
`tools/moving_detector_readings.py` forms them; the decay's count read
back from the click as `clock` less the row's `age`; that over 64).
GAMEBOARD, labelled and never a verdict: the tick of every line, the
`become` line, the `step` lines' gaps, the `energy` lines and the owed
intervals, the final `age` against the intervals. The record checks
(completed, the books balanced at every tick) fail the tool; a reading
outside its pin is printed with its numbers and never moved. The readings
are written to `run_4ab_readings.json` beside the pins, with the source
fingerprint and the digests of every run.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe.trimmed_record import refuse_trimmed_record  # noqa: E402

HERE = Path(__file__).resolve().parent
PINS = HERE / "run_4ab_pins.json"
OUT = HERE / "run_4ab_readings.json"
J4_PREFIX = "beam-fail-rows-j4-muon-"
CART_PREFIX = "beam-fail-rows-cart-"
STARS_MODEL = "rays-hubble-stars-record-covariant-none-space-v1"
ORDINAL_MASK = (1 << 32) - 1
AT = 64


@dataclass
class Click:
    count: int
    node: int
    ordinal: int
    tick: int


@dataclass
class Run:
    name: str
    model: str
    folder: Path
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    fingerprint: str
    hypotheses: list[str]
    roles: dict[str, int]
    final_age: dict[int, int]
    digests: dict[str, str]
    events: list[dict[str, object]] = field(default_factory=list)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path) -> Run:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    if not record.get("clock_stamp"):
        raise SystemExit(f"{folder}: the record carries no clock stamp; nothing here reads the tick")
    refuse_trimmed_record(folder)
    roles = {str(entry["family"]): int(number) for number, entry in record["numbers"].items()}
    events = [
        json.loads(text)
        for text in (folder / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if text.strip()
    ]
    return Run(
        name=folder.parent.name,
        model=str(record["model"]),
        folder=folder,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=int(record["completed_ticks"]),
        elapsed=float(record["elapsed_seconds"]),
        fingerprint=str(record["source_sha256"]),
        hypotheses=list(record["hypotheses"]),
        roles=roles,
        final_age={int(m["number"]): int(m["age"]) for m in record["measured"]},
        digests={
            "state_sha256": digest(folder / "state.json"),
            "audit_sha256": hashlib.sha256(
                json.dumps(record.get("audit", [])).encode("utf-8")
            ).hexdigest(),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        events=events,
    )


def ratio_over(clicks: list[Click], from_count: int) -> tuple[Fraction | None, int]:
    """The counts apart over the ordinals apart from the first click at or
    after `from_count` to the last, and the window's length in counts."""
    window = [click for click in clicks if click.count >= from_count]
    if len(window) < 2 or window[-1].ordinal == window[0].ordinal:
        return None, 0
    first, last = window[0], window[-1]
    return Fraction(last.count - first.count, last.ordinal - first.ordinal), last.count - first.count


def verdict_band(value: float | None, pin: float, band: float) -> str:
    if value is None:
        return "NOT READ"
    return "PASS" if abs(value - pin) <= band else "FAIL"


def gameboard_lines(run: Run) -> tuple[list[str], dict[str, object]]:
    steps = [int(e["tick"]) for e in run.events if e["event"] == "step"]
    gaps = Counter(b - a for a, b in zip(steps, steps[1:], strict=False))
    energy = sum(1 for e in run.events if e["event"] == "energy")
    owed = max((int(e.get("owed", 0)) for e in run.events if e["event"] == "energy"), default=0)
    out = [
        f"  GAMEBOARD: {len(steps)} step lines, the gaps between hops {dict(sorted(gaps.items()))}; "
        f"{energy} energy lines, the most intervals owed to proper time on one line {owed}; "
        f"the final ages {run.final_age} against {run.ticks} intervals; the tick of every line read by nothing above"
    ]
    return out, {
        "steps": len(steps),
        "gaps": {str(k): v for k, v in sorted(gaps.items())},
        "energy_lines": energy,
        "owed": owed,
    }


def j4_lines(run: Run, pin: dict[str, object]) -> tuple[list[str], dict[str, object], int, int]:
    muon, detector = run.roles["mu"], run.roles["detector"]
    become = [e for e in run.events if e["event"] == "become" and e.get("measured") == muon]
    clicks = [
        e
        for e in run.events
        if e["event"] == "click" and e.get("measured") == detector and e.get("family") == "beta"
    ]
    out: list[str] = []
    block: dict[str, object] = {}
    passed = failed = 0
    pin_click = dict(pin["click"])  # type: ignore[arg-type]
    pin_decay = dict(pin["decay"])  # type: ignore[arg-type]
    pin_ratio = dict(pin["ratio"])  # type: ignore[arg-type]
    for line in become:
        out.append(
            f"  GAMEBOARD the become line: tick {line['tick']} at x = {line['node'][0]}, the muon's own count {line.get('clock')} "
            f"(the pin's integer {pin_decay['tick']} at x = {pin_decay['node'][0]}; printed, not a verdict)"
        )
    block["become"] = [
        {"tick": line["tick"], "node": line["node"], "clock": line.get("clock")} for line in become
    ]
    if not clicks:
        out.append("  DETECTOR the beta click at the detector body: NOT READ")
        block["click"] = None
        return out, block, passed, failed + 1
    click = clicks[0]
    count, age = int(click["clock"]), int(click["age"]) if "age" in click else int(click["reading"])
    expected, tolerance = int(pin_click["count"]), int(pin_click["tolerance"])
    verdict = "PASS" if abs(count - expected) <= tolerance else "FAIL"
    passed += verdict == "PASS"
    failed += verdict == "FAIL"
    out.append(
        f"  DETECTOR the beta click at the detector body (x = {click['node'][0]}): the detector's own count {count} "
        f"(the pin {expected} +- {tolerance}): {verdict}; the row's own age on the line {age} (the flight's, "
        f"the pin's a(steps) {pin_click['flight_age']}); {len(clicks)} beta click(s)"
    )
    decay_from_click = count - age
    ratio = decay_from_click / AT
    out.append(
        f"  CONVERSION the decay's count read back from the click, clock less the row's age: {decay_from_click}; "
        f"the ratio over 64: {ratio:.4f} (the pin's form {float(pin_ratio['value']):.4f}; gamma {float(pin_ratio['gamma']):.4f} the thing compared with)"
    )
    block["click"] = {
        "count": count,
        "tick": click["tick"],
        "node": click["node"],
        "row_age": age,
        "pin": expected,
        "tolerance": tolerance,
        "verdict": verdict,
        "decay_from_click": decay_from_click,
        "ratio": ratio,
    }
    return out, block, passed, failed


def cart_lines(run: Run, pin: dict[str, object]) -> tuple[list[str], dict[str, object], int, int]:
    cart, lamp, post = run.roles["cart"], run.roles["source"], run.roles["post"]
    lamp_clicks: list[Click] = []
    returns: list[Click] = []
    post_lines: list[Click] = []
    for e in run.events:
        kind = e["event"]
        if kind == "click" and e.get("measured") == cart and "record" in e:
            click = Click(
                int(e["clock"]), int(e["node"][0]), int(e["record"]) & ORDINAL_MASK, int(e["tick"])
            )
            if int(e["number"]) == lamp:
                lamp_clicks.append(click)
            elif int(e["number"]) == post:
                if int(e["record"]) >> 32 != cart:
                    raise SystemExit(f"{run.folder}: a return not born at the cart")
                returns.append(click)
        elif kind == "rerelease" and e.get("measured") == post:
            for row in e.get("rows", []):
                identity = int(row[0])
                if identity >> 32 == cart:
                    post_lines.append(Click(int(e["clock"]), 1, identity & ORDINAL_MASK, int(e["tick"])))
    windows = dict(pin["windows"])  # type: ignore[arg-type]
    one_way, round_from = int(windows["one_way_from_count"]), int(windows["round_trip_from_count"])
    out: list[str] = []
    block: dict[str, object] = {}
    passed = failed = 0

    rate = float(pin["rate_r"])
    pace = float(pin["pace_links_per_interval"])
    dwell = 55 / 32  # one Link of a heading row, intervals (the flight table)

    def one(
        label: str, clicks: list[Click], from_count: int, pin_value: float, reads: str, remainder: float
    ) -> Fraction | None:
        """One ratio against its pin: the band 2 / W as pinned (section 3.2);
        beside it, COMPUTATION, the counts by which the window's span misses
        the closed form's span and the meeting's own remainder per end
        (`remainder`, in the reading detector's counts), and the band in the
        form PREREGISTRATION_V2 section 5 states it, 2 g / (ordinals apart)."""
        nonlocal passed, failed
        value, window = ratio_over(clicks, from_count)
        band = 2 / window if window else 0.0
        verdict = verdict_band(None if value is None else float(value), pin_value, band)
        passed += verdict == "PASS"
        failed += verdict == "FAIL"
        ordinals = window / float(value) if value else 0.0
        off = window - pin_value * ordinals if value else 0.0
        band_v2 = (2 + (2 if label == "round_trip" else 0)) / ordinals if ordinals else 0.0
        verdict_v2 = verdict_band(None if value is None else float(value), pin_value, band_v2)
        out.append(
            f"  DETECTOR {label} = {reads}, from the count {from_count}: "
            f"{'none' if value is None else f'{float(value):.5f}'} over {window} counts ({len(clicks)} lines); "
            f"the pin {pin_value:.5f}, the band 2 / W = {band:.5f}: {verdict}"
        )
        out.append(
            f"    COMPUTATION the window's span misses the closed form's by {off:+.1f} counts over {ordinals:.0f} ordinals; "
            f"the meeting's remainder per end {remainder:.1f} counts (one hop 1 / v plus one dwell 55 / 32, in the reader's counts); "
            f"the band as PREREGISTRATION_V2 section 5 states it, 2 g / (ordinals apart){' + 2 counts' if label == 'round_trip' else ''} = {band_v2:.5f}: {verdict_v2}"
        )
        block[label] = {
            "value": None if value is None else float(value),
            "window": window,
            "band": band,
            "pin": pin_value,
            "verdict": verdict,
            "counts_off": off,
            "ordinals": ordinals,
            "remainder_per_end": remainder,
            "band_v2": band_v2,
            "verdict_v2": verdict_v2,
        }
        return value

    # The remainders per end: a lamp row meeting the hopping cart lands within
    # one hop (1 / v intervals) plus one dwell of the cart's count r; a cart
    # row born at a self-creation (within 1 / r intervals) reaching the fixed
    # post within one dwell, in the post's count (r_R = 1); a return adds the
    # post's next self-creation (one count) and the meeting with the cart.
    k_ab = one(
        "k_AB",
        lamp_clicks,
        one_way,
        float(dict(pin["k_AB"])["value"]),
        "the cart's counts apart over the lamp's ordinals apart",
        (1 / pace + dwell) * rate,
    )  # type: ignore[arg-type]
    k_ba = one(
        "k_BA",
        post_lines,
        one_way,
        float(dict(pin["k_BA"])["value"]),
        "the post's counts apart over the cart's ordinals apart",
        1 / rate + dwell,
    )  # type: ignore[arg-type]
    ratio_pin = dict(pin["ratio_k_BA_over_k_AB"])  # type: ignore[arg-type]
    if k_ab is not None and k_ba is not None:
        ratio = k_ba / k_ab
        window_ab = ratio_over(lamp_clicks, one_way)[1]
        window_ba = ratio_over(post_lines, one_way)[1]
        band = 2 / min(window_ab, window_ba)
        verdict = verdict_band(float(ratio), float(ratio_pin["value"]), band)
        passed += verdict == "PASS"
        failed += verdict == "FAIL"
        out.append(
            f"  COMPUTATION the ratio k_BA / k_AB (two detectors' counts, carries r_R / r_D^2): {float(ratio):.5f}; "
            f"the pin {float(ratio_pin['value']):.5f} (on c^2 = 1/3 {float(ratio_pin['on_the_identity_c']):.5f}; the comparison 1), "
            f"the band {band:.5f}: {verdict}; against the comparison 1: {'PASS' if abs(float(ratio) - 1) <= band else 'FAIL'}"
        )
        block["ratio_k_BA_over_k_AB"] = {
            "value": float(ratio),
            "pin": float(ratio_pin["value"]),
            "band": band,
            "verdict": verdict,
            "against_1": abs(float(ratio) - 1) <= band,
        }
    one(
        "round_trip",
        returns,
        round_from,
        float(dict(pin["round_trip"])["value"]),
        "the cart's counts apart between two returns over its ordinals apart between the births they carry, r-free",
        (1 / rate + dwell + 1 + 1 / pace + dwell) * rate,
    )  # type: ignore[arg-type]
    gaps = Counter(b.ordinal - a.ordinal for a, b in zip(lamp_clicks, lamp_clicks[1:], strict=False))
    out.append(
        f"  DETECTOR the lamp's ordinals at the cart's consecutive clicks advance by {dict(sorted(gaps.items()))} (a missed birth would show as a gap of 2)"
    )
    block["lamp_ordinal_gaps"] = {str(k): v for k, v in sorted(gaps.items())}
    changes = Counter(b.node - a.node for a, b in zip(lamp_clicks, lamp_clicks[1:], strict=False))
    per_count = all(
        abs(b.node - a.node) <= b.count - a.count
        for a, b in zip(lamp_clicks, lamp_clicks[1:], strict=False)
    )
    out.append(
        f"  DETECTOR the least step: the Node's change between consecutive clicks of the lamp's rows {dict(sorted(changes.items()))}, "
        f"at most one per count {'holds' if per_count else 'FAILS'} (a check of the frame, not a pin here)"
    )
    block["least_step"] = {
        "changes": {str(k): v for k, v in sorted(changes.items())},
        "per_count": per_count,
    }
    out.append("  the radar velocity: NOT READ (issue #937; batch 933 stays as recorded)")
    return out, block, passed, failed


def coasting_lines(run: Run) -> tuple[list[str], dict[str, object], int, int]:
    centre = run.roles["detector"]
    stamped = [e for e in run.events if e.get("measured") == centre and "clock" in e]
    differing = [e for e in stamped if int(e["clock"]) != int(e["tick"])]
    ticks_with_click = len({int(e["tick"]) for e in stamped if e["event"] == "click"})
    verdict = "PASS" if stamped and not differing else "FAIL"
    out = [
        f"  DETECTOR the stamp check: {len(stamped)} stamped lines of the centre's measured event, "
        f"{len(differing)} with clock differing from the line's tick, {ticks_with_click} intervals with a click "
        f"(the pin: equal on every stamped line, r_A = 1 at suspension 0): {verdict}",
        "  DETECTOR z: read by tools/covariant_readings.py on this root (the centre's pointer over the late window [300, 400), in the centre's own count by the check above)",
    ]
    block = {
        "stamped_lines": len(stamped),
        "differing": len(differing),
        "ticks_with_click": ticks_with_click,
        "verdict": verdict,
    }
    return out, block, int(verdict == "PASS"), int(verdict == "FAIL")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    root = Path(sys.argv[1])
    pins = json.loads(PINS.read_text(encoding="utf-8"))
    out: list[str] = []
    readings: dict[str, object] = {
        "format": "fail-rows-run-4ab-readings-v1",
        "pins": str(PINS.name),
        "runs": {},
    }
    total_pass = total_fail = record_failures = 0
    for path in sorted(root.rglob("run.json")):
        if path.parent.name == "resolved_view":
            continue
        run = read_run(path.parent)
        out.append(
            f"{run.name}: {run.model}; {run.ticks} intervals, {run.elapsed:.2f} s HOST, {run.hypotheses}; source {run.fingerprint[:12]}"
        )
        if not run.completed or not run.balanced:
            record_failures += 1
            out.append("  RECORD CHECK FAILED: not completed or the books unbalanced")
        else:
            out.append("  the record: completed, the books balanced at every tick")
        if run.model.startswith(J4_PREFIX):
            lines, block, p, f = j4_lines(run, pins["j4"][run.name])
        elif run.model.startswith(CART_PREFIX):
            lines, block, p, f = cart_lines(run, pins["ladder"][run.name])
        elif run.model == STARS_MODEL:
            lines, block, p, f = coasting_lines(run)
        else:
            continue
        out.extend(lines)
        board, board_block = gameboard_lines(run)
        out.extend(board)
        total_pass += p
        total_fail += f
        readings["runs"][run.name] = {  # type: ignore[index]
            "model": run.model,
            "source_sha256": run.fingerprint,
            "completed_ticks": run.ticks,
            "elapsed_seconds": run.elapsed,
            "hypotheses": run.hypotheses,
            "balanced": run.balanced,
            **run.digests,
            "readings": block,
            "gameboard": board_block,
        }
    out.append(
        f"{record_failures} record checks failed, {total_pass} pins PASS, {total_fail} pins FAIL, nothing moved"
    )
    text = "\n".join(out) + "\n"
    print(text, end="")
    (HERE / "run_4ab_readings.out").write_text(text, encoding="utf-8")
    OUT.write_text(json.dumps(readings, indent=1) + "\n", encoding="utf-8")
    return 1 if record_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
