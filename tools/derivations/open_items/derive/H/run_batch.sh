#!/bin/bash
# Draft H's engine batch: one engine process at a time; before each run, wait while S/check.lock exists.
S=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad
H=$S/derive/H
OUT=$H/$1
shift
VARIANTS="$1"
shift
for v in $VARIANTS; do
  for wt in "$@"; do
    w=${wt%:*}; t=${wt#*:}
    while [ -e $S/check.lock ]; do sleep 20; done
    /home/user/Universe24/venv314/bin/python -I $H/h_engine.py $v $w $t >> $OUT 2>> $OUT.err
  done
done
echo done >> $OUT.done
