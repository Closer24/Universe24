"""Hand X2: every place that reads or writes a Link's number (the owner's addition of 2026-10-25: the act on the Link
is one generic atomic act in one place).

A place is a function that reads a neighbour's integer through a Port (a call of arrival, shifted, ports, roll,
np.roll, slices (the Link's two ends by slices), ported, frame_of, ports_of, opposite) or that is one of the named Link
readings (the Link factor, the tension, the Link pace, the current, the Link's phase pair and count, the odd line on
the Link, the one-Link read, the take across the Link, the Link birth's two ends, the horizon). Counted by the syntax
tree per function: the Port reads inside it and the named Link functions it calls.

Usage: python link_places.py <root> <subdir> <out.json>
"""
import ast
import json
import sys
from pathlib import Path

PORT_READS = ("arrival", "shifted", "ports", "roll", "slices", "ported", "frame_of", "ports_of", "opposite", "frame_nodes")
LINK_NAMES = ("link_factor", "link_factors", "link_tension", "link_tensions", "link_pace", "link_pace_of", "axis_pace",
              "axis_paces", "current", "momentum_terms", "tension", "stress", "sense_current_of", "currents_of",
              "stresses_of", "axis_sources_of", "axis_neighbours", "momentum_of", "link_levels", "link_wall", "link_guard",
              "link_pairs", "sign_pairs", "phase_links", "frame_signs", "frames_of", "phase_counts", "link_fluxes",
              "turned_link_fluxes", "gathered_line", "gathered_plane", "lattice_of", "taken_at", "horizon_ports",
              "frames", "link_phases", "centred_count", "tensions", "read_number", "framed", "fold")


def calls_in(node):
    found = []
    for inner in ast.walk(node):
        if isinstance(inner, ast.Call):
            callee = inner.func
            name = callee.id if isinstance(callee, ast.Name) else (callee.attr if isinstance(callee, ast.Attribute) else "")
            if name in PORT_READS or name in LINK_NAMES:
                found.append((inner.lineno, name))
    return found


def main():
    root, sub, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    base = root / sub
    places = []
    for path in sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        rel = str(path.relative_to(base))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                own_calls = calls_in(node)
                is_link_function = node.name in LINK_NAMES
                if own_calls or is_link_function:
                    ports = sorted({(l, n) for l, n in own_calls if n in PORT_READS})
                    named = sorted({(l, n) for l, n in own_calls if n in LINK_NAMES})
                    places.append({"file": rel, "function": node.name, "start": node.lineno, "end": node.end_lineno,
                                   "lines": node.end_lineno - node.lineno + 1, "port_reads": ports, "link_calls": named,
                                   "is_link_function": is_link_function})
    total_lines = sum(p["lines"] for p in places)
    port_read_calls = sum(len(p["port_reads"]) for p in places)
    report = {"subdir": sub, "places": len(places), "lines": total_lines, "port_read_calls": port_read_calls,
              "files": sorted({p["file"] for p in places}), "list": places}
    Path(out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{sub}: {len(places)} functions read or write a Link's number, {total_lines} lines, {port_read_calls} Port reads, in {len(report['files'])} files")
    for p in places:
        print(f"  {p['file']}:{p['function']} {p['start']}-{p['end']} ({p['lines']}) ports {[n for _l, n in p['port_reads']]} links {[n for _l, n in p['link_calls']]}")


if __name__ == "__main__":
    main()
