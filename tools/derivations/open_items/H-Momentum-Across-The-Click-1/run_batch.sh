#!/bin/bash
# mk1: every world under the flagged copy (f), the copy unflagged (n) and the head's src (h), in parallel
H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mk1/tools/derivations/open_items/H-Momentum-Across-The-Click-1; W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mk1; PY=/home/user/Universe24/venv314/bin/python
export TMPDIR=/dev/shm/tmp
job() { # tag world intervals back
  local tag=$1 world=$2 n=$3 back=$4 base src flag
  base=$(basename $world .json)
  case $tag in f) src=$H/src_mk1; flag=1;; n) src=$H/src_mk1; flag=;; h) src=$W/src; flag=;; esac
  MK1_RECOIL=$flag PYTHONPATH=$src nice -n 19 $PY $H/probe_mk1.py $world $n $back $H/out/${tag}_${base}_${n}.json > $H/out/${tag}_${base}_${n}.log 2>&1
  echo "done $tag $base $n $(date +%T)"
}
export -f job; export H W PY
T=$W/tests/worlds
{
echo "f $T/world_hole.json 60 10"
echo "n $T/world_hole.json 60 10"
echo "h $T/world_hole.json 60 10"
echo "f $H/worlds/world_compton.json 60 10"
echo "n $H/worlds/world_compton.json 60 10"
echo "f $T/world_chiral.json 60 10"
echo "f $T/world_plasma_3.json 170 10"
echo "f $T/world_plasma_3.json 90 10"
echo "n $T/world_plasma_3.json 170 10"
echo "f $T/world_sea_3.json 240 10"
echo "n $T/world_sea_3.json 240 10"
echo "f $T/world_bodies.json 300 10"
echo "n $T/world_bodies.json 300 10"
echo "f $T/world_universe.json 400 10"
echo "n $T/world_universe.json 400 10"
} | xargs -P 6 -L 1 bash -c 'job $0 $1 $2 $3'
echo "all done $(date +%T)"
