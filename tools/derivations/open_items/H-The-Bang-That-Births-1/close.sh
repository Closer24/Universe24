#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; K="$3"; O=/dev/shm/tmp/bb1
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd "$O"
echo "== the conserved form in full on the decisive record b14"
nice -n 19 $P "$K/conservation_check.py" "$O/b14_cyc_q5000000_240.json" out "$D/out/b14_cons.json" > "$D/out/b14_cons.txt" 2>&1 || true
tail -2 "$D/out/b14_cons.txt"
echo "== the one-Link reach on the decisive seed"
nice -n 19 $P "$K/reach.py" "$D/worlds/b14_cyc_q5000000_240.json" 6 0,0,0 5 "$D/out/b14_reach.json" cube 4 > "$D/out/b14_reach.txt" 2>&1 || echo "reach nonzero"
tail -3 "$D/out/b14_reach.txt"
echo DONE1
