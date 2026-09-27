"""The old ALGEBRA.md citations rewrite to the condensed law's anchors from the mathematician's table (tools/rewrite_algebra_citations.py)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "rewrite_algebra_citations", ROOT / "tools" / "rewrite_algebra_citations.py"
)
assert _SPEC is not None and _SPEC.loader is not None
TOOL = importlib.util.module_from_spec(_SPEC)
sys.modules["rewrite_algebra_citations"] = TOOL
_SPEC.loader.exec_module(TOOL)
TABLE = TOOL.load_table()


def test_the_table_holds_every_section_of_chapter_nine():
    assert sorted(TABLE, key=lambda k: int(k.split(".")[1])) == [f"9.{n}" for n in range(1, 122)]
    assert all(v is None or v.startswith("#") for v in TABLE.values())


def test_a_group_with_qualifiers_becomes_its_anchors_once():
    text = "the wall (ALGEBRA.md 9.57 (1), 9.91 (2); 9.35 (2), (3) and 9.34 item 5)"
    new, unknown = TOOL.rewrite(text, TABLE)
    assert new == "the wall (ALGEBRA.md #the-line, #the-interval, #the-paces)"
    assert unknown == []
    new, _ = TOOL.rewrite("ALGEBRA.md 9.108 items 3, 11; ALGEBRA.md 9.117 item 2", TABLE)
    assert new == "ALGEBRA.md #the-paces, #the-primitives"


def test_a_history_section_drops_and_a_bare_number_stays_for_a_hand():
    new, _ = TOOL.rewrite("(ALGEBRA.md 9.16; the old step)", TABLE)
    assert new == "(ALGEBRA.md; the old step)"
    new, _ = TOOL.rewrite("g = 9.81 at the ground, (9.22 (4): W = 700), 9.113 item 2, (9.111)", TABLE)
    assert new == (
        "g = 9.81 at the ground, (ALGEBRA.md #a-familys-declaration: W = 700), "
        "ALGEBRA.md #the-primitives, (ALGEBRA.md #the-primitives)"
    )
    assert TOOL.bare_references(new) == ["9.81"]
    new, unknown = TOOL.rewrite("ALGEBRA.md 9.130 (1)", TABLE)
    assert new == "ALGEBRA.md 9.130 (1)" and unknown == ["9.130"]
