#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/cb24; M=$S/hands/cb24_merge; K=$S/e5/tools/derivations/open_items/H-Kit-48-Re-Cut-1; P=/home/user/Universe24/venv314/bin/python
D=/dev/shm/tmp/cb24; L=$D/logs; R=$D/records; C=$D/compare.py
mkdir -p $R
export TMPDIR=/dev/shm/tmp CHECK_BASE=6703dd95c
stamp() { echo "[$(date +%H:%M:%S) load $(cut -d' ' -f1 /proc/loadavg)] $*" >> $L/chain.log; }
stamp start; $P $K/wait_load.py 3 >> $L/chain.log 2>&1; stamp "load ok"
cd $W; export PYTHONPATH=$W/src
run() { # $1 world $2 out $3 back
  cd $R; s=$(date +%s); nice -n 19 $P -m event_universe.run $W/tests/worlds/$1 $R/$2 back $3 > $L/run_$2.out 2>&1; echo "$2 exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; cd $W
}
run world_hole.json world_hole_60.json 20; stamp "hole done"
run world_nature.json world_chiral_60.json 20; stamp "chiral done"
run world_bodies.json world_bodies_120.json 20; stamp "bodies done"
for p in hole:world_hole_60 chiral:world_chiral_60 bodies:world_bodies_120; do n=${p%%:*}; f=${p##*:}; echo "$n: $($P $C $W/examples/records/$n.json $R/$f.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-400)" >> $L/compare_records.txt; done
stamp "compare done"
for f in world_hole_60 world_chiral_60; do nice -n 19 $P $K/conservation_check.py $R/$f.json out $L/cons_$f.json > $L/cons_$f.out 2>&1; echo "$f conservation exit $?" >> $L/runs.txt; done
stamp "conservation done"
$P $K/wait_load.py 3 >> $L/chain.log 2>&1; stamp "load ok for the suite"
cd $W; s=$(date +%s); nice -n 19 $P -m pytest -q -p no:cacheprovider -n 2 --junitxml=$D/junit.xml > $L/pytest.out 2>&1; echo "pytest exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; stamp "pytest done"
$D/gates.sh $M $L/gates_merge.txt; stamp "gates merge done"
stamp "all done"
