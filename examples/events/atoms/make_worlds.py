"""Write the two worlds of the atoms series under form B (the model owner's
word of 2026-09-21, record 333, "it is important to show one atom or two, to
close all the corners"; the Boss's order): hydrogen at r = 12, the one
registered radius of series H with a whole closure (j = 4.01, DERIVATIONS_BEAM
7.2), and helium, the alpha of binding-v1 (series I's registered square) as the
nucleus with two electrons of the register's electron. Both are series H's
base (`../bohr/make_worlds.py`, whose fan, flux count and orbit arithmetic this
generator imports) with the momentum derived under form B's drive
(light_speed/FORM.md section 3: a body's pace on an axis n / (Q S + n T_D / Q)
in place of the per-axis n / (Q S + n), n = p / M_e, T_D / Q = 110 / 64;
since 2026-09-22 the line drive, the law's drive of a body, the model
owner's record 972, docs/designs/drive_b/DEFAULT.md: the same integers as
series H's generator now derives, `bohr/make_worlds.py` under LINE_DRIVE), the
action re-fixed by series H's own rule (h = 16 p(8) under the same drive), a
`wave` detector at the nucleus, and, in helium, the electrons' mutual push
(each electron releases on the fan's band |c| <= 2) with the nucleus fixed as the proton
of series H is (one world has one width: the electron's 45120 would throw the
square's nucleons at nearly c, and the square disperses by tick 538 in its own
base, series I). Every derived number is a GAMEBOARD reading of the design
(the host's view of the mechanism); the pins are in
docs/designs/atoms/PINS.md, printed by docs/designs/atoms/atoms_map.py. No run
is made here.

    python examples/events/atoms/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402


def _bohr_generator():
    """Series H's generator, imported from its file (one source of the fan,
    the flux count and the orbit's arithmetic)."""
    spec = importlib.util.spec_from_file_location(
        "bohr_make_worlds", HERE.parent / "bohr" / "make_worlds.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BOHR = _bohr_generator()
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

K, N, Q = BOHR.K, BOHR.N, BOHR.Q
ELECTRON, PROTON, RATIO, SHELL = BOHR.ELECTRON, BOHR.PROTON, BOHR.RATIO, BOHR.SHELL
WIDTH = 45120  # series H's registered width (v = 0.06 at r = 8 under the per-axis drive of history)
RADIUS = 12
REFERENCE_RADIUS, REFERENCE_J = BOHR.REFERENCE_RADIUS, BOHR.REFERENCE_J
T_D_AXIS = math.isqrt(3 * Q * Q)  # 110: the axis direction's period constant
PACE = T_D_AXIS / Q  # form B's second wall term per unit of n on an axis, 110 / 64
C_ROWS = 1 / math.sqrt(3)  # the rows' Euclidean pace, Links per interval
TURNS = 5
# The nucleus of helium: binding-v1's square (examples/events/binding/
# alpha_square_bond.json), the proton's charge 4 and its held content as
# registered, fixed; the four Nodes about the centre c.
NUCLEUS_CHARGE_P = 4
NUCLEUS = (
    ((0, 0, 0), "p", 1834),
    ((1, 0, 0), "n", 1837),
    ((0, 1, 0), "n", 1837),
    ((1, 1, 0), "p", 1834),
)
HELD = {"nuclear": 1, "bond": 2}
# The electrons of helium release on the fan's band |c| <= ELECTRON_BAND (with
# the four in-plane headings): every line of the fan that reaches the partner's
# three Nodes at 2r lies in it, and no ray of the band steps from one Node of
# the electron's own set into another (a whole-fan release would send the
# near-z lines of the outer Nodes through the middle Node).
ELECTRON_BAND = 2
# The two electrons, point-symmetric about the square's centre (c + 1/2, c + 1/2, c).
ELECTRON_OFFSETS = ((13, 1, 0), (-12, 0, 0))
HELIUM_RADIUS = math.hypot(12.5, 0.5)
Json = dict[str, object]


def ring_flux(count: dict[tuple[int, int, int], int], radius: float) -> float:
    """E_body(r) for a real radius: the entries per shell the body's three
    Nodes (z = -1, 0, 1) receive, averaged over the ring r - 1/2 < |x| <= r + 1/2 of the plane z = 0."""
    span = int(radius) + 2
    ring = [
        (x, y)
        for x in range(-span, span + 1)
        for y in range(-span, span + 1)
        if radius - 0.5 < math.hypot(x, y) <= radius + 0.5
    ]
    total = sum(count.get((x, y, z), 0) for x, y in ring for z in (-1, 0, 1))
    return total / len(ring)


def node_flux(count: dict[tuple[int, int, int], int], offset: tuple[int, int, int]) -> int:
    """The entries per shell the body's three Nodes at `offset` from the source receive: exact at that place."""
    x, y, z = offset
    return sum(count.get((x, y, z + dz), 0) for dz in (-1, 0, 1))


def orbit_form_b(a: float, radius: float) -> dict[str, float]:
    """The circular orbit under form B's drive: n^2 / (Q S + PACE n) = A, the
    real root, the whole momentum p = M_e n, the pace, the period."""
    reach = Q * WIDTH
    n = (PACE * a + math.sqrt((PACE * a) ** 2 + 4 * reach * a)) / 2
    p = max(1, round(n * ELECTRON))
    speed = n / (reach + PACE * n)
    period = 2 * math.pi * radius / speed
    return {"A": a, "n": n, "p": p, "speed": speed, "period": period, "beta": speed / C_ROWS}


def derive() -> dict[str, object]:
    """Everything the two worlds declare and the pins are read from."""
    directions = BOHR.fan(BOHR.FAN_LOW, BOHR.FAN_HIGH)
    count = BOHR.entries_per_node(directions, 2 * RADIUS + 4)
    # Hydrogen: series H's flux at r = 12 and at the reference radius, the orbit under form B, the action re-fixed.
    flux = {r: BOHR.body_flux(count, r) for r in (REFERENCE_RADIUS, RADIUS)}
    hydrogen = {
        r: orbit_form_b((1 + RATIO) * Q * flux[r] * r / SHELL, r) for r in (REFERENCE_RADIUS, RADIUS)
    }
    action = 4 * int(hydrogen[REFERENCE_RADIUS]["p"]) * REFERENCE_RADIUS // REFERENCE_J
    # Helium: the nucleus's four sources and the partner electron, exact at the start Nodes and on the ring.
    e1 = ELECTRON_OFFSETS[0]
    products = {"p": abs(-RATIO * NUCLEUS_CHARGE_P - 1), "n": 1}  # |rho_e rho_k - 1|: 61 and 1, inward
    repulsion = RATIO * RATIO - 1  # rho_e^2 - 1 = 224, outward
    start_inward = 0.0
    for offset, family, _amount in NUCLEUS:
        d = (e1[0] - offset[0], e1[1] - offset[1], e1[2] - offset[2])
        dist = math.hypot(d[0], d[1])
        radial = (d[0] * 12.5 + d[1] * 0.5) / (
            dist * HELIUM_RADIUS
        )  # the cosine to the centre's direction
        start_inward += products[family] * node_flux(count, d) * radial
    partner = (e1[0] - ELECTRON_OFFSETS[1][0], e1[1] - ELECTRON_OFFSETS[1][1], 0)
    start_partner = node_flux(count, partner)
    band = band_directions(directions)
    band_count = BOHR.entries_per_node(band, 2 * RADIUS + 4)
    start_partner_band = node_flux(band_count, partner)
    ring_nucleus = sum(products[f] for _o, f, _a in NUCLEUS) * ring_flux(count, HELIUM_RADIUS)
    ring_partner = repulsion * ring_flux(count, 2 * HELIUM_RADIUS)
    helium = orbit_form_b(Q * HELIUM_RADIUS * (ring_nucleus - ring_partner) / SHELL, HELIUM_RADIUS)
    return {
        "directions": directions,
        "count": count,
        "flux": flux,
        "hydrogen": hydrogen,
        "action": action,
        "helium": {
            **helium,
            "radius": HELIUM_RADIUS,
            "start_inward": start_inward,
            "start_partner": start_partner,
            "start_partner_band": start_partner_band,
            "band_directions": len(band),
            "ring_nucleus": ring_nucleus,
            "ring_partner": ring_partner,
            "repulsion": repulsion,
            "products": products,
        },
    }


def ticks_for(period: float) -> int:
    return max(BOHR.LEAST_TICKS, int(math.ceil(TURNS * period / 100.0)) * 100)


def base(
    model_id: str, side: int, ticks: int, action: int, directions: list[tuple[int, int, int]]
) -> Json:
    declared = [list(v) for v in directions if v not in BOHR.HEADINGS]
    return {
        "law": "beam",
        "model_id": model_id,
        "shape": [side, side, side],
        "boundary": "open",
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": [1, PROTON * SHELL],
        "suspension": 0,
        "width": WIDTH,
        "action": action,
        "directions": declared,
    }


def whole_fan(directions: list[tuple[int, int, int]]) -> list[int]:
    declared = [v for v in directions if v not in BOHR.HEADINGS]
    return list(range(2, 8 + len(declared)))


def band_fan(directions: list[tuple[int, int, int]]) -> list[int]:
    """The table indices of the four in-plane headings and of the fan's
    directions with |c| <= ELECTRON_BAND, in the world's table order."""
    declared = [v for v in directions if v not in BOHR.HEADINGS]
    headings = [2 + BOHR.HEADINGS.index(tuple(h)) for h in BOHR.IN_PLANE]
    band = [8 + i for i, v in enumerate(declared) if abs(v[2]) <= ELECTRON_BAND]
    return headings + band


def band_directions(directions: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return [v for v in directions if abs(v[2]) <= ELECTRON_BAND]


def hydrogen_world(derived: dict[str, object]) -> Json:
    directions = derived["directions"]  # type: ignore[assignment]
    reading = derived["hydrogen"][RADIUS]  # type: ignore[index]
    side = BOHR.side_for(RADIUS)
    c = side // 2
    document = base(
        "rays-atoms-hydrogen-r12-form-b-v1",
        side,
        ticks_for(reading["period"]),
        int(derived["action"]),
        directions,
    )  # type: ignore[arg-type]
    document["families"] = [
        {"name": "p", "quantum": 0, "charge": [1, 1], "phase": False},
        {"name": "e", "quantum": 0, "charge": -RATIO, "phase": True},
    ]
    document["measured"] = [
        {
            "position": [c, c, c],
            "family": "p",
            "amount": PROTON,
            "fixed": True,
            "directions": whole_fan(directions),
        },  # type: ignore[arg-type]
        {
            "position": [c + RADIUS, c, c],
            "family": "e",
            "amount": ELECTRON,
            "phase": 0,
            "fixed": False,
            "momentum": [0, int(reading["p"]), 0],
            "span": list(BOHR.SPAN),
            "phase_by_momentum": True,
            "directions": BOHR.IN_PLANE,
        },
    ]
    # A detector names Nodes that carry a measured event (the validator's rule): the proton's Node.
    document["detectors"] = [
        {"name": "at_proton", "positions": [[c, c, c]], "threshold": 1, "reading": "wave"}
    ]
    return document


def helium_world(derived: dict[str, object]) -> Json:
    directions = derived["directions"]  # type: ignore[assignment]
    reading = derived["helium"]  # type: ignore[assignment]
    side = BOHR.side_for(RADIUS + 1)
    c = side // 2
    document = base(
        "rays-atoms-helium-r12-form-b-v1",
        side,
        ticks_for(reading["period"]),
        int(derived["action"]),
        directions,
    )  # type: ignore[arg-type]
    document["families"] = [
        {"name": "p", "quantum": 0, "charge": NUCLEUS_CHARGE_P, "phase": False},
        {"name": "n", "quantum": 0, "phase": False},
        {
            "name": "nuclear",
            "quantum": 0,
            "columns": {"strong": {"value": 10000, "sign": -1}},
            "lifetime": 3,
            "phase": False,
        },
        {"name": "bond", "quantum": 1, "lifetime": 3, "phase": False},
        {"name": "e", "quantum": 0, "charge": -RATIO, "phase": True},
    ]
    fan = whole_fan(directions)  # type: ignore[arg-type]
    measured: list[Json] = [
        {
            "position": [c + o[0], c + o[1], c + o[2]],
            "family": family,
            "amount": amount,
            "held": dict(HELD),
            "fixed": True,
            "directions": fan,
        }
        for o, family, amount in NUCLEUS
    ]
    p = int(reading["p"])
    for offset, sign in zip(ELECTRON_OFFSETS, (1, -1), strict=True):
        measured.append(
            {
                "position": [c + offset[0], c + offset[1], c + offset[2]],
                "family": "e",
                "amount": ELECTRON,
                "phase": 0,
                "fixed": False,
                "momentum": [0, sign * p, 0],
                "span": list(BOHR.SPAN),
                "phase_by_momentum": True,
                "directions": band_fan(directions),  # type: ignore[arg-type]
            }
        )
    document["measured"] = measured
    nodes = [[c + o[0], c + o[1], c + o[2]] for o, _f, _a in NUCLEUS]
    document["detectors"] = [
        {"name": "at_nucleus", "positions": nodes, "threshold": 1, "reading": "wave"}
    ]
    return document


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    derived = derive()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, builder in (("hydrogen_r12", hydrogen_world), ("helium_r12", helium_world)):
        document = families_by_definition(builder(derived), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
