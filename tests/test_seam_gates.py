"""The seam gates (paper/general_formula/seam_gates.py): the four reports run on the paper and their helpers read
numbers, segments and conditions as the hands specified (#1538, 6004213909 and 6004314227); no ratchet yet."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
FORMULA = ROOT / "paper" / "general_formula"


def seams() -> ModuleType:
    if str(FORMULA) not in sys.path:
        sys.path.insert(0, str(FORMULA))
    spec = importlib.util.spec_from_file_location("seam_gates", FORMULA / "seam_gates.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_number_holds_by_its_printed_digits() -> None:
    module = seams()
    assert module.holds("3.37", "the ratio $3.3713 \\times 10^6$ against")
    assert module.holds("1.9e-17", "below $1.9 \\times 10^{-17}$ at the bound")
    assert not module.holds("3.85", "the drop is $3.864$ percent")
    assert not module.holds("62.2", "the roots $15.28$ and $32.72$")


def test_the_numbers_of_a_sentence_leave_out_pointers_years_and_small_counts() -> None:
    module = seams()
    sentence = (
        "the fall $4 / 15$ at $[2, 3]$ against $2 / 7$ at $[3, 4]$ over $34$ Links in 2018 "
        "(derived; clicks; S.44, and S.53 of the long version; Section~\\ref{sec:fall}; Eq.~(10))"
    )
    assert module.numbers_of(sentence) == ["15", "34"]


def test_a_status_line_is_read_by_the_segment_a_mark_cites() -> None:
    module = seams()
    status = "(a), (b), (d) derived; (c), (e) to (j) derived under the proposition of Section 2.5.2; lattice; no run"
    assert (
        module.status_for(status, {"f"})
        == "(c), (e) to (j) derived under the proposition of Section 2.5.2"
    )
    assert module.status_for(status, {"a"}) == "(a), (b), (d) derived"
    assert module.status_for(status, set()) == status
    assert module.CONDITION.findall(
        "derived under the one assumption; to first order in U; lattice"
    ) == [
        "under the one assumption",
        "to first order in U",
    ]


def test_the_four_reports_run_on_the_paper() -> None:
    module = seams()
    main = module.MAIN.read_text(encoding="utf-8")
    supplement = module.SUPPLEMENT.read_text(encoding="utf-8")
    law = module.LAW.read_text(encoding="utf-8")
    for rows in (
        module.gate_pointer_holds(main, supplement),
        module.gate_status_rank(main, supplement),
        module.gate_law(main, law),
        module.gate_words(main, supplement),
    ):
        assert isinstance(rows, list)
        assert all(row.startswith(("main.tex:", "supplement.tex:")) for row in rows)


def test_the_free_nouns_are_read_on_their_word_boundary() -> None:
    module = seams()
    rows = module.gate_words("A NodeDetector clicks; the detector alone is barred; a grid is too.", "")
    assert len(rows) == 2
    assert "'detector'" in rows[0] and "'grid'" in rows[1]
