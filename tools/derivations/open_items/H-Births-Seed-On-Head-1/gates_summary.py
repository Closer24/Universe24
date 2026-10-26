"""rg1: the engine's gates file (one JSON line per gate) summed: the gates shown, not shown and not read, by their verdict's first words, with gate 1's numbers. Usage: python gates_summary.py <gates.jsonl> [...]"""
import json
import sys

for path in sys.argv[1:]:
    lines = [json.loads(l) for l in open(path) if l.startswith("{")]
    shown, not_shown, not_read, other = [], [], [], []
    for d in lines:
        for k, v in d.items():
            verdict = v.get("verdict", "") if isinstance(v, dict) else str(v)
            if not verdict and isinstance(v, dict):
                verdict = next((x for x in v.values() if isinstance(x, str) and "SHOWN" in x), "")
            head = verdict.split(":")[0].strip()
            name = k.split(" ")[0]
            if head.startswith("NOT SHOWN"):
                not_shown.append(name)
            elif head.startswith("NOT READ"):
                not_read.append(name)
            elif head.startswith("SHOWN"):
                shown.append(name)
            else:
                other.append((name, verdict[:60]))
            if name == "1":
                print(path.split("/")[-1], "gate 1:", json.dumps({kk: vv for kk, vv in v.items() if kk != "rows' reading"})[:700])
    print(path.split("/")[-1], "| SHOWN", len(shown), shown, "| NOT SHOWN", len(not_shown), not_shown, "| NOT READ", len(not_read), not_read, "| other", other)
