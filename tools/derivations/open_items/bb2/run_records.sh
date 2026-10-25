#!/bin/sh
# bb2: the records with the engine's own writer, run back 10 (one command per world; no loop).
W=$(cd "$(dirname "$0")/../../.." && pwd)
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd "$W/tools/derivations/bb2"
$PY -m event_universe.run worlds/world_sea3_400.json out/sea3_400.json back 10 > out/sea3_400.log 2>&1
$PY -m event_universe.run worlds/world_sea5_400.json out/sea5_400.json back 10 > out/sea5_400.log 2>&1
$PY -m event_universe.run worlds/world_one3_400.json out/one3_400.json back 10 > out/one3_400.log 2>&1
$PY -m event_universe.run worlds/world_hole3_400.json out/hole3_400.json back 10 > out/hole3_400.log 2>&1
$PY -m event_universe.run worlds/world_one5_400.json out/one5_400.json back 10 > out/one5_400.log 2>&1
$PY -m event_universe.run worlds/world_hole5_400.json out/hole5_400.json back 10 > out/hole5_400.log 2>&1
$PY -m event_universe.run worlds/world_holeat5_400.json out/holeat5_400.json back 10 > out/holeat5_400.log 2>&1
$PY -m event_universe.run worlds/world_chiral5_300.json out/chiral5_300.json back 10 > out/chiral5_300.log 2>&1
echo done
