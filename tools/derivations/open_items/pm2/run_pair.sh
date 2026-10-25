#!/bin/sh
# pm2: one record under the default src and under the flagged copy; $1 the world's file name, $2 the tag
ROOT=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/pm2
P=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
cd $ROOT/tools/derivations/pm2
PYTHONPATH=$ROOT/src $P -m event_universe.run worlds/$1 out/$2_default.json back 10 > out/$2_default.txt 2>&1 &
PYTHONPATH=$ROOT/tools/derivations/pm2/src_pm2 $P -m event_universe.run worlds_flag/$1 out/$2_flag.json back 10 > out/$2_flag.txt 2>&1 &
wait
echo done $2
