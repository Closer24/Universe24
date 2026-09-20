"""Rewrite ray worlds to the form of 2026-09-20: the kind of a family derived
from its quantum, only the table entries that differ from the default, and
the charge per unit of content on the family.

The model owner's decisions of 2026-09-19 (Highlights 5.4, "I approve 1 and
3") and of 2026-09-20 (charge is per unit of content of a family;
docs/MIGRATION.md): the table of a measured event is generated from the
families' keys (`world.default_table`: a free family is read, a paid one
measured, no window), and a world declares only what differs; the key `kind`
is refused, the quantum decides (0 free, 1 or more paid); a measured event
declares no `charge`, its family declares the charge per unit of content as
an integer or a pair `[n, d]`. This tool rewrites a world file in place, or
prints the rewritten document with `--check`, changing nothing physical:

- a family's `kind` becomes its `quantum` at the same place (free: 0; paid:
  the declared quantum or 1); a family without either is refused;
- a measured event's `charge` becomes its family's `charge`, the reduced
  pair [charge // g, amount // g] with g the greatest common divisor (a
  charge of 0 is dropped; a whole per-unit charge stays an integer); when
  two measured events of one family imply different pairs, or the family
  already declares another, the file is refused naming them: the world
  must split the family first (as `examples/events/coupling/make_worlds.py`
  does for item 7, the families `q` and `p`);
- a table entry equal to the default for its family is dropped (the rule
  string, or the object with the default rule, no window and the default
  `reads`); inside a kept object the default `rule` is dropped; an empty
  `table` is dropped;
- the file keeps its own style: compact on one line, or indented by two,
  with its trailing newline.

An entity definitions file (`format` `event-entities-v1`) declares no
families and is left as it is: its tables are the apparatus's, read against
the families of the world that places it.

    PYTHONPATH=src python tools/migrate_ray_worlds.py examples/events/*.json
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from pathlib import Path

from event_universe.events.world import (
    FREE_QUANTUM,
    KIND_KEY,
    FamilyDefinition,
    default_reads,
    default_rule,
)

Json = dict[str, object]


def migrate_family(entry: Json) -> Json:
    """The family with its quantum in place of its kind."""
    if KIND_KEY not in entry:
        if "quantum" not in entry:
            raise ValueError(f"family {entry.get('name')!r} declares neither kind nor quantum")
        return dict(entry)
    kind = entry[KIND_KEY]
    if kind not in ("free", "paid"):
        raise ValueError(f"family {entry.get('name')!r} has an unknown kind {kind!r}")
    quantum = FREE_QUANTUM if kind == "free" else int(str(entry.get("quantum", 1)))
    found: Json = {}
    for key, value in entry.items():
        if key == KIND_KEY:
            found["quantum"] = quantum
        elif key != "quantum":
            found[key] = value
    return found


def trim_entry(value: object, rule: str) -> object | None:
    """The entry with what equals the default removed; None if nothing is left."""
    if isinstance(value, str):
        return None if value == rule else value
    if not isinstance(value, dict):
        return value
    kept = dict(value)
    entry_rule = str(kept.get("rule", rule))
    if entry_rule == rule:
        kept.pop("rule", None)
    if kept.get("reads") == default_reads(entry_rule):
        kept.pop("reads", None)
    return kept or None


def charge_pair(value: object, label: str) -> tuple[int, int]:
    """A declared family charge as the pair (n, d): an integer c is (c, 1)."""
    if isinstance(value, bool) or (not isinstance(value, int) and not isinstance(value, list)):
        raise ValueError(f"{label}: charge must be an integer or [numerator, denominator]")
    if isinstance(value, int):
        return value, 1
    if len(value) != 2 or any(isinstance(v, bool) or not isinstance(v, int) for v in value):
        raise ValueError(f"{label}: charge must be an integer or [numerator, denominator]")
    return int(value[0]), int(value[1])


def charge_per_unit(charge: int, amount: int) -> tuple[int, int]:
    """The reduced pair of a whole charge on a content."""
    common = math.gcd(abs(charge), amount) or 1
    return charge // common, amount // common


def migrate_charges(families: list[Json], measured: list[object]) -> None:
    """Move every measured event's `charge` to its family as the charge per
    unit of content; refuse a family whose events imply different pairs."""
    by_name = {str(family["name"]): family for family in families}
    implied: dict[str, tuple[tuple[int, int], str]] = {}
    for index, entry in enumerate(measured):
        if not isinstance(entry, dict) or "charge" not in entry:
            continue
        label = f"measured[{index}]"
        charge = entry.pop("charge")
        if isinstance(charge, bool) or not isinstance(charge, int):
            raise ValueError(f"{label}: a measured event's charge was a whole integer")
        amount = entry.get("amount")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 1:
            raise ValueError(f"{label}: amount must be a positive integer")
        name = str(entry.get("family"))
        if name not in by_name:
            raise ValueError(f"{label}: names an unknown family {name!r}")
        pair = charge_per_unit(int(charge), int(amount))
        if pair == (0, 1):
            continue
        if name in implied and implied[name][0] != pair:
            raise ValueError(
                f"{label} implies the charge per unit of content {list(pair)} for the family "
                f"{name!r} where {implied[name][1]} implied {list(implied[name][0])}: split the "
                "family before migrating (one charge per unit of content per family)"
            )
        implied[name] = (pair, label)
    for name, (pair, label) in implied.items():
        family = by_name[name]
        declared = charge_pair(family.get("charge", 0), f"family {name!r}")
        if declared[0] and charge_per_unit(*declared) != pair:
            raise ValueError(
                f"family {name!r} declares the charge {family['charge']} where {label} implies "
                f"{list(pair)} per unit of content"
            )
        family["charge"] = pair[0] if pair[1] == 1 else list(pair)


def migrate_world(document: Json) -> Json:
    """The world with derived kinds, the charge per unit of content on the
    family and only the table entries that differ."""
    if document.get("law") != "rays":
        raise ValueError('not a world of the law of the ray (no "law": "rays")')
    result = copy.deepcopy(document)
    families_value = result.get("families")
    if not isinstance(families_value, list):
        raise ValueError("families must be a list")
    families = [migrate_family(dict(entry)) for entry in families_value]
    result["families"] = families
    measured_entries = result.get("measured", [])
    if not isinstance(measured_entries, list):
        raise ValueError("measured must be a list")
    migrate_charges(families, measured_entries)
    rules = {
        str(family["name"]): default_rule(
            FamilyDefinition(str(family["name"]), int(str(family["quantum"])))
        )
        for family in families
    }
    measured_value = result.get("measured", [])
    if not isinstance(measured_value, list):
        raise ValueError("measured must be a list")
    for entry in measured_value:
        if not isinstance(entry, dict) or not isinstance(entry.get("table"), dict):
            continue
        table: Json = {}
        for name, value in entry["table"].items():
            if name not in rules:
                raise ValueError(f"table names an unknown family {name!r}")
            kept = trim_entry(value, rules[name])
            if kept is not None:
                table[name] = kept
        if table:
            entry["table"] = table
        else:
            del entry["table"]
    return result


def render(document: Json, original: str) -> str:
    """The document in the original's style: indented by two when the
    original was, compact otherwise; the trailing newline as before."""
    indent = 2 if original.startswith("{\n") else None
    text = json.dumps(document, indent=indent)
    return text + ("\n" if original.endswith("\n") else "")


def migrate_file(path: Path, *, check: bool) -> bool:
    """Rewrite one file; returns whether it changed."""
    original = path.read_text(encoding="utf-8")
    document = json.loads(original)
    if not isinstance(document, dict):
        raise ValueError(f"{path}: a world is a JSON object")
    if document.get("format") == "event-entities-v1":
        print(f"{path}: entity definitions, left as they are")
        return False
    rewritten = render(migrate_world(document), original)
    changed = rewritten != original
    if check:
        print(f"{path}: {'would change' if changed else 'unchanged'}")
    elif changed:
        path.write_text(rewritten, encoding="utf-8")
        print(f"{path}: rewritten")
    else:
        print(f"{path}: unchanged")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("worlds", nargs="+", type=Path, help="world files to rewrite")
    parser.add_argument("--check", action="store_true", help="report without writing")
    args = parser.parse_args(argv)
    for path in args.worlds:
        migrate_file(path, check=bool(args.check))
    return 0


if __name__ == "__main__":
    sys.exit(main())
