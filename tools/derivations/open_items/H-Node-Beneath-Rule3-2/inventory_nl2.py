"""The inventory of every function of src/event_universe (the Reader's modules left out: board, clicks, decoder, events, gates, predicates, circle) by role with its line count (H-Node-Beneath-Rule3-2): ACT (the law's act, the primitive or composition named), REC (record-keeping: the log, the frame, the census, the counts, the hashes, the state's containers), REF (a refusal by name), READ (a reading, no state move), SECOND (a second road to an act already written, the audit's kind), WRAP (a name for a composition). The roles are read by hand from the code; the line counts by ast. Prints the table (Markdown) and the sums per role and per module.

Usage: python inventory_nl2.py <worktree> <out dir>
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

worktree, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
root = worktree / "src" / "event_universe"
SKIP = {"board.py", "clicks.py", "decoder.py", "events.py", "gates.py", "predicates.py", "circle.py", "__init__.py"}

# file: {name: role or [roles in order of appearance]}; a role "ACT:<what>" names the primitive (P1 the carried division, P2 the slot exchange with the mirror, P3 the lay) or the composition
ROLES: dict[str, dict[str, object]] = {
    "bodies.py": {"bodies": "READ", "frame_of": "READ", "bilinears_of": "READ", "credit": "REC"},
    "close.py": {"Birth(class)": "REC", "Kid(class)": "REC", "refused": "REF", "list_of": "READ", "meet": "READ", "refuse": "REF", "births": "WRAP", "child_laid": "ACT:P3", "children": "REC", "click": "WRAP"},
    "core/paces.py": {"rounded": "READ", "odd_rounded": "READ", "sine_den": "READ", "Side(class)": "READ", "sides": "READ", "certified": "REF", "side_of": "READ", "clock": "READ", "link_pace": "READ", "frozen_content": "READ", "looked_up": "READ", "clock_of": "READ", "link_pace_of": "READ", "reach": "READ", "undecided": "REF"},
    "core/ports.py": {"shifted": "READ", "port_of": "READ", "wrap": "READ", "across": "READ"},
    "core/rule3.py": {"Rule(class)": "READ", "wall_of": "READ", "mass": "READ", "rule_integers": "READ", "link_factor": "READ", "scaled": "READ", "carried_division": "ACT:P1", "flux_total": "READ", "rule3": "WRAP", "division_forward": "WRAP", "link_unit_of": "READ", "held_wall": "READ", "held_numerator": "READ", "unit_of": "READ", "mirrored": "ACT:P2 mirror", "signed_quotient": "WRAP", "half": "WRAP", "odd": "WRAP", "share_weight": "READ", "quotient": "WRAP", "remainder": "WRAP", "lattice": "READ", "least_root": "READ", "balanced_pair": "READ", "largest_below": "READ", "form_term": "READ"},
    "draw.py": {"read_number": "READ"},
    "gram.py": {"identity": "READ", "gram": "READ", "rotation": "READ", "conjugation": "READ", "axes": "READ", "scale": "READ", "matvec": "READ", "matmul": "READ", "weighted": "READ", "form": "READ", "charge": "READ", "conjugated": "READ", "current": "READ", "density": "READ", "curl": "READ", "term": "READ", "share": "READ", "moving": "READ", "rest": "WRAP", "cosine_count": "READ", "period": "READ", "levels": "READ"},
    "interval.py": {"laid_on": "REC", "Interval(class)": "REC", "run": "WRAP", "__init__": "REC", "at": "READ", "lines": "WRAP", "ends": "WRAP", "mean_wall": "READ", "readings": "READ", "kick": "ACT:P1 (the charge's write) + reads", "division": "ACT:P1 P2 P3 (act, ride, lays)", "lays": "ACT:P1 P3 (write)", "swap": "WRAP", "close": "REC"},
    "links.py": {"coupling_of": "READ", "cross": "READ", "turn_pair": "READ", "Link(class)": "READ", "links_of": "READ", "link": "READ", "link_wall": "READ", "turned": "READ", "gradient": "READ", "wronskian": "READ", "plane_current": "SECOND", "link_current": "READ", "row_current": "READ", "row_twist": "READ", "net_current": "READ", "twist": "SECOND", "__init__": "READ"},
    "loader/world.py": {"refused_keys": "REF", "read_world": "REF", "load_world": "READ"},
    "merger.py": {"child_at": "ACT:P3 + booking", "walls_of": "READ", "products": "SECOND", "share_at": "SECOND", "share_fall": "READ", "levels_at": "READ", "read_ends": "READ", "write_ends": "ACT:P1 P3 (move, lay) + log", "takes": "WRAP", "summed": "REC", "rise_of": "SECOND", "light_children": "ACT:P1 P3", "rise": "SECOND"},
    "metric.py": {"stress_parts": "READ", "shear_parts": "READ", "tensor_parts": "READ", "net_flux": "READ", "rotation_of": "READ", "fold_links": "READ"},
    "node.py": {"bits_of": "REC", "Node(class)": "REC", "__init__": "REF", "start_state": "REC", "ride_walls": "READ", "node_of": "REF", "row": "WRAP", "emitter": "WRAP", "records": "WRAP", "rule": "WRAP", "rule_of": "READ", "content": "WRAP", "link_factors": "WRAP", "share": "WRAP", "turned_arrival": "READ", "arrivals": "READ", "rotate": ["ACT:P1 + shift (P2 P3)", "WRAP"], "write": ["ACT:P1 P3", "WRAP"], "act": "ACT:P1 P2 P3", "restore": "REC", "rows": "WRAP", "set_rows": "WRAP", "all_lines": "WRAP", "is_im": "READ", "exchange": "ACT:P2", "swap": "ACT:P2 + the peak read", "read_lines": "READ", "digit_of": "WRAP", "run": "WRAP", "click": "WRAP", "lay": "WRAP", "step": "WRAP", "step_back": "WRAP", "arrays": "REC", "census": "REC", "state_bytes": "REC", "state_hash": "REC"},
    "quartet.py": None,
    "readings.py": None,
    "rows.py": {"zeros": "REC", "Row(class)": "REC", "Line(class)": "REC", "write_walls": "READ", "lines_of": "REC", "order_key": "READ", "rows_of": "REF", "row_of": "WRAP", "walled_of": "WRAP", "records_of": "WRAP", "__init__": ["REC", "REC"], "gap": "READ", "copy": "REC"},
    "run.py": None,
    "seed.py": {"lay_world": "ACT:P3 + refusals", "raised_cosine": "READ", "offsets": "READ", "envelope_of": "READ", "circle_point": "READ", "axis_pairs": "READ", "phase_of": "READ", "phases_of": "READ", "running_rotation": "READ", "rest_record": "READ", "uniform_levels": "READ", "share_at_node": "WRAP", "lay_uniform": "ACT:P3 + search", "packet_share": "WRAP", "fitted": "SECOND", "wave_of": "READ", "lay_packet": "ACT:P3", "share_of": "WRAP"},
    "take.py": {"neighbour": "READ", "frame_nodes": "READ", "at_node": "READ", "fall_of": "READ", "lay": "ACT:P3", "momentum_of": "REC", "move": "ACT:P1 P3", "fall": "READ"},
    "wave.py": {"cycle_phases": "READ", "cycle_levels": "READ", "lay_cycle": "ACT:P3 + search", "least_share": "SECOND"},
}
WHOLE = {"quartet.py": "READ", "readings.py": "READ", "run.py": "REC"}  # every function of the module one role

rows = []
per_role: dict[str, int] = {}
per_module: dict[str, dict[str, int]] = {}
headers = 0
for path in sorted(root.rglob("*.py")):
    if path.name in SKIP:
        continue
    rel = str(path.relative_to(root))
    text = path.read_text()
    tree = ast.parse(text)
    seen: dict[str, int] = {}
    def_lines = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.ClassDef):
            methods = sum(x.end_lineno - x.lineno + 1 for x in node.body if isinstance(x, ast.FunctionDef))
            name, lines = node.name + "(class)", node.end_lineno - node.lineno + 1 - methods
        else:
            name, lines = node.name, node.end_lineno - node.lineno + 1
        def_lines += lines
        if rel in WHOLE:
            role = WHOLE[rel]
        else:
            found = ROLES[rel][name]
            if isinstance(found, list):
                role = found[seen.get(name, 0)]
                seen[name] = seen.get(name, 0) + 1
            else:
                role = found
        kind = role.split(":")[0]
        rows.append((rel, name, node.lineno, lines, role))
        per_role[kind] = per_role.get(kind, 0) + lines
        module = per_module.setdefault(rel, {})
        module[kind] = module.get(kind, 0) + lines
    headers += len(text.splitlines()) - def_lines
    per_module.setdefault(rel, {})["header"] = len(text.splitlines()) - def_lines

rows.sort(key=lambda r: (r[0], r[2]))
table = ["| module | function | line | lines | role |", "|---|---|---|---|---|"]
table += [f"| {m} | {n} | {ln} | {c} | {r} |" for m, n, ln, c, r in rows]
sums = {"per_role": per_role, "headers (imports, constants, module docstrings)": headers, "functions": sum(r[3] for r in rows), "per_module": per_module}
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "inventory_table.md").write_text("\n".join(table) + "\n")
(out_dir / "inventory_sums.json").write_text(json.dumps(sums, indent=1) + "\n")
print(json.dumps({"per_role": per_role, "headers": headers, "functions": sums["functions"], "count": len(rows)}))
for m in sorted(per_module):
    print(m, json.dumps(per_module[m]))
