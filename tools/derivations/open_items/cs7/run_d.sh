#!/bin/sh
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cs7/tools/derivations/cs7
cd $D
export TMPDIR=/dev/shm/tmp
mkdir -p out/survey2
CS7_EQ=n nice -n 19 /home/user/Universe24/venv314/bin/python survey_cs7.py out/survey2 1 0,1 p hhga gahh hgahg > out/survey_pairs.txt 2>&1
echo done > out/run_d.done
