#!/bin/bash
# tests_shape.py at each commit of the range, in a throwaway worktree stepped through the commits
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
P=/home/user/Universe24/venv314/bin/python; T=/dev/shm/tmp/cb24/wt; L=/dev/shm/tmp/cb24/logs/ratchet.txt
export CHECK_BASE=6703dd95c TMPDIR=/dev/shm/tmp
git -C $S/hands/cb24 worktree add --detach $T 3d7729581 > /dev/null 2>&1
for c in 3d7729581 dfe53db5c 538137d91 5c44be40a d2f1f1658 caa39b681 5f9ba749f 62b754c09 1637d151d; do
  git -C $T checkout --detach -q $c; cd $T; export PYTHONPATH=$T/src
  echo "$c | tests_shape: $(nice -n 19 $P tools/tests_shape.py 2>&1 | tail -1 | cut -c1-160) | exit ${PIPESTATUS[0]} | tests lines $(cat tests/*.py | wc -l)" >> $L
done
git -C $S/hands/cb24 worktree remove --force $T; echo done >> $L
