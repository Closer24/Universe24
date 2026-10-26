"""The inventory of the readers (H-Readers-Unification-1): functions per module with their lines, the call graph by ast, the functions no row reaches, the fields the readers parse again, the three name tables against each other, the verdict handling sites, and one traced run of the decoder on the hole record (sys.setprofile, the venv has no coverage) with the page written. Usage: python inventory.py <worktree>."""

from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "src"))
READERS = {
    "decoder": "src/event_universe/decoder.py",
    "gates": "src/event_universe/gates.py",
    "events": "src/event_universe/events.py",
    "board": "src/event_universe/board.py",
    "clicks": "src/event_universe/clicks.py",
    "predicates": "src/event_universe/predicates.py",
    "circle": "src/event_universe/circle.py",
    "readings": "src/event_universe/readings.py",
    "page": "tools/page.py",
    "phenomena": "tools/phenomena.py",
    "test_the_record": "tests/test_the_record.py",
}
out: dict = {}

# (D) functions per module, their lines, and the call graph
funcs: dict[str, dict[str, tuple[int, int]]] = {}
calls: dict[str, set[str]] = defaultdict(set)
row_keys: dict[str, list[str]] = {}
for mod, rel in READERS.items():
    src = (ROOT / rel).read_text(encoding="utf-8")
    tree = ast.parse(src)
    funcs[mod] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[mod][node.name] = (node.lineno, node.end_lineno - node.lineno + 1)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    f = sub.func
                    if isinstance(f, ast.Name):
                        calls[f"{mod}.{node.name}"].add(f.id)
                    elif isinstance(f, ast.Attribute):
                        calls[f"{mod}.{node.name}"].add(f.attr if not isinstance(f.value, ast.Name) else f"{f.value.id}.{f.attr}")
                if isinstance(sub, ast.Name) and sub.id in funcs.get(mod, {}):
                    calls[f"{mod}.{node.name}"].add(sub.id)
    # keys of rows: string literals matching "<n> " or named rows at a dict key position in a return
    keys = sorted({c.value for c in ast.walk(tree) if isinstance(c, ast.Constant) and isinstance(c.value, str) and re.match(r"^(\d+[bc]? |the conservations in the clicks$|the three constants$)", c.value)})
    row_keys[mod] = keys
out["functions per module"] = {m: {"count": len(f), "lines in functions": sum(n for _l, n in f.values()), "names": sorted(f)} for m, f in funcs.items()}
out["row keys per module"] = row_keys

# (F) names referenced anywhere in the readers, run.py and the tests (a function no reader calls)
all_text = "\n".join((ROOT / rel).read_text(encoding="utf-8") for rel in READERS.values())
all_text += "\n" + "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "src").rglob("*.py")) + "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").rglob("*.py")) + "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tools").glob("*.py"))
unref = {}
for mod, fs in funcs.items():
    for name, (line, n) in fs.items():
        hits = len(re.findall(rf"\b{re.escape(name)}\b", all_text))
        if hits <= 1 and not name.startswith("test_") and name != "main":
            unref[f"{mod}.{name}"] = {"line": line, "lines": n, "mentions in all readers, src, tests, tools": hits}
out["(F) functions named once only (defined, never called)"] = unref

# (F) a traced run of the decoder on hole.json and the page
import event_universe.gates as G  # noqa: E402
reached: Counter[str] = Counter()
WATCH = {str((ROOT / r).resolve()) for r in READERS.values()}
def prof(frame, event, arg):
    if event == "call" and str(Path(frame.f_code.co_filename).resolve()) in WATCH:
        reached[f"{Path(frame.f_code.co_filename).stem}.{frame.f_code.co_name}"] += 1
