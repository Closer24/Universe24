def test_the_reading_gate_reruns_a_folder_and_compares_each_number_bit_for_bit(tmp_path, capsys):
    """The reading gate (tools/reading_gate.py) on a copy of the shipped Zeno world re-declared beside tmp_path with a design of three amplitudes, the trials' knob: the document's gate's table re-read row by row (the run, the trials, the back-in-time pass), MATCH on the numbers this test reads from the same run, DIFFERS on a wrong value and on a wrong label, a shipped screen table read in the block's place, UNFILLED without either, the report's shape (JSON lines, then the summary) and the exit code; the imports stand inside the test so that the file is the test alone, the room the ratchet gives it."""
    import json

    import pytest

    from event_universe.lattice import Lattice
    from event_universe.world_files import load_world
    from tests.laws import EVENTS, ROOT, load_file, world_beside
    from tests.laws_content import ZENO_ATOM, opened, with_content

    gate = load_file("reading_gate", ROOT / "tools" / "reading_gate.py")
    copied = world_beside(
        tmp_path, EVENTS / "resonance" / "resonant.json", opened
    )  # re-pinned 2026-10-20
    (tmp_path / "examples" / "events" / "zeno" / "zeno_atom.json").write_text(
        json.dumps(with_content(ZENO_ATOM)), encoding="utf-8"
    )  # the copy's universe with the content: the shipped world's run is refused by name at the body 1 of 'atom' at the interval 41 (the law's third refusal of the click's read, ALGEBRA.md The digits' budget: the room 2^45.8 of the digits read, the pulse's five at three values each on the universe zeno_atom.json, which declares no content, and the atom's three at the lay's origin, below the absorption draw's total 2^53.9), so the claim is read on the content copy (tests/laws_content.content_world with `opened`, the born universe's holders prepended), which carries every draw
    folder, world, document = copied.parent, copied.name, copied.parent / "blind_and_reading.md"
    design = json.loads((EVENTS / "resonance" / "design.json").read_text(encoding="utf-8"))
    design.pop("seeds", None)
    design["knob"], design["knob_values"] = "amplitude", [392, 393, 394]  # three worlds, the knob
    (folder / "design.json").write_text(json.dumps(design), encoding="utf-8")
    board = Lattice(load_world(folder / world), (lines := []).append)
    for _ in range(board.world.intervals):
        board.step()
    clicks = [line for line in lines if line["event"] == "credit" and line["label"] == "NODEDETECTOR"]
    absorptions = sum(
        1 for line in clicks if line["absorbed"] and line["node_detector"] == "body 1"
    )  # the taker
    quanta, total = board.books()["pulse"]["quanta"], sum(int(line["count"]) for line in clicks)
    body_0 = sum(int(line["count"]) for line in clicks if line["node_detector"] == "body 0")
    emissions = sum(
        1 for line in clicks if line["emitted"]
    )  # the record takes climbing, emits descending
    assert absorptions + emissions == sum(int(line["count"]) for line in clicks)
    trials = gate.trials_reading(folder / world, folder / "design.json", None)
    ends = trials["ends_in_part"]["body 0"].get("e", [0])[0]
    rows = [
        ("NODEDETECTOR", "run_inputs", "absorptions body 1", absorptions),
        ("NODEDETECTOR", "run_inputs", "clicks", total),
        ("LATTICE", "run_inputs", "books pulse quanta", quanta),
        ("LATTICE", "run_inputs", "intervals", board.world.intervals),
        ("LATTICE", "back_in_time", f"intervals {board.world.intervals}", "MATCH"),
        ("NODEDETECTOR", "meeting_trials", "ends in e body 0", ends),
        ("LATTICE", "meeting_trials", "trials", 3),
    ]
    wrong = [
        ("NODEDETECTOR", "run_inputs", "absorptions body 1", absorptions + 1),
        ("NODEDETECTOR", "run_inputs", "intervals", 48),
    ]
    head = "# A copy of the resonant world\n\n## The gate's table\n\n| label | world | by | reading | value |\n"

    def written(table):
        body = "".join(
            f"| {label} | {world} | {by} | {reading} | {value} |\n"
            for label, by, reading, value in table
        )
        document.write_text(head + "| --- | --- | --- | --- | --- |\n" + body, encoding="utf-8")

    def report(code):
        with pytest.raises(SystemExit) as left:
            gate.main([str(folder)])
        assert left.value.code == code
        out = capsys.readouterr().out.splitlines()
        assert out[-1].startswith("the reading gate: ") and out[-2].startswith(folder.as_posix() + ": ")
        return [json.loads(line) for line in out[:-2]]

    written(rows)
    read = report(0)
    assert [line["verdict"] for line in read] == ["MATCH"] * len(rows)
    assert set(read[0]) == {
        "folder",
        "label",
        "world",
        "by",
        "reading",
        "value",
        "read",
        "verdict",
        "table",
    }
    assert (read[0]["read"], read[0]["label"], read[4]["read"], read[6]["read"]) == (
        str(absorptions),
        "NODEDETECTOR",
        "MATCH",
        "3",
    )
    written(rows + wrong)
    read = report(1)
    assert [line["verdict"] for line in read[-2:]] == ["DIFFERS", "DIFFERS"]
    assert (read[-2]["read"], read[-2]["value"]) == (
        str(absorptions),
        str(absorptions + 1),
    ) and "reason" not in read[-2]
    assert read[-1]["reason"] == "the reading's own label is LATTICE"
    screen = f"| region | resonant clicks | resonant share |\n| --- | --- | --- |\n| body 0 | {body_0} | 1.0 |\n| N | {total} | |\n"
    document.write_text("# A copy\n\n## The reading\n\n" + screen, encoding="utf-8")
    read = report(0)
    assert [(line["reading"], line["table"]) for line in read] == [
        ("clicks body 0", "shipped"),
        ("clicks", "shipped"),
    ]
    document.write_text("# A copy\n", encoding="utf-8")
    assert report(1)[0]["verdict"] == "UNFILLED"


