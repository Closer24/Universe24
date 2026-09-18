"""The catalog of nature (`catalog/nature.json`): the rays of nature and their
couplings as data on the one generic engine, and the two apparatus kinds, with
"undecided" wherever the model owner has not decided a value. The file parses
under the strict decoder with no float; every ray, coupling and apparatus record
carries its required keys and every reference resolves; every "undecided" names
the experiment or hypothesis that decides it and is listed in docs/CATALOG.md;
the register's confrontation entries and the catalog's agree; every ray a world
can select, the shadow set a family declares and every decided coupling the
engine runs today is built from the file into a minimal inline world, parsed and
run against pinned integers, an external body under each of its decided
couplings among them.

Under the law of the bit (Highlights 5.4, the model owner, 2026-09-18; the
cleanup of the same day, `cleanup-law-v1`): there is no field family, every ray
record is a family of things whose shadows are rays of the same family with the
bit 0, its shadow set the `release` it declares; light and the gluon are real
families; the phase circle is one for the world, N, and no record declares a
width; the electron's turn is a momentum table on its own family's shadows and
the recoil is the return of the law, no coupling.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Catalog of nature")
before the first run.
"""

import re
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, Ray
from event_universe.initialization import parse_initial_state
from event_universe.json_documents import parse_json_document

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog/nature.json"
JsonObject = dict[str, Any]
Lamp = tuple[tuple[int, int, int], str, int, int, int]
Shares = tuple[int, int, int, int, int, int]
UNDECIDED = "undecided"
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Every world of this module runs at the width of the reference Born table, 8 steps.
REFERENCE_BITS = 3
SECTIONS = {
    "schema",
    "date",
    "owner",
    "statement",
    "units",
    "rays",
    "couplings",
    "layers",
    "apparatus",
    "experiments",
}
RAY_KEYS = {"kind", "content", "clock", "charge", "release", "note"}
COUPLING_KEYS = {"status", "engine", "participants", "invariants", "note"}
# A coupling has outputs (a binding coupling among them, an outputs rule whose
# loop closes, loop-binding-v1), a momentum table (a thing pushed by shadows,
# bit-law-v1 point 16) or is the sink of an external body.
RESULT_KEYS = {"outputs", "momentum_table", "sink"}
APPARATUS_KEYS = {"world_key", "engine", "declaration", "does", "note"}
EXPERIMENT_KEYS = {"rays", "couplings", "apparatus", "note"}
# The rays a world can select today (a decided content), in catalog order, the
# families whose shadow set a world can declare today, and the couplings the
# engine runs today: a newly decided entry must join these lists and get a world.
RUNNABLE_RAYS = ["light", "electron", "positron", "gluon"]
RUNNABLE_RELEASES = ["electron", "positron"]
RUNNABLE_COUPLINGS = [
    "born_steering",
    "electron_field_turn",
    "absorber",
    "mirror",
    "phase_plate",
    "polarizer",
]
# The names a world writes into an external-body coupling of the catalog: the met
# family for "any" and "same", the body's family for "body", the offset for "setting".
BODY_NAMES: dict[str, str | int] = {"any": "light", "same": "light", "body": "apparatus", "setting": 3}
# The Born split of 16 quanta at phase difference d: the +Y and the -Y amounts.
STEERED = {0: (16, 0), 1: (14, 2), 2: (8, 8), 4: (0, 16)}
# The world's K for a family with a clock: the lamp's 5 quanta advance one step per
# interval (clock-readings-v1: content / K), 20 for the pushed electron below.
K = 5


def catalog() -> JsonObject:
    text = CATALOG.read_text(encoding="utf-8")
    assert text.endswith("\n") and not text.endswith("\n\n")
    document = parse_json_document(text)
    assert isinstance(document, dict) and not floats(document)
    return document


def floats(value: object) -> list[float]:
    if isinstance(value, float):
        return [value]
    items = value.values() if isinstance(value, dict) else value if isinstance(value, list) else []
    return [found for item in items for found in floats(item)]


def undecided(value: object, path: str = "") -> dict[str, list[object]]:
    """Every "undecided" in the tree by path, with the deciders its record names for it."""
    found: dict[str, list[object]] = {}
    if isinstance(value, dict):
        deciders = value.get("decided_by")
        for key, item in value.items():
            here = f"{path}.{key}" if path else key
            if item == UNDECIDED:
                named = deciders.get(key) if isinstance(deciders, dict) else deciders
                found[here] = named if isinstance(named, list) else [named]
            else:
                found.update(undecided(item, here))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            here = f"{path}[{index}]"
            if item == UNDECIDED:
                found[here] = [None]
            else:
                found.update(undecided(item, here))
    return found


