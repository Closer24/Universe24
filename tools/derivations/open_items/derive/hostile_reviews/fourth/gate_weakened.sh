#!/bin/bash
# Weakened copies of Sofer's scan in the worktree, each run through the self-test (the ratchet F3 adds), then restored.
# Usage: gate_weakened.sh <worktree>
W=$1
PY=/home/user/Universe24/venv314/bin/python
S=tools/derivations/open_items/scribe_scan.py
export CHECK_BASE=67b765312 TMPDIR=/dev/shm/tmp
cd "$W" || exit 2

weaken() {  # label, python expression editing text t
  $PY - "$S" "$2" <<'EOF'
import sys
from pathlib import Path
p, expr = Path(sys.argv[1]), sys.argv[2]
t = p.read_text()
old, new = eval(expr)
assert t.count(old) == 1, old
p.write_text(t.replace(old, new))
EOF
  out=$($PY tools/derivations/open_items/scribe_scan_selftest.py 2>&1); rc=$?
  printf '%-70s rc=%s %s\n' "$1" "$rc" "$(echo "$out" | tail -1)"
  git checkout -q -- $S
}

weaken "the root may import numpy" \
  "('return top in sys.stdlib_module_names  #', 'return top in sys.stdlib_module_names or top == \"numpy\"  #')"
weaken "the root imports anything (root wall off)" \
  "('if folder == \"__init__.py\":\n        return top in sys.stdlib_module_names', 'if folder == \"__init__.py\":\n        return True')"
weaken "a root module extra.py listed" "('{\"__init__.py\", \"main.py\"}', '{\"__init__.py\", \"main.py\", \"extra.py\"}')"
weaken "unlisted folders not refused (root modules alone)" \
  "('(len(parts) == 2 and parts[1] not in ROOT_MODULES) or (\n            len(parts) > 2 and parts[1] not in WALLS\n        )', '(len(parts) == 2 and parts[1] not in ROOT_MODULES)')"
weaken "the floor applied even where the tree lacks it" \
  "('return floor if git(repo, \"merge-base\", \"--is-ancestor\", floor, tree_rev).returncode == 0 else found', 'return floor')"
weaken "the floor's ancestry read backwards" \
  "('git(repo, \"merge-base\", \"--is-ancestor\", floor, found).returncode == 0', 'git(repo, \"merge-base\", \"--is-ancestor\", found, floor).returncode == 0')"
weaken "FLOOR moved to HEAD (the tree's own commit)" "('FLOOR = \"526a5666d\"', 'FLOOR = \"HEAD\"')"
weaken "FLOOR moved to 4b39f234b" "('FLOOR = \"526a5666d\"', 'FLOOR = \"4b39f234b\"')"
weaken "merge_base returns the tree itself" \
  "('found = git(repo, \"merge-base\", commit, tree_rev)', 'found = git(repo, \"rev-parse\", tree_rev)')"
echo "restored: $(git status --short | wc -l) changes in the worktree"

# what FLOOR = "HEAD" does to the base the ratchet reads
$PY - "$W" <<'EOF'
import importlib.util, sys
from pathlib import Path
wt = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("gate", wt / "tools/derivations/open_items/scribe_scan.py")
gate = importlib.util.module_from_spec(spec); sys.modules["gate"] = gate; spec.loader.exec_module(gate)
print("as adopted:      merge_base ->", gate.merge_base(wt, "67b765312", "HEAD"))
gate.FLOOR = "HEAD"
print("FLOOR = 'HEAD':  merge_base ->", gate.merge_base(wt, "67b765312", "HEAD"), "(HEAD is", gate.resolve(wt, "HEAD")[:9] + ")")
EOF
