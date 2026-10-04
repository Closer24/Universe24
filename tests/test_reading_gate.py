def test_the_reading_gate_reruns_a_folder_and_compares_each_number_bit_for_bit(tmp_path, capsys):
    """The reading gate (tools/reading_gate.py) on a copy of the shipped Zeno world with a design of three seeds: the document's gate's table re-read row by row (the run, the trials, the back-in-time pass), MATCH on the numbers this test reads from the same run, DIFFERS on a wrong value and on a wrong label, a shipped screen table read in the block's place, UNFILLED without either, the report's shape (JSON lines, then the summary) and the exit code; the imports stand inside the test so that the file is the test alone, the room the ratchet gives it."""
    import json
    import shutil

    import pytest

    from event_universe.game_board import GameBoard
    from event_universe.world_files import load_world
    from tests.laws import EVENTS, ROOT, load_file

    gate = load_file("reading_gate", ROOT / "tools" / "reading_gate.py")
    folder, world, document = (
        tmp_path / "zeno",
        "zeno_4.json",
        tmp_path / "zeno" / "blind_and_reading.md",
    )
    folder.mkdir()
    for name in (world, "zeno_4.mode.json"):
        shutil.copy(EVENTS / "zeno" / name, folder / name)
    design = json.loads((EVENTS / "zeno" / "design.json").read_text(encoding="utf-8"))
    design["seeds"] = design["seeds"][:3]
    (folder / "design.json").write_text(json.dumps(design), encoding="utf-8")
    board = GameBoard(load_world(folder / world), (lines := []).append)
    for _ in range(board.world.ticks):
        board.step()
    clicks = [line for line in lines if line["event"] == "credit" and line["label"] == "NODEREADER"]
    takings, quanta = sum(1 for line in clicks if line["taken"]), board.books()["pulse"]["quanta"]
    givings = sum(
        1 for line in clicks if line["given"]
    )  # the record takes climbing, gives back descending
    assert takings + givings == sum(int(line["count"]) for line in clicks)
    trials = gate.trials_reading(folder / world, folder / "design.json", None)
    ends = trials["ends_in_part"]["body 0"].get("e", [0])[0]
    rows = [
        ("NODEREADER", "run_inputs", "takings body 0", takings),
        ("NODEREADER", "run_inputs", "clicks", takings),
        ("GAMEBOARD", "run_inputs", "books pulse quanta", quanta),
        ("GAMEBOARD", "run_inputs", "ticks", board.world.ticks),
        ("GAMEBOARD", "back_in_time", f"intervals {board.world.ticks}", "MATCH"),
        ("NODEREADER", "meeting_trials", "ends in e body 0", ends),
        ("GAMEBOARD", "meeting_trials", "trials", 3),
    ]
    wrong = [
        ("NODEREADER", "run_inputs", "takings body 0", takings + 1),
        ("NODEREADER", "run_inputs", "ticks", 48),
    ]
    head = (
        "# A copy of the Zeno world\n\n## The gate's table\n\n| label | world | by | reading | value |\n"
    )

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
        str(takings),
        "NODEREADER",
        "MATCH",
        "3",
    )
    written(rows + wrong)
    read = report(1)
    assert [line["verdict"] for line in read[-2:]] == ["DIFFERS", "DIFFERS"]
    assert (read[-2]["read"], read[-2]["value"]) == (
        str(takings),
        str(takings + 1),
    ) and "reason" not in read[-2]
    assert read[-1]["reason"] == "the reading's own label is GAMEBOARD"
    screen = f"| region | zeno_4 clicks | zeno_4 share |\n| --- | --- | --- |\n| body 0 | {takings} | 1.0 |\n| N | {takings} | |\n"
    document.write_text("# A copy\n\n## The reading\n\n" + screen, encoding="utf-8")
    read = report(0)
    assert [(line["reading"], line["table"]) for line in read] == [
        ("clicks body 0", "shipped"),
        ("clicks", "shipped"),
    ]
    document.write_text("# A copy\n", encoding="utf-8")
    assert report(1)[0]["verdict"] == "UNFILLED"
