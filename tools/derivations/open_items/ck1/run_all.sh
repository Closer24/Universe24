#!/bin/sh
# ck1: the eight records, 400 intervals, back 10, the 4-cube; every command written out (no loop); four at a time
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
D=$S/hands/ck1/tools/derivations/ck1
cd $D
export PYTHONPATH=$D/src_ck1 TMPDIR=/dev/shm/tmp A48B_FOLD=frame2
PY=/home/user/Universe24/venv314/bin/python
nice -n 19 $PY ck1_run.py worlds/sea4_400.json out/r1_sea_checker_400.json back 10 lays worlds/lay_b.json > out/r1.log 2>&1 &
nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r2_parity_sea_400.json back 10 lays worlds/lay_ps.json > out/r2.log 2>&1 &
CK1_CROSS=1 nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r2b_parity_sea_cross_400.json back 10 lays worlds/lay_ps.json > out/r2b.log 2>&1 &
nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r3_parity_checker_400.json back 10 lays worlds/lay_ps_b.json > out/r3.log 2>&1 &
wait
MA1_ODD=2 CK1_CROSS=1 nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r3b_parity_checker_odd_cross_400.json back 10 lays worlds/lay_ps_b.json > out/r3b.log 2>&1 &
nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r4_nosea_checker_400.json back 10 lays worlds/lay_b_nosea.json > out/r4.log 2>&1 &
MA1_ODD=2 nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r5_nosea_checker_odd_400.json back 10 lays worlds/lay_b_nosea.json > out/r5.log 2>&1 &
MA1_ODD=2 CK1_CROSS=1 nice -n 19 $PY ck1_run.py worlds/empty4_400.json out/r6_nosea_checker_odd_cross_400.json back 10 lays worlds/lay_b_nosea.json > out/r6.log 2>&1 &
wait
echo done > out/run_all.done
