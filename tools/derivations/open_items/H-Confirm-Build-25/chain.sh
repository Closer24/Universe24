#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/cb25; K=$S/e5/tools/derivations/open_items/H-Kit-48-Re-Cut-1; P=/home/user/Universe24/venv314/bin/python
F=$W/tools/derivations/open_items/H-Confirm-Build-25
D=/dev/shm/tmp/cb25; L=$D/logs; R=$D/records
mkdir -p $R $L
export TMPDIR=/dev/shm/tmp CHECK_BASE=6703dd95c
stamp() { echo "[$(date -u +%H:%M:%S) load $(cut -d' ' -f1 /proc/loadavg)] $*" >> $L/chain.log; }
stamp start
$P $K/wait_load.py 3 >> $L/chain.log 2>&1; stamp "load ok"
bash $F/gates.sh $W $L/gates_head.txt; stamp "gates head done"
run() {
  cd $R; s=$(date +%s); nice -n 19 $P -m event_universe.run $W/tests/worlds/$1 $R/$2 back $3 > $L/run_$2.out 2>&1
  echo "$2 exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; cd $W
}
cd $W; export PYTHONPATH=$W/src
run world_hole.json world_hole_60.json 20; stamp "hole done"
run world_nature.json world_chiral_60.json 20; stamp "chiral done"
run world_bodies.json world_bodies_120.json 20; stamp "bodies done"
echo "hole: $($P $F/compare.py $W/examples/records/hole.json $R/world_hole_60.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-400)" >> $L/compare_records.txt
echo "chiral: $($P $F/compare.py $W/examples/records/chiral.json $R/world_chiral_60.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-400)" >> $L/compare_records.txt
echo "bodies: $($P $F/compare.py $W/examples/records/bodies.json $R/world_bodies_120.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-400)" >> $L/compare_records.txt
stamp "compare done"
nice -n 19 $P $K/conservation_check.py $R/world_hole_60.json out $L/cons_hole60.json > $L/cons_hole60.out 2>&1; echo "hole conservation exit $?" >> $L/runs.txt
nice -n 19 $P $K/conservation_check.py $R/world_chiral_60.json out $L/cons_chiral60.json > $L/cons_chiral60.out 2>&1; echo "chiral conservation exit $?" >> $L/runs.txt
stamp "conservation done"
$P $K/wait_load.py 3 >> $L/chain.log 2>&1; stamp "load ok for the suite"
cd $W; s=$(date +%s); nice -n 19 $P -m pytest -q -p no:cacheprovider -n 2 --junitxml=$D/junit.xml > $L/pytest.out 2>&1
echo "pytest exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; stamp "pytest done"
stamp "all done"
