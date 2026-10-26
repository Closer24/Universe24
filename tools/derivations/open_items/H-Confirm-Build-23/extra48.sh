#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad; P=/home/user/Universe24/venv314/bin/python; K=$S/hands/kit; L=/dev/shm/tmp/cb23/logs
export TMPDIR=/dev/shm/tmp
until grep -q "all done" $L/chain.log; do sleep 10; done
$P $K/wait_load.py 3 >> $L/chain.log 2>&1
export PYTHONPATH=/dev/shm/tmp/cb23/tw/src; cd /dev/shm/tmp/cb23; s=$(date +%s)
nice -n 19 $P $K/clicks_48.py /dev/shm/tmp/cb23/tw/tests/worlds/world_nature.json 60 /dev/shm/tmp/cb23/clicks48_chiral3_tw.json cube 3 > $L/clicks48_tw.out 2>&1
echo "clicks48 at 853582d7b (the tw worktree) exit $? $(( $(date +%s) - s )) s" >> $L/runs.txt; echo "[$(date +%H:%M:%S)] extra48 done" >> $L/chain.log
