#!/bin/sh
# bg1: the three records on the engine's default (src), back 10; prediction written in the report before the run
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bg1
P=/home/user/Universe24/venv314/bin/python
cd $W/tools/derivations/bg1
export TMPDIR=/dev/shm/tmp
$P diag.py worlds/world_chiral.json out/chiral2400_default.jsonl intervals 2400 back 10 > out/chiral2400_default.log 2>&1 &
$P diag.py worlds/world_collapse_800.json out/collapse800_default.jsonl intervals 400 back 10 > out/collapse800_default.log 2>&1 &
$P diag.py worlds/world_bodies.json out/bodies120_default.jsonl intervals 120 back 10 > out/bodies120_default.log 2>&1 &
wait
echo DONE
