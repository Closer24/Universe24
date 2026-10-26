"""fr1's flagged COPY of the engine (engine-5.0-test 38655ef18), written from the worktree's src by exact text replacements, each named
below; the engine's own files are never touched. The flag is the environment key FR1_RELEASE (unset or empty: the engine bit for bit;
"1": the swap's own trigger unmasked at the frozen Nodes, so a frozen Node whose held line is a weak maximum (before < now = after
the restore) is turned by the letter's exchange of now and before, and the run back restores a frozen Node to the pre-state the
exchange returned). Run: python make_copy_fr1.py  (writes src_fr1/ beside this file; refuses where a replacement does not match exactly once)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "..", "src", "event_universe")
DST = os.path.join(HERE, "src_fr1", "event_universe")

FLAG = '''"""fr1's flag (2026-10-26): the release of the frozen Node by the turn of its time, under test in this COPY of the engine; read from the environment key FR1_RELEASE; unset or empty is the engine bit for bit."""
import os


def release() -> bool:
    """The swap's own trigger unmasked at the frozen Nodes (the exchange of now and before at a frozen Node whose held line is a weak maximum), and the run back's restore of a frozen Node to the pre-state the exchange returned."""
    return os.environ.get("FR1_RELEASE", "") != ""
'''

REPLACEMENTS = {
    "node.py": [
        # the import
        ("from event_universe.links import Link, turned\n", "from event_universe.links import Link, turned\nfrom event_universe import fr1_flag\n"),
        # the swap's trigger masked at the frozen Nodes (BH-S1) -- unmasked under the flag
        ("        if frozen is not None:\n            top = top & ~frozen\n", "        if frozen is not None and not fr1_flag.release():\n            top = top & ~frozen\n"),
    ],
    "interval.py": [
        ("from event_universe import gram, readings\n", "from event_universe import fr1_flag, gram, readings\n"),
        # backward, a frozen Node restored to the pre-state the exchange returned (kept), the same as held where the Node was not turned
        (
            "        node.restore(node.all_lines(), [line for row in self.held for line in row], self.frozen)\n",
            "        rest = self.kept if (fr1_flag.release() and self.direction == -1 and self.kept is not None) else self.held\n        node.restore(node.all_lines(), [line for row in rest for line in row], self.frozen)\n",
        ),
    ],
}


def main() -> None:
    if os.path.exists(os.path.dirname(DST)):
        shutil.rmtree(os.path.dirname(DST))
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))
    for name, pairs in REPLACEMENTS.items():
        path = os.path.join(DST, name)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for old, new in pairs:
            if text.count(old) != 1:
                raise SystemExit("refused: %s matches %d times in %s" % (old[:60], text.count(old), name))
            text = text.replace(old, new)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    with open(os.path.join(DST, "fr1_flag.py"), "w", encoding="utf-8") as f:
        f.write(FLAG)
    print("written", DST)


if __name__ == "__main__":
    main()
