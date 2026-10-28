#!/bin/bash
# One engine process at a time: wait while S/check.lock exists, take it with mkdir, run, release.
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
V=$S/derive/H_verify
PY=/home/user/Universe24/venv314/bin/python
STOP=$(date -u -d "14:31" +%s)
run_one() {
  while true; do
    if [ "$(date -u +%s)" -gt "$STOP" ]; then echo "skipped $* (time)" >> $V/v3_engine.log; return; fi
    if mkdir $S/check.lock 2>/dev/null; then
      echo "H_verify $(date -u +%H:%M:%S)" > $S/check.lock/owner
      echo "start $* $(date -u +%H:%M:%S)" >> $V/v3_engine.log
      timeout 600 $PY -I $V/v3_engine.py "$@" >> $V/v3_engine.jsonl 2>> $V/v3_engine.err
      echo "end $* $(date -u +%H:%M:%S) rc=$?" >> $V/v3_engine.log
      rm -rf $S/check.lock
      return
    fi
    sleep 10
  done
}
run_one FULL world_node.json 20
run_one WMIN world_node.json 20
run_one NORM world_hole.json 10
run_one HEAD world_hole.json 10
echo done >> $V/v3_engine.log
