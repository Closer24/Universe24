P=/home/user/Universe24/venv314/bin/python
K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit
D=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/cm2/tools/derivations/open_items/H-The-Close-One-Moment-2
export TMPDIR=/dev/shm/tmp
cd /dev/shm/tmp/cm2
PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 $P $D/compare.py /dev/shm/tmp/cm2/head_world_hole.json /dev/shm/tmp/cm2/one_hole.json > $D/out/cmp_head_one_hole.json 2>&1
PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 $P $D/moment_split.py /dev/shm/tmp/cm2/one_hole.json /dev/shm/tmp/cm2/one_nature.json > $D/out/moment_split_flag.json 2>&1
PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 nice -n 19 $P -m event_universe.decoder /dev/shm/tmp/cm2/head_world_hole.json > $D/out/gates_head_hole.txt 2>&1
PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 nice -n 19 $P -m event_universe.decoder /dev/shm/tmp/cm2/one_hole.json > $D/out/gates_one_hole.txt 2>&1
PYTHONPATH=/dev/shm/tmp/cm2/src_cm2 ONE_MOMENT=1 nice -n 19 $P $K/conservation_check.py /dev/shm/tmp/cm2/one_hole.json out $D/out/cons_one_hole.json > $D/out/cons_one_hole.txt 2>&1
echo TAILDONE
