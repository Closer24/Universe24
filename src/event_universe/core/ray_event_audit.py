"""The world ledger of the ray-event model (ray-event-audit-v1).

One exact ledger per completed tick for each conserved readout: the amount of
every conserved field (momentum being the three-component field among them)
and the charge of every ray family. Each line reads initial, sourced, current,
escaped, annulled, absorbed (the external bodies' sinks), absorbed_by_marks
(what the Detector marks absorbed on their clicks, detector-absorb-v1) and,
since bit-law-v1 (2026-09-18), returned (what came home: the shadows absorbed
back into their things, whose re-release is on the sourced line, and the
momentum delivered outside the identity, to a body or a record without a
recoil field), and balances when

    initial + sourced = current + escaped + annulled + absorbed + absorbed_by_marks + returned

exactly, component by component; a line recorded before those dates carries no
absorbed_by_marks or returned and reads them as zero. Beside it, since
bit-law-v1, the things' own line per ray family (`things`): the things conserve
exactly with no source line but their emissions and conversions, initial +
sourced = current + escaped + annulled + absorbed + absorbed_by_marks over the
things alone, the shadows' line being initial + sourced = current + escaped +
returned. The ledger is a read-only host diagnostic over the readouts the
engine already keeps (Highlights 3.15): it changes no physics and charges no
model cost. `audit_failure` re-checks a recorded ledger from its integers
alone, so a hand-altered record reports the tick and the line that no longer
balances.
"""

from collections.abc import Mapping, Sequence
from typing import cast

RAY_EVENT_AUDIT = "ray-event-audit-v1"
LINE_KEYS = (
    "initial",
    "sourced",
    "current",
    "escaped",
    "annulled",
    "absorbed",
    "absorbed_by_marks",
    "returned",
    "spent",
)
# The lines a record may leave out, read as zero: absorbed_by_marks before
# detector-absorb-v1, returned before bit-law-v1, spent before clock-readings-v1
# and on every line but the momentum field's.
OPTIONAL_LINES = ("absorbed_by_marks", "returned", "spent")

Line = dict[str, object]


def _components(value: object) -> tuple[int, ...]:
    if isinstance(value, int):
        return (value,)
    return tuple(int(v) for v in cast(Sequence[int], value))


def line_balanced(line: Mapping[str, object]) -> bool:
    """initial + sourced == current + escaped + annulled + absorbed + absorbed_by_marks
    + returned + spent, exactly; a line without absorbed_by_marks (recorded before
    detector-absorb-v1), without returned (before bit-law-v1) or without spent (the
    momentum field's line alone carries it, clock-readings-v1) reads it as zero."""
    values = {key: _components(line[key]) for key in LINE_KEYS if key in line}
    width = {len(v) for v in values.values()}
    required = [key for key in LINE_KEYS if key not in OPTIONAL_LINES]
    if len(width) != 1 or any(key not in values for key in required):
        return False
    zero = (0,) * next(iter(width))
    taken = values.get("absorbed_by_marks", zero)
    returned = values.get("returned", zero)
    spent = values.get("spent", zero)
    return all(
        values["initial"][c] + values["sourced"][c]
        == values["current"][c]
        + values["escaped"][c]
        + values["annulled"][c]
        + values["absorbed"][c]
        + taken[c]
        + returned[c]
        + spent[c]
        for c in range(width.pop())
    )


def ledger_line(
    initial: object,
    sourced: object,
    current: object,
    escaped: object,
    annulled: object,
    absorbed: object,
    absorbed_by_marks: object,
    returned: object = 0,
    spent: object | None = None,
) -> Line:
    """One ledger line; `spent` joins it when given (the momentum field's line,
    clock-readings-v1) and is left out otherwise."""
    line: Line = {
        "initial": initial,
        "sourced": sourced,
        "current": current,
        "escaped": escaped,
        "annulled": annulled,
        "absorbed": absorbed,
        "absorbed_by_marks": absorbed_by_marks,
        "returned": returned,
    }
    if isinstance(returned, int) and not isinstance(initial, int):
        line["returned"] = (0,) * len(_components(initial))
    if spent is not None:
        line["spent"] = spent
    line["balanced"] = line_balanced(line)
    return line


def world_ledger(
    tick: int,
    fields: dict[str, Line],
    charge: dict[str, Line],
    bodies: dict[str, object],
    marks: dict[str, object],
    things: dict[str, Line] | None = None,
    shadows: dict[str, Line] | None = None,
) -> dict[str, object]:
    """The ledger of one completed tick: a line per conserved field and per ray family,
    the external bodies' own lines (external-body-v1): their count, the exact sum
    of their momentum, the sum of their declared charge and their sinks per field,
    and the Detector marks' own lines (detector-absorb-v1): their count, the exact
    sum of their momentum and their counters per field. A body's content never
    enters a sum, so its lines are beside the identity, not in it; what its sinks
    took is the `absorbed` line of every field, and what the marks absorbed on their
    clicks the `absorbed_by_marks` line."""
    balanced = all(bool(line["balanced"]) for line in fields.values()) and all(
        bool(line["balanced"]) for line in charge.values()
    )
    things_conserved = things is None or all(bool(line["balanced"]) for line in things.values())
    ledger: dict[str, object] = {
        "tick": tick,
        "balanced": balanced and things_conserved,
        "fields": fields,
        "charge": charge,
        "bodies": bodies,
        "marks": marks,
    }
    if things is not None:
        # The things' and the shadows' own lines per ray family (bit-law-v1,
        # point 7): the things conserve exactly with no source line but their own.
        ledger["things"] = things
        ledger["shadows"] = {} if shadows is None else shadows
        ledger["things_conserved"] = things_conserved
    return ledger


def audit_failure(audit: Sequence[Mapping[str, object]]) -> dict[str, object] | None:
    """The first line of a recorded audit that does not balance, re-checked from its
    integers (the recorded `balanced` flags are not trusted): the tick, the readout
    (`fields` or `charge`) and the line's name; None when every line balances."""
    for ledger in audit:
        for readout in ("fields", "charge", "things", "shadows"):
            lines = cast(Mapping[str, Mapping[str, object]], ledger.get(readout, {}))
            for name, line in lines.items():
                if not line_balanced(line):
                    return {"tick": ledger["tick"], "readout": readout, "line": name}
    return None
