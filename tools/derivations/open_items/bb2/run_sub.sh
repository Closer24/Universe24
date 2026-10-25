#!/bin/sh
W=$(cd "$(dirname "$0")/../../.." && pwd)
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd "$W/tools/derivations/bb2"
$PY sub_drift.py worlds/world_sea3_400.json 1 out/sub_L1.json > out/sub_L1.log 2>&1
$PY sub_drift.py worlds/world_sea3_400.json 4 out/sub_L4.json > out/sub_L4.log 2>&1
$PY sub_drift.py worlds/world_sea3_400.json 16 out/sub_L16.json > out/sub_L16.log 2>&1
$PY sub_drift.py worlds/world_sea3_400.json 64 out/sub_L64.json > out/sub_L64.log 2>&1
$PY sub_drift.py worlds/world_sea3_400.json 128 out/sub_L128.json > out/sub_L128.log 2>&1
echo done
