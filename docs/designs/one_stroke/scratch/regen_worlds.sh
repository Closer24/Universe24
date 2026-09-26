#!/bin/bash
cd /tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad/wt_ec
export PYTHONPATH=src
PY=/home/user/Universe24/.venv/bin/python
echo "== massive_record $(date -u +%T)"; $PY examples/events/massive_record/make_worlds.py 2>&1 | tail -3
echo "== toward_nature $(date -u +%T)"; $PY examples/events/toward_nature/make_worlds.py 2>&1 | tail -3
echo "== dark_body $(date -u +%T)"; $PY examples/events/dark_body/make_worlds.py 2>&1 | tail -3
echo "== point_emitter $(date -u +%T)"; $PY examples/events/point_emitter/make_worlds.py 2>&1 | tail -3
echo "== done $(date -u +%T)"
echo "== light clock $(date -u +%T)"; $PY ../generic/regen_light_clock.py 2>&1 | tail -3
echo "== all done $(date -u +%T)"
