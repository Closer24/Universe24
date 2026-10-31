"""STOP1 reader: one line per run from stopped.py's outputs (rec/<name>_1.txt), with the two runs' byte check from
rec/batch.log. Usage: python -I summary.py <rec dir> [name ...]"""

import re
import sys
from pathlib import Path

REC = Path(sys.argv[1])
names = sys.argv[2:] or sorted({p.name[:-6] for p in REC.glob("*_1.txt")})
log = REC.joinpath("batch.log").read_text(encoding="utf-8") if REC.joinpath("batch.log").exists() else ""


def grab(pattern, text, group=1):
    m = re.search(pattern, text, re.M)
    return m.group(group) if m else "-"


for name in names:
    p = REC.joinpath(name + "_1.txt")
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    if "ran:" not in t:
        continue
    ran = grab(r"^ran: (\d+) of (\d+)", t) + "/" + grab(r"^ran: (\d+) of (\d+)", t, 2)
    named = grab(r"named: (\[.*?\]|None)", t)
    named = "none" if named == "None" else grab(r"'round (\d+):", named)
    wide = grab(r"^widest over the run: (\d+) bits; least: (\d+)", t, 2) + ".." + grab(r"^widest over the run: (\d+) bits", t)
    firsts = grab(r"^first round past 8/16/32/64/128 bits: (.*)$", t)
    back = grab(r"board and every tooth: (True|False)", t)
    held = grab(r"run back holds for the last (\d+) of (\d+) rounds \(back to round (\d+)\)", t, 3)
    ret = grab(r"start seed again: (\w+)", t)
    books = grab(r"^books: (SHOWN|NOT SHOWN|NOT READ|NO CLICK)", t)
    places = grab(r"^places whose q sum to other than 0: (\d+ of \d+)", t)
    turns = grab(r"^the 24: alike in (\d+ of 24 turns over \d+ rounds)", t)
    chain = grab(r"^board chain digest: (\w{16})", t)
    rec = grab(r"^record sha256: (\w{16})", t)
    led = grab(r"ledger sha256: (\w{16})", t)
    lines = grab(r"^click lines: (\d+)", t)
    alike = grab(rf"^\S+ {re.escape(name)} \(.*?\): (outputs \w+, records \w+)", log)
    print(f"{name}: ran {ran}; named {named}; bits {wide}; past 8/16/32/64/128 {firsts}; run back exact {back}, "
          f"held back to round {held}; whole state back at the start seed at round {ret}; the 24 {turns}; "
          f"books {books} ({places} places open); click lines {lines}; chain {chain}; record {rec}; ledger {led}; "
          f"twice: {alike}")
