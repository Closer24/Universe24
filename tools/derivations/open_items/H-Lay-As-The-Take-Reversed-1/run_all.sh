#!/bin/sh
# lt1: every measurement under nice 19, one run at a time, the load rule before any run above a minute (the kit's wait_load.py)
P=/home/user/Universe24/venv314/bin/python
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt1
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
F=$W/tools/derivations/open_items/H-Lay-As-The-Take-Reversed-1
S=/dev/shm/tmp/lt1/src_lt1
O=/dev/shm/tmp/lt1
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$S
cd $O
echo "start $(date -u +%T)"
LT1_RECOIL=1 nice -n 19 $P -m pytest -q -p no:cacheprovider $F/test_one_node_lt1.py > $F/out/one_node_test.txt 2>&1; echo "test exit $? $(date -u +%T)"
LT1_RECOIL=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_hole.json $O/lt1_hole60.json back 10 > $F/out/hole60_run.txt 2>&1; echo "hole exit $? $(date -u +%T)"
LT1_RECOIL=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json $O/lt1_chiral60.json back 10 > $F/out/chiral60_run.txt 2>&1; echo "chiral exit $? $(date -u +%T)"
nice -n 19 $P $F/lt1_moment.py $O/lt1_hole60.json > $F/out/moment_hole60.json 2>&1; echo "moment hole exit $?"
nice -n 19 $P $F/lt1_moment.py $O/lt1_chiral60.json > $F/out/moment_chiral60.json 2>&1; echo "moment chiral exit $?"
LT1_RECOIL=1 nice -n 19 $P $K/conservation_check.py $O/lt1_hole60.json out $F/out/cons_hole60.json > $F/out/cons_hole60.txt 2>&1; echo "cons hole exit $? $(date -u +%T)"
LT1_RECOIL=1 nice -n 19 $P $K/conservation_check.py $O/lt1_chiral60.json out $F/out/cons_chiral60.json > $F/out/cons_chiral60.txt 2>&1; echo "cons chiral exit $? $(date -u +%T)"
$P $K/wait_load.py 3
LT1_RECOIL=1 nice -n 19 $P -m event_universe.run $F/world_ga2_450.json $O/lt1_ga2_450.json back 10 > $F/out/ga2_450_run.txt 2>&1; echo "ga2 exit $? $(date -u +%T)"
nice -n 19 $P $F/lt1_moment.py $O/lt1_ga2_450.json > $F/out/moment_ga2_450.json 2>&1; echo "moment ga2 exit $?"
nice -n 19 $P $F/ga2_return.py $O/lt1_ga2_450.json 2,218,442 > $F/out/ga2_return_flag.json 2>&1; echo "return flag exit $?"
$P $K/wait_load.py 3
PYTHONPATH=$W/src nice -n 19 $P -m event_universe.run $F/world_ga2_450.json $O/head_ga2_450.json back 10 > $F/out/ga2_450_head_run.txt 2>&1; echo "ga2 head exit $? $(date -u +%T)"
nice -n 19 $P $F/ga2_return.py $O/head_ga2_450.json 2,218,442 > $F/out/ga2_return_head.json 2>&1; echo "return head exit $?"
$P $K/wait_load.py 3
LT1_RECOIL=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_bodies.json $O/lt1_bodies300.json back 10 > $F/out/bodies300_run.txt 2>&1; echo "bodies exit $? $(date -u +%T)"
nice -n 19 $P $F/lt1_moment.py $O/lt1_bodies300.json > $F/out/moment_bodies300.json 2>&1; echo "moment bodies exit $?"
$P $K/wait_load.py 3
LT1_RECOIL=1 nice -n 19 $P $K/clicks_48.py $K/world_chiral_300.json 60 $F/out/c48_chiral_3cube_60_flag.json cube 3 > $F/out/c48_run.txt 2>&1; echo "c48 exit $? $(date -u +%T)"
echo "all done $(date -u +%T)"
