#!/bin/sh
# gp1: every measurement in parallel under nice; GP1_FORM=ii the children's lay with the charge's sign on re_now; empty the head bit for bit
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=../../../../../../records/2ab32b518
export TMPDIR=/dev/shm/tmp
mkdir -p $TMPDIR out
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
GP1_FORM=ii run mir3_ii_u $PY mirror_state.py src_gp1 worlds/world_chiral_3_30.json 60 out/mir3_ii_u.json 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 gp1u &
GP1_FORM=ii run mir3_ii_l $PY mirror_state.py src_gp1 worlds/world_chiral_3_30.json 60 out/mir3_ii_l.json 4,1,2,3 gp1l &
GP1_FORM=   run mir3_off_u $PY mirror_state.py src_gp1 worlds/world_chiral_3_30.json 60 out/mir3_off_u.json 4,1,3 gp1u &
GP1_FORM=   run mir3_off_law $PY mirror_state.py src_gp1 worlds/world_chiral_3_30.json 60 out/mir3_off_law.json 4 law &
GP1_FORM=ii run mir5_ii_u $PY mirror_state.py src_gp1 worlds/world_chiral_5_60.json 60 out/mir5_ii_u.json 4,1,3 gp1u &
GP1_FORM=ii run mir5_ii_l $PY mirror_state.py src_gp1 worlds/world_chiral_5_60.json 60 out/mir5_ii_l.json 4,1 gp1l &
GP1_FORM=   run mir5_off_u $PY mirror_state.py src_gp1 worlds/world_chiral_5_60.json 60 out/mir5_off_u.json 4 gp1u &
GP1_FORM=ii run c48_3_ii $PY run_48.py src_gp1 worlds/world_chiral_3_30.json 60 out/c48_3_ii.json &
GP1_FORM=   run c48_3_off $PY run_48.py src_gp1 worlds/world_chiral_3_30.json 60 out/c48_3_off.json &
GP1_FORM=ii run ga2_ii $PY ga2_course.py src_gp1 $W/tests/worlds/world_ga2.json 450 10 out/ga2_ii.json 2,218,442 &
GP1_FORM=ii run hole60_ii $PY run_record.py src_gp1 $W/tests/worlds/world_hole.json 60 10 out/hole60_ii.json $R/world_hole_60.json &
GP1_FORM=ii run chiral60_ii $PY run_record.py src_gp1 $W/tests/worlds/world_chiral.json 60 10 out/chiral60_ii.json $R/world_chiral_60.json &
GP1_FORM=ii run universe400_ii $PY run_record.py src_gp1 $W/tests/worlds/world_universe.json 400 10 out/universe400_ii.json $R/world_universe_400.json &
GP1_FORM=ii run pair400_ii $PY run_record.py src_gp1 $W/tests/worlds/world_pair_3.json 400 10 out/pair400_ii.json $R/world_pair_3_400.json &
GP1_FORM=ii run plasma170_ii $PY run_record.py src_gp1 $W/tests/worlds/world_plasma_3.json 170 10 out/plasma170_ii.json $R/world_plasma_3_170.json &
GP1_FORM=   run hole60_off $PY run_record.py src_gp1 $W/tests/worlds/world_hole.json 60 10 out/hole60_off.json $R/world_hole_60.json &
wait
echo all > out/run_all.done
