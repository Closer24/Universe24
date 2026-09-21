"""The family table of the register, compiled from its one source (read-only,
the mathematician, 2026-09-21; docs/designs/paper_families/FAMILY_TABLE_AUDIT.md):
every family the shipped definitions declare (examples/events/entities/
families.json, grouped by the entity that declares it: the sets), every family a
world declares inline beyond them, the content every family carries on the
measured events of the worlds (the masses as declared), and the group each
declared quantity lives on. The paper's family table (P8) names the columns;
this script prints the rows. No run.

Run from the repository root:

    python docs/designs/paper_families/family_table.py > docs/designs/paper_families/family_table.out
"""

from __future__ import annotations

import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVENTS = ROOT / "examples" / "events"
DEFINITIONS = json.loads((EVENTS / "entities" / "families.json").read_text("utf-8"))


def key(f: dict) -> tuple:
    return (
        f["name"],
        f.get("quantum"),
        json.dumps(f.get("charge")),
        json.dumps(f.get("columns")),
        f.get("lifetime"),
        f.get("phase"),
        json.dumps(f.get("phase_per_link")),
        f.get("hand"),
    )


def group_of(f: dict) -> str:
    """The group each declared quantity of the family lives on (PREDICTIONS 26):
    the quantised ones on compact groups, the free ones on the scale."""
    parts = []
    parts.append(
        "the content M on the scale (free, an input)"
        if f.get("quantum", 0) == 0
        else f"the quantum h = {f['quantum']} units per unit of amount (E = h f, the click's content in whole turns)"
    )
    c = f.get("charge")
    if c is None:
        parts.append("no charge line")
    elif isinstance(c, list):
        parts.append(f"the charge per unit of content rho = {c[0]}/{c[1]}, a winding on the circle (Z)")
    elif f.get("quantum", 0) == 0:
        parts.append(f"the charge per unit of content rho = {c} (Z)")
    else:
        parts.append(
            f"the whole charge per unit of amount {c} (Z; a paid family's rays push by their label)"
        )
    cols = f.get("columns")
    if cols:
        for name, col in cols.items():
            parts.append(
                f"the column `{name}` sigma = {col.get('value')} with the sign {col.get('sign')} (a signed scalar per unit)"
            )
    if f.get("phase", True):
        parts.append(
            "a phase on the circle Z_N"
            + (f", turning {f.get('phase_per_link')} per Link" if f.get("phase_per_link") else "")
        )
    else:
        parts.append("no phase circle (turns never, clicks by no phase)")
    if f.get("lifetime") is not None:
        parts.append(f"the lifetime L = {f['lifetime']} Links (Z)")
    if f.get("hand") is not None:
        parts.append(f"the hand {f['hand']:+d} (Z_2, the pseudoscalar of the 48)")
    parts.append("its rows' directions on the fan F_P under the 48 signed axis permutations")
    return "; ".join(parts)


print("A. THE SHIPPED DEFINITIONS: THE SETS (the entities) AND THEIR FAMILIES, WITH EVERY DECLARED KEY")
print("| entity (the set) | family | quantum h | charge | columns | lifetime | phase circle | hand |")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")
shipped = {}
for e in DEFINITIONS["entities"]:
    for f in e["families"]:
        shipped[f["name"]] = f
        print(
            f"| `{e['name']}` | `{f['name']}` | {f.get('quantum')} | {json.dumps(f.get('charge')) if f.get('charge') is not None else 'none'} | "
            f"{json.dumps(f.get('columns')) if f.get('columns') else 'none'} | {f.get('lifetime') if f.get('lifetime') is not None else 'for ever'} | "
            f"{'yes' if f.get('phase', True) else 'no'} | {f.get('hand') if f.get('hand') is not None else 'none'} |"
        )
print(
    f"{sum(len(e['families']) for e in DEFINITIONS['entities'])} families in {len(DEFINITIONS['entities'])} entities"
)
print()

