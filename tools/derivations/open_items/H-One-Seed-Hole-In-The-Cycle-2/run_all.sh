#!/bin/sh
# os2: every candidate on the head's src (no flag), integers only, nice -n 19, TMPDIR=/dev/shm/tmp
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=../../../../src
export TMPDIR=/dev/shm/tmp
run() { out=$1; shift; s=$(date +%s); nice -n 19 "$@" > out/$out.stdout 2> out/$out.stderr; echo "done $(( $(date +%s) - s )) s" > out/$out.done; }
run n0 $PY course.py $SRC worlds/n0_ga2.json 450 10 out/n0.json &
run n1 $PY course.py $SRC worlds/n1_hole_origin.json 450 10 out/n1.json &
run n2 $PY course.py $SRC worlds/n2_hole_class0.json 450 10 out/n2.json &
run n3 $PY course.py $SRC worlds/n3_hole_every_node.json 450 10 out/n3.json &
wait
run n4 $PY course.py $SRC worlds/n4_sea_hole_class0.json 450 10 out/n4.json &
run n5 $PY course.py $SRC worlds/n5_mirror1.json 450 10 out/n5.json &
run n6 $PY course.py $SRC worlds/n6_hole_period2.json 450 10 out/n6.json &
run n7 $PY course.py $SRC worlds/n7_sea_hole_every_node.json 450 10 out/n7.json &
wait
echo all > out/run_all.done
run n2_8 $PY course.py $SRC worlds/n2_hole_class0_8cube.json 230 10 out/n2_8.json
echo all8 > out/run_all8.done
