#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; O=/dev/shm/tmp/bb1
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd "$O"
for n in 2500000 5000000 20000000 40000000; do
  b=b13_cyc_q${n}_24
  nice -n 19 $P -m event_universe.run "$D/worlds/$b.json" "$O/$b.json" back 10 > "$O/$b.out" 2>&1
  nice -n 19 $P -m event_universe.gates "$O/$b.json" > "$D/out/${b}_gates.txt" 2>&1
  nice -n 19 $P "$D/read_record.py" "$O/$b.json" "$D/out/$b.tsv" 1 > "$D/out/${b}_read.txt"
done
echo DONE
