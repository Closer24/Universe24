"""The inventory of every function of src/event_universe (the Reader's modules left out), each tagged by role with its lines (whole, and without its docstring), the sums per role (H-Node-Beneath-Rule3-1)."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

LEFT_OUT = {"board.py", "clicks.py", "decoder.py", "events.py", "gates.py", "predicates.py", "circle.py"}
ROLES = ("act", "record", "refusal", "reading", "second", "wrapper", "state")
# the roles: act (the law's act: P1 the carried division with the direction, P2 the slot exchange with the mirror,
# P3 the lay on a slot), record (the log, the frame, the census, the hashes, the counts), refusal (by name),
# reading (no state move), second (a second road), wrapper (a name for a composition), state (the integers' holder)
DEFAULT = {
    "core/rule3.py": "reading",
    "core/ports.py": "reading",
    "core/paces.py": "reading",
    "node.py": "wrapper",
    "interval.py": "reading",
    "take.py": "wrapper",
    "close.py": "reading",
    "merger.py": "reading",
    "links.py": "reading",
    "rows.py": "reading",
    "gram.py": "reading",
    "metric.py": "reading",
    "seed.py": "reading",
    "wave.py": "reading",
    "bodies.py": "reading",
    "readings.py": "reading",
    "run.py": "record",
    "quartet.py": "reading",
    "draw.py": "reading",
    "loader/world.py": "refusal",
    "features/phase.py": "reading",
    "features/volume.py": "reading",
    "features/click.py": "reading",
}
TAGS = {
    "core/rule3.py": {
        "carried_division": "act:P1",
        "rule3": "act:P1",
        "mirrored": "act:P2",
        "division_forward": "wrapper",
        "signed_quotient": "wrapper",
        "half": "wrapper",
        "odd": "wrapper",
        "quotient": "wrapper",
        "remainder": "wrapper",
        "least_root": "second",
        "largest_below": "reading",
        "balanced_pair": "reading",
    },
    "core/ports.py": {"port_of": "wrapper", "wrap": "wrapper", "across": "reading"},
    "core/paces.py": {"rounded": "wrapper", "odd_rounded": "wrapper", "certified": "refusal"},
    "node.py": {
        "bits_of": "record",
        "__init__": "refusal",
        "start_state": "record",
        "ride_walls": "act:P3",
        "node_of": "refusal",
        "rule": "reading",
        "rule_of": "reading",
        "turned_arrival": "reading",
        "arrivals": "reading",
        "rotate": "act:P1",
        "write": "act:P1",
        "act": "wrapper",
        "restore": "record",
        "exchange": "act:P2",
        "swap": "act:P2",
        "arrays": "record",
        "census": "record",
        "state_bytes": "record",
        "state_hash": "record",
    },
    "interval.py": {
        "laid_on": "record",
        "__init__": "record",
        "readings": "reading",
        "kick": "act:P1",
        "division": "act:P1",
        "lays": "act:P1",
        "swap": "wrapper",
        "close": "record",
        "run": "wrapper",
        "lines": "wrapper",
        "ends": "wrapper",
        "at": "reading",
        "mean_wall": "reading",
    },
    "take.py": {
        "fall_of": "reading",
        "lay": "act:P3",
        "momentum_of": "record",
        "move": "act:P1",
    },
    "close.py": {
        "refused": "refusal",
        "refuse": "refusal",
        "births": "wrapper",
        "child_laid": "act:P3",
        "children": "record",
        "click": "wrapper",
        "Birth": "state",
        "Kid": "state",
    },
    "merger.py": {
        "child_at": "act:P3",
        "products": "second",
        "share_at": "second",
        "write_ends": "act:P1",
        "takes": "wrapper",
        "summed": "record",
        "rise_of": "second",
        "rise": "second",
        "light_children": "act:P3",
    },
    "links.py": {"plane_current": "second", "twist": "second", "Link": "state", "__init__": "state"},
    "rows.py": {
        "zeros": "wrapper",
        "Row": "state",
        "Line": "state",
        "__init__": "state",
        "copy": "state",
        "gap": "state",
        "rows_of": "refusal",
        "row_of": "wrapper",
        "walled_of": "wrapper",
        "records_of": "wrapper",
    },
    "seed.py": {
        "lay_world": "act:P3",
        "lay_uniform": "act:P3",
        "lay_packet": "act:P3",
        "fitted": "second",
        "share_of": "second",
        "share_at_node": "wrapper",
    },
    "wave.py": {"lay_cycle": "act:P3", "least_share": "second"},
    "bodies.py": {"bodies": "wrapper", "bilinears_of": "record", "credit": "act:P1"},
    "run.py": {"main": "wrapper"},
}


def tag_of(module: str, name: str) -> str:
    return TAGS.get(module, {}).get(name, DEFAULT.get(module, "reading"))


def main(root: str) -> None:
    base = Path(root)
    rows = []
    for path in sorted(base.rglob("*.py")):
        rel = str(path.relative_to(base))
        if path.name in LEFT_OUT or path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                whole = node.end_lineno - node.lineno + 1
                doc = 0
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(
                    getattr(node.body[0], "value", None), ast.Constant
                ):
                    first = node.body[0]
                    doc = first.end_lineno - first.lineno + 1
                if isinstance(node, ast.ClassDef):
                    inner = sum(
                        c.end_lineno - c.lineno + 1
                        for c in node.body
                        if isinstance(c, (ast.FunctionDef, ast.ClassDef))
                    )
                    whole -= inner
                rows.append((rel, node.name, node.lineno, whole, whole - doc, tag_of(rel, node.name)))
    sums: dict[str, list[int]] = {}
    lines = ["| module | function | line | lines | lines less docstring | role |", "| --- | --- | --- | --- | --- | --- |"]
    for rel, name, at, whole, code, tag in rows:
        lines.append(f"| {rel} | {name} | {at} | {whole} | {code} | {tag} |")
        role = tag.split(":")[0]
        s = sums.setdefault(role, [0, 0, 0])
        s[0] += 1
        s[1] += whole
        s[2] += code
    lines.append("")
    lines.append("| role | functions | lines | lines less docstring |")
    lines.append("| --- | --- | --- | --- |")
    total = [0, 0, 0]
    for role in ROLES:
        s = sums.get(role, [0, 0, 0])
        lines.append(f"| {role} | {s[0]} | {s[1]} | {s[2]} |")
        total = [a + b for a, b in zip(total, s)]
    lines.append(f"| total | {total[0]} | {total[1]} | {total[2]} |")
    prim: dict[str, list[int]] = {}
    for rel, name, at, whole, code, tag in rows:
        if tag.startswith("act:"):
            p = prim.setdefault(tag[4:], [0, 0, 0])
            p[0] += 1
            p[1] += whole
            p[2] += code
    lines.append("")
    lines.append("| primitive | functions | lines | lines less docstring |")
    lines.append("| --- | --- | --- | --- |")
    for p in sorted(prim):
        lines.append(f"| {p} | {prim[p][0]} | {prim[p][1]} | {prim[p][2]} |")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
