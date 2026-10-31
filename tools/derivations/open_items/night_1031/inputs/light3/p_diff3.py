"""LIGHT3's board check of the reflector lay (two records compared: a check, never the reading): the click lines of
two runs that differ only in the lay at one site. Lines are matched by (round, site, train); a line differs where it
is in one record alone or its q, sides or across differ. Printed: the count of differing lines and sites, the first
differing line, and per tenth round the sites where lines differ, as the lowest and highest site labels on each side
of the laid site (labels only, a board check against the site order)."""

import json
import sys
from pathlib import Path


def lines_of(path):
    held = {}
    with path.open(encoding="utf-8") as f:
        for text in f:
            e = json.loads(text)
            if e.get("kind") == "click":
                held[(e["round"], e["site"], e["train"])] = (e["q"], e["sides"], e["across"])
    return held


def main():
    one, two, site = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    a, b = lines_of(one), lines_of(two)
    keys = sorted(set(a) | set(b))
    diff = [k for k in keys if a.get(k) != b.get(k)]
    print(f"{one.name} against {two.name}: {len(a)} and {len(b)} lines; {len(diff)} differ, at "
          f"{len({k[1] for k in diff})} sites")
    if not diff:
        return
    print(f"  the first differing line: round {diff[0][0]}, site {diff[0][1]}, train {diff[0][2]}")
    rounds = sorted({k[0] for k in diff})
    for r in range(rounds[0], rounds[-1] + 1):
        at = sorted({k[1] for k in diff if k[0] == r})
        if at and (r % 10 == 0 or r == rounds[0] or r == rounds[-1]):
            below = [s for s in at if s < site]
            above = [s for s in at if s > site]
            print(f"  round {r}: {len(at)} sites differ; below {site}: {min(below) if below else '-'} to "
                  f"{max(below) if below else '-'}; at {site}: {site in at}; above: {min(above) if above else '-'} to "
                  f"{max(above) if above else '-'}")


if __name__ == "__main__":
    main()
