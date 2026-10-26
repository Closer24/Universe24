#!/bin/bash
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf2
F=$W/tools/derivations/open_items/H-Matter-From-The-Floor-2
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
P=/home/user/Universe24/venv314/bin/python
S=/dev/shm/tmp/mf2/src_mf2
export PYTHONPATH=$S TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/mf2
cp $F/worlds/*.json /dev/shm/tmp/mf2/
date -u > chain.log
$P $K/wait_load.py 3 >> chain.log
MF2_DIGITS=1 nice -n 19 $P -m event_universe.run world_ga2_450.json ga2_450_digits.json back 10 > ga2_450_digits.stdout 2>&1
date -u >> chain.log; echo ga2_base >> chain.log
MF2_DIGITS=1 nice -n 19 $P -m event_universe.run world_chiral_60.json chiral_60_digits.json back 20 > chiral_60_digits.stdout 2>&1
MF2_DIGITS=1 nice -n 19 $P -m event_universe.run world_hole_60.json hole_60_digits.json back 20 > hole_60_digits.stdout 2>&1
date -u >> chain.log; echo chiral_hole >> chain.log
MF2_DIGITS=1 MF2_COVARIANT=1 nice -n 19 $P -m event_universe.run world_ga2_450.json ga2_450_cov.json back 10 > ga2_450_cov.stdout 2>&1
date -u >> chain.log; echo ga2_cov >> chain.log
MF2_DIGITS=1 nice -n 19 $P -m event_universe.run world_ga2_450_cz3.json ga2_450_cz3.json back 10 > ga2_450_cz3.stdout 2>&1
date -u >> chain.log; echo ga2_cz3 >> chain.log
MF2_DIGITS=1 MF2_COVARIANT=1 nice -n 19 $P -m event_universe.run world_chiral_60.json chiral_60_cov.json back 20 > chiral_60_cov.stdout 2>&1
date -u >> chain.log; echo chiral_cov >> chain.log
$P $K/wait_load.py 3 >> chain.log
MF2_COVARIANT=1 nice -n 19 $P $K/clicks_48.py world_chiral_60.json 60 c48_chiral_cov_cube3.json cube 3 > c48_chiral_cov_cube3.stdout 2>&1
date -u >> chain.log; echo c48_cov >> chain.log
MF2_DIGITS=1 nice -n 19 $P -m event_universe.run world_ga2_450_px.json ga2_450_px.json back 10 > ga2_450_px.stdout 2>&1
date -u >> chain.log; echo ga2_px >> chain.log
nice -n 19 $P $K/conservation_check.py ga2_450_digits.json board off out cons_ga2_450_digits.json > cons_ga2_450_digits.stdout 2>&1
nice -n 19 $P $K/conservation_check.py ga2_450_cov.json board off out cons_ga2_450_cov.json > cons_ga2_450_cov.stdout 2>&1
date -u >> chain.log; echo CHAIN_DONE >> chain.log
