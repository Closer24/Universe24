#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
H=$S/hands/vf16/tools/derivations/open_items/H-Confirm-Build-16
cd $S/hands/vf16; export PYTHONPATH=$S/hands/vf16/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python; V=/home/user/Universe24/venv314/bin
run() { local n=$1; shift; nice -n 19 "$@" > $H/logs/check_$n.txt 2>&1; echo "$n exit $?" >> $H/logs/checks_exit.txt; }
run ruff_check $V/ruff check .
run ruff_format $V/ruff format --check .
run mypy $V/mypy
run record_code_shape $PY tools/record_code_shape.py
run engine_gates $PY tools/engine_gates.py
CHECK_BASE=6a482bffb run tests_shape env CHECK_BASE=6a482bffb $PY tools/tests_shape.py
run documents_gates $PY tools/documents_gates.py
echo CHECKS_DONE >> $H/logs/checks_exit.txt
