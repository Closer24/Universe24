#!/bin/sh
# rl2: the 48 on the chiral 3-cube to 60 under each form, two at a time beside the record queue
cd "$(dirname "$0")"
export TMPDIR=/dev/shm/tmp
O=/dev/shm/tmp/rl2/out
n=0
while IFS= read -r cmd; do n=$((n+1)); echo "nice -n 19 env $cmd > $O/c48q$n.stdout 2> $O/c48q$n.stderr; echo done > $O/c48q$n.done"; done < $O/queue48.txt | xargs -P 2 -I{} sh -c '{}'
echo all > $O/run_48s.done
