#!/bin/sh
# tw2's batch: every world at every trace weight under the flagged copy, 3 at a time at nice 19; the summaries under out/
H=$(cd "$(dirname "$0")" && pwd)
W=$H/../../../../tests/worlds
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
mkdir -p $TMPDIR $H/out
for world in world_universe world_hole world_chiral world_plasma_3 world_sea_3; do
  for t in 54 27 108 36 48 60 72 6 9 18; do
    echo "$world $t"
  done
done | xargs -P 3 -L 1 sh -c 'TW2_TRACE=$1 nice -n 19 '"$PY"' '"$H"'/run_tw2.py '"$W"'/$0.json '"$H"'/out/$0.t$1.json > '"$H"'/out/$0.t$1.log 2>&1'
echo BATCH DONE
