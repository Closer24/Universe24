"""STOP1 reader: the shipped click world's ledger against its one Node-clock's (the probe lay click1), every round,
every Node-clock and every train: each site's counts against click1's site 0. A clock fact of the board: whether the
27 Node-clocks laid alike run alike, and alike with the one. Usage: python -I sites.py <27-site ledger> <1-site ledger>
"""

import json
import sys
from pathlib import Path

BIG, ONE = Path(sys.argv[1]), Path(sys.argv[2])
one = {}
for text in ONE.read_text(encoding="utf-8").splitlines():
    line = json.loads(text)
    one[(line["round"], line["train"])] = line["count"]
lines = alike = 0
first_off = None
rounds = set()
for text in BIG.read_text(encoding="utf-8").splitlines():
    line = json.loads(text)
    lines += 1
    rounds.add(line["round"])
    if one.get((line["round"], line["train"])) == line["count"]:
        alike += 1
    elif first_off is None:
        first_off = (line["round"], line["site"], line["train"])
print(f"{BIG.parent.parent.name}: {lines} count lines over {len(rounds)} rounds; alike with {ONE.parent.parent.name}'s "
      f"site 0: {alike} of {lines}; first apart: {first_off}")
