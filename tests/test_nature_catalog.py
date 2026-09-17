"""The catalog of nature (`catalog/nature.json`): the rays of nature and their
couplings as data on the one generic engine, and the two apparatus kinds, with
"undecided" wherever the model owner has not decided a value. The file parses
under the strict decoder with no float; every ray, coupling and apparatus record
carries its required keys and every reference resolves; every "undecided" names
the experiment or hypothesis that decides it and is listed in docs/CATALOG.md;
the register's confrontation entries and the catalog's agree; every ray a world
can select, every release a world can declare and every decided coupling the
engine runs today is built from the file into a minimal inline world, parsed and
run for two ticks against pinned integers, an external body under each of its
decided couplings among them. Light is the field of a charge (Highlights 3.5,
2026-09-17): one family, released by the electron and the positron and emitted
by any source, its spread table open for feature 12.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Catalog of nature")
before the first run.
"""

import re
from pathlib import Path
from typing import Any

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import Ray
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
    "phase_bits",
    "lag_bits",
    "rays",
    "couplings",
    "layers",
    "apparatus",
    "experiments",
}
RAY_KEYS = {"kind", "rest_rate", "charge", "phase_bits", "field", "note"}
COUPLING_KEYS = {"status", "engine", "participants", "invariants", "note"}
RESULT_KEYS = {"outputs", "binds", "sink"}
APPARATUS_KEYS = {"world_key", "engine", "declaration", "does", "note"}
EXPERIMENT_KEYS = {"rays", "couplings", "apparatus", "note"}
# The rays a world can select today, in catalog order, the releases a world can
# declare today as (releaser, field), and the couplings the engine runs today: a
# newly decided entry must join these lists and get a world below.
RUNNABLE_RAYS = ["light", "electron", "positron"]
RUNNABLE_RELEASES = [("electron", "light"), ("positron", "light")]
RUNNABLE_COUPLINGS = ["born_steering", "electron_field_turn", "absorber", "mirror", "phase_plate"]
# The names a world writes into an external-body coupling of the catalog: the met
# family for "any" and "same", the body's family for "body", the offset for "setting".
BODY_NAMES: dict[str, str | int] = {"any": "light", "same": "light", "body": "apparatus", "setting": 3}
# The Born split of 16 quanta at phase difference d: the +Y and the -Y amounts.
STEERED = {0: (16, 0), 1: (14, 2), 2: (8, 8), 4: (0, 16)}


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


def spatial_field(records: JsonObject, name: str, source: str | None = None) -> JsonObject:
    """The world's `spatial_fields` entry for one catalog ray, at the reference width;
    with `source`, the ray is declared as the released field of that family."""
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
        "phase_bits": REFERENCE_BITS,
        "kerengonen": {"phase_advance": ray["rest_rate"]},
        "charge": ray["charge"],
    }
    if source is not None:
        assert ray["kind"] == "field" and source in ray["field_of"], name
        entry |= {"field_of": source, "release": ray["release"]}
    return entry


def board(
    records: JsonObject,
    names: list[str],
    lamps: list[Lamp],
    rules: list[JsonObject],
    bodies: list[JsonObject] | None = None,
    released: dict[str, str] | None = None,
) -> JsonObject:
    """A periodic 15^3 board of the named catalog rays (or the apparatus family);
    `lamps` are (position, ray, amount, heading index, phase), each a holding lamp
    that emits once, funded; `bodies` are external-body declarations; `released`
    maps a field ray to the family of the world that releases it."""
    return {
        "schema_version": 1,
        "model_id": "nature-catalog-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 2,
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
        "fields": [scalar(name) for name in names],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [name],
                "defaults": {name: amount},
                "transport": {"mode": "hold"},
            }
            for index, (_, name, amount, _, _) in enumerate(lamps)
        ],
        "spatial_fields": [spatial_field(records, name, (released or {}).get(name)) for name in names],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": name,
                "amount": amount,
                "denominator": 1,
                "source": False,
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


