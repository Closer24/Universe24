"""NATURE2: one record read by node-all 9d75a4904's records.read (with writer E's guard) and, where admitted, its books
and its meetings verdicts (decoder/shadow.py). Usage: python3 -I guardread.py <tree> <record .jsonl>"""

import sys
from pathlib import Path

TREE = Path(sys.argv[1])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

from tensor24.decoder import records, shadow  # noqa: E402

held, cause = records.read(sys.argv[2])
print(f"{Path(sys.argv[2]).name}: {'admitted by the guard' if held is not None else 'refused: ' + cause[:200]}")
if held is not None:
    for name, verdict in (("books", shadow.books(held)), ("meetings", shadow.meetings(held))):
        print(f"  {name}: {verdict['kind']}: {verdict['cause'][:200]}")