def deciders() -> set[str]:
    """The names a decided_by may carry: an entry of the register, a hypothesis of the
    hypotheses page, or a feature of the ray-event model's migration list."""
    register = (ROOT / "docs/EXPERIMENTS.md").read_text(encoding="utf-8")
    hypotheses = (ROOT / "docs/HYPOTHESES.md").read_text(encoding="utf-8")
    model = (ROOT / "docs/RAY_EVENT_MODEL.md").read_text(encoding="utf-8")
    return (
        set(re.findall(r"^### ([AB]\d+)\. ", register, re.M))
        | {f"hypothesis {number}" for number in re.findall(r"^## (\d+)\. ", hypotheses, re.M)}
        | {f"feature {number}" for number in re.findall(r"\b[Ff]eature (\d+b?)\b", model)}
    )


def documented_undecided() -> dict[str, list[object]]:
    """The rows of the undecided table of docs/CATALOG.md: path to its deciders."""
    text = (ROOT / "docs/CATALOG.md").read_text(encoding="utf-8")
    section = text.split("## Undecided entries and what decides each", 1)[1].split("\n## ", 1)[0]
    return {
        path: [decider.strip() for decider in named.split(",")]
        for path, named in re.findall(r"^\| `([^`]+)` \| [^|]+ \| ([^|]+) \|$", section, re.M)
    }


def types_of(participant: JsonObject) -> list[str]:
    declared = participant["type"]
    return list(declared) if isinstance(declared, list) else [declared]


def scalar(name: str) -> JsonObject:
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def spatial_field(records: JsonObject, name: str, released: bool = False) -> JsonObject:
    """The world's `spatial_fields` entry for one catalog ray (the world runs at the
    reference width, N 8): its charge, its clock (a family with a clock declares `clock`, the world K) and,
    with `released`, the shadow set its record declares (`release` on the family
    itself: a shadow is a ray of the same family, bit-law-v1)."""
    ray = records[name]
    entry = {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 16,
        "metric": "links",
        "pace": [1, 1],
        "charge": ray["charge"],
    }
    if ray["clock"]:
        entry["clock"] = True
    if released:
        assert ray["release"] != UNDECIDED, name
        entry["release"] = ray["release"]
    # No table of the spread is read: a shadow spreads by the Node's mixing
    # (node-mixing-v1, Highlights 5.4 point 24), and no record declares a width.
    assert not {"spread", "steering", "phase_bits", "field", "field_of"} & ray.keys()
    return entry


def board(
    records: JsonObject,
    names: list[str],
    lamps: list[Lamp],
    rules: list[JsonObject],
    bodies: list[JsonObject] | None = None,
    released: list[str] | None = None,
    shadows: dict[str, list[JsonObject]] | None = None,
    clock: int = K,
) -> JsonObject:
    """A periodic 15^3 board of the named catalog rays (or the apparatus family);
    `lamps` are (position, ray, amount, heading index, phase), each a holding lamp
    that emits once and holds the world's momentum field; `bodies` are
    external-body declarations; `released` names the families declared with their
    shadow set; `shadows` a profile of shadows per family (`initial_field`)."""
    momentum = {
        "name": "momentum",
        "components": 3,
        "units": "quantum",
        "signed": True,
        "conserved": True,
        "extensive": True,
    }
    document = {
        "schema_version": 1,
        "model_id": "nature-catalog-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 2,
        "K": clock,
        "N": 1 << REFERENCE_BITS,
        # The wait per whole quantum read (Highlights 5.4 point 23) is pinned in
        # tests/test_wait_rule.py; these worlds pin the catalog without it.
        "wait_per_quantum": 0,
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
        "fields": [scalar(name) for name in names] + [momentum],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [name, "momentum"],
                "defaults": {name: amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index, (_, name, amount, _, _) in enumerate(lamps)
        ],
        "spatial_fields": [spatial_field(records, name, name in (released or [])) for name in names],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": name,
                "amount": amount,
                "denominator": 1,
                "heading": HEADINGS[heading],
                "kerengonen_phase": phase,
            }
            for index, (_, name, amount, heading, phase) in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _, _) in enumerate(lamps)
        ],
        "ray_interactions": rules,
        **({} if bodies is None else {"external_bodies": bodies}),
    }
    if shadows:
        document["initial_field"] = {name: {"rays": rays} for name, rays in shadows.items()}
    return document


