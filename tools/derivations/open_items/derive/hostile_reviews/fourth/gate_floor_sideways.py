"""floored() where the merge base lies on another line than the floor (neither an ancestor of the other), in a scratch repo.

Usage: python gate_floor_sideways.py <worktree>. The docstring says the floor replaces a merge base older than it.
"""
import importlib.util, subprocess, sys, tempfile
from pathlib import Path

wt = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("gate", wt / "tools/derivations/open_items/scribe_scan.py")
gate = importlib.util.module_from_spec(spec); sys.modules["gate"] = gate; spec.loader.exec_module(gate)
with tempfile.TemporaryDirectory(dir="/dev/shm/tmp") as d:
    g = ["git", "-C", d, "-c", "user.name=p", "-c", "user.email=p@example.invalid"]
    run = lambda *a: subprocess.run([*g, *a], capture_output=True, text=True, check=True).stdout.strip()
    run("init", "-q", "-b", "trunk"); run("commit", "-q", "--allow-empty", "-m", "root")
    run("checkout", "-q", "-b", "side"); run("commit", "-q", "--allow-empty", "-m", "side, after the root")
    side = run("rev-parse", "HEAD")
    run("checkout", "-q", "trunk"); run("commit", "-q", "--allow-empty", "-m", "floor"); floor = run("rev-parse", "HEAD")
    run("merge", "-q", "--no-ff", "-m", "tree: the floor's line with the side merged", "side"); tree = run("rev-parse", "HEAD")
    gate.FLOOR = floor
    got = gate.floored(Path(d), side, tree)
    print("merge base on a side line (not older than the floor, not after it): floored() gives",
          "the floor" if got == floor else "the merge base")
