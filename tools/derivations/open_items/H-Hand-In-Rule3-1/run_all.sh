#!/bin/bash
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/hd1/src TMPDIR=/dev/shm/tmp
P=/home/user/Universe24/venv314/bin/python
H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/hd1/tools/derivations/open_items/H-Hand-In-Rule3-1
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/hd1/tests/worlds
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
cd /dev/shm/tmp/hd1
date -u > chain.log
nice -n 19 $P $H/parity_reader.py $W/world_hole.json 60 pr_hole_60.json back 20 > pr_hole_60.stdout 2> pr_hole_60.stderr
date -u >> chain.log
nice -n 19 $P $H/parity_reader.py $W/world_nature.json 60 pr_chiral_60.json back 20 > pr_chiral_60.stdout 2> pr_chiral_60.stderr
date -u >> chain.log
$P $K/wait_load.py 3 >> chain.log
nice -n 19 $P $K/clicks_48.py $W/world_hole.json 60 c48_hole_60_cube5.json > c48_hole_60_cube5.stdout 2> c48_hole_60_cube5.stderr
date -u >> chain.log
nice -n 19 $P $H/parity_reader.py $W/world_ga2.json 450 pr_ga2_450.json back 10 > pr_ga2_450.stdout 2> pr_ga2_450.stderr
date -u >> chain.log
echo CHAIN_DONE >> chain.log
