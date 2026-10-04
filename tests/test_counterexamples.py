"""The breaker's gate (the method of 2026-10-04): every row of tools/derivations/counterexamples.py, a claim of the paper tried inside its condition and outside it in the algebra of Rule3's line, is green, its key a row of paper/claims_breakers.json of the kind (a); a red row is listed in RED_ROWS by key and reported for the hands, never silenced by rewording a claim."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BREAKER = ROOT / "tools" / "derivations" / "counterexamples.py"
RED_ROWS: set[str] = set()  # a finding for the hands: the rows that are BROKE or FENCE today, by key


def breaker():
    spec = importlib.util.spec_from_file_location("counterexamples", BREAKER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_breaker_row_is_green_and_keyed_to_the_claims_table():
    """Every row's key is a kind (a) row of the claims table; every row is green but those named red; the red set only shrinks."""
    table = json.loads((ROOT / "paper" / "claims_breakers.json").read_text(encoding="utf-8"))
    results = breaker().run()
    assert results, "the registry holds rows"
    for key, _, _ in results:
        assert key in table and table[key]["kind"] == "a", key
    red = {key for key, state, _ in results if state != "green"}
    assert red == RED_ROWS, [
        (key, state, witness) for key, state, witness in results if state != "green"
    ]
