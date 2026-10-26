#!/bin/sh
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf18/tools/derivations/open_items/H-Confirm-Build-18
export PYTHONPATH=$S/hands/vf18/src TMPDIR=/dev/shm/tmp
PY=/home/user/Universe24/venv314/bin/python
cd $S/hands/vf18
c() { name=$1; shift; nice -n 19 "$@" > $H/logs/check_$name.out 2>&1; echo "$name exit $?" >> $H/logs/checks_exit.txt; }
: > $H/logs/checks_exit.txt
c ruff $PY -m ruff check .
c format $PY -m ruff format --check .
c mypy $PY -m mypy
c record_code_shape $PY tools/record_code_shape.py
c engine_gates $PY tools/engine_gates.py
c tests_shape env CHECK_BASE=50c73c972 $PY tools/tests_shape.py
c documents_gates $PY tools/documents_gates.py
c kit_node $PY tools/derivations/conservations/conservation_check.py tests/worlds/world_node.json 20
c kit_chiral $PY tools/derivations/conservations/conservation_check.py tests/worlds/world_chiral.json 60
c test_rule3 $PY -m pytest -q tests/test_rule3.py
echo CHECKS_DONE >> $H/logs/checks_exit.txt
