"""The lay a world declares for its bodies and the resolution the integer budget derives from a declared tolerance (the body round at the owner's words of 2026-10-02, 17:40 and 17:55: the body worlds of one kind, the lay at the integer fixed point under the body's own paces and the resolution derived from a declared tolerance; HIGHLIGHTS.md, the mathematician's 162 (1) and (3) and 168 items 1 and 2 with the advisor's second hand): the world file's key `lay`, its `kind` the generator's lay by name (`repeat`, the lay-and-rest map iterated to the start's own rule of the repeat with the counts' half step, the lay of every world without the key; `fixed_point`, the record and the content re-laid in each other's paces until the levels repeat within `stop` units at every Node inside `passes` passes, the stop and the passes the file's numbers and none the engine's), its `seed`, the first pass's lay by name (`one_node`, the declared count at the seed Node, the seed of every world without the key; `compact`, the count at the seed Node and the Nodes of its six Ports in the proportion `profile` [centre, neighbour] declares, two integers of the file, the compact branch's profile the law's line names at that count), and its `tolerance` [num, den], the relative deviation of the body's share the run may read, from which the least quantum action T follows by the budget's line, T >= 4 (5.66 / 2)^2 num^2 n sin(omega_s) / (9 den^2 epsilon^2 c_i) with n the run's intervals, c_i the quanta per Node of the body and sin omega_s the family's gap, written as integers with no root, (5.66 / 2)^2 = 8 and sin^2 omega_s = (den^2 - num^2) / den^2: a world whose T is below the least power of two meeting it is refused by name, the least T printed; nothing physical depends on T, the unit of action, and the engine reads none of these keys."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.keys import integer, keyed

LAY_KEYS, LAY_REQUIRED = ("kind", "stop", "passes", "tolerance", "seed", "profile"), ("kind",)
REPEAT, FIXED_POINT = "repeat", "fixed_point"  # the generator's two lays, by name
KINDS = (REPEAT, FIXED_POINT)
ONE_NODE, COMPACT = "one_node", "compact"  # the first pass's two seeds, by name
SEEDS = (ONE_NODE, COMPACT)


@dataclass(frozen=True)
class Lay:
    """The lay as declared: its kind by name, the stop (the largest change of a level between two passes at which the fixed-point lay repeats, in units; 0 the exact repeat), the passes allowed to it, the tolerance epsilon as [num, den], None where the world declares none and the budget gates nothing, the seed of the first pass by name (`one_node` where the world declares none) and the compact seed's profile [centre, neighbour], None with the one-Node seed."""

    kind: str
    stop: int
    passes: int
    tolerance: tuple[int, int] | None
    seed: str
    profile: tuple[int, int] | None


