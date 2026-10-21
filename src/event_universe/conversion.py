"""The conversion, a click's act outside the step (ALGEBRA.md, The conversion; Only a click moves a quantum between families; The declarations by name 5; the round of 2026-10-21, the conversion built in the toy): a record of one family arriving at a declared instrument region is taken whole at the drawn Node by the region's credit and given back as whole quanta of other families laid at that Node, the rotations adding exactly in the integers. The table is derived from the pairs and never typed: a rotation whose cosine is num / den has a rational sine iff den^2 - num^2 is a square (the pair Pythagorean, the point num + i s a Gaussian integer of norm den, `gaussian`), angle addition is the Gaussian product, so a list of whole quanta at their rest rotations carries the parent's rotation exactly iff the product of its points times the parent's den equals the parent's point times the product of their dens, both components (`exact`); the universe's key `converts` on the parent family names what the table keeps beyond the write's own, the count by whole units (`keeps`: `wronskian`, the senses' sum, the law's one charge, exact at the lay with the planes' exact split; `baryon`, the count of records of three lines, declared as the law has it), and the sense of each record out that is a plane (`senses`, the table's declaration, the anti-record the same plane family at the opposite sense), and the loader admits the one exact list that keeps what is named, refusing by name a parent whose pair is not Pythagorean with the sentence why, a parent with no exact list (the candidates without an integer sine named) and one with several (`declared`). The when is the region's, the window's close of the arriving record's passage, the Node the credit's own draw by the digits (`lists.region`, `lists.credited_node`); the act is the credit's hole over every line of the record and one lay by the count per record out at that Node at its family's massless pair (`emission.laid_by_count`), the identity asserted in the integers at the write and the conversion line written beside the credit's (`converted`, `line`). The Node knows no conversion; Rule3 steps the records out as it steps every record."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from itertools import combinations_with_replacement
from typing import TYPE_CHECKING, Any

from event_universe import reports
from event_universe.core.rule3 import largest_below
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import Gauss, times
from event_universe.loader.keys import CONVERTS_KEYS, CONVERTS_REQUIRED, KEEPS, Node, keyed

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

WRONSKIAN, BARYON = (
    KEEPS  # the two names a table may keep: the senses' sum and the records of three lines
)
BARYON_LINES = 3  # the baryon's shape in the law's families: a record of three lines, real or planes
LISTED = 3  # the most records out one table lists, the search's bound (the law's tables name three)
Table = tuple[tuple[int, int], ...]  # the records out, each its family by position and its sense


def sine_of(pair: tuple[int, int]) -> int | None:
    """The integer sine of a pair, s with s^2 = den^2 - num^2 (sin omega times den), None where the pair is not Pythagorean: the rotation's cosine and sine are both rational iff den^2 - num^2 is a square."""
    num, den = pair
    gap = den * den - num * num
    sine = largest_below(gap)
    return sine if sine * sine == gap else None


def gaussian(pair: tuple[int, int]) -> Gauss | None:
    """The pair's point on the circle as a Gaussian integer, num + i s of norm den, None where the pair is not Pythagorean (`sine_of`)."""
    sine = sine_of(pair)
    return None if sine is None else (pair[0], sine)


def exact(parent: tuple[int, int], pairs: Sequence[tuple[int, int]]) -> bool:
    """Whether the rotations of `pairs` sum exactly to the parent's in the integers: every pair Pythagorean, and the Gaussian product of their points times the parent's den equal to the parent's point times the product of their dens in both components, the rational points of the circle forming a group under angle addition (the exactness clause of The conversion)."""
    points = [gaussian(pair) for pair in (parent, *pairs)]
    if any(point is None for point in points):
        return False
    first, *rest = [point for point in points if point is not None]
    product, scale = (1, 0), 1
    for point, pair in zip(rest, pairs, strict=True):
        product, scale = times(product, point), scale * pair[1]
    return (product[0] * parent[1], product[1] * parent[1]) == (first[0] * scale, first[1] * scale)


def irrational(pair: tuple[int, int]) -> str:
    """The sentence why a pair is not Pythagorean: its den^2 - num^2 and that it is no square, so its sine is irrational and no sum of rotations is exact with it in the integers."""
    num, den = pair
    return (
        f"[{num}, {den}] has den^2 - num^2 = {den * den - num * num}, no square: its sine is irrational"
    )


