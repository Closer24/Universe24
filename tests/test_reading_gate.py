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
