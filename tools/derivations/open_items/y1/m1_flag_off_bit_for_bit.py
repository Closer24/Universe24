"""m1 (hand y1): the branch's path with U24_METRIC unset against the pristine src of 78d192531 (git archive HEAD src into /dev/shm/tmp/pristine), 14 intervals of the bare 3-cube hole seed through the births at 4, the snapshot's digest at every interval and every output line compared. Run twice, once with PYTHONPATH=<worktree>/src and once with PYTHONPATH=/dev/shm/tmp/pristine/src, each writing its digests; the comparison is the third call with --compare."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
INTERVALS = 14


def run(out: Path) -> None:
    import y1lib

    lines: list = []
    board = y1lib.board_of(Path("/dev/shm/tmp") / out.stem, lines)
    digests = [y1lib.digest(y1lib.snapshot(board))]
    for _ in range(INTERVALS):
        board.step()
        digests.append(y1lib.digest(y1lib.snapshot(board)))
    out.write_text(json.dumps({"digests": digests, "lines": lines}, sort_keys=True, default=str))
    print(out, "written", len(digests), "digests,", len(lines), "lines")


if __name__ == "__main__":
    if sys.argv[1] == "--compare":
        a, b = (json.loads(Path(p).read_text()) for p in sys.argv[2:4])
        same_digests = sum(x == y for x, y in zip(a["digests"], b["digests"], strict=True))
        same_lines = a["lines"] == b["lines"]
        verdict = {
            "intervals": INTERVALS,
            "digests_equal": same_digests,
            "digests_total": len(a["digests"]),
            "output_lines_equal": int(same_lines),
            "output_lines": len(a["lines"]),
            "BIT_FOR_BIT": int(same_digests == len(a["digests"]) and same_lines),
        }
        print(json.dumps(verdict))
        (HERE / "m1_flag_off_bit_for_bit.json").write_text(json.dumps(verdict, indent=1))
    else:
        run(Path(sys.argv[1]))
