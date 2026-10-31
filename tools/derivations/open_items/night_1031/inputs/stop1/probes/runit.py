"""The tree's own runner (main.ran) on the three files: the departures it names, or its record's sha256 and end line.
Usage: python -I runit.py <tree> <files dir> <record .jsonl>"""
import hashlib, json, sys
from pathlib import Path
TREE, FILES, RECORD = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)
from tensor24 import main as tmain
from tensor24.runner import run as runmod
found = tmain.ran([FILES.joinpath(n + ".json") for n in ("universe", "piece", "setting")], RECORD)
print("departures named:", found[:3])
if not found:
    print("record sha256:", hashlib.sha256(RECORD.read_bytes()).hexdigest(), "; ledger sha256:", hashlib.sha256(runmod.ledger_of(RECORD).read_bytes()).hexdigest())
    print("end:", RECORD.read_text(encoding="utf-8").splitlines()[-1][:400])
