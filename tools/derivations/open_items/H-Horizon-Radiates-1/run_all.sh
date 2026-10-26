#!/bin/sh
# hr1: the chiral world to 8,000 under FR-S1's form (FR2_RELEASE=1 on the copy src_hr1), streamed; the fed one-Node world to 4,000 standing and risen (before 93 below); the run back 10; nice -n 19
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
export TMPDIR=/dev/shm/tmp
mkdir -p /dev/shm/tmp out
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
FR2_RELEASE=1 run chiral8000_f $PY hr1_stream.py src_hr1 $W/tests/worlds/world_chiral.json 8000 10 /dev/shm/tmp/hr1_chiral8000_f.jsonl &
FR2_RELEASE=1 run one_node_risen_4000 $PY hr1_one_node.py src_hr1 $W/tests/worlds/world_node.json 93 4000 10 out/one_node_risen_4000.jsonl &
FR2_RELEASE=1 run one_node_standing_4000 $PY hr1_one_node.py src_hr1 $W/tests/worlds/world_node.json 0 4000 10 out/one_node_standing_4000.jsonl &
wait
echo all > out/run_all.done
