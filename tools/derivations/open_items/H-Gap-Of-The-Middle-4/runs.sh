#!/bin/sh
# the measurement runs of hand g4 (each one process, no loop), PYTHONPATH the worktree's src
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONPATH="$PWD/src" TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
D=tools/derivations/open_items/H-Gap-Of-The-Middle-4
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 --run-back > $D/log_well_q25.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 1 --intervals 200 --run-back > $D/log_well_q1.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode flat --depth 75 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 --run-back > $D/log_flat_q25.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode pair --depth 0 --separation 3 --senses 1,1 --sigma-tenths 12 --quanta 25 --intervals 300 --run-back > $D/log_pair_pp.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode pair --depth 0 --separation 3 --senses 1,-1 --sigma-tenths 12 --quanta 25 --intervals 300 --run-back > $D/log_pair_pm.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode clock --depth 0 --offset 0 --sigma-tenths 20 --quanta 25 --intervals 200 > $D/log_clock_c0.txt 2>&1 &
$PY $D/fall.py --den 348893 --g 0.74 --cube 9 --mode clock --depth 300 --offset 0 --sigma-tenths 20 --quanta 25 --intervals 200 > $D/log_clock_c300.txt 2>&1 &
$PY $D/fall.py --den 15162856759112389 --g 0.83 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 --run-back > $D/log_well_control54.txt 2>&1 &
$PY $D/fall.py --den 193253 --g 0.657 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 > $D/log_well_g657.txt 2>&1 &
$PY $D/fall.py --den 546037 --g 0.931 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 > $D/log_well_g931.txt 2>&1 &
$PY $D/fall.py --den 6485 --g 0.4 --cube 9 --mode well --depth 300 --offset 3 --sigma-tenths 12 --quanta 25 --intervals 200 > $D/log_well_g400.txt 2>&1 &
wait
echo ALL DONE
