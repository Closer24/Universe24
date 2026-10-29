"""Tensor24's three files checked and loaded: whole numbers alone, the integers and the sides at least 1, each train,
kind, part and site referred to there; then each refusal of the load by name (a kind the 24's five do not hold, a twin
hand, a channel the 24 forbid, a gradient off A1, the strides before stage 7c, a component off its train's rows).

Usage: `python tools/tensor24_files.py [universe piece setting]` prints every departure (the examples by default)
and exits 1 if there is one; files that are not three are argparse's usage error. The fine tooth within its teeth is
the load's promise, read where the teeth are.
"""

import argparse
import json
import sys
from pathlib import Path

from tensor24.main import made
from tensor24.runner.files import NAMES, departures, sites_of
from tensor24.runner.load import load

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "tensor24"


def loaded(universe: Path, piece: Path, setting: Path) -> list[str]:
    """The load's departures of three files the checker holds, on the kinds of the piece's board."""
    u, p, s = (json.loads(path.read_text(encoding="utf-8")) for path in (universe, piece, setting))
    return load(u, s, sites_of(p["shape"]), *made(tuple(p["shape"])))[1]


def main(argv: list[str]) -> int:
    """Check and load the files, print each departure or that they hold, and return 1 on a departure."""
    parser = argparse.ArgumentParser(description="Tensor24's three files checked and loaded.")
    parser.add_argument(
        "files", nargs="*", type=Path, help=f"{' '.join(NAMES)}, or none for the examples"
    )
    given = parser.parse_args(argv).files
    if len(given) not in (0, len(NAMES)):
        parser.error("the three files, or none for the examples")
    files = given or [EXAMPLES / f"{name}.json" for name in NAMES]
    found = departures(*files)
    found = found or loaded(*files)
    print(
        "\n".join(found)
        if found
        else "the three files hold and load: whole numbers, the integers at least 1, references whole, every"
        " kind, part, channel and component the 24's (the fine tooth's promise is the load's, where the teeth are read)"
    )
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
