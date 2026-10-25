"""Hand D3: the two views of the decoder on one clicks log (BRIEF_d (d)). Integers only.

The whole view: every credit line, grouped by place (`support`) and body (`identity`). The one-place view: one body's credits alone, in the order of its own closes (`windows`), read by its own clock (`proper`): its proper spacing between successive clicks, the credit's `beat` and `point`, and nothing of the board's interval. Beside it, for the comparison, what the whole view adds from the board's labels: the same spacing in board intervals, and the pairing of two Nodes' clocks at one board interval (the board's simultaneity, the method of gate 10), which no one-place reading has. The light arriving at a Node from another body (W-S1) is counted: the credits of light's identity at a Node that is not a birth's Node at that interval.

Usage: PYTHONPATH=<worktree>/src python tools/derivations/d3/d3_one_place.py [--log tools/derivations/d3/out/clicks.jsonl] [--out tools/derivations/d3/out]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve()


def quotient(a: int, b: int) -> list[int]:
    """a over b as the integer quotient with its remainder, [q, r], a = q b + r, 0 <= r < b."""
    return [a // b, a % b] if b else [None, a]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--log", type=Path, default=HERE.parent / "out" / "clicks.jsonl")
    parser.add_argument("--out", type=Path, default=HERE.parent / "out")
    args = parser.parse_args()
    lines = [json.loads(x) for x in args.log.read_text(encoding="utf-8").splitlines() if x.strip()]
    credits = [x for x in lines if x.get("event") == "credit"]
    births = [x for x in lines if x.get("event") == "birth"]
    light = min((x["identity"][0] for x in credits), default=None)  # light's row index is the smallest family index among the credits' identities on the bare torus (the seed's row); checked below against the births
    born_at = {(x["interval"], tuple(node)) for x in births for node in x["nodes"]}
    light_ids = {tuple(x["identity"]) for x in credits if (x["interval"], tuple(x["support"])) in born_at}
    assert all(i[0] == light for i in light_ids), "light's identity is the births' credits'"
    tracks: dict[tuple, list[dict]] = {}
    for x in credits:
        tracks.setdefault((tuple(x["support"]), tuple(x["identity"])), []).append(x)
    one_place = []
    for (support, identity), found in sorted(tracks.items()):
        if identity[0] == light or len(found) < 2:
            continue
        found.sort(key=lambda x: x["windows"])  # the body's own order: its Node's count of closes, no board interval
        proper = [x["proper"] for x in found]
        windows = [x["windows"] for x in found]
        intervals = [x["interval"] for x in found]  # the board's, for the comparison alone
        d_proper = [b - a for a, b in zip(proper, proper[1:], strict=False)]
        d_interval = [b - a for a, b in zip(intervals, intervals[1:], strict=False)]
        pace = [quotient(1000 * p, i) for p, i in zip(d_proper, d_interval, strict=True)]  # proper per interval in thousandths, the board's view
        one_place.append({
            "place": list(support), "body": list(identity), "clicks": len(found),
            "own_clock_proper_at_each_click": proper, "own_closes_windows": windows,
            "proper_spacing": d_proper, "proper_spacing_first_last": [d_proper[0], d_proper[-1]],
            "beat_on_the_credit": [x["beat"] for x in found], "point_on_the_credit": [x["point"] for x in found[:2]],
            "board_view_interval_spacing": d_interval, "board_view_pace_thousandths": pace,
        })
    # the board's simultaneity: two Nodes' proper at shared board intervals (gate 10's method), which the one-place view lacks
    clocks: dict[tuple, dict[int, int]] = {}
    for x in credits:
        clocks.setdefault(tuple(x["support"]), {})[x["interval"]] = x["proper"]
    pairs, equal, unequal = 0, 0, 0
    for a in sorted(clocks):
        for b in sorted(clocks):
            if b <= a:
                continue
            shared = sorted(set(clocks[a]) & set(clocks[b]))
            if len(shared) < 2:
                continue
            pairs += 1
            da = clocks[a][shared[-1]] - clocks[a][shared[0]]
            db = clocks[b][shared[-1]] - clocks[b][shared[0]]
            equal += da == db
            unequal += da != db
    light_from_another_body = sum(1 for x in credits if x["identity"][0] == light and (x["interval"], tuple(x["support"])) not in born_at)
    found = {
        "credits": len(credits), "places_credited": len(clocks), "tracks": len(tracks), "body_tracks_with_two_or_more_clicks": len(one_place),
        "one_place_view": one_place,
        "whole_view_board_simultaneity": {"node_pairs_with_two_shared_intervals": pairs, "proper_increments_equal": equal, "proper_increments_unequal": unequal},
        "light_credits_from_another_body_at_a_node": light_from_another_body,
        "what_the_one_place_view_computes": "its own clock (proper), its own order (windows), its proper spacing per click, the point and the beat on its credits",
        "what_it_cannot_compute": "another clock's rate (the dilation) and simultaneity with another Node; on this engine 0 light credits arrive from another body, so W-S1 is the missing channel",
    }
    (args.out / "one_place.json").write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
