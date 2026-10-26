#!/bin/sh
# rl2: every measurement under nice, four at a time, in the queue's order; the flag RL2_FORM names the form, empty the head
cd "$(dirname "$0")"
PY=/home/user/Universe24/venv314/bin/python
SRC=/dev/shm/tmp/rl2/src_rl2
W=../../../..
R=../../../../../../records/2ab32b518
O=/dev/shm/tmp/rl2/out
export TMPDIR=/dev/shm/tmp
mkdir -p $O
cat > $O/queue.txt <<Q
RL2_FORM=arith $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_arith.json
RL2_FORM=link $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_link.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_arith.json $R/world_hole_60.json
RL2_FORM= $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_off.json $R/world_hole_60.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_link.json $R/world_hole_60.json
RL2_FORM= $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_off.json
RL2_FORM=harm $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_harm.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_arith.json $R/world_chiral_60.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_chiral.json 60 10 $O/chiral60_link.json $R/world_chiral_60.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_arith.json $R/world_ga2_450.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_ga2.json 450 10 $O/ga2_link.json $R/world_ga2_450.json
RL2_FORM=harm $PY run_record.py $SRC $W/tests/worlds/world_hole.json 60 10 $O/hole60_harm.json $R/world_hole_60.json
RL2_FORM=geom $PY run_48.py $SRC worlds/world_chiral_3_30.json 60 $O/c48_geom.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_universe.json 400 10 $O/universe400_arith.json $R/world_universe_400.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_plasma_3.json 170 10 $O/plasma170_arith.json $R/world_plasma_3_170.json
RL2_FORM=arith $PY run_record.py $SRC $W/tests/worlds/world_pair_3.json 400 10 $O/pair400_arith.json $R/world_pair_3_400.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_universe.json 400 10 $O/universe400_link.json $R/world_universe_400.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_plasma_3.json 170 10 $O/plasma170_link.json $R/world_plasma_3_170.json
RL2_FORM=link $PY run_record.py $SRC $W/tests/worlds/world_pair_3.json 400 10 $O/pair400_link.json $R/world_pair_3_400.json
Q
n=0
while IFS= read -r cmd; do n=$((n+1)); echo "nice -n 19 env $cmd > $O/q$n.stdout 2> $O/q$n.stderr; echo done > $O/q$n.done"; done < $O/queue.txt | xargs -P 4 -I{} sh -c '{}'
echo all > $O/run_all.done
