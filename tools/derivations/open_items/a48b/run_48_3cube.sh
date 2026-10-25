#!/bin/sh
# a48b: the 48 on the chiral 3-cube at 30 under the flag off, lattice, ones (the copy's src)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=src_a48b TMPDIR=/dev/shm/tmp
A48B_FOLD= $PY a48b_48.py worlds/world_chiral_3_30.json 30 out/c48_chiral3_30_off.json > out/c48_chiral3_30_off.stdout 2>&1
A48B_FOLD=lattice $PY a48b_48.py worlds/world_chiral_3_30.json 30 out/c48_chiral3_30_lattice.json > out/c48_chiral3_30_lattice.stdout 2>&1
A48B_FOLD=ones $PY a48b_48.py worlds/world_chiral_3_30.json 30 out/c48_chiral3_30_ones.json > out/c48_chiral3_30_ones.stdout 2>&1
echo done > out/run_48_3cube.done
