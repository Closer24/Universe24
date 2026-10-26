#!/bin/bash
# mk2: every world under the flagged copy (f), the copy unflagged (n); the head's hole 60 stands in the record cache
H=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mk2/tools/derivations/open_items/H-Momentum-Across-The-Click-2; W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/mk2; PY=/home/user/Universe24/venv314/bin/python; R=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/ebf595808
export TMPDIR=/dev/shm/tmp
job() { local tag=$1 world=$2 n=$3 back=$4 base flag; base=$(basename $world .json)
  case $tag in f) flag=1;; n) flag=;; esac
  MK2_RECOIL=$flag PYTHONPATH=$H/src_mk2 nice -n 19 $PY $H/probe_mk2.py run $world $n $back $H/out/${tag}_${base}_${n}.json > $H/out/${tag}_${base}_${n}.log 2>&1
  echo "done $tag $base $n $(date -u +%T)"; }
export -f job; export H W PY
T=$W/tests/worlds
{
echo "f $T/world_hole.json 60 10"
echo "n $T/world_hole.json 60 10"
echo "f $T/world_chiral.json 60 10"
echo "f $H/worlds/world_compton.json 60 10"
echo "n $H/worlds/world_compton.json 60 10"
echo "f $H/worlds/world_two_packets.json 60 10"
echo "f $T/world_plasma_3.json 170 10"
echo "f $T/world_sea_3.json 240 10"
echo "f $T/world_universe.json 400 10"
echo "f $T/world_bodies.json 300 10"
} | xargs -P 4 -L 1 bash -c 'job $0 $1 $2 $3'
echo "all done $(date -u +%T)"
