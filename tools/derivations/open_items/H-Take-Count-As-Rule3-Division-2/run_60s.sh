#!/bin/bash
# the hole 60 and the chiral 60: the head's src, the copy with the flag empty (done), the copy with the flag set; one record at a time
F=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/tools/derivations/open_items/H-Take-Count-As-Rule3-Division-2; P=/home/user/Universe24/venv314/bin/python; export TMPDIR=/dev/shm/tmp; cd $F
date -u
PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/src nice -n 19 $P tc2_record.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/src worlds/world_toy.json 60 10 /dev/shm/tmp/tc2/hole60_head.json > out/hole60_head.txt 2>&1
PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/src nice -n 19 $P tc2_record.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/tc2/src worlds/world_chiral.json 60 10 /dev/shm/tmp/tc2/chiral60_head.json > out/chiral60_head.txt 2>&1
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_toy.json 60 10 /dev/shm/tmp/tc2/hole60_on.json > out/hole60_on.txt 2>&1
TC2_CHORD_COUNT=1 PYTHONPATH=/dev/shm/tmp/tc2/src_tc2 nice -n 19 $P tc2_record.py /dev/shm/tmp/tc2/src_tc2 worlds/world_chiral.json 60 10 /dev/shm/tmp/tc2/chiral60_on.json > out/chiral60_on.txt 2>&1
date -u; echo done60
