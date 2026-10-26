#!/bin/sh
# gp1: the 5-cube under the table gp1w with the children's lay ii, the pick on: the mirror STATE to 60 (the dig prints every interval; the mirror_state row at the end)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export GP1_PICK=1
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM=ii run dig5_ii_w $PY dig_off.py src_gp1_pick worlds/world_chiral_5_60.json 60 4 gp1w &
GP1_FORM=ii run mir5_ii_w $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_ii_w.json 4 gp1w &
GP1_FORM=   run dig5_off_w $PY dig_off.py src_gp1_pick worlds/world_chiral_5_60.json 60 4 gp1w &
wait
echo all > out/run_w5.done
