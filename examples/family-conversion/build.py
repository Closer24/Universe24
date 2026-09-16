"""Energy-dependent conversion between catalog particle families on the N-to-M contract.

Five supplied laws, each an explicit named candidate declared between catalog
families through the generic N-to-M conversion (``participants`` -> ``outputs``)
and decided by the participants' energies:

* ``annihilation``: electron + positron -> photon + photon (2 -> 2).
* ``pair_production``: photon + photon -> electron + positron (2 -> 2), only above
  the declared energy threshold; below it the photons cross without reacting.
* ``compton``: photon + electron -> photon' + electron' (2 -> 2, same families out;
  an energy-dependent exchange with the integer Compton formula at a lattice angle).
* ``three_photon``: electron + positron -> photon + photon + photon (2 -> 3).
* ``four_body``: electron + positron + photon + photon, four rays through four
  Ports -> four photons (4 -> 4) in one joint transaction whose every output
  reads all four inputs.

The collinear variants of the last two send two products on one Port; they exist
only as controls of the product-Port veto and are expected to fail before commit.

Electron, positron and photon values are derived from the catalog with the
reference-unit authoring adapter: energy in keV, momentum in keV/c (one unit per
keV/c, so a photon has ``energy == |momentum|``), charge in thirds of the
positive elementary charge; the rest energy is the catalog mass encoded to the
nearest keV/c2 and identified with keV through c = 1. The binding of every rule
to catalog entity ids and interaction families is written to bindings.json.
The engine sees only generic operations; no physical name selects behavior.
Every rule is a supplied discrete kinematics, not a derived cross section.

    python examples/family-conversion/build.py --write
    python examples/family-conversion/build.py --run annihilation --output artifacts/family-conversion
    python examples/family-conversion/build.py --scale annihilation --pairs 16 --energy 10000000 --output artifacts/family-scale
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from event_universe.entity_catalog import resolve_property, validate_catalog
from event_universe.reference_units import encode_components

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CATALOG = ROOT / "examples/known-entities/catalog.json"
UNITS = ROOT / "examples/known-entities/physical-units.json"

ENTITIES = ("electron", "positron", "photon", "muon")
MASS_FIELD = {"components": 1, "units": "keV/c2", "scale": 1, "signed": False}
MASS_ERROR_BY_UNIT = {"eV/c2": "500", "MeV/c2": "0.0005", "GeV/c2": "0.0000005"}
FIELDS = [
    {"name": "energy", "components": 1, "units": "keV", "signed": False, "conserved": True},
    {"name": "momentum", "components": 3, "units": "keV/c", "signed": True, "conserved": True},
    {
        "name": "charge",
        "components": 1,
        "units": "one third of positive elementary charge",
        "signed": True,
        "conserved": True,
    },
]
FIELD_NAMES = [field["name"] for field in FIELDS]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def catalog_values() -> dict[str, dict]:
    """Encode charge and rest energy of each family from the catalog, with provenance."""
    catalog, registry = _load(CATALOG), _load(UNITS)
    validate_catalog(catalog)
    result = {}
    for identity in ENTITIES:
        charge = resolve_property(catalog, identity, "electric_charge")
        charge_encoding = encode_components(registry, charge["value_decimal"], charge["unit"], FIELDS[2])
        mass = resolve_property(catalog, identity, "mass")
        mass_encoding = encode_components(
            registry,
            mass["value_decimal"],
            mass["unit"],
            MASS_FIELD,
            max_error=MASS_ERROR_BY_UNIT[mass["unit"]],
        )
        result[identity] = {
            "catalog_id": identity,
            "charge": charge_encoding["value"],
            "rest_energy_keV": mass_encoding["value"],
            "charge_encoding": charge_encoding,
            "mass_encoding": mass_encoding,
            "mass_reference": mass,
        }
    return result


VALUES = catalog_values()
REST_ENERGY = VALUES["electron"]["rest_energy_keV"]
"""Electron rest energy in keV: catalog mass encoded to the nearest keV/c2, c = 1."""
PAIR_THRESHOLD = 2 * REST_ENERGY
"""Declared pair-production threshold on the total photon energy, keV."""
ELECTRON_CHARGE = VALUES["electron"]["charge"]
POSITRON_CHARGE = VALUES["positron"]["charge"]
MUON_REST_ENERGY = VALUES["muon"]["rest_energy_keV"]
"""Muon rest energy in keV; the muon is a spectator family in the Port control only."""
assert VALUES["positron"]["rest_energy_keV"] == REST_ENERGY
assert VALUES["photon"]["rest_energy_keV"] == 0 and VALUES["photon"]["charge"] == 0

SHAPE = [17, 7, 7]
CENTER = 3
LEFT_X, RIGHT_X = 2, 14
MEETING_X = 8
NORMAL_BUDGET = 100_000_000
"""Cycle budget above the rational-projection tariff so a conversion adds no delay."""

# The lattice offers six port directions; relative to an incoming direction their
# cosines are exact: forward +1, the four transverse directions 0, backward -1.
# No fixed-point approximation is needed for these rows; oblique angles are not
# lattice directions and are not used.
LATTICE_COSINES = {"forward": 1, "transverse": 0, "backward": -1}
# Transverse direction: the right-hand cyclic successor of the axis,
# +X -> +Y, +Y -> +Z, +Z -> +X (negative directions map to their negatives).
TRANSVERSE_MATRIX = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]

MODEL_IDS = {
    "annihilation": "family-conversion-annihilation-v1",
    "pair_production": "family-conversion-pair-production-v1",
    "compton": "family-conversion-compton-v1",
    "three_photon": "family-conversion-three-photon-v1",
    "four_body": "family-conversion-four-body-v1",
    "three_photon_collinear": "family-conversion-three-photon-collinear-v1",
    "four_body_collinear": "family-conversion-four-body-collinear-v1",
}
BINDINGS = {
    "annihilation": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": "electron_positron_two_photon_annihilation",
        "participants": ["electron", "positron"],
        "outputs": ["photon", "photon"],
    },
    "pair_production": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": "two_photon_pair_creation",
        "participants": ["photon", "photon"],
        "outputs": ["electron", "positron"],
    },
    "compton": {
        "interaction_family": "electromagnetic_scattering",
        "representative_channel": "compton_scattering",
        "participants": ["photon", "electron"],
        "outputs": ["photon", "electron"],
    },
    "three_photon": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": None,
        "participants": ["electron", "positron"],
        "outputs": ["photon", "photon", "photon"],
        "note": "The catalog lists the two-photon channel only; the three-photon channel is the supplied 2 -> 3 candidate.",
    },
    "four_body": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": None,
        "participants": ["electron", "positron", "photon", "photon"],
        "outputs": ["photon", "photon", "photon", "photon"],
        "note": "A supplied joint four-ray kinematics between catalog families; the catalog has no four-body channel. The muon is a catalog spectator family that no rule selects.",
    },
    "three_photon_collinear": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": None,
        "participants": ["electron", "positron"],
        "outputs": ["photon", "photon", "photon"],
        "note": "Control only: two forward photons on one Port; the product-Port veto rejects the cycle before commit.",
    },
    "four_body_collinear": {
        "interaction_family": "pair_creation_annihilation",
        "representative_channel": None,
        "participants": ["electron", "positron", "photon", "photon"],
        "outputs": ["photon", "photon", "photon", "photon"],
        "note": "Control only: four photons on the lepton axis, two per Port; the product-Port veto rejects the cycle before commit.",
    },
}


def op(name: str, *args: object) -> dict:
    return {"op": name, "args": list(args)}


def pin(index: int, name: str) -> dict:
    return {"field": name, "participant": index}


def l1(vector: dict) -> dict:
    return op("sum", op("abs", vector))


def axis_aligned(vector: dict) -> dict:
    """1 when at most one component is nonzero (the zero vector included).

    dot(v, v) equals |v|_1 squared exactly when no two components are both nonzero.
    """
    return op("eq", op("dot", vector, vector), op("mul", l1(vector), l1(vector)))


def parallel(first: dict, second: dict) -> dict:
    return op("eq", l1(op("cross", first, second)), 0)


def all_of(*conditions: dict) -> dict:
    result = conditions[0]
    for condition in conditions[1:]:
        result = op("mul", result, condition)
    return result


def on_shell_photon(index: int) -> dict:
    return op("eq", pin(index, "energy"), l1(pin(index, "momentum")))


def total(name: str) -> dict:
    return op("add", pin(0, name), pin(1, name))


def invariants() -> list[dict]:
    """Per-record readouts summed over all inputs and all outputs."""
    return [{"name": name, "expression": {"field": name}} for name in FIELD_NAMES]


def assign(output: int, field: str, expression: object) -> dict:
    return {"output": output, "field": field, "expression": expression}


def transport() -> dict:
    """One Link per tick along the reduced lattice direction of the momentum.

    A zero momentum holds. The direction is the momentum divided by the gcd of
    its components, so an axis-aligned momentum gives unit port weights whose
    cyclic phase stays zero; the conversion contract rejects any carried
    routing phase, and the raw momentum as weights would advance it every hop.
    This is a declared transport rule, not the physical speed |p|/E: a
    fractional rate would also carry state that the conversion contract rejects.
    """
    return {
        "mode": "move",
        "direction": op("rational_direction", op("ratio", {"field": "momentum"}, 1)),
        "rate": 1,
        "rate_denominator": 1,
    }


def families() -> list[dict]:
    lepton_check = [
        {"name": "rest_energy_bound", "expression": op("gt", {"field": "energy"}, REST_ENERGY - 1)}
    ]
    photon_check = [
        {
            "name": "energy_bounds_momentum",
            "expression": op("gt", op("add", {"field": "energy"}, 1), l1({"field": "momentum"})),
        }
    ]
    muon_check = [
        {
            "name": "rest_energy_bound",
            "expression": op("gt", {"field": "energy"}, MUON_REST_ENERGY - 1),
        }
    ]
    return [
        {
            "name": "electron",
            "fields": FIELD_NAMES,
            "defaults": {"energy": REST_ENERGY, "momentum": [0, 0, 0], "charge": ELECTRON_CHARGE},
            "transport": transport(),
            "checks": lepton_check,
        },
        {
            "name": "positron",
            "fields": FIELD_NAMES,
            "defaults": {"energy": REST_ENERGY, "momentum": [0, 0, 0], "charge": POSITRON_CHARGE},
            "transport": transport(),
            "checks": lepton_check,
        },
        {
            "name": "photon",
            "fields": FIELD_NAMES,
            "defaults": {"energy": 0, "momentum": [0, 0, 0], "charge": 0},
            "transport": transport(),
            "checks": photon_check,
        },
        {
            "name": "muon",
            "fields": FIELD_NAMES,
            "defaults": {
                "energy": MUON_REST_ENERGY,
                "momentum": [0, 0, 0],
                "charge": VALUES["muon"]["charge"],
            },
            "transport": transport(),
            "checks": muon_check,
        },
    ]


def collision_axis() -> dict:
    """Unit lattice vector along p_0 - p_1; +X when both are at rest."""
    relative = op("sub", pin(0, "momentum"), pin(1, "momentum"))
    at_rest = op("sub", 1, op("gt", l1(relative), 0))
    padded = op("add", relative, op("mul", at_rest, [1, 0, 0]))
    # |padded| = |relative| + at_rest, written as a scalar to stay within depth 16.
    return op("exact_div", padded, op("add", l1(relative), at_rest))


def annihilation_rule() -> dict:
    """e- + e+ -> photon (+u) + photon (-u), u the collision axis.

    Discrete kinematics: E_a = whole((E + P.u) / 2) and p_a = whole((E u + P) / 2)
    with truncation toward zero, so E_a = |p_a|; E_b = E - E_a, p_b = P - p_a.
    Totals are exact. When E + P.u is odd, the indivisible unit stays as energy
    of photon b, whose energy then exceeds |p_b| by one unit; nothing is dropped.
    """
    axis = collision_axis()
    energy = total("energy")
    momentum = total("momentum")
    photon_a = op("rational_whole", op("ratio", op("add", op("mul", energy, axis), momentum), 2))
    energy_a = op("rational_whole", op("ratio", op("add", energy, op("dot", momentum, axis)), 2))
    return {
        "name": "annihilation",
        "participants": [{"type": "electron"}, {"type": "positron"}],
        "outputs": [{"type": "photon"}, {"type": "photon"}],
        "when": all_of(
            parallel(pin(0, "momentum"), pin(1, "momentum")),
            axis_aligned(pin(0, "momentum")),
            axis_aligned(pin(1, "momentum")),
        ),
        "assignments": [
            assign(0, "energy", energy_a),
            assign(0, "momentum", photon_a),
            assign(0, "charge", 0),
            assign(1, "energy", op("sub", energy, energy_a)),
            assign(1, "momentum", op("sub", momentum, photon_a)),
            assign(1, "charge", 0),
        ],
        "invariants": invariants(),
    }


def pair_production_rule() -> dict:
    """photon + photon -> e- + e+ above the declared threshold.

    Guard: head-on photons on one lattice axis, each on shell, total energy
    >= 1022 keV and E1 * E2 >= 511^2 (the invariant-mass condition for head-on
    photons; equal to the total-energy threshold for equal energies).
    Discrete kinematics: the pair shares energy and momentum equally,
    E_e = floor(E / 2), p_e = whole(P / 2); the positron owns any odd unit.
    Exactly on shell at threshold; above it the excess is lepton energy at rest
    in the pair frame. A physical pair would carry |p| = sqrt(E_e^2 - m^2).
    """
    energy = total("energy")
    momentum = total("momentum")
    electron_energy = op("rational_floor", op("ratio", energy, 2))
    electron_momentum = op("rational_whole", op("ratio", momentum, 2))
    return {
        "name": "pair_production",
        "participants": [{"type": "photon"}, {"type": "photon"}],
        "outputs": [{"type": "electron"}, {"type": "positron"}],
        "when": all_of(
            op("gt", energy, PAIR_THRESHOLD - 1),
            op("gt", op("mul", pin(0, "energy"), pin(1, "energy")), REST_ENERGY * REST_ENERGY - 1),
            parallel(pin(0, "momentum"), pin(1, "momentum")),
            op("gt", op("add", l1(pin(0, "momentum")), l1(pin(1, "momentum"))), l1(momentum)),
            axis_aligned(pin(0, "momentum")),
            on_shell_photon(0),
            on_shell_photon(1),
        ),
        "assignments": [
            assign(0, "energy", electron_energy),
            assign(0, "momentum", electron_momentum),
            assign(0, "charge", ELECTRON_CHARGE),
            assign(1, "energy", op("sub", energy, electron_energy)),
            assign(1, "momentum", op("sub", momentum, electron_momentum)),
            assign(1, "charge", POSITRON_CHARGE),
        ],
        "invariants": invariants(),
    }


def compton_rule() -> dict:
    """photon + electron at rest -> photon' (transverse) + electron' (recoil).

    E' = floor(E m / (m + E (1 - cos theta))) with cos theta = 0 for the
    transverse lattice row, m the rest energy read as the energy of the
    target at rest. The electron owns the remainder as recoil energy:
    E_e' = E + m - E', p_e' = p - p'. Exact energy and momentum totals. One
    joint transaction at the shared Node; no Node-owned intermediate hold.
    """
    rest = pin(1, "energy")
    incoming = pin(0, "energy")
    scattered = op(
        "rational_floor",
        op(
            "ratio",
            op("mul", incoming, rest),
            op("add", rest, op("mul", incoming, 1 - LATTICE_COSINES["transverse"])),
        ),
    )
    heading = op("exact_div", pin(0, "momentum"), incoming)
    direction = {"op": "transform", "args": [heading], "matrix": TRANSVERSE_MATRIX}
    scattered_momentum = op("mul", direction, scattered)
    return {
        "name": "compton",
        "participants": [{"type": "photon"}, {"type": "electron"}],
        "outputs": [{"type": "photon"}, {"type": "electron"}],
        "when": all_of(
            op("gt", incoming, 0),
            op("eq", l1(pin(1, "momentum")), 0),
            axis_aligned(pin(0, "momentum")),
            on_shell_photon(0),
        ),
        "assignments": [
            assign(0, "energy", scattered),
            assign(0, "momentum", scattered_momentum),
            assign(0, "charge", 0),
            assign(1, "energy", op("sub", total("energy"), scattered)),
            assign(1, "momentum", op("sub", pin(0, "momentum"), scattered_momentum)),
            assign(1, "charge", pin(1, "charge")),
        ],
        "invariants": invariants(),
    }


def three_photon_collinear_rule() -> dict:
    """Control variant of the 2 -> 3 rule: three photons on the collision axis.

    E_f = floor((E + |P|) / 2) is shared by two forward photons along +u,
    E_a = floor(E_f / 2) and E_b = E_f - E_a; the backward photon takes
    E_c = E - E_f with p_c = P - E_f u. Totals are exact, but two products leave
    on +u, so the product-Port veto must reject the cycle before commit.
    """
    energy = total("energy")
    momentum = total("momentum")
    net = l1(momentum)
    axis = op("exact_div", momentum, net)
    forward = op("rational_floor", op("ratio", op("add", energy, net), 2))
    first = op("rational_floor", op("ratio", forward, 2))
    return {
        "name": "three_photon_collinear",
        "participants": [{"type": "electron"}, {"type": "positron"}],
        "outputs": [{"type": "photon"}, {"type": "photon"}, {"type": "photon"}],
        "when": all_of(
            parallel(pin(0, "momentum"), pin(1, "momentum")),
            axis_aligned(pin(0, "momentum")),
            axis_aligned(pin(1, "momentum")),
            op("gt", net, 0),
            op("gt", op("sub", energy, net), 1),
        ),
        "assignments": [
            assign(0, "energy", first),
            assign(0, "momentum", op("mul", axis, first)),
            assign(0, "charge", 0),
            assign(1, "energy", op("sub", forward, first)),
            assign(1, "momentum", op("mul", axis, op("sub", forward, first))),
            assign(1, "charge", 0),
            assign(2, "energy", op("sub", energy, forward)),
            assign(2, "momentum", op("sub", momentum, op("mul", axis, forward))),
            assign(2, "charge", 0),
        ],
        "invariants": invariants(),
    }


def three_photon_rule() -> dict:
    """e- + e+ with net momentum -> photon (along P) + photon (+v) + photon (-v).

    Discrete kinematics: photon c carries the whole momentum, E_c = |P|, p_c = P;
    the remaining energy E - |P| is shared by a back-to-back transverse pair
    along v, the right-hand successor of the axis: E_t = floor((E - |P|) / 2),
    p_a = +v E_t, p_b = -v E_t, E_b = E_t, and photon a owns any odd unit as
    energy above |p_a|. Three distinct Ports. Guard: momenta on one axis,
    |P| > 0 (P = 0 has no lattice three-photon solution on distinct Ports) and
    E - |P| >= 2 so every photon carries energy.
    """
    energy = total("energy")
    momentum = total("momentum")
    net = l1(momentum)
    axis = op("exact_div", momentum, net)
    transverse = {"op": "transform", "args": [axis], "matrix": TRANSVERSE_MATRIX}
    pair_energy = op("rational_floor", op("ratio", op("sub", energy, net), 2))
    photon_a = op("mul", transverse, pair_energy)
    return {
        "name": "three_photon_annihilation",
        "participants": [{"type": "electron"}, {"type": "positron"}],
        "outputs": [{"type": "photon"}, {"type": "photon"}, {"type": "photon"}],
        "when": all_of(
            parallel(pin(0, "momentum"), pin(1, "momentum")),
            axis_aligned(pin(0, "momentum")),
            axis_aligned(pin(1, "momentum")),
            op("gt", net, 0),
            op("gt", op("sub", energy, net), 1),
        ),
        "assignments": [
            assign(0, "energy", net),
            assign(0, "momentum", momentum),
            assign(0, "charge", 0),
            assign(1, "energy", op("sub", op("sub", energy, net), pair_energy)),
            assign(1, "momentum", photon_a),
            assign(1, "charge", 0),
            assign(2, "energy", pair_energy),
            assign(2, "momentum", op("neg", photon_a)),
            assign(2, "charge", 0),
        ],
        "invariants": invariants(),
    }


def four_body_rule() -> dict:
    """e- + e+ + photon + photon, four rays through four Ports -> four photons (4 -> 4).

    Guard: the leptons cancel each other's momentum, so do the photons, both
    pairs move on axis-aligned perpendicular axes u and w, hence P = 0. Discrete
    kinematics: the four energies pool into Q; H = floor(Q / 2), E_x = floor(H / 2),
    E_y = H - E_x; photons leave along +u and -u with E_x and along +w and -w
    with E_y; photon a (+u) owns the odd unit Q - 2H as energy above |p_a|.
    Every output depends on all four inputs, so the rule is not a product of
    two 2 -> 2 rules. One joint transaction, four distinct Ports.
    """
    energy = op(
        "add",
        op("add", pin(0, "energy"), pin(1, "energy")),
        op("add", pin(2, "energy"), pin(3, "energy")),
    )
    lepton_axis = op("exact_div", pin(0, "momentum"), l1(pin(0, "momentum")))
    photon_axis = op("exact_div", pin(2, "momentum"), l1(pin(2, "momentum")))
    half = op("rational_floor", op("ratio", energy, 2))
    along = op("rational_floor", op("ratio", half, 2))
    across = op("sub", half, along)
    odd = op("sub", energy, op("mul", half, 2))
    return {
        "name": "four_body",
        "participants": [
            {"type": "electron"},
            {"type": "positron"},
            {"type": "photon"},
            {"type": "photon"},
        ],
        "outputs": [{"type": "photon"}] * 4,
        "when": all_of(
            op("eq", l1(op("add", pin(0, "momentum"), pin(1, "momentum"))), 0),
            op("eq", l1(op("add", pin(2, "momentum"), pin(3, "momentum"))), 0),
            op("gt", l1(pin(0, "momentum")), 0),
            op("gt", l1(pin(2, "momentum")), 0),
            op("eq", op("dot", pin(0, "momentum"), pin(2, "momentum")), 0),
            axis_aligned(pin(0, "momentum")),
            axis_aligned(pin(2, "momentum")),
        ),
        "assignments": [
            assign(0, "energy", op("add", along, odd)),
            assign(0, "momentum", op("mul", lepton_axis, along)),
            assign(0, "charge", 0),
            assign(1, "energy", along),
            assign(1, "momentum", op("neg", op("mul", lepton_axis, along))),
            assign(1, "charge", 0),
            assign(2, "energy", across),
            assign(2, "momentum", op("mul", photon_axis, across)),
            assign(2, "charge", 0),
            assign(3, "energy", across),
            assign(3, "momentum", op("neg", op("mul", photon_axis, across))),
            assign(3, "charge", 0),
        ],
        "invariants": invariants(),
    }


def four_body_collinear_rule() -> dict:
    """Control variant of the 4 -> 4 rule: all four photons on the lepton axis.

    Same guard and pooled energy Q, H = floor(Q / 2), E_x = floor(H / 2); photons
    a and b leave along +u with E_x and H - E_x, photons c and d along -u with
    the same energies; photon a owns the odd unit. Totals are exact, but two
    products share each Port, so the product-Port veto must reject the cycle.
    """
    rule = four_body_rule()
    rule["name"] = "four_body_collinear"
    energy = op(
        "add",
        op("add", pin(0, "energy"), pin(1, "energy")),
        op("add", pin(2, "energy"), pin(3, "energy")),
    )
    lepton_axis = op("exact_div", pin(0, "momentum"), l1(pin(0, "momentum")))
    half = op("rational_floor", op("ratio", energy, 2))
    along = op("rational_floor", op("ratio", half, 2))
    rest = op("sub", half, along)
    odd = op("sub", energy, op("mul", half, 2))
    rule["assignments"] = [
        assign(0, "energy", op("add", along, odd)),
        assign(0, "momentum", op("mul", lepton_axis, along)),
        assign(0, "charge", 0),
        assign(1, "energy", rest),
        assign(1, "momentum", op("mul", lepton_axis, rest)),
        assign(1, "charge", 0),
        assign(2, "energy", along),
        assign(2, "momentum", op("neg", op("mul", lepton_axis, along))),
        assign(2, "charge", 0),
        assign(3, "energy", rest),
        assign(3, "momentum", op("neg", op("mul", lepton_axis, rest))),
        assign(3, "charge", 0),
    ]
    return rule


RULES = {
    "annihilation": annihilation_rule,
    "pair_production": pair_production_rule,
    "compton": compton_rule,
    "three_photon": three_photon_rule,
    "four_body": four_body_rule,
    "three_photon_collinear": three_photon_collinear_rule,
    "four_body_collinear": four_body_collinear_rule,
}


def seed(kind: str, position: list[int], energy: int, momentum: list[int]) -> dict:
    return {"position": position, "type": kind, "values": {"energy": energy, "momentum": momentum}}


def configuration(
    law: str,
    seeds: list[dict],
    *,
    shape: list[int] | None = None,
    ticks: int,
    slots: int = 4,
) -> dict:
    rules = [RULES[law]()]
    if law in ("four_body", "four_body_collinear"):
        # The declared fallback for fewer than four rays: the two-to-two rule.
        rules.append(annihilation_rule())
    return {
        "schema_version": 1,
        "model_id": MODEL_IDS[law],
        "boundary": "open",
        "shape": list(shape or SHAPE),
        "slots_per_node": slots,
        "link_ticks": 1,
        "normal_budget": NORMAL_BUDGET,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": FIELDS,
        "disturbance_types": families(),
        "interactions": rules,
        "conservation": {
            "name": "keV-energy-momentum-audit",
            "energy_units": "keV",
            "momentum_units": "keV/c",
            "carriers": [
                {
                    "requires": FIELD_NAMES,
                    "energy": {"field": "energy"},
                    "momentum": {"field": "momentum"},
                }
            ],
        },
        "seeds": seeds,
    }


def line(y: int = CENTER, z: int = CENTER) -> tuple[list[int], list[int], list[int]]:
    return [LEFT_X, y, z], [RIGHT_X, y, z], [MEETING_X, y, z]


def annihilation_fixture() -> dict:
    """On-shell e- (E 1825, p +1752) and e+ (E 1825, p -1752) meet head-on."""
    first, second, _ = line()
    return configuration(
        "annihilation",
        [seed("electron", first, 1825, [1752, 0, 0]), seed("positron", second, 1825, [-1752, 0, 0])],
        ticks=18,
    )


def pair_production_fixture(energy: int = REST_ENERGY) -> dict:
    """Two head-on photons of equal energy; 511 each is exactly the threshold."""
    first, second, _ = line()
    return configuration(
        "pair_production",
        [seed("photon", first, energy, [energy, 0, 0]), seed("photon", second, energy, [-energy, 0, 0])],
        ticks=18,
    )


def compton_fixture(energy: int = REST_ENERGY) -> dict:
    """A photon of the given energy meets an electron at rest."""
    first, _, target = line()
    return configuration(
        "compton",
        [
            seed("photon", first, energy, [energy, 0, 0]),
            seed("electron", target, REST_ENERGY, [0, 0, 0]),
        ],
        ticks=24,
    )


def three_photon_fixture(*, slots: int = 4, spectator: bool = False, collinear: bool = False) -> dict:
    """An on-shell e- (E 1825, p +1752) meets a resting e+; net momentum 1752.

    ``slots=2`` is the capacity control: the third photon has no free slot.
    ``collinear`` is the Port control: the collinear variant sends two products
    on +X. ``spectator`` adds a photon that arrives at the meeting Node in the
    same tick and leaves on +Y, the Port of a transverse product; ordinary
    transport admits it beside the product.
    """
    shape = [17, 13, 7] if spectator else SHAPE
    center = 6 if spectator else CENTER
    first, _, target = line(y=center)
    seeds = [
        seed("electron", first, 1825, [1752, 0, 0]),
        seed("positron", target, REST_ENERGY, [0, 0, 0]),
    ]
    if spectator:
        seeds.append(seed("photon", [MEETING_X, 0, CENTER], 100, [0, 100, 0]))
    law = "three_photon_collinear" if collinear else "three_photon"
    return configuration(law, seeds, shape=shape, ticks=18, slots=slots)


def four_body_fixture(*, arrivals: int = 4, collinear: bool = False, spectator: bool = False) -> dict:
    """Four rays meet at (8, 6, 3) at tick 6 through four Ports on a 17 x 13 x 7 world.

    ``arrivals=3`` omits the -Y photon: the 4 -> 4 rule cannot fire and the
    declared 2 -> 2 annihilation acts instead. ``collinear`` is the Port control:
    the collinear variant sends two products on each of +X and -X. ``spectator``
    adds a catalog muon arriving with the positron and leaving on -X beside a
    product; ordinary transport admits it.
    """
    center = 6
    seeds = [
        seed("electron", [LEFT_X, center, CENTER], 1825, [1752, 0, 0]),
        seed("positron", [RIGHT_X, center, CENTER], 1825, [-1752, 0, 0]),
        seed("photon", [MEETING_X, 0, CENTER], 300, [0, 300, 0]),
    ]
    if arrivals == 4:
        seeds.append(seed("photon", [MEETING_X, 12, CENTER], 300, [0, -300, 0]))
    if spectator:
        seeds.append(seed("muon", [RIGHT_X, center, CENTER], MUON_REST_ENERGY, [-100, 0, 0]))
    law = "four_body_collinear" if collinear else "four_body"
    return configuration(law, seeds, shape=[17, 13, 7], ticks=18, slots=6)


FIXTURES = {
    "annihilation": annihilation_fixture,
    "pair-production": pair_production_fixture,
    "pair-production-control": lambda: pair_production_fixture(500),
    "compton": compton_fixture,
    "three-photon": three_photon_fixture,
    "three-photon-capacity-control": lambda: three_photon_fixture(slots=2),
    "three-photon-port-control": lambda: three_photon_fixture(collinear=True),
    "four-body": four_body_fixture,
    "four-body-three-arrive-control": lambda: four_body_fixture(arrivals=3),
    "four-body-port-control": lambda: four_body_fixture(collinear=True),
}


def scale_seeds(law: str, pairs: int, energy: int, shape: list[int]) -> list[dict]:
    """Distinct head-on pairs along X, one per (y, z) line, energies stepping up to `energy`."""
    seeds = []
    # An even separation is required: records that hop one Link per tick from
    # an odd separation swap Nodes without ever being co-resident.
    first_x = 2
    last_x = first_x + 2 * ((shape[0] - 3 - first_x) // 2)
    for index in range(pairs):
        y, z = 3 + 2 * (index % 8), 3 + 2 * (index // 8)
        share = energy * (index + 1) // pairs
        first, second = [first_x, y, z], [last_x, y, z]
        target = [(first_x + last_x) // 2, y, z]
        if law == "annihilation":
            # Ultrarelativistic on-shell to within the keV unit: p = E - 1.
            seeds += [
                seed("electron", first, share, [share - 1, 0, 0]),
                seed("positron", second, share, [-(share - 1), 0, 0]),
            ]
        elif law == "pair_production":
            half = max(share // 2, REST_ENERGY)
            seeds += [
                seed("photon", first, half, [half, 0, 0]),
                seed("photon", second, half, [-half, 0, 0]),
            ]
        elif law == "three_photon":
            seeds += [
                seed("electron", first, share, [share - 1, 0, 0]),
                seed("positron", target, REST_ENERGY, [0, 0, 0]),
            ]
        elif law == "four_body":
            # Quadruples on distinct z lines: leptons along X, photons along Y,
            # all four arriving at the meeting Node in the same tick.
            reach = (last_x - first_x) // 2
            y, z = shape[1] // 2, 3 + 2 * index
            quarter = max(share // 4, 1)
            seeds = seeds[: 4 * index] + [
                seed("electron", [first_x, y, z], share, [share - 1, 0, 0]),
                seed("positron", [last_x, y, z], share, [-(share - 1), 0, 0]),
                seed("photon", [target[0], y - reach, z], quarter, [0, quarter, 0]),
                seed("photon", [target[0], y + reach, z], quarter, [0, -quarter, 0]),
            ]
        else:
            seeds += [
                seed("photon", first, share, [share, 0, 0]),
                seed("electron", target, REST_ENERGY, [0, 0, 0]),
            ]
    return seeds


def scale_configuration(law: str, pairs: int, energy: int, size: int, ticks: int) -> dict:
    shape = [size, size, size]
    return configuration(law, scale_seeds(law, pairs, energy, shape), shape=shape, ticks=ticks)


def bindings() -> dict:
    """Catalog provenance of every family value and the family each rule is declared between."""
    return {
        "catalog": CATALOG.relative_to(ROOT).as_posix(),
        "units": UNITS.relative_to(ROOT).as_posix(),
        "conversion_contract": "family-conversion-n-to-m-v1",
        "identification": "rest energy in keV = catalog mass encoded to the nearest keV/c2 with c = 1; momentum unit keV/c",
        "rest_energy_keV": REST_ENERGY,
        "pair_threshold_keV": PAIR_THRESHOLD,
        "entities": VALUES,
        "rules": {law: {"model_id": MODEL_IDS[law], **BINDINGS[law]} for law in RULES},
        "exclusions": [
            "No nucleus, bound state or binding energy is represented: pair production uses the two-photon channel.",
            "The catalog photon has no energy property; the shared energy/momentum layout is the representation supplied here.",
        ],
    }


def write_fixtures() -> list[Path]:
    paths = []
    for name, build in FIXTURES.items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(build(), indent=2) + "\n", encoding="utf-8")
        paths.append(path)
    path = HERE / "bindings.json"
    path.write_text(json.dumps(bindings(), indent=2) + "\n", encoding="utf-8")
    paths.append(path)
    return paths


def run(path: Path, output: Path) -> None:
    shutil.rmtree(output, ignore_errors=True)
    subprocess.run(
        [sys.executable, "-m", "event_universe", "--init", str(path), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="Regenerate the checked-in fixtures")
    parser.add_argument("--run", choices=sorted(FIXTURES), help="Run one checked-in fixture")
    parser.add_argument("--scale", choices=sorted(RULES), help="Build and run a larger world")
    parser.add_argument("--pairs", type=int, default=16)
    parser.add_argument("--energy", type=int, default=10_000_000, help="Largest pair energy, keV")
    parser.add_argument("--size", type=int, default=48)
    parser.add_argument("--ticks", type=int, default=64)
    parser.add_argument("--output", default="artifacts/family-conversion")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if args.write:
        for path in write_fixtures():
            print(path)
    if args.run:
        run(HERE / f"{args.run}.json", output)
        print(output)
    if args.scale:
        config = scale_configuration(args.scale, args.pairs, args.energy, args.size, args.ticks)
        output.parent.mkdir(parents=True, exist_ok=True)
        path = output.parent / f"{output.name}-{args.scale}-input.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        run(path, output)
        print(path, "->", output)


if __name__ == "__main__":
    main()
