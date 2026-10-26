#!/bin/sh
# gp1: the table gp1w (gp1v with the walled row odd: the sign holder, its record's re line and its flux row C-odd as a whole; the planes' im lines, the carrier and the other rows even), the children's lay ii, the pick on
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export GP1_PICK=1
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM=ii run mir3_ii_w $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_ii_w.json 4,1,3 gp1w &
GP1_FORM=ii run mir5_ii_w $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_ii_w.json 4 gp1w &
GP1_FORM=ii run dig3_ii_w $PY dig_off.py src_gp1_pick worlds/world_chiral_3_30.json 60 4 gp1w &
GP1_FORM=   run dig3_off_w $PY dig_off.py src_gp1_pick worlds/world_chiral_3_30.json 60 4 gp1w &
wait
echo all > out/run_w.done
