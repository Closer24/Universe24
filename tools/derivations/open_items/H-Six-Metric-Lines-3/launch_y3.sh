#!/bin/bash
# the runs of the hand H-Six-Metric-Lines-3: the head and the flagged copy on every named world
cd "$(dirname "$0")/../../../.." || exit 1
Y3=tools/derivations/open_items/H-Six-Metric-Lines-3
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
run() { # engine world intervals back tag
  local env=""; local path=src
  if [ "$1" = head ]; then path=src; elif [ "$1" = on ]; then path=$Y3/src_y3; env="Y3_METRIC=1"; fi
  env $env PYTHONPATH=$path:. nice -n 19 $P $Y3/run_y3.py tests/worlds/$2 $3 $4 $Y3/out/$5_$1.json > $Y3/out/$5_$1.log 2>&1
}
(run head world_hole.json 60 10 hole60; run on world_hole.json 60 10 hole60; run head world_chiral.json 60 10 chiral60; run on world_chiral.json 60 10 chiral60) &
(run head world_plasma_3.json 170 10 plasma170; run on world_plasma_3.json 170 10 plasma170; run head world_plasma_3.json 90 10 plasma90; run on world_plasma_3.json 90 10 plasma90; run head world_sea_3.json 240 10 sea240; run on world_sea_3.json 240 10 sea240) &
(run head world_universe.json 400 10 universe400; run on world_universe.json 400 10 universe400) &
(run head world_bodies.json 300 10 bodies300; run on world_bodies.json 300 10 bodies300) &
wait
echo ALL DONE
