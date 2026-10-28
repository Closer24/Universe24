"""Records and ledgers on which records.read or tools/tensor24_decode.py raises instead of naming a cause.

usage: python -I decoder_raises.py <worktree> <scratch folder>
Sofer's G1 to G3 (a record that reads raising on a click's or a holding's fields, floats and truth values read as
whole numbers, a click booked twice) are not re-run here. Each case prints what records.read returns, or what it
raises, and the tool's exit code and last line.
"""

import json
import subprocess
import sys
from pathlib import Path

WT, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(WT / "src")]
from tensor24.decoder import records  # noqa: E402

PY = "/home/user/Universe24/venv314/bin/python"
HEADER = {"kind": "header", "record": "tensor24", "major": 1, "minor": 0}
END = {"kind": "end", "rounds": 1, "digest": "", "undone": 0, "exact": 1}
RATE = {"kind": "rate", "round": 1, "site": 0, "count": 1, "dial": 0, "k": 1}
CLICK = {"kind": "whole", "round": 1, "site": 0, "count": 1, "train": 0, "ends": [],
         "taken": [{"train": 1, "windings": [7, 4], "kept": [3, 2]}], "laid": [{"train": 0, "windings": [0, 4], "kept": [0, 0]}]}
LEDGER = [{"round": 1, "at": at, "train": t, "windings": w} for t, pair in {0: (0, 4), 1: (10, 7)}.items()
          for at, w in zip(("step", "clicks"), pair, strict=True)]


def lines(*xs):
    return "".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in xs)


def case(label, record, ledger=None, ledger_path=None):
    folder = OUT / "".join(ch if ch.isalnum() else "_" for ch in label)[:60]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "record.jsonl"
    path.write_text(record, encoding="utf-8")
    try:
        got, cause = records.read(str(path))
        verdict = f"read: {'a record' if got else 'None'}, cause {cause!r}"
    except BaseException as error:  # noqa: BLE001
        verdict = f"records.read RAISED {type(error).__name__}: {str(error)[:70]}"
    args = [str(path)]
    if ledger is not None:
        (folder / "ledger.jsonl").write_text(ledger, encoding="utf-8")
        args.append(str(folder / "ledger.jsonl"))
    if ledger_path is not None:
        args.append(ledger_path)
    tool = subprocess.run([PY, "-I", str(WT / "tools" / "tensor24_decode.py"), *args], capture_output=True, text=True)
    tail = ((tool.stderr or tool.stdout).strip().splitlines() or [""])[-1][:110]
    print(f"{label}\n    {verdict}\n    tool: exit {tool.returncode}, {tail}")


case("control: the decoder's own lawful record, with its ledger", lines(HEADER, CLICK, RATE, END), lines(*LEDGER))
case("a line nested 100,000 deep", lines(HEADER, "[" * 100000 + "]" * 100000, END))
case("an object nested 100,000 deep inside a lawful line",
     lines(HEADER, '{"kind": "rate", "round": 1, "site": 0, "count": 1, "k": 1, "x": ' + "[" * 100000 + "]" * 100000 + "}", END))
case("a whole number of 4,301 digits in a field (the schema: whole numbers of any width)",
     lines(HEADER, json.dumps(RATE).replace('"dial": 0', '"dial": ' + "9" * 4301), END))
case("the ledger's path given, its file absent (the plan: those rows read NOT READ, the cause named)",
     lines(HEADER, CLICK, RATE, END), ledger_path=str(OUT / "no_such_ledger.jsonl"))
case("a ledger with a blank line", lines(HEADER, CLICK, RATE, END), lines(*LEDGER) + "\n")
case("a ledger line that is no JSON", lines(HEADER, CLICK, RATE, END), lines(*LEDGER, "no json"))
case("a ledger line that is a list", lines(HEADER, CLICK, RATE, END), lines(*LEDGER, [1, "step", 0, 4]))
case("a ledger line without its 'at'", lines(HEADER, CLICK, RATE, END), lines(*LEDGER, {"round": 1, "train": 0, "windings": 4}))
case("a whole click at a Node-clock with no rate line (the tool's ticks)",
     lines(HEADER, CLICK, {**RATE, "site": 1}, END))
case("a label holding U+2028 written raw (json.dumps with ensure_ascii=False: lawful JSON)",
     json.dumps(HEADER) + "\n" + json.dumps({**RATE, "note": "a\u2028b"}, ensure_ascii=False) + "\n" + json.dumps(END) + "\n")
case("a label holding U+0085 written raw (lawful JSON)",
     json.dumps(HEADER) + "\n" + json.dumps({**RATE, "note": "a\u0085b"}, ensure_ascii=False) + "\n" + json.dumps(END) + "\n")
