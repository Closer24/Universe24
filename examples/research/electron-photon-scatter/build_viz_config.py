"""Authoring script (exploration lane): catalog electron meets a directional quantum stream.

Run:  PYTHONPATH=src python examples/research/electron-photon-scatter/build_viz_config.py --output DIR

Derives the initialization from the checked-in radiation-scattering adapter
(examples/radiation-scattering/build.py: configuration()) and binds the carrier's
charge and mass to the entity catalog through the shared reference-unit encoder,
exactly as examples/catalog-contact/prepare.py does. Adds one outward
`electric_signal` field emitted by the carrier (the causal_charge.json halo
pattern, restricted to what schema 1 supports: conservative outward transport,
no attenuation law). Nothing in the engine is touched.

Everything physical in this file is either catalog data (charge, mass), a
supplied rule (presence marker, hold fraction presence*2, back-stream and
recoil assignment, outward halo emission) or an exact-accounting invariant
(quanta, total_momentum). No law is derived.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from event_universe.entity_catalog import resolve_property, validate_catalog
from event_universe.reference_units import encode_components

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_OUTPUT = ROOT / "artifacts" / "research" / "electron-photon-scatter"
BUILD = ROOT / "examples/radiation-scattering/build.py"
CATALOG = ROOT / "examples/known-entities/catalog.json"
UNITS = ROOT / "examples/known-entities/physical-units.json"

SHAPE = [17, 7, 7]
CENTER = 3
CARRIER_X = 8
SOURCE_X = 1  # six pulses at x = 1..6, i.e. 2..7 links from the electron
TICKS = 16
RATE_DENOMINATOR = 48  # electron hop rate = sum|p| / 48 per interval: supplied transport rule
HALO_PER_INTERVAL_FACTOR = 72  # electric_signal amount = charge * 72 = -216 per interval (charge_third units): 27 per octant, 9 per axis at the source


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


def build(halo: bool = True) -> tuple[dict, dict]:
    spec = importlib.util.spec_from_file_location("radiation_scattering_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    catalog, registry = load(CATALOG), load(UNITS)
    validate_catalog(catalog)
    charge_field = {"components": 1, "units": "charge_third", "scale": 1, "signed": True}
    mass_field = {"components": 1, "units": "keV/c2", "scale": 1, "signed": False}
    charge_ref = resolve_property(catalog, "electron", "electric_charge")
    mass_ref = resolve_property(catalog, "electron", "mass")
    charge_enc = encode_components(
        registry, charge_ref["value_decimal"], charge_ref["unit"], charge_field
    )
    mass_enc = encode_components(
        registry, mass_ref["value_decimal"], mass_ref["unit"], mass_field, max_error="0.0005"
    )
    charge_thirds = charge_enc["value"]
    mass_kev = mass_enc["value"]
    assert charge_thirds == -3 and mass_kev == 511, (charge_thirds, mass_kev)

    # The adapter's own configuration; its `charge` argument is only the type default,
    # which is replaced below by the catalog encoding.
    raw = module.configuration(charge_thirds, ticks=TICKS)
    raw["model_id"] = "viz-catalog-electron-directional-quanta-scattering-v1"
    raw["shape"] = SHAPE
    for field in raw["fields"]:
        if field["name"] == "charge":
            field.update(units="charge_third", scale=1)
        elif field["name"] == "mass":
            field.update(units="keV/c2", scale=1)
        elif field["name"] == "presence":
            field["units"] = "elementary charge squared"
    scatterer = raw["disturbance_types"][0]
    scatterer["name"] = "electron"  # a storage layout label; it selects no law
    scatterer["defaults"] = {"mass": mass_kev, "charge": charge_thirds, "momentum": [0, 0, 0]}
    # The electron is a moving ray: its own momentum is its travel direction; the hop rate
    # |p| / RATE_DENOMINATOR per interval is a SUPPLIED transport rule (no derived kinematics).
    scatterer["transport"] = {
        "mode": "move",
        "direction_field": "momentum",
        "rate": op("sum", op("abs", {"field": "momentum"})),
        "rate_denominator": RATE_DENOMINATOR,
    }
    # Family selection by carried properties (docs/PROPERTY_COUPLINGS.md), not by type name:
    # any layout carrying `charge` emits the markers; any layout carrying `charge` and
    # `momentum` takes part in the joint transaction with the radiation-quantum fields.
    for emission in raw["emissions"]:
        emission.pop("type")
        emission["requires"] = ["charge"]
    for rule in raw["spatial_interactions"]:
        rule.pop("type")
        rule["requires"] = ["charge", "momentum"]

    # Presence marker in e^2 so that the supplied hold fraction presence*2 keeps the
    # candidate's documented value (2 quanta per interval for |q| = 1 e). The catalog stores
    # thirds of e, so (q/3)^2 = exact_div(q*q, 9); exact for every catalog charge.
    for emission in raw["emissions"]:
        if emission["field"] == "presence":
            emission["amount"] = op("exact_div", op("mul", {"field": "charge"}, {"field": "charge"}), 9)

    raw["spatial_seeds"] = [
        {"position": [SOURCE_X + i, CENTER, CENTER], "field": "rad_px", "populations": [10] + [0] * 7}
        for i in range(6)
    ]
    raw["seeds"] = [{"position": [CARRIER_X, CENTER, CENTER], "type": "electron"}]

    if halo:
        raw["fields"].append(
            {
                "name": "electric_signal",
                "components": 1,
                "units": "retarded source unit",
                "signed": True,
                "conserved": True,
            }
        )
        raw["spatial_fields"].append({"field": "electric_signal", "baseline": 0, "transport": "outward"})
        raw["emissions"].append(
            {
                "requires": ["charge"],
                "field": "electric_signal",
                "amount": op("mul", {"field": "charge"}, HALO_PER_INTERVAL_FACTOR),
                "denominator": 1,
                "source": True,
            }
        )

    report = {
        "derived_from": str(BUILD.relative_to(ROOT)),
        "catalog": str(CATALOG.relative_to(ROOT)),
        "units": str(UNITS.relative_to(ROOT)),
        "entity": "electron",
        "charge_encoding": charge_enc,
        "mass_encoding": mass_enc,
        "mass_reference": mass_ref,
        "charge_reference": charge_ref,
        "supplied_rules": [
            "presence marker = exact_div(charge*charge, 9) per field interval (e^2); supplied, cleared each interval",
            "hold fraction min(rad_px, presence*2): supplied selection rule, not a cross section",
            "scatter_held_quanta: held quanta become rad_mx, carrier gains 2*held along +X: supplied assignment",
            "electric_signal halo: outward emission charge*72 = -216 per interval (schema 1: conservative outward, no attenuation law); a configured field, not a Coulomb law",
            "six pulses of 10 quanta pre-seeded at x=1..6 travelling +X: the configured 'photon' stream (radiation-quantum family: integer quanta, 1 momentum unit each, no charge, no mass, no energy register)",
            "electron transport: move along its own momentum at sum|p|/48 hops per interval: supplied transport rule, not derived kinematics",
            "family selection: emissions requires ['charge']; joint transaction requires ['charge','momentum'] (docs/PROPERTY_COUPLINGS.md), no type-name dispatch",
        ],
        "exact_consequences": [
            "quanta invariant on every rule and transaction",
            "total_momentum invariant (carrier momentum + direction-weighted quanta) on the joint transaction",
        ],
        "not_reproduced": [
            "photon energy/frequency shift (Compton formula)",
            "Klein-Nishina or any derived cross section",
            "relativistic kinematics; the 511 keV/c2 mass is inert inventory in this rule",
            "Coulomb 1/r^2 field; electric_signal is a configured outward signal only",
            "energy-family law: absent. No declared relation between the photon quanta's energy/momentum and the electron family's response; the hold fraction presence*2 is fixed",
        ],
        "dependencies_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (BUILD, CATALOG, UNITS)
        },
    }
    return raw, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-halo", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw, report = build(halo=not args.no_halo)
    stem = "electron-photon-scatter" + ("-nohalo" if args.no_halo else "")
    (args.output / f"{stem}.json").write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    (args.output / f"{stem}.bindings.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(args.output / f"{stem}.json")


if __name__ == "__main__":
    main()
