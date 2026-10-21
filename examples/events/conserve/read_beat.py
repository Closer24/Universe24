"""The emission's hazard of a bound body of Rule3 read on the box of 15 (2026-10-21; ALGEBRA.md, The click writes on the lattice (5): the rate the beat's current through the declared boundary over W_c plus the declared constant): the world examples/events/conserve/box_c15.json run for the intervals given, and per interval the beat's current booked by the engine (`NodeBooks.beat`, the electron's own record's conserved current through its standing region's front Ports, inward positive, in the unit G^2), its sum over each window of the lifetime, the outflow floored at 0 as the hazard reads it, over W_c G^2 of the light the body gives to, the share of a light quantum per window the beat term adds to the constant's 1 / lifetime; the books of the electron and of the photon beside them and every click line. A reading, no number of the law; written as JSON lines to the file named.

Run from the repository root with PYTHONPATH=src:

    python examples/events/conserve/read_beat.py --intervals 99 --out <file>.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe import reports
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

WORLD = Path("examples/events/conserve/box_c15.json")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--intervals", type=int, default=99)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(WORLD), lines.append)
    names = [family.name for family in board.families]
    electron, photon = names.index("electron"), names.index("photon")
    (books,) = board.credit.bodies
    rate = books.declared.rates[0]
    wall = count_wall(board.families[photon], board.world.quantum_action) * board.unit * board.unit
    own = board.credit.units[electron] * board.unit * board.unit
    with args.out.open("w", encoding="utf-8") as out:
        out.write(
            json.dumps(
                {
                    "world": WORLD.name,
                    "region": len(books.nodes),
                    "part": books.part,
                    "lifetime": rate.lifetime,
                    "window": books.declared.draw.window if books.declared.draw else None,
                    "W_c_light_G2": wall,
                    "W_rec_electron_G2": own,
                }
            )
            + "\n"
        )
        before, window_sum, closes = 0, 0, 0
        for _ in range(args.intervals):
            beat_before = books.beat
            board.step()
            came = books.beat - beat_before if books.beat else -beat_before  # the interval's booking
            if (
                books.beat == 0 and beat_before != 0
            ):  # the window closed this interval: the sum begun again
                came = 0
                closes += 1
            window_sum = books.beat
            clicks = [
                c for c in lines if c["event"] == reports.CREDIT and c["interval"] == board.interval
            ]
            out.write(
                json.dumps(
                    {
                        "interval": board.interval,
                        "beat_interval": came,
                        "beat_window": window_sum,
                        "elapsed": books.elapsed,
                        "windows": books.windows,
                        "parts": list(books.counts),
                        "electron": board.books()["electron"],
                        "photon": board.books()["photon"],
                        "clicks": [
                            {
                                k: v
                                for k, v in c.items()
                                if k
                                in ("node_detector", "before", "realised", "emitted", "count", "lost")
                            }
                            for c in clicks
                        ],
                    }
                )
                + "\n"
            )
            out.flush()
            before = books.beat
        out.write(json.dumps({"closes": closes, "final_beat": before}) + "\n")


if __name__ == "__main__":
    main()
