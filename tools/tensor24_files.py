"""Tensor24's three files checked: whole numbers alone, the integers and the sides at least 1, every reference whole.

Usage: `python tools/tensor24_files.py [universe piece setting]` prints every departure (the examples by default)
and exits 1 if there is one, 2 if the files are not three.
"""

import sys
from pathlib import Path

from tensor24.runner.files import departures

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"
NAMES = ("universe", "piece", "setting")


def main(argv: list[str]) -> int:
    if len(argv) not in (0, len(NAMES)):
        print(f"usage: tensor24_files.py [{' '.join(NAMES)}]: the three files, or none for the examples")
        return 1 + 1
    files = [Path(a) for a in argv] or [EXAMPLES / f"{name}.json" for name in NAMES]
    universe, piece, setting = files
    found = departures(universe, piece, setting)
    print(
        "\n".join(found)
        if found
        else "the three files hold: whole numbers, the integers at least 1, references whole"
    )
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
