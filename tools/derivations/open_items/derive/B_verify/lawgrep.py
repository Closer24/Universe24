"""Find phrases in the law's text and print the line number with a short excerpt (ASCII only)."""
import sys
path, phrases = sys.argv[1], sys.argv[2:]
lines = open(path, encoding="utf-8").read().split("\n")
for no, line in enumerate(lines, 1):
    for p in phrases:
        i = line.find(p)
        if i >= 0:
            a, b = max(0, i - 120), min(len(line), i + len(p) + 220)
            ex = line[a:b].encode("ascii", "replace").decode()
            print(f"{no} [{p}] len={len(line)}: ...{ex}...")
