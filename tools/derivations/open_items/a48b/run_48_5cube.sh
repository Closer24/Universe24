#!/bin/sh
# a48b: the 48 on the chiral 5-cube at 24 under the flag off, lattice, ones (the copy's src); the state tracking off for speed on lattice and ones
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=src_a48b TMPDIR=/dev/shm/tmp
A48B_FOLD=lattice $PY a48b_48.py worlds/world_chiral_5_24.json 24 out/c48_chiral5_24_lattice.json notrack > out/c48_chiral5_24_lattice.stdout 2>&1
A48B_FOLD= $PY a48b_48.py worlds/world_chiral_5_24.json 24 out/c48_chiral5_24_off.json notrack > out/c48_chiral5_24_off.stdout 2>&1
A48B_FOLD=ones $PY a48b_48.py worlds/world_chiral_5_24.json 24 out/c48_chiral5_24_ones.json notrack > out/c48_chiral5_24_ones.stdout 2>&1
echo done > out/run_48_5cube.done
