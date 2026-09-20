"""Genericity probe: rename every family and detector of a world to an arbitrary
token, run both, and compare events.jsonl and state.json with the names mapped back."""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
python = sys.argv[3]
TOKENS = [
    "measure",
    "__proto__",
    "rule",
    "wave",
    "sum",
    "0",
    "face:+x ",
    "read",
    "constructor",
    "pass",
    "rerelease",
    "beam",
    "K",
    "N",
    "lamp",
    "gate",
    "record",
    "amount",
    "phase",
    "true",
    "null",
    "x",
    "yy",
    "zz1",
    "the light",
    "mass",
    "gravity",
]


def rename_world(d):
    names = [f["name"] for f in d["families"]]
    fam = {n: f"{TOKENS[i % len(TOKENS)]}~{i}" for i, n in enumerate(names)}
    det = {
        x["name"]: f"{TOKENS[(i + 7) % len(TOKENS)]}#{i}" for i, x in enumerate(d.get("detectors", []))
    }
    col = {}

    def cols(fd):
        for c in list(fd.get("columns", {})):
            col.setdefault(c, f"col{len(col)}~{TOKENS[len(col) % len(TOKENS)]}")

    for f in d["families"]:
        cols(f)
    r = json.loads(json.dumps(d))
    for f in r["families"]:
        f["name"] = fam[f["name"]]
        if "columns" in f:
            f["columns"] = {col[k]: v for k, v in f["columns"].items()}
    for m in r.get("measured", []):
        m["family"] = fam[m["family"]]
        if "held" in m:
            m["held"] = {fam[k]: v for k, v in m["held"].items()}
        if "table" in m:
            t = {}
            for k, v in m["table"].items():
                if isinstance(v, dict):
                    v = dict(v)
                    if isinstance(v.get("phase_window"), dict):
                        v["phase_window"] = {
                            **v["phase_window"],
                            "reads": fam[v["phase_window"]["reads"]],
                        }
                    if "into" in v:
                        v["into"] = fam[v["into"]]
                    if "products" in v:
                        v["products"] = [[fam[p[0]], p[1], p[2]] for p in v["products"]]
                t[fam[k]] = v
            m["table"] = t
        if "become" in m:
            b = dict(m["become"])
            b["into"] = fam[b["into"]]
            b["products"] = [[fam[p[0]], p[1], p[2]] for p in b["products"]]
            m["become"] = b
    for x in r.get("in_transit", []):
        x["family"] = fam[x["family"]]
    for x in r.get("detectors", []):
        x["name"] = det[x["name"]]
    return r, fam, det, col


def run(world_path, target, ticks):
    if target.exists():
        shutil.rmtree(target)
    cmd = [python, "-m", "event_universe", "--init", str(world_path), "--output", str(target / "run")]
    if ticks:
        cmd += ["--ticks", str(ticks)]
    subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        env={"PYTHONPATH": str(root / "src"), "PATH": "/usr/bin:/bin"},
    )
    return target / "run"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


verdicts = []
for spec in sys.argv[4:]:
    rel, _, ticks = spec.partition(":")
    ticks = int(ticks) if ticks else None
    src = root / "examples/events" / rel
    d = json.load(open(src))
    if "entity_definitions" in d:
        print("skip (entities)", rel)
        continue
    r, fam, det, col = rename_world(d)
    stem = src.stem
    (out / f"{stem}_renamed.json").write_text(json.dumps(r))
    a = run(src, out / f"{stem}_a", ticks)
    b = run(out / f"{stem}_renamed.json", out / f"{stem}_b", ticks)
    back = {v: k for m in (fam, det, col) for k, v in m.items()}

    def unmap(text):
        # map the renamed tokens back by exact JSON string value
        for new, old in sorted(back.items(), key=lambda kv: -len(kv[0])):
            text = text.replace(json.dumps(new), json.dumps(old))
        return text

    ev_a = (a / "events.jsonl").read_text()
    ev_b = unmap((b / "events.jsonl").read_text())
    st_a = json.loads((a / "state.json").read_text())
    st_b = json.loads(unmap((b / "state.json").read_text()))
    ra = json.loads((a / "run.json").read_text())
    rb = json.loads(unmap((b / "run.json").read_text()))
    for k in ("elapsed_seconds", "initialization_sha256", "source_sha256"):
        ra.pop(k, None)
        rb.pop(k, None)
    lines = len(ev_a.splitlines())
    v = (
        "events " + ("identical" if ev_a == ev_b else "DIFFER"),
        "state " + ("identical" if st_a == st_b else "DIFFER"),
        "run.json " + ("identical" if ra == rb else "DIFFER"),
        f"{lines} lines, {ra['completed_ticks']} ticks, families {len(fam)}, detectors {len(det)}",
    )
    print(rel, *v)
    verdicts.append((rel, v))
