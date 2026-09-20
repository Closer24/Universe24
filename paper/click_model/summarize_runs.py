"""Summarise the runs of series L for the paper: the numbers the tables and
figures cite, read from each run's `run.json` (the world's list of gathers)
and compared with `examples/events/amplitude/expectations.json`.

    PYTHONPATH=src python paper/click_model/summarize_runs.py RUNS_DIR \
        --output paper/click_model/figures/summary.json

RUNS_DIR is the output of `tools/run_series.py` over the worlds of
`examples/events/amplitude/` (one directory per world with `run/run.json`).
Nothing is computed from the engine here: the gathers are counted as the
register counts them, over the records whose ordinal is at most N (one birth
per birth phase u). The summary carries every run's source fingerprint so
that the figures name the tree they came from.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

MZ_WORLDS = (
    "mz_equal",
    "mz_half",
    "mz_quarter",
    "mz_balanced",
    "mz_345",
    "mz_unequal_f0",
    "mz_unequal_f8",
    "mz_unequal_f16",
    "ev_29",
    "ev_169",
)
PAIR_WORLDS = {
    64: ("bell_0_8", "bell_0_24", "bell_16_8", "bell_16_24"),
    1024: ("bell_n1024_0_128", "bell_n1024_0_384", "bell_n1024_256_128", "bell_n1024_256_384"),
    4096: ("bell_n4096_0_512", "bell_n4096_0_1536", "bell_n4096_1024_512", "bell_n4096_1024_1536"),
}
PATH_WORLDS = ("path_0_8", "path_0_24", "path_16_8", "path_16_24")
GHZ_WORLDS = ("ghz_xxx", "ghz_xyy", "ghz_yxy", "ghz_yyx", "ghz_yyy")


def load_run(runs: Path, world: str) -> dict:
    return json.loads((runs / world / "run" / "run.json").read_text(encoding="utf-8"))


def ordinal(record: int) -> int:
    return record & 0xFFFFFFFF


def gathers(run: dict, births: int) -> list[dict]:
    return [g for g in run["world"] if ordinal(g["record"]) <= births]


def outcomes(gather: dict) -> tuple[str, ...]:
    """The channel per arm in arm order: '+' or '-' at a rotated set, the set's name otherwise."""
    chosen = sorted(gather["chosen"], key=lambda item: item[1])
    return tuple(channel if channel in "+-" else name for name, _arm, channel in chosen)


def signs(gather: dict) -> str:
    """The rotated sets' channels in arm order ('+' or '-'), a which-path read left out."""
    return "".join(o for o in outcomes(gather) if o in "+-")


def pair_cells(run: dict, births: int) -> dict[str, int]:
    counts = Counter(signs(g) for g in gathers(run, births))
    return {key: counts.get(key, 0) for key in ("++", "+-", "-+", "--")}


def correlation(cells: dict[str, int], births: int) -> Fraction:
    return Fraction(cells["++"] + cells["--"] - cells["+-"] - cells["-+"], births)


def marginals(cells: dict[str, int]) -> dict[str, int]:
    return {"A+": cells["++"] + cells["+-"], "B+": cells["++"] + cells["-+"]}


