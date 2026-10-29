"""The reader's sketch of tests more for the decoder (eighth review), beside tests/test_the_tensor24_decoder.py.

usage (a worktree's root, or a mutant's scratch tree, with this file copied into its tests/):
    python -m pytest -q tests/decoder_tests_s8.py -k "not required"   # part A: passes on 823690afc
    python -m pytest -q tests/decoder_tests_s8.py -k required         # part B: the required readings, fails on it

Part A pins the halves of the new guards and readings that no test holds (each kills one surviving mutant of
decoder_mutants_s8.py). Part B pins what the review requires: the wind over every train of the header, the books tied
to the click, and a k that is no bit not read.
"""

import subprocess
import sys

import pytest

from tensor24.decoder import books, clocks, records
from tests.test_the_tensor24_decoder import (
    END,
    GOOD,
    HEADER,
    PAIR,
    TAKE,
    TOOL,
    click,
    holding,
    ledger,
    rate,
    read,
    text,
    without,
)


def cause_of(lines, tmp_path):
    path = tmp_path / "record.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read(str(path))[1]


def ledger_cause(lines, tmp_path):
    path = tmp_path / "ledger.jsonl"
    path.write_text(text(lines), encoding="utf-8")
    return records.read_ledger(str(path))[1]


# part A


def test_a_label_holding_no_label_is_not_read(tmp_path):
    assert cause_of([{**HEADER, "engine": [1]}, END], tmp_path) == "line 1's engine has not its shape in the schema"
    assert cause_of([HEADER, {**END, "digest": 1}], tmp_path) == "line 2's digest has not its shape in the schema"


def test_the_first_misfit_field_is_named(tmp_path):
    line = {**rate(1, 0, 1, 1), "count": 0.5, "k": 0.5}
    assert cause_of([HEADER, line, END], tmp_path) == "line 2's count has not its shape in the schema"


def test_the_order_holds_the_train(tmp_path):
    one, zero = {**TAKE, "train": 1}, {**TAKE, "train": 0}
    assert cause_of([HEADER, one, zero, END], tmp_path) == "the events stand out of the schema's order"
    assert cause_of([HEADER, zero, one, END], tmp_path) == ""


def test_an_event_without_its_round_is_not_read(tmp_path):
    line = without(rate(1, 0, 1, 1), "round")
    assert cause_of([HEADER, line, END], tmp_path) == "line 2 stands at no whole round and site"


def test_a_pair_booked_again_in_the_clicks_laid_and_a_click_of_three_ends(tmp_path):
    again = {**PAIR, "laid": [holding(1, (0, 9))]}
    three = click(1, 0, ends=[*PAIR["ends"], PAIR["ends"][1]])
    assert cause_of([HEADER, again, END], tmp_path) == "line 2's whole click books at the click and again at its ends"
    assert cause_of([HEADER, three, END], tmp_path) == "line 2's whole click's ends number 3, where the schema holds both or none"


@pytest.mark.parametrize("key", ["round", "train"])
def test_a_ledger_line_without_its_round_or_train_is_not_read(tmp_path, key):
    line = without({"round": 1, "at": "step", "train": 0, "wind": 4}, key)
    stands = "the ledger's line 5 stands at no whole round and train, after the step or the clicks"
    assert ledger_cause([*GOOD, line], tmp_path) == stands


@pytest.mark.parametrize(
    "lacking",
    [
        click(1, 0, [without(holding(1, (7, 4), (3, 2)), "windings")], [holding(0, (0, 4))]),
        click(1, 0, [holding(1, (7, 4), (3, 2))], [without(holding(0, (0, 4)), "kept")]),
    ],
)
def test_a_holding_that_lacks_its_windings_or_a_laid_one_its_kept_reads_not_read(tmp_path, lacking):
    verdict = books.row_15(read([HEADER, lacking, END], tmp_path), GOOD)
    assert verdict["kind"] == "NOT READ" and verdict["cause"].endswith("lacks a field its books are read from")


def test_one_click_closed_and_one_open_is_not_shown(tmp_path):
    opened = {**click(1, 1, [holding(1, (7, 4), (3, 3))], [holding(0, (0, 4))])}
    verdict = books.row_15(read([HEADER, TAKE, opened, END], tmp_path), ledger(1, {0: (0, 8), 1: (10, 2)}))
    assert verdict["kind"] == "NOT SHOWN" and verdict["cause"].startswith("the books open at 1 of")


def test_a_round_whose_lines_hold_other_trains_or_lack_a_wind_is_not_read(tmp_path):
    record = read([HEADER, TAKE, END], tmp_path)
    wider = [GOOD[0], GOOD[1], {"round": 1, "at": "clicks", "train": 1, "wind": 6}]
    windless = [*GOOD[:-1], without(GOOD[-1], "wind")]
    assert all(books.row_15(record, held)["kind"] == "NOT READ" for held in (wider, windless))


def test_a_major_that_is_a_truth_value_is_no_major(tmp_path):
    assert cause_of([{**HEADER, "major": True}, END], tmp_path) == "the header holds no major version"


def tool(*args):
    return subprocess.run([sys.executable, "-I", str(TOOL), *map(str, args)], capture_output=True, text=True)


def test_the_tool_on_three_arguments_on_a_record_not_read_and_on_ticks_not_read(tmp_path):
    broken, clicked = tmp_path / "broken.jsonl", tmp_path / "clicked.jsonl"
    broken.write_text(text([HEADER, "no json", END]), encoding="utf-8")
    clicked.write_text(text([HEADER, TAKE, END]), encoding="utf-8")
    three, unread, ticks = tool(broken, broken, broken), tool(broken), tool(clicked)
    assert three.returncode == 1 + 1 and three.stdout == "" and three.stderr.startswith("usage:")
    assert unread.returncode == 0 and unread.stderr == "" and unread.stdout == "not read: line 2 is no JSON object with its kind\n"
    assert ticks.returncode == 0 and "0 read, 1 not read, the first not read at round 1, site 0" in ticks.stdout


# part B: the required readings


HT = {**HEADER, "trains": [{"index": t, "label": "t", "kinds": [0], "part": 1, "winding": 1} for t in (0, 1)]}


@pytest.mark.parametrize("held", [{7: (5, 5)}, {0: (0, 4)}, {1: (10, 10)}])
def test_required_the_wind_is_read_over_every_train_of_the_header(tmp_path, held):
    record = read([HT, TAKE, END], tmp_path)
    assert books.row_15(record, GOOD)["kind"] == "SHOWN"
    assert books.row_15(record, ledger(1, held))["kind"] == "NOT READ"


@pytest.mark.parametrize(
    "broken",
    [
        {**click(1, 0), "train": 1, "q": 5},  # no books at all
        {**click(1, 0, [holding(1, (4, 8))], [holding(0, (4, 0))]), "train": 1, "q": 4},  # a take that gains
        {**click(1, 0, [holding(0, (4, 0))], [holding(1, (0, 4))]), "train": 1, "q": 4},  # its own train not taken
    ],
)
def test_required_the_books_hold_the_click(tmp_path, broken):
    verdict = books.row_15(read([HT, broken, END], tmp_path), ledger(1, {0: (4, 4), 1: (6, 6)}))
    assert verdict["kind"] != "SHOWN"


@pytest.mark.parametrize("k", [1 + 1, -1])
def test_required_a_k_that_is_no_bit_is_not_read(k):
    assert clocks.ticks_to([(1, k)], 1 + 1 + 1) is None
