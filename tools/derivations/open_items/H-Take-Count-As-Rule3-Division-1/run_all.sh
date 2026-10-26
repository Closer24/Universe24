#!/bin/bash
# tc1: the flag empty bit for bit on the hole 60 and the chiral 60 (head, off), then on (the item's measure first), then the takes reader on the head
F=$(cd "$(dirname "$0")" && pwd); W=$F/../../../..; P=/home/user/Universe24/venv314/bin/python; C=/dev/shm/tmp/tc1/src_tc1
export TMPDIR=/dev/shm/tmp; cd $F
PYTHONPATH=$W/src nice -n 19 $P run_hash.py $W/src world_hole.json 60 back 10 > out/hash_hole_head.txt
PYTHONPATH=$C nice -n 19 $P run_hash.py $C world_hole.json 60 back 10 > out/hash_hole_off.txt
TC1_DIVISION_COUNT=1 PYTHONPATH=$C nice -n 19 $P run_hash.py $C world_hole.json 60 back 10 > out/hash_hole_on.txt
PYTHONPATH=$W/src nice -n 19 $P run_hash.py $W/src world_chiral.json 60 back 10 > out/hash_chiral_head.txt
PYTHONPATH=$C nice -n 19 $P run_hash.py $C world_chiral.json 60 back 10 > out/hash_chiral_off.txt
TC1_DIVISION_COUNT=1 PYTHONPATH=$C nice -n 19 $P run_hash.py $C world_chiral.json 60 back 10 > out/hash_chiral_on.txt
PYTHONPATH=$W/src nice -n 19 $P tc1_takes.py world_hole.json 60 out/takes_hole_60.json > out/takes_hole_60.txt
PYTHONPATH=$W/src nice -n 19 $P tc1_takes.py world_chiral.json 60 out/takes_chiral_60.json > out/takes_chiral_60.txt
date -u; echo six done
