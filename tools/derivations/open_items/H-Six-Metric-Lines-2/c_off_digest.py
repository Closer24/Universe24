"""The flag off is the branch bit for bit: the digest of every array of every state of the hole seed on the bare 3-cube at den 1,021 after 8 intervals (through the first birth and the turns), with the output lines' count, run once with this worktree's src (U24_METRIC unset) and once with a pristine checkout of 78d192531 (PYTHONPATH pointing at it); the two digests compared by the caller. Also the loader's rows under the flag off (the volume row's 4 lines, 4 walls) and the readings' count (6).

Run: PYTHONPATH=<src> TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Six-Metric-Lines-2/c_off_digest.py <label>
"""

from __future__ import annotations

import json
import sys

from y2lib import bare_board, digest, rows_table

from event_universe import board_readings


def main() -> None:
    label = sys.argv[1] if len(sys.argv) > 1 else "worktree"
    lines_out: list = []
    board = bare_board(intervals=8, lines=lines_out)
    rows = rows_table(board)
    stresses = board_readings.stresses(board)
    readings_per_source = sorted({len(v) for v in stresses.values()})
    for _ in range(8):
        board.step()
    found = {
        "label": label,
        "src": __import__("event_universe").__file__,
        "digest_after_8": digest(board),
        "output_lines": len(lines_out),
        "volume_row_lines": rows[0]["width"],
        "volume_row_walls": rows[0]["walls"],
        "readings_per_source": readings_per_source,
    }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
