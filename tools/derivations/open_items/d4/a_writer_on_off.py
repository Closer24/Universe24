"""(a) The output writer on and off: the hole seed run twice for N intervals, once with every line kept and once with no output; the whole state compared bit for bit (every line, remainder, write remainder, phase line, counter and the interval); then the writer-on board run back N intervals, each returned state compared with the kept forward state (MATCH count). Integer readings only.
Command: cd <worktree> && PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/d4/a_writer_on_off.py 40"""

from __future__ import annotations

import sys
from pathlib import Path

from d4lib import HERE, compare, dump, hole_board, state_of

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
tmp = Path("/dev/shm/tmp/d4_a")
on, lines = hole_board(tmp / "on", N, True)
off, _ = hole_board(tmp / "off", N, False)
kept = [state_of(on)]
per_interval = []
for _ in range(N):
    on.step()
    off.step()
    kept.append(state_of(on))
    n, eq, bad = compare(kept[-1], state_of(off))
    per_interval.append([int(on.interval), n, eq, len(bad)])
n_arrays, equal, unequal = compare(kept[-1], state_of(off))
events = {}
for line in lines:
    events[line["event"]] = events.get(line["event"], 0) + 1
COUNTERS = ("proper_count", "closes", "standing", "crossed", "beats")
def law_part(state):
    return {k: v for k, v in state.items() if not k.startswith(COUNTERS)}
def counter_part(state):
    return {k: v for k, v in state.items() if k.startswith(COUNTERS)}
back = back_counters = 0
back_rows = []
first_unequal_counters = None
for k in range(N):
    on.step_inverse()
    now = state_of(on)
    n, eq, bad = compare(law_part(now), law_part(kept[N - 1 - k]))
    nc, eqc, badc = compare(counter_part(now), counter_part(kept[N - 1 - k]))
    back += int(len(bad) == 0)
    back_counters += int(len(badc) == 0)
    if badc and first_unequal_counters is None:
        first_unequal_counters = badc
    back_rows.append([int(on.interval), n, eq, len(bad), nc, eqc, len(badc)])
result = {
    "intervals": N,
    "writer_on_lines": len(lines),
    "events": events,
    "final_state_arrays_compared": n_arrays,
    "final_state_arrays_equal": equal,
    "final_state_unequal_names": unequal,
    "per_interval_[interval, arrays, equal, unequal]": per_interval,
    "intervals_with_every_array_equal": sum(1 for r in per_interval if r[3] == 0),
    "run_back_law_state_MATCH_(lines, remainders, write remainders, phase lines)": back,
    "run_back_counters_MATCH_(proper_count, closes, standing, crossed, beats; the run back reads none of them)": back_counters,
    "counters_unequal_at_the_first_step_back": first_unequal_counters,
    "run_back_rows_[interval, law arrays, equal, unequal, counter arrays, equal, unequal]": back_rows,
    "verdict": "the board's course is the same bit for bit with the writer on and off" if equal == n_arrays and all(r[3] == 0 for r in per_interval) else "the writer changes the course",
}
dump(HERE / "a_writer_on_off.json", result)
print({k: v for k, v in result.items() if "rows" not in k and "per_interval" not in k})
