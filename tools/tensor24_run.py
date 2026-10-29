"""Tensor24's run (stage 10): the three files run to a record of the schema, every due beat firing in every round
until each Node-clock's count stands at the setting's ticks, the rewind checked, every departure of the files named
and no record written past one.

Usage: python -I tools/tensor24_run.py <universe> <piece> <setting> <record .jsonl>
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tensor24 import main as tensor24  # noqa: E402


def main() -> int:
    """Run the files, print each departure or the record written; exit 1 on a departure."""
    parser = argparse.ArgumentParser(description="Tensor24's run: three files to a record.")
    for name in ("universe", "piece", "setting", "record"):
        parser.add_argument(name, type=Path)
    held = parser.parse_args()
    found = tensor24.ran([held.universe, held.piece, held.setting], held.record)
    print("\n".join(found) or f"{held.record}: written")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
