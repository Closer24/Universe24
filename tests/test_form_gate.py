"""The form gate (paper/general_formula/cut_tools/form_gate.py): the body's lines, the sentences' words with a
formula as one word, and the status parentheses read as mid-sentence or fenceless."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "paper" / "general_formula" / "cut_tools" / "form_gate.py"


def load():
    spec = importlib.util.spec_from_file_location("form_gate", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["form_gate"] = module
    spec.loader.exec_module(module)
    return module


def test_the_body_the_words_and_the_parentheses() -> None:
    gate = load()
    text = "\n".join(
        [
            "\\maketitle",
            "\\section{Introduction}\\label{sec:intro}",
            "The clock's rate is $N = e^{-U}$ exactly (derived; lattice; S.31). It holds (theorem for the line; S.7), and more.",
            "\\begin{itemize}",
            "The rest (computed) stands; the rest stands too.",
            "\\section{Statements and Declarations}",
            "Not the body.",
        ]
    )
    lines = gate.body_lines(text)
    assert [number for number, _ in lines] == [3, 5]
    assert gate.words_of("the rate is $N = e^{-U}$ now") == 5
    marks = gate.parentheses_of(lines[0][1])
    assert [(mid, fenceless) for _, _, mid, fenceless in marks] == [(False, False), (True, True)]
    m = gate.measure(text)
    assert (
        m["sentences"] == 3
        and m["mid-sentence status parentheses"] == 2
        and m["fenceless status parentheses"] == 2
    )
    assert m["semicolons"] == 4


def test_the_main_is_measured_and_the_targets_are_named() -> None:
    gate = load()
    m = gate.measure((ROOT / "paper" / "general_formula" / "main.tex").read_text(encoding="utf-8"))
    assert m["sentences"] > 100 and m["longest"] >= m["mean"] and set(gate.TARGETS) <= set(m)
