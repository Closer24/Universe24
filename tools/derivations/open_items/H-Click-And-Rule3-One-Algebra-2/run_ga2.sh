#!/bin/bash
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/ca2
F=$W/tools/derivations/open_items/H-Click-And-Rule3-One-Algebra-2
P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp PYTHONPATH=$W/src; cd $F
$P poll_load.py; date -u
(time timeout 900 $P q8_takes.py world_ga2.json 450 out/q8_ga2_450.txt) > /dev/shm/tmp/ca2/ga2.log 2>&1
$P poll_load.py; date -u
(time CA2_EVEN_LAY=1 PYTHONPATH=/dev/shm/tmp/ca2/src_ca2 timeout 900 $P run_flag_3cube.py /dev/shm/tmp/ca2/src_ca2 world_ga2.json 450) > out/flag_ga2_on.txt 2>&1
date -u; echo ga2 done
