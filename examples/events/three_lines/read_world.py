"""The fifth feasibility world's reader (the Boss's list, #1572 comment 5963599079 (A) 5; the advisor's blind, 5963681796): a world of the dimension-3 family is loaded as the runner loads it and stepped by the engine's own step over its `ticks` with an observer, and the blind's rows are read from the lines and the GameBoard: the `credit` lines (how many, the interval, the count moved and left, the parts kept), the `parts` lines of the counter over the first window line by line, the signed level sums themselves (a : b : c with their signs, the mathematician's 204) and the sum of the squares of each line's two sums over the window over the three lines' total, and the form per line, the share of each line summed over the board at the start and at the first window's end over the record's (the hard click's fractions, quadratic, a^2 : b^2 : c^2), as exact fractions beside the blind's, the record's three lines' levels and remainders at the click's Node after the two intervals that follow the click (a GameBoard reading labelled so), the count in the books, and every line after the click; the tool holds no number of the law and compares nothing.

PYTHONPATH=src python examples/events/three_lines/read_world.py --expectation examples/events/three_lines/expectation.json examples/events/three_lines/triple_weighted.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe import share
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world


def line_shares(board: GameBoard, index: int) -> dict[str, Any]:
    """The form per line, a GameBoard reading: each line's share summed over the board at the paces of the record's read, in the current's units, and its fraction of the record's, the hard click's reading of a line's share of the form (quadratic)."""
    family, content_factors = board.families[index], board.read(index)
    gamma, unit = board.world.node_clock, board.unit
    own = [
        int(share.share(family.pair, line, board.wrap, gamma, *content_factors, unit).sum(dtype=object))
        for line in board.states[index].lines
    ]
    total = sum(own)
    return {
        "label": "GAMEBOARD",
        "interval": board.tick,
        "shares": own,
        "fractions": [[s, total] for s in own] if total else None,
        "decimal": [float(Fraction(s, total)) for s in own] if total else None,
    }


def reading(path: Path, window: int) -> dict[str, Any]:
    """One world's reading: the credit lines, the fractions over the first window, the levels and remainders at the click's Node two intervals after the click, the books' count and the lines after the click."""
    board = GameBoard(load_world(path), (lines := []).append)
    family = next(f for f in board.families if f.quanta)
    index = board.families.index(family)
    at_click: dict[str, Any] = {}
    shares = {"at_the_start": line_shares(board, index)}
    while board.ended is None and board.tick < board.world.ticks:
        board.step()
        if board.tick == window:
            shares["at_the_windows_end"] = line_shares(board, index)
        credits = [line for line in lines if line["event"] == "credit"]
        if credits and board.tick == int(credits[0]["tick"]) + 2:  # the face's two intervals done
            node = tuple(int(a) + b for a, b in zip(credits[0]["node"]["at"], board.offset, strict=True))
            state = board.states[index]
            at_click = {
                "label": "GAMEBOARD",
                "node": list(credits[0]["node"]["at"]),
                "interval": board.tick,
                "levels": [
                    [int(r.now[node]), int(r.before[node]), int(r.remainder[node])] for r in state.lines
                ],
            }
    credits = [line for line in lines if line["event"] == "credit"]
    sums = [line for line in lines if line["event"] == "parts" and line["tick"] <= window]
    squares, signed = [0] * family.lines, [0] * family.lines
    for line in sums:
        for k, (now, before) in enumerate(line["levels"]):
            squares[k] += now * now + before * before
            signed[k] += now + before
    total = sum(squares)
    fractions = [[s, total] for s in squares] if total else None
    first = int(credits[0]["tick"]) if credits else None
    after = [
        line for line in lines if first is not None and line["tick"] > first and line["event"] != "field"
    ]
    return {
        "world": path.name,
        "ticks": board.tick,
        "ended": board.ended,
        "credits": [{k: v for k, v in c.items() if k != "node"} for c in credits],
        "clicks": len(credits),
        "parts_lines_in_window": len(sums),
        "parts_signed_sums_over_the_window": signed,
        "parts_squared_sums_fractions": fractions,
        "parts_squared_sums_decimal": [float(Fraction(s, total)) for s in squares] if total else None,
        "form_per_line": shares,
        "at_the_click_node_after_the_face": at_click,
        "count_in_the_books": board.credit.counts[index],
        "credits_after_the_first": [line for line in after if line["event"] == "credit"],
        "lines_after_the_first_click": sorted({str(line["event"]) for line in after}),
        "books": board.books(),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="+", help="the world files, with their mode files beside them"
    )
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    blind = json.loads(args.expectation.read_text(encoding="utf-8"))
    found = {"label": "GAMEBOARD and DETECTOR", "blind": blind["worlds"], "readings": {}}
    for path in args.worlds:
        found["readings"][path.stem] = reading(path, int(blind["window"][1]))
    print(json.dumps(found, indent=1, default=str))


if __name__ == "__main__":
    main()
