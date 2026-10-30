# Rerun of the draft's nine probes (2026-10-30, ~16:35 UTC)

Command: scratchpad/t24b/.venv/bin/python -I <probe>.py, from scratchpad/quaternion, outputs in qa_phys/rerun/.

| probe | exit | against the stored .txt |
| --- | --- | --- |
| probe.py | 0 | identical |
| probe_units.py | 0 | identical |
| probe_carry.py | 0 | identical (the stored .err says "exit 0") |
| probe_carry_big.py | 0 | identical |
| probe_time.py | 0 | identical |
| probe_square.py | 0 | identical |
| probe_ring.py | 0 | identical |
| probe_books.py | 0 | identical |
| probe_double.py | 1 | the first 6 lines identical, then TypeError: turned_edge() missing 'wd' |

probe_double.py imports scratchpad/edge/edge_lib.py (another agent's live harness), whose
turned_edge() grew a fourth positional argument `wd` at 16:33:19 UTC, four minutes after the
draft's output was written (16:29:12). The draft's main probe for the double Node-clock no
longer runs; its edge-act results (q+ = q j on the edge act, the phase 12 of 12, the swap,
12 unticks, the cube of side 3, the 24-gear train section) cannot be rerun from the draft's
folder as it stands. The act-as-built lines of the same probe are the ones that matter for
"the act as built", and those come after the failure point too.

Fix: copy the edge_lib the probe was run against into scratchpad/quaternion (pinned), or
measure the double Node-clock on step.tick alone (the engine's act is on main and does not
move). My own probes below use step.tick only.