def candidates(families: tuple[FamilyRule, ...], parent: int) -> list[int]:
    """The families a record out may be: the families of quanta other than the parent with a gap (num below den), each at its rest rotation; a massless family rests at the rotation 0 and a one-Node lay carries no wave number, so it is no record out of a table laid at one Node."""
    return [
        index
        for index, family in enumerate(families)
        if index != parent and not family.held and family.pair[0] != family.pair[1]
    ]


def kept(families: tuple[FamilyRule, ...], parent: int, table: Table, keeps: Sequence[str]) -> bool:
    """Whether a table keeps what the key names: the Wronskian's sum, each plane record out at its sense and a record of real lines at 0, equal to the parent's, 1 for a plane and 0 for real lines (the arriving record's own sense turns the whole table at the click, `sense_at`); the baryon, as many records of three lines out as in."""
    if WRONSKIAN in keeps:
        own = 1 if families[parent].plane else 0
        if sum(sense for out, sense in table if families[out].plane) != own:
            return False
    if BARYON in keeps:
        own = 1 if families[parent].laid == BARYON_LINES else 0
        if sum(1 for out, _sense in table if families[out].laid == BARYON_LINES) != own:
            return False
    return True


def tables_of(
    families: tuple[FamilyRule, ...], parent: int, keeps: Sequence[str], senses: Mapping[int, int]
) -> list[Table]:
    """Every list of at most LISTED whole quanta of the candidate families whose rotations sum exactly to the parent's (`exact`) and that keeps what the key names (`kept`), each as its (family, sense) rows, the sense the declared one for a plane family and 0 for real lines."""
    found = []
    for size in range(1, LISTED + 1):
        for outs in combinations_with_replacement(candidates(families, parent), size):
            if not exact(families[parent].pair, [families[out].pair for out in outs]):
                continue
            table = tuple((out, senses.get(out, 0)) for out in outs)
            if kept(families, parent, table, keeps):
                found.append(table)
    return found


def keeps_of(value: object, label: str) -> list[str]:
    """The key's `keeps`: a list of the law's two names, each once; refused by name otherwise (the law has no lepton number and no other count a click keeps)."""
    if not isinstance(value, list) or not all(isinstance(name, str) for name in value):
        raise ValueError(f"{label} lists what the table keeps, among {list(KEEPS)}")
    names = [str(name) for name in value]
    if any(name not in KEEPS for name in names) or len(set(names)) != len(names):
        raise ValueError(
            f"{label} is a list of {list(KEEPS)}, each once, got {names!r}: the count by whole units and the "
            "rotations' sum are the write's own and need no name; the law has no lepton number"
        )
    return names


