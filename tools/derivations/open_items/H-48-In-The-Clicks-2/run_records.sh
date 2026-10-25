#!/bin/sh
# a48b: the records (chiral 300, hole 60, bodies 120) under the flag off and lattice, the run back 10
cd "$(dirname "$0")/worlds"
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=../src_a48b TMPDIR=/dev/shm/tmp
A48B_FOLD= $PY -m event_universe.run world_hole_60.json ../out/rec_hole60_off.json back 10 > ../out/rec_hole60_off.stdout 2>&1
A48B_FOLD=lattice $PY -m event_universe.run world_hole_60.json ../out/rec_hole60_lattice.json back 10 > ../out/rec_hole60_lattice.stdout 2>&1
A48B_FOLD= $PY -m event_universe.run world_chiral_300.json ../out/rec_chiral300_off.json back 10 > ../out/rec_chiral300_off.stdout 2>&1
A48B_FOLD=lattice $PY -m event_universe.run world_chiral_300.json ../out/rec_chiral300_lattice.json back 10 > ../out/rec_chiral300_lattice.stdout 2>&1
A48B_FOLD= $PY -m event_universe.run world_bodies_120.json ../out/rec_bodies120_off.json back 10 > ../out/rec_bodies120_off.stdout 2>&1
A48B_FOLD=lattice $PY -m event_universe.run world_bodies_120.json ../out/rec_bodies120_lattice.json back 10 > ../out/rec_bodies120_lattice.stdout 2>&1
echo done > ../out/run_records.done
