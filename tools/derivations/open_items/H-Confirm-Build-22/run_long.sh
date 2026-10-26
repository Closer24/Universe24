#!/bin/sh
# H-Confirm-Build-22: the long runs after the load rule (push_done and the 1-minute load below 3, or 60 minutes and the load below 3).
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/cb22; M=$S/hands/cb22_merge; H=$W/tools/derivations/open_items/H-Confirm-Build-22; L=$H/logs
R=$S/records/8b1dbb781; O=/dev/shm/tmp/cb22/records; MR=/dev/shm/tmp/cb22/merge_records
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp CHECK_BASE=6703dd95c
t0=$(date +%s)
load() { cut -d' ' -f1 /proc/loadavg | cut -d. -f1; }
while :; do
  now=$(date +%s); l=$(load)
  if [ -f $S/push_done ] && [ "$l" -lt 3 ]; then echo "gate open: push_done present, load $(cut -d' ' -f1 /proc/loadavg) at $(date -u +%T) after $((now-t0)) s" > $L/gate.txt; break; fi
  if [ $((now-t0)) -ge 3600 ] && [ "$l" -lt 3 ]; then echo "gate open: 60 minutes passed without push_done, load $(cut -d' ' -f1 /proc/loadavg) at $(date -u +%T)" > $L/gate.txt; break; fi
  echo "$(date -u +%T) load $(cut -d' ' -f1 /proc/loadavg) push_done $( [ -f $S/push_done ] && echo yes || echo no )" >> $L/gate_wait.log
  sleep 60
done
run() { start=$(date +%s); cd $W; PYTHONPATH=$W/src nice -n 19 $PY -m event_universe.run $1 $O/$2.json back $3 > $L/run_$2.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $L/run_$2.out; }
( run tests/worlds/world_bodies.json world_bodies_300 20; run tests/worlds/world_nature.json world_chiral_60 20; run tests/worlds/world_pair_3.json world_pair_3_400 10 ) &
( run /dev/shm/tmp/cb22/world_ga2_450.json world_ga2_450 10; run tests/worlds/world_universe.json world_universe_400 10; run tests/worlds/world_hole.json world_hole_60 20; run /dev/shm/tmp/cb22/world_plasma_3_170.json world_plasma_3_170 10 ) &
( cd $W; start=$(date +%s); nice -n 19 $PY -m mypy > $L/gate_cb22_mypy.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $L/gate_cb22_mypy.out ) &
wait
echo "worlds done at $(date -u +%T), $(( $(date +%s)-t0 )) s from the start" >> $L/gate.txt
: > $H/compare_worlds.txt
for n in world_universe_400 world_pair_3_400 world_plasma_3_170 world_ga2_450 world_hole_60 world_chiral_60 world_bodies_300; do
  echo "$n: $($PY $H/compare.py $O/$n.json $R/$n.json 2>&1 | cut -c1-600)" >> $H/compare_worlds.txt
done
: > $H/compare_records.txt
for p in hole:world_hole_60 chiral:world_chiral_60 bodies:world_bodies_300; do n=${p%%:*}; r=${p##*:}
  echo "$n.json (committed at 3dc12e307) against the build's own $r: $($PY $H/compare.py $W/examples/records/$n.json $O/$r.json 2>&1 | cut -c1-600)" >> $H/compare_records.txt
done
# the merge: the readings regenerated on the merged tree, compared with both sides, then set in place for the run
cd $M
for n in hole chiral bodies; do
  git show :2:examples/records/$n.reading.jsonl > $MR/$n.reading.ours.jsonl; git show :3:examples/records/$n.reading.jsonl > $MR/$n.reading.theirs.jsonl
  PYTHONPATH=$M/src nice -n 19 $PY -m event_universe.gates examples/records/$n.json > $MR/$n.reading.jsonl 2> $L/merge_reading_$n.err
  echo "$n: regenerated $(wc -l < $MR/$n.reading.jsonl) lines; against engine-5.0-test's: $(cmp -s $MR/$n.reading.jsonl $MR/$n.reading.ours.jsonl && echo EQUAL || echo APART) ($(wc -l < $MR/$n.reading.ours.jsonl) lines); against toys-5's: $(cmp -s $MR/$n.reading.jsonl $MR/$n.reading.theirs.jsonl && echo EQUAL || echo APART) ($(wc -l < $MR/$n.reading.theirs.jsonl) lines)" >> $H/merge_readings.txt
  cp $MR/$n.reading.jsonl $M/examples/records/$n.reading.jsonl
done
for n in hole chiral bodies; do PYTHONPATH=$W/src nice -n 19 $PY -m event_universe.gates $W/examples/records/$n.json > $MR/$n.reading.cb22.jsonl 2>/dev/null; echo "$n on 3dc12e307 alone: $(cmp -s $MR/$n.reading.cb22.jsonl $W/examples/records/$n.reading.jsonl && echo EQUAL || echo APART) to the committed" >> $H/merge_readings.txt; done
git show :2:tests/test_the_record.py > /dev/shm/tmp/cb22/merge_tests/test_the_record_ours.py; git show :3:tests/test_the_record.py > /dev/shm/tmp/cb22/merge_tests/test_the_record_theirs.py
: > $L/merge_gates_exit.txt
for g in "ruff check ." "ruff format --check ." "$PY -m mypy" "$PY tools/engine_gates.py" "$PY tools/record_code_shape.py" "$PY tools/tests_shape.py" "$PY tools/documents_gates.py"; do n=$(echo "$g" | awk '{print $NF}' | tr '/.' '__'); PYTHONPATH=$M/src nice -n 19 $g > $L/gate_merge_$n.out 2>&1; echo "$g -> exit $? : $(tail -1 $L/gate_merge_$n.out | cut -c1-200)" >> $L/merge_gates_exit.txt; done
for side in theirs ours; do PYTHONPATH=$M/src:$M nice -n 19 $PY -m pytest -q -p no:cacheprovider --rootdir=$M /dev/shm/tmp/cb22/merge_tests/test_the_record_$side.py > $L/merge_test_the_record_$side.out 2>&1; echo "test_the_record ($side side of the conflict, on the merged tree with the regenerated readings): exit $?: $(tail -1 $L/merge_test_the_record_$side.out)" >> $L/merge_gates_exit.txt; done
echo "merge done at $(date -u +%T), $(( $(date +%s)-t0 )) s" >> $L/gate.txt
cd $W; start=$(date +%s); mkdir -p artifacts; PYTHONPATH=$W/src nice -n 19 $PY -m pytest -n 2 -q --junitxml=artifacts/junit.xml > $L/pytest_suite.out 2>&1; echo "exit $? seconds $(($(date +%s)-start))" >> $L/pytest_suite.out
echo "suite done at $(date -u +%T), $(( $(date +%s)-t0 )) s" >> $L/gate.txt
echo ALL_DONE > $L/run_long.done