run = json.loads((ROOT / "examples/records/hole.json").read_text(encoding="utf-8"))
sys.setprofile(prof)
reading = G.gates(run)
sys.setprofile(None)
committed = [json.loads(l) for l in (ROOT / "examples/records/hole.reading.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
same = [ {k: v} for k, v in reading.items()] == committed
out["decoder on hole.json equals the committed reading bit for bit"] = same
never = {}
for mod in ("decoder", "gates", "events", "board", "clicks", "predicates", "circle"):
    for name, (line, n) in funcs[mod].items():
        if reached[f"{mod}.{name}"] == 0 and name != "main" and not name.startswith("<"):
            never[f"{mod}.{name}"] = {"line": line, "lines": n}
out["(F) reader functions never entered by gates(hole)"] = never
out["(F) calls per function on gates(hole), the heaviest"] = dict(reached.most_common(14))
# Record.to count and verdicts(record) count
out["(C) Record.to calls on gates(hole)"] = reached["decoder.to"]
# page
sys.path.insert(0, str(ROOT / "tools"))
import importlib.util as iu  # noqa: E402
spec = iu.spec_from_file_location("page", ROOT / "tools/page.py"); page = iu.module_from_spec(spec); spec.loader.exec_module(page)
html = page.page_of(run, committed)
out["page bytes on hole"] = len(html)
# the fields of the reading the page reads
page_src = (ROOT / "tools/page.py").read_text(encoding="utf-8")
out["(E) page reads of the reading (events' fields, in the script)"] = sorted(set(re.findall(r"e\.(gate|label|i|node|numbers)\b", page_src)))
out["(E) page regexes on the gate key (the page derives the eras and the bangs from the key's number)"] = re.findall(r"/\^[^/]+/", page_src)
# (C) verdict handling sites
sites = []
for mod, rel in READERS.items():
    for k, line in enumerate((ROOT / rel).read_text(encoding="utf-8").splitlines(), 1):
        if re.search(r'startswith\(|\.split\(": "|split\(";"\)|KINDS|kind_of|"NOT READ|"NOT SHOWN|"SHOWN|in part', line) and mod not in ("test_the_record",):
            if re.search(r'startswith\(|split\(": "|split\(";"\)|kind_of\(|cause_of\(|in_part|KINDS', line):
                sites.append(f"{rel}:{k}: {line.strip()[:110]}")
out["(C) verdict string handling sites"] = sites
# (C) verdict literals per module (the decision written as strings)
out["(C) verdict literals per module"] = {m: len(re.findall(r'"(?:SHOWN|NOT SHOWN|NOT READ|NOT REACHED)', (ROOT / r).read_text(encoding="utf-8"))) for m, r in READERS.items()}
# (D) fields parsed again: record["cube"] and the index arithmetic, distance functions, the senses' signs, taken/booked
pats = {
    "int(record.run[\"cube\"])": r'int\(record\.run\["cube"\]\)',
    "the Node's index from x, y, z or back (cube * cube)": r"cube \* cube",
    "the senses' signs (w > 0) - (w < 0)": r"\(w > 0\) - \(w < 0\)",
    "booked and taken summed over the births": r'sum\(b\["booked"\]',
    "the takes = births + credits by event": r'in \("birth", "credit"\)',
    "a dict by (Node, line)": r"\(tuple\(c\[\"node\"\]\), c\[\"line\"\]\)",
    "a torus distance function": r"def distance\(",
    "the births by species via line_name[b[\"line_pair\"]]": r'line_name\[b\["line_pair"\]\]',
    "a verdict chain of conditional expressions (if ... else) inside a dict": r'^\s+(?:if|else) ',
}
dup = {}
for what, pat in pats.items():
    found = []
    for mod, rel in READERS.items():
        for k, line in enumerate((ROOT / rel).read_text(encoding="utf-8").splitlines(), 1):
            if re.search(pat, line):
                found.append(f"{rel}:{k}")
    dup[what] = found if what != "a verdict chain of conditional expressions (if ... else) inside a dict" else len(found)
out["(D) fields and forms parsed again across the four modules"] = dup
# (B) three name tables
import event_universe.events as E  # noqa: E402
spec2 = iu.spec_from_file_location("phen", ROOT / "tools/phenomena.py"); ph = iu.module_from_spec(spec2); spec2.loader.exec_module(ph)
keys = [k for k in reading if re.match(r"^\d", k)]
titles = {k.split()[0]: " ".join(k.split()[1:]) for k in keys}
tables = {}
for n in sorted(titles, key=lambda s: (int(re.match(r"\d+", s).group()), s)):
    tables[n] = {"decoder key": titles[n], "LABELS": E.LABELS.get(n), "PHENOMENA": ph.PHENOMENA.get(int(re.match(r"\d+", n).group())) if n.isdigit() else None}
out["(B) the three name tables, row by row"] = tables
out["(B) counts"] = {"decoder keys (numbered)": len(keys), "LABELS": len(E.LABELS), "PHENOMENA": len(ph.PHENOMENA), "rows of TABLE": len(G.TABLE), "rows in events (gates(hole))": len(reading["events"])}
# (G) the test
test = (ROOT / "tests/test_the_record.py").read_text(encoding="utf-8")
out["(G) asserts in test_the_record.py"] = len(re.findall(r"^\s+assert ", test, re.M))
out["(G) gate rows named in VERDICTS"] = sorted({k for name in ("hole", "chiral", "bodies") for k in re.findall(r'"(\d+[bc]? [^"]+)": "', test)})
(ROOT / "tools/derivations/open_items/H-Readers-Unification-1/inventory.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
# the difference against the committed reading, by key
diff = []
for k, v in reading.items():
    c = next((line[k] for line in committed if k in line), None)
    if c != v:
        diff.append(k if k != "events" else f"events ({len(v)} against {len(c) if c else None})")
print("DIFF against committed:", diff)
for k in diff[:3]:
    if k.startswith("events"):
        continue
    c = next((line[k] for line in committed if k in line), None)
    for kk in set(v := reading[k]) | set(c or {}):
        if (c or {}).get(kk) != v.get(kk):
            print("  ", k, "|", kk, "| committed", str((c or {}).get(kk))[:150], "| found", str(v.get(kk))[:150])