def rule(name: str, coupling: JsonObject) -> JsonObject:
    """A `ray_interactions` rule taken from a decided coupling of the catalog: its
    outputs, or its momentum table with its reading."""
    result = {
        "name": name,
        "participants": coupling["participants"],
        "invariants": coupling["invariants"],
    }
    if "outputs" in coupling:
        result["outputs"] = coupling["outputs"]
    else:
        result["momentum_table"] = coupling["momentum_table"]
        result["reads"] = coupling["reads"]
    return result


def with_names(value: Any) -> Any:
    """The same rule with the world's names written in: the external body's role
    becomes its family, and the `field`, `type` and `offset` placeholders their names."""
    if isinstance(value, dict):
        if value == {"apparatus": "external_body"}:
            return {"type": BODY_NAMES["body"]}
        return {
            key: BODY_NAMES.get(item, item)
            if key in ("field", "type", "offset") and isinstance(item, str)
            else with_names(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [with_names(item) for item in value]
    return value


def run(document: JsonObject, ticks: int = 2) -> Simulation:
    simulation = Simulation(parse_initial_state(document))
    for _tick in range(ticks):
        simulation.step()
        assert all(item["balanced"] for item in simulation.spatial_accounting().values())
        assert simulation.audit()["balanced"]
    return simulation


def rays_at(simulation: Simulation, position: tuple[int, int, int]) -> list[Ray]:
    node = next((n for n in simulation.inventory_view().nodes if n.position == position), None)
    if node is None or not node.rays:
        return []
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return sorted(
        (replace(ray, owner=0) for bundle in node.rays for ray in bundle),
        key=lambda ray: (ray.heading, ray.event_ports),
    )


def event_ray(
    heading: int,
    amount: int,
    phase: int,
    mask: int,
    shares: Shares,
    steps: int = 1,
    momentum: tuple[int, int, int] | None = None,
) -> Ray:
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=steps,
        event_ports=mask,
        event_shares=shares,
        momentum=momentum,
    )


def shadow_ray(
    heading: int,
    amount: int,
    phase: int,
    sign: int,
    outbound: int = 1,
    momentum: tuple[int, int, int] | None = None,
) -> Ray:
    """A shadow: a ray of its owner's family with the bit 0, no event, its owner's
    charge sign (negated on its way back), one Link walked."""
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=1,
        outbound=outbound,
        detector=BIT_SHADOW,
        source_sign=sign,
        momentum=momentum,
    )


def neighbor(position: tuple[int, int, int], heading: int) -> tuple[int, int, int]:
    x, y, z = (c + s for c, s in zip(position, HEADINGS[heading], strict=True))
    return (x, y, z)


