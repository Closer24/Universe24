"""THE RUN FILES OF THE SOURCE VERB (record 2217; ALGEBRA.md #the-paces.116 item 4b):
examples/events/source/ holds two worlds and the fragment universe_entries.json with `sourced` and
`readings` as the ledger names them; the load waits on the loop. No pin; HOST counts alone."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.world_files import parse_nature_beam_world
from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples" / "events" / "source"
SHIPPED_UNIVERSE = ROOT / "examples" / "events" / "universe.json"
UNIVERSE = "examples/events/universe.json"
NAMES = ("source_rest", "source_moving")
MOVING = {"source_moving"}
FAMILIES = ("field", "field_table", "control")
SOURCED_KEYS = {"of", "weight", "scale", "cap"}
READING_KINDS = {"level", "total", "support", "centre"}
DELETED_WORLD_KEYS = {
    "law",
    "model_id",
    "K",
    "N",
    "release",
    "width",
    "clock_stamp",
    "detector_law",
    "massive_record",
    "body_record",
    "point_emitter",
    "age_bound",
    "amplitude_bound",
    "node_clock",
    "momentum_unit",
    "twist_table",
    "input",
    "probes",
    "mode_axis",
    "families",
}
DELETED_BLOCK_KEYS = {"momentum", "spin", "moment", "margin", "charge", "held", "fixed"}


def generator():
    return load_file("source_make_worlds", FOLDER / "make_worlds.py")


def document(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


def entries() -> list[dict]:
    fragment = json.loads((FOLDER / "universe_entries.json").read_text(encoding="utf-8"))
    assert set(fragment) == {"families"}
    return fragment["families"]


@pytest.mark.parametrize("name", NAMES)
def test_every_world_speaks_record_2128_and_declares_its_readings(name):
    doc = document(name)
    assert doc["universe"] == UNIVERSE
    assert not DELETED_WORLD_KEYS & set(doc), sorted(DELETED_WORLD_KEYS & set(doc))
    assert set(doc) >= {
        "shape",
        "boundary",
        "ticks",
        "engine",
        "measured",
        "detectors",
        "readings",
        "stamp",
    }
    count = doc["shape"][0] * doc["shape"][1] * doc["shape"][2]
    assert len(doc["measured"]) == 1
    body = doc["measured"][0]
    assert not DELETED_BLOCK_KEYS & set(body), sorted(DELETED_BLOCK_KEYS & set(body))
    assert body["family"] == "matter" and body["q"] == 0 and body["amount"] == 2000
    assert "kind" in body and "pair" in body and "clock" in body and "twist" in body
    seed = body["seed"]
    if name in MOVING:
        assert set(seed) == {"now", "before"} and len(seed["now"]) == len(seed["before"]) == count
        assert seed["now"] != seed["before"]
    else:
        assert isinstance(seed, list) and len(seed) == count
    # THE READINGS: every line a kind by name on a declared family, Node or body, every one
    # a GameBoard reading (the ledger's run declarations)
    kinds = [line["kind"] for line in doc["readings"]]
    assert set(kinds) <= READING_KINDS
    # a name per reading, unique in the world, the output's word for it (Main Loop's interface)
    names = [line["name"] for line in doc["readings"]]
    assert len(set(names)) == len(names) and all(
        name.startswith(line["kind"]) for name, line in zip(names, doc["readings"], strict=True)
    )
    for line in doc["readings"]:
        assert isinstance(line["every"], int) and line["every"] >= 1
        if line["kind"] == "level":
            assert line["family"] in ("field", "field_table") and len(line["node"]) == 3
            assert all(0 <= v < s for v, s in zip(line["node"], doc["shape"], strict=True))
        if line["kind"] == "total":
            assert line["family"] == "control"
    assert kinds.count("level") == 4 and kinds.count("support") == 2 and kinds.count("total") == 1
    assert ("centre" in kinds) == (name in MOVING)


def test_the_fragment_holds_the_three_families_for_the_one_universe():
    """The fragment appended to the shipped universe file gives the generator's universe of the
    day the source lands: the shipped part untouched, the three families after it, no second
    universe file in the folder (record 2075)."""
    module = generator()
    shipped = json.loads(SHIPPED_UNIVERSE.read_text(encoding="utf-8"))
    added = entries()
    assert [entry["name"] for entry in added] == list(FAMILIES)
    merged = module.universe_document(module.SCALE, module.TABLE_CAP)
    assert set(merged) == set(shipped) == {"integers", "families"}
    assert merged["integers"] == shipped["integers"]
    assert merged["families"] == shipped["families"] + added
    assert not set(entry["name"] for entry in added) & set(
        entry["name"] for entry in shipped["families"]
    )
    assert not (FOLDER / "universe.json").exists()
    field, table, control = added
    for entry in added:
        assert entry["parts"] == [1] and entry["phase"] == 2 and entry["pair"] == [1000, 1019]
        assert entry["reads"] == [] and entry["self_source"] == {"unit": 0}
        assert set(entry) <= {
            "name",
            "sign",
            "parts",
            "phase",
            "pair",
            "quantum",
            "reads",
            "self_source",
            "sourced",
        }
    assert "sourced" not in control and "sourced" in field and "sourced" in table


def test_the_source_is_declared_as_the_ledger_names_it():
    """`sourced` {of, weight, scale, cap}: of a record family (its pair the body's), the weight a
    nonzero integer, the scale E_s an integer from 1, the cap an integer from 1 on the table form
    alone; the scale the generator's one integer (SCALE)."""
    module = generator()
    shipped = json.loads(SHIPPED_UNIVERSE.read_text(encoding="utf-8"))
    field, table, _control = entries()
    for entry in (field, table):
        sourced = entry["sourced"]
        assert set(sourced) <= SOURCED_KEYS and {"of", "weight", "scale"} <= set(sourced)
        record = next(item for item in shipped["families"] if item["name"] == sourced["of"])
        assert record["pair"] == "body"
        assert isinstance(sourced["weight"], int) and sourced["weight"] != 0
        assert isinstance(sourced["scale"], int) and sourced["scale"] >= 1
        assert sourced["scale"] == module.SCALE == 18910
    assert "cap" not in field["sourced"]
    assert isinstance(table["sourced"]["cap"], int) and table["sourced"]["cap"] == module.TABLE_CAP >= 1


def test_every_shipped_world_is_the_generators_and_carries_no_pin():
    shipped = {path.stem for path in FOLDER.glob("*.json")}
    assert shipped == set(NAMES) | {"universe_entries"}
    assert not (FOLDER / "expectations.json").exists() and not list(FOLDER.glob("*.pins.json"))


def test_the_record_count_and_the_table_are_the_algebras_integers():
    """D_i = p_i^2 (2 b - a) div b at the seed's symmetric point (ALGEBRA.md #the-paces with the clock
    [a, b]); s_i = D_i div E_s; the table s_cap D_i div (s_cap E_s + D_i) (ALGEBRA.md #the-paces)."""
    import numpy as np

    module = generator()
    profile = np.array([[[0, 3, 4096]]], dtype=np.int64)
    clock = [1978960, 1048576]  # 2 cos omega = a / b, the rest world's mode
    record = module.record_count(profile, clock)
    a, b = clock
    assert [int(v) for v in record.ravel()] == [0, 9 * (2 * b - a) // b, 4096 * 4096 * (2 * b - a) // b]
    assert int(record.ravel()[2]) == 1891072
    plain = module.counts(record, 18910, None)
    table = module.counts(record, 18910, 60)
    assert plain.tolist() == [[[0, 0, 100]]]
    assert table.tolist() == [[[0, 0, (60 * 1891072) // (60 * 18910 + 1891072)]]] == [[[0, 0, 37]]]


@pytest.mark.xfail(
    strict=True,
    reason="the loader requires the old form's world keys N, age_bound, body_record, clock_stamp "
    "and massive_record, which the loop still reads (Main Loop's next piece on #1198, #1194's "
    "b-marks); the mark comes off when those reads go",
)
@pytest.mark.parametrize("name", NAMES)
def test_the_source_worlds_load_lawful(name):
    parse_nature_beam_world(document(name))