def senses_of(
    value: object, label: str, families: tuple[FamilyRule, ...], parent: int
) -> dict[int, int]:
    """The key's `senses`: per plane family among the candidates, by name, the sense 1 or -1 of its record out (the table's declaration); a name that is no candidate plane family is refused."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} maps each plane family out to its sense, 1 or -1")
    found = {}
    for name, sense in value.items():
        index = next((k for k in candidates(families, parent) if families[k].name == name), None)
        if index is None or not families[index].plane:
            raise ValueError(
                f"{label} names {name!r}: a sense is declared for a plane family of quanta that may stand in the "
                "table, other than the parent and with a gap"
            )
        if sense not in (1, -1):
            raise ValueError(f"{label}.{name} is 1 or -1, got {sense!r}")
        found[index] = int(sense)
    return found


def declared(
    families: tuple[FamilyRule, ...], converting: Mapping[int, object]
) -> tuple[FamilyRule, ...]:
    """The converting families' tables, derived at load from the universe's pairs and each parent's key `converts` (`keeps_of`, `senses_of`, `tables_of`): refused by name on a held row, on a parent whose pair is not Pythagorean (`irrational`), where a plane candidate of an exact list has no declared sense, where no exact list keeps what is named (the candidates without an integer sine named with the sentence why) and where several do; the families returned with each parent's table in its rule."""
    found = list(families)
    for parent, value in converting.items():
        label = f"families[{parent}] ({families[parent].name!r}).converts"
        if families[parent].held:
            raise ValueError(f"{label}: a held row converts nothing; the key is a family of quanta's")
        if gaussian(families[parent].pair) is None:
            raise ValueError(
                f"{label}: {irrational(families[parent].pair)}, and no list sums to it exactly"
            )
        row = keyed(value, label, CONVERTS_KEYS, CONVERTS_REQUIRED)
        keeps = keeps_of(row[CONVERTS_KEYS[0]], f"{label}.{CONVERTS_KEYS[0]}")
        senses = senses_of(
            row.get(CONVERTS_KEYS[1], {}), f"{label}.{CONVERTS_KEYS[1]}", families, parent
        )
        tables = tables_of(families, parent, keeps, senses)
        unsensed = [
            families[out].name
            for table in tables
            for out, _sense in table
            if families[out].plane and out not in senses
        ]
        if unsensed:
            raise ValueError(
                f"{label}.senses: the plane families {sorted(set(unsensed))} stand in an exact list and declare no "
                "sense; a plane record out is laid at the sense the table declares, 1 or -1"
            )
        if not tables:
            missing = [
                f"{families[k].name!r} {irrational(families[k].pair)}"
                for k in candidates(families, parent)
                if gaussian(families[k].pair) is None
            ]
            raise ValueError(
                f"{label}: no list of at most {LISTED} whole quanta of the other families sums to the pair "
                f"{list(families[parent].pair)} exactly keeping {keeps}; the candidates with an irrational sine: {missing}"
            )
        if len(tables) > 1:
            named = [[families[out].name for out, _sense in table] for table in tables]
            raise ValueError(f"{label}: several exact lists keep {keeps}: {named}; one table per family")
        found[parent] = replace(families[parent], converts=tables[0])
    return tuple(found)


def sense_at(board: Lattice, index: int, at: Node) -> int:
    """The arriving record's sense at the drawn Node, the sign of its first plane's Wronskian there, 1 or -1, 0 for a record of real lines or where the levels stand at 0: the anti-record is the same plane family at the opposite sense, and it converts by the declared table with every sense turned."""
    family, state = board.families[index], board.states[index]
    if not family.plane:
        return 0
    where = (
        int(at[0]) + int(board.offset[0]),
        int(at[1]) + int(board.offset[1]),
        int(at[2]) + int(board.offset[2]),
    )
    re, im = state.lines[0], state.lines[1]
    wronskian = int(re.now[where]) * int(im.before[where]) - int(im.now[where]) * int(re.before[where])
    return 0 if wronskian == 0 else (1 if wronskian > 0 else -1)


def line(board: Lattice, index: int, name: str, senses: Sequence[int]) -> dict[str, Any]:
    """The conversion line beside the credit's, labelled NODEDETECTOR: the interval, the record converted (its count the credit line's), the region by name, the window drawn over, `into`, the families of the records out in the table's order, each up by one whole quantum laid at the credited Node, and their senses as laid; no Node, the lay lines carrying it."""
    family = board.families[index]
    found = dict(
        zip(
            reports.REPORT_KEYS,
            (reports.CONVERSION, reports.MEASUREMENT, board.interval, family.name, name),
            strict=True,
        )
    )
    found[reports.CREDIT_KEYS[0]] = board.credit.window_of(board.interval)
    found[reports.INTO] = [board.families[out].name for out, _sense in family.converts]
    found[reports.SENSES] = list(senses)
    return found


def converted(
    board: Lattice, index: int, name: str, found: Sequence[tuple[Node, tuple[int, ...]]]
) -> list[tuple[int, int]]:
    """The records out of a converting family's credited quantum, the rows the conversion adds to the credit's list (`lists.region`): where the family's table stands, per record out its family and its sense as laid, the table's sense turned by the arriving record's own (`sense_at`; 0 for a record of real lines), the rotations' identity asserted in the integers before the write and the conversion line written beside the credit's; the list lays each as one whole quantum at the credited Node by the count at its family's massless pair (`emission.laid_by_count`); nothing for a family that converts nothing or whose quantum was credited at no Node."""
    family = board.families[index]
    if not family.converts or not found:
        return []
    turn = sense_at(board, index, found[0][0]) or 1
    assert exact(family.pair, [board.families[out].pair for out, _sense in family.converts])
    senses = [sense * turn for _out, sense in family.converts]
    if board.output is not None:
        board.output(line(board, index, name, senses))
    return [(out, sense) for (out, _declared), sense in zip(family.converts, senses, strict=True)]