@pytest.mark.parametrize("case", ["records", "undecided", "experiments", "worlds"])
def test_the_catalog_of_nature_validates_as_data_on_the_one_engine(case: str) -> None:
    data = catalog()
    rays, couplings, apparatus = data["rays"], data["couplings"], data["apparatus"]
    if case == "records":
        # (a) The sections, the units and every record with its required keys, every
        # reference resolving: a ray is a family of things with its shadow set; a
        # bound group's charge is the sum over its members and its binding is a
        # corner table; a decided coupling has nothing undecided in what it does;
        # an external-body coupling is one the external body lists, and the
        # Detector's declaration is the mark's three keys.
        assert set(data) == SECTIONS
        assert (data["schema"], data["date"]) == ("nature-catalog-v1", "2026-09-18")
        assert data["units"]["content"]["value"] == 1 and data["units"]["charge"]["per_e"] == 3
        assert "rest_rate" not in data["units"]
        # One N for the world (the definitions of the law, 2026-09-18): the phase
        # unit names N, and no section and no record declares a width or a lag.
        assert "N, the number of steps of the phase circle" in data["units"]["phase"]["note"]
        assert not {"phase_bits", "lag_bits"} & data.keys()
        assert set(data["layers"]) == {"note"}
        for name, ray in rays.items():
            assert RAY_KEYS <= ray.keys(), name
            assert ray["kind"] in ("ray", "bound_group"), name
            content = ray["content"]
            assert content == UNDECIDED or (type(content) is int and content >= 0), name
            # A clock is a family's declaration, not a rate (clock-readings-v1).
            assert type(ray["clock"]) is bool and ray["clock"] == (content != 0), name
            assert type(ray["charge"]) is int, name
            # No field family, no field of a family, no width per family (bit-law-v1,
            # point 12; the cleanup of 2026-09-18): a family's field is its shadow
            # set, the release it declares, decided or not.
            assert not {"field", "field_of", "phase_bits", "source_sign", "spread"} & ray.keys(), name
            release = ray["release"]
            assert release == UNDECIDED or (
                len(release) == 2
                and all(type(part) is int for part in release)
                and 1 <= release[0] <= release[1]
            ), name
            if ray["kind"] == "bound_group":
                members = ray["members"]
                assert all(
                    rays[member]["kind"] == "ray" and type(count) is int and count >= 1
                    for member, count in members.items()
                ), name
                assert sum(rays[m]["charge"] * count for m, count in members.items()) == ray["charge"]
                # A bound group's binding is a corner table (loop-binding-v1,
                # 2026-09-17): an outputs rule whose loop closes, decided or not.
                assert "outputs" in couplings[ray["binding"]], name
                assert "decay" not in ray or ray["decay"]["coupling"] in couplings, name
            else:
                assert not {"members", "binding", "decay"} & ray.keys(), name
        external = set()
        for name, coupling in couplings.items():
            assert COUPLING_KEYS <= coupling.keys(), name
            assert coupling["status"] in ("decided", "open"), name
            engine = coupling["engine"]
            assert isinstance(engine["identity"], str) and type(engine["landed"]) is bool, name
            results = RESULT_KEYS & coupling.keys()
            assert len(results) == 1 and 1 <= len(coupling["participants"]) <= 6, name
            for participant in coupling["participants"]:
                if "apparatus" in participant:
                    assert participant == {"apparatus": "external_body"}, name
                    external.add(name)
                else:
                    assert set(participant) == {"type"}, name
                    assert all(kind == "any" or kind in rays for kind in types_of(participant)), name
            assert all({"name", "expression"} <= inv.keys() for inv in coupling["invariants"]), name
            if coupling["status"] == "decided":
                assert not undecided({key: coupling[key] for key in results}), name
                assert engine["landed"], name
            else:
                assert undecided(coupling), name
        for name, item in apparatus.items():
            assert APPARATUS_KEYS <= item.keys(), name
            assert isinstance(item["declaration"], dict) and item["declaration"], name
            assert type(item["engine"]["landed"]) is bool, name
        assert set(apparatus) == {"detector", "external_body"}
        # node-is-ports-v1: no seed, no counter, no coupling on the bit; the mark's
        # table and the resident thing's on_click.
        assert set(apparatus["detector"]["declaration"]) == {"position", "setting", "on_click"}
        assert set(apparatus["external_body"]["couplings"]) == external
        assert apparatus["external_body"]["default_coupling"] in external
        assert set(apparatus["external_body"]["declaration"]) == {
            "position",
            "family",
            "amount",
            "charge",
            "phase",
            "initial_momentum",
            "coupling",
            "momentum_table",
            "reads",
            "thing",
            "polarizer",
        }
        piece = apparatus["external_body"]["apparatus_family"]
        assert (piece["content"], piece["clock"], piece["charge"]) == (0, False, 0)
        assert piece["name"] not in rays and "field" not in piece
        assert apparatus["detector"]["engine"]["landed"]
        # The thing resident at the mark and its one table (node-is-ports-v1): the
        # couplings on the bit a ray carries went with bit-law-v1 (the bit never
        # changes at a meeting and a mark reads it, never a coupling on it).
        mark_couplings = apparatus["detector"]["couplings"]
        assert set(mark_couplings) == {"on_click"}
        assert "node-is-ports-v1" in apparatus["detector"]["engine"]["identity"]
        assert "node-is-ports-v1" in apparatus["external_body"]["engine"]["identity"]
        # A click is an absorption (Highlights 5.4, 2026-09-18; detector-absorb-v1,
        # feature 2c): the coupling on a catch, per family, absorb the default.
        click = mark_couplings["on_click"]
        assert (click["status"], click["world_key"], click["engine"]) == (
            "decided",
            "on_click",
            {"identity": "detector-absorb-v1", "landed": True},
        )
        assert set(click["values"]) == {"absorb", "pass"} and "decided_by" not in click
        assert not undecided(click)
        assert click["default"] == "absorb for every family"
        assert "detector-absorb-v1" in apparatus["detector"]["engine"]["identity"]
        assert apparatus["external_body"]["engine"]["landed"]
        assert len(rays) == 11 and len(couplings) == 14
        # The mass field and gravity by delay are retired (point 18); the recoil is
        # the return of the law (point 3), no coupling.
        assert not {"mass_field_delay", "recoil_return"} & couplings.keys()
        assert "mass_field" not in rays
        # A decay is a table (point 20): weak_conversion declares its condition.
        assert set(couplings["weak_conversion"]["decay"]) == {"after_periods", "decided_by"}
        assert "draw" not in couplings["weak_conversion"] and "setting" not in rays["neutron"]["decay"]
        # Light and the gluon are real families (Highlights 3.26 as amended on
        # 2026-09-18): things without content on the ladder and without a clock,
        # the gluon's colour and both shadow sets undecided; the charged families
        # declare their shadow set, the same ratio for the three.
        for name in ("light", "gluon"):
            assert (rays[name]["kind"], rays[name]["content"], rays[name]["clock"]) == ("ray", 0, False)
            assert rays[name]["release"] == UNDECIDED, name
        assert rays["gluon"]["colour"] == UNDECIDED
        assert all(rays[name]["release"] == [1, 4] for name in ("electron", "positron", "proton"))
        # Feature 11 (ray-polarization-v1): the polarization decided by A12, a
        # transverse direction on the circle of the world's width, and spin the
        # same property at one bit on the electron family.
        light = rays["light"]
        assert (light["polarization"], light["polarization_bits"]) == ("transverse", "default")
        assert all(rays[name]["polarization_bits"] == 1 for name in ("electron", "positron"))
        polarizer = couplings["polarizer"]
        assert (polarizer["status"], polarizer["world_name"]) == ("decided", "polarizer")
        assert polarizer["outputs"]["table"] == [8, 7, 4, 1, 0, 1, 4, 7]
        assert polarizer["outputs"]["reference_bits"] == REFERENCE_BITS
        assert not {"electron_field", "positron_field"} & rays.keys()
        # The electron's turn is a momentum table on its own family's shadows
        # (points 12 and 16): the same family on both sides, read by charge.
        turn = couplings["electron_field_turn"]
        assert [types_of(p) for p in turn["participants"]] == [["electron"], ["electron"]]
        assert (turn["momentum_table"], turn["reads"], turn["status"]) == (
            {"electron": 1},
            "charge",
            "decided",
        )
        assert "outputs" not in turn and "opposite_charge" not in turn
    elif case == "undecided":
        # (b) Every "undecided" names, in its own record, an entry of the register or
        # a hypothesis of the hypotheses page that decides it, and the table of
        # docs/CATALOG.md lists exactly these paths with these deciders.
        found = undecided(data)
        known = deciders()
        for path, named in found.items():
            assert named and all(decider in known for decider in named), (path, named)
        assert documented_undecided() == found
        # 25 on 2026-09-18 under clock-readings-v1; 29 since the cleanup of the same
        # day: the lag's world key and the recoil coupling left (the delay and the
        # word register retired, the recoil the return of the law), and the shadow
        # set of every family the model owner has not sized joined (light, the
        # gluon, the muon, the two neutrinos, the two quarks, the neutron), each
        # hypothesis 17's, the gluon's also hypothesis 13's.
        assert len(found) == 29
        assert {decider for named in found.values() for decider in named} == {
            "A1",
            "A2",
            "A3",
            "A5",
            "A8",
            "A9",
            "A10",
            "hypothesis 12",
            "hypothesis 13",
            "hypothesis 17",
        }
        assert all(found[f"rays.{name}.release"] == ["hypothesis 17"] for name in ("light", "muon"))
    elif case == "experiments":
        # (c) The catalog lists exactly the confrontation entries of the register,
        # and every id an entry uses resolves, once.
        register = (ROOT / "docs/EXPERIMENTS.md").read_text(encoding="utf-8")
        assert set(data["experiments"]) == set(re.findall(r"^### (A\d+)\. ", register, re.M))
        assert len(data["experiments"]) == 14
        for name, experiment in data["experiments"].items():
            assert EXPERIMENT_KEYS <= experiment.keys(), name
            for key, table in (("rays", rays), ("couplings", couplings), ("apparatus", apparatus)):
                listed = experiment[key]
                assert len(listed) == len(set(listed)), (name, key)
                assert all(item in table for item in listed), (name, key)
        assert data["experiments"]["A1"]["couplings"][0] == "born_steering"
        assert data["experiments"]["A5"]["couplings"] == ["electron_field_turn"]
    else:
        # (d) Every ray a world can select today: one lamp of 5 at (7,7,7) emitting
        # along +X at phase 3; after two ticks the ray is at (9,7,7), its phase
        # advanced twice by one step per interval when its family has a clock (K 5,
        # content 5) and unchanged for light and the gluon, real families without
        # a clock (Highlights 3.26 as amended, 2026-09-18).
        runnable = [name for name, ray in rays.items() if ray["content"] != UNDECIDED]
        assert runnable == RUNNABLE_RAYS
        released = [name for name, ray in rays.items() if ray["release"] != UNDECIDED]
        assert released == [*RUNNABLE_RELEASES, "proton"]
        for name in runnable:
            simulation = run(board(rays, [name], [((7, 7, 7), name, 5, 0, 3)], []))
            rate = 1 if rays[name]["clock"] else 0
            expected = event_ray(0, 5, (3 + 2 * rate) % 8, 1, (5, 0, 0, 0, 0, 0), 2)
            assert rays_at(simulation, (9, 7, 7)) == [expected]
            assert simulation.totals() == {name: (5,), "momentum": (0, 0, 0)}
            assert simulation.charge_totals() == {name: 5 * rays[name]["charge"]}
            assert (simulation.real_content(), simulation.shadow_content()) == (5, 0)
        # Every shadow set a world can declare today, the electron's and the
        # positron's (bit-law-v1, point 12: a shadow is a ray of the same family
        # with the bit 0): the same lamp with its family's `release`, and one
        # shadow of its thing, amount 9, given with the board at (3,3,3) heading +X
        # (fresh, steps 0). After tick 1 the shadow is at (4,3,3), one Link walked;
        # in the cycle of tick 2 the Node mixes it (node-mixing-v1, point 24): a
        # lone arrival turns back four ninths, at phase 4 (the half turn, the
        # returning share the minus), and sends one ninth on each of the five other
        # headings at its own phase, so after tick 2 four quanta are at (3,3,3) on
        # -X and one at each of (5,3,3) +X, (4,4,3) +Y, (4,2,3) -Y, (4,3,4) +Z,
        # (4,3,2) -Z. The books: 5 real and 9 shadow at every tick, the family's
        # total 14, the charge total the thing's alone (a shadow carries no charge).
        for name in RUNNABLE_RELEASES:
            sign = (rays[name]["charge"] > 0) - (rays[name]["charge"] < 0)
            profile = [
                {
                    "position": [3, 3, 3],
                    "heading": [1, 0, 0],
                    "amount": 9,
                    "phase": 0,
                    "sign": sign,
                    "owner": 1,
                    "steps": 0,
                }
            ]
            document = board(rays, [name], [((7, 7, 7), name, 5, 0, 3)], [], released=[name])
            document["initial_field"] = {name: {"rays": profile}}
            simulation = Simulation(parse_initial_state(document))
            simulation.step()
            assert rays_at(simulation, (4, 3, 3)) == [shadow_ray(0, 9, 0, sign)]
            simulation.step()
            assert rays_at(simulation, (3, 3, 3)) == [shadow_ray(1, 4, 4, sign)]
            for heading in (0, 2, 3, 4, 5):
                assert rays_at(simulation, neighbor((4, 3, 3), heading)) == [
                    shadow_ray(heading, 1, 0, sign)
                ]
            assert rays_at(simulation, (4, 3, 3)) == []
            assert rays_at(simulation, (9, 7, 7)) == [event_ray(0, 5, 5, 1, (5, 0, 0, 0, 0, 0), 2)]
            assert simulation.totals() == {name: (14,), "momentum": (0, 0, 0)}
            assert simulation.charge_totals() == {name: 5 * rays[name]["charge"]}
            assert (simulation.real_content(), simulation.shadow_content()) == (5, 9)
            assert simulation.audit()["balanced"]
        # Every decided coupling the engine runs today, with its rule taken from the
        # file. born_steering: two light rays of 8 meet head-on at (7,7,7) after tick
        # 1 and are steered at tick 2 between +Y and -Y by the table at their phase
        # difference d, the rest output owning the remainder.
        decided = [
            name
            for name, coupling in couplings.items()
            if coupling["status"] == "decided" and coupling["engine"]["landed"]
        ]
        assert decided == RUNNABLE_COUPLINGS
        steering = couplings["born_steering"]
        # The table is computed from N (point 17): the catalog declares none.
        assert steering["outputs"][0]["amount"] == {"of": "sum", "index": "phase_difference"}
        assert [types_of(p) for p in steering["participants"]] == [["light"], ["light"]]
        for delta, (plus, minus) in STEERED.items():
            lamps = [((6, 7, 7), "light", 8, 0, 0), ((8, 7, 7), "light", 8, 1, delta)]
            simulation = run(board(rays, ["light"], lamps, [rule("born_steering", steering)]))
            mask = (4 if plus else 0) | (8 if minus else 0)
            shares = (0, 0, plus, minus, 0, 0)
            assert rays_at(simulation, (7, 8, 7)) == (
                [event_ray(2, plus, 0, mask, shares)] if plus else []
            )
            assert rays_at(simulation, (7, 6, 7)) == (
                [event_ray(3, minus, delta, mask, shares)] if minus else []
            )
            assert rays_at(simulation, (7, 7, 7)) == []
            # The momentum the corner moves between lines is booked as the meeting's
            # source (ray-meeting-conversion-v1, feature 14's rule): +Y less -Y.
            assert simulation.totals() == {"light": (16,), "momentum": (0, plus - minus, 0)}
            assert simulation.source_totals() == {"light": (0,), "momentum": (0, plus - minus, 0)}
        # electron_field_turn (bit-law-v1, points 3, 15 and 16): an electron of 20
        # (lamp 0, K 20, one phase step per interval) emitted along +X from (6,7,7)
        # and a shadow of 1 of a second electron (lamp 1 at (13,13,13), thing 2,
        # whole charge -60 over content 20) heading -Y from (7,8,7) meet at (7,7,7)
        # after tick 1. In the cycle of tick 2 the electron takes the push: sign 1
        # x amount 1 x heading (0,-1,0) x the owner's charge over its content (-3)
        # x the electron's charge (-3) = (0,-9,0), below its content, so it goes on
        # along +X to (8,7,7) carrying momentum (0,-9,0) (no event, no step); the
        # shadow turns back with the opposite sign, fresh at (7,7,7), and after
        # tick 2 is at (7,8,7) on +Y, returning (outbound 0, sign +1), carrying
        # (0,9,0). The books: the family's total 41, real 40, shadow 1, the two
        # things' momentum {1: (20,-9,0), 2: (20,0,0)}, the ledger balanced.
        turn = couplings["electron_field_turn"]
        lamps = [((6, 7, 7), "electron", 20, 0, 0), ((13, 13, 13), "electron", 20, 0, 0)]
        document = board(rays, ["electron"], lamps, [rule("electron_field_turn", turn)], clock=20)
        document["initial_field"] = {
            "electron": {
                "rays": [
                    {
                        "position": [7, 8, 7],
                        "heading": [0, -1, 0],
                        "amount": 1,
                        "phase": 0,
                        "sign": -1,
                        "owner": 2,
                        "steps": 0,
                    }
                ]
            }
        }
        simulation = run(document)
        assert rays_at(simulation, (8, 7, 7)) == [
            event_ray(0, 20, 2, 1, (20, 0, 0, 0, 0, 0), 2, momentum=(0, -9, 0))
        ]
        assert rays_at(simulation, (7, 8, 7)) == [shadow_ray(2, 1, 0, 1, outbound=0, momentum=(0, 9, 0))]
        assert rays_at(simulation, (7, 7, 7)) == []
        assert simulation.totals() == {"electron": (41,), "momentum": (0, 0, 0)}
        assert simulation.thing_momentum() == {1: [20, -9, 0], 2: [20, 0, 0]}
        assert (simulation.real_content(), simulation.shadow_content()) == (40, 1)
        assert simulation.charge_totals() == {"electron": -120}
        # The apparatus. A Detector mark parses under the admission these worlds
        # share. An external body at (8,7,7) meets a light ray of 5 emitted at
        # (7,7,7) along +X at phase 1: under the absorber (the sink, a body of the
        # electron family, a large charge) the ray ends in the body's sink in its
        # arrival interval; under the mirror and the phase plate (a body of the
        # apparatus family) it is met at tick 2 and leaves reversed on its line, or
        # continues with its phase plus the setting, the token counted as one
        # quantum on +X in the event's shares.
        body = apparatus["external_body"]
        piece = body["apparatus_family"]
        records = rays | {piece["name"]: piece}
        lamps = [((7, 7, 7), "light", 5, 0, 1)]
        document = board(records, ["light"], lamps, [])
        document[apparatus["detector"]["world_key"]] = [{"position": [9, 7, 7], "setting": [1, 1]}]
        assert len(parse_initial_state(document).detectors) == 1
        at_rest = {
            "index": 0,
            "position": [8, 7, 7],
            "stepping": False,
            "momentum": [0, 0, 0],
            "accumulators": [0, 0, 0],
        }
        sink = {"position": [8, 7, 7], "family": "electron", "amount": 4096, "charge": -3}
        sink["coupling"] = couplings[body["default_coupling"]]["world_name"]
        simulation = run(board(records, ["light", "electron"], lamps, [], [sink]))
        # The lamp keeps its recoil (-5 on X) and the sink took the ray's momentum.
        assert simulation.totals() == {"light": (0,), "electron": (0,), "momentum": (-5, 0, 0)}
        assert not any(any(node.rays) for node in simulation.inventory_view().nodes)
        assert simulation.external_body_totals() == {
            "light": (5,),
            "electron": (0,),
            "momentum": (5, 0, 0),
        }
        assert simulation.external_bodies() == [at_rest | {"sink": {"light": 5}}]
        assert simulation.external_body_momentum() == (0, 0, 0)
        # The momentum a body's table moves is booked as the meeting's source (feature
        # 14's rule, the meeting's momentum change): the ray's momentum on X after
        # the meeting, -5 under the mirror, less its 5 before, beside the lamp's
        # recoil -5 in the totals. The phase plate's token is written on the ray's
        # own heading and shares its lane, so under lanes-v1 (Highlights 5.4, point
        # 25) the departure is refused until bodies are things with their own line
        # (the cleanup of 2026-09-18 pins the refusal; the coordinator holds the
        # question of #293).
        for name, position, product, ray_momentum in (
            ("mirror", (7, 7, 7), event_ray(1, 5, 1, 3, (1, 5, 0, 0, 0, 0)), -5),
            ("phase_plate", (9, 7, 7), None, 5),
        ):
            assert [types_of(p) for p in couplings[name]["participants"][:1]] == [["any"]]
            declared = {"position": [8, 7, 7], "family": piece["name"], "amount": 4096, "coupling": name}
            document = board(
                records,
                ["light", piece["name"]],
                lamps,
                [with_names(rule(name, couplings[name]))],
                [declared],
            )
            if product is None:
                with pytest.raises(ValueError, match="point 25"):
                    run(document)
                continue
            simulation = run(document)
            assert rays_at(simulation, position) == [product]
            assert rays_at(simulation, (8, 7, 7)) == []
            assert simulation.totals() == {
                "light": (5,),
                piece["name"]: (0,),
                "momentum": (-5 + ray_momentum, 0, 0),
            }
            assert simulation.source_totals()["momentum"] == (ray_momentum - 5, 0, 0)
            assert simulation.external_body_totals() == {
                "light": (0,),
                piece["name"]: (0,),
                "momentum": (0, 0, 0),
            }
            assert simulation.external_bodies() == [at_rest | {"sink": {}}]
        # The polarizer (ray-polarization-v1): the same lamp polarized along +Y (step
        # 0) at a body of angle 2 (45 degrees on the eight-step circle) with the
        # catalog's table: 5 x 4 / 8 passes 2 with polarization 2, sinks 2, and the
        # two shares of 4/8 wait in the body's registers as one quantum, at phase 1.
        polarizer = couplings["polarizer"]
        assert [types_of(p) for p in polarizer["participants"][:1]] == [["light"]]
        document = board(records, ["light", piece["name"]], lamps, [])
        document["emissions"][0]["polarization"] = 0
        document["external_bodies"] = [
            {
                "position": [8, 7, 7],
                "family": piece["name"],
                "amount": 4096,
                "coupling": polarizer["world_name"],
                "polarizer": {
                    "family": "light",
                    "angle": 2,
                    "pass": [1, 0, 0],
                    "table": polarizer["outputs"]["table"],
                },
            }
        ]
        simulation = run(document)
        assert rays_at(simulation, (9, 7, 7)) == [
            Ray(
                0,
                (0, 0, 0),
                2,
                phase=1,
                steps=1,
                event_ports=1,
                event_shares=(2, 0, 0, 0, 0, 0),
                polarization=2,
            )
        ]
        assert rays_at(simulation, (8, 7, 7)) == []
        # The lamp's recoil -5 and the passing 2 on +X; the shares held in the body's
        # registers count outside the totals (a body's content enters no sum).
        assert simulation.totals() == {"light": (3,), piece["name"]: (0,), "momentum": (-3, 0, 0)}
        # The body's line: the two quanta sunk and the one held, all on +X.
        assert simulation.external_body_totals() == {
            "light": (2,),
            piece["name"]: (0,),
            "momentum": (3, 0, 0),
        }
        assert simulation.external_bodies() == [
            at_rest
            | {"sink": {"light": 2}, "held": [0, 0, 4, 4, 0, 0], "held_phases": [0, 0, 1, 1, 0, 0]}
        ]
