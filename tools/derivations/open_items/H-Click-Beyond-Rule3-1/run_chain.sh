#!/bin/sh
# cx1: the runs in order, one at a time, nice 19, wait_load before each run above a minute.
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cx1; H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cx1/tools/derivations/open_items/H-Click-Beyond-Rule3-1; K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit; P=/home/user/Universe24/venv314/bin/python; D=/dev/shm/tmp/cx1; S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
cd $D
$P $K/wait_load.py 3
echo "ga2 start $(date -u +%H:%M:%S)" >> $D/chain.log
nice -n 19 $P $H/cx1_clicks_read.py $S/records/8b1dbb781/world_ga2_450.json 450 $H/out/cx1_ga2_450.json back 10 > $D/ga2.stdout 2>&1
echo "ga2 done $(date -u +%H:%M:%S)" >> $D/chain.log
$P $K/wait_load.py 3
echo "flag start $(date -u +%H:%M:%S)" >> $D/chain.log
nice -n 19 $P $K/make_flagged_copy.py cx1 CX1_ONE_OBJECT $H/cx1_flag_replacements.json src $W/src worlds $W/tests/worlds/world_hole.json,$W/tests/worlds/world_nature.json python $P > $D/flag_check.stdout 2>&1
echo "flag check exit $? $(date -u +%H:%M:%S)" >> $D/chain.log
PYTHONPATH=$D/src_cx1 CX1_ONE_OBJECT=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_hole.json $D/flag_hole.json back 20 > $D/flag_hole.stdout 2>&1
PYTHONPATH=$D/src_cx1 CX1_ONE_OBJECT=1 nice -n 19 $P -m event_universe.run $W/tests/worlds/world_nature.json $D/flag_chiral.json back 20 > $D/flag_chiral.stdout 2>&1
$P $H/cx1_compare_records.py $D/flag_hole.json $D/head_world_hole.json > $H/out/flag_on_hole_vs_head.json 2>&1
$P $H/cx1_compare_records.py $D/flag_chiral.json $D/head_world_nature.json > $H/out/flag_on_chiral_vs_head.json 2>&1
echo "flag on compared $(date -u +%H:%M:%S)" >> $D/chain.log
nice -n 19 $P $D/bk1_click_read.py $W/tests/worlds/world_hole.json $H/out/bk1_hole_60.json > $D/bk1_hole.stdout 2>&1
nice -n 19 $P $D/bk1_click_read.py $W/tests/worlds/world_nature.json $H/out/bk1_chiral_60.json > $D/bk1_chiral.stdout 2>&1
echo "bell done $(date -u +%H:%M:%S)" >> $D/chain.log
$P $K/wait_load.py 3
echo "48 start $(date -u +%H:%M:%S)" >> $D/chain.log
CX1_ONE_OBJECT=1 nice -n 19 $P $K/clicks_48.py $W/tests/worlds/world_nature.json 60 $H/out/c48_chiral_cube3_flag.json cube 3 src $D/src_cx1 > $D/c48.stdout 2>&1
echo "48 done $(date -u +%H:%M:%S)" >> $D/chain.log
echo DONE >> $D/chain.log