def rule(name: str, coupling: JsonObject) -> JsonObject:
    """A `ray_interactions` rule taken from a decided coupling of the catalog."""
    return {
        "name": name,
        "participants": coupling["participants"],
        "outputs": coupling["outputs"],
        "invariants": coupling["invariants"],
    }


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


def run(document: JsonObject) -> Simulation:
    simulation = Simulation(parse_initial_state(document))
    for _tick in range(2):
        simulation.step()
        assert all(item["balanced"] for item in simulation.spatial_accounting().values())
    return simulation


def rays_at(simulation: Simulation, position: tuple[int, int, int]) -> list[Ray]:
    node = next((n for n in simulation.inventory_view().nodes if n.position == position), None)
    if node is None or not node.rays:
        return []
    return sorted(
        (ray for bundle in node.rays for ray in bundle),
        key=lambda ray: (ray.heading, ray.event_ports),
    )


def event_ray(heading: int, amount: int, phase: int, mask: int, shares: Shares, steps: int = 1) -> Ray:
    return Ray(
        heading, (0, 0, 0), amount, phase=phase, steps=steps, event_ports=mask, event_shares=shares
    )


def released_ray(heading: int, amount: int, phase: int) -> Ray:
    """A field ray: no event, its source's phase at the release, one Link walked."""
    return Ray(heading, (0, 0, 0), amount, phase=phase, steps=1)


def neighbor(position: tuple[int, int, int], heading: int) -> tuple[int, int, int]:
    x, y, z = (c + s for c, s in zip(position, HEADINGS[heading], strict=True))
    return (x, y, z)


