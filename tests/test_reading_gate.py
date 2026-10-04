def test_the_reading_gate_reruns_a_folder_and_compares_each_number_bit_for_bit(tmp_path, capsys):
    """The reading gate (tools/reading_gate.py) on a copy of the shipped Zeno world with a design of three seeds: the document's gate's table re-read row by row (the run, the trials, the back-in-time pass), MATCH on the numbers this test reads from the same run, DIFFERS on a wrong value and on a wrong label, a shipped screen table read in the block's place, UNFILLED without either, the report's shape (JSON lines, then the summary) and the exit code; the imports stand inside the test so that the file is the test alone, the room the ratchet gives it."""
    import json
    import shutil

    import pytest

    from event_universe.lattice import Lattice
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
    board = Lattice(load_world(folder / world), (lines := []).append)
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
        ("LATTICE", "run_inputs", "books pulse quanta", quanta),
        ("LATTICE", "run_inputs", "ticks", board.world.ticks),
        ("LATTICE", "back_in_time", f"intervals {board.world.ticks}", "MATCH"),
        ("NODEREADER", "meeting_trials", "ends in e body 0", ends),
        ("LATTICE", "meeting_trials", "trials", 3),
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
    assert read[-1]["reason"] == "the reading's own label is LATTICE"
    screen = f"| region | zeno_4 clicks | zeno_4 share |\n| --- | --- | --- |\n| body 0 | {takings} | 1.0 |\n| N | {takings} | |\n"
    document.write_text("# A copy\n\n## The reading\n\n" + screen, encoding="utf-8")
    read = report(0)
    assert [(line["reading"], line["table"]) for line in read] == [
        ("clicks body 0", "shipped"),
        ("clicks", "shipped"),
    ]
    document.write_text("# A copy\n", encoding="utf-8")
    assert report(1)[0]["verdict"] == "UNFILLED"


