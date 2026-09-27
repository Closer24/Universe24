"""One owner per area (tools/ownership.py; #1198, gate 8): another owner's area needs its hand-over line in the body."""

from __future__ import annotations

import os
from pathlib import Path

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
GATE = load_file("ownership", ROOT / "tools" / "ownership.py")
OWNERS = {
    "Main Loop": {
        "sessions": ["session_loop"],
        "areas": ["src/core/", "src/core/rule3.py", "law/step.json"],
    },
    "Paper Writer": {"sessions": ["session_paper"], "areas": ["tools/check.py"]},
}
BY_PAPER = "Lines: tools +1 -1\n\nhttps://claude.ai/code/session_loop quoted\nhttps://claude.ai/code/session_paper\n"


def test_the_pull_request_touches_only_its_authors_areas_or_handed_ones():
    if GATE.on_pull_request(dict(os.environ)):
        changed = GATE.changed_files(ROOT, GATE.base_ref())
        assert GATE.violations(changed, os.environ.get("PR_BODY", ""), GATE.load_owners()) == []
    owners = GATE.load_owners()
    sessions = [s for entry in owners.values() for s in entry["sessions"]]
    assert len(sessions) == len(set(sessions))
    for entry in owners.values():
        assert all((ROOT / area).exists() for area in entry["areas"])


def test_the_longest_area_names_the_owner_and_the_last_session_link_the_author():
    assert GATE.owner_of("src/core/rule3.py", OWNERS) == "Main Loop"
    assert GATE.owner_of("src/core_notes.md", OWNERS) is None
    assert GATE.owner_of("tests/test_a.py", OWNERS) is None
    assert GATE.author(BY_PAPER, OWNERS) == "Paper Writer"
    assert GATE.author("no link", OWNERS) is None
    assert GATE.author("https://claude.ai/code/session_other", OWNERS) is None


def test_another_owners_file_fails_until_that_owner_hands_it_over():
    changed = ["tools/check.py", "tests/test_a.py", "src/core/rule3.py", "law/step.json"]
    found = GATE.violations(changed, BY_PAPER, OWNERS)
    assert found == [
        f"{path} is Main Loop's area and Paper Writer touches it: add 'HANDED BY Main Loop: {path}' to the body"
        for path in ("src/core/rule3.py", "law/step.json")
    ]
    assert (
        GATE.violations(changed, BY_PAPER + "HANDED BY Main Loop: src/core/, law/step.json\n", OWNERS)
        == []
    )
    wrong = BY_PAPER + "HANDED BY Paper Writer: src/core/ law/step.json\n"
    assert len(GATE.violations(changed, wrong, OWNERS)) == 2
    assert len(GATE.violations(["tools/check.py"], "no link", OWNERS)) == 1
