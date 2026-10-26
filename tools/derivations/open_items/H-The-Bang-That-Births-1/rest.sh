#!/bin/sh
set -e
P=/home/user/Universe24/venv314/bin/python
D="$1"; W="$2"; K="$3"; O=/dev/shm/tmp/bb1
export PYTHONPATH="$W/src" TMPDIR=/dev/shm/tmp
cd "$O"
echo "== the period law: the fourth form at the count 500,000"
nice -n 19 $P -m event_universe.run "$D/worlds/b11_sea_q500000_800.json" "$O/b11.json" back 20 > "$O/b11.out" 2>&1
nice -n 19 $P "$D/read_record.py" "$O/b11.json" "$D/out/b11_sea_q500000_800.tsv" 1
echo "== the width past the freeze: the fifth form at the count 2,500,000 to 40"
nice -n 19 $P -m event_universe.run "$D/worlds/b5_cyc_q2500000_40.json" "$O/b5.json" back 20 > "$O/b5.out" 2>&1
nice -n 19 $P "$D/read_record.py" "$O/b5.json" "$D/out/b5_cyc_q2500000_40.tsv" 1
echo "== the gates on the decisive record (the fifth form at 700,000)"
nice -n 19 $P -m event_universe.decoder "$O/b8_cyc_q700000_40.json" > "$D/out/b8_gates.txt" 2>&1
echo "== the gates on the lead carried to 3,600"
nice -n 19 $P -m event_universe.decoder "$O/b1_sea_q50000_3600.json" > "$D/out/b1_gates.txt" 2>&1
echo "== the conserved form in full on the decisive record"
nice -n 19 $P "$K/conservation_check.py" "$O/b8_cyc_q700000_40.json" out "$D/out/b8_cons.json" > "$D/out/b8_cons.txt" 2>&1 || true
echo DONE
