"""Read the records of experiment A12 (docs/EXPERIMENTS.md), Malus's law and the
three-polarizer chain, and evaluate its criterion clause by clause: the content
that clicked at the marked Node behind the last polarizer per run (the
`detector_click` records), what every polarizer passed, sank and holds (the
`polarizer` records, with the polarization of every ray leaving it, the body's
angle), the exact expectation of the declared table's integer rule (the same
floors and registers, computed here from the world file alone), Malus's cos^2 in
floating point for comparison, the ledger and the exactness of every split. A
Renderer of records in the sense of Highlights 3.29: it reads only what the runner
wrote (``run.json``, ``events.jsonl``, ``initialization.json``) and never the engine.

Run:  python examples/nature/a12_malus/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
where RUN is a run directory (``run.json`` beside ``events.jsonl``) of one world
of ``make_worlds.py``. The per-run table and the clause table are printed;
``--out`` writes the full summary and ``--record`` the small committed record.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

MALUS_CHAIN_OF_FOUR = math.cos(math.radians(22.5)) ** 8


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    events = []
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"polarizer"' in line or '"detector_click"' in line or '"external_body_absorbed"' in line:
                events.append(json.loads(line))
    return directory, metadata, world, events


def geometry(world):
    """The source (its amount per pulse, its pulses and its polarization), the
    polarizers in beam order (position, angle, table) and the marked Node behind
    the last one."""
    lamp = world["disturbance_types"][0]
    emission = world["emissions"][0]
    stock = lamp["defaults"][emission["field"]]
    amount = emission["amount"]
    bodies = sorted(world["external_bodies"], key=lambda body: body["position"][0])
    polarizers = [
        {
            "position": body["position"],
            "angle": body["polarizer"]["angle"],
            "steps": len(body["polarizer"]["table"]),
            "table": body["polarizer"]["table"],
        }
        for body in bodies
    ]
    source = world["seeds"][0]["position"]
    marks = [d["position"] for d in world["detectors"] if d["position"] != source]
    return {
        "source": source,
        "amount": amount,
        "pulses": stock // amount,
        "emitted": stock,
        "polarization": emission.get("polarization", -1),
        "polarizers": polarizers,
        "mark": marks[0],
        "steps": polarizers[0]["steps"] if polarizers else None,
    }


def table_rule(geo):
    """The declared table's integer rule, pulse by pulse: what each polarizer
    passes and sinks and what its registers hold, the same floors and registers
    as the engine's (ray-polarization-v1), from the world file alone."""
    steps = geo["steps"]
    bodies = [
        {"pass_register": 0, "sink_register": 0, "passed": 0, "sunk": 0} for _ in geo["polarizers"]
    ]
    clicked = 0
    for _ in range(geo["pulses"]):
        content, polarization = geo["amount"], geo["polarization"]
        for body, polarizer in zip(bodies, geo["polarizers"], strict=True):
            if not content:
                break
            if polarization < 0:
                share = sum(polarizer["table"]) // steps
            else:
                share = polarizer["table"][(polarizer["angle"] - polarization) % steps]
            passed, pass_fraction = divmod(content * share, steps)
            sunk, sink_fraction = divmod(content * (steps - share), steps)
            body["pass_register"] += pass_fraction
            body["sink_register"] += sink_fraction
            released, body["pass_register"] = divmod(body["pass_register"], steps)
            sunk_released, body["sink_register"] = divmod(body["sink_register"], steps)
            passed += released
            sunk += sunk_released
            body["passed"] += passed
            body["sunk"] += sunk
            content, polarization = passed, polarizer["angle"]
        clicked += content
    return {
        "clicked": clicked,
        "bodies": bodies,
        "held": sum((b["pass_register"] + b["sink_register"]) // steps for b in bodies),
    }


def malus(geo):
    """Malus's law in floating point: the product of cos^2 of the successive
    differences, times the emitted content."""
    steps = geo["steps"]
    fraction = 1.0
    polarization = geo["polarization"]
    for polarizer in geo["polarizers"]:
        if polarization < 0:
            fraction *= 0.5
        else:
            fraction *= math.cos(math.pi * (polarizer["angle"] - polarization) / steps) ** 2
        polarization = polarizer["angle"]
    return fraction


def analyze(run):
    directory, metadata, world, events = load(run)
    geo = geometry(world)
    mark = geo["mark"]
    clicks = [e for e in events if e["event"] == "detector_click" and e["position"] == mark]
    clicked = sum(e["amount"] for e in clicks)
    per_body = []
    for polarizer in geo["polarizers"]:
        records = [
            e for e in events if e["event"] == "polarizer" and e["position"] == polarizer["position"]
        ]
        per_body.append(
            {
                "position": polarizer["position"],
                "angle": polarizer["angle"],
                "arrivals": len(records),
                "amount_in": sum(e["amount"] for e in records),
                "passed": sum(e["passed"] + e["released"][0] for e in records),
                "sunk": sum(e["sunk"] + e["released"][1] for e in records),
                "polarizations_in": sorted(
                    {e["polarization"] for e in records}, key=lambda p: (p is None, p)
                ),
                "polarization_out": polarizer["angle"],
                "differences": sorted({e["difference"] for e in records}, key=lambda d: (d is None, d)),
                "shares": sorted({e["share"] for e in records}),
                "registers_final": records[-1]["registers"] if records else None,
                "register_ever_nonzero": any(any(e["registers"]) for e in records),
                "released": [
                    sum(e["released"][0] for e in records),
                    sum(e["released"][1] for e in records),
                ],
                # Every record exact: amount = passed + sunk + the whole quantum the two
                # fractions make (0 or 1), the fractions summing to 0 or to the steps.
                "every_record_exact": all(
                    e["amount"] == e["passed"] + e["sunk"] + (sum(e["held"]) // e["steps"])
                    and sum(e["held"]) in (0, e["steps"])
                    for e in records
                ),
            }
        )
    expected = table_rule(geo)
    fraction = malus(geo)
    audit = metadata["audit"]
    final_bodies = metadata["external_bodies"]
    held_final = sum(
        sum(body["final"]["held"]) // geo["steps"] for body in final_bodies if body["final"].get("held")
    )
    return {
        "run": str(directory),
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "elapsed_seconds": metadata["elapsed_seconds"],
        "ticks": metadata["completed_ticks"],
        "angles": [p["angle"] for p in geo["polarizers"]],
        "degrees": [p["angle"] * 180 / geo["steps"] for p in geo["polarizers"]],
        "steps": geo["steps"],
        "emitted": geo["emitted"],
        "pulses": geo["pulses"],
        "clicked": clicked,
        "clicks": len(clicks),
        "clicked_fraction": clicked / geo["emitted"],
        "table_expected": expected["clicked"],
        "table_expected_held": expected["held"],
        "table_bodies": expected["bodies"],
        "malus_fraction": fraction,
        "malus_expected": fraction * geo["emitted"],
        "polarizers": per_body,
        "sink_totals": metadata["external_body_totals"],
        "held_final": held_final,
        "escaped_totals": metadata["escaped_totals"],
        "final_totals": metadata["final_totals"],
        "all_balanced": all(line["balanced"] for line in audit),
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "ray_polarization": metadata.get("ray_polarization"),
    }


def clauses(results):
    """The criterion of A12, each clause with its verdict and its numbers."""
    singles = [r for r in results if len(r["angles"]) == 1 and r["model"].startswith("a12-malus-single")]
    table = []
    # 1. One polarizer passes the table's cos^2 of the content exactly, the remainder owned.
    single = {
        r["model"]: {
            "degrees": r["degrees"][0],
            "clicked": r["clicked"],
            "table_expected": r["table_expected"],
            "malus_expected": r["malus_expected"],
            "clicked_fraction": r["clicked_fraction"],
            "malus_fraction": r["malus_fraction"],
            "exact": r["clicked"] == r["table_expected"]
            and all(p["every_record_exact"] for p in r["polarizers"]),
            "remainder_rule_exercised": any(p["register_ever_nonzero"] for p in r["polarizers"]),
        }
        for r in singles
    }
    table.append(
        {
            "clause": "one polarizer passes the table's cos^2 of the content exactly, the remainder owned",
            "pass": bool(single) and all(v["exact"] for v in single.values()),
            "numbers": single,
        }
    )
    # 2. The chain y, 90 passes 0.
    crossed = next((r for r in results if r["model"] == "a12-malus-chain-90"), None)
    table.append(
        {
            "clause": "the chain y, 90 passes 0",
            "pass": crossed is not None and crossed["clicked"] == 0,
            "numbers": None if crossed is None else {"clicked": crossed["clicked"]},
        }
    )
    # 3. The chain y, 45, 90 passes 1/4 of the content within the table's rounding.
    quarter = next((r for r in results if r["model"] == "a12-malus-chain-45-90"), None)
    numbers3 = None
    if quarter is not None:
        band = abs(quarter["table_expected"] - quarter["emitted"] / 4) + len(quarter["angles"])
        numbers3 = {
            "clicked": quarter["clicked"],
            "quarter": quarter["emitted"] / 4,
            "table_expected": quarter["table_expected"],
            "band": band,
            "fail_zero_or_half": quarter["clicked"] in (0, quarter["emitted"] // 2),
        }
    table.append(
        {
            "clause": "the chain y, 45, 90 passes 1/4 of the content within the table's rounding",
            "pass": quarter is not None
            and abs(quarter["clicked"] - quarter["emitted"] / 4) <= numbers3["band"]
            and not numbers3["fail_zero_or_half"],
            "numbers": numbers3,
        }
    )
    # 4. The chain of four passes cos^8(22.5) = 0.531 within the rounding.
    four = next((r for r in results if r["model"] == "a12-malus-chain-22-45-67-90"), None)
    numbers4 = None
    if four is not None:
        # The table's own compounded fraction, the product of the recorded shares
        # (one share per polarizer, since one polarization arrives at each) over the
        # steps; the rounding is its distance from cos^8, in quanta, plus one quantum
        # per polarizer for the registers' timing.
        table_fraction = 1.0
        for p in four["polarizers"]:
            table_fraction *= (p["shares"][0] if p["shares"] else 0) / four["steps"]
        rounding = abs(table_fraction - MALUS_CHAIN_OF_FOUR) * four["emitted"]
        band = rounding + len(four["angles"])
        numbers4 = {
            "clicked": four["clicked"],
            "clicked_fraction": four["clicked_fraction"],
            "cos8": MALUS_CHAIN_OF_FOUR,
            "cos8_expected": MALUS_CHAIN_OF_FOUR * four["emitted"],
            "table_fraction": table_fraction,
            "table_expected": four["table_expected"],
            "rounding_of_the_table": rounding,
            "band": band,
            "held_final": four["held_final"],
        }
    table.append(
        {
            "clause": "the chain of four passes cos^8(22.5) = 0.531 within the rounding",
            "pass": four is not None
            and abs(four["clicked"] - MALUS_CHAIN_OF_FOUR * four["emitted"]) <= numbers4["band"],
            "numbers": numbers4,
        }
    )
    # 5. Content exact at every tick, every split exact.
    exact = {
        r["model"]: {
            "all_balanced": r["all_balanced"],
            "conserved": r["conserved_at_every_completed_tick"],
            "status": r["status"],
            "every_record_exact": all(p["every_record_exact"] for p in r["polarizers"]),
            "clicked_plus_sunk_plus_held_plus_escaped": r["clicked"]
            + sum(v[0] for v in r["sink_totals"].values())
            + r["held_final"],
            "emitted": r["emitted"],
            "sunk": {k: v[0] for k, v in r["sink_totals"].items() if v[0]},
            "held_final": r["held_final"],
            "table_expected_held": r["table_expected_held"],
        }
        for r in results
    }
    table.append(
        {
            "clause": "content exact at every tick, every split exact",
            "pass": bool(exact)
            and all(
                v["all_balanced"]
                and v["conserved"]
                and v["status"] == "completed"
                and v["every_record_exact"]
                and v["clicked_plus_sunk_plus_held_plus_escaped"] == v["emitted"]
                for v in exact.values()
            ),
            "numbers": exact,
        }
    )
    return table


def print_run(r):
    print(f"\n== {r['model']}  angles {r['angles']} ({', '.join(f'{d:g}' for d in r['degrees'])} deg)")
    print(
        f"   emitted {r['emitted']} in {r['pulses']} pulses; clicked {r['clicked']} "
        f"({r['clicked_fraction']:.4f}); table rule {r['table_expected']} "
        f"(+{r['table_expected_held']} held); Malus {r['malus_expected']:.1f} ({r['malus_fraction']:.4f})"
    )
    for p in r["polarizers"]:
        print(
            f"   polarizer at x={p['position'][0]} angle {p['angle']}: in {p['amount_in']} "
            f"passed {p['passed']} sunk {p['sunk']} released {p['released']} "
            f"registers {p['registers_final']} polarization out {p['polarization_out']} "
            f"(in {p['polarizations_in']}, d {p['differences']}, share {p['shares']})"
        )
    print(
        f"   sinks {r['sink_totals']} held {r['held_final']} escaped {r['escaped_totals']}; "
        f"balanced {r['all_balanced']} conserved {r['conserved_at_every_completed_tick']} "
        f"status {r['status']} {r['elapsed_seconds']:.1f} s"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    for r in results:
        print_run(r)
    table = clauses(results)
    print("\n== Criterion of A12, clause by clause")
    for entry in table:
        verdict = "PASS" if entry["pass"] else "FAIL"
        print(f"   {verdict}  {entry['clause']}")
        print("         " + json.dumps(entry["numbers"], default=str)[:1500])
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "clauses": table}, indent=1) + "\n", encoding="utf-8"
        )
    if args.record:
        record = {"runs": [{k: r[k] for k in r if k != "run"} for r in results], "clauses": table}
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
