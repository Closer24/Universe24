"""The lay lock read in two units (hand V2, 2026-10-25; the brief's item (d)): the bare torus of the tests' small universe (den 1,021) run with every act and the close for N intervals from the hole seed; after every interval each born point family's share per Node (the engine's `share_of`, the conserved form's Node term at the frame's weight 1 / p_a^2) is read against its unit W_rec as the lay's refusal reads it, and beside it the same share at the vacuum's weight, share x p_a^2 div Gamma^2 (one division per Node), against the same unit; the Nodes at or above one unit are counted under each reading, with the close's refusals by cause from the output lines, the births, the light's quanta under both readings and the content; integers throughout. Command: PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Pump-And-Redshift-2/lay_lock.py [cube] [intervals]"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np

from common import GAMMA, dump, lattice_of, quotient

from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume


def corrected(shares: np.ndarray, content: np.ndarray) -> np.ndarray:
    """A share at the vacuum's weight: share x p_a^2 div Gamma^2 at every Node, p_a the Link's pace at the content read there."""
    pace = np.asarray(paces.link_pace_of(GAMMA, content), dtype=object)
    found = np.asarray(shares, dtype=object) * pace * pace
    return np.asarray(division_forward(found, GAMMA * GAMMA, 0)[0], dtype=object)


def total_of(array: np.ndarray) -> int:
    return int(sum(int(s) for s in np.asarray(array, dtype=object).ravel()))


def main() -> None:
    cube = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    intervals = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    lines: list[dict] = []
    board = lattice_of(Path(tempfile.mkdtemp(prefix="v2_lock_")), (cube,) * 3, lines)
    light, held = board.world.seed, board.held[0]
    nodes = int(np.prod(board.shape))
    rows = []
    seen = 0
    for _ in range(intervals):
        board.step()
        new = lines[seen:]
        seen = len(lines)
        births = sum(1 for li in new if li["event"] == "birth")
        refusals: dict[str, int] = {}
        for li in new:
            if li["event"] == "refused":
                cause = str(li.get("cause"))
                refusals[cause] = refusals.get(cause, 0) + 1
        time = board.states[held].lines[0]
        levels = np.asarray(volume.level_of(GAMMA, time.now), dtype=object)
        row = {
            "interval": board.interval,
            "births": births,
            "refusals": refusals,
            "content_sum_over_nodes": quotient(total_of(levels), nodes),
            "content_max": int(levels.max()),
            "families": {},
        }
        shares, _ = board.share_of(light)
        content = board.read(light)[0]
        fixed = corrected(shares, content)
        unit = int(board.credit.units[light])
        plain = np.asarray(shares, dtype=object)
        row["light"] = {
            "unit": unit,
            "quanta_engine_total": quotient(total_of(plain), unit),
            "quanta_corrected_total": quotient(total_of(fixed), unit),
            "nodes_at_two_engine": int((plain >= 2 * unit).sum()),
            "nodes_at_two_corrected": int((fixed >= 2 * unit).sum()),
        }
        if any(li["event"] == "birth" for li in lines):
            for index in board.turning:
                shares, _ = board.share_of(index)
                plain = np.asarray(shares, dtype=object)
                if not plain.any():
                    continue
                content = board.read(index)[0]
                fixed = corrected(shares, content)
                unit = int(board.credit.units[index])
                row["families"][board.families[index].name] = {
                    "unit": unit,
                    "share_engine_total_over_unit": quotient(total_of(plain), unit),
                    "share_corrected_total_over_unit": quotient(total_of(fixed), unit),
                    "nodes_above_unit_engine": int((plain >= unit).sum()),
                    "nodes_above_unit_corrected": int((fixed >= unit).sum()),
                    "nodes_with_level": int((plain != 0).sum()),
                    "max_engine_over_unit": quotient(int(plain.max()), unit),
                    "max_corrected_over_unit": quotient(int(fixed.max()), unit),
                }
        rows.append(row)
        if births or refusals or board.interval % 10 == 0:
            summary = " ".join(
                f"{name}: eng {f['nodes_above_unit_engine']}/{nodes} cor {f['nodes_above_unit_corrected']}/{nodes} "
                f"(max {f['max_engine_over_unit']['quotient']}+{f['max_engine_over_unit']['remainder']}/{f['unit']} "
                f"/ {f['max_corrected_over_unit']['quotient']}+{f['max_corrected_over_unit']['remainder']}/{f['unit']})"
                for name, f in row["families"].items()
            )
            print(
                f"interval {board.interval:4d} births {births:3d} refusals {refusals} content mean "
                f"{row['content_sum_over_nodes']['quotient']} light quanta eng {row['light']['quanta_engine_total']['quotient']} "
                f"cor {row['light']['quanta_corrected_total']['quotient']} nodes at two: eng {row['light']['nodes_at_two_engine']} "
                f"cor {row['light']['nodes_at_two_corrected']} | {summary}"
            )
    print(dump(f"lay_lock_{cube}.json", {"cube": cube, "rows": rows}))


if __name__ == "__main__":
    main()
