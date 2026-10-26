#!/bin/sh
# bg1: every measurement under nice; the flags FR2_RELEASE and BG1_FORM from the environment (unset: the head bit for bit)
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
W=../../../..
S=../../../../../..
R=$S/records/2ab32b518
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo done > out/$out.done; }
( FR2_RELEASE=1 BG1_FORM=1 run chiral3000_form $PY bg1_probe.py src_bg1 $W/tests/worlds/world_chiral.json 3000 10 out/chiral3000_form.jsonl ) &
( FR2_RELEASE=1 BG1_FORM=1 run node400_form $PY bg1_probe.py src_bg1 $W/tests/worlds/world_node.json 400 10 out/node400_form.jsonl 4268834097 2560000000 ) &
( for r in universe_400 pair_3_400 plasma_3_170 ga2_450 hole_60 chiral_60 bodies_300; do FR2_RELEASE=1 BG1_FORM=1 run ${r}_form $PY bg1_cached.py src_bg1 $R/world_$r.json 10 /dev/shm/tmp/bg1_${r}_form.json; done; FR2_RELEASE= BG1_FORM= run chiral_60_off $PY bg1_cached.py src_bg1 $R/world_chiral_60.json 10 /dev/shm/tmp/bg1_chiral_60_off.json; FR2_RELEASE= BG1_FORM= run hole_60_off $PY bg1_cached.py src_bg1 $R/world_hole_60.json 10 /dev/shm/tmp/bg1_hole_60_off.json ) &
( FR2_RELEASE=1 BG1_FORM=1 run c48_3cube_60_form $PY ../H-Frozen-Node-Release-2/run_48.py src_bg1 ../H-Frozen-Node-Release-2/worlds/world_chiral_3_30.json 60 out/c48_3cube_60_form.json ) &
wait
echo all > out/run_all.done
