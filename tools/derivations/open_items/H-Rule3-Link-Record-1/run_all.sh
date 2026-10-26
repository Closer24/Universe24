#!/bin/sh
# rl1: every measurement in parallel under nice, the flag RL1_FORM from the environment; the records against the cache 2ab32b518
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
R=$S/records/2ab32b518
SRC=/dev/shm/tmp/rl1/src
SRCF=/dev/shm/tmp/rl1/src_fr
A48=../H-48-In-The-Clicks-3
WD=../H-Frozen-Node-Release-2/worlds
RR=../H-Lay-Rest-Mirror-2/run_record.py
TQ=../H-Torque-Of-The-Step-1/tq1_torque.py
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
for F in "" sum geo link; do
  N=${F:-off}
  RL1_FORM=$F run c48_3cube_60_$N $PY $A48/run_48.py $SRC $WD/world_chiral_3_30.json 60 out/c48_3cube_60_$N.json &
  RL1_FORM=$F run hole60_$N $PY $RR $SRC $W/tests/worlds/world_hole.json 60 10 out/hole60_$N.json $R/world_hole_60.json &
  RL1_FORM=$F PYTHONPATH=$SRC run tq_hole60_$N $PY $TQ $R/world_hole_60.json out/tq_hole60_$N.json &
done
for F in sum geo link; do
  RL1_FORM=$F run chiral60_$F $PY $RR $SRC $W/tests/worlds/world_chiral.json 60 10 out/chiral60_$F.json $R/world_chiral_60.json &
done
for F in sum link; do
  RL1_FORM=$F run universe400_$F $PY $RR $SRC $W/tests/worlds/world_universe.json 400 10 out/universe400_$F.json $R/world_universe_400.json &
  RL1_FORM=$F run pair3_400_$F $PY $RR $SRC $W/tests/worlds/world_pair_3.json 400 10 out/pair3_400_$F.json $R/world_pair_3_400.json &
  RL1_FORM=$F run plasma3_170_$F $PY $RR $SRC $W/tests/worlds/world_plasma_3.json 170 10 out/plasma3_170_$F.json $R/world_plasma_3_170.json &
  RL1_FORM=$F run ga2_450_$F $PY $RR $SRC $W/tests/worlds/world_ga2.json 450 10 out/ga2_450_$F.json $R/world_ga2_450.json &
  RL1_FORM=$F FR2_RELEASE=1 run chiral3000_fr_$F $PY rl1_probe.py $SRCF $W/tests/worlds/world_chiral.json 3000 100 /dev/shm/tmp/rl1/out/chiral3000_fr_$F.json &
done
RL1_FORM=sum run c48_5cube_30_sum $PY $A48/run_48.py $SRC $WD/world_chiral_5_60.json 30 out/c48_5cube_30_sum.json &
RL1_FORM= run c48_5cube_30_off $PY $A48/run_48.py $SRC $WD/world_chiral_5_60.json 30 out/c48_5cube_30_off.json &
wait
echo all > out/run_all.done
