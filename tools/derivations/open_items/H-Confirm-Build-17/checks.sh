#!/bin/sh
cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17; export PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python; L=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf17/tools/derivations/open_items/H-Confirm-Build-17/logs
r() { n=$1; shift; nice -n 19 "$@" > $L/check_$n.out 2>&1; echo "exit $?" >> $L/check_$n.out; }
r ruff_check $PY -m ruff check .
r ruff_format $PY -m ruff format --check .
r shape $PY tools/record_code_shape.py
r engine_gates $PY tools/engine_gates.py
CHECK_BASE=50c73c972 r tests_shape $PY tools/tests_shape.py
r documents_gates $PY tools/documents_gates.py
r mypy $PY -m mypy
echo CHECKS DONE > $L/CHECKS_DONE
