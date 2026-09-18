#!/bin/bash
S=/tmp/claude-0/-home-user-Universe24/0b03033a-a270-572b-b3b6-f528960b6109/scratchpad
cd $S/wt-runs-field
until [ -f artifacts/e11_law/summary.md ]; do sleep 20; done
echo "E11 series done $(date -u)"
PYTHONPATH=src $S/venv/bin/python tools/run_series.py --jobs 1 --out artifacts/e11_law_closed examples/nature/e11_law/standing_closed.json > artifacts/e11_closed_series.log 2>&1
echo "E11 closed done $(date -u) exit $?"
PYTHONPATH=src $S/venv/bin/python examples/nature/e11_law/analyze.py artifacts/e11_law --closed artifacts/e11_law_closed --record examples/nature/e11_law/record.json --tables examples/nature/e11_law/tables.md > artifacts/e11_analyze.log 2>&1
echo "E11 analysis done $(date -u) exit $?"
PYTHONPATH=src $S/venv/bin/python tools/run_series.py --jobs 2 --out artifacts/a5s_law examples/nature/a5s_law/pp_d4.json examples/nature/a5s_law/pp_d6.json examples/nature/a5s_law/pp_d8.json examples/nature/a5s_law/pp_d12.json examples/nature/a5s_law/pp_d8_110.json examples/nature/a5s_law/pp_d8_111.json examples/nature/a5s_law/pq_d8.json examples/nature/a5s_law/qq_d8.json > artifacts/a5s_series.log 2>&1
echo "A5s open series done $(date -u) exit $?"
PYTHONPATH=src $S/venv/bin/python examples/nature/a5s_law/analyze.py artifacts/a5s_law --replay pq_d8 --record examples/nature/a5s_law/record.json --tables examples/nature/a5s_law/tables.md > artifacts/a5s_analyze.log 2>&1
echo "A5s open analysis done $(date -u) exit $?"
PYTHONPATH=src $S/venv/bin/python tools/run_series.py --jobs 2 --out artifacts/a5s_law_closed examples/nature/a5s_law/pp_d4_closed.json examples/nature/a5s_law/pp_d6_closed.json examples/nature/a5s_law/pp_d8_closed.json examples/nature/a5s_law/pp_d12_closed.json > artifacts/a5s_closed_series.log 2>&1
echo "A5s closed series done $(date -u) exit $?"
PYTHONPATH=src $S/venv/bin/python examples/nature/a5s_law/analyze.py artifacts/a5s_law --closed artifacts/a5s_law_closed --record examples/nature/a5s_law/record.json --tables examples/nature/a5s_law/tables.md > artifacts/a5s_analyze2.log 2>&1
echo "A5s closed analysis done $(date -u) exit $?"
echo CHAIN_DONE
