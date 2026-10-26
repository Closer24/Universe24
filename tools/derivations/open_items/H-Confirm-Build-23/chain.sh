#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/cb23; M=$S/hands/cb23_merge; K=$S/hands/kit; P=/home/user/Universe24/venv314/bin/python
D=/dev/shm/tmp/cb23; L=$D/logs; R=$D/records; C=$D/compare.py
export TMPDIR=/dev/shm/tmp CHECK_BASE=6703dd95c
stamp() { echo "[$(date +%H:%M:%S) load $(cut -d' ' -f1 /proc/loadavg)] $*" >> $L/chain.log; }
gates() { # $1 tree $2 tag
  cd $1; export PYTHONPATH=$1/src
  for g in "ruff check ." "ruff format --check ." "mypy" "$P tools/engine_gates.py" "$P tools/record_code_shape.py" "$P tools/tests_shape.py" "$P tools/documents_gates.py"; do
    n=$(echo "$g" | tr ' /.' '___'); nice -n 19 $g > $L/gate_$2_$n.out 2>&1; e=$?
    echo "$2 | $g | exit $e | $(tail -1 $L/gate_$2_$n.out | cut -c1-200)" >> $L/gates_$2.txt
  done
}
stamp start; $P $K/wait_load.py 3 >> $L/chain.log 2>&1; stamp "load ok"
gates $W head; stamp "gates head done"
cd $W; export PYTHONPATH=$W/src
$P $D/toy_check.py $W > $L/toy_check.out 2>&1; stamp "toy check done"
run() { # $1 world $2 out $3 back
  cd $R; s=$(date +%s); nice -n 19 $P -m event_universe.run $W/tests/worlds/$1 $R/$2 back $3 > $L/run_$2.out 2>&1; echo "$2 exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; cd $W
}
run world_hole.json world_hole_60.json 20; run world_nature.json world_chiral_60.json 20; run world_bodies.json world_bodies_300.json 20
stamp "three records done"
for p in hole:world_hole_60 chiral:world_chiral_60 bodies:world_bodies_300; do n=${p%%:*}; f=${p##*:}; echo "$n: $($P $C $W/examples/records/$n.json $R/$f.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-400)" >> $L/compare_records.txt; done
for f in world_hole_60 world_chiral_60; do nice -n 19 $P $K/conservation_check.py $R/$f.json out $L/cons_$f.json > $L/cons_$f.out 2>&1; echo "$f conservation exit $?" >> $L/runs.txt; done
stamp "conservation done"
cd $W; nice -n 19 $P -m pytest -n 2 -q --junitxml=$W/artifacts/junit.xml > $L/pytest.out 2>&1; echo "pytest exit $?" >> $L/runs.txt; stamp "pytest done"
$P $K/wait_load.py 3 >> $L/chain.log 2>&1
cd $D; s=$(date +%s); nice -n 19 $P $K/clicks_48.py $W/tests/worlds/world_nature.json 60 $D/clicks48_chiral3.json cube 3 > $L/clicks48.out 2>&1; echo "clicks48 exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; stamp "clicks48 done"
gates $M merge; stamp "gates merge done"
cd $W; export PYTHONPATH=$W/src
run world_universe.json world_universe_400.json 10; run world_pair_3.json world_pair_3_400.json 10; run world_plasma_3.json world_plasma_3_170.json 10; run world_ga2.json world_ga2_450.json 10
stamp "seven worlds done"
for f in world_universe_400 world_pair_3_400 world_plasma_3_170 world_bodies_300 world_hole_60 world_chiral_60 world_ga2_450; do echo "$f: $($P $C /dev/shm/tmp/cb22/records/$f.json $R/$f.json 2>&1 | tail -3 | tr '\n' ' ' | cut -c1-500)" >> $L/compare_worlds.txt; done
stamp "compare worlds done"
run world_sea_3.json world_sea_3.json 10; run world_universe_3.json world_universe_3.json 10; run world_plasma.json world_plasma.json 10
stamp "all done"