def test_the_trials_coincidence_rows_are_every_record_alone_and_every_pair(tmp_path):
    """The trials tool's coincidence rows (tools/meeting_trials.py, `coincidence_rows`; the advisor's breaker and the mathematician's audit, #1793 comments 5981736108 K6, 5982140872 B3; the Boss's 5981734131 item 6; two hands): the rows derived from the records' count and from no fixed key, every record alone and every pair (`itertools.combinations`), neither, and alpha per pair; on the shipped two-record anticoincidence world over three of the design's seeds the report's rows are the keys listed here by hand, A_only, B_only, both, neither and alpha in that order, the four counts summing to the trials and alpha the fraction of the counts; with three records the function gives the three singles, the three pairs by their letters, `all` for the trials where every record took, neither and the three alphas, an absorption at the third record alone, which the fixed keys (0,), (1,), (0, 1) never counted, its own row, every trial with an absorption in exactly one row; under two records no row."""
    import json
    from collections import Counter
    from fractions import Fraction

    import pytest

    from tests.laws import EVENTS, ROOT, load_file, world_beside

    trials = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py")
    folder = (
        EVENTS / "resonance"
    )  # re-pinned 2026-10-20 from the anticoincidence folder: two records, no packet
    from tests.laws_content import ZENO_ATOM, with_content

    path = world_beside(tmp_path, folder / "resonant.json", lambda world: None)
    (tmp_path / "examples" / "events" / "zeno" / "zeno_atom.json").write_text(
        json.dumps(with_content(ZENO_ATOM)), encoding="utf-8"
    )  # the copy's universe with the content: the shipped resonant world's run is refused by name at the body 1 of 'atom' at the interval 41 (the law's third refusal of the click's read, the room 2^45.8 of the digits read below the absorption draw's total 2^53.9 on zeno_atom.json, which declares no content), so every trial ran refused and the rows read nothing; the copies carry every draw (2026-10-23)
    design = json.loads((folder / "design.json").read_text(encoding="utf-8"))
    design = {k: v for k, v in design.items() if k != "seeds"}
    design.update(knob="source", knob_values=[0, 1, 2], trial_intervals=48)  # three worlds
    (tmp_path / "design.json").write_text(json.dumps(design), "utf-8")
    found = trials.reading(path, tmp_path / "design.json", None, tmp_path / "trials")
    seeded = {**design, "seeds": [1, 2, 3]}
    (tmp_path / "seeded.json").write_text(json.dumps(seeded), "utf-8")
    with pytest.raises(ValueError, match="names `seeds`: the click reads the board"):
        trials.reading(path, tmp_path / "seeded.json", None, tmp_path / "trials")
    rows, run = found["coincidence"], found["trials"]
    # the trials' length from the design's own key, not the world's run length (the control run of 2026-10-05)
    assert found["intervals"] == design["trial_intervals"] == 48 != design["intervals"]
    assert list(rows) == ["A_only", "B_only", "both", "neither", "alpha"]  # the keys by hand, in order
    a_only, b_only, both, neither = (rows[key][0] for key in ("A_only", "B_only", "both", "neither"))
    assert a_only + b_only + both + neither == run == 3 and rows["A_only"][1] == run
    a, b = a_only + both, b_only + both
    alpha = Fraction(both * run, a * b) if a and b else None
    assert rows["alpha"] == ([alpha.numerator, alpha.denominator] if alpha is not None else None)
    absorbed = Counter({(2,): 2, (0, 1): 1, (): 1, (0, 1, 2): 1})  # five trials over three records
    three = trials.coincidence_rows(absorbed, 3, 5)
    singles, pairs = ["A_only", "B_only", "C_only"], ["A_B_only", "A_C_only", "B_C_only"]
    assert list(three) == singles + pairs + ["all", "neither", "alpha_A_B", "alpha_A_C", "alpha_B_C"]
    assert [three[key] for key in singles + pairs] == [[0, 5], [0, 5], [2, 5], [1, 5], [0, 5], [0, 5]]
    assert (
        three["all"] == [1, 5]
        and sum(three[key][0] for key in singles + pairs + ["all", "neither"]) == 5
    )
    assert (three["neither"], three["alpha_A_B"], three["alpha_A_C"]) == ([1, 5], [5, 2], [5, 6])
    assert three["alpha_B_C"] == [5, 6] and trials.coincidence_rows(Counter({(0,): 2}), 1, 2) == {}
    print(f"the two-record rows over {run} trials {rows}; the three-record rows {three}")
