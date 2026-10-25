#!/bin/sh
# ma1's records, every command written out (no loop); the engine's src for the unflagged runs
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
D=$S/hands/ma1/tools/derivations/ma1
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$S/hands/ma1/src
cd $D
nice -n 19 $PY ma_run.py worlds/sea3_400.json out/sea3_400 back 10 every 50 > out/sea3_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/sea4_400.json out/sea4_400 back 10 every 50 > out/sea4_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/a3_400.json out/a3_400 back 10 every 50 > out/a3_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/c3_400.json out/c3_400 back 10 every 50 > out/c3_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/b4_400.json out/b4_400 back 10 every 50 > out/b4_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/b3_60.json out/b3_60 back 10 every 20 > out/b3_60.log 2>&1
nice -n 19 $PY ma_run.py worlds/b4_flip_400.json out/b4_flip_400 back 10 every 50 > out/b4_flip_400.log 2>&1
nice -n 19 $PY ma_run.py worlds/s4_400.json out/s4_400 back 10 every 50 > out/s4_400.log 2>&1
nice -n 19 $PY -m event_universe.run worlds/file27_3_400.json out/file27_3_400_record.json back 10 > out/file27_3_400.log 2>&1
nice -n 19 $PY -m event_universe.gates out/file27_3_400_record.json > out/file27_3_400_gates.jsonl 2>&1
nice -n 19 $PY -m event_universe.gates out/sea4_400_record.json > out/sea4_400_gates.jsonl 2>&1
nice -n 19 $PY -m event_universe.gates out/b4_400_record.json > out/b4_400_gates.jsonl 2>&1
echo DONE > out/run_all.done