def lay_of(value: object, label: str) -> Lay:
    """The key `lay` read: `kind` one of the generator's lays by name; `stop` (from 0) and `passes` (from 1) required with the fixed-point lay and refused with the repeat, which has the start's own rule; `tolerance` [num, den] with num and den from 1 and num at most den, optional; `seed` one of the first pass's seeds by name, `one_node` without the key, and `profile` [centre, neighbour] (the centre's parts from 1, a neighbour's from 0) required with the compact seed and refused with the one-Node seed; every other key and every other word refused by name."""
    lay = keyed(value, label, LAY_KEYS, LAY_REQUIRED)
    kind = lay["kind"]
    if kind not in KINDS:
        raise ValueError(
            f"{label}.kind is one of {list(KINDS)}, the generator's lays by name, got {kind!r}"
        )
    fixed = kind == FIXED_POINT
    for key in ("stop", "passes"):
        if (key in lay) != fixed:
            raise ValueError(
                f"{label}.{key} is declared with the lay {FIXED_POINT!r} and not with {REPEAT!r}, whose stop "
                "is the start's own rule of the repeat (ALGEBRA.md #the-generator)"
            )
    stop = integer(lay["stop"], f"{label}.stop", 0) if fixed else 0
    passes = integer(lay["passes"], f"{label}.passes", 1) if fixed else 0
    tolerance = None
    if "tolerance" in lay:
        pair = lay["tolerance"]
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f"{label}.tolerance must be [num, den], the relative deviation epsilon")
        den = integer(pair[1], f"{label}.tolerance's den", 1)
        tolerance = (integer(pair[0], f"{label}.tolerance's num", 1, den), den)
    seed = lay.get("seed", ONE_NODE)
    if seed not in SEEDS:
        raise ValueError(
            f"{label}.seed is one of {list(SEEDS)}, the first pass's seeds by name, got {seed!r}"
        )
    if ("profile" in lay) != (seed == COMPACT):
        raise ValueError(
            f"{label}.profile [centre, neighbour] is declared with the seed {COMPACT!r} and not with "
            f"{ONE_NODE!r}, the declared count at the seed Node (ALGEBRA.md #the-generator)"
        )
    profile = None
    if seed == COMPACT:
        parts = lay["profile"]
        if not isinstance(parts, list) or len(parts) != 2:
            raise ValueError(
                f"{label}.profile must be [centre, neighbour], the seed's parts at the Node and at each of its six Ports' Nodes"
            )
        profile = (
            integer(parts[0], f"{label}.profile's centre", 1),
            integer(parts[1], f"{label}.profile's neighbour", 0),
        )
    return Lay(kind, stop, passes, tolerance, seed, profile)


def least_action(pair: tuple[int, int], intervals: int, quanta: int, tolerance: tuple[int, int]) -> int:
    """The least quantum action T the budget admits, a power of two (HIGHLIGHTS.md, 168 item 1's last line): the share's deviation over the body, 5.66 sigma sqrt(n) / A with sigma = (num / (3 den)) sqrt(6 / 12) levels per interval and A = sqrt(T c_i / (2 sin omega_s)), within epsilon = e_num / e_den gives T >= 32 num^2 n sin(omega_s) / (9 den^2 epsilon^2 c_i); squared, with sin^2 omega_s = (den^2 - num^2) / den^2, the integer line 81 den^6 e_num^4 c_i^2 T^2 >= 1024 num^4 n^2 e_den^4 (den^2 - num^2), 1024 = (4 x 8)^2 with 4 x 8 = 4 (5.66 / 2)^2 and 81 = (3 x 3)^2, and T the least power of two whose square meets it, by doubling from 1; 1 where the pair has no gap (a massless family's deviation has no quantum to read)."""
    num, den = pair
    e_num, e_den = tolerance
    left = (3 * den * 3 * den * den) ** 2 * e_num ** (2 + 2) * quanta * quanta  # 81 den^6 e_num^4 c_i^2
    right = (
        (2 * 2 * num * 2 * 2 * 2 * num) ** 2 * intervals * intervals * e_den ** (2 + 2)
    )  # 1024 num^4 n^2 e_den^4
    right *= den * den - num * num  # den^2 sin^2 omega_s
    action = 1
    while left * action * action < right:
        action += action
    return action


def budget_gate(
    lay: Lay | None, pairs: list[tuple[int, int]], counts: list[int], intervals: int, action: int
) -> None:
    """The budget's gate at load: for every body (its family's pair and its quanta per Node, the largest declared count) the least T the declared tolerance needs over the run's intervals (`least_action`); a universe whose T is below it is refused by name with the least T printed."""
    if lay is None or lay.tolerance is None:
        return
    for pair, quanta in zip(pairs, counts, strict=True):
        least = least_action(pair, intervals, quanta, lay.tolerance)
        if action < least:
            raise ValueError(
                f"the universe's quantum action T = {action} is below the least T = {least} the lay's tolerance "
                f"{list(lay.tolerance)} needs for a body of the pair {list(pair)} with {quanta} quanta per Node "
                f"over {intervals} intervals: T >= 32 num^2 n sin(omega_s) / (9 den^2 epsilon^2 c_i), the "
                "share's deviation 5.66 sigma sqrt(n) / A within epsilon (HIGHLIGHTS.md, the integer budget)"
            )
