#!/bin/sh
# a48: the second chain, one run at a time: the flags off bit for bit again (the exchange edited), then the 48 on the clicks
# under A48_READ=even A48_SWAP=half on the chiral 3-cube at 30 and the 5-cube at 24, then the hole 60 and the chiral 300
# under both flags with back 10 and the gates.
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
CP=src_a48
SRC=../../../src
PYTHONPATH=$CP $P -m event_universe.run worlds/chiral_5cube_24.json out/chiral5_24_copy_off2.json back 10 > out/copy_off2.txt 2>&1
echo "PREDICTION both flags 3-cube 30: 24 equal / 24 with the ends and senses exchanged / 0 apart on the births and the clicks" > out/c48_both_3cube30.txt
A48_READ=even A48_SWAP=half PYTHONPATH=$CP:. $P a48_48.py worlds/chiral_3cube_30.json 3 30 out/c48_both_3cube30.json >> out/c48_both_3cube30.txt 2>&1
echo "PREDICTION both flags 5-cube 24: 24 / 24 / 0 on the births and the clicks" > out/c48_both_5cube24.txt
A48_READ=even A48_SWAP=half PYTHONPATH=$CP:. $P a48_48.py worlds/chiral_5cube_24.json 5 24 out/c48_both_5cube24.json >> out/c48_both_5cube24.txt 2>&1
echo "PREDICTION records under both flags: the run back 10 of 10; the charge 0 at every birth; taken >= booked; the counts change from the engine's" > out/records_both.txt
A48_READ=even A48_SWAP=half PYTHONPATH=$CP $P -m event_universe.run worlds/world_hole.json out/hole60_both.json back 10 >> out/records_both.txt 2>&1
A48_READ=even A48_SWAP=half PYTHONPATH=$CP $P -m event_universe.run worlds/world_chiral_300.json out/chiral300_both.json back 10 >> out/records_both.txt 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/chiral300_both.json > out/gates_chiral300_both.jsonl 2>&1
PYTHONPATH=$SRC $P -m event_universe.gates out/hole60_both.json > out/gates_hole60_both.jsonl 2>&1
echo CHAIN2 DONE > out/chain2_done.txt
