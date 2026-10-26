#!/bin/sh
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
LR2_LAY=1 LR2_PICK=1 run c48_3cube_60_LP $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_LP.json &
LR2_LAY=  LR2_PICK=1 run c48_3cube_60_P $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_P.json &
LR2_LAY=1 LR2_PICK=  run c48_3cube_60_L $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_L.json &
LR2_LAY=  LR2_PICK=  run c48_3cube_60_off $PY run_48.py src_lr2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_off.json &
wait
LR2_LAY=1 LR2_PICK=1 run c48_5cube_60_LP $PY run_48.py src_lr2 worlds/world_chiral_5_60.json 60 out/c48_5cube_60_LP.json
echo all > out/run_48s.done
