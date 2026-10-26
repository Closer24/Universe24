#!/bin/bash
# vf11: every record at both shas, in parallel; the build's src at $W/src, the parent's at $D/parent/src
W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf11
D=$W/tools/derivations/open_items/H-Confirm-Build-11
PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
job() { # src tag world intervals script
  local src=$1 tag=$2 world=$3 n=$4 script=$5
  local base=$(basename $world .json)
  if [ "$script" = probe ]; then
    PYTHONPATH=$src nice -n 19 $PY $D/probe.py $W/tests/worlds/$world $D/out/${tag}_${base}.json $n > $D/out/${tag}_${base}.log 2>&1
  else
    PYTHONPATH=$src nice -n 19 $PY $D/plasma.py $W/tests/worlds/$world $n $D/out/${tag}_${base}_retrace.json > $D/out/${tag}_${base}_retrace.log 2>&1
  fi
  echo "done $tag $base $script $(date +%T)"
}
export -f job; export W D PY
mkdir -p $D/out
{
for tag_src in "b $W/src" "p $D/parent/src"; do
  set -- $tag_src
  for ws in "world_bodies.json 300" "world_universe.json 400" "world_plasma_3.json 400" "world_pair_3.json 400" "world_sea_3.json 240" "world_hole.json 60" "world_chiral.json 60"; do
    echo "$2 $1 $ws probe"
  done
  echo "$2 $1 world_plasma_3.json 400 plasma"
done
echo "$W/src b world_plasma.json 400 plasma"
} | xargs -P 4 -L 1 bash -c 'job $0 $1 $2 $3 $4'
echo "all done $(date +%T)"
