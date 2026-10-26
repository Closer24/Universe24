#!/bin/bash
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mf1/src TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/mf1
date -u > base.log
nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run world_ga2_450.json ga2_450.json back 20 > ga2_450.stdout 2> ga2_450.stderr
date -u >> base.log
echo DONE >> base.log