def test_the_trials_seed_each_record_by_a_hash_and_not_by_an_arithmetic_progression():
    """The trials tool's seeding (tools/meeting_trials.py, `hashed_state`; the mathematician's finding of 2026-10-04 on #1827 at the advisor's second): the generator of the files is affine, so trial labels in arithmetic progression (the seed times the records' number plus the record's number, the tool's rule before the fix) stay one progression at every depth of the draw and the trials' variates at a fixed depth are one Weyl sequence; with the files' generator and the control's labels_unit the states of 200 such trials after each of the first four draws have one consecutive difference modulo the modulus and their picks over a fixed total, (state times total) div 2^width, two adjacent consecutive differences modulo the total, one Weyl sequence (under the pick by the state modulo the total, until the clean main of 2026-10-04, the second draw fell in the even tenths alone; the pick from the high bits, the mathematician's #1793 comment 5981866600 K1, spreads the one progression evenly over the tenths and hides the defect from a histogram). The state from a hash of the label breaks the progression: over 1,000 such trials the tenth each of the first four draws falls in is flat by the chi-square on 9 degrees at 1 percent, and no three consecutive states share a difference. The engine's `drawn` is the generator read; the tool holds no number of the law."""
    from event_universe.features.click import drawn
    from tests.laws import ROOT, load_file

    trials = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py")
    multiplier, increment, width = 6364136223846793005, 1442695040888963407, (1 << 63) - 1
    labels_unit, modulus = 16305915721555161 + 2094318374976, 1 << 63
    tenths = [labels_unit // 10] * 10  # the draw's variate x mod unit read by its tenth

    def histograms(states):  # per depth the tenths' counts and the states after the draws
        found, after = [], []
        for depth in range(1, 5):
            counts, ends = [0] * 10, []
            for state in states:
                for _ in range(depth):
                    index, state = drawn(state, multiplier, increment, modulus, tenths)
                counts[index] += 1
                ends.append(state)
            found.append(counts)
            after.append(ends)
        return found, after

    affine, states = histograms([seed * 2 for seed in range(1, 201)])  # the rule before the fix
    hashed, _ = histograms([trials.hashed_state(seed * 2, width) for seed in range(1, 1001)])
    flat = [sum((count - 100) ** 2 / 100 for count in counts) for counts in hashed]  # chi-square on 9
    total = sum(tenths)
    steps = [{(b - a) % modulus for a, b in zip(ends, ends[1:], strict=False)} for ends in states]
    picks = [
        {(b - a) % total for a, b in zip(p, p[1:], strict=False)}
        for p in ([s * total // modulus for s in e] for e in states)
    ]
    print(
        f"the affine seeding's second draw over 200 trials {affine[1]}, its states' differences {[len(s) for s in steps]} "
        f"and its picks' {[len(p) for p in picks]}; the hash's four draws over 1,000 trials {hashed}, "
        f"their chi-squares on 9 degrees {[round(f, 1) for f in flat]} against the 1 percent 21.7"
    )
    assert all(len(s) == 1 for s in steps) and sum(affine[1]) == 200  # one progression at every depth
    assert all(len(p) <= 2 and max(p) - min(p) <= 1 for p in picks)  # the Weyl sequence's two steps
    assert all(f < 21.7 for f in flat)  # the hash's draws flat at every depth, 1 percent on 9 degrees
    states = [trials.hashed_state(label, width) for label in range(400)]
    assert all(0 <= state < modulus for state in states)
    assert all(b - a != c - b for a, b, c in zip(states, states[1:], states[2:], strict=False))


def test_the_pick_is_the_states_fraction_of_the_weights_total_and_no_low_bit_enters():
    """The generator's pick (ALGEBRA.md, The click is the meeting, How it chooses; the mathematician's line #1793 comment 5981866600 K1 with K2, the advisor's breaker 5981736108, two hands; `features/click.drawn`): the pick is the state's fraction of the weights' total, (x times total) div 2^width, and the index the first whose cumulative weight exceeds it, so the state's low bits, each with the period of its own count, enter no pick. With the shipped generator (the two slits' design, 6364136223846793005 and 1442695040888963407 at the modulus 2^63) from the seed 24, through the engine's own `drawn`: (a) the weights [1, 1] over 8,000 draws give each index near 4,000 and the equal consecutive pairs near 4,000 (the pick by the low bits, the state modulo the total until the clean main of 2026-10-04, alternated 0, 1 and gave none); (b) [1, 1, 1, 1] over 4,000 draws is no cycle of period 4 and flat, Pearson's chi-square under 11.3 on 3 degrees; (c) [2^62, 2^62, 2^62], a total above the modulus, draws the third index near a third (never under the pick by the low bits; no refusal of a total enters, K2); (d) a random list of weights is flat at the 1 percent band on 5 degrees; (e) [1, 7], the breaker's rate-8 conversion with the window 1, over 64 seeds through `drawn` alone: the first hit's interval spreads with a geometric tail beyond 8 and the hits within 8 are near 1 - (7 / 8)^8 of the seeds, not exactly 8 seeds per interval 1 to 8 (the shipped neutron conversion's world run costs about two seconds per seed and is not run here); and the law's count: over every state of the modulus 2^10 (the multiplier 1 and the increment 0 keep the state) the index i is drawn ceiling(c_(i+1) m / total) - ceiling(c_i m / total) times, within one of w_i m / total, a weight of 0 never, the lower index on a tie; the product state times total is above 2^width at any total above 1, so the pick is taken in Python's integers (the reviewer's #1793 comment 5982079576 D): a total near 2^60 given as numpy's 64-bit integers, the state among them, draws bit for bit as Python's integers do, both indices reached near half each, and the total 1 + 2^63 above the modulus draws its second index."""
    import json
    import math

    import numpy as np

    from event_universe.features.click import drawn
    from tests.laws import EVENTS

    design = json.loads((EVENTS / "two_slits" / "design.json").read_text(encoding="utf-8"))["draw"]
    multiplier, increment, modulus = design["multiplier"], design["increment"], 1 << 63
    assert (multiplier, increment) == (6364136223846793005, 1442695040888963407)

    def draws(weights, count, seed=24):  # the indices drawn from the seed, the state carried
        found, state = [], seed
        for _ in range(count):
            index, state = drawn(state, multiplier, increment, modulus, weights)
            found.append(index)
        return found

    def chi(found, weights):  # Pearson's chi-square against the weights' expectation
        total, n = sum(weights), len(found)
        return sum(
            (found.count(k) - n * w / total) ** 2 / (n * w / total) for k, w in enumerate(weights)
        )

    pairs = draws([1, 1], 8000)
    counts, equal = (
        [pairs.count(k) for k in (0, 1)],
        sum(a == b for a, b in zip(pairs, pairs[1:], strict=False)),
    )
    four, thirds = draws([1, 1, 1, 1], 4000), draws([1 << 62] * 3, 3000)
    weights = [int(w) for w in np.random.default_rng(24).integers(1, 50, 6)]
    hits = []
    for seed in range(64):  # the breaker's construction through drawn alone: the first hit's interval
        state = seed
        for interval in range(1, 200):
            index, state = drawn(state, multiplier, increment, modulus, [1, 7])
            if index == 0:
                hits.append(interval)
                break
    print(
        f"[1, 1] counts {counts} with {equal} equal pairs; [1, 1, 1, 1] chi-square {chi(four, [1] * 4):.2f}; "
        f"[2^62] x 3 third index {thirds.count(2)} of 3,000; {weights} chi-square {chi(draws(weights, 6000), weights):.2f}; "
        f"[1, 7] first hits {[hits.count(k) for k in range(1, 9)]} within 8, {sum(h > 8 for h in hits)} beyond, the last at {max(hits)}"
    )
    assert all(abs(c - 4000) < 3 * math.sqrt(2000) for c in (*counts, equal))
    assert any(four[k] != four[k + 4] for k in range(len(four) - 4)) and chi(four, [1] * 4) < 11.3
    assert abs(thirds.count(2) - 1000) < 3 * math.sqrt(1000 * 2 / 3)
    assert chi(draws(weights, 6000), weights) < 15.1
    within = sum(h <= 8 for h in hits)  # 64 x 0.656 = 42 +/- 3.8: within three deviations
    assert max(hits) > 8 and 31 <= within <= 53 and [hits.count(k) for k in range(1, 9)] != [8] * 8
    small, kept = 1 << 10, [3, 5, 0, 2]
    drawn_at = [drawn(state, 1, 0, small, kept)[0] for state in range(small)]
    below = [sum(kept[:k]) for k in range(len(kept) + 1)]  # the cumulative weight below each index
    for k, weight in enumerate(kept):
        count = math.ceil(below[k + 1] * small / sum(kept)) - math.ceil(below[k] * small / sum(kept))
        assert drawn_at.count(k) == count and abs(count - weight * small / sum(kept)) < 1
    assert drawn_at[0] == 0 and 2 not in drawn_at and drawn(0, 1, 0, small, [2, 0, 2])[0] == 0
    halves, state, typed = [1 << 59, 1 << 59], 24, np.int64(24)  # the total 2^60 in numpy's integers
    for _ in range(1000):
        (index, state), (found, typed) = (
            drawn(state, multiplier, increment, modulus, halves),
            drawn(typed, multiplier, increment, modulus, [np.int64(w) for w in halves]),
        )
        assert (index, state) == (found, int(typed)) and isinstance(typed, int)
    assert (
        440 < draws(halves, 1000).count(1) < 560
        and drawn(24, multiplier, increment, modulus, [1, 1 << 63])[0] == 1
    )


def test_the_trials_coincidence_rows_are_every_record_alone_and_every_pair(tmp_path):
    """The trials tool's coincidence rows (tools/meeting_trials.py, `coincidence_rows`; the advisor's breaker and the mathematician's audit, #1793 comments 5981736108 K6, 5982140872 B3; the Boss's 5981734131 item 6; two hands): the rows derived from the records' count and from no fixed key, every record alone and every pair (`itertools.combinations`), neither, and alpha per pair; on the shipped two-record anticoincidence world over three of the design's seeds the report's rows are the keys listed here by hand, A_only, B_only, both, neither and alpha in that order, the four counts summing to the trials and alpha the fraction of the counts; with three records the function gives the three singles, the three pairs by their letters, `all` for the trials where every record took, neither and the three alphas, a taking at the third record alone, which the fixed keys (0,), (1,), (0, 1) never counted, its own row, every trial with a taking in exactly one row; under two records no row."""
    import json
    from collections import Counter
    from fractions import Fraction

    from tests.laws import EVENTS, ROOT, load_file

    trials = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py")
    folder = EVENTS / "anticoincidence"
    design = json.loads((folder / "design.json").read_text(encoding="utf-8"))
    (tmp_path / "design.json").write_text(json.dumps({**design, "seeds": design["seeds"][:3]}), "utf-8")
    found = trials.reading(folder / "one_photon.json", tmp_path / "design.json", None)
    rows, run = found["coincidence"], found["trials"]
    assert list(rows) == ["A_only", "B_only", "both", "neither", "alpha"]  # the keys by hand, in order
    a_only, b_only, both, neither = (rows[key][0] for key in ("A_only", "B_only", "both", "neither"))
    assert a_only + b_only + both + neither == run == 3 and rows["A_only"][1] == run
    a, b = a_only + both, b_only + both
    alpha = Fraction(both * run, a * b) if a and b else None
    assert rows["alpha"] == ([alpha.numerator, alpha.denominator] if alpha is not None else None)
    took = Counter({(2,): 2, (0, 1): 1, (): 1, (0, 1, 2): 1})  # five trials over three records
    three = trials.coincidence_rows(took, 3, 5)
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
