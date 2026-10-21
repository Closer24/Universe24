"""A, the blind by the law's real line (README.md, section A): the shipped two slits' world from the mode
file's lay stepped in real arithmetic (fields.py), the screen's twelve regions' inflows over the window
[45, 130] and the return region's (x = 0 and 1 over every row, the front its +x Ports) over [1, 130], over
the lay's share: the shares of one quantum, the blind row of the one-quantum world with every exit
declared; and the shipped geometry's share through the screen per laid quantum.

    PYTHONPATH=src python papers/one_rule/variants/scripts/a_real_line.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fields  # noqa: E402
import two_slits_real_line as tsl  # noqa: E402

OUT = HERE.parent / "out"


def main() -> None:
    world, expected, board, line, wall = fields.loaded()
    regions = dict(board.regions)
    regions["return"] = tuple((x, y) for x in (0, 1) for y in range(board.height))
    board = tsl.Board(
        board.length, board.height, board.beyond, regions, board.screen, board.packet, board.intervals
    )
    now0, before0 = tsl.mode_lay(world, board)
    both = fields.stepped(board, line, now0, before0, board.intervals)
    laid = fields.share(line, world.node_clock, now0, before0).sum()  # the lay's share, current's units
    window = (int(expected["window"][0]), int(expected["window"][1]))
    screen = [fields.windowed(fields.region_inflow(board, line, both, n), window) for n in board.screen]
    profile = fields.region_inflow(board, line, both, "return")
    whole = (1, board.intervals)
    ret = fields.windowed(profile, whole)
    floored = float(sum(max(profile[t - 1], 0.0) for t in range(whole[0], whole[1] + 1)))
    total = sum(screen) + ret
    left = fields.share(line, world.node_clock, both.now[-1], both.before[-1]).sum()
    first_above = next(t + 1 for t in range(len(profile)) if profile[t] > 0.01 * profile.max())
    report = {
        "laid_share_over_W_c": laid / wall,
        "screen_regions_over_W_c_[45,130]": [round(v / wall, 3) for v in screen],
        "screen_total_over_W_c": round(sum(screen) / wall, 3),
        "return_over_W_c_[1,130]_net": round(ret / wall, 3),
        "return_over_W_c_[1,130]_floored_per_interval": round(floored / wall, 3),
        "left_on_the_board_at_130_over_W_c": round(left / wall, 3),
        "screen_share_per_laid_quantum": round(sum(screen) / laid, 5),
        "return_share_per_laid_quantum": round(ret / laid, 5),
        "sum_credited_per_laid_quantum": round(total / laid, 5),
        "blind_shares_over_every_exit": {
            **{n: round(v / total, 5) for n, v in zip(board.screen, screen, strict=True)},
            "return": round(ret / total, 5),
        },
        "blind_screen_shares_within_the_screen": [round(v / sum(screen), 5) for v in screen],
        "return_arrival_first_interval_above_1pc_of_peak": int(first_above),
        "return_peak_interval": int(profile.argmax() + 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "a_real_line.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
