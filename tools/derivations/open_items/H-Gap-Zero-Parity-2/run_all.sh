#!/bin/sh
# gp2: every measurement in parallel under nice; F = GP2_FORM children_sign, P = GP2_PICK 1 (lr2's centred pick)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
R=../../../../../../records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
DIAG=0,1,2,3,4,5,6,7
GP2_FORM=children_sign GP2_PICK=1 run mirror_mK_3cube_60_FP $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_3_30.json 60 out/mirror_mK_3cube_60_FP.json $DIAG mK &
GP2_FORM=              GP2_PICK=1 run mirror_mK_3cube_60_P  $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_3_30.json 60 out/mirror_mK_3cube_60_P.json $DIAG mK &
GP2_FORM=              GP2_PICK=1 run mirror_K_3cube_60_P   $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_3_30.json 60 out/mirror_K_3cube_60_P.json $DIAG K &
GP2_FORM=children_sign GP2_PICK=1 run mirror_K_3cube_60_FP  $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_3_30.json 60 out/mirror_K_3cube_60_FP.json $DIAG K &
GP2_FORM=children_sign GP2_PICK=1 run mirror_mK_5cube_60_FP $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_5_60.json 60 out/mirror_mK_5cube_60_FP.json $DIAG mK &
GP2_FORM=              GP2_PICK=1 run mirror_mK_5cube_60_P  $PY mirror_state_gp2.py src_gp2 worlds/world_chiral_5_60.json 60 out/mirror_mK_5cube_60_P.json $DIAG mK &
GP2_FORM=children_sign GP2_PICK=  run c48_3cube_60_F  $PY run_48.py src_gp2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_F.json &
GP2_FORM=children_sign GP2_PICK=1 run c48_3cube_60_FP $PY run_48.py src_gp2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_FP.json &
GP2_FORM=              GP2_PICK=  run c48_3cube_60_off $PY run_48.py src_gp2 worlds/world_chiral_3_30.json 60 out/c48_3cube_60_off.json &
GP2_FORM=children_sign GP2_PICK=  run ga2_F $PY ga2_course.py src_gp2 $W/tests/worlds/world_ga2.json 450 10 out/ga2_F.json 2,218,442 &
GP2_FORM=children_sign GP2_PICK=  run hole60_F $PY run_record.py src_gp2 $W/tests/worlds/world_hole.json 60 10 out/hole60_F.json $R/world_hole_60.json &
GP2_FORM=children_sign GP2_PICK=  run chiral60_F $PY run_record.py src_gp2 $W/tests/worlds/world_chiral.json 60 10 out/chiral60_F.json $R/world_chiral_60.json &
GP2_FORM=              GP2_PICK=  run hole60_off $PY run_record.py src_gp2 $W/tests/worlds/world_hole.json 60 10 out/hole60_off.json $R/world_hole_60.json &
GP2_FORM=children_sign GP2_PICK=  run universe400_F $PY run_record.py src_gp2 $W/tests/worlds/world_universe.json 400 10 out/universe400_F.json $R/world_universe_400.json &
GP2_FORM=children_sign GP2_PICK=  run pair3_400_F $PY run_record.py src_gp2 $W/tests/worlds/world_pair_3.json 400 10 out/pair3_400_F.json $R/world_pair_3_400.json &
GP2_FORM=children_sign GP2_PICK=  run plasma170_F $PY run_record.py src_gp2 $W/tests/worlds/world_plasma_3.json 170 10 out/plasma170_F.json $R/world_plasma_3_170.json &
wait
echo all > out/run_all.done
