"""Tensor24's three files checked and loaded: whole numbers alone, the integers and the sides at least 1, each train,
kind, part and site referred to there, and no coupling; then each refusal of the load by name (a kind none of the
eight, a kind with no whole basis outside the four-vector's square, a train of a half-speed kind, admitted or not, a
component off its train's rows).

Usage: `python tools/tensor24_files.py [universe piece setting]` prints every departure (the examples by default)
and exits 1 if there is one; files that are not three are argparse's usage error. The fine tooth within its teeth is
the run's promise, read before every round where the teeth are.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.joinpath("src")))

from tensor24.main import made  # noqa: E402
from tensor24.runner.files import NAMES, departures, held_departures, sites_of, vocabulary  # noqa: E402
from tensor24.runner.load import load, star  # noqa: E402

EXAMPLES = Path(__file__).resolve().parents[1].joinpath("examples", "tensor24")


def loaded(universe: Path, piece: Path, setting: Path) -> list[str]:
    """The load's departures of three files the checker holds, on the kinds of the piece's board."""
    u, p, s = (json.loads(path.read_text(encoding="utf-8")) for path in (universe, piece, setting))
    kinds, tables, square, lifted = made(star(len(p["shape"])))
    held = held_departures(u, s, vocabulary(kinds, square, lifted))
    return held or load(u, s, sites_of(p["shape"]), kinds, tables, square, lifted)[1]


def main(argv: list[str]) -> int:
    """Check and load the files, print each departure or that they hold, and return 1 on a departure."""
    parser = argparse.ArgumentParser(description="Tensor24's three files checked and loaded.")
    for name in NAMES:
        parser.add_argument(
            name, nargs="?", type=Path, help=f"the {name} file, or none of the three for the examples"
        )
    held = vars(parser.parse_args(argv))
    given = [held[name] for name in NAMES]
    if any(given) and not all(given):
        parser.error("the three files, or none for the examples")
    files = [path or EXAMPLES.joinpath(f"{name}.json") for name, path in zip(NAMES, given, strict=True)]
    found = departures(*files)
    found = found or loaded(*files)
    print(
        "\n".join(found)
        if found
        else "the three files hold and load: whole numbers, the integers at least 1, references whole, every"
        " kind, part and component the 24's (the fine tooth's promise is the run's, read before every round)"
    )
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