def summarise(runs: Path, expectations: dict) -> dict:
    out: dict = {
        "fingerprints": {},
        "mach_zehnder": {},
        "pair": {},
        "which_path": {},
        "ghz": {},
        "two_slits": {},
    }
    for world in MZ_WORLDS:
        run = load_run(runs, world)
        out["fingerprints"][world] = run["source_sha256"]
        rows = gathers(run, 64)
        counts = Counter(outcomes(g)[0] for g in rows)
        unit = run["layer"]["unit"]
        totals = sorted({str(Fraction(g["total"][0], g["total"][1]) / unit) for g in rows})
        expected = expectations["mach_zehnder"][world]["clicks"]
        out["mach_zehnder"][world] = {
            "clicks": dict(counts),
            "expected": expected,
            "agrees": all(counts.get(k, 0) == v for k, v in expected.items()),
            "gathers": len(rows),
            "distinct_totals": len(totals),
            "totals": totals,
        }
    for births, worlds in PAIR_WORLDS.items():
        entries = {}
        s = Fraction(0)
        for world, sign in zip(worlds, (1, -1, 1, 1), strict=True):
            run = load_run(runs, world)
            out["fingerprints"][world] = run["source_sha256"]
            cells = pair_cells(run, births)
            e = correlation(cells, births)
            s += sign * e
            entries[world] = {
                "cells": cells,
                "E": str(e),
                "E_times_N": e.numerator * (births // e.denominator),
                "marginals": marginals(cells),
                "gathers": len(gathers(run, births)),
            }
        out["pair"][str(births)] = {"worlds": entries, "S": str(s), "S_float": float(s)}
    for world in PATH_WORLDS:
        run = load_run(runs, world)
        out["fingerprints"][world] = run["source_sha256"]
        cells = pair_cells(run, 64)
        out["which_path"][world] = {"cells": cells, "E": str(correlation(cells, 64))}
    s = Fraction(0)
    for world, sign in zip(PATH_WORLDS, (1, -1, 1, 1), strict=True):
        s += sign * Fraction(out["which_path"][world]["E"])
    out["which_path"]["S"] = str(s)
    for world in GHZ_WORLDS:
        run = load_run(runs, world)
        out["fingerprints"][world] = run["source_sha256"]
        counts = Counter("".join(outcomes(g)) for g in gathers(run, 64))
        products = sorted({(-1) ** key.count("-") for key in counts})
        out["ghz"][world] = {"triples": dict(sorted(counts.items())), "products": products}
    run = load_run(runs, "slits_low")
    out["fingerprints"]["slits_low"] = run["source_sha256"]
    rows = gathers(run, 64)
    per_set = Counter(outcomes(g)[0] for g in rows)
    kinds = {"wall": 0, "screen": 0, "faces": 0}
    for name, count in per_set.items():
        kinds[
            "wall"
            if name.startswith("measured:")
            else "screen"
            if name.startswith("screen_")
            else "faces"
        ] += count
    expected = expectations["two_slits"]
    out["two_slits"] = {
        "clicks": dict(sorted(per_set.items())),
        "clicks_by_kind": kinds,
        "expected_clicks_by_kind": expected["clicks_by_kind"],
        "agrees": dict(per_set) == {k: v for k, v in expected["clicks"].items()},
        "weights": expected["weights"],
        "screen_alone": expected["screen_alone"],
        "pearson": expected["pearson"],
        "gathers": len(rows),
    }
    # the choosers' 15 setting pairs, binned by the windows carried on the gather
    run = load_run(runs, "bell_choosers")
    out["fingerprints"]["bell_choosers"] = run["source_sha256"]
    bins: dict[tuple[int, int], Counter] = {}
    n_steps = run["N"]
    # the register's bins: the 960 births from tick 8 (the ordinals 8 .. 967), 64 per setting pair
    for g in run["world"]:
        if not 8 <= ordinal(g["record"]) <= 967:
            continue
        windows = {name: setting for name, setting, _turn in g["windows"]}
        # the setting is the plus counter's window; the minus counter's is its complement
        a = (
            windows["alice_plus"]
            if "alice_plus" in windows
            else (windows.get("alice_minus", 0) - n_steps // 2) % n_steps
        )
        b = (
            windows["bob_plus"]
            if "bob_plus" in windows
            else (windows.get("bob_minus", 0) - n_steps // 2) % n_steps
        )
        if not windows:
            continue
        bins.setdefault((a, b), Counter())[signs(g)] += 1
    choosers = {}
    for (a, b), counter in sorted(bins.items()):
        cells = {key: counter.get(key, 0) for key in ("++", "+-", "-+", "--")}
        n = sum(cells.values())
        choosers[f"{a}_{b}"] = {
            "cells": cells,
            "pairs": n,
            "E": str(correlation(cells, n)) if n else None,
        }
    out["choosers"] = choosers
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("runs", type=Path)
    parser.add_argument("--output", type=Path, default=Path("paper/click_model/figures/summary.json"))
    parser.add_argument(
        "--expectations", type=Path, default=Path("examples/events/amplitude/expectations.json")
    )
    args = parser.parse_args()
    expectations = json.loads(args.expectations.read_text(encoding="utf-8"))
    summary = summarise(args.runs, expectations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    for world, entry in summary["mach_zehnder"].items():
        print(
            f"{world:16s} {entry['clicks']}  expected {entry['expected']}  agrees {entry['agrees']}  totals {entry['distinct_totals']}"
        )
    for n, entry in summary["pair"].items():
        print(
            f"N={n}: S = {entry['S']} = {entry['S_float']:.6f}; "
            + "; ".join(
                f"{w}: {v['cells']} E={v['E']} marg={v['marginals']}" for w, v in entry["worlds"].items()
            )
        )
    print("which-path S =", summary["which_path"]["S"])
    for world, entry in summary["ghz"].items():
        print(world, entry["triples"], "products", entry["products"])
    print(
        "two slits:",
        summary["two_slits"]["clicks_by_kind"],
        "expected",
        summary["two_slits"]["expected_clicks_by_kind"],
        "agrees",
        summary["two_slits"]["agrees"],
    )
    print("choosers:", {k: v["E"] for k, v in summary["choosers"].items()})
    print("fingerprints:", sorted({v[:12] for v in summary["fingerprints"].values()}))


if __name__ == "__main__":
    main()
