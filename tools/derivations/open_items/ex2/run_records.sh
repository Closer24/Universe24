#!/bin/bash
# the records one at a time: base (the engine's src), off (the copy, flag absent), on (the copy, EX2_CARRY=1); then the compare and the reading
PY=/home/user/Universe24/venv314/bin/python
W=$(cd "$(dirname "$0")/../../.." && pwd)
D=$W/tools/derivations/ex2
export TMPDIR=/dev/shm/tmp
run_one() {
  name=$1; world=$2
  (time env PYTHONPATH=$W/src $PY -m event_universe.run $D/worlds/$world $D/out/base_$name.json back 10) > $D/out/base_$name.txt 2>&1
  (time env PYTHONPATH=$D/engine $PY -m event_universe.run $D/worlds/$world $D/out/off_$name.json back 10) > $D/out/off_$name.txt 2>&1
  (time env EX2_CARRY=1 PYTHONPATH=$D/engine $PY -m event_universe.run $D/worlds/$world $D/out/on_$name.json back 10) > $D/out/on_$name.txt 2>&1
  echo "== $name: off against base:" ; $PY $D/compare_records.py $D/out/base_$name.json $D/out/off_$name.json
  echo "== $name: base reading" ; $PY $D/read_exact.py $D/out/base_$name.json
  echo "== $name: on reading" ; $PY $D/read_exact.py $D/out/on_$name.json
  echo "== $name: gates on" ; PYTHONPATH=$W/src $PY -m event_universe.gates $D/out/on_$name.json > $D/out/on_${name}_gates.txt 2>&1
  PYTHONPATH=$W/src $PY -m event_universe.gates $D/out/base_$name.json > $D/out/base_${name}_gates.txt 2>&1
  grep -h "real" $D/out/base_$name.txt $D/out/on_$name.txt
}
run_one chiral_60 world_chiral_60.json
run_one bodies_120 world_bodies_120.json
run_one chiral_300 world_chiral_300.json
echo ALL DONE
