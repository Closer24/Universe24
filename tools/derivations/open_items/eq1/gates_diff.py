"""Two gates files compared: every numbered gate whose verdict's kind (SHOWN / NOT SHOWN / other) differs, with both verdicts' heads."""
import json, sys


def read(path):
    found = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        d = json.loads(line)
        for k, v in d.items():
            if k.split()[0].isdigit() and isinstance(v, dict) and "verdict" in v:
                found[k] = v["verdict"]
    return found


a, b = read(sys.argv[1]), read(sys.argv[2])
kind = lambda v: "SHOWN" if v.startswith("SHOWN") else ("NOT SHOWN" if v.startswith("NOT SHOWN") else v.split(":")[0])
shown = lambda d: sorted(int(k.split()[0]) for k, v in d.items() if kind(v) == "SHOWN")
print("SHOWN before:", shown(a))
print("SHOWN after: ", shown(b))
for k in sorted(set(a) | set(b), key=lambda s: int(s.split()[0])):
    va, vb = a.get(k, "-"), b.get(k, "-")
    if kind(va) != kind(vb):
        print("  %s: %s -> %s" % (k, va[:120], vb[:120]))
