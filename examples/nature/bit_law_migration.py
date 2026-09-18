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
  `spread` table and a `steering` table on any spatial field are dropped.
"""

from __future__ import annotations

from typing import Any


def migrate(document: dict[str, Any]) -> dict[str, Any]:
    _node_is_ports(document)
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
    return document


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
