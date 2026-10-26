#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; K="$3"; O=/dev/shm/tmp/bb1
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd "$O"
echo "== the gates on the lead carried to 3,600"
nice -n 19 $P -m event_universe.gates "$O/b1_sea_q50000_3600.json" > "$D/out/b1_gates.txt" 2>&1 || echo "gates failed"
echo "== the flagged copy, the gate's width alone, the flag empty bit for bit"
nice -n 19 $P "$K/make_flagged_copy.py" bb1 BB1_STATE_WIDTH "$D/flag_width.json" src "$W/src" worlds "$W/tests/worlds/world_hole.json,$W/tests/worlds/world_nature.json" python "$P" > "$D/out/flag_check.txt" 2>&1 || echo "flag check nonzero"
echo "== the gate's width raised on the parted record"
PYTHONPATH=/dev/shm/tmp/bb1/src_bb1 BB1_STATE_WIDTH=1024 nice -n 19 $P -m event_universe.gates "$O/b5.json" > "$D/out/b5_gates_1024.txt" 2>&1 || echo "raised gates failed"
PYTHONPATH=/dev/shm/tmp/bb1/src_bb1 nice -n 19 $P -m event_universe.gates "$O/b5.json" > "$D/out/b5_gates_128.txt" 2>&1 || echo "empty-flag gates failed"
echo DONE
