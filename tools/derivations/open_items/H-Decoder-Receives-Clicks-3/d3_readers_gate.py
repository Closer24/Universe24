"""Hand D3: the decoder's gate, the form that mends the readers (BRIEF_d (c); BRIEF_COMMON, Addition 4). Two checks, integers only.

(1) The credit line's keys against the decoder's view. Every key of every credit line of a clicks log is sorted into its class: NODE_OWN, the Node's own readings the decoder may read (point, kind, sense, beat, proper, windows, momentum, with identity the row's number and support the place's label by the owner's word); TAKE, the Node's own act numbers (taken, walls, excess, step); BOARD, the board's labels (interval, window, node_detector, label, event); NAMES, names the loader gave (family, before, realised, absorbed, emitted); BOOKS, the credit's books (kept, count, left, lost, source). The gate fails on a key outside the five classes, and reports per class how many lines carry each key.

(2) The readers' use of the board's interval and of floats, by function. tools/record_gates.py, tools/clicks_read.py and tools/look/captions.py are scanned function by function for a read of a line's `interval` key (`["interval"]`, `.get("interval")`, `interval_of(`), for `float(` and for `Fraction(`; the count per function is printed. The gate's rule (the law's line to be approved): a function of the decoder that reads a credit's `interval` reads the board's view; it is named, and a gate of general relativity resting on it is the board's and not an observer's.

Usage: PYTHONPATH=<worktree>/src python tools/derivations/open_items/H-Decoder-Receives-Clicks-3/d3_readers_gate.py [--log tools/derivations/open_items/H-Decoder-Receives-Clicks-3/out/clicks.jsonl] [--out tools/derivations/open_items/H-Decoder-Receives-Clicks-3/out]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]

CLASSES = {
    "NODE_OWN": ("point", "kind", "sense", "beat", "proper", "windows", "momentum", "identity", "support"),
    "TAKE": ("taken", "walls", "excess", "step"),
    "BOARD": ("interval", "window", "node_detector", "label", "event"),
    "NAMES": ("family", "before", "realised", "absorbed", "emitted"),
    "BOOKS": ("kept", "count", "left", "lost", "source"),
}
DECODER_VIEW = ("point", "kind", "identity", "sense", "beat", "proper", "windows", "momentum", "support")
PATTERNS = {
    "interval_read": re.compile(r'\[\s*"interval"\s*\]|\.get\(\s*"interval"|interval_of\('),
    "float": re.compile(r"\bfloat\("),
    "fraction": re.compile(r"\bFraction\("),
}


def functions_of(text: str) -> list[tuple[str, str]]:
    """The source split at its top-level and method `def` lines: (name, body)."""
    found, name, body = [], "<module>", []
    for line in text.splitlines():
        match = re.match(r"^\s*def\s+(\w+)\s*\(", line)
        if match:
            found.append((name, "\n".join(body)))
            name, body = match.group(1), [line]
        else:
            body.append(line)
    found.append((name, "\n".join(body)))
    return found


def scan(path: Path) -> dict:
    counts = {}
    for name, body in functions_of(path.read_text(encoding="utf-8")):
        row = {k: len(p.findall(body)) for k, p in PATTERNS.items()}
        if any(row.values()):
            counts[name] = row
    totals = {k: sum(r[k] for r in counts.values()) for k in PATTERNS}
    return {"file": str(path.relative_to(ROOT)), "totals": totals, "per_function": counts}


def keys_gate(log: Path) -> dict:
    credits = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    credits = [x for x in credits if x.get("event") == "credit"]
    known = {k for keys in CLASSES.values() for k in keys}
    per_key: dict[str, int] = {}
    unknown: dict[str, int] = {}
    for line in credits:
        for key in line:
            per_key[key] = per_key.get(key, 0) + 1
            if key not in known:
                unknown[key] = unknown.get(key, 0) + 1
    by_class = {c: {k: per_key.get(k, 0) for k in keys if k in per_key} for c, keys in CLASSES.items()}
    constant = {k: len({json.dumps(x.get(k), default=str) for x in credits}) for k in per_key}
    null = {k: sum(1 for x in credits if x.get(k) is None) for k in per_key}
    view_only = [{k: x.get(k) for k in DECODER_VIEW} for x in credits[:3]]
    return {
        "credit_lines": len(credits),
        "keys_by_class": by_class,
        "keys_outside_the_classes": unknown,
        "distinct_values_per_key": constant,
        "null_per_key": null,
        "decoder_view_first_three_lines": view_only,
        "gate": "PASS" if not unknown else "FAIL: a key outside the five classes",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--log", type=Path, default=HERE.parent / "out" / "clicks.jsonl")
    parser.add_argument("--out", type=Path, default=HERE.parent / "out")
    args = parser.parse_args()
    found = {
        "keys": keys_gate(args.log) if args.log.exists() else "no log",
        "readers": [scan(ROOT / "tools" / "record_gates.py"), scan(ROOT / "tools" / "clicks_read.py"), scan(ROOT / "tools" / "look" / "captions.py")],
    }
    (args.out / "readers_gate.json").write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
