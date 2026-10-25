"""Hand r4, round 3, the open board: the standing-wave seed with every act but the close, 80 intervals through a top and 80
back (ride_round3.run with close False): MATCH, the counts at the seed and at the top (the engine's, the vacuum's weight,
the mode's unit), the beat per proper interval over the two halves, the currents' sum; and the 48 per interval over the
first 10 intervals of the closed standing run (where the births' draw breaks them). Outputs ride_round3_open_<flag>.json."""

import json
import os
import sys
from pathlib import Path

FLAG = sys.argv[1] if len(sys.argv) > 1 else "2"
os.environ["U24_RIDES"] = FLAG
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ride_round3 as r3  # noqa: E402  (sets the paths and the flag)

from tests.laws_universe import node_arrays  # noqa: E402

if __name__ == "__main__":
    base = Path(os.environ.get("TMPDIR", "/dev/shm/tmp")) / f"r4_round3_open_{r3.TAG}"
    found = {"flag": FLAG, "sign_rides": os.environ.get("U24_SIGN_RIDES") == "1"}
    found["standing_open"] = r3.run(base / "open", r3.standing_seed, False, 80)
    board, lines = r3.board_of(base / "per_interval", 20, r3.standing_seed)
    per_interval = []
    for t in range(1, 11):
        board.step()
        kept_levels, kept_all = r3.forty_eight(node_arrays(board))
        births = sum(1 for line in lines if "senses" in line and line.get("interval") == t)
        per_interval.append({"interval": t, "elements_keeping_levels": kept_levels, "elements_keeping_all": kept_all, "turned": int(board.turned.sum()), "births": births})
    found["standing_closed_48_per_interval"] = per_interval
    out = HERE / f"ride_round3_open_{r3.TAG}.json"
    out.write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
    print(json.dumps(found, indent=1, default=str))
