#!/bin/sh
# hr2: the chiral world to 8,000 under FR-S1's form (the flag on), the run back 10; the fed one-Node world (world_node.json, the centre fed to the frozen content 3,793 with its before at 3,700 and at 3,780) to 4,000, the run back 10; streamed per interval to out/*.jsonl
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
export TMPDIR=/dev/shm/tmp
export PYTHONPATH=$PWD/src_hr2
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
FR2_RELEASE=1 run chiral_8000 $PY hr2_stream.py src_hr2 $W/tests/worlds/world_chiral.json 8000 10 out/chiral_8000.jsonl out/chiral_8000.json &
FR2_RELEASE=1 run one_node_3700_4000 $PY hr2_stream.py src_hr2 $W/tests/worlds/world_node.json 4000 10 out/one_node_3700_4000.jsonl out/one_node_3700_4000.json 3793 3700 &
FR2_RELEASE=1 run one_node_3780_4000 $PY hr2_stream.py src_hr2 $W/tests/worlds/world_node.json 4000 10 out/one_node_3780_4000.jsonl out/one_node_3780_4000.json 3793 3780 &
wait
echo all > out/run_all.done
