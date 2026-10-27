"""The committed charts (examples/records: the hole setting at 60 on the 5-cube, the chiral setting at 60, the bodies' setting at 120 on the 7-cube, regenerated under PM-S1 on 2026-10-25, again under CK-S1 and the release's odd rounding the same day, again under the crossing read even and the unsprung hand no bob (the hand at the spring 0 never chimed as a bob), and again under PL-S1 (the sweep read at the impulse in its push form, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423; the bodies bit for bit): the era of matter SHOWN on the hole setting, Coulomb's sign NOT SHOWN there under PL-S1 (SHOWN in part, unlike senses approach, under the former drive of 2 W after the step; NOT SHOWN under the crossing odd at a touch of zero) and the collisions NOT SHOWN with it on the hole (SHOWN under the former drive; SHOWN on the chiral), the bodies' well SHOWN, the bodies' chimed clocks receding, the bodies' gate 8 NOT SHOWN by two chimes at turned-over clocks reckoning beyond the floor, so the unwind's event stands for the strike; the hole's fittings 16 and chimes 777 under PL-S1 (24 and 1,124 under A48-S1 (05cca50, the read of the fine tooth at the pawl of its setting, reverted for the tie of the sign train's drive fine tooth and the fittings' setting); 16 and 233 under the former drive of 2 W after the step, 20 and 514 before), the chiral's 17 and 2,943 with the collisions SHOWN (19 and 3,052 with them NOT SHOWN under the reverted read; 2,914; 16 and 2,336 before), the bodies' 1,973 bit for bit (1,819 before CK-S1)) read by the reckoner's gates, each verdict asserted by name so that a lost or a gained verdict fails by name, the rim's points under gate 19 by their count (MS-S2: 26 points at the toy's rim, 8 at the middle's, the typed ratios among them); the conservation check over every chart's log (the sweep, the count unwound against tallied, the integers' count constant, every integer within the width, the rewind exact); the hole chart re-run by the engine and compared with the committed one bit for bit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from event_universe import great_clock, meshes, strikes, swings, symmetries, tick
from event_universe.clock import Clock
from event_universe.core import rates
from event_universe.core.spokes import AXES
from event_universe.events import NAMES
from event_universe.gates import gates
from event_universe.reckoner import Chart, shown
from event_universe.run import chart
from event_universe.trains import HAND
from tests.laws import ROOT, load_file, state_of, world_of

RECORDS = ROOT / "examples" / "records"
CIRCLES = {"bodies": (8, 2), "chiral": (26, 3), "hole": (26, 3)}  # the rim: its points, the typed
SHOWN_ROWS = {  # the numbered rows SHOWN (whole or in part) per chart, the Boss's count in Universe24
    # on the charts of 3dc12e307 (the five sentences built on toys-5, the slack and the unspringing among them): the hole loses 2 (the meshes lengthening in the strikes, under GP-S1's setting) and gains 47 (the exact unwind, the excess kept as the slack, EX-S1); the chiral loses 58 and gains 24 (two pairs into light, MG-S1), 15 kept by the reckoner's read of the slack, 17 lost by the engine's bug at an unspringing's tie end (H-Children-Charge-Bug-1: the unsprung hand advanced as the advance of a fitted hand with a sweep, the fitted hands' own sweeps -36,000 over the fittings; SHOWN again at the fix); the bodies gain 8 and 16 with the chimes the slack pays; the hole under PL-S1 before: 9 and 22 among them under the former drive of 2 W after the step
    "hole": {
        int(n)
        for n in "2 4 5 7 8 10 15 16 17 18 19 21 22 25 26 27 30 37 43 45 47 56 58 59 60 62 64 65 66 67 68 70 71 72".split()
    },
    "chiral": {
        int(n)
        for n in "2 4 5 7 8 9 10 15 16 17 18 19 21 24 25 26 27 30 37 43 45 47 56 59 60 62 64 65 66 67 68 70 71 72".split()
    },
    "bodies": {
        int(n)
        for n in "4 5 7 10 15 17 18 21 22 24 25 26 27 30 37 43 45 47 58 59 60 62 64 65 66 67 68 70 71 72".split()
    },
}
VERDICTS = {  # the verdicts' words by name
    "hole": {
        "63 the uniformity in the clicks": "NOT SHOWN: 0 regions without a credit, the least 154 against the largest 454",
        "65 the lepton number": "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click",
        "67 CPT in the clicks": "SHOWN: the charge odd under C and under T and even under CPT on 2228 of 2228 frames",
        "9 collisions": "NOT SHOWN: the credited Nodes receding, farthest 4 Links at first and 6 at last",
        "22 Coulomb's sign": "SHOWN in part: unlike senses approach",
        "45 the bodies' well, binding and collapse": "SHOWN: a body stands in its own well through the run",
        "56 Bell": "SHOWN in part: the law's own bound met exactly, S = -240 / 120, S squared 4",
        "58 the fast expansion after the bang": "SHOWN: the credits' spacing grows fastest in the first eighths",
        "59 the deceleration in the clicks": "SHOWN: an eighth's growth of the spacing smaller than the one before",
        "60 the acceleration in the clicks": "SHOWN: after a slowing, an eighth's growth of the spacing larger than the one before",
        "15 conservation at the click": "SHOWN exact: taken + the remainder before - the remainder after = booked on every birth",
        "47 the exact take": "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node",
        "62 the arrow of time in the clicks": "SHOWN: the charge odd under the slot exchange, 2228 of 2228 frames",
        "68 matter against antimatter": "SHOWN: the + child at the take's Node on 6 moving births and at the other end on 12, the hand's choice at every one; 0 m",
        "69 the neutrino's one hand": "NOT SHOWN: both hands stand, 6 and 12 moving births",
        "70 the baryon number": "SHOWN: the children's own charges sum to 0 at every birth, no matter made by a click",
        "71 the momentum booked on the Link": "SHOWN exact: -dP p_0^2 + the carry before - the carry after = the levels laid times the write wall on 6948 of 6948 axis ",
        "72 the angular momentum booked on the Link": "SHOWN exact: the move's moment and the moment written on the Link's record sum to 0 at 2316 of 2316 bookings, the record",
        "73 E = mc^2 at the merger": "NOT READ: no merger in the record; the predicate: at every merger end the pair's share taken equal to the light's quantu",
    },
    "chiral": {
        "64 dark matter in kind": "SHOWN: 97 of 143 bodies credited at a Node where no light was laid",
        "65 the lepton number": "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click",
        "66 the energy in the clicks": "SHOWN in part: on most pairs",
        "24 the merger (a pair into light)": "SHOWN: 1 pairs into light",
        "62 the arrow of time in the clicks": "SHOWN: the charge odd under the slot exchange, 2856 of 2856 frames",
        "17 charge conservation": "SHOWN: the senses sum to 0 over every birth, each pair opposite, each merger's children 0 and 0",
        "9 collisions": "SHOWN: two bodies' credited Nodes approached and stood one Link apart",
        "15 conservation at the click": "SHOWN: taken + the remainder before - the remainder after = booked on every birth carrying the remainder",
        "47 the exact take": "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node",
        "1b the board tops, every Node turning at once": "NOT SHOWN: no interval with every Node turned",
        "1c the board returns to the seed": "NOT SHOWN: no return to the seed's first state",
        "56 Bell": "SHOWN in part: the law's own bound met exactly, S = -120 / 60, S squared 4",
        "68 matter against antimatter": "SHOWN: the + child at the take's Node on 7 moving births and at the other end on 8, the hand's choice at every one; 1 me",
        "69 the neutrino's one hand": "NOT SHOWN: both hands stand, 7 and 8 moving births",
        "70 the baryon number": "SHOWN: the children's own charges sum to 0 at every birth, no matter made by a click",
        "71 the momentum booked on the Link": "SHOWN exact: -dP p_0^2 + the carry before - the carry after = the levels laid times the write wall on 9159 of 9159 axis ",
        "72 the angular momentum booked on the Link": "SHOWN exact: the move's moment and the moment written on the Link's record sum to 0 at 3053 of 3053 bookings, the record",
        "73 E = mc^2 at the merger": "NOT SHOWN: at 2 of 2 merger ends the pair's share taken exceeds the light's quantum booked, up to 1103 thousandths of it",
    },
    "bodies": {
        "64 dark matter in kind": "SHOWN: 335 of 409 bodies credited at a Node where no light was laid",
        "67 CPT in the clicks": "SHOWN: the charge odd under C and under T and even under CPT on 17115 of 17115 frames",
        "37 Maxwell's one Link per interval": "SHOWN: the current's reach grows by one Link per interval",
        "55 the two slits": "NOT READ: no two gap-0 packets at one centre with one wave mirrored on one axis in the seed; the predicate: the gap-0 ro",
        "56 Bell": "NOT READ: 23 births, 3 of the four setting cells filled by pairs clicked at both ends; the predicate: S from the pairs' ",
        "57 GHZ": "NOT READ: a birth gives two ends at one Link and a shared take four, no three ends with one root in the record; the pred",
        "61 the horizon radiates": "NOT READ: no frozen Node in the record",
        "62 the arrow of time in the clicks": "SHOWN: the charge odd under the slot exchange, 17115 of 17115 frames",
        "58 the fast expansion after the bang": "SHOWN: the credits' spacing grows fastest in the first eighths",
        "59 the deceleration in the clicks": "SHOWN: an eighth's growth of the spacing smaller than the one before",
        "68 matter against antimatter": "SHOWN: the + child at the take's Node on 5 moving births and at the other end on 3, the hand's choice at every one; 15 m",
        "69 the neutrino's one hand": "NOT SHOWN: both hands stand, 5 and 3 moving births",
        "70 the baryon number": "SHOWN: the children's own charges sum to 0 at every birth, no matter made by a click",
        "71 the momentum booked on the Link": "SHOWN exact: -dP p_0^2 + the carry before - the carry after = the levels laid times the write wall on 54129 of 54129 axi",
        "72 the angular momentum booked on the Link": "SHOWN exact: the move's moment and the moment written on the Link's record sum to 0 at 18043 of 18043 bookings, the reco",
        "73 E = mc^2 at the merger": "NOT SHOWN: at 30 of 30 merger ends the pair's share taken exceeds the light's quantum booked, up to 25516 thousandths of",
    },
}


def loaded(name: str) -> dict[str, Any]:
    return json.loads((RECORDS / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_committed_record_shows_the_gates_by_name(name: str) -> None:
    found = gates(loaded(name))
    kinds = {int(k[:2]): v["kind"] for k, v in found.items() if k[:2].strip().isdigit()}
    assert set(kinds) == {int(k) for k in NAMES if k.isdigit()}  # the rows named once, in events.NAMES
    assert {n for n, kind in kinds.items() if kind.startswith("SHOWN")} == SHOWN_ROWS[name]
    assert {n for n, kind in kinds.items() if kind == "NOT REACHED"} == {14, 34}  # the horizon
    for gate, verdict in VERDICTS[name].items():
        assert found[gate]["verdict"].startswith(verdict), (name, gate, found[gate]["verdict"])
    assert found["the three constants"]["verdict"].startswith("SHOWN")
    rim_points = next(v for k, v in found["19 mass ratios (parts per million)"].items() if "circle" in k)
    assert (len(rim_points), sum(1 for _ratio, typed in rim_points if typed)) == CIRCLES[name]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_conservations_hold_on_the_record(name: str) -> None:
    """The independent check: the conservations recomputed from the chart's log alone, beside what rows 15, 17, 18 and the constants read."""
    run = loaded(name)
    births = [e for e in run["log"] if e["event"] == "birth"]
    pairs = [
        b for b in births if "exact_lay" not in b
    ]  # an unspringing's unsprung fitted hands carry no sense (MG-S1)
    signs = [(w > 0) - (w < 0) for b in pairs for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs

    # EX-S1's identity at the unsprung unwind; an unspringing's ends unwound whole (MG-S1)
    paid = [b["taken"] + b.get("remainder_was", 0) - b.get("remainder", 0) - b["booked"] for b in births]
    assert all(x == 0 if "remainder" in b else x >= 0 for x, b in zip(paid, births, strict=True))
    assert len({row["integers"] for row in run["rows"]}) == 1  # the law's constant, no width bound
    assert run["run_back"]["exact"] == run["run_back"]["intervals"] == 20
    assert int(run["counts"]["births"]) == len(births)
    assert all("sense" in e for e in run["log"] if e["event"] == "lay")


def test_the_hole_record_is_the_engines_own_bit_for_bit() -> None:
    calibre, piece = world_of("world_hole.json")
    committed = loaded("hole")
    assert committed["world"] == piece and committed["universe"] == calibre
    found = json.loads(json.dumps(chart(calibre, piece, 20, lambda line: None)))
    assert found["log"] == committed["log"] and found["counts"] == committed["counts"]
    assert found["turns"] == committed["turns"] and found["run_back"] == {"intervals": 20, "exact": 20}
    timeless = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
    assert timeless == [{k: v for k, v in r.items() if k != "milliseconds"} for r in committed["rows"]]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_committed_reading_is_the_decoders_own_whole(name: str) -> None:
    """The whole reading beside the chart equals a fresh read, line for line after JSON (the one check of every key, number, verdict, field and event)."""
    assert [{k: v} for k, v in json.loads(json.dumps(gates(loaded(name)))).items()] == reading_of(name)


def reading_of(name: str) -> list[dict[str, Any]]:
    """The committed reading beside the chart, one JSON per line (the gates' output)."""
    lines = (RECORDS / f"{name}.reading.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_record_carries_a_node_line_per_interval_and_the_reading_its_events(name: str) -> None:
    run = loaded(name)
    count = int(run["cube"]) ** 3
    assert [line["i"] for line in run["nodes"]] == list(range(1, int(run["intervals"]) + 1))
    for line in run["nodes"]:
        assert len(line["X"]) == len(line["content"]) == count
        sites = line["turned"] + line["frozen"] + [h[0] for h in line["held"]]
        assert all(0 <= i < count for i in sites)
        assert all(h[1] in (0, 1, 2) for h in line["held"])
    assert sum(len(line["turned"]) for line in run["nodes"]) == int(run["counts"]["turns"])
    events = next(line["events"] for line in reading_of(name) if "events" in line)
    labels = [e["label"] for e in events]
    assert "the run back exact" in labels
    struck = (
        "a pair born",
        "a body clicks",
        "light absorbed at a take",
    )  # gate 7's unwind is every strike's
    first = next((e for e in events if e["label"] in struck), None)
    assert first is not None and first["i"] == min(
        e["i"] for e in run["log"] if e["event"] in ("birth", "credit")
    )
    assert all(len(e["label"].split()) <= 6 for e in events)
    rows = {k[:2]: v for line in reading_of(name) for k, v in line.items() if k[:2] in ("1b", "1c")}
    eras = next(line["the eras"] for line in reading_of(name) if "the eras" in line)
    returns = int(rows["1c"]["cause"].split()[0]) if rows["1c"]["kind"] == "SHOWN" else 0
    tops = int(rows["1b"]["cause"].split(" tops")[0].split()[-1]) if rows["1b"]["kind"] == "SHOWN" else 0
    assert (
        len(eras["bangs"]) == 1 + returns and len(eras["tops"]) == tops
    )  # every one, beyond the eight listed


def test_the_momentum_booked_on_the_link_is_an_identity_on_every_booking() -> None:
    """Row 71 on the chiral chart's tallies, an unspringing's two unwinds, cross term and two advances among them: SHOWN exact at the drive teeth of the calibre file's own trace, NOT SHOWN at another trace (the one tally advancing a notch) or with one carry moved by one notch, NOT READ with the keys struck (a chart run before LT-S1)."""
    run, gate = loaded("chiral"), "71 the momentum booked on the Link"
    rec, ints = Chart(run), run["universe"]["integers"]
    held, whole = symmetries.momentum_booked(rec)[gate]["axis bookings holding the identity / in all"]
    assert held == whole == len(symmetries.tallies_of(rec)) * AXES == 9159
    ints["trace"], trace = ints["trace"] * ints["trace"], ints["trace"]
    failed = "NOT SHOWN: the identity fails on 1 of"
    assert symmetries.momentum_booked(Chart(run))[gate]["verdict"].startswith(failed)
    ints["trace"] = trace
    rec.unwinds[-1]["carry"][0] += 1
    assert symmetries.momentum_booked(Chart(run))[gate]["verdict"].startswith(failed)
    for entry in rec.unwinds:
        for key in ("recoil", "recoil_ends", "cross", "takes"):
            entry.pop(key, None)
    assert symmetries.momentum_booked(Chart(run))[gate]["verdict"].startswith("NOT READ")


def test_the_angular_momentum_closes_at_every_booking_and_the_mass_becomes_light() -> None:
    """Rows 72 and 73 on the chiral chart: the moment closed at every tally with the unspringing's cross term off the mesh's axis counted, open once one carry is moved by one notch; the pair's wind unwound above the light's quantum at both unspringing ends, SHOWN once it is the quantum, NOT READ on the hole with no unspringing."""
    run, light = loaded("chiral"), "73 E = mc^2 at the merger"
    turn = "72 the angular momentum booked on the Link"
    rec = Chart(run)
    found = symmetries.angular_momentum(rec)[turn]
    off = "mergers whose cross term carries a part off the Link's own axis / with a cross term"
    assert found[off] == [1, 1] and found["verdict"].startswith("SHOWN exact")
    assert not shown(symmetries.mass_to_light(rec)[light]["verdict"])
    rec.unwinds[-1]["carry"][0] += 1
    verdict = symmetries.angular_momentum(Chart(run))[turn]["verdict"]
    assert verdict.startswith("NOT SHOWN: the moment does not close at 1 of")
    for unwind in (t for b in rec.fittings for t in b.get("takes", [])):
        unwind["taken"] = unwind["booked"]
    verdict = symmetries.mass_to_light(Chart(run))[light]["verdict"]
    assert verdict.startswith("SHOWN: at every one of 2 merger ends")
    assert symmetries.mass_to_light(Chart(loaded("hole")))[light]["verdict"].startswith("NOT READ")


def test_the_horizon_is_read_from_the_node_lines_not_the_rows() -> None:
    """Gate 14 on the hole chart with one clock stopped on one clock line by hand (the Boss's 6416277638): the rows, one at every twelfth tick, keep their maximum below the stopped load while the clock line carries it, and the gate reads the horizon as silence from the clock lines; NOT REACHED on the chart as committed."""
    run = loaded("hole")
    rec, stopped = Chart(run), rates.stopped_load(int(run["gamma"]))
    line = run["nodes"][len(run["nodes"]) // 2]
    chimed = {rec.index(c["node"]) for c in rec.chimes if int(c["i"]) == int(line["i"])}
    at = next(k for k in range(len(line["content"])) if k not in chimed)
    line["content"][at], line["frozen"] = stopped, [at]
    found = great_clock.standstill(Chart(run))["14 the horizon"]
    assert (
        found["max content in the rows (one row at every twelfth interval)"]
        < stopped
        <= found["max content in the Node lines"]
    )
    assert found["Nodes frozen"] == 1 and found["verdict"].startswith("SHOWN as silence")
    assert great_clock.standstill(Chart(loaded("hole")))["14 the horizon"]["verdict"] == "NOT REACHED"


def test_the_exact_return_is_the_seeds_first_state_and_the_horizon_standing() -> None:
    """Rows 1, 1c and 61 on the hole chart with its clock lines written by hand (the Boss's 6416499848 and 6416342006): a clock line equal to the first in X and load is an exact return and a swing, a bottom at Gamma is not; every clock stopped on one line and released on the next is a standstill that stands at that tick alone, so a chime after the release counts as beyond it, and a great clock stopped whole to the end lets no chime pass."""
    run = loaded("hole")
    clocks = run["nodes"]
    k = len(clocks) // 2
    clocks[k]["X"], clocks[k]["content"] = list(clocks[0]["X"]), list(clocks[0]["content"])
    found = swings.recurring_swing(Chart(run))["1 recurring bangs"]
    assert found["exact returns to the seed's first state (interval)"] == [clocks[k]["i"]]
    assert found["bangs numbered (the interval each begins)"] == [1, clocks[k]["i"]]
    assert swings.returns(Chart(run))["1c the board returns to the seed"]["verdict"].startswith(
        "SHOWN: 1 exact"
    )
    assert swings.exact_of(Chart(loaded("hole"))) == []
    run = loaded("hole")
    every = list(range(len(run["nodes"][0]["X"])))
    run["nodes"][k]["frozen"] = every
    found = strikes.horizon_radiates(Chart(run))["61 the horizon radiates"]
    later = [c for c in run["log"] if c["event"] == "credit" and int(c["i"]) > run["nodes"][k]["i"]]
    assert found["the whole board frozen at once"] and found[
        "of them after the whole board's release (no Node frozen at the interval)"
    ] == len(later)
    for line in run["nodes"][k:]:
        line["frozen"] = every
    found = strikes.horizon_radiates(Chart(run))["61 the horizon radiates"]
    assert found["credits two or more Links from every Node frozen at the credit's interval"] == 0
    assert found["verdict"].startswith("NOT SHOWN")


def test_the_gates_of_the_phenomena_are_one_table_written_from_the_readings(tmp_path: Path) -> None:
    tool = load_file("phenomena", ROOT / "tools" / "phenomena.py")
    readings = {name: tool.reading_of(RECORDS / f"{name}.reading.jsonl") for name in SHOWN_ROWS}
    whole = {g for rows in readings.values() for g, r in rows.items() if r["kind"] == "SHOWN"}
    table = tool.table_of("test", readings, {})
    rows = [
        line
        for line in table.splitlines()
        if line.startswith("| ") and line.split("|")[2].strip().isdigit()
    ]
    names = {g: r["phenomenon"] for rows in readings.values() for g, r in rows.items()}
    count = len(
        {int(k) for k in NAMES if k.isdigit()}
    )  # the rows named once, the table's count from the readings
    assert len(rows) == tool.rows_in(readings) == count and all(names[k] in rows[k - 1] for k in names)
    assert (
        whole <= set.union(*SHOWN_ROWS.values())
        and f"SHOWN in Universe24: {len(whole)} of {count} on test" in table
    )
    document = tmp_path / "UNIVERSE24.md"
    document.write_text(
        "## 2\n\n### The gates widened to everything derived\n\nrest\n", encoding="utf-8"
    )
    assert tool.write(document, "test", readings) in document.read_text(encoding="utf-8")


def test_the_page_is_one_html_from_the_record_and_the_reading_with_nothing_typed(tmp_path: Path) -> None:
    page = load_file("page", ROOT / "tools" / "page.py")
    out = tmp_path / "hole.html"
    page.write_page(RECORDS / "hole.json", RECORDS / "hole.reading.jsonl", out)
    text = out.read_text(encoding="utf-8")
    run = loaded("hole")
    assert text.isascii() and text.count("<canvas") == 1 and "color-scheme: dark" in text
    assert f"den {run['universe']['integers']['den']}" in text
    assert f"shape {run['world']['shape']}" in text
    events = next(line["events"] for line in reading_of("hole") if "events" in line)
    assert all(e["label"] in text for e in events)
    source = (ROOT / "tools" / "page.py").read_text(encoding="utf-8")
    assert str(run["den"]) not in source and "electron" not in source and "light" not in source


def test_the_page_of_the_bangs_is_one_html_from_the_records_and_the_readings(tmp_path: Path) -> None:
    """The page of the swings (tools/bangs_page.py, the owner's words of 2026-10-26 through the Boss, 6417065257 and 6417873704): one HTML from the charts and their readings with the pages named beside, the charts' numbers and what each brings read from its rows, every numbered row in the table with its verdict per chart; ASCII, nothing of a calibre typed in the tool."""
    tool = load_file("bangs_page", ROOT / "tools" / "bangs_page.py")
    out = tmp_path / "bangs.html"
    run = loaded("hole")
    pages = [(name, run, str(RECORDS / "hole.reading.jsonl"), f"{name}.html") for name in ("one", "two")]
    out.write_text(
        tool.page_of(pages, [("beside", str(RECORDS / "chiral.reading.jsonl"))]), encoding="utf-8"
    )
    text = out.read_text(encoding="utf-8")
    rows = {k for line in reading_of("hole") for k in line if k[:2].strip().isdigit()}
    assert text.isascii() and text.count("<iframe") == 2 and "color-scheme: dark" in text
    assert text.count("<tr><td>") == len(rows) and "It brings:" in text and "Together:" in text
    source = (ROOT / "tools" / "bangs_page.py").read_text(encoding="utf-8")
    assert str(run["den"]) not in source and "electron" not in source and "light" not in source


def test_a_train_of_four_gears_at_a_spring_is_twin_hands_and_keeps_the_spin() -> None:
    """Spin one half on two hands (David's DAVID-SPIN-SOLVED.md, toys-5 67f2ff192, the owner's words of 2026-10-27, 12:02 UTC): the node piece's calibre with every sprung hand's train named as four gears is twin hands per train, read from the count and the ratio; at 20 ticks every fitting advances its - fitted hand and its + fitted hand in twin hands, every unspringing unwinds across them, and the 20 ticks rewind exactly (a fitting group of two fitted hands at one clock undone by its one unwind once)."""
    calibre, piece = world_of("world_node.json")
    rim = int(calibre["integers"]["den"])
    four = [
        dict(t, shape=HAND + HAND) if t.get("pair") and t["shape"] == HAND and t["pair"][0] < rim else t
        for t in calibre["rows"]
    ]
    clock = Clock(dict(calibre, rows=four), piece)
    hands = clock.hands()
    twin = {k: hands.index(r.twin) for k, r in enumerate(hands) if r.twin is not None}
    assert twin and all(twin[b] == a and hands[a].size == HAND for a, b in twin.items())
    kept, quantum = [], clock.A * clock.B
    for _ in range(20):
        kept.append(state_of(clock))
        clock.tick()
        twins = [r.gears for r in clock.hands() if r.twin]
        sweeps = [
            abs(int(w))
            for g in twins
            for w in meshes.cross(*(x.now for x in g), *(x.before for x in g)).flat
        ]
        assert max(sweeps) < quantum + quantum  # Pauli: one fitted quantum's sweep per hand per clock
    fittings = [e for e in clock.log if e["event"] == "birth"]
    assert [e for e in fittings if "takes" not in e] and all(
        twin[e["line_pair"]] == e["plus_hand"] for e in fittings if "takes" not in e
    )
    for e in (e for e in fittings if "takes" in e):
        ends = [unwind.get("hand", e["taken_row"]) for unwind in e["takes"]]
        assert twin[ends[0]] == ends[1]
    assert sum(state_of(clock) == kept[19 - k] for k in range(20) if not clock.tick(-1)) == 20


def test_spin_one_half_reads_minus_one_after_one_turn_and_comes_home_after_two(monkeypatch: Any) -> None:
    """Spin one half seen on the great clock (the owner's rule of 2026-10-27, 14:5x UTC: a push's test sees what it was pushed for; David's DAVID-SPIN-IN-CLOCKS full turn): the toy calibre's sprung hands as twin hands, one mode on the heavy lift's up twin of a 5-cube, a held curl turning the twins, the offset's turn of the twins off; beside it the free run, the twins' pulls off. After one turn of the spin (tick 15) S_z is home and the hands read -1 (the overlap with the free run below -1/2); after two turns (tick 36) above +1/2."""
    calibre, _ = world_of("world_node.json")
    rim = calibre["integers"]["den"]
    four = [
        dict(r, shape=HAND + HAND) if r["shape"] == HAND and r["pair"][0] < rim else r
        for r in calibre["rows"]
    ]
    piece = {
        "shape": [5] * 3,
        "intervals": 36,
        "seed": [{"lay": "sea", "row": 2, "hand": 0, "quanta": 1, "sense": 1}],
    }
    held = [16000, 0, 0]
    monkeypatch.setattr(tick, "offset_curl", lambda odd: [odd[0] * 0 + c for c in held])
    monkeypatch.setattr(
        tick, "coupling_of", lambda r: 0 if r.twin is not None else meshes.coupling_of(r)
    )
    runs = []
    for pulls in (tick.Tick.twin_pulls, lambda self: None):
        monkeypatch.setattr(tick.Tick, "twin_pulls", pulls)
        clock, kept = Clock(dict(calibre, rows=four), piece), {}
        up = next(k for k, r in enumerate(clock.hands()) if r.ratio == tuple(four[2]["pair"]) and r.twin)
        for t in range(36):
            clock.tick()
            kept[t + 1] = [g.now for r in (clock.hands()[up], clock.hands()[up].twin) for g in r.gears]
        runs.append(kept)
    for t, sign in ((15, -1), (36, 1)):
        dot = sum(int((a * b).sum()) for a, b in zip(runs[0][t], runs[1][t], strict=True))
        assert sign * (dot + dot) > sum(int((b * b).sum()) for b in runs[1][t])
    s_z = [sum(int((g * g).sum()) for g in runs[0][15][k : k + HAND]) for k in (0, HAND)]
    assert s_z[0] > s_z[1]
