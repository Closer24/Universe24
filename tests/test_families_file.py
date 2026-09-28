"""THE ONE FAMILIES FILE WITH ITS THREE ENTRIES (ALGEBRA.md #a-familys-declaration, #the-primitives, #the-interval; record 2075): every shipped world names examples/events/universe.json; the loader refuses its defects by name; the emitter's clock and the body's kind stand where the family declares none. HOST; no pin."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from event_universe import world_files
from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.loader import derived, frame
from event_universe.world_files import input_stamp, parse_nature_beam_world, read_repository_json
from tests.running import refused
from tests.worlds import FILE, emitter_specimen, family_entry, on_the_file

ROOT = Path(__file__).resolve().parents[1]
ATTRIBUTES = {"name", "m", "pair", "held", "clock", "spins_step"}  # the file's rows; the rest derives


def test_the_file_holds_the_integers_and_three_families_as_laws_and_every_world_names_it():
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    assert "law" not in document  # one engine, no name and no version (record 2128)
    table = document["integers"].pop("twist_table")
    expected = dict(node_clock=10000, momentum_unit=64, most_steps=65536, width=63, most_families=20)
    assert document["integers"] == {
        **expected,
        "least_residues": 500,
    }  # the owner's two numbers, in the file
    # the twist table (ALGEBRA.md #the-primitives; commit 4): the unit 4 Gamma 2^16, 2^10 fine and 2^15 coarse triples, every one c^2 + s^2 = d^2 with d at most 10^9
    assert table["unit"] == 4 * 10000 * 65536
    assert len(table["fine"]) == 1024 and len(table["coarse"]) == 32768
    assert all(c * c + s * s == d * d and d <= 10**9 for c, s, d in table["fine"] + table["coarse"])
    document["integers"]["twist_table"] = table
    names = [entry["name"] for entry in document["families"]]
    assert names == ["gravity", "charge", "matter"]
    gravity, charge, matter = document["families"]
    # THE FAMILIES FROM THE RULE: the file holds the rows of the five numbers and nothing the rule derives
    assert all(set(entry) <= ATTRIBUTES for entry in document["families"])
    spins = {"curl": [1, 4], "tidal": [3, 4]}
    held, moment = {"count": "content", "divisor": 40000}, {"count": "sign", "divisor": 40000}
    assert gravity == {"name": "gravity", "pair": [1, 1], "held": held, "spins_step": spins}
    assert charge == {"name": "charge", "pair": [1, 1], "clock": [512, 1], "held": moment}
    assert matter == {"name": "matter", "pair": "body"}
    entries, integers = frame.universe(FILE, {FILE: read_repository_json(FILE)}, discover())
    # the frame reads the table's lists as tuples (core/schema.py); the same numbers
    assert json.loads(json.dumps(integers)) == document["integers"] and len(entries) == 3
    gravity, charge, matter = (derived.filled(entry, entries, 10000) for entry in entries)
    # gravity rank 3 and real; the charge rank 2 with clicks (light its wave); matter a scalar of quanta
    assert gravity["parts"] == [1, 3, 6] and gravity["phase"] == 1 and "clicks" not in gravity
    assert gravity["pair"] == [1, 1] == charge["pair"]  # the pair as written (THE WALL IS ONE)
    spin = {"count": "content", "divisor": 40000, "factors": [1] * 3, "dipole": "spin", "dipole_div": 1}
    moment = {"count": "sign", "divisor": 40000, "factors": [1, 1], "dipole": "moment", "dipole_div": 2}
    assert gravity["held"] == spin and gravity["reads"] == []
    assert charge["parts"] == [1, 3] and charge["phase"] == 2 and charge["held"] == moment
    assert charge["reads"] == [{"family": "gravity", "weight": 1, "twist": "own", "by": 1}]
    assert charge["clicks"] == {"gives": True, "takes": True, "quantum": 1} == matter["clicks"]
    assert matter["parts"] == [1] and matter["phase"] == 2 and "held" not in matter
    charge_read = {"family": "charge", "weight": 1, "twist": "own", "by": "q"}
    assert matter["reads"] == [charge["reads"][0], charge_read]
    for path in (ROOT / "examples/events").glob("*/*.json"):
        if path.name.endswith((".mode.json", ".expectation.json")):  # the tool's files beside a world
            continue
        text = json.loads(path.read_text(encoding="utf-8"))
        # a world of the engine; the check-mode worlds (Nature24's generator, ahead of the audit of ALGEBRA.md #the-primitives) carry none of the keys the loader still requires the check-mode worlds and the source verb's run files (Nature24's generators, ahead of the loader's words: `readings`, `sourced`, the residue keys) carry keys the loader does not read yet; tests/test_source_worlds.py reads their structure
        ahead = {"check_mode", "generated", "source"}
        if isinstance(text, dict) and "universe" in text and not ahead & set(path.parts):
            assert text["universe"] == FILE, path
            assert "node_clock" not in text and "amplitude_bound" not in text, path
            world = parse_nature_beam_world(text)
            assert world.universe_file == FILE and world.node_clock == 10000
            assert [family.name for family in world.families] == names
            gravity_family, charge_family, matter_family = world.families
            assert gravity_family.parts == (1, 3, 6) and gravity_family.components == 10
            assert gravity_family.held == "content" and gravity_family.clicks is None
            assert not gravity_family.booked and gravity_family.held_factors == (1, 1, 1)
            assert charge_family.parts == (1, 3) and charge_family.held == "sign"
            assert charge_family.clicks == (True, True) and charge_family.booked
            assert matter_family.pair_on_body and matter_family.massive_kind and matter_family.booked
            for entry in world.measured:
                if entry.block is not None and entry.family == 2:
                    assert entry.block.kind[1] > entry.block.kind[0]


def test_the_rules_own_universe_loads_beside_the_universe_of_record_and_a_pixel_world_on_it():
    """THE RULE'S OWN UNIVERSE (ALGEBRA.md; the owner's word of 2026-09-28, 15:11 Israel: Gamma = 24, a whole universe in small): examples/events/planck.json holds Gamma = 24 (a multiple of 6; the horizon 12, the pixels 6 to 11), T = 1, and three rows in pairs over Gamma: gravity [24, 24] content at the divisor 1, charge [24, 24] sign at the divisor 36 (0.86 (Gamma / 2)^(3 / 2), one quantum per window, derived from Gamma), matter [16, 24]; the least residues 1 (light's pair leaves one remainder value at Gamma = 24); nothing else. THE FINDING (Nature24, 15:30 Israel): the width's amplitude unit at Gamma = 24 is A = 37,066,663,599,756 (the wall 6 Gamma^3 = 82,944), so the transport's total 3 d_1 d_0 (A + 1) admits d_1 d_0 below 83,000 and no table of the tool's form (its triples reach d = 10^9) loads; the file carries the identity table [1, 0, 1] alone, so it loads and a nonzero twist is refused by name at the step until the mathematician's line on A at a small Gamma. A world of three pixels (one Node each) on it loads with the ranks derived and THE SIGN IS THE BODY'S: the sign's source at a pixel's Node is its q times its count. A PAIR'S NUMERATOR MAY BE NEGATIVE: the third [-12, 24] on an inline list loads as the mirror band; den at or below |num| and den 0 are refused by name."""
    planck = "examples/events/planck.json"
    table = (document := json.loads((ROOT / planck).read_bytes()))["integers"].pop("twist_table")
    units = dict(node_clock=24, quantum_action=1, momentum_unit=64, most_steps=65536, width=63)
    assert document["integers"] == {**units, "most_families": 20, "least_residues": 1}
    assert table == {"unit": 4 * 24 * 65536, "fine": [[1, 0, 1]], "coarse": [[1, 0, 1]]}  # the finding
    assert [f["name"] for f in document["families"]] == ["gravity", "charge", "matter"]
    assert [f["pair"] for f in document["families"]] == [[24, 24], [24, 24], [16, 24]]
    assert [f.get("held", {}).get("divisor") for f in document["families"]] == [1, 36, None]
    assert all(set(f) <= {"name", "pair", "held"} for f in document["families"])  # no spins_step
    world = {"shape": [40, 1, 1], "boundary": {"x": "closed", "y": "periodic", "z": "periodic"}, "N": 64}
    world |= {"ticks": 10, "face_depth": 1, "engine": "examples/events/engine_start.json"}
    world |= {"universe": planck, "detectors": [{"name": "taker", "block": 2}]}
    n, at = {"momentum": [0] * 3, "momentum_before": [0] * 3}, ((10, 8, 1), (20, 6, -1), (30, 8, 0))
    node = lambda x, c: [{"node": [x, 0, 0], "count": c}]  # noqa: E731
    bodies = [{"family": "matter", "nodes": node(x, c), "q": q, **n} for x, c, q in at]
    loaded = parse_nature_beam_world({**world, "measured": bodies})  # three pixels, count in [6, 12)
    ranks = [("gravity", (1, 3, 6), "content"), ("charge", (1, 3), "sign"), ("matter", (1,), None)]
    assert [(f.name, f.parts, f.held) for f in loaded.families] == ranks
    assert loaded.families[2].pair == (16, 24) and (A := loaded.amplitude_bound) > 0
    assert 384 * A * A <= derived.MAX_WORK_INT - 10 < 384 * (A + 1) ** 2  # the count's line's, w 16
    assert [entry.block.q for entry in loaded.measured if entry.block is not None] == [1, -1, 0]
    simulation = DetectorLawSimulation(loaded)
    signs = [simulation.node_sources(number, "sign") for number in range(3)]
    assert signs == [[((10, 0, 0), 8)], [((20, 0, 0), -6)], [((30, 0, 0), 0)]]
    assert [simulation._body_charge(number) for number in range(3)] == [8, -6, 0]
    six = {**world, "universe": "examples/events/planck_6000.json", "measured": bodies}  # after 24
    assert parse_nature_beam_world(six).families[2].pair == (4000, 6000)  # Gamma 6,000, the record's
    inline = {**world, "measured": bodies, "node_clock": 24, "momentum_unit": 64, "twist_table": table}
    inline["universe"] = [*document["families"], third := {"name": "third", "pair": [-12, 24]}]
    f, least = [[1, 0, 1], [1999, 1998000, 1998001]], derived.MAX_WORK_INT // (3 * 1998001**2) - 1
    w = parse_nature_beam_world({**inline, "twist_table": {**table, "fine": f, "coarse": f}})
    assert (w.families[3].pair, w.amplitude_bound) == ((-12, 24), least)  # a wide table: the transport's
    six = parse_nature_beam_world({**inline, "node_clock": [24, 6]})  # GAMMA IS NOT CONSTANT: a pair
    assert (six.node_clock, six.clock_step, six.families[3].pair) == (24, 6, (-12, 24))
    pairs = [f.pair for f in six.families]  # light and the sign +6, matter +4, the third -3 per interval
    assert derived.clock_at(pairs, 24, 6, 1) == (30, [(30, 30), (30, 30), (20, 30), (-15, 30)])
    odd = [*document["families"], {**third, "pair": [23, 24]}]  # the electron's band at a stepping Gamma
    refused({**inline, "node_clock": [24, 6], "universe": odd}, "does not step with the clock")
    for clock in ([0, 6], [24, -1], [24, 6, 1], [24, 6.0]):
        refused({**inline, "node_clock": clock}, "node_clock")
    for pair, match in (([-24, 24], r"den from 1, and den > \|num\|"), ([1, 0], "den from 1")):
        refused({**inline, "universe": [*document["families"], {**third, "pair": pair}]}, match)


def test_the_file_and_the_inline_list_step_bit_for_bit(tmp_path, monkeypatch):
    inline = emitter_specimen(stock=2, ticks=300)
    # the shipped file's three entries with the test world's own integers (its A is 2^22, the shipped file's 2^20), written as a families file of the test's root
    document = json.loads((ROOT / FILE).read_text(encoding="utf-8"))
    document["integers"]["node_clock"] = inline["node_clock"]
    charge = next(row for row in document["families"] if row["name"] == "charge")
    for row in inline[
        "universe"
    ]:  # the inline light holds the sign as the file's charge does: one E_s for the window's write on both sides
        if row["name"] == "light":
            row["held"] = dict(charge["held"])
    # the sign's holder is a vector family (THE FAMILIES FROM THE RULE): the giver's moment names the component
    inline["measured"][0]["moment"] = [1, 0, 0]
    inline["stamp"] = input_stamp(inline)
    (tmp_path / "universe.json").write_text(json.dumps(document), encoding="utf-8")
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    a = DetectorLawSimulation(parse_nature_beam_world(inline))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    moved = on_the_file(inline)
    moved["universe"], moved["engine"] = "universe.json", "start.json"
    moved["stamp"] = input_stamp(moved)
    b = DetectorLawSimulation(parse_nature_beam_world(moved))
    assert b.world.universe_file == "universe.json" and a.world.universe_file is None
    names_a = [family.name for family in a.families]
    names_b, rename = [family.name for family in b.families], {"light": "charge", "clicks": "gravity"}
    lines_a, lines_b = list[dict](), list[dict]()
    a.record, b.record = lines_a.append, lines_b.append
    # 60 intervals: the two worlds are one until A's first kick at 61 (the recoil at its first giving's close); from there the file's held rows, the shipped file's gravity (1, 4, 2) and charge (1, 1) and not the specimen's, carry the momentum into the fields
    for _ in range(60):
        a.step()
        b.step()
    word = lambda line: rename.get(line["family"], line["family"])  # noqa: E731
    renamed = [{**line, "family": word(line)} if "family" in line else line for line in lines_a]
    assert set(a.records) == set(b.records) and renamed == lines_b and len(lines_a) > 0
    for identity, live in a.records.items():
        other = b.records[identity]
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
        assert names_b[other.family] == rename.get(names_a[live.family], names_a[live.family])
    for source in ("content", "sign"):
        assert np.array_equal(a.level_of(source), b.level_of(source))
    # every other part with no source stays exactly zero and silent (ALGEBRA.md #the-interval); the light emitter's moment [0, 0, 1] writes the charge's dipole on its neighbours (9.82 (3) (d), ALGEBRA.md #the-interval; commit 4), which nothing reads at q = 0
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
    """Every family renamed adversarially in the whole universe file: the light clock runs bit for bit."""
    rename = {"gravity": "matter", "charge": "gravity", "matter": "charge"}
    universe = json.loads(
        (ROOT / "tests/universe_fixtures.json").read_text(encoding="utf-8")
    )  # the light clock's own universe copy (the write's divisor)
    for entry in universe["families"]:
        entry["name"] = rename[entry["name"]]
        for read in entry.get("reads", []):
            read["family"] = rename[read["family"]]
    (tmp_path / "universe.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "start.json").write_text(json.dumps({"mode": "check"}), encoding="utf-8")
    clock = json.loads((ROOT / "tests/light_clock.json").read_text())
    a, renamed = DetectorLawSimulation(parse_nature_beam_world(clock)), json.loads(json.dumps(clock))
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
    lines_a, lines_b = list[dict](), list[dict]()
    a.record, b.record = lines_a.append, lines_b.append
    for _ in range(120):
        a.step()
        b.step()
    back = [{**line, "family": rename[line["family"]]} if "family" in line else line for line in lines_a]
    assert lines_a and back == lines_b and set(a.records) == set(b.records)
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
    document = on_the_file(emitter_specimen(stock=1, ticks=10))
    second = json.loads(json.dumps(document))
    second["node_clock"] = 10000
    refused(second, "the world declares node_clock, which the engine never reads")
    ray = json.loads(json.dumps(document))
    ray["detector_law"] = False  # the flag was the law's name, refused by name (#the-primitives)
    refused(ray, "the world has unknown keys: detector_law")
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

    C = {"gives": True, "takes": True, "quantum": 2}  # noqa: N806  # a clicks card at another quantum
    H = lambda f: lambda d: f(d["families"][0]["held"])  # noqa: E731  # a change of the held row
    R = lambda **k: lambda d: d["families"][2].__setitem__("reads", [{"family": "gravity", **k}])  # noqa: E731, N806
    refuses(lambda d: d["integers"].pop("node_clock"), "integers lacks keys: node_clock")
    refuses(lambda d: d["integers"].__setitem__("Lambda", 1), r"integers has unknown keys: Lambda")
    refuses(lambda d: d["families"][2].pop("pair"), r"the family 'matter' lacks keys: m")
    # THE FAMILIES FROM THE RULE: a key the rule fixes, declared at another value, is refused by name
    refuses(
        lambda d: d["families"][0].__setitem__("parts", [1]),
        r"families\[0\]\.parts \[1\] contradicts the rule",
    )
    refuses(
        lambda d: d["families"][1].__setitem__("phase", 1),
        r"families\[1\]\.phase 1 contradicts the rule",
    )
    refuses(
        lambda d: d["families"][0].__setitem__("clicks", C),
        r"families\[0\]\.clicks .* contradicts the rule",
    )
    refuses(R(weight=2), r"families\[2\]\.reads .* contradicts the rule, which fixes")
    refuses(R(twist=0), r"families\[2\]\.reads .* contradicts the rule, which fixes")
    refuses(
        lambda d: d["families"][2].__setitem__("reads", []),
        r"families\[2\]\.reads \[\] contradicts the rule",
    )
    refuses(
        H(lambda h: h.update(factors=[1, 4, 2])), r"families\[0\]\.held\.factors \[1, 4, 2\] contradicts"
    )
    refuses(
        H(lambda h: h.update(dipole_div=2)), r"families\[0\]\.held\.dipole_div 2 contradicts the rule"
    )
    refuses(lambda d: d["families"][0].__setitem__("phase", 3), r"phase must be one of \[1, 2\], not 3")
    # the self-source's unit (ALGEBRA.md #the-interval; commit 6): 0, or at least 24 A
    refuses(lambda d: d["families"][0].__setitem__("self_source", {"unit": 24}), "is below 24 A")
    refuses(lambda d: d["families"][0]["held"].__setitem__("count", "mass"), "count must be one of")
    refuses(lambda d: d["families"][2].update(spins_step=d["families"][0]["spins_step"]), "no spin's")
    refuses(lambda d: d["families"][0].pop("name"), r"families\[0\] lacks keys: name")
    refuses(lambda d: d["families"][0].__setitem__("quantum", 0), "quantum is 0, below its least 1")
    refuses(
        lambda d: d["families"][2].__setitem__("clicks", C),
        r"families\[2\]\.clicks .* contradicts the rule",
    )
    # no default written for the dipole's divisor: the universe file writes it (the hold's card)
    refuses(H(lambda h: h.update(dipole="spin", dipole_div=0)), r"dipole_div is 0, below its least 1")
    refuses(H(lambda h: h.pop("divisor")), r"held lacks (keys: )?divisor")  # the sum's divisor E_s
    refuses(lambda d: d["families"][2].update(pair="mine"), r"pair must be a list, not 'mine'")
    refuses(R(weight="Mu"), "names 'Mu', no integer")
    refuses(R(by=2), r"by must be one of \[1, 'q'\], not 2")
    refuses(H(lambda h: h.update(dipole="twist")), r"dipole must be one of \['spin', 'moment'\]")
    good["families"][0].pop("spins_step")  # optional on the spin's holder: the file loads without it
    refuses(lambda d: d["families"][0].update(spins_step={"curl": 3}), "spins_step lacks keys: tidal")
    refuses(lambda d: d.__setitem__("law", "beam-v1"), "the universe file .* has unknown keys: law")
    (tmp_path / "universe.json").write_text(json.dumps(good), encoding="utf-8")
    document["stamp"] = input_stamp(document)
    assert parse_nature_beam_world(document).universe_file == "universe.json"


def test_the_given_clock_is_the_familys_row_and_the_emitter_declares_none():
    """The given record's clock is the given family's row's (ALGEBRA.md #the-primitives, L479): the charge row's [512, 1] on the file; `clock` on the emitter refused by name; a given family whose row declares none refused by name."""
    document = on_the_file(emitter_specimen(stock=1, ticks=10))
    world = parse_nature_beam_world(document)
    emitter = world.measured[0].block.emitter  # type: ignore[union-attr]
    assert emitter is not None and emitter.clock == (512, 1)
    assert emitter.weight == 3  # the window's (commit 7; the train retired)
    assert emitter.pair == (1, 1)  # the charge family's declared pair, light's kind
    declared = json.loads(json.dumps(document))
    declared["measured"][0]["emitter"]["clock"] = [512, 1]
    refused(declared, r"measured\[0\]\.emitter has unknown keys: clock")
    inline = emitter_specimen(stock=1, ticks=10)
    del inline["universe"][0]["clock"]
    refused(inline, r"measured\[0\]\.emitter: the given family 'light' declares no clock")


def test_the_bodys_kind_and_the_emitters_pair_stand_where_the_family_declares_no_pair():
    document = on_the_file(emitter_specimen(stock=1, ticks=10))
    world = parse_nature_beam_world(document)
    body = world.measured[0]
    assert body.block is not None and body.block.kind == (800, 809) and body.block.pair == (800, 801)
    without = json.loads(json.dumps(document))
    del without["measured"][0]["kind"]
    refused(without, r"measured\[0\]\.kind is required: the family 'matter' declares no pair")
    light_kind = json.loads(json.dumps(document))
    light_kind["measured"][0]["kind"] = [809, 800]
    refused(light_kind, r"measured\[0\]\.kind \[809, 800\] is no massive kind")
    inline = emitter_specimen(stock=1, ticks=10)
    inline["measured"][0]["kind"] = [800, 809]
    refused(inline, r"measured\[0\]\.kind is refused: the family 'matter' declares its pair")
    # an emitter giving a family whose pair is the body's declares the given record's pair: on an inline list, a body of a second massive kind giving matter (under the three entries a body of matter cannot give matter, its own family; ALGEBRA.md #the-primitives waits)
    giving_matter = emitter_specimen(stock=1, ticks=10)
    names = {family["name"]: family for family in giving_matter["universe"]}
    names["matter"]["pair"] = "body"
    giving_matter["universe"].append(family_entry("heavy", [1600, 1618]))
    body = giving_matter["measured"][0]
    body["family"] = "heavy"
    body["stocks"] = {"matter": 1}
    body["emitter"]["family"] = "matter"
    names["matter"]["clock"] = [512, 1]  # the given record's clock is the row's (L479)
    refused(giving_matter, r"measured\[0\]\.emitter\.pair is required: the given family 'matter'")
    inline_pair = emitter_specimen(stock=1, ticks=10)
    inline_pair["measured"][0]["emitter"]["pair"] = [1, 1]
    refused(inline_pair, r"measured\[0\]\.emitter\.pair is refused: the given family 'light' declares")


def test_age_bound_fixed_sign_and_the_family_clock_are_refused_by_name_when_absent_or_wrong():
    """The keys #1236 made required, no default: each refused by the schema's or the loader's name."""
    for change, match in (
        (lambda d: d["universe"][0].pop("pair"), r"the family 'light' lacks keys: m"),
        (lambda d: d["universe"][0].__setitem__("clock", 3), r"clock must be a list, not 3"),
        (lambda d: d["universe"][0].__setitem__("clock", [1, 0]), r"has q from 1"),
    ):
        document = emitter_specimen(stock=1, ticks=4)
        change(document)
        refused(document, match)
