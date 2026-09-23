"""Row 2a's fan options, each visibility a COMPUTATION before any run (the
FAIL Runner C, 2026-09-23; docs/designs/fail_rows/RUN_13_2A.md section 5).

The register's own algebra, `docs/designs/paper_criteria/slits_huygens_pin.py`
(the pin of NATURE row 2a for the registered fan of width 48), applied to
the same world written at other fan widths P by the register's own
generator `examples/events/amplitude/make_worlds.py` (`two_slits_huygens`
with HUYGENS_WIDTH = P; the weights by angle at the grain 2^18 as the
registered world has them, or at a coarser grain where the load-time
ceiling asks it). Nothing here runs the engine: the pin tool imports the
engine's tables and the ladder's `rungs` and `cell_of` so that the
integers are the click's, as the registered pin did. For every P it
prints the fan's size, the sum of squares A of one opening's weights
against the load-time ceiling (A^2 within 2^62), the weights' visibility
and Pearson of the first record, and THE VISIBILITY OF THE CLICKS over the
4096 births of the golden wheel (the criterion of row 2a). At P = 48 the
harness must reproduce the registered pin 0.9659 bit for bit, else it is
not trusted and says so.

Run from the repository root:

    .venv/bin/python docs/designs/fail_rows/run_2a_fan_map.py > docs/designs/fail_rows/run_2a_fan_map.out
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))


def _script(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AMW = _script("amplitude_make_worlds", ROOT / "examples" / "events" / "amplitude" / "make_worlds.py")
PIN = _script("slits_huygens_pin", ROOT / "docs" / "designs" / "paper_criteria" / "slits_huygens_pin.py")

from event_universe.world_loading import families_by_definition, load_world  # noqa: E402

WIDTHS = (16, 24, 32, 40, 48, 56, 64, 80, 96)
CEILING = 1 << 31  # A within 2^31 so that A^2 stays within 2^62 (make_worlds.py, HUYGENS_GRAIN)
REGISTERED = {"clicks": 0.9659, "weights": 0.966, "pearson": 0.891}
CLICKS_RE = re.compile(r"THE VISIBILITY OF THE CLICKS ([\d.]+)")
WEIGHTS_RE = re.compile(
    r"the visibility \(mean bright - mean dark\) / \(mean bright \+ mean dark\) ([\d.]+)"
)
PEARSON_W_RE = re.compile(r"Pearson with the two-source cosine ([\d.]+)")
PEARSON_C_RE = re.compile(r"Pearson\(counts, cosine\) ([\d.]+)")
BRIGHT_RE = re.compile(r"the bright pixels \[([\d, ]+)\] \(registered")
DARK_RE = re.compile(r"the dark \[([\d, ]+)\] \(registered")
TOTALS_RE = re.compile(r"a computation: wall (\d+), screen (\d+) on (\d+) pixels, faces (\d+)")


def world_at(width: int, grain: int) -> dict[str, object]:
    AMW.HUYGENS_WIDTH = width
    AMW.HUYGENS_GRAIN = grain
    world = AMW.two_slits_huygens()
    return families_by_definition(world, AMW.FAMILY_DEFINITIONS, AMW.DEFINITIONS_SOURCE)


def opening_weights(world: dict[str, object]) -> list[int]:
    for entry in world["measured"]:  # type: ignore[union-attr]
        table = entry.get("table")
        if (
            isinstance(table, dict)
            and isinstance(table.get("light"), dict)
            and "weights" in table["light"]
        ):
            return list(table["light"]["weights"])
    raise RuntimeError("no opening")


def pin_at(path: Path) -> dict[str, object]:
    PIN.WORLD = path
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        PIN.main()
    text = buffer.getvalue()
    found: dict[str, object] = {"text": text}
    for key, pattern in (
        ("clicks", CLICKS_RE),
        ("weights", WEIGHTS_RE),
        ("pearson_weights", PEARSON_W_RE),
        ("pearson_clicks", PEARSON_C_RE),
    ):
        match = pattern.search(text)
        found[key] = float(match.group(1)) if match else None
    for key, pattern in (("bright", BRIGHT_RE), ("dark", DARK_RE)):
        match = pattern.search(text)
        found[key] = [int(v) for v in match.group(1).split(",")] if match else None
    match = TOTALS_RE.search(text)
    found["totals"] = tuple(int(v) for v in match.groups()) if match else None
    return found


def main() -> None:
    print("ROW 2a: THE FAN'S OPTIONS, EACH VISIBILITY A COMPUTATION BEFORE ANY RUN (no engine run)")
    print(
        "the world: examples/events/amplitude/make_worlds.py two_slits_huygens() at HUYGENS_WIDTH = P;"
        " the pin: docs/designs/paper_criteria/slits_huygens_pin.py on that world (4096 births, the golden wheel"
        " [2531, 4096], N = 64, the screen at x = 52, the bright pixels y = 35..38, 59..61, 82..85 and the dark"
        " 13..20, 48..50, 70..72, 100..107 of the two-source cosine, unchanged for every P)"
    )
    print()
    print(
        "| P | directions per opening (admitted / full fan) | the grain | A = sum a^2 of one opening"
        " | A < 2^31 (loads) | the weights' visibility (first record) | Pearson (weights) |"
        " THE CLICKS' VISIBILITY (4096 births) | Pearson (clicks) | wall / screen / pixels / faces |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    results: dict[int, dict[str, object]] = {}
    with tempfile.TemporaryDirectory() as tmp:
        for width in WIDTHS:
            grain = 1 << 18
            world = world_at(width, grain)
            weights = opening_weights(world)
            a_sum = sum(w * w for w in weights)
            note = ""
            while a_sum >= CEILING:
                grain //= 2
                world = world_at(width, grain)
                weights = opening_weights(world)
                a_sum = sum(w * w for w in weights)
                note = f" (the grain lowered from 2^18 to 2^{grain.bit_length() - 1} for the ceiling)"
            admitted = len(weights)
            full = len(AMW.huygens_fan()[1])
            path = Path(tmp) / f"slits_huygens_p{width}.json"
            path.write_text(json.dumps(world, separators=(",", ":")) + "\n", encoding="utf-8")
            loads = "yes"
            try:
                # The loader on the world's JSON text, the family reference
                # resolved from the registered folder as the shipped file's is.
                load_world(
                    path.read_text(encoding="utf-8"), base_dir=ROOT / "examples" / "events" / "amplitude"
                )
            except Exception as error:  # noqa: BLE001
                loads = f"NO ({type(error).__name__}: {str(error)[:140]})"
            found = pin_at(path)
            results[width] = found
            totals = found["totals"]
            print(
                f"| {width} | {admitted} / {full} | 2^{grain.bit_length() - 1}{note} | {a_sum} | "
                f"{'yes' if a_sum < CEILING else 'no'}, loader: {loads} | {found['weights']:.3f} | "
                f"{found['pearson_weights']:.3f} | **{found['clicks']:.4f}** | {found['pearson_clicks']:.3f} | "
                f"{totals[0]} / {totals[1]} / {totals[2]} / {totals[3]} |"
            )
    print()
    at48 = results[48]
    trusted = (
        abs(at48["clicks"] - REGISTERED["clicks"]) < 5e-5
        and at48["bright"] == PIN.REGISTERED_BRIGHT
        and at48["dark"] == PIN.REGISTERED_DARK
        and at48["totals"] == (882, 1711, 107, 1503)
    )
    print(
        f"THE HARNESS AT P = 48 AGAINST THE REGISTERED PIN: the clicks' visibility {at48['clicks']:.4f} "
        f"(registered 0.9659), the bright {at48['bright']} and the dark {at48['dark']} pixels, the totals "
        f"{at48['totals']} (registered 882, 1711 on 107, 1503): {'REPRODUCED bit for bit' if trusted else 'NOT REPRODUCED: the table above is not trusted'}"
    )
    print()
    print("the bright and dark pixels' counts per P (the clicks over 4096 births):")
    for width in WIDTHS:
        print(f"  P = {width}: bright {results[width]['bright']}, dark {results[width]['dark']}")
    print()
    print(
        "THE PIN TOOL'S FULL OUTPUT PER P (the counts per cell, bit for bit, the pin of a run at that width):"
    )
    for width in WIDTHS:
        print()
        print(f"===== P = {width} =====")
        print(results[width]["text"].rstrip())
    best = max(WIDTHS, key=lambda w: results[w]["clicks"])
    print()
    print(
        f"the highest visibility in the clicks among the options computed: {results[best]['clicks']:.4f} at P = {best};"
        f" against the verified two-slit figure 0.94 (Jacques et al. 2005, the biprism's central fringe) every option"
        f" at or above 0.94 is a bound met, and none reaches the ideal 1"
    )


if __name__ == "__main__":
    main()
