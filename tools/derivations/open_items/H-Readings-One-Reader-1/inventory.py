"""The inventory of the readings: every reading function of the Node pair's table (nl1's out/inventory.md on 3dc12e307), grouped by the object it reads, with its callers in src (the act that consumes it) found by a grep of `name(` over src/event_universe; integers only."""

import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
TABLE = Path(sys.argv[2])
OUT = Path(sys.argv[3])

GROUPS = {
    "link": {  # the Link's record F_ij and its parts, read across one Link
        "links.py": ["coupling_of", "cross", "turn_pair", "links_of", "link", "link_wall", "turned", "gradient", "link_current", "row_current", "row_twist", "net_current", "plane_current", "twist"],
        "readings.py": ["link_factors", "frames", "link_phases", "centred_count", "pair_angle"],
        "metric.py": ["fold_links", "rotation_of", "net_flux", "stress_parts", "shear_parts", "tensor_parts"],
        "core/rule3.py": ["link_factor", "link_unit_of"],
    },
    "gram": {  # the row's shape: the bilinear form with the axis matrices
        "gram.py": ["identity", "gram", "rotation", "conjugation", "axes", "scale", "matvec", "matmul", "weighted", "form", "charge", "conjugated", "current", "density", "curl", "term", "share", "moving", "rest", "cosine_count", "period", "levels"],
        "links.py": ["wronskian"],
        "quartet.py": ["*"],
        "node.py": ["is_im"],
    },
    "rule": {  # the file's constants and the paces: Rule3's integers of a pair at the content
        "core/rule3.py": ["Rule", "wall_of", "mass", "rule_integers", "scaled", "held_wall", "held_numerator", "unit_of", "share_weight", "lattice", "balanced_pair", "largest_below", "form_term", "least_root", "flux_total"],
        "core/paces.py": ["sine_den", "Side", "sides", "side_of", "clock", "link_pace", "frozen_content", "looked_up", "clock_of", "link_pace_of", "reach", "undecided"],
        "readings.py": ["paces_of", "frozen_of", "content", "floor"],
        "node.py": ["rule", "rule_of"],
        "interval.py": ["Interval", "at", "mean_wall", "readings"],
        "core/ports.py": ["shifted", "across"],
        "rows.py": ["write_walls", "lines_of", "order_key"],
    },
    "carrier": {  # the carrier's lines and the click's readers
        "node.py": ["turned_arrival", "arrivals"],
        "close.py": ["list_of", "meet"],
        "merger.py": ["walls_of", "share_fall", "levels_at", "read_ends", "share_at", "products", "rise_of", "rise"],
        "take.py": ["fall_of"],
        "draw.py": ["read_number"],
        "bodies.py": ["frame_of"],
    },
    "seed": {  # the seed's envelopes, read once at the load
        "seed.py": ["*"],
        "wave.py": ["cycle_phases", "cycle_levels", "least_share"],
    },
}

rows = []
for line in TABLE.read_text().splitlines():
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 6 and cells[5] in ("reading", "second") and cells[2].isdigit():
        rows.append(cells)

code = {}
for p in SRC.rglob("*.py"):
    code[str(p.relative_to(SRC))] = p.read_text()


def group_of(module, name):
    for g, mods in GROUPS.items():
        names = mods.get(module, [])
        if "*" in names or name in names:
            return g
    return "other"


def callers(name):
    found = {}
    pat = re.compile(r"\b" + re.escape(name) + r"\(")
    for mod, text in code.items():
        for k, ln in enumerate(text.splitlines(), 1):
            if pat.search(ln) and not ln.lstrip().startswith("def " + name) and not ln.lstrip().startswith('"""'):
                found.setdefault(mod, []).append(k)
    return found


sums = {}
lines_out = ["| group | module | function | line | lines | callers (module:lines) |", "| --- | --- | --- | --- | --- | --- |"]
by_group = {}
for module, name, line, n, n_less, role in rows:
    g = group_of(module, name)
    by_group.setdefault(g, []).append((module, name, int(line), int(n), role))
for g in ("link", "gram", "rule", "carrier", "seed", "other"):
    total = 0
    for module, name, line, n, role in sorted(by_group.get(g, [])):
        total += n
        c = callers(name)
        cs = "; ".join(f"{m}:{','.join(str(x) for x in ls[:6])}" for m, ls in sorted(c.items()))
        tag = " (second)" if role == "second" else ""
        lines_out.append(f"| {g} | {module} | {name}{tag} | {line} | {n} | {cs or 'NONE'} |")
    sums[g] = (len(by_group.get(g, [])), total)
lines_out.append("")
lines_out.append("| group | functions | lines |")
lines_out.append("| --- | --- | --- |")
grand = [0, 0]
for g, (k, n) in sums.items():
    lines_out.append(f"| {g} | {k} | {n} |")
    grand[0] += k
    grand[1] += n
lines_out.append(f"| total | {grand[0]} | {grand[1]} |")
OUT.write_text("\n".join(lines_out) + "\n")
print("\n".join(lines_out[-8:]))
