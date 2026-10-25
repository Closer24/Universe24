"""(c) The acts on the three shapes (BRIEF_u, item (c); ALGEBRA.md, The Node: Every act of the Node is one act on every row alike; The two kinds of act): every branch in src/event_universe whose test names a row's kind or identity (the attributes wronskian, rotation, plane, quanta, held, motion_volume, axes, flux, turns(...), charged(...), world.seed), counted per file by the syntax tree (if, while, ternary, comprehension conditions, boolean short-circuits), with the line numbers; and the functions of each act named by the brief verified present in the tree (a count of definitions found). Integers only.

Run: PYTHONPATH=<worktree>/src python tools/derivations/u2/c_acts_by_kind.py
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

from u2lib import ROOT, write

KIND_NAMES = ("wronskian", "rotation", "plane", "quanta", "held", "motion_volume", "axes", "flux")
KIND_CALLS = ("turns", "charged", "reads_content", "carried")
PACKAGE = ROOT / "src" / "event_universe"

ACTS = {
    "the held write (act(rows): the metric from every row's form and stresses, the potential from every plane's Wronskian and currents)": [
        ("records.py", "write_sources"),
        ("records.py", "scaled_sum"),
        ("records.py", "pressure_term"),
        ("records.py", "form"),
        ("records.py", "wronskian"),
        ("features/held_write/__init__.py", "held_write"),
        ("node.py", "held_write_at"),
        ("lattice.py", "Lattice.held_write"),
        ("bookings.py", "booked_of"),
        ("readings.py", "axis_sources_of"),
        ("readings.py", "stresses_of"),
        ("readings.py", "sense_current_of"),
        ("features/currents/__init__.py", "tension"),
        ("features/currents/__init__.py", "current"),
    ],
    "the rotation, Rule3 on every line (act(row))": [
        ("core/rule3.py", "rule3"),
        ("core/rule3.py", "carried_division"),
        ("flux.py", "step_line"),
        ("flux.py", "step_plane"),
        ("flux.py", "step_momentum"),
        ("flux.py", "step_family"),
        ("flux.py", "step_records"),
        ("flux.py", "link_fluxes"),
        ("flux.py", "turned_link_fluxes"),
    ],
    "the planes' phase read from the potential (the Link's pair)": [
        ("node.py", "turning"),
        ("node.py", "clocked_potentials"),
        ("node.py", "phase_counts"),
        ("node.py", "phase_carried"),
        ("node.py", "phased"),
        ("plane.py", "link_levels"),
        ("plane.py", "sign_pairs"),
        ("plane.py", "phase_links"),
        ("plane.py", "link_pairs"),
        ("features/phase/__init__.py", "iterate"),
        ("features/phase/__init__.py", "fold"),
        ("core/paces.py", "turn_factor"),
    ],
    "the planes' arrivals turned by the metric's lines (the paces, the Link factor)": [
        ("node.py", "read"),
        ("node.py", "read_lines"),
        ("node.py", "rulers"),
        ("node.py", "rule_of"),
        ("features/read/__init__.py", "content_of"),
        ("features/read/__init__.py", "link_tensions"),
        ("features/read/__init__.py", "link_factors"),
        ("features/read/__init__.py", "axis_paces"),
        ("core/paces.py", "node_paces"),
        ("core/paces.py", "clock_of"),
        ("core/paces.py", "link_pace_of"),
        ("core/rule3.py", "rule_integers"),
        ("core/rule3.py", "link_factor"),
        ("features/volume/__init__.py", "level_of"),
    ],
}


def names_in(test: ast.AST) -> list[str]:
    found = []
    for node in ast.walk(test):
        if isinstance(node, ast.Attribute) and node.attr in KIND_NAMES:
            found.append(node.attr)
        if isinstance(node, ast.Attribute) and node.attr == "seed" and isinstance(node.value, ast.Attribute) and node.value.attr == "world":
            found.append("world.seed")
        if isinstance(node, ast.Call):
            callee = node.func
            name = callee.id if isinstance(callee, ast.Name) else (callee.attr if isinstance(callee, ast.Attribute) else "")
            if name in KIND_CALLS:
                found.append(name + "()")
    return found


def branches(path: Path) -> list[dict]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        tests: list[tuple[str, ast.AST]] = []
        if isinstance(node, ast.If | ast.While):
            tests.append(("if" if isinstance(node, ast.If) else "while", node.test))
        elif isinstance(node, ast.IfExp):
            tests.append(("ternary", node.test))
        elif isinstance(node, ast.comprehension):
            tests.extend(("comprehension", t) for t in node.ifs)
        elif isinstance(node, ast.BoolOp):
            tests.append(("boolop", node))
        for shape, test in tests:
            names = names_in(test)
            if names:
                found.append({"line": getattr(test, "lineno", getattr(node, "lineno", 0)), "shape": shape, "names": sorted(set(names))})
    return found


def definitions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            found.add(node.name)
        if isinstance(node, ast.ClassDef):
            for inner in node.body:
                if isinstance(inner, ast.FunctionDef):
                    found.add(f"{node.name}.{inner.name}")
    return found


def main() -> None:
    per_file = {}
    total = 0
    for path in sorted(PACKAGE.rglob("*.py")):
        found = branches(path)
        # a BoolOp inside an If's test is counted once with the If: drop boolops whose line is already listed
        lines_seen = set()
        kept = []
        for entry in sorted(found, key=lambda e: (e["line"], e["shape"] == "boolop")):
            if entry["shape"] == "boolop" and entry["line"] in lines_seen:
                continue
            lines_seen.add(entry["line"])
            kept.append(entry)
        if kept:
            per_file[str(path.relative_to(PACKAGE))] = kept
            total += len(kept)
    acts = {}
    missing = 0
    for act, places in ACTS.items():
        verified = []
        for file, name in places:
            present = name in definitions(PACKAGE / file)
            missing += not present
            verified.append({"file": file, "function": name, "present": present})
        acts[act] = verified
    by_name: dict[str, int] = {}
    for entries in per_file.values():
        for entry in entries:
            for name in entry["names"]:
                by_name[name] = by_name.get(name, 0) + 1
    report = {
        "branches_on_a_rows_kind_total": total,
        "branches_by_attribute": dict(sorted(by_name.items())),
        "branches_per_file": {k: len(v) for k, v in per_file.items()},
        "branches_listed": per_file,
        "acts_functions": acts,
        "acts_functions_missing": missing,
    }
    write("c_acts_by_kind.json", json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
