"""The paper's mechanical gates (paper/general_formula/paper_gates.py; the advisor's proposal of 2026-10-04 and the owner's
word "everything tonight"): the struck phrases stand nowhere in main.tex and supplement.tex, the numbers printed in two
places agree, and no mark or fence stands outside the key; the derived and theorem marks with no fence beside them are the
25 places listed on #1793 for the hands' word, and the count may only fall."""

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "paper" / "general_formula" / "paper_gates.py"
FENCELESS_MARKS_TONIGHT = 25  # the hands' word on each fence brings this to 0


def gates() -> tuple[ModuleType, dict[str, str]]:
    spec = importlib.util.spec_from_file_location("paper_gates", GATES)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    texts = {name: path.read_text(encoding="utf-8") for name, path in module.FILES.items()}
    return module, texts


def test_the_struck_phrases_stand_nowhere_in_the_paper() -> None:
    module, texts = gates()
    assert module.gate_stale(texts) == []


def test_every_number_printed_in_two_places_agrees() -> None:
    module, texts = gates()
    assert module.gate_twins(texts) == []


def test_every_mark_and_fence_is_in_the_key_and_the_fenceless_marks_only_fall() -> None:
    module, texts = gates()
    misses = module.gate_marks(texts)
    outside = [m for m in misses if "outside the key" in m]
    assert outside == []
    fenceless = [m for m in misses if "no fence beside it" in m]
    assert len(fenceless) <= FENCELESS_MARKS_TONIGHT, fenceless
