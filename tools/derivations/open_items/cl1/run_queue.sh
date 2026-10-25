#!/bin/bash
# cl1's run queue: one run at a time, each named (no loop). Run from tools/derivations/cl1.
P=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cl1/src TMPDIR=/dev/shm/tmp
( time $P run_cl1.py worlds/world_single_d3.json out/single_d3.json back 10 > out/single_d3.txt 2>&1 ) 2> out/single_d3.time
( time $P run_cl1.py worlds/world_like_d6.json out/like_d6.json back 10 > out/like_d6.txt 2>&1 ) 2> out/like_d6.time
( time $P run_cl1.py worlds/world_opposite_d6.json out/opposite_d6.json back 10 > out/opposite_d6.txt 2>&1 ) 2> out/opposite_d6.time
( time $P run_cl1.py worlds/world_like_d3_Tdiv2.json out/like_d3_Tdiv2.json back 10 > out/like_d3_Tdiv2.txt 2>&1 ) 2> out/like_d3_Tdiv2.time
( time $P run_cl1.py worlds/world_opposite_d3_Tdiv2.json out/opposite_d3_Tdiv2.json back 10 > out/opposite_d3_Tdiv2.txt 2>&1 ) 2> out/opposite_d3_Tdiv2.time
echo done > out/queue_done.txt
