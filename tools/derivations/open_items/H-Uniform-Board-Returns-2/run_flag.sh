#!/bin/sh
W=$(cd "$(dirname "$0")/../../.." && pwd)
B=$W/tools/derivations/bb2
export PYTHONPATH=$B/engine TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd "$B"
# the flag absent: bit for bit
$PY -m event_universe.run worlds/world_one3_400.json out/one3_400_off.json back 10 > out/one3_400_off.log 2>&1
export BB2_SWAP=7
$PY -m event_universe.run worlds/world_sea3_400.json out/sea3_400_s7.json back 10 > out/sea3_400_s7.log 2>&1
$PY -m event_universe.run worlds/world_one3_400.json out/one3_400_s7.json back 10 > out/one3_400_s7.log 2>&1
$PY -m event_universe.run worlds/world_hole3_400.json out/hole3_400_s7.json back 10 > out/hole3_400_s7.log 2>&1
BB2_SRC=$B/engine $PY sub_drift.py worlds/world_sea3_400.json 1 out/sub_L1_s7.json > out/sub_L1_s7.log 2>&1
BB2_SRC=$B/engine $PY sub_drift.py worlds/world_sea3_400.json 64 out/sub_L64_s7.json > out/sub_L64_s7.log 2>&1
$PY -m event_universe.run worlds/world_chiral5_300.json out/chiral5_300_s7.json back 10 > out/chiral5_300_s7.log 2>&1
$PY -m event_universe.run worlds/world_holeat5_400.json out/holeat5_400_s7.json back 10 > out/holeat5_400_s7.log 2>&1
echo done
