#!/bin/bash
# the return probes on ga2 450, the flag empty and set, after the long chain; under a minute each
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/tools/derivations/open_items/H-Take-Count-As-Rule3-Division-2; P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
$P wait_for.py /dev/shm/tmp/tc2/run_long.log donelong
date -u
PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_return.py /dev/shm/tmp/tc2/src_tc2 worlds/world_ga2_450.json 450 out/return_ga2_off.txt 2,218,219,221,225,442 > out/return_ga2_off_summary.txt 2>&1
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_return.py /dev/shm/tmp/tc2/src_tc2 worlds/world_ga2_450.json 450 out/return_ga2_on.txt 2,218,219,221,225,442 > out/return_ga2_on_summary.txt 2>&1
date -u; echo donereturn
