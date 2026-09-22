"""Helpers for the thirty-page assembly: blocks of the base text (the paper at
commit b684ba0b, the last form before the cut) selected by anchor.

The base is read from the repository's history, never from a copy: the one
canonical text of that form is the commit itself.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE_COMMIT = "b684ba0b"
BASE = subprocess.run(
    ["git", "-C", str(ROOT), "show", f"{BASE_COMMIT}:paper/general_formula/main.tex"],
    check=True, capture_output=True, text=True).stdout


def B(start, end=None, include_end=False):
    """The base text from the first line containing `start` to the line before the first later line containing `end`."""
    i = BASE.index(start)
    i = BASE.rfind("\n", 0, i) + 1
    if end is None:
        return BASE[i:]
    j = BASE.index(end, i + len(start))
    if include_end:
        j = BASE.index("\n", j) + 1
    else:
        j = BASE.rfind("\n", 0, j) + 1
    return BASE[i:j]


def sub(text, old, new, count=1):
    """Replace `old` by `new` in `text`, whitespace tolerant, exactly `count` times."""
    pat = r"\s+".join(re.escape(t) for t in old.split())
    m = re.findall(pat, text)
    assert len(m) == count, ("sub", len(m), count, old[:70])
    return re.sub(pat, lambda _: new, text)


def cutp(text, start, end):
    """Remove from `start` to just before `end` inside `text` (whitespace tolerant anchors)."""
    ps = r"\s+".join(re.escape(t) for t in start.split())
    pe = r"\s+".join(re.escape(t) for t in end.split())
    ms = re.search(ps, text)
    assert ms, ("cutp start", start[:60])
    me = re.search(pe, text[ms.end():])
    assert me, ("cutp end", end[:60])
    return text[:ms.start()] + text[ms.end() + me.start():]
