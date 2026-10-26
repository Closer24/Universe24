#!/bin/sh
# After the v2 chain: the 48 on the chiral 5-cube (the file's shape) to 60 under v2, one record at a time.
P=/home/user/Universe24/venv314/bin/python
until grep -q DONE /dev/shm/tmp/lt2/v2.log; do sleep 20; done
export TMPDIR=/dev/shm/tmp PYTHONPATH=/dev/shm/tmp/lt2b/src_lt2b LT2_LAY_REVERSED=1
date -u > /dev/shm/tmp/lt2/v3.log
$P /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/wait_load.py 3 >> /dev/shm/tmp/lt2/v3.log
nice -n 19 $P /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/clicks_48.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/lt2/tests/worlds/world_nature.json 60 /dev/shm/tmp/lt2/c48_v2_cube5.json 2>&1 | tail -1 >> /dev/shm/tmp/lt2/v3.log
date -u >> /dev/shm/tmp/lt2/v3.log
echo DONE >> /dev/shm/tmp/lt2/v3.log
