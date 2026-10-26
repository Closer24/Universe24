#!/bin/bash
# tc1's chain under the load rule (poll until the 1-minute load is below 3 before each run above a minute; one record at a time; nice 19)
F=$(cd "$(dirname "$0")" && pwd); W=$F/../../../..; P=/home/user/Universe24/venv314/bin/python; C=/dev/shm/tmp/tc1/src_tc1; O=/dev/shm/tmp/tc1/out
export TMPDIR=/dev/shm/tmp; cd $F
run() { name=$1; shift; $P poll_load.py >> out/chain.log; date -u >> out/chain.log; echo "$name" >> out/chain.log; nice -n 19 "$@" > out/$name.txt 2> out/$name.err; echo "$name done $(date -u)" >> out/chain.log; }
run ga2_head $P ga2_course.py $W/src $W/tests/worlds/world_ga2.json 450 10 $O/ga2_head.json 2,218,442
TC1_DIVISION_COUNT=1 TC1_DIVISION_GUARD=1 run ga2_guard $P ga2_course.py $C $W/tests/worlds/world_ga2.json 450 10 $O/ga2_guard.json 2,218,442
TC1_DIVISION_COUNT=1 run ga2_pure $P ga2_course.py $C $W/tests/worlds/world_ga2.json 450 10 $O/ga2_pure.json 2,218,442
run c48_off $P run_48.py $C world_chiral_3_30.json 60 $O/c48_off.json
TC1_DIVISION_COUNT=1 TC1_DIVISION_GUARD=1 run c48_guard $P run_48.py $C world_chiral_3_30.json 60 $O/c48_guard.json
TC1_DIVISION_COUNT=1 run c48_pure $P run_48.py $C world_chiral_3_30.json 60 $O/c48_pure.json
run rec_hole_head $P run_record.py $W/src $W/tests/worlds/world_hole.json 60 10 $O/rec_hole_head.json
TC1_DIVISION_COUNT=1 run rec_nature_pure $P run_record.py $C $W/tests/worlds/world_nature.json 60 10 $O/rec_nature_pure.json
run moment_hole_head $P kl2_moment.py $O/rec_hole_head.json
run moment_nature_pure $P kl2_moment.py $O/rec_nature_pure.json
run bodies_head $P run_hash.py $W/src world_bodies.json 300 back 10
TC1_DIVISION_COUNT=1 TC1_DIVISION_GUARD=1 run bodies_guard $P run_hash.py $C world_bodies.json 300 back 10
TC1_DIVISION_COUNT=1 run bodies_pure $P run_hash.py $C world_bodies.json 300 back 10
PYTHONPATH=$W/src run takes_ga2 $P tc1_takes.py world_ga2.json 450 $O/takes_ga2.json
echo chain done >> out/chain.log
