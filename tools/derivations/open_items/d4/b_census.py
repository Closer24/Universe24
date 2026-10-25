"""(b) Only a bound body clicks, on the hole seed run with the writer on for N intervals: every credit line classed as the light's at a birth (its (interval, support) a birth line's (interval, node)), a body's (a charged plane family's record) or other; refused lines counted by cause; every output line kept beside as hole_N.lines.jsonl for (d) and (e). Beside it the clicks log tools/eras.py writes for the same world (its `keep` filter) compared event by event with the board's own output.
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/d4/b_census.py 120"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from d4lib import HERE, ROOT, dump, hole_board

sys.path.insert(0, str(ROOT / "tests"))
from laws import load_file  # noqa: E402

from event_universe import bound_body, share  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
tmp = Path("/dev/shm/tmp/d4_b")
board, lines = hole_board(tmp / "run", N, True)
for _ in range(N):
    board.step()
light = board.world.seed
with (HERE / f"hole_{N}.lines.jsonl").open("w", encoding="utf-8") as out:
    for line in lines:
        out.write(json.dumps(line) + "\n")
births = {(l["interval"], tuple(n)) for l in lines if l["event"] == "birth" for n in l["nodes"]}
credits = [l for l in lines if l["event"] == "credit"]
light_at_birth = light_not_at_birth = body = other = 0
body_families = set()
for c in credits:
    k = c["identity"][0]
    fam = board.families[k]
    if k == light:
        if (c["interval"], tuple(c["support"])) in births:
            light_at_birth += 1
        else:
            light_not_at_birth += 1
    elif share.charged(fam) and fam.plane and all(key in c for key in ("taken", "walls", "excess", "step")):
        body += 1
        body_families.add(k)
    else:
        other += 1
refused = {}
for l in lines:
    if l["event"] == "refused":
        refused[l["cause"]] = refused.get(l["cause"], 0) + 1
events = {}
for l in lines:
    events[l["event"]] = events.get(l["event"], 0) + 1
body_records = bound_body.body_records(board)
# the eras tool's clicks log for the same world: which events its keep filter writes
eras = load_file("eras_tool_d4", ROOT / "tools" / "eras.py")
world = tmp / "run" / "bare.json"
from event_universe import world_files  # noqa: E402

world_files.REPOSITORY_ROOT = tmp / "run"
eras.run(world, tmp / "eras.jsonl", 1000, N, tmp / "eras.clicks.jsonl", None, False)
kept = [json.loads(x) for x in (tmp / "eras.clicks.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
kept_events = {}
for l in kept:
    kept_events[l["event"]] = kept_events.get(l["event"], 0) + 1
result = {
    "intervals": N,
    "families": [[k, f.name, int(f.pair[0]), int(f.pair[1]), bool(f.plane), bool(share.charged(f))] for k, f in enumerate(board.families)],
    "light_index": light,
    "output_events": events,
    "credits": len(credits),
    "light_credits_at_a_birth": light_at_birth,
    "light_credits_not_at_a_birth": light_not_at_birth,
    "body_credits_(charged_plane_record_with_the_take)": body,
    "body_families": sorted(body_families),
    "other_credits": other,
    "refused_by_cause": refused,
    "birth_lines": events.get("birth", 0),
    "body_records_on_the_board_at_the_end": [list(x) for x in body_records],
    "eras_py_clicks_log_events": kept_events,
    "eras_py_drops_events": sorted(set(events) - set(kept_events)),
    "eras_py_dropped_lines": sum(v for k, v in events.items() if k not in kept_events),
}
dump(HERE / f"b_census_{N}.json", result)
print(result)
