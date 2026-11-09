"""Bit-for-bit equivalence of ``VariantEngine`` and the native ``Engine``.

Every recorded preparation of ``research/matter_light_blocks_v1`` (they use all
eight sign triples) and the three engine examples are run side by side by the
native Engine and by a VariantEngine holding the same reference table. All
retained components ``(a, b, r)`` of every complete state are compared at every
update, the variant inverse is checked at every update, and each block's final
state must equal the SHA-256 recorded in its catalog. ``--family`` instead
builds and fully validates every member of ``covariant_family()``.

    python -m research.coupling_variants_v1.audit --quick            # skip blocks marked heavy
    python -m research.coupling_variants_v1.audit --output runs/variant-equivalence.json
    python -m research.coupling_variants_v1.audit --family           # all 61,440 tables (about 3 minutes)
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

from universe24.experiments import load as load_reference

from .coupling import VariantCoupling, covariant_family, sign_text
from .engine import VariantEngine

ROOT = Path(__file__).resolve().parents[2]
ENGINE_EXAMPLES = ("examples/impulse.json", "examples/signed_impulse.json", "examples/clock.json")


def compare(engine, initial, steps: int) -> dict:
    """Run both executors; return counts and the first difference, if any."""
    variant = VariantEngine(VariantCoupling.reference(engine.coupling.body_signs))
    reference = state = initial
    for t in range(1, steps + 1):
        reference_next = engine.advance(reference)
        variant_next = variant.advance(state)
        if variant_next != reference_next:
            return {"steps": steps, "transitions": t - 1, "first_difference": t}
        if variant.rewind(variant_next) != state:
            return {"steps": steps, "transitions": t - 1, "inverse_failure": t}
        reference, state = reference_next, variant_next
    return {"steps": steps, "transitions": steps, "final": state}


def run(quick: bool = False, names=None) -> dict:
    from research.matter_light_blocks_v1 import verify as blocks

    cases, failures = [], []
    for path in ENGINE_EXAMPLES:
        experiment = load_reference(ROOT / path)
        cases.append((path, experiment.engine, experiment.initial, experiment.steps, None))
    for entry in blocks.load_catalog()["entries"]:
        if (quick and entry.get("heavy")) or (names and entry["name"] not in names):
            continue
        if entry.get("coupling", {}).get("kind") == "variant":
            continue  # a variant block has no reference Engine to be compared with
        engine, initial, steps, _ = blocks.load(entry["name"])
        cases.append((entry["name"], engine, initial, steps, entry["final_state_sha256"]))
    per_signs, transitions, start = Counter(), 0, time.time()
    for name, engine, initial, steps, final_hash in cases:
        result = compare(engine, initial, steps)
        transitions += result["transitions"]
        per_signs[sign_text(engine.coupling.body_signs)] += 1
        if "final" not in result:
            failures.append({"case": name, **result})
        elif final_hash is not None and blocks.state_hash(result["final"]) != final_hash:
            failures.append({"case": name, "final_state_hash": "differs from catalog"})
    return {"format": "coupling_variants_v1-equivalence-1", "cases": len(cases),
            "cases_per_sign_triple": dict(sorted(per_signs.items())),
            "compared_transitions": transitions, "failures": failures,
            "checks": "every complete state (a,b,r) equal at every update; variant inverse at every update; "
                      "final state SHA-256 equal to the blocks catalog",
            "seconds": round(time.time() - start, 1)}


def family() -> dict:
    """Construct and validate every reciprocal 2O-covariant unit-weight table."""
    start, fingerprints, references, pairings = time.time(), set(), 0, Counter()
    for actions, weights in covariant_family():
        coupling = VariantCoupling.from_body_actions("member", actions, weights)
        fingerprints.add(coupling.fingerprint)
        references += not coupling.is_variant
        pairings[coupling.pairs] += 1
    return {"format": "coupling_variants_v1-family-1", "validated_tables": sum(pairings.values()),
            "distinct_fingerprints": len(fingerprints), "pairings": len(pairings),
            "tables_per_pairing": sorted(set(pairings.values())), "reference_tables": references,
            "failures": [], "seconds": round(time.time() - start, 1)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m research.coupling_variants_v1.audit")
    parser.add_argument("--quick", action="store_true", help="skip blocks marked heavy")
    parser.add_argument("--output", type=Path, help="write the JSON report (never overwrites)")
    parser.add_argument("--family", action="store_true", help="validate every covariant_family() table")
    parser.add_argument("names", nargs="*", help="restrict to these block names")
    args = parser.parse_args(argv)
    report = family() if args.family else run(args.quick, set(args.names) or None)
    text = json.dumps(report, indent=1)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
