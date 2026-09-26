#!/bin/bash
cd /tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad
PY=/home/user/Universe24/.venv/bin/python
for spec in "massive_record/light_clock.json 700 light=charge" "massive_record/boxed_clock_side_20_at_rest.json 120 light=charge" "dark_body/bright.json 150 light=charge" "toward_nature/lorentz_moving_long.json 300 light=charge" "point_emitter/point_light_clock.json 2500 light=charge point=matter"; do
  set -- $spec
  echo "== $1 $2 $(date -u +%T)"
  timeout 1800 $PY generic/bitwise_compare.py $1 $2 $3 $4 2>&1 | tail -4
done
echo "== done $(date -u +%T)"
