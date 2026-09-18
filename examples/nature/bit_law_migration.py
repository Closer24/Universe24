"""The mechanical migration of a world to the law of the bit (bit-law-v1, the
model owner's decision of 2026-09-18): a shadow is a ray of the same family as
its thing with the bit 0, so a family declared `field_of` another is folded into
its owner; and to a Node that is its six Ports (node-is-ports-v1, feature 17,
Highlights 5.4 point 22): a source is a thing that spends its content and a
mark has no seed. Every world generator of examples/nature applies `migrate` to
what it writes; the physics of each experiment is to be declared again on the
final law (a prefilled field, `initial_field`), which is not this migration's
business.

The rules, applied to a world document in place:

- (node-is-ports-v1) an emission on a ray family loses `source`, `recoil_field`
  and `funded`: it is paid from the emitting type's content and recoils into the
  type's momentum, so an unfunded source (`source` true) gets the content of its
  run, its whole amount per interval times the world's `ticks`, as the type's
  default of the emitted field (an expression amount cannot be migrated and is
  left for the world's author), and a type that emits holds the world's one
  momentum field (a signed three-component conserved field), zero by default;
- (node-is-ports-v1) a mark loses `seed` (there is no lottery and no counter);

- a spatial field with `field_of` X loses the key; its `release` and `spread`
  move to X (X's own declaration wins when it has one), and X's `ray_slots`
  become the larger of the two, since X now carries its things and its shadows;
- everywhere a rule, a body or a mark names the field family (a participant's
  `type`, an output's `field`, a `momentum_table` key, an `on_click` key), it
  names the owner instead, the first entry winning when two fold into one, and
  a momentum table gets its `reads` (point 16): "charge" when an owner it
  names carries a charge, "content" otherwise;
- the field family's value field and spatial field stay declared (nothing else
  of the world refers to them by anything but the name), unused;
- since node-mixing-v1 (Highlights 5.4, point 24, the model owner, 2026-09-18) a
  shadow spreads by the Node's mixing and nothing of the spread is declared: a
  `spread` table and a `steering` table on any spatial field are dropped;
- (the cleanup of 2026-09-18, `cleanup-law-v1`: no field family, Highlights 5.4
  point 12) a ray family that nothing in the world names any more once its
  `field_of` has been folded into its owner (no type's `fields` or `defaults`,
  no emission, seed, body, rule, mark or `initial_field`) is an orphan of the
  old field program and leaves the world: its spatial field, its value field
  and its `initial_field` entry are dropped, so no world of nature declares a
  field family.

The clock, the decay table and one Link per interval (clock-readings-v1, the
model owner's decisions of 2026-09-18, Highlights 5.4 points 19, 20, 21 and 23;
`migrate_clock`, applied by `migrate` as well):

- `kerengonen.phase_advance` leaves every family; a family whose rate was
  nonzero declares `clock` true, and the world declares `K`, the content per
  phase step per interval, the smallest K that keeps every declared thing's
  content / K below half the phase circle, raised to keep the rate of the
  largest declared content where that is admissible (a thing's clock is its
  content, so the old per-family rates are not preserved: the physics of each
  experiment is to be declared again on the law);
- `kerengonen_advance` leaves every emission;
- `draw` [n, d] and `seed` leave every rule: the rule declares `decay`
  {"after_periods": d // n} (a group breaks at that meeting under the rule), or
  {"content_at_most": 0} for a setting of 0 (never);
- `ray_delay`, `ray_phase_per_tick`, and on a board of ray fields
  `computation_field`, `delay_direction` and `least_delay_routing`, leave the
  world: every ray moves one Link per interval.
"""

from __future__ import annotations

from typing import Any


