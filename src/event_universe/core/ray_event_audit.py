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
bit-law-v1, the ledgers per bit per ray family, named by the bit's values,
`real` (1) and `shadow` (0) (the model owner, 2026-09-18), in the form of
node-is-ports-v1 (Highlights 5.4 point 22, no sourced line anywhere): the
real line (`real`) reads initial + converted = current + escaped +
absorbed over the things alone, `converted` being what a meeting turned into
or out of the family (a source is a thing that spends its content, and the
pieces it makes are things of the family it emits) and `absorbed` what ended
in a body, in the thing resident at a mark or at an inverse split in annul
mode; the shadow line (`shadow`) reads initial = current + escaped +
absorbed_at_home, the shadows given with the board and never sourced, lost
only at the board's edge and absorbed only into the resident thing of the
mark that is their home. The ledger is a read-only host diagnostic over the
readouts the engine already keeps (Highlights 3.15): it changes no physics
and charges no model cost. `audit_failure` re-checks a recorded ledger from
its integers alone, so a hand-altered record reports the tick and the line
that no longer balances.
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
)
# The lines a record may leave out, read as zero: absorbed_by_marks before
# detector-absorb-v1, returned before bit-law-v1.
OPTIONAL_LINES = ("absorbed_by_marks", "returned")

Line = dict[str, object]


def _components(value: object) -> tuple[int, ...]:
    if isinstance(value, int):
        return (value,)
    return tuple(int(v) for v in cast(Sequence[int], value))


THING_LINE_KEYS = ("initial", "converted", "current", "escaped", "absorbed")
SHADOW_LINE_KEYS = ("initial", "current", "escaped", "absorbed_at_home")


def _bit_line_balanced(line: Mapping[str, object], keys: tuple[str, ...]) -> bool:
    values = {key: _components(line[key]) for key in keys if key in line}
    if any(key not in values for key in keys) or len({len(v) for v in values.values()}) != 1:
        return False
    width = len(values["initial"])
    gained = values.get("converted", (0,) * width)
    return all(
        values["initial"][c] + gained[c]
        == sum(values[key][c] for key in keys if key not in ("initial", "converted"))
        for c in range(width)
    )


def line_balanced(line: Mapping[str, object]) -> bool:
    """initial + sourced == current + escaped + annulled + absorbed + absorbed_by_marks
    + returned, exactly; a line without absorbed_by_marks (recorded before
    detector-absorb-v1) or without returned (before bit-law-v1) reads it as zero.
    A things' line (node-is-ports-v1) reads initial + converted == current +
    escaped + absorbed, a shadows' line initial == current + escaped +
    absorbed_at_home."""
    if "sourced" not in line:
        if "converted" in line:
            return _bit_line_balanced(line, THING_LINE_KEYS)
        if "absorbed_at_home" in line:
            return _bit_line_balanced(line, SHADOW_LINE_KEYS)
    values = {key: _components(line[key]) for key in LINE_KEYS if key in line}
    width = {len(v) for v in values.values()}
    required = [key for key in LINE_KEYS if key not in OPTIONAL_LINES]
    if len(width) != 1 or any(key not in values for key in required):
        return False
    zero = (0,) * next(iter(width))
    taken = values.get("absorbed_by_marks", zero)
    returned = values.get("returned", zero)
    return all(
        values["initial"][c] + values["sourced"][c]
        == values["current"][c]
        + values["escaped"][c]
        + values["annulled"][c]
        + values["absorbed"][c]
        + taken[c]
        + returned[c]
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
) -> Line:
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
    line["balanced"] = line_balanced(line)
    return line


def thing_line(
    initial: object, converted: object, current: object, escaped: object, absorbed: object
) -> Line:
    """The things' line of one ray family (node-is-ports-v1): initial + converted =
    current + escaped + absorbed, exact."""
    line: Line = {
        "initial": initial,
        "converted": converted,
        "current": current,
        "escaped": escaped,
        "absorbed": absorbed,
    }
    line["balanced"] = line_balanced(line)
    return line


def shadow_line(initial: object, current: object, escaped: object, absorbed_at_home: object) -> Line:
    """The shadows' line of one ray family (node-is-ports-v1): initial = current +
    escaped + absorbed_at_home, exact; nothing is sourced."""
    line: Line = {
        "initial": initial,
        "current": current,
        "escaped": escaped,
        "absorbed_at_home": absorbed_at_home,
    }
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
    and the Detector marks' own lines (node-is-ports-v1): their count, the exact
    sum of their residents' momentum and what the residents hold per field, the
    things absorbed and the shadows absorbed at home. A body's content never
    enters a sum, so its lines are beside the identity, not in it; what its sinks
    took is the `absorbed` line of every field, and what the marks absorbed the
    `absorbed_by_marks` line."""
    balanced = all(bool(line["balanced"]) for line in fields.values()) and all(
        bool(line["balanced"]) for line in charge.values()
    )
    real_conserved = things is None or all(bool(line["balanced"]) for line in things.values())
    ledger: dict[str, object] = {
        "tick": tick,
        "balanced": balanced and real_conserved,
        "fields": fields,
        "charge": charge,
        "bodies": bodies,
        "marks": marks,
    }
    if things is not None:
        # The things' and the shadows' own lines per ray family (bit-law-v1,
        # point 7): the things conserve exactly with no source line but their own.
        ledger["real"] = things
        ledger["shadow"] = {} if shadows is None else shadows
        ledger["real_conserved"] = real_conserved
    return ledger


def audit_failure(audit: Sequence[Mapping[str, object]]) -> dict[str, object] | None:
    """The first line of a recorded audit that does not balance, re-checked from its
    integers (the recorded `balanced` flags are not trusted): the tick, the readout
    (`fields` or `charge`) and the line's name; None when every line balances."""
    for ledger in audit:
        for readout in ("fields", "charge", "real", "shadow"):
            lines = cast(Mapping[str, Mapping[str, object]], ledger.get(readout, {}))
            for name, line in lines.items():
                if not line_balanced(line):
                    return {"tick": ledger["tick"], "readout": readout, "line": name}
    return None
