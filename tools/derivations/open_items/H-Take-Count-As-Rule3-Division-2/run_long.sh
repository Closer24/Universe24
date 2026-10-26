#!/bin/bash
# ga2 450, the bodies 300 and the 48 on the chiral 3-cube to 60, each with the flag empty and set; the load rule polled before each; one record at a time
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/tools/derivations/open_items/H-Take-Count-As-Rule3-Division-2; P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
$P wait_for.py /dev/shm/tmp/tc2/run_60s.log done60
$P poll_load.py; date -u
PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_ga2_450.json 450 10 /dev/shm/tmp/tc2/ga2_off.json > out/ga2_450_off.txt 2>&1
$P poll_load.py; date -u
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_ga2_450.json 450 10 /dev/shm/tmp/tc2/ga2_on.json > out/ga2_450_on.txt 2>&1
$P poll_load.py; date -u
PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P run_48_tc2.py /dev/shm/tmp/tc2/src_tc2 worlds/world_chiral_3_30.json 60 out/c48_chiral3_60_off.json > out/c48_chiral3_60_off.txt 2>&1
$P poll_load.py; date -u
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P run_48_tc2.py /dev/shm/tmp/tc2/src_tc2 worlds/world_chiral_3_30.json 60 out/c48_chiral3_60_on.json > out/c48_chiral3_60_on.txt 2>&1
$P poll_load.py; date -u
PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_bodies.json 300 10 /dev/shm/tmp/tc2/bodies_off.json > out/bodies_300_off.txt 2>&1
$P poll_load.py; date -u
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_bodies.json 300 10 /dev/shm/tmp/tc2/bodies_on.json > out/bodies_300_on.txt 2>&1
date -u; echo donelong