@pytest.mark.parametrize("case", ["records", "undecided", "experiments", "worlds"])
def test_the_catalog_of_nature_validates_as_data_on_the_one_engine(case: str) -> None:
    data = catalog()
    rays, couplings, apparatus = data["rays"], data["couplings"], data["apparatus"]
    if case == "records":
        # (a) The sections, the units and every record with its required keys, every
        # reference resolving: a field lists its sources and each source lists it; a
        # bound group's charge is the sum over its members; a decided coupling has
        # nothing undecided in what it does; an external-body coupling is one the
        # external body lists, and the Detector's declaration is the mark's three keys.
        assert set(data) == SECTIONS
        assert (data["schema"], data["date"]) == ("nature-catalog-v1", "2026-09-17")
        assert data["units"]["rest_rate"]["value"] == 1 and data["units"]["charge"]["per_e"] == 3
        assert data["phase_bits"]["default"] == 8
        assert data["phase_bits"]["reference_table"] == REFERENCE_BITS
        assert "real" not in data["phase_bits"]
        lag = data["lag_bits"]
        assert (lag["status"], lag["world_key"], lag["engine"]["landed"]) == ("open", UNDECIDED, False)
        assert set(data["layers"]) == {"note"}
        for name, ray in rays.items():
            assert RAY_KEYS <= ray.keys(), name
            assert ray["kind"] in ("ray", "field", "bound_group"), name
            rate = ray["rest_rate"]
            assert rate == UNDECIDED or (type(rate) is int and rate >= 0), name
            assert type(ray["charge"]) is int and ray["phase_bits"] == "default", name
            for field in ray["field"]:
                assert rays[field]["kind"] == "field" and name in rays[field]["field_of"], name
            if ray["kind"] == "field":
                assert (ray["rest_rate"], ray["charge"], ray["field"]) == (0, 0, []), name
                assert all(name in rays[source]["field"] for source in ray["field_of"]), name
                release = ray["release"]
                assert release == UNDECIDED or (
                    len(release) == 2
                    and all(type(part) is int for part in release)
                    and 1 <= release[0] <= release[1]
                ), name
            else:
                assert not {"field_of", "release"} & ray.keys(), name
            if ray["kind"] == "bound_group":
                members = ray["members"]
                assert all(
                    rays[member]["kind"] == "ray" and type(count) is int and count >= 1
                    for member, count in members.items()
                ), name
                assert sum(rays[m]["charge"] * count for m, count in members.items()) == ray["charge"]
                assert "binds" in couplings[ray["binding"]], name
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
            assert results and 1 <= len(coupling["participants"]) <= 6, name
            for participant in coupling["participants"]:
                if "apparatus" in participant:
                    assert participant == {"apparatus": "external_body"}, name
                    external.add(name)
                else:
                    assert set(participant) == {"type"}, name
                    assert all(kind == "any" or kind in rays for kind in types_of(participant)), name
            assert all({"name", "expression"} <= inv.keys() for inv in coupling["invariants"]), name
            assert all(kind in rays for kind in coupling.get("binds", [])), name
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
        assert set(apparatus["detector"]["declaration"]) == {"position", "setting", "seed"}
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
        }
        piece = apparatus["external_body"]["apparatus_family"]
        assert (piece["rest_rate"], piece["charge"], piece["field"]) == (0, 0, [])
        assert piece["name"] not in rays
        assert apparatus["detector"]["engine"]["landed"]
        assert apparatus["external_body"]["engine"]["landed"]
        assert len(rays) == 12 and len(couplings) == 16
        # Light is the field of a charge (Highlights 3.5, 2026-09-17): the one
        # electromagnetic family, released by both charged families, its spread
        # table open, and no other family the field of a charged ray.
        light = rays["light"]
        assert (light["kind"], light["field_of"], light["release"]) == (
            "field",
            ["electron", "positron"],
            [1, 4],
        )
        assert light["spread"] == UNDECIDED and light["decided_by"]["spread"] == "feature 12"
        assert not {"electron_field", "positron_field"} & rays.keys()
        assert all("light" in rays[name]["field"] for name in ("electron", "positron"))
    elif case == "undecided":
        # (b) Every "undecided" names, in its own record, an entry of the register or
        # a hypothesis of the hypotheses page that decides it, and the table of
        # docs/CATALOG.md lists exactly these paths with these deciders.
        found = undecided(data)
        known = deciders()
        for path, named in found.items():
            assert named and all(decider in known for decider in named), (path, named)
        assert documented_undecided() == found
        assert len(found) == 29
        assert {decider for named in found.values() for decider in named} == {
            "A1",
            "A2",
            "A3",
            "A5",
            "A6",
            "A8",
            "A9",
            "A10",
            "A12",
            "hypothesis 12",
            "hypothesis 13",
            "feature 8b",
            "feature 12",
        }
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
        assert data["experiments"]["A5"]["couplings"][0] == "electron_field_turn"
    else:
        # (d) Every ray a world can select today: one lamp of 5 at (7,7,7) emitting
        # along +X at phase 3; after two ticks the ray is at (9,7,7) with its phase
        # advanced twice by its rest rate. Every release a world can declare today,
        # light by the electron and light by the positron: the same lamp of the
        # releaser, whose departure from (8,7,7) releases five field rays, one per
        # Port heading but its own.
        runnable = [
            name
            for name, ray in rays.items()
            if ray["kind"] != "bound_group"
            and ray["rest_rate"] != UNDECIDED
            and (ray["kind"] != "field" or ray["release"] != UNDECIDED)
        ]
        assert runnable == RUNNABLE_RAYS
        releases = [
            (source, name)
            for name, ray in rays.items()
            if ray["kind"] == "field" and ray["release"] != UNDECIDED
            for source in ray["field_of"]
            if rays[source]["rest_rate"] != UNDECIDED
        ]
        assert releases == RUNNABLE_RELEASES
        for source, name in [(name, None) for name in runnable] + releases:
            names = [source] if name is None else [source, name]
            released = {} if name is None else {name: source}
            lamps: list[Lamp] = [((7, 7, 7), source, 5, 0, 3)]
            simulation = run(board(rays, names, lamps, [], released=released))
            rate = rays[source]["rest_rate"]
            assert rays_at(simulation, (9, 7, 7)) == [
                event_ray(0, 5, (3 + 2 * rate) % 8, 1, (5, 0, 0, 0, 0, 0), 2)
            ]
            totals = {source: (5,)}
            if name is not None:
                numerator, denominator = rays[name]["release"]
                each = 5 * numerator // denominator
                for heading in range(1, 6):
                    assert rays_at(simulation, neighbor((8, 7, 7), heading)) == [
                        released_ray(heading, each, (3 + rate) % 8)
                    ]
                totals[name] = (5 * each,)
                assert simulation.source_totals()[name] == (5 * each,)
            assert simulation.totals() == totals
            assert simulation.charge_totals() == {
                held: 5 * rays[held]["charge"] if held == source else 0 for held in names
            }
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
        assert steering["outputs"][0]["amount"]["table"] == [8, 7, 4, 1, 0, 1, 4, 7]
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
            assert simulation.totals() == {"light": (16,)}
            assert simulation.source_totals() == {"light": (0,)}
        # electron_field_turn: an electron of 5 and a light ray of 1, the field the
        # electron family releases, meet at (7,7,7) after tick 1; at tick 2 the
        # electron leaves on the field ray's heading -Y, the field ray returns
        # reversed, and the electron's departure releases five light rays of amount
        # 1 with its phase 1.
        turn = couplings["electron_field_turn"]
        assert [types_of(p) for p in turn["participants"]] == [["electron"], ["light"]]
        lamps = [((6, 7, 7), "electron", 5, 0, 0), ((7, 8, 7), "light", 1, 3, 0)]
        names = ["electron", "light"]
        simulation = run(
            board(
                rays, names, lamps, [rule("electron_field_turn", turn)], released={"light": "electron"}
            )
        )
        shares = (0, 0, 1, 5, 0, 0)
        assert rays_at(simulation, (7, 6, 7)) == [event_ray(3, 5, 2, 12, shares)]
        assert rays_at(simulation, (7, 7, 7)) == []
        for heading in (0, 1, 2, 4, 5):
            expected = [released_ray(heading, 1, 1)]
            if heading == 2:
                expected.append(event_ray(2, 1, 0, 12, shares))
            assert rays_at(simulation, neighbor((7, 7, 7), heading)) == expected
        assert simulation.totals() == {"electron": (5,), "light": (6,)}
        assert simulation.source_totals() == {"electron": (0,), "light": (5,)}
        assert simulation.charge_totals() == {"electron": -15, "light": 0}
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
        document[apparatus["detector"]["world_key"]] = [
            {"position": [9, 7, 7], "setting": [1, 1], "seed": 0}
        ]
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
        assert simulation.totals() == {"light": (0,), "electron": (0,)}
        assert not any(any(node.rays) for node in simulation.inventory_view().nodes)
        assert simulation.external_body_totals() == {"light": (5,), "electron": (0,)}
        assert simulation.external_bodies() == [at_rest | {"sink": {"light": 5}}]
        assert simulation.external_body_momentum() == (0, 0, 0)
        for name, position, product in (
            ("mirror", (7, 7, 7), event_ray(1, 5, 1, 3, (1, 5, 0, 0, 0, 0))),
            ("phase_plate", (9, 7, 7), event_ray(0, 5, 4, 1, (6, 0, 0, 0, 0, 0))),
        ):
            assert [types_of(p) for p in couplings[name]["participants"][:1]] == [["any"]]
            declared = {"position": [8, 7, 7], "family": piece["name"], "amount": 4096, "coupling": name}
            simulation = run(
                board(
                    records,
                    ["light", piece["name"]],
                    lamps,
                    [with_names(rule(name, couplings[name]))],
                    [declared],
                )
            )
            assert rays_at(simulation, position) == [product]
            assert rays_at(simulation, (8, 7, 7)) == []
            assert simulation.totals() == {"light": (5,), piece["name"]: (0,)}
            assert simulation.external_body_totals() == {"light": (0,), piece["name"]: (0,)}
            assert simulation.external_bodies() == [at_rest | {"sink": {}}]
