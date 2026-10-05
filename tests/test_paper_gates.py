"""The paper's mechanical gates (paper/general_formula/paper_gates.py): the struck phrases stand nowhere in main.tex and
supplement.tex, the numbers printed in two places agree, no mark or fence stands outside the key, and the derived or
computed marks naming no script and the fenceless marks are counted, a count that may only fall."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "paper" / "general_formula" / "paper_gates.py"
FENCELESS_MARKS_TONIGHT = 0  # every derived or theorem mark carries its fence since ecf653d
UNMATCHED_ROWS_TONIGHT = 0  # the gate of Table 1's move into the supplement (the advisor's word of 2026-10-05): rows of the claims table without a marked sentence at their place, a count that may only fall, at 0 before Table 1 leaves the main
MARKS_OUTSIDE_THE_KEY_TONIGHT = (
    0  # plain marks whose first word is not the key's, a count that may only fall
)
SCRIPTLESS_MARKS_TONIGHT = 11  # the ratchet: ten of 2026-10-04 and the atoms' ground levels computed by hand (S.60), named so at the advisor's word of 2026-10-05


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


def test_the_marks_naming_no_script_only_fall() -> None:
    module, texts = gates()
    scriptless = module.gate_scripts(texts)
    assert len(scriptless) <= SCRIPTLESS_MARKS_TONIGHT, len(scriptless)


def test_every_row_of_the_claims_table_has_a_marked_sentence_or_the_count_falls() -> None:
    module, texts = gates()
    claims_table = sys.modules["claims_table"]  # loaded beside the gates, from the paper's own directory
    assert module.gate_inputs_graph is claims_table.gate_inputs_graph
    misses = claims_table.unmatched_rows(texts["main.tex"], texts["supplement.tex"])
    assert len(misses) <= UNMATCHED_ROWS_TONIGHT, misses


def test_every_plain_mark_opens_with_the_keys_word_or_the_count_falls() -> None:
    _, texts = gates()
    claims_table = sys.modules["claims_table"]
    outside = claims_table.marks_outside_the_key(texts["main.tex"])
    assert len(outside) <= MARKS_OUTSIDE_THE_KEY_TONIGHT, outside


def test_no_breaker_is_keyed_to_another_derivation_after_a_renumbering() -> None:
    import json

    _, texts = gates()
    claims_table = sys.modules["claims_table"]
    breakers = json.loads((ROOT / "paper" / "claims_breakers.json").read_text(encoding="utf-8"))
    assert claims_table.misattached_breakers(texts["supplement.tex"], breakers) == []
