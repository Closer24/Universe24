"""THE ONE FAMILIES FILE WITH ITS THREE ENTRIES (ALGEBRA.md 9.83 (2), 9.85 (3), 9.86 (2), 9.91
(7); the model owner's record 2075 through the Boss, "in every experiment we put all the
families into action"; the one stroke of record 2106, commit 1; BUILD.md section 26 items 59
and 60): (1) examples/events/families.json holds the universe's integers and three families as
laws, gravity [1, 3, 6], the charge [1, 3] with light as its wave and matter [1] with the pair
on every body; every shipped world of the detector law names it as `families` and declares no
node_clock and no amplitude_bound of its own; (2) the loader translates the file's entries and
refuses by name a missing key, a wrong parts list, a phase other than 1 or 2, a self-source
unit other than 0, an entry with neither held nor clicks, a read's weight word the universe
does not name, and a world that names the file under the ray law or beside its own integers;
(3) the light record's clock is its emitter's: `clock` on the emitter, required when the given
family declares none and refused when it does; (4) a body of matter declares its `kind`, the
emitter of matter its `pair`, refused where the family declares one; (5) a small world built
on the file's three entries and the same world with the tests' four-family inline list step
bit for bit. HOST; no physics, no pin."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events import world as loader
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import families_file_entries, input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
FILE = "examples/events/families.json"
ATTRIBUTES = {"name", "parts", "phase", "pair", "reads", "self_source"}


def refused(document: dict, match: str) -> None:
    document["input"] = input_stamp(document)
    with pytest.raises(ValueError, match=match):
        parse_nature_beam_world(document)


def test_the_file_holds_the_integers_and_three_families_as_laws_and_every_world_names_it():
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    assert document["law"] == "detector-law-v1"
    table = document["integers"].pop("twist_table")
    assert document["integers"] == {
        "node_clock": 10000,
        "amplitude_bound": 1 << 20,
        "charge_weight": 1,
        "momentum_unit": 64,
    }
    # the twist table (ALGEBRA.md 9.96 (2) (c); commit 4): the unit 4 Gamma 2^16, 2^10 fine
    # and 2^15 coarse triples, every one c^2 + s^2 = d^2 with d at most 10^9
    assert table["unit"] == 4 * 10000 * 65536
    assert len(table["fine"]) == 1024 and len(table["coarse"]) == 32768
    assert all(c * c + s * s == d * d and d <= 10**9 for c, s, d in table["fine"] + table["coarse"])
    document["integers"]["twist_table"] = table
    names = [entry["name"] for entry in document["families"]]
    assert names == ["gravity", "charge", "matter"]
    gravity, charge, matter = document["families"]
    for entry in document["families"]:
        assert ATTRIBUTES <= set(entry) and entry["self_source"] == {"unit": 0}
        assert "held" in entry or "clicks" in entry
        assert "booked" not in entry and "quantum" not in entry and "charge" not in entry
    # gravity: ten components, one level, held content with the factors (1, 4, 2) and the spin's
    # dipole, no reads, no clicks (9.91 (7))
    assert gravity["parts"] == [1, 3, 6] and gravity["phase"] == 1 and gravity["pair"] == [1, 1]
    assert gravity["held"] == {"count": "content", "factors": [1, 4, 2], "dipole": "spin"}
    assert gravity["reads"] == [] and "clicks" not in gravity
    # the charge: four components, two levels, held sign with the moment's dipole halved, reads
    # gravity, and clicks: light is its wave
    assert charge["parts"] == [1, 3] and charge["phase"] == 2 and charge["pair"] == [1, 1]
    assert charge["held"] == {"count": "sign", "factors": [1, 1], "dipole": "moment", "dipole_div": 2}
    assert charge["reads"] == [{"family": "gravity", "weight": 1, "twist": "own", "by": 1}]
    assert charge["clicks"] == {"gives": True, "takes": True, "quantum": 1}
    # matter: a scalar, two levels, the pair on every body, reads gravity and the charge at
    # Lambda by its sign, clicks
    assert matter["parts"] == [1] and matter["phase"] == 2 and matter["pair"] == "body"
    assert "held" not in matter and matter["clicks"] == {"gives": True, "takes": True, "quantum": 1}
    assert matter["reads"] == [
        {"family": "gravity", "weight": 1, "twist": "own", "by": 1},
        {"family": "charge", "weight": "Lambda", "twist": "own", "by": "q"},
    ]
    entries, integers = families_file_entries(FILE)
    assert integers == document["integers"] and len(entries) == 3
    assert entries[0]["held"] == "content" and entries[1]["held"] == "sign" and "held" not in entries[2]
    assert entries[2]["reads"][1] == {"family": "charge", "weight": 1, "by": "sign", "twist": "own"}
    for path in (ROOT / "examples/events").glob("*/*.json"):
        text = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(text, dict) and text.get("detector_law") is True:
            assert text["families"] == FILE, path
            assert "node_clock" not in text and "amplitude_bound" not in text, path
            world = parse_nature_beam_world(text)
            assert world.families_file == FILE and world.node_clock == 10000
            assert [family.name for family in world.families] == names
            gravity_family, charge_family, matter_family = world.families
            assert gravity_family.parts == (1, 3, 6) and gravity_family.components == 10
            assert gravity_family.held == "content" and gravity_family.clicks is None
            assert not gravity_family.booked and gravity_family.held_factors == (1, 4, 2)
            assert charge_family.parts == (1, 3) and charge_family.held == "sign"
            assert charge_family.clicks == (True, True) and charge_family.booked
            assert matter_family.pair_on_body and matter_family.massive_kind and matter_family.booked
            for entry in world.measured:
                if entry.block is not None and entry.family == 2:
                    assert entry.block.kind[1] > entry.block.kind[0]


def on_the_file(document: dict, clock: list[int]) -> dict:
    """The emitter world moved onto the families file: the path, no integers of its own, the
    given clock on the emitter; light is the charge family (9.86 (2) (b)), the emitter body of
    matter with its kind (9.91 (7))."""
    moved = json.loads(json.dumps(document))
    names = {family["name"]: family for family in moved["families"]}
    moved["families"] = FILE
    del moved["node_clock"]
    del moved["amplitude_bound"]
    del moved["momentum_unit"]
    for entry in moved["measured"]:
        if entry["family"] == "light":
            entry["family"] = "charge"
        if entry["family"] == "matter":
            entry["kind"] = list(names["matter"]["pair"])
        if "light" in entry.get("held", {}):
            entry["held"] = {"charge": entry["held"]["light"]}
        if "emitter" in entry:
            entry["emitter"]["clock"] = clock
            if entry["emitter"]["family"] == "light":
                entry["emitter"]["family"] = "charge"
            # the light's component along the body's moment (ALGEBRA.md 9.82 (3) (d); commit 4)
            entry["moment"] = [0, 0, 1]
    moved["input"] = input_stamp(moved)
    return moved


def test_the_file_and_the_inline_list_step_bit_for_bit(tmp_path, monkeypatch):
    inline = emitter_world(stock=2, ticks=300)
    # the shipped file's three entries with the test world's own integers (its A is 2^22, the
    # shipped file's 2^20), written as a families file of the test's root
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    document["integers"]["node_clock"] = inline["node_clock"]
    document["integers"]["amplitude_bound"] = inline["amplitude_bound"]
    (tmp_path / "families.json").write_text(json.dumps(document), encoding="utf-8")
    (tmp_path / "start.json").write_text(
        json.dumps({"law": "detector-law-v1", "mode": "check"}), encoding="utf-8"
    )
    a = DetectorLawSimulation(parse_nature_beam_world(inline))
    monkeypatch.setattr(loader, "REPOSITORY_ROOT", tmp_path)
    moved = on_the_file(inline, [512, 1])
    moved["families"] = "families.json"
    moved["engine"] = "start.json"
    moved["input"] = input_stamp(moved)
    b = DetectorLawSimulation(parse_nature_beam_world(moved))
    assert b.world.families_file == "families.json" and a.world.families_file is None
    names_a = [family.name for family in a.families]
    names_b = [family.name for family in b.families]
    rename = {"light": "charge", "clicks": "gravity"}
    lines_a: list[dict] = []
    lines_b: list[dict] = []
    a.record, b.record = lines_a.append, lines_b.append
    for _ in range(300):
        a.step()
        b.step()
    renamed = [
        {**line, "family": rename.get(line["family"], line["family"])} if "family" in line else line
        for line in lines_a
    ]
    assert set(a.records) == set(b.records) and renamed == lines_b and len(lines_a) > 0
    for identity, live in a.records.items():
        other = b.records[identity]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
        assert names_b[other.family] == rename.get(names_a[live.family], names_a[live.family])
    for source in ("content", "sign"):
        assert np.array_equal(a.level_of(source), b.level_of(source))
    # every other part with no source stays exactly zero and silent (9.91 (9) (a)); the
    # light emitter's moment [0, 0, 1] writes the charge's dipole on its neighbours (9.82
    # (3) (d), 9.91 (3); commit 4), which nothing reads at q = 0
    for family, parts in b.held_parts.items():
        for record in parts:
            if record.silent:
                assert not record.now.any() and not record.remainder.any()
            else:
                assert b.families[family].held == "sign" and record.part in (1, 2)
    assert b.leaks() == []


def test_the_loader_refuses_the_files_defects_and_the_worlds_second_copy(tmp_path, monkeypatch):
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    second = json.loads(json.dumps(document))
    second["node_clock"] = 10000
    refused(second, "the world declares node_clock, which the detector law never reads")
    ray = json.loads(json.dumps(document))
    ray["detector_law"] = False
    del ray["engine"]
    refused(ray, "families as a file path is admitted under `detector_law` alone")
    missing = json.loads(json.dumps(document))
    missing["families"] = "examples/events/nowhere.json"
    refused(missing, "no file at the repository's root")
    # the file's own defects, one at a time
    good = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    monkeypatch.setattr(loader, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "start.json").write_text(
        json.dumps({"law": "detector-law-v1", "mode": "check"}), encoding="utf-8"
    )
    document["engine"] = "start.json"
    document["families"] = "families.json"

    def refuses(change, match):
        broken = json.loads(json.dumps(good))
        change(broken)
        (tmp_path / "families.json").write_text(json.dumps(broken), encoding="utf-8")
        refused(json.loads(json.dumps(document)), match)

    refuses(lambda d: d["integers"].pop("node_clock"), "integers must hold exactly")
    refuses(lambda d: d["integers"].pop("charge_weight"), "integers must hold exactly")
    refuses(lambda d: d["families"][0].pop("parts"), r"families\[0\] lacks keys: parts")
    refuses(lambda d: d["families"][0].__setitem__("parts", [3]), "parts must be one of")
    refuses(lambda d: d["families"][0].__setitem__("phase", 3), "phase must be 1 or 2")
    refuses(
        lambda d: d["families"][0]["self_source"].__setitem__("unit", 24), "self_source.unit must be 0"
    )
    refuses(lambda d: d["families"][0].pop("held"), "declares neither held")
    refuses(
        lambda d: d["families"][2].__setitem__("pair", "mine"), r"pair must be \[num, den\] or the word"
    )
    refuses(
        lambda d: d["families"][2]["reads"][1].__setitem__("weight", "Mu"),
        "names no integer of the universe",
    )
    refuses(lambda d: d["families"][2]["reads"][1].__setitem__("by", 2), r'by must be 1 or "q"')
    refuses(lambda d: d["families"][0]["held"].__setitem__("factors", [1, 4]), "held_factors must be 3")
    refuses(
        lambda d: d["families"][0]["held"].__setitem__("dipole", "twist"), "held_dipole must be one of"
    )
    refuses(lambda d: d.__setitem__("law", "beam-v1"), "declares law 'beam-v1'")
    (tmp_path / "families.json").write_text(json.dumps(good), encoding="utf-8")
    document["input"] = input_stamp(document)
    assert parse_nature_beam_world(document).families_file == "families.json"


def test_the_given_clock_is_the_emitters_when_the_family_declares_none():
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    world = parse_nature_beam_world(document)
    emitter = world.measured[0].block.emitter  # type: ignore[union-attr]
    assert emitter is not None and emitter.clock == (512, 1) and emitter.train is not None
    assert emitter.train.clock == (512, 1) and emitter.train.wavelength == 4
    assert emitter.pair == (1, 1)  # the charge family's declared pair, light's kind
    without = json.loads(json.dumps(document))
    del without["measured"][0]["emitter"]["clock"]
    refused(
        without,
        r"measured\[0\]\.emitter\.clock is required: the given family 'charge' declares no clock",
    )
    inline = emitter_world(stock=1, ticks=10)
    inline["measured"][0]["emitter"]["clock"] = [512, 1]
    refused(
        inline, r"measured\[0\]\.emitter\.clock is refused: the given family 'light' declares its own"
    )


def test_the_bodys_kind_and_the_emitters_pair_stand_where_the_family_declares_no_pair():
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    world = parse_nature_beam_world(document)
    body = world.measured[0]
    assert body.block is not None and body.block.kind == (800, 809) and body.block.pair == (800, 801)
    without = json.loads(json.dumps(document))
    del without["measured"][0]["kind"]
    refused(without, r"measured\[0\]\.kind is required: the family 'matter' declares no pair")
    light_kind = json.loads(json.dumps(document))
    light_kind["measured"][0]["kind"] = [809, 800]
    refused(light_kind, r"measured\[0\]\.kind \[809, 800\] is no massive kind")
    inline = emitter_world(stock=1, ticks=10)
    inline["measured"][0]["kind"] = [800, 809]
    refused(inline, r"measured\[0\]\.kind is refused: the family 'matter' declares its pair")
    # an emitter giving a family whose pair is the body's declares the given record's pair: on
    # an inline list, a body of a second massive kind giving matter (under the three entries a
    # body of matter cannot give matter, its own family; ALGEBRA.md 9.85 (7) waits)
    giving_matter = emitter_world(stock=1, ticks=10)
    names = {family["name"]: family for family in giving_matter["families"]}
    names["matter"]["pair"] = "body"
    giving_matter["families"].append(
        {
            "name": "heavy",
            "quantum": 1,
            "pair": [1600, 1618],
            "charge": 0,
            "reads": names["matter"]["reads"],
        }
    )
    body = giving_matter["measured"][0]
    body["family"] = "heavy"
    body["held"] = {"matter": 1}
    body["emitter"]["family"] = "matter"
    body["emitter"]["clock"] = [512, 1]
    refused(giving_matter, r"measured\[0\]\.emitter\.pair is required: the given family 'matter'")
    inline_pair = emitter_world(stock=1, ticks=10)
    inline_pair["measured"][0]["emitter"]["pair"] = [1, 1]
    refused(inline_pair, r"measured\[0\]\.emitter\.pair is refused: the given family 'light' declares")
