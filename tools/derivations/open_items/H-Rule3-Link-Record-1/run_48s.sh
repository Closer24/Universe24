#!/bin/sh
# rl1: the 48 on the clicks alone (the worlds with the head's universe: H-Frozen-Node-Release-2/worlds), relaunched
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/rl1/src
A48=../H-48-In-The-Clicks-3
WD=../H-Frozen-Node-Release-2/worlds
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
for F in "" sum geo link; do
  N=${F:-off}
  RL1_FORM=$F run c48_3cube_60_$N $PY $A48/run_48.py $SRC $WD/world_chiral_3_30.json 60 out/c48_3cube_60_$N.json &
done
RL1_FORM=sum run c48_5cube_30_sum $PY $A48/run_48.py $SRC $WD/world_chiral_5_60.json 30 out/c48_5cube_30_sum.json &
RL1_FORM= run c48_5cube_30_off $PY $A48/run_48.py $SRC $WD/world_chiral_5_60.json 30 out/c48_5cube_30_off.json &
wait
echo all > out/run_48s.done
