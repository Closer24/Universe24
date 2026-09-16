"""Audit helper: tabulate every entity in the catalog JSON file (read-only).

usage: PYTHONPATH=src python examples/research/entity-audit/dump_catalog.py [CATALOG] [--output FILE]
"""

from __future__ import annotations

import argparse
import contextlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "examples" / "known-entities" / "catalog.json"


def prop_summary(p: dict) -> str:
    parts = [p.get("status", "?")]
    if "value_decimal" in p:
        parts.append(p["value_decimal"] + " " + p.get("unit", ""))
    elif "metadata_key" in p:
        parts.append("meta:" + p["metadata_key"])
    elif "entity_id" in p:
        parts.append("ref:" + p["entity_id"] + ("*-1" if p.get("reference_sign") == -1 else ""))
    elif "value" in p:
        parts.append(str(p["value"])[:60])
    if "uncertainty_decimal" in p:
        parts.append("+-" + p["uncertainty_decimal"])
    if "uncertainty_plus_decimal" in p:
        parts.append("+" + p["uncertainty_plus_decimal"] + "/-" + p["uncertainty_minus_decimal"])
    if "bound_kind" in p:
        parts.append(p["bound_kind"])
    if "confidence_level" in p:
        parts.append("CL" + str(p["confidence_level"]))
    parts.append("src=" + ",".join(p.get("sources", [])))
    return " | ".join(parts)


def dump(c: dict) -> None:
    for e in c["particle_entities"]:
        print(
            "\n==",
            e["id"],
            e["label"],
            e["category"],
            "anti=",
            e.get("antiparticle_id"),
            "Q/3=",
            e["electric_charge_thirds"],
            "2s=",
            e["twice_spin"],
            e["physical_status"],
            e["representation_status"],
            e["dynamics_status"],
        )
        for k, p in e["physical_properties"].items():
            print("   ", k, "::", prop_summary(p))
    print("\n\n######## FIELDS")
    for e in c["field_entities"]:
        print(
            "\n==",
            e["id"],
            e["label"],
            e["physical_status"],
            e["representation_status"],
            e["dynamics_status"],
            e["emergence_status"],
            "exc=",
            e.get("excitation_ids"),
        )
        for k, p in e["physical_properties"].items():
            print("   ", k, "::", prop_summary(p))
    print("\n\n######## DISTURBANCE FAMILIES")
    for e in c["disturbance_families"]:
        print(
            "\n==",
            e["id"],
            e["label"],
            e["physical_status"],
            "fields=",
            e.get("field_ids"),
            "src=",
            e.get("sources"),
        )
        for k, p in e["physical_properties"].items():
            print("   ", k, "::", prop_summary(p))
    print("\n\n######## INTERACTIONS")
    for e in c["interaction_families"]:
        print(
            "==",
            e["id"],
            e["physical_status"],
            e["claim_level"],
            "parts=",
            e["participant_ids"],
            "med=",
            e["mediator_ids"],
        )
    print("\n\n######## CHANNELS")
    for e in c["representative_channels"]:
        print(
            "==",
            e["id"],
            e["interaction_id"],
            e["incoming_ids"],
            "->",
            e["outgoing_ids"],
            e["physical_status"],
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path, nargs="?", default=CATALOG)
    parser.add_argument("--output", type=Path, help="write the listing to this file instead of stdout")
    args = parser.parse_args()
    c = json.loads(args.catalog.read_text(encoding="utf-8"))
    if args.output is None:
        dump(c)
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle, contextlib.redirect_stdout(handle):
        dump(c)


if __name__ == "__main__":
    main()
