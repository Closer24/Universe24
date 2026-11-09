"""Replay and check the published matter/light building blocks.

Uses only the unchanged engine package ``universe24`` and the standard library.
For every catalog entry it:

1. checks the SHA-256 of the init file against the catalog;
2. loads it with ``universe24.experiments.from_dict`` (the official init format);
3. runs the native ``Engine`` for the declared horizon and checks the exact
   inverse ``Engine.rewind`` at every update;
4. compares the complete final state with the recorded SHA-256;
5. re-checks the generic part of the declared signature (period, translation,
   silence, click counts and kinds, no-return bound) with the native click
   classifier.

Researcher-specific checks ("custom" in the catalog) were run by the source
library when the package was built; they are listed, not re-run here.
Local "box" checks are re-run: a declared set of sites is exactly P-periodic on
a time window (an atom candidate in its trap), or equals its 360-degree image
C (every channel g -> z*g, z = 14) after each lap and itself after two laps
(a spinor-class ring).

    python -m research.matter_light_blocks_v1.verify              # every block
    python -m research.matter_light_blocks_v1.verify --quick      # skip blocks marked heavy
    python -m research.matter_light_blocks_v1.verify fiber_x_packet spinor_screw
    python -m research.matter_light_blocks_v1.verify --list
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

from universe24.experiments import from_dict
from universe24.observation import clicks
from universe24.core.group_2o import group

HERE = Path(__file__).resolve().parent
CATALOG = HERE / "catalog.json"


def state_hash(state) -> str:
    """SHA-256 of a complete state (side, background, every non-background cell)."""
    blob = json.dumps([state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())],
                      separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def load(name: str):
    """(engine, initial state, horizon, catalog entry) for one block."""
    entry = next(e for e in load_catalog()["entries"] if e["name"] == name)
    experiment = from_dict(json.loads((HERE / entry["file"]).read_text(encoding="utf-8")))
    return experiment.engine, experiment.initial, experiment.steps, entry


def _shift(state, v):
    L = state.cube.side
    dx, dy, dz = v
    return {((x + dx) % L, (y + dy) % L, (z + dz) % L, g): c for (x, y, z, g), c in state.cells.items()}


def replay(entry: dict) -> dict:
    """Native run with exact inverse every update; returns the measured quantities."""
    experiment = from_dict(json.loads((HERE / entry["file"]).read_text(encoding="utf-8")))
    engine, initial, steps = experiment.engine, experiment.initial, experiment.steps
    sig = entry.get("signature", {})
    trans = sig.get("translation")
    keep_t = {trans["period"]} if trans else set()
    kept = {}
    box_sites = {tuple(x) for b in entry.get("box_checks", []) for x in b["sites"]}
    boxes = {0: _box(initial, box_sites)} if box_sites else {}
    per_step, kinds_per_step = [], []
    first_return = None
    state = initial
    for t in range(1, steps + 1):
        nxt = engine.advance(state)
        if engine.rewind(nxt) != state:
            raise ArithmeticError(f"{entry['name']}: exact inverse failed at update {t}")
        events = list(clicks(state, nxt, t))
        per_step.append(len(events))
        kinds_per_step.append(Counter(f"C{e.kind}" for e in events))
        if first_return is None and nxt == initial:
            first_return = t
        if t in keep_t:
            kept[t] = nxt
        if box_sites:
            boxes[t] = _box(nxt, box_sites)
        state = nxt
    return {"initial": initial, "final": state, "steps": steps, "per_step": per_step,
            "kinds_per_step": kinds_per_step, "first_return": first_return, "kept": kept, "boxes": boxes}


def _box(state, sites) -> dict:
    return {k: tuple(v) for k, v in state.cells.items() if k[:3] in sites}


def _c_image(box: dict, power: int = 1) -> dict:
    mult = group().multiplication
    out = box
    for _ in range(power % 2):
        out = {(x, y, z, mult[14][g]): v for (x, y, z, g), v in out.items()}
    return out


def _restrict(box: dict, sites) -> dict:
    return {k: v for k, v in box.items() if k[:3] in sites}


def check_boxes(entry: dict, measured: dict) -> list[str]:
    fails = []
    boxes = measured.get("boxes", {})
    for b in entry.get("box_checks", []):
        sites = {tuple(x) for x in b["sites"]}
        if b["type"] == "periodic":
            P, t0, t1 = b["period"], b["from"], b["to"]
            series = [_restrict(boxes[t], sites) for t in range(t0, t1 + 1)]
            if not any(v[0] or v[1] for v in series[0].values()):
                fails.append(f"{b['label']}: no counters in the box at t={t0}")
            if any(series[i] != series[i + P] for i in range(len(series) - P)):
                fails.append(f"{b['label']}: box not {P}-periodic on [{t0},{t1}]")
            if P > 1 and all(series[i] == series[i + 1] for i in range(len(series) - 1)):
                fails.append(f"{b['label']}: box is static, not a clock")
        elif b["type"] == "c_image":
            t0, T, k = b["t0"], b["lap"], b["laps"]
            base = _restrict(boxes[t0], sites)
            if _restrict(boxes[t0 + T], sites) == base:
                fails.append(f"{b['label']}: box returns after one lap (no 720-degree behaviour)")
            for j in range(1, k + 1):
                if _restrict(boxes[t0 + j * T], sites) != _c_image(base, j):
                    fails.append(f"{b['label']}: lap {j} is not C^{j} of t0={t0}")
                    break
        else:
            fails.append(f"unknown box check type {b['type']}")
    return fails


def check(entry: dict, measured: dict) -> list[str]:
    """Generic signature checks; returns a list of failure messages (empty = pass)."""
    fails = []
    sig = entry.get("signature", {})
    steps = measured["steps"]
    fr = measured["first_return"]
    if state_hash(measured["final"]) != entry["final_state_sha256"]:
        fails.append("final state hash differs")
    period = sig.get("period")
    if period is not None and period <= steps and fr != period:
        fails.append(f"first return {fr} != declared period {period}")
    trans = sig.get("translation")
    if trans:
        T, v = trans["period"], trans["shift"]
        if T <= steps and measured["kept"][T].cells != _shift(measured["initial"], v):
            fails.append(f"S({T}) is not S(0) shifted by {v}")
    if sig.get("silent") and sum(measured["per_step"]) != 0:
        fails.append("declared silent but clicks occur")
    span = period if period is not None else (trans["period"] if trans else None)
    if span is not None and span <= steps:
        if sig.get("clicks_per_period") is not None and sum(measured["per_step"][:span]) != sig["clicks_per_period"]:
            fails.append("clicks per period differ")
        if sig.get("kinds_per_period") is not None:
            total = Counter()
            for c in measured["kinds_per_step"][:span]:
                total.update(c)
            if {k: v for k, v in total.items() if v} != {k: v for k, v in sig["kinds_per_period"].items() if v}:
                fails.append(f"kinds per period {dict(total)} != {sig['kinds_per_period']}")
    first = sig.get("clicks_first")
    if first is not None and measured["per_step"][:len(first)] != list(first):
        fails.append("clicks of the first updates differ")
    nrw = sig.get("no_return_within")
    if nrw is not None and fr is not None and fr <= min(nrw, steps):
        fails.append(f"returned at {fr} although declared not to return within {nrw}")
    fails.extend(check_boxes(entry, measured))
    return fails


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    catalog = load_catalog()
    entries = catalog["entries"]
    if "--list" in argv:
        for e in entries:
            print(f"{e['name']:55s} {e['group']:28s} {e['file']}")
        return 0
    names = [a for a in argv if not a.startswith("--")]
    if names:
        unknown = set(names) - {e["name"] for e in entries}
        if unknown:
            raise SystemExit(f"unknown block(s): {sorted(unknown)}")
        entries = [e for e in entries if e["name"] in names]
    if "--quick" in argv:
        entries = [e for e in entries if not e.get("heavy")]
    passed, failed = 0, []
    start = time.time()
    for e in entries:
        path = HERE / e["file"]
        if file_sha256(path) != e["file_sha256"]:
            failed.append((e["name"], ["init file hash differs"]))
            continue
        fails = check(e, replay(e))
        if fails:
            failed.append((e["name"], fails))
        else:
            passed += 1
    for name, fails in failed:
        print(f"FAIL {name}: {'; '.join(fails)}")
    print(f"{passed}/{len(entries)} blocks pass ({time.time() - start:.0f} s); "
          f"native Engine, exact inverse at every update")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
