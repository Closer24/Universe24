"""The one command: a list of world files in, one output file per world out, each world in its own process. A world is loaded (LAWFUL, or REFUSED with the loader's reason, the guard's among them), run on the GameBoard for its declared intervals, headless (a refusal inside the run is written too, REFUSED with its reason and interval; a run whose front reaches a receding face's largest size ends there, LAWFUL, the end named under `ended` with the intervals run), and `<name>.output.json` is written into `--out`: the world's name, the verdict, the intervals run, the end if the run ended, the output lines `click` (the detectors' clicks, the measurements: each the region's name, the family and the Ports crossed, never a Node) and the books (a GameBoard diagnostic, the least Link pace of the final state among them). The output carries no time.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/run_inputs.py --out runs/first --jobs 4 <world>.json ...
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from event_universe.game_board import GameBoard
from event_universe.world_files import load_world

LINES = ("click", "seen")  # the lines written: the detectors' clicks and what they saw


def run_input(path: str, out_dir: str) -> dict[str, object]:
    """One world in this process: the verdict at load, the run, the output file; its summary returned."""
    source, lines = Path(path), []
    output: dict[str, object] = {"input": source.name, "verdict": "LAWFUL", "ticks": 0}
    try:
        board = GameBoard(load_world(source), lambda line: lines.append(line))
        for _ in range(board.world.ticks):
            board.step()
            if board.ended is not None:
                break
        output.update(ticks=board.tick, ended=board.ended, books=board.books())
    except (ValueError, RuntimeError) as refusal:
        output.update(verdict="REFUSED", reason=str(refusal))
    output["lines"] = [line for line in lines if line["event"] in LINES]
    target = Path(out_dir) / f"{source.stem}.output.json"
    target.write_text(json.dumps(output, indent=1) + "\n", encoding="utf-8")
    return {"input": source.name, "verdict": output["verdict"], "ticks": output["ticks"]}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs", nargs="+", help="the world files, each with its mode file beside it")
    parser.add_argument("--out", required=True, type=Path, help="the folder of the output files")
    parser.add_argument("--jobs", type=int, default=None, help="the processes at once (the cores)")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        for summary in pool.map(run_input, args.inputs, [str(args.out)] * len(args.inputs)):
            print(json.dumps(summary))


if __name__ == "__main__":
    main()
