#!/bin/sh
# gp1: the table gp1v (every plane (det, even); the potential's time line det, its odd lines det times the axis's sign: the sign holder C-odd as a whole; the carrier and the walled row even), with the children's lay ii, the pick on
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export GP1_PICK=1
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM=ii run mir3_ii_v $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_ii_v.json 4,1 gp1v &
GP1_FORM=ii run mir5_ii_v $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_ii_v.json 4 gp1v &
GP1_FORM=ii run dig3_ii_v $PY dig_off.py src_gp1_pick worlds/world_chiral_3_30.json 60 4 gp1v &
wait
echo all > out/run_v.done
