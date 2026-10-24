"""The eras' tools (tools/eras.py and tools/look/eras_page.py; docs/ENGINE.md section 5; DESIGN section 4 (g)): the log of a world as the board reads it under the one Node, one JSON line per interval, and the page that draws it, both host tools holding no number of the law."""

import json

from event_universe import world_files
from event_universe.loader.universe import MASSLESS, VOLUME
from event_universe.world_files import load_world
from tests.laws import ROOT, load_file, refused
from tests.laws_universe import GAMMA, small_universe

ERAS = load_file("eras_tool", ROOT / "tools" / "eras.py")
ERAS_PAGE = load_file("eras_page_tool", ROOT / "tools" / "look" / "eras_page.py")


def test_the_eras_log_holds_the_boards_readings_per_interval_and_the_page_draws_them(
    tmp_path, monkeypatch
):
    """The log on the bare 3-cube torus of the one universe file over 8 intervals: the header names the world's integers and the held rows by name, no former key; each interval's line holds gravity's row (the level reading and its remainder, U, the velocity, the writes per family, n_eff the mix's exponent, the constraint's residual, the three tension lines' means and velocities, the volume's sums now and before and the volume form's own constraint R_vol from the second interval on, the seed's level, contrast and clock ratio where a seed stands) and each family of quanta's readings (the largest level, the quanta, the frozen count); the last line is the last interval's, nothing named unreturning (the volume form's run back is exact); the numbers are the engine's own: U the fine reading from the volume's sums with the level reading's own U beside it within a hundredth, the writes' keys the sourcing families, the mix's exponent between the pairs' integers, the tension lines' means alike and within one level per interval; the spans' estimator reads n_eff from the slope of 1 / v where the velocity is above 0; `--every` below 1 is refused by name; the page from the log holds its panels (the course, the writes, the residual with R_nat and R_vol, the mix's exponent, the seed, the clocks, the rulers, the tension lines, the Links' factors, the quanta), the blind's table where a blind is given, the notes where given, the held row's keys in its words, and refuses a log without the header by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)  # the tests' small universe, den 1,021 with its two points
    world = tmp_path / "eras.json"
    world.write_text(json.dumps({"shape": [3, 3, 3], "intervals": 8, "universe": "u.json"}), "utf-8")
    out = tmp_path / "eras.eras.jsonl"
    lines = ERAS.run(world, out, 4, None)
    log = ERAS_PAGE.read_log(out)
    header, last = log[0], log[-1]
    assert (
        header["held"] == [VOLUME] and "keys" not in header and header["seed"] == MASSLESS
    )  # the held rows by name, no former key reported (2026-10-23)
    assert (header["node_clock"], header["quantum_action"], header["intervals"]) == (GAMMA, 36000, 8)
    assert (
        header["width"] == load_world(world).width.bit_length() and "unobservable" not in header
    )  # the derived width (2026-10-24), no flag
    assert (
        header["den"] == 1021
        and header["primes"] == [[1021, 1]]
        and set(header["points"]) == {"point -2", "point 2"}
    )
    assert header["points"]["point 2"] == [
        779,
        660,
    ]  # the least leg under its label, the page's captions read from it
    assert len(lines) == 8 and [line["interval"] for line in lines] == list(range(1, 9))
    assert last == lines[-1] and last["interval"] == 8 and "unreturning" not in last
    for line in lines:
        row = line["rows"][VOLUME]
        assert row["U_level"] == (row["level"] + row["level_remainder"] / row["nodes"]) / GAMMA
        assert (
            abs(row["U"] - row["U_level"]) < 0.01 and row["nodes"] == 27
        )  # the fine U beside the level's
        assert (
            set(row["writes"]) == {MASSLESS, "point -2", "point 2"} and row["writes"][MASSLESS] > 0
        )  # every family of quanta sources the holder it reads, the sign holder none (the reads derived, 2026-10-24; the charge among gravity's sources under rule.json's declared reads to that day)
        assert 5 <= row["n_eff"] <= 6  # the mix of the gapped points' 5 and the massless point's 6
        assert len(row["tension_means"]) == 3 and len(set(row["tension_means"])) == 1
        assert all(abs(v) <= 1 for v in row["tension_velocities"])
        assert -1 <= row["nature_residual"] and row["H"] == row["velocity"] / GAMMA
        assert "seed_level" not in row and "weight_low" not in row  # no seed Node; no hill
        assert row["volume"] > row["volume_before"] > 0  # the volume's sums, the record's own
        assert (row["volume_residual"] is None) == (line["interval"] == 1)
        assert row["volume_residual"] is None or -1.2 <= row["volume_residual"] <= 1
        for name in (MASSLESS,):  # the seed's family alone carries a record (2026-10-24)
            quanta = line["quanta"][name]
            assert quanta["largest"] > 0 and quanta["quanta"] >= 0 and quanta["frozen"] == 0
            assert "share_within_one_link" not in quanta
    spans = ERAS.spans(lines, VOLUME, 4, GAMMA)
    assert spans and all(span["q_p"] == span["n_eff"] / 2 - 2 for span in spans)
    assert all(span["velocity"] > 0 for span in spans)
    refused("--every takes an integer from 1", ERAS.main, [str(world), "--every", "0"])
    blind = tmp_path / "eras.blind.json"
    blind.write_text(
        json.dumps(
            {"rows": [{"reading": "U at 8", "blind": 0.3, "status": "DERIVED", "fence": "LATTICE"}]}
        )
    )
    notes = tmp_path / "notes.md"
    notes.write_text(
        "# The notes\n\nOne paragraph with `code` and **bold**.\n\n- an item\n", encoding="utf-8"
    )
    page = tmp_path / "eras.html"
    ERAS_PAGE.main(
        [str(out), "--blind", str(blind), "--notes", str(notes), "--span", "4", "--out", str(page)]
    )
    html = page.read_text(encoding="utf-8")
    for anchor in (
        "course",
        "writes",
        "residual",
        "exponent",
        "seed",
        "contrast",
        "rulers",
        "tensions",
        "links",
        "quanta",
    ):
        assert f'id="{anchor}"' in html
    assert "R_nat" in html and "R_vol" in html and "U at 8" in html and "The notes" in html
    assert "The held row's keys" not in html  # no former key on the page
    assert "lattice reading" in html and "0.3" in html
    refused("header naming the held rows", ERAS_PAGE.page, [{"world": "x"}], None, None, 4, "")
    refused("--span takes an integer from 2", ERAS_PAGE.page, log, None, None, 1, "")
