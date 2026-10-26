"""The release clause read by calls alone, on the history as it stands (no commit): the version at the refs, `released` where the versions agree and where they differ, and what base_ref returns."""
import os, sys
from pathlib import Path
W = Path(sys.argv[1])
sys.path.insert(0, str(W / "tools"))
import merge_base as mb  # noqa: E402
root = W
for ref in ("HEAD", "6703dd95c", "origin/main", "43cbefbc8", "0963ae9ff"):
    print("version at", ref, "=", mb.version_at(root, ref))
print("--- released(root, '6703dd95c') (the versions agree):", mb.released(root, "6703dd95c"))
print("--- released(root, 'origin/main') (the versions agree):", mb.released(root, "origin/main"))
print("--- released(root, '43cbefbc8') (the base names no version):")
print("    returned:", mb.released(root, "43cbefbc8"))
os.environ["CHECK_BASE"] = "6703dd95c"
print("--- base_ref with CHECK_BASE=6703dd95c:", mb.base_ref())
