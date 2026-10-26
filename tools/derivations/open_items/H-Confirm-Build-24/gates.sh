#!/bin/bash
# the seven gates at a worktree: $1 the worktree, $2 the log
W=$1; L=$2
PY=/home/user/Universe24/venv314/bin/python
export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp CHECK_BASE=6703dd95c
cd $W
{
echo "== gates at $W $(git rev-parse --short HEAD) $(date -u)"
echo "-- ruff check"; nice -n 19 $PY -m ruff check . ; echo "exit $?"
echo "-- ruff format --check"; nice -n 19 $PY -m ruff format --check . ; echo "exit $?"
echo "-- mypy"; nice -n 19 $PY -m mypy 2>&1 | tail -5 ; echo "exit ${PIPESTATUS[0]}"
echo "-- engine_gates"; nice -n 19 $PY tools/engine_gates.py 2>&1 | tail -5; echo "exit ${PIPESTATUS[0]}"
echo "-- record_code_shape"; nice -n 19 $PY tools/record_code_shape.py 2>&1 | tail -5; echo "exit ${PIPESTATUS[0]}"
echo "-- tests_shape"; nice -n 19 $PY tools/tests_shape.py 2>&1 | tail -5; echo "exit ${PIPESTATUS[0]}"
echo "-- documents_gates"; nice -n 19 $PY tools/documents_gates.py 2>&1 | tail -5; echo "exit ${PIPESTATUS[0]}"
echo "== done $(date -u)"
} > $L 2>&1
