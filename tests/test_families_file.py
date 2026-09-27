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

from event_universe import world_files
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import families_file_entries, input_stamp, parse_nature_beam_world
from tests.running import refused
from tests.worlds import FILE, emitter_world, on_the_file

ROOT = Path(__file__).resolve().parents[1]
ATTRIBUTES = {"name", "parts", "phase", "pair", "reads", "self_source"}


def test_the_file_holds_the_integers_and_three_families_as_laws_and_every_world_names_it():
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    assert "law" not in document  # one engine, no name and no version (record 2128)
    table = document["integers"].pop("twist_table")
    assert document["integers"] == {
        "node_clock": 10000,
        "amplitude_bound": 1 << 20,
        "Lambda": 1,
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
        # a world of the engine; the check-mode worlds (Nature24's generator, ahead of the
        # audit of ALGEBRA.md 9.90 (3)) carry none of the keys the loader still requires
        # the check-mode worlds and the source verb's run files (Nature24's generators, ahead of
        # the loader's words: `readings`, `sourced`, the residue keys) carry keys the loader
        # does not read yet; tests/test_check_mode_worlds.py and tests/test_source_worlds.py
        # read their structure and hold their load as expected failures
        ahead = {"check_mode", "source"}
        if isinstance(text, dict) and "universe" in text and not ahead & set(path.parts):
            assert text["universe"] == FILE, path
            assert "node_clock" not in text and "amplitude_bound" not in text, path
            world = parse_nature_beam_world(text)
            assert world.universe_file == FILE and world.node_clock == 10000
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


def test_the_file_and_the_inline_list_step_bit_for_bit(tmp_path, monkeypatch):
    inline = emitter_world(stock=2, ticks=300)
    # the shipped file's three entries with the test world's own integers (its A is 2^22, the
    # shipped file's 2^20), written as a families file of the test's root
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    document["integers"]["node_clock"] = inline["node_clock"]
    document["integers"]["amplitude_bound"] = inline["amplitude_bound"]
    (tmp_path / "universe.json").write_text(json.dumps(document), encoding="utf-8")
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    a = DetectorLawSimulation(parse_nature_beam_world(inline))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    moved = on_the_file(inline, [512, 1])
    moved["universe"] = "universe.json"
    moved["engine"] = "start.json"
    moved["stamp"] = input_stamp(moved)
    b = DetectorLawSimulation(parse_nature_beam_world(moved))
    assert b.world.universe_file == "universe.json" and a.world.universe_file is None
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


def test_every_family_renamed_adversarially_in_the_whole_universe_file_runs_bit_for_bit(
    tmp_path, monkeypatch
):
    """ITEM 53's ADVERSARIAL TEST OVER THE WHOLE UNIVERSE FILE (the Boss's record 2128 (1)): a copy
    of examples/events/universe.json with every family renamed to another family's word (gravity
    to "matter", the charge to "gravity", matter to "charge") and every read, body, stock,
    emitter and detector of the shipped light clock renamed with it runs 120 intervals bit for
    bit with the original: the rows, the remainders, the held levels and every line (the
    family's word on a line the renamed one). The engine reads no family's name (HOST; no pin)."""
    rename = {"gravity": "matter", "charge": "gravity", "matter": "charge"}
    universe = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    for entry in universe["families"]:
        entry["name"] = rename[entry["name"]]
        for read in entry["reads"]:
            read["family"] = rename[read["family"]]
    (tmp_path / "universe.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    clock = json.loads((ROOT / "examples/events/massive_record/light_clock.json").read_text())
    a = DetectorLawSimulation(parse_nature_beam_world(clock))
    renamed = json.loads(json.dumps(clock))
    for entry in renamed["measured"]:
        entry["family"] = rename[entry["family"]]
        if "stocks" in entry:
            entry["stocks"] = {rename[k]: v for k, v in entry["stocks"].items()}
        if "emitter" in entry:
            entry["emitter"]["family"] = rename[entry["emitter"]["family"]]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    renamed["universe"] = "universe.json"
    renamed["engine"] = "start.json"
    renamed["stamp"] = input_stamp(renamed)
    b = DetectorLawSimulation(parse_nature_beam_world(renamed))
    assert [family.name for family in b.families] == [rename[f.name] for f in a.families]
    lines_a: list[dict] = []
    lines_b: list[dict] = []
    a.record, b.record = lines_a.append, lines_b.append
    for _ in range(120):
        a.step()
        b.step()
    assert (
        lines_a
        and [
            {**line, "family": rename[line["family"]]} if "family" in line else line for line in lines_a
        ]
        == lines_b
    )
    assert set(a.records) == set(b.records)
    for identity, live in a.records.items():
        other = b.records[identity]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.before, other.before)
        assert np.array_equal(live.remainder, other.remainder)
    for family_a, record in a.held_records.items():
        family_b = [f.name for f in b.families].index(rename[a.families[family_a].name])
        assert np.array_equal(record.now, b.held_records[family_b].now)
    books_a, books_b = a.books(), b.books()
    assert a.held == b.held
    assert {rename[k]: v for k, v in books_a.pop("families").items()} == books_b.pop("families")
    assert books_a == books_b


def test_the_loader_refuses_the_files_defects_and_the_worlds_second_copy(tmp_path, monkeypatch):
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    second = json.loads(json.dumps(document))
    second["node_clock"] = 10000
    refused(second, "the world declares node_clock, which the engine never reads")
    ray = json.loads(json.dumps(document))
    ray["detector_law"] = False  # the flag was the law's name: refused by name (9.90 (1))
    refused(ray, "the world.detector_law is refused: one engine")
    missing = json.loads(json.dumps(document))
    missing["universe"] = "examples/events/nowhere.json"
    refused(missing, "no file at the repository's root")
    # the file's own defects, one at a time
    good = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    document["engine"] = "start.json"
    document["universe"] = "universe.json"

    def refuses(change, match):
        broken = json.loads(json.dumps(good))
        change(broken)
        (tmp_path / "universe.json").write_text(json.dumps(broken), encoding="utf-8")
        refused(json.loads(json.dumps(document)), match)

    refuses(lambda d: d["integers"].pop("node_clock"), "integers must hold exactly")
    refuses(lambda d: d["integers"].pop("Lambda"), "integers must hold exactly")
    refuses(lambda d: d["families"][0].pop("parts"), r"families\[0\] lacks keys: parts")
    refuses(lambda d: d["families"][0].__setitem__("parts", [3]), "parts must be one of")
    refuses(lambda d: d["families"][0].__setitem__("phase", 3), "phase must be 1 or 2")
    # the self-source's unit (9.91 (5); commit 6): 0, or at least 24 A
    refuses(lambda d: d["families"][0]["self_source"].__setitem__("unit", 24), "is below 24 A")
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
    refuses(lambda d: d.__setitem__("law", "beam-v1"), "the universe file .* has unknown keys: law")
    (tmp_path / "universe.json").write_text(json.dumps(good), encoding="utf-8")
    document["stamp"] = input_stamp(document)
    assert parse_nature_beam_world(document).universe_file == "universe.json"


def test_the_given_clock_is_the_emitters_when_the_family_declares_none():
    document = on_the_file(emitter_world(stock=1, ticks=10), [512, 1])
    world = parse_nature_beam_world(document)
    emitter = world.measured[0].block.emitter  # type: ignore[union-attr]
    assert emitter is not None and emitter.clock == (512, 1)
    assert emitter.train is None and emitter.weight == 3  # the window's (commit 7; the train retired)
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
    names = {family["name"]: family for family in giving_matter["universe"]}
    names["matter"]["pair"] = "body"
    giving_matter["universe"].append(
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
    body["stocks"] = {"matter": 1}
    body["emitter"]["family"] = "matter"
    body["emitter"]["clock"] = [512, 1]
    refused(giving_matter, r"measured\[0\]\.emitter\.pair is required: the given family 'matter'")
    inline_pair = emitter_world(stock=1, ticks=10)
    inline_pair["measured"][0]["emitter"]["pair"] = [1, 1]
    refused(inline_pair, r"measured\[0\]\.emitter\.pair is refused: the given family 'light' declares")
