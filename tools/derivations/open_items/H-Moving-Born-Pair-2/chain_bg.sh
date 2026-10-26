#!/bin/sh
# H-Moving-Born-Pair-2's background chain, one run at a time: the bodies 120 under the flag, the bodies 120 with the flag empty (the head), the measurement world on the 5-cube at the third lift under the flag, the 48 on the chiral 3-cube under the flag.
export TMPDIR=/dev/shm/tmp PYTHONPATH=/dev/shm/tmp/mb2/src_mb2
cd /dev/shm/tmp/mb2
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb2/tools/derivations/open_items/H-Kit-48-Re-Cut-1/wait_load.py 3
MB_S1=1 HQ_S1=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/world_bodies_120.json /dev/shm/tmp/mb2/mb_bodies_120.json back 20 > mb_bodies_120.out 2>&1
echo bodies_flag_done
nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/world_bodies_120.json /dev/shm/tmp/mb2/head_bodies_120.json back 20 > head_bodies_120.out 2>&1
echo bodies_head_done
MB_S1=1 HQ_S1=1 nice -n 19 /home/user/Universe24/venv314/bin/python -m event_universe.run /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb2/tools/derivations/open_items/H-Quartet-Carriage-2/worlds/world_measure5_60_lift3.json /dev/shm/tmp/mb2/mb_measure5_60_lift3.json back 20 > mb_measure5_60_lift3.out 2>&1
echo measure_done
/home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb2/tools/derivations/open_items/H-Kit-48-Re-Cut-1/wait_load.py 3
MB_S1=1 HQ_S1=1 nice -n 19 /home/user/Universe24/venv314/bin/python /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb2/tools/derivations/open_items/H-Kit-48-Re-Cut-1/clicks_48.py /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mb2/tools/derivations/open_items/H-Moving-Born-Pair-2/worlds/world_chiral3_60_lift3.json 60 /dev/shm/tmp/mb2/c48_mb_chiral3_60_lift3.json cube 3 > c48_mb_chiral3_60_lift3.out 2>&1
echo c48_done
