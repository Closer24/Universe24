#!/bin/sh
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/bg1
P=/home/user/Universe24/venv314/bin/python
cd $W/tools/derivations/bg1
export TMPDIR=/dev/shm/tmp
$P diag.py worlds/world_sea3.json out/sea3_default.jsonl back 10 > out/sea3_default.log 2>&1
for_each() { :; }
$P diag.py worlds/world_chiral.json out/chiral2400_a.jsonl intervals 2400 back 10 flag a > out/chiral2400_a.log 2>&1 &
$P diag.py worlds/world_chiral.json out/chiral2400_b.jsonl intervals 2400 back 10 flag b > out/chiral2400_b.log 2>&1 &
$P diag.py worlds/world_chiral.json out/chiral2400_c.jsonl intervals 2400 back 10 flag c > out/chiral2400_c.log 2>&1 &
$P diag.py worlds/world_chiral.json out/chiral2400_d.jsonl intervals 2400 back 10 flag d > out/chiral2400_d.log 2>&1 &
wait
$P diag.py worlds/world_collapse_800.json out/collapse800_a.jsonl intervals 400 back 10 flag a > out/collapse800_a.log 2>&1 &
$P diag.py worlds/world_collapse_800.json out/collapse800_b.jsonl intervals 400 back 10 flag b > out/collapse800_b.log 2>&1 &
$P diag.py worlds/world_collapse_800.json out/collapse800_c.jsonl intervals 400 back 10 flag c > out/collapse800_c.log 2>&1 &
$P diag.py worlds/world_collapse_800.json out/collapse800_d.jsonl intervals 400 back 10 flag d > out/collapse800_d.log 2>&1 &
wait
$P diag.py worlds/world_bodies.json out/bodies120_a.jsonl intervals 120 back 10 flag a > out/bodies120_a.log 2>&1 &
$P diag.py worlds/world_bodies.json out/bodies120_b.jsonl intervals 120 back 10 flag b > out/bodies120_b.log 2>&1 &
$P diag.py worlds/world_bodies.json out/bodies120_c.jsonl intervals 120 back 10 flag c > out/bodies120_c.log 2>&1 &
$P diag.py worlds/world_bodies.json out/bodies120_d.jsonl intervals 120 back 10 flag d > out/bodies120_d.log 2>&1 &
wait
$P diag.py worlds/world_sea3.json out/sea3_b.jsonl back 10 flag b > out/sea3_b.log 2>&1 &
$P diag.py worlds/world_sea3.json out/sea3_d.jsonl back 10 flag d > out/sea3_d.log 2>&1 &
$P diag.py worlds/world_sea3.json out/sea3_a.jsonl back 10 flag a > out/sea3_a.log 2>&1 &
wait
echo DONE
