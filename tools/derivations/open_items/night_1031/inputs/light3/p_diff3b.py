"""LIGHT3's board check beside p_diff3: of the lines that differ between two records (matched by round, site and
train), how many differ in their across field, how many stand in one record alone, and which trains they belong to."""
import json
import sys
from pathlib import Path


def lines(path):
    held = {}
    with path.open(encoding="utf-8") as f:
        for text in f:
            e = json.loads(text)
            if e.get("kind") == "click":
                held[(e["round"], e["site"], e["train"])] = e
    return held


one, two = Path(sys.argv[1]), Path(sys.argv[2])
a, b = lines(one), lines(two)
d = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
across = sum(1 for k in d if (a.get(k) or {}).get("across") != (b.get(k) or {}).get("across"))
alone = sum(1 for k in d if (k in a) != (k in b))
print(f"{one.name} against {two.name}: {len(d)} lines differ; with a different across field {across}; in one record "
      f"alone {alone}; trains {sorted({k[2] for k in d})}; sites {sorted({k[1] for k in d})[:6]}")
