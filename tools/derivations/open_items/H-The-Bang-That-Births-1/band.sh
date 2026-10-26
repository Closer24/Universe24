#!/bin/sh
# The band's edge on the fifth form: the first birth round's count of Nodes at each count.
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"
O=/dev/shm/tmp/bb1
export PYTHONPATH="$2/src" TMPDIR=/dev/shm/tmp
cd "$O"
for w in "$D"/worlds/b2_cyc_q*_24.json; do
  b=$(basename "$w" .json)
  nice -n 19 $P -m event_universe.run "$w" "$O/$b.json" back 10 > "$O/$b.out" 2>&1 || echo "FAILED $b"
  nice -n 19 $P "$D/read_record.py" "$O/$b.json" "$D/out/$b.tsv" 1 >> "$D/out/band_readings.txt"
done
