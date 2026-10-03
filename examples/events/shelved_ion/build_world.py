"""The shelved ion's builder (examples/events/shelved_ion; ENGINE.md section 9): the blind `expectation.json` written from the design's `blind` byte for byte, the design holding every number of the two worlds and the blind written before any run (the owner's word of 2026-10-02, the characterising experiment of the click's round); the worlds themselves are declared by hand in the folder, the ion laid in its parts by the engine's own start and the drives by the generator (`tools/pixel_mode.py`), so the builder lays nothing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    blind = json.dumps(design["blind"], indent=1, ensure_ascii=False) + "\n"
    (args.folder / "expectation.json").write_text(blind, encoding="utf-8")


if __name__ == "__main__":
    main()
