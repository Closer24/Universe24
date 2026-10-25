#!/bin/sh
# a48: the measurement chain, one run at a time (no loops): the 48 on the clicks under the engine and under the flagged copy
# (A48_READ=even) on the chiral 3-cube at 30 and the 5-cube at 24; then the three records under the flag with back 10 and
# the gates. Run from tools/derivations/open_items/H-48-In-The-Clicks-1 with TMPDIR=/dev/shm/tmp.
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
SRC=../../../src
CP=src_a48
echo "PREDICTION engine 3-cube 30: births few, all in one close before any im line is nonzero: 24 equal / 24 exchanged / 0 apart on births and clicks; pm2's senses-alone read: 24 / 0 / 24 by construction" > out/c48_engine_3cube30.txt
PYTHONPATH=$SRC:. $P a48_48.py worlds/chiral_3cube_30.json 3 30 out/c48_engine_3cube30.json >> out/c48_engine_3cube30.txt 2>&1
echo "PREDICTION engine 5-cube 24: births 14 over several closes: 24 rotations equal (the odd lines' digits do not fall differently) / reflections 0 exchanged / 24 apart, the first apart birth after interval 6 at a Node within one Link of a laid im level" > out/c48_engine_5cube24.txt
PYTHONPATH=$SRC:. $P a48_48.py worlds/chiral_5cube_24.json 5 24 out/c48_engine_5cube24.json >> out/c48_engine_5cube24.txt 2>&1
echo "PREDICTION copy even 3-cube 30: 24 / 24 / 0 (the record may change: the digits are read even)" > out/c48_even_3cube30.txt
A48_READ=even PYTHONPATH=$CP:. $P a48_48.py worlds/chiral_3cube_30.json 3 30 out/c48_even_3cube30.json >> out/c48_even_3cube30.txt 2>&1
echo "PREDICTION copy even 5-cube 24: 24 rotations equal / 24 reflections with the senses exchanged / 0 apart on the births and the clicks (the residual: a digit at a turned Node's C-odd line off by 2 in the distance, flipping a digit with the chance 2 / F, F above 2^60: none expected)" > out/c48_even_5cube24.txt
A48_READ=even PYTHONPATH=$CP:. $P a48_48.py worlds/chiral_5cube_24.json 5 24 out/c48_even_5cube24.json >> out/c48_even_5cube24.txt 2>&1
echo "PREDICTION records under the even read: the run back 10 of 10 on each; the births change in count (the digits differ); the charge 0 at every birth; taken >= booked" > out/records_even.txt
A48_READ=even PYTHONPATH=$CP $P -m event_universe.run worlds/world_hole.json out/hole60_even.json back 10 >> out/records_even.txt 2>&1
PYTHONPATH=$SRC $P -m event_universe.run worlds/world_hole.json out/hole60_engine.json back 10 >> out/records_engine.txt 2>&1
A48_READ=even PYTHONPATH=$CP $P -m event_universe.run worlds/world_chiral_300.json out/chiral300_even.json back 10 >> out/records_even.txt 2>&1
PYTHONPATH=$SRC $P -m event_universe.run worlds/world_chiral_300.json out/chiral300_engine.json back 10 >> out/records_engine.txt 2>&1
A48_READ=even PYTHONPATH=$CP $P -m event_universe.run worlds/world_bodies_120.json out/bodies120_even.json back 10 >> out/records_even.txt 2>&1
PYTHONPATH=$SRC $P -m event_universe.run worlds/world_bodies_120.json out/bodies120_engine.json back 10 >> out/records_engine.txt 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/chiral300_even.json > out/gates_chiral300_even.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/chiral300_engine.json > out/gates_chiral300_engine.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/hole60_even.json > out/gates_hole60_even.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/hole60_engine.json > out/gates_hole60_engine.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/bodies120_even.json > out/gates_bodies120_even.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/bodies120_engine.json > out/gates_bodies120_engine.jsonl 2>&1
echo CHAIN DONE > out/chain_done.txt
