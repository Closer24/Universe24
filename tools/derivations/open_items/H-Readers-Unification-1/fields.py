"""The record's fields against the readers' reads, the call counts of the shared helpers on gates(hole), the distinct cuts, the per-function lines of the stubs, and the JSON round trip of the fresh reading against the committed one."""
import ast, json, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "src"))
import event_universe.gates as G, event_universe.decoder as Dc
run = json.loads((ROOT / "examples/records/hole.json").read_text())
reached = Counter(); cuts = Counter()
orig_to = Dc.Record.to
def to(self, i): cuts[i] += 1; return orig_to(self, i)
Dc.Record.to = to
import event_universe.events as E
E.Record = Dc.Record
WATCH = {str((ROOT / r).resolve()) for r in ("src/event_universe/board.py", "src/event_universe/clicks.py", "src/event_universe/gates.py", "src/event_universe/circle.py", "src/event_universe/decoder.py", "src/event_universe/predicates.py")}
def prof(frame, event, arg):
    if event == "call" and str(Path(frame.f_code.co_filename).resolve()) in WATCH and not frame.f_code.co_name.startswith("<"):
        reached[f"{Path(frame.f_code.co_filename).stem}.{frame.f_code.co_name}"] += 1
sys.setprofile(prof); reading = G.gates(run); sys.setprofile(None)
committed = (ROOT / "examples/records/hole.reading.jsonl").read_text()
fresh = "".join(json.dumps({k: v}) + "\n" for k, v in reading.items())
print("fresh reading == committed after JSON:", fresh == committed)
print("Record.to calls", sum(cuts.values()), "distinct cuts", len(cuts))
for k in ("gates.verdicts", "circle.circle_of", "board.volumes", "board.bottoms_of", "board.marks", "board.lift_of", "gates.approach", "clicks.tracks_of", "clicks.solved", "decoder.decoded_credits", "decoder.solve", "board.neighbours", "gates.distance", "predicates.distance", "gates.restated", "predicates.unread", "gates.kind_of", "events.first_interval"):
    print(f"  {k}: {reached[k]}")
rows_called = Counter(k for k in reached if any(k.startswith(m + ".") for m in ("board", "clicks", "gates", "predicates")))
print("row functions called more than once (all rows, by events' search):", sum(1 for k, n in reached.items() if n > 1 and k.split(".")[1] in {f.__name__ for f in G.TABLE}), "of", len(G.TABLE), "; max", max(reached[f"{f.__module__.split('.')[-1]}.{f.__name__}"] for f in G.TABLE))
# the record's fields against the readers
readers = "\n".join((ROOT / r).read_text() for r in ("src/event_universe/decoder.py", "src/event_universe/gates.py", "src/event_universe/events.py", "src/event_universe/board.py", "src/event_universe/clicks.py", "src/event_universe/predicates.py", "tools/page.py"))
def unread(name, keys):
    missing = [k for k in keys if ('"' + k + '"') not in readers and ("'" + k + "'") not in readers]
    print(f"  {name}: fields {sorted(keys)}; unread by every reader: {sorted(missing)}")
unread("run", run.keys())
unread("credit", next(e for e in run["log"] if e["event"] == "credit").keys())
unread("credit.frame", next(e for e in run["log"] if e["event"] == "credit" and "re_now" in e["frame"])["frame"].keys())
unread("birth", next(e for e in run["log"] if e["event"] == "birth").keys())
unread("refused", next(e for e in run["log"] if e["event"] == "refused").keys())
unread("row", run["rows"][0].keys())
unread("node line", run["nodes"][0].keys())
unread("counts", run["counts"].keys())
print("log events by kind:", dict(Counter(e["event"] for e in run["log"])))
# the stubs' lines in predicates and the restated rows in gates
tree = ast.parse((ROOT / "src/event_universe/predicates.py").read_text())
stubs = [(n.name, n.end_lineno - n.lineno + 1) for n in tree.body if isinstance(n, ast.FunctionDef) and any(isinstance(s, ast.Return) and isinstance(s.value, ast.Call) and getattr(s.value.func, "id", "") == "unread" for s in n.body)]
print("predicates stubs returning unread:", len(stubs), "lines", sum(l for _n, l in stubs), [n for n, _l in stubs])
tree = ast.parse((ROOT / "src/event_universe/gates.py").read_text())
rest = [(n.name, n.end_lineno - n.lineno + 1) for n in tree.body if isinstance(n, ast.FunctionDef) and any(isinstance(s, ast.Return) and isinstance(s.value, ast.Call) and getattr(s.value.func, "id", "") == "restated" for s in n.body)]
print("gates restated rows:", len(rest), "lines", sum(l for _n, l in rest))
# hand-written NOT READ ...; the predicate: outside predicates.unread
for r in ("src/event_universe/gates.py", "src/event_universe/board.py", "src/event_universe/clicks.py", "src/event_universe/predicates.py"):
    for k, line in enumerate((ROOT / r).read_text().splitlines(), 1):
        if "the predicate:" in line and "unread(" not in line and "def unread" not in line and '"""' not in line:
            print("  hand-written predicate clause", f"{r}:{k}")
# events: numbers field vs the row's own numbers
print("events numbers sample:", [e["numbers"] for e in reading["events"]][:4])