print(
    "B. THE FAMILIES THE WORLDS DECLARE INLINE (a declaration that differs from the shipped one, or a name the definitions lack), with the worlds"
)
inline = collections.defaultdict(list)
for p in sorted(EVENTS.rglob("*.json")):
    d = json.loads(p.read_text("utf-8"))
    if "format" in d:
        continue
    for f in d.get("families", []) or []:
        inline[key(f)].append(f"{p.parent.name}/{p.stem}")
print("| family | quantum | charge | columns | lifetime | phase | phase_per_link | hand | worlds |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for k in sorted(inline, key=lambda t: (t[0], str(t))):
    worlds = inline[k]
    same_as_shipped = k[0] in shipped and key(shipped[k[0]]) == k
    print(
        f"| `{k[0]}`{'' if not same_as_shipped else ' (as shipped)'} | {k[1]} | {k[2]} | {k[3]} | {k[4]} | {k[5]} | {k[6]} | {k[7]} | {len(worlds)}: {', '.join(worlds[:3])}{'...' if len(worlds) > 3 else ''} |"
    )
print()

print(
    "C. THE CONTENT EVERY FAMILY CARRIES ON THE WORLDS' MEASURED EVENTS (the masses as declared; `held` beside)"
)
amounts = collections.defaultdict(lambda: collections.defaultdict(set))
held = collections.defaultdict(lambda: collections.defaultdict(set))
for p in sorted(EVENTS.rglob("*.json")):
    d = json.loads(p.read_text("utf-8"))
    if "format" in d:
        continue
    for m in d.get("measured", []):
        amounts[m["family"]][m["amount"]].add(p.parent.name)
        for fam, c in (m.get("held") or {}).items():
            held[fam][c].add(p.parent.name)
print("| family | the amounts declared (series) |")
print("| --- | --- |")
for fam in sorted(amounts):
    cells = "; ".join(f"{a} ({', '.join(sorted(s))})" for a, s in sorted(amounts[fam].items()))
    print(f"| `{fam}` | {cells} |")
print(
    "| held | "
    + "; ".join(f"`{f}` {c} ({', '.join(sorted(s))})" for f, v in held.items() for c, s in v.items())
    + " |"
)
print()

print(
    "D. THE GROUP EACH DECLARED QUANTITY LIVES ON, PER SHIPPED FAMILY OF THE PHYSICS (the apparatus materials and the star sources listed once)"
)
physics = [
    "light",
    "e",
    "beta",
    "p",
    "n",
    "nuclear",
    "bond",
    "u",
    "glue",
    "nu",
    "nubar",
    "w",
    "m",
    "mass",
    "probe",
    "q",
    "d",
]
for name in physics:
    f = shipped[name]
    print(f"- `{name}`: {group_of(f)}")
print(
    "- the apparatus materials (`wall`, `screen`, `counter`, `apparatus`, `carrier`, `detector`): paid, h = 1, no charge, a phase circle, the click's readers"
)
print(
    "- the sources (`s`, `sa`, `sb`, the 24 `thrown_sources`, the 24 `hubble_stars`): free or paid sources of the register's throws, no charge"
)
print()

print("E. THE STATE VECTOR PER KIND (what a row and a body carry, ENGINE.md and LAW.md section 1)")
print(
    "- a row: its Node (Z^3 on the box), its direction (a primitive vector of the fan F_P), its age (Z), its phase (Z_N), its number (the family), its amount, its content per unit; under a record its identity, its label (bits, one per arm), its multiplicity and its birth phase u (Z_W); its momentum label amount x u_d at the scale Q (a vector of label units)"
)
print(
    "- a body (a measured event): its Node, its content M, its momentum vector p (label units), its charge per column (rho x M), its held content per family, its table of counts (one accumulator per count: the drive, the clock, the wheel, the action), its set of Nodes (`span`)"
)
print(
    "- the six verbs on these: the translation, the bilinear form, the group-ring addition on Z[Z_N], the permutation (the 48), the evaluation (the tables), the Euclidean division with the remainder kept"
)
