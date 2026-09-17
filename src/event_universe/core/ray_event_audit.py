"""The world ledger of the ray-event model (ray-event-audit-v1).

One exact ledger per completed tick for each conserved readout: the amount of
every conserved field (momentum being the three-component field among them)
and the charge of every ray family. Each line reads initial, sourced, current,
escaped, annulled and absorbed, and balances when

    initial + sourced = current + escaped + annulled + absorbed

exactly, component by component. The ledger is a read-only host diagnostic
over the readouts the engine already keeps (Highlights 3.15): it changes no
physics and charges no model cost. `audit_failure` re-checks a recorded ledger
from its integers alone, so a hand-altered record reports the tick and the
line that no longer balances.
"""

from collections.abc import Mapping, Sequence
from typing import cast

RAY_EVENT_AUDIT = "ray-event-audit-v1"
LINE_KEYS = ("initial", "sourced", "current", "escaped", "annulled", "absorbed")

Line = dict[str, object]


def _components(value: object) -> tuple[int, ...]:
    if isinstance(value, int):
        return (value,)
    return tuple(int(v) for v in cast(Sequence[int], value))


def line_balanced(line: Mapping[str, object]) -> bool:
    """initial + sourced == current + escaped + annulled + absorbed, exactly."""
    values = {key: _components(line[key]) for key in LINE_KEYS}
    width = {len(v) for v in values.values()}
    if len(width) != 1:
        return False
    return all(
        values["initial"][c] + values["sourced"][c]
        == values["current"][c] + values["escaped"][c] + values["annulled"][c] + values["absorbed"][c]
        for c in range(width.pop())
    )


def ledger_line(
    initial: object,
    sourced: object,
    current: object,
    escaped: object,
    annulled: object,
    absorbed: object,
) -> Line:
    line: Line = {
        "initial": initial,
        "sourced": sourced,
        "current": current,
        "escaped": escaped,
        "annulled": annulled,
        "absorbed": absorbed,
    }
    line["balanced"] = line_balanced(line)
    return line


def world_ledger(
    tick: int,
    fields: dict[str, Line],
    charge: dict[str, Line],
    bodies: dict[str, object],
) -> dict[str, object]:
    """The ledger of one completed tick: a line per conserved field and per ray family,
    and the external bodies' own lines (external-body-v1): their count, the exact sum
    of their momentum, the sum of their declared charge and their sinks per field. A
    body's content never enters a sum, so its lines are beside the identity, not in
    it; what its sinks took is the `absorbed` line of every field."""
    balanced = all(bool(line["balanced"]) for line in fields.values()) and all(
        bool(line["balanced"]) for line in charge.values()
    )
    return {"tick": tick, "balanced": balanced, "fields": fields, "charge": charge, "bodies": bodies}


def audit_failure(audit: Sequence[Mapping[str, object]]) -> dict[str, object] | None:
    """The first line of a recorded audit that does not balance, re-checked from its
    integers (the recorded `balanced` flags are not trusted): the tick, the readout
    (`fields` or `charge`) and the line's name; None when every line balances."""
    for ledger in audit:
        for readout in ("fields", "charge"):
            lines = cast(Mapping[str, Mapping[str, object]], ledger.get(readout, {}))
            for name, line in lines.items():
                if not line_balanced(line):
                    return {"tick": ledger["tick"], "readout": readout, "line": name}
    return None
