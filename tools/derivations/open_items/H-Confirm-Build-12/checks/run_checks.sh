#!/bin/sh
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12
export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
C=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/checks
for t in engine_gates record_code_shape tests_shape documents_gates; do nice -n 19 $PY tools/$t.py > $C/$t.log 2>&1; echo "exit=$?" >> $C/$t.log; done
nice -n 19 ruff check . > $C/ruff_check.log 2>&1; echo "exit=$?" >> $C/ruff_check.log
nice -n 19 ruff format --check . > $C/ruff_format.log 2>&1; echo "exit=$?" >> $C/ruff_format.log
nice -n 19 $PY -m mypy > $C/mypy.log 2>&1; echo "exit=$?" >> $C/mypy.log
echo done > $C/done
