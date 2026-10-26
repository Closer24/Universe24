#!/bin/sh
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cb26
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp/cb26 CHECK_BASE=6703dd95c
P=/home/user/Universe24/venv314/bin/python
cd $W
echo "--- ruff check"; nice -19 $W/../../../../../../../home/user/Universe24/venv314/bin/ruff check . 2>&1 | tail -3; echo "exit $?"
