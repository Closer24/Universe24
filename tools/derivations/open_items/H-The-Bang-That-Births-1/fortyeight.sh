#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; K="$3"; O=/dev/shm/tmp/bb1
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd "$O"
nice -n 19 $P "$K/clicks_48.py" "$D/worlds/b17_cyc_q12000000_16.json" 16 "$D/out/b17_48.json" cube 4 > "$D/out/b17_48.txt" 2>&1 || echo "48 nonzero"
tail -4 "$D/out/b17_48.txt"
echo DONE48
