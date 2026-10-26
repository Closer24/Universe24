#!/bin/sh
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cb26
D=$W/tools/derivations/open_items/H-Confirm-Build-26
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp/cb26
cd $W
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/wait_load.py 3 > $D/logs/wait_suite.txt 2>&1
nice -n 19 /home/user/Universe314/bin/true 2>/dev/null
nice -n 19 /home/user/Universe24/venv314/bin/python -m pytest -q -p no:cacheprovider -n 2 --junitxml=/dev/shm/tmp/cb26/junit.xml > $D/logs/pytest.out 2>&1
echo "exit $?" >> $D/logs/pytest.out
