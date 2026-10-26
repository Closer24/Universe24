#!/bin/sh
# gp1: the mirror STATE beside the base with lr2's centred pick on (GP1_PICK=1, the read's parting kept out), the sign table by the law for a diagonal image: law (lr2's: every plane re even, im by det; the potential's time line by det, its odd lines by their axis; the carrier and the walled row even), gp1l (law with the gap-0 plane alone at (det, even): David's one sign changed), gp1u (every plane at (det, even): gp1's uniform table); GP1_FORM=ii the children's lay with the charge's sign on re_now, empty the head
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
export GP1_PICK=1
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM=   run mir3_off_law $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_off_law.json 4,1 law &
GP1_FORM=   run mir3_off_l $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_off_l.json 4,1 gp1l &
GP1_FORM=ii run mir3_ii_l $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_ii_l.json 4,1,3 gp1l &
GP1_FORM=ii run mir3_ii_u $PY mirror_state.py src_gp1_pick worlds/world_chiral_3_30.json 60 out/mir3_ii_u.json 4,1,3 gp1u &
GP1_FORM=   run mir5_off_l $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_off_l.json 4 gp1l &
GP1_FORM=ii run mir5_ii_l $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_ii_l.json 4 gp1l &
GP1_FORM=ii run mir5_ii_u $PY mirror_state.py src_gp1_pick worlds/world_chiral_5_60.json 60 out/mir5_ii_u.json 4 gp1u &
wait
echo all > out/run_more.done
