"""Tensor24's three files checked: whole numbers alone, every divisor at least 1, every reference whole.

Usage: `python tools/tensor24_files.py [universe piece setting]` prints every departure (the examples by default)
and exits 1 if there is one.
"""

import sys
from pathlib import Path

from tensor24.runner.files import departures

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"


def main(argv: list[str]) -> int:
    files = [Path(a) for a in argv] or [
        EXAMPLES / f"{name}.json" for name in ("universe", "piece", "setting")
    ]
    found = departures(*files)
    print(
        "\n".join(found)
        if found
        else "the three files hold: whole numbers, divisors at least 1, references whole"
    )
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
