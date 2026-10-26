#!/bin/sh
# rw2: every measurement in parallel under nice; RW2_FORM=1 selects the folded copy src_rw2, unset the head copy src_head (the flag is the src path)
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
W=$S/hands/rw2
D=/dev/shm/tmp/rw2
R=$S/records/2ab32b518
PY=/home/user/Universe24/venv314/bin/python
REC=$W/tools/derivations/open_items/H-Lay-Rest-Mirror-2/run_record.py
R48=$W/tools/derivations/open_items/H-48-In-The-Clicks-3/run_48.py
export TMPDIR=/dev/shm/tmp
src() { if [ "$RW2_FORM" = "1" ]; then echo $D/src_rw2; else echo $D/src_head; fi; }
run() { out=$1; shift; nice -n 19 "$@" > $D/out/$out.stdout 2> $D/out/$out.stderr; echo done > $D/out/$out.done; }
export RW2_FORM=1
for wn in hole:60 chiral:60 bodies:300 universe:400 pair_3:400 plasma_3:170 ga2:450; do
  w=${wn%%:*}; n=${wn##*:}
  run ${w}_${n}_f1 $PY $REC $(src) $W/tests/worlds/world_$w.json $n 10 $D/out/${w}_${n}_f1.json $R/world_${w}_${n}.json &
done
run sea_3_240_f1 $PY $REC $(src) $W/tests/worlds/world_sea_3.json 240 10 $D/out/sea_3_240_f1.json &
run universe_3_60_f1 $PY $REC $(src) $W/tests/worlds/world_universe_3.json 60 10 $D/out/universe_3_60_f1.json &
run plasma_60_f1 $PY $REC $(src) $W/tests/worlds/world_plasma.json 60 10 $D/out/plasma_60_f1.json &
run hole_60_b20_f1 $PY $REC $(src) $W/tests/worlds/world_hole.json 60 20 $D/out/hole_60_b20_f1.json &
run chiral_60_b20_f1 $PY $REC $(src) $W/tests/worlds/world_chiral.json 60 20 $D/out/chiral_60_b20_f1.json &
run c48_3cube_60_f1 $PY $R48 $(src) $W/tools/derivations/open_items/H-48-In-The-Clicks-3/worlds/world_chiral_3_30.json 60 $D/out/c48_3cube_60_f1.json &
unset RW2_FORM
run sea_3_240_off $PY $REC $(src) $W/tests/worlds/world_sea_3.json 240 10 $D/out/sea_3_240_off.json &
run universe_3_60_off $PY $REC $(src) $W/tests/worlds/world_universe_3.json 60 10 $D/out/universe_3_60_off.json &
run plasma_60_off $PY $REC $(src) $W/tests/worlds/world_plasma.json 60 10 $D/out/plasma_60_off.json &
run c48_3cube_60_off $PY $R48 $(src) $W/tools/derivations/open_items/H-48-In-The-Clicks-3/worlds/world_chiral_3_30.json 60 $D/out/c48_3cube_60_off.json &
(cd $W && run suite_f1 $PY -m pytest -q -x -o pythonpath=$D/src_rw2 tests) &
wait
echo all > $D/out/run_all.done
