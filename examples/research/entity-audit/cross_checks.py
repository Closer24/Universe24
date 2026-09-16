"""Audit helper: cross-file consistency checks of the entity catalog (read-only).

usage: PYTHONPATH=src python examples/research/entity-audit/cross_checks.py [--output FILE]
"""

from __future__ import annotations

import argparse
import contextlib
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG = ROOT / "examples" / "known-entities" / "catalog.json"
CONTRACTS = ROOT / "examples" / "particle-contracts" / "entities.json"


def checks() -> None:
    c = json.loads(CATALOG.read_text(encoding="utf-8"))
    P = {e["id"]: e for e in c["particle_entities"]}

    # 1. channel charge and baryon-number balance; lepton sector count
    def bnum(i: str) -> Fraction:
        p = P[i]["physical_properties"].get("baryon_number")
        if not p:
            return Fraction(0)
        return Fraction(p["value"], 3 if "third" in p["unit"] else 1)

    def lnum(i: str) -> int:
        s = P[i]["physical_properties"].get("lepton_sector", {}).get("value", "")
        return (
            1
            if s == "lepton interaction sector"
            else (-1 if s == "antilepton interaction sector" else 0)
        )

    for ch in c["representative_channels"]:
        q_in = sum(P[i]["electric_charge_thirds"] for i in ch["incoming_ids"])
        q_out = sum(P[i]["electric_charge_thirds"] for i in ch["outgoing_ids"])
        b_in = sum(bnum(i) for i in ch["incoming_ids"])
        b_out = sum(bnum(i) for i in ch["outgoing_ids"])
        l_in = sum(lnum(i) for i in ch["incoming_ids"])
        l_out = sum(lnum(i) for i in ch["outgoing_ids"])
        flag = "" if (q_in == q_out and b_in == b_out and l_in == l_out) else "  <-- IMBALANCE"
        print(
            f"{ch['id']:45s} Q {q_in:>3}->{q_out:<3} B {str(b_in):>4}->{str(b_out):<4} "
            f"L {l_in:>2}->{l_out:<2}{flag}".rstrip()
        )
    # 2. antiparticle reciprocity and conjugate charges
    print()
    for i, e in P.items():
        a = e["antiparticle_id"]
        assert P[a]["antiparticle_id"] == i, i
        assert P[a]["electric_charge_thirds"] == -e["electric_charge_thirds"], i
        assert P[a]["twice_spin"] == e["twice_spin"], i
    print(f"reciprocity, conjugate charge and equal spin OK for {len(P)} records")
    # 3. mass consistency across files
    pc = json.loads(CONTRACTS.read_text(encoding="utf-8"))["entities"]
    me = Decimal(P["electron"]["physical_properties"]["mass"]["value_decimal"])
    for n in ["proton", "neutron", "muon"]:
        ratio = Decimal(P[n]["physical_properties"]["mass"]["value_decimal"]) / me * 1000
        if P[n]["physical_properties"]["mass"]["unit"] != "MeV/c2":
            ratio = None
        print(
            n,
            "particle-contracts mass",
            pc[n]["mass"],
            "catalog-derived ratio*1000 =",
            round(ratio, 2) if ratio else ratio,
            "diff",
            (pc[n]["mass"] - ratio) if ratio else None,
        )
    print(
        "alpha in particle-contracts:",
        pc["alpha"],
        "; alpha in catalog:",
        "alpha" in P,
        "; helium nucleus record in catalog:",
        any("helium" in json.dumps(x).lower() for x in c["disturbance_families"]),
    )
    # 4. catalog-contact keV rounding losses
    for n in ["electron", "proton", "neutron", "muon", "tau", "up_quark", "top_quark", "higgs_boson"]:
        m = P[n]["physical_properties"]["mass"]
        v = Decimal(m["value_decimal"])
        u = m["unit"]
        kev = v * (1000 if u == "MeV/c2" else 1000000 if u == "GeV/c2" else Decimal("0.001"))
        print(
            f"{n:12s} catalog {v} {u} -> keV {kev} -> encoded {int(kev.to_integral_value())} "
            f"loss {kev - int(kev.to_integral_value())} keV; catalog uncertainty {m.get('uncertainty_decimal')} {u}"
        )
    # 5. which particles have magnetic moment / lifetime / width measured
    print()
    for k in ["magnetic_moment", "lifetime", "decay_width", "mass"]:
        st: dict[str, list[str]] = {}
        for i, e in P.items():
            p = e["physical_properties"].get(k)
            st.setdefault(p["status"] if p else "ABSENT", []).append(i)
        print(k, {s: len(v) for s, v in st.items()})
        if k == "magnetic_moment":
            print("   absent:", st.get("ABSENT"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the report to this file instead of stdout")
    args = parser.parse_args()
    if args.output is None:
        checks()
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle, contextlib.redirect_stdout(handle):
        checks()


if __name__ == "__main__":
    main()
