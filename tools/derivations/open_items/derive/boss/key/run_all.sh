#!/bin/sh
# Runs every key probe on the committed 7b act (src/); each writes its .txt beside it. About 2 minutes.
D=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-python3}  # the repository's interpreter, with numpy
export PYTHONDONTWRITEBYTECODE=1
for s in p1_covariance p2_books p3_tensors p4_closure p5_resolution p6_reversal_keys; do
  echo "== $s"; "$PY" -I "$D/$s.py" > "$D/$s.txt" || exit 1
done