def migrate_clock(document: dict[str, Any]) -> dict[str, Any]:
    """The clock, the decay table and one Link per interval (clock-readings-v1),
    applied to a world document in place; see the module's docstring."""
    fields = document.get("spatial_fields", [])
    rays = any(entry.get("transport") == "ray" for entry in fields)
    for key in ("ray_delay", "ray_phase_per_tick"):
        document.pop(key, None)
    if rays:
        for key in ("computation_field", "delay_direction", "least_delay_routing"):
            document.pop(key, None)
    rates: dict[str, int] = {}
    for entry in fields:
        phased = entry.get("kerengonen")
        if not isinstance(phased, dict) or "phase_advance" not in phased:
            continue
        rate = int(phased.pop("phase_advance"))
        if rate > 0:
            entry["clock"] = True
            rates[entry["field"]] = rate
        if not phased:
            del entry["kerengonen"]
    for emission in document.get("emissions", []):
        emission.pop("kerengonen_advance", None)
    for rule in document.get("ray_interactions", []):
        if "draw" in rule:
            numerator, denominator = (int(v) for v in rule.pop("draw"))
            rule.pop("seed", None)
            rule["decay"] = (
                {"after_periods": max(1, denominator // numerator)}
                if numerator > 0
                else {"content_at_most": 0}
            )
    if not rates or "K" in document:
        return document
    contents: dict[str, int] = {}
    types = {kind["name"]: kind for kind in document.get("disturbance_types", [])}
    for kind in types.values():
        for name, stock in kind.get("defaults", {}).items():
            if name in rates and isinstance(stock, int):
                contents[name] = max(contents.get(name, 0), abs(stock))
    for emission in document.get("emissions", []):
        name, amount = emission.get("field"), emission.get("amount")
        if name in rates and isinstance(amount, int):
            contents[name] = max(contents.get(name, 0), abs(amount))
    minimum, preferred = 1, 1
    for entry in fields:
        name = entry["field"]
        if name not in rates:
            continue
        bits = int(entry.get("phase_bits", 0))
        steps = int((entry.get("kerengonen") or {}).get("phase_steps", 0))
        if steps and not bits:
            bits = steps.bit_length() - 1
        modulus = 1 << bits
        content = contents.get(name, 1)
        minimum = max(minimum, 2 * content // modulus + 1)
        preferred = max(preferred, content // rates[name])
    document["K"] = max(minimum, preferred)
    return document


def migrate(document: dict[str, Any]) -> dict[str, Any]:
    _node_is_ports(document)
    migrate_clock(document)
    fields = document.get("spatial_fields", [])
    by_name = {entry["field"]: entry for entry in fields}
    renames: dict[str, str] = {}
    for entry in fields:
        # The Node mixes the six (node-mixing-v1): no table of the spread is declared.
        entry.pop("spread", None)
        entry.pop("steering", None)
        if "field_of" not in entry:
            continue
        owner = entry.pop("field_of")
        renames[entry["field"]] = owner
        target = by_name[owner]
        if "release" in entry:
            target.setdefault("release", entry.pop("release"))
        target["ray_slots"] = max(int(target.get("ray_slots", 0)), int(entry.get("ray_slots", 0)))
    if not renames:
        _drop_orphan_families(document)
        return document

    def rekey(table: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, value in table.items():
            result.setdefault(renames.get(name, name), value)
        return result

    def rename(name: Any) -> Any:
        if isinstance(name, list):
            seen: list[Any] = []
            for item in name:
                item = renames.get(item, item)
                if item not in seen:
                    seen.append(item)
            return seen
        return renames.get(name, name)

    def reads_of(table: dict[str, Any]) -> str:
        # The 0-meets-1 table's reading (point 16): a charged owner's shadows are
        # read times the thing's charge, a neutral one's times its content.
        return "charge" if any(int(by_name[name].get("charge", 0)) for name in table) else "content"

    for rule in document.get("ray_interactions", []):
        for role in rule.get("participants", []):
            role["type"] = rename(role["type"])
        for output in rule.get("outputs", []):
            if "field" in output:
                output["field"] = rename(output["field"])
        if "momentum_table" in rule:
            rule["momentum_table"] = rekey(rule["momentum_table"])
            rule.setdefault("reads", reads_of(rule["momentum_table"]))
    for body in document.get("external_bodies", []):
        if "momentum_table" in body:
            body["momentum_table"] = rekey(body["momentum_table"])
            body.setdefault("reads", reads_of(body["momentum_table"]))
    for mark in document.get("detectors", []):
        if isinstance(mark.get("on_click"), dict):
            mark["on_click"] = rekey(mark["on_click"])
    _cap_layers(document)
    _drop_orphan_families(document)
    return document


def _named_families(document: dict[str, Any]) -> set[Any]:
    """Every field name the world's declarations refer to, outside the fields and
    the spatial fields themselves."""
    names: set[Any] = set()
    for kind in document.get("disturbance_types", []):
        names.update(kind.get("fields", []))
        names.update(kind.get("defaults", {}))
    for emission in document.get("emissions", []):
        names.add(emission.get("field"))
        names.add(emission.get("recoil_field"))
    for seed in document.get("spatial_seeds", []):
        names.add(seed.get("field"))
    for body in document.get("external_bodies", []):
        names.add(body.get("family"))
        names.update(body.get("momentum_table", {}))
        if isinstance(body.get("polarizer"), dict):
            names.add(body["polarizer"].get("family"))
    for rule in document.get("ray_interactions", []):
        for role in rule.get("participants", []):
            kinds = role.get("type")
            names.update(kinds if isinstance(kinds, list) else [kinds])
        for output in rule.get("outputs", []):
            names.add(output.get("field"))
        names.update(rule.get("momentum_table", {}))
    for mark in document.get("detectors", []):
        if isinstance(mark.get("on_click"), dict):
            names.update(mark["on_click"])
    names.update(document.get("initial_field", {}))
    for key in ("couplings", "spatial_couplings", "field_rules", "spatial_interactions", "field_groups"):
        for entry in document.get(key, []):
            for value in entry.values():
                if isinstance(value, str):
                    names.add(value)
                elif isinstance(value, list):
                    names.update(item for item in value if isinstance(item, str))
    for key in ("computation_field", "cost_field"):
        names.add(document.get(key))
    return names


def _drop_orphan_families(document: dict[str, Any]) -> None:
    """A ray family nothing names (the field family the fold left behind) leaves
    the world with its value field and its initial field, if any."""
    used = _named_families(document)
    orphans = {
        entry["field"]
        for entry in document.get("spatial_fields", [])
        if entry.get("transport") == "ray" and entry["field"] not in used
    }
    if not orphans:
        return
    document["spatial_fields"] = [
        entry for entry in document["spatial_fields"] if entry["field"] not in orphans
    ]
    document["fields"] = [item for item in document.get("fields", []) if item["name"] not in orphans]
    if isinstance(document.get("initial_field"), dict):
        for name in orphans:
            document["initial_field"].pop(name, None)


def _node_is_ports(document: dict[str, Any]) -> None:
    """A source is a thing that spends its content and a mark has no seed
    (node-is-ports-v1): the emissions on ray families lose their `source`,
    `recoil_field` and `funded` keys, an unfunded source gets the content of its
    run, an emitting type holds the world's momentum field, and the marks lose
    `seed`."""
    ray_families = {
        entry["field"] for entry in document.get("spatial_fields", []) if entry.get("transport") == "ray"
    }
    octants = {entry["field"] for entry in document.get("spatial_fields", [])}
    vectors = [
        item["name"]
        for item in document.get("fields", [])
        if item.get("components") == 3
        and item.get("signed")
        and item.get("conserved")
        and item["name"] not in octants
    ]
    momentum = vectors[0] if len(vectors) == 1 else None
    kinds = {kind["name"]: kind for kind in document.get("disturbance_types", [])}
    ticks = int(document.get("ticks", 0))
    for emission in document.get("emissions", []):
        if emission.get("field") not in ray_families:
            continue
        unfunded = emission.pop("source", False) is True
        emission.pop("recoil_field", None)
        emission.pop("funded", None)
        kind = kinds.get(emission.get("type"))
        if kind is None:
            continue
        kind.setdefault("defaults", {})
        if unfunded and isinstance(emission.get("amount"), int):
            # A lamp burns content: the run's worth of its emission.
            if emission["field"] not in kind["fields"]:
                kind["fields"].append(emission["field"])
            stock = int(kind["defaults"].get(emission["field"], 0))
            kind["defaults"][emission["field"]] = stock + emission["amount"] * ticks
        if momentum is not None and momentum not in kind["fields"]:
            kind["fields"].append(momentum)
            kind["defaults"].setdefault(momentum, [0, 0, 0])
    for mark in document.get("detectors", []):
        mark.pop("seed", None)


def _cap_layers(document: dict[str, Any]) -> None:
    """The engine admits at most 32 selected ray slots in one layer (the families a
    rule couples). Two things of coupled families that now carry their shadows
    in their own families may exceed it; their slots are scaled down to fit, in
    proportion, so that the world parses. Such a world must be declared again on
    the final law before it is run (the slots are then its own decision)."""
    fields = document.get("spatial_fields", [])
    by_name = {entry["field"]: entry for entry in fields}
    parent = {name: name for name in by_name}

    def root(name: str) -> str:
        while parent[name] != name:
            name = parent[name]
        return name

    selected: set[str] = set()
    for rule in document.get("ray_interactions", []):
        names: list[str] = []
        for role in rule.get("participants", []):
            kinds = role["type"] if isinstance(role["type"], list) else [role["type"]]
            names.extend(kinds)
        for output in rule.get("outputs", []):
            if isinstance(output.get("field"), str) and output["field"] in by_name:
                names.append(output["field"])
        names.extend(rule.get("momentum_table", {}))
        names = [name for name in names if name in by_name]
        selected.update(names)
        for name in names[1:]:
            parent[root(name)] = root(names[0])
    layers: dict[str, list[str]] = {}
    for name in by_name:
        layers.setdefault(root(name), []).append(name)
    for members in layers.values():
        if not selected.intersection(members):
            continue
        total = sum(int(by_name[name].get("ray_slots", 0)) for name in members)
        if total <= 32:
            continue
        for name in members:
            slots = int(by_name[name].get("ray_slots", 0))
            by_name[name]["ray_slots"] = max(1, slots * 32 // total)
