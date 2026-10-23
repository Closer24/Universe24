"""The conversion, a click's act outside the step (ALGEBRA.md, The conversion; Only a click moves a quantum between families; The declarations by name 5; the owner's word of 2026-10-21, the table's declaration deleted): a record of one family credited at a declared instrument region is taken whole at the drawn Node by the region's credit and given back as whole quanta of other families laid at that Node, the rotations adding exactly in the integers. No table and no key names the records out: given the pairs, every family of quanta with a gap and a Pythagorean pair converts wherever exactly one list of the universe's other gapped families keeps the law's conservations, which are fixed and never declared, the count by whole quanta, the rotation (a rotation whose cosine is num / den has a rational sine iff den^2 - num^2 is a square, the point num + i s a Gaussian integer of norm den, `gaussian`, angle addition the Gaussian product, so a list of whole quanta at their rest rotations carries the parents' rotations exactly iff the two Gaussian products agree once each is scaled by the other's dens, `rotation`, `exact`), the charge (the Wronskian's sum, the plane records out at their senses summing to the parents' senses) and the baryon (as many records of three lines out as in, `kept`); a family with no such list never converts, its stability derived (`listed`, `declared`), and one with several is refused by name, the law having no share among them. The one residual declaration is the senses of a real-line parent's plane records out, the row's key `senses` (`senses_of`): a parent of real lines has the Wronskian 0, which (+, -) and (-, +) keep alike, so which record out is the particle is not in the pairs; one plane record out named and the rest the sum's; refused on a plane parent, whose own sense as read at the click turns its list (`sense_at`). The same rule for N credited quanta (the collision, `listed` with the parents' rotations' product and their senses summed; the null list, the parents themselves, the identity of the group and the no-conversion outcome, never a second list); the search bounded at N + BEYOND records out, a bound named and no law. The when is the region's, the window's close of the arriving record's passage, the Node the credit's own draw by the digits (`lists.region`, `lists.credited_node`); the act is the credit's hole over every line of the record and one lay by the count per record out at that Node at its family's massless pair (`emission.laid_by_count`), the identity asserted in the integers at the write and the conversion line written beside the credit's (`converted`, `line`). The Node knows no conversion; Rule3 steps the records out as it steps every record."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from itertools import combinations_with_replacement, product
from typing import TYPE_CHECKING, Any

from event_universe import reports
from event_universe.core.rule3 import largest_below
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import Gauss, times
from event_universe.loader.keys import Node

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

BARYON_LINES = 3  # the baryon's shape in the law's families: a record of three lines, real or planes
BEYOND = (
    2  # the search's bound, named and no law: a list of N parents has at most N + BEYOND records out
)
Pair = tuple[int, int]
Table = tuple[tuple[int, int], ...]  # the records out, each its family by position and its sense
Parents = tuple[
    tuple[int, int], ...
]  # the records in, each its family and its sense as read, 0 for real lines

MET = 3  # the search's bound on the quanta met at one close, named and no law: the world's multisets of two to MET laid quanta derived at load


def sine_of(pair: Pair) -> int | None:
    """The integer sine of a pair, s with s^2 = den^2 - num^2 (sin omega times den), None where the pair is not Pythagorean: the rotation's cosine and sine are both rational iff den^2 - num^2 is a square."""
    num, den = pair
    gap = den * den - num * num
    sine = largest_below(gap)
    return sine if sine * sine == gap else None


def gaussian(pair: Pair) -> Gauss | None:
    """The pair's point on the circle as a Gaussian integer, num + i s of norm den, None where the pair is not Pythagorean (`sine_of`)."""
    sine = sine_of(pair)
    return None if sine is None else (pair[0], sine)


def rotation(pairs: Sequence[Pair]) -> tuple[Gauss, int] | None:
    """The rotations' sum of several pairs as one point over one scale, the Gaussian product of their points over the product of their dens (angle addition the Gaussian product, the rational points of the circle a group); None where a pair is not Pythagorean."""
    point, scale = (1, 0), 1
    for pair in pairs:
        found = gaussian(pair)
        if found is None:
            return None
        point, scale = times(point, found), scale * pair[1]
    return point, scale


def exact(parents: Sequence[Pair], products: Sequence[Pair]) -> bool:
    """Whether the products' rotations sum exactly to the parents' in the integers (the exactness clause of The conversion): every pair Pythagorean and the two sums (`rotation`) equal once each is scaled by the other's dens' product, both components; one parent the conversion, several the collision."""
    before, after = rotation(parents), rotation(products)
    if before is None or after is None:
        return False
    (point, scale), (other, span) = before, after
    return (point[0] * span, point[1] * span) == (other[0] * scale, other[1] * scale)


def irrational(pair: Pair) -> str:
    """The sentence why a pair is not Pythagorean: its den^2 - num^2 and that it is no square, so its sine is irrational and no sum of rotations is exact with it in the integers."""
    num, den = pair
    return (
        f"[{num}, {den}] has den^2 - num^2 = {den * den - num * num}, no square: its sine is irrational"
    )


def candidates(families: tuple[FamilyRule, ...]) -> list[int]:
    """The families a record out may be: the families of quanta with a gap (num below den), each at its rest rotation; a massless family rests at the rotation 0 and a one-Node lay carries no wave number, so it is no record out, and a held row holds no quantum."""
    return [
        k for k, family in enumerate(families) if not family.held and family.pair[0] != family.pair[1]
    ]


def baryons(families: tuple[FamilyRule, ...], rows: Sequence[tuple[int, int]]) -> int:
    """The records of three lines among the rows, the baryon's count, the law's shape for it (`BARYON_LINES`)."""
    return sum(1 for k, _sense in rows if families[k].laid == BARYON_LINES)


def kept(families: tuple[FamilyRule, ...], parents: Parents, table: Table) -> bool:
    """Whether a list keeps the law's two conservations beyond the count's and the rotation's, fixed and never declared: the charge, the Wronskian's sum, the plane records out at their senses (a record of real lines at 0) summing to the parents' senses summed (each parent's as read at the Node, `sense_at`, 1 at rest for a plane and 0 for real lines); the baryon, as many records of three lines out as in (`baryons`)."""
    senses = sum(sense for out, sense in table if families[out].plane)
    if senses != sum(sense for _parent, sense in parents):
        return False
    return baryons(families, table) == baryons(families, parents)


def fits(families: tuple[FamilyRule, ...], parents: Parents, table: Table) -> bool:
    """Whether a list is some parents' own: their null list, the parents' families themselves (the group's identity, the no-conversion outcome), or a list exact for their rotations (`exact`) keeping both conservations for them (`kept`)."""
    if sorted(k for k, _sense in table) == sorted(k for k, _sense in parents):
        return True
    return exact(
        [families[k].pair for k, _sense in parents], [families[k].pair for k, _sense in table]
    ) and kept(families, parents, table)


def reducible(families: tuple[FamilyRule, ...], parents: Parents, table: Table) -> bool:
    """Whether a list of several parents is a disjoint union of two lists over a partition of the parents into two non-empty sub-multisets, each part's own (`fits`): such a list is the quanta's separate clicks, one converting by its own list while the other passes or each converting alone, and no meeting; a meeting's list is irreducible (the reader's rule of 2026-10-21 on the spectator lists: two neutrons credited at one close have {n, p, e} = {n} + {p, e} and {p, p, e, e} = {p, e} + {p, e}, both reducible, so each converts by its own list as a lone quantum does)."""
    count = len(parents)
    for split in range(1, 2**count - 1):
        if not split & 1:
            continue  # every partition once, the first parent in the first part
        first = tuple(parent for at, parent in enumerate(parents) if split >> at & 1)
        second = tuple(parent for at, parent in enumerate(parents) if not split >> at & 1)
        for take in range(2 ** len(table)):
            one = tuple(row for at, row in enumerate(table) if take >> at & 1)
            other = tuple(row for at, row in enumerate(table) if not take >> at & 1)
            if fits(families, first, one) and fits(families, second, other):
                return True
    return False


def listed(
    families: tuple[FamilyRule, ...], parents: Parents, declared: Mapping[int, int]
) -> list[Table]:
    """Every list of at most N + BEYOND whole quanta of the candidate families, other than the parents' own multiset (the null list, the group's identity: the no-conversion outcome and never a second list), whose rotations sum exactly to the parents' (`exact`) and that keeps the two conservations (`kept`), each as its (family, sense) rows in the families' order: a plane record out at the sense its family is declared (`declared`, the real-line parents' key `senses`) and at either sense where none is, the assignments the sum keeps collected as distinct lists; a record of real lines at 0; of several parents the irreducible lists alone (`reducible`), a list that is the quanta's separate clicks being no meeting."""
    found: list[Table] = []
    own = sorted(k for k, _sense in parents)
    before = [families[k].pair for k in own]
    for size in range(1, len(parents) + BEYOND + 1):
        for outs in combinations_with_replacement(candidates(families), size):
            if list(outs) == own or not exact(before, [families[k].pair for k in outs]):
                continue
            free = [at for at, out in enumerate(outs) if families[out].plane and out not in declared]
            for choice in product((1, -1), repeat=len(free)):
                senses = [declared.get(out, 0) if families[out].plane else 0 for out in outs]
                for at, sense in zip(free, choice, strict=True):
                    senses[at] = sense
                table = tuple(sorted(zip(outs, senses, strict=True)))
                if table not in found and kept(families, parents, table):
                    found.append(table)
    return [table for table in found if not reducible(families, parents, table)]


def names(families: tuple[FamilyRule, ...], rows: Sequence[tuple[int, int]]) -> list[str]:
    """The families of the rows by name, a list's or the parents', for a refusal's sentence."""
    return [families[k].name for k, _sense in rows]


def senses_of(value: object, label: str, families: tuple[FamilyRule, ...]) -> dict[int, int]:
    """The row's key `senses` (the one residual declaration of The conversion): per plane family of quanta with a gap, by name, the sense 1 or -1 its records out of this parent's list are laid at; refused by name on a name that is no such family and on a sense other than 1 or -1."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} maps each plane family out to its sense, 1 or -1")
    found = {}
    for name, sense in value.items():
        index = next((k for k in candidates(families) if families[k].name == name), None)
        if index is None or not families[index].plane:
            raise ValueError(
                f"{label} names {name!r}: a sense is declared for a plane family of quanta with a gap, a record out"
            )
        if sense not in (1, -1):
            raise ValueError(f"{label}.{name} is 1 or -1, got {sense!r}")
        found[index] = int(sense)
    return found


def declared(
    families: tuple[FamilyRule, ...], declaring: Mapping[int, object]
) -> tuple[FamilyRule, ...]:
    """The families' lists derived at load from the pairs and the law's conservations with no key (`listed` with each family of quanta with a gap and a Pythagorean pair as the one parent at rest, a plane at the sense 1 and real lines at 0): a family with no list converts nothing, its stability derived; one list is the family's (`FamilyRule.converts`, its declared senses beside it); refused by name: the key `senses` (`senses_of`) on a held row, on a massless family, on a parent that is not Pythagorean (`irrational`), on a parent with no list (the candidates with an irrational sine named), on a plane parent (its records out take its own sense as read at the click, which turns the list), naming a family that is no record out of the list, or contradicting the Wronskian's sum; several lists of different families keeping both conservations (the law has no share among them); and one list whose plane senses the sum leaves free, a real-line parent lacking the key (one plane record out named, the rest the sum's) or a plane parent (several lists)."""
    found = list(families)
    for index, family in enumerate(families):
        row = f"families[{index}] ({family.name!r})"
        label = f"{row}.senses"
        value = declaring.get(index)
        senses = {} if value is None else senses_of(value, label, families)
        gapped = not family.held and family.pair[0] != family.pair[1]
        if family.held and value is not None:
            raise ValueError(f"{label}: a held row converts nothing; the key is a family of quanta's")
        if not gapped and value is not None:
            raise ValueError(f"{label}: a massless family has no gap and converts nothing")
        if gaussian(family.pair) is None and value is not None:
            raise ValueError(f"{label}: {irrational(family.pair)}, and no list sums to it exactly")
        if not gapped or gaussian(family.pair) is None:
            continue
        if family.plane and value is not None:
            raise ValueError(
                f"{label}: a plane parent's records out take its own sense as read at the click, which turns "
                "its list; the senses are a real-line parent's declaration"
            )
        parents: Parents = ((index, 1 if family.plane else 0),)
        under_the_law = listed(families, parents, {})
        if not under_the_law:
            if value is not None:
                missing = [
                    f"{families[k].name!r} {irrational(families[k].pair)}"
                    for k in candidates(families)
                    if gaussian(families[k].pair) is None
                ]
                raise ValueError(
                    f"{label} is declared and no list of at most {1 + BEYOND} whole quanta of the other families "
                    f"sums to the pair {list(family.pair)} exactly keeping the charge and the baryon; the candidates "
                    f"with an irrational sine: {missing}"
                )
            continue
        lists = sorted({tuple(out for out, _sense in table) for table in under_the_law})
        if len(lists) > 1:
            raise ValueError(
                f"{row}: several exact lists keep the charge and the baryon: "
                f"{[names(families, [(k, 0) for k in one]) for one in lists]}; the law has no share among them"
            )
        stray = sorted(families[k].name for k in senses if k not in lists[0])
        if stray:
            raise ValueError(
                f"{label} names {stray}, no record out of its one list {names(families, under_the_law[0])}"
            )
        tables = listed(families, parents, senses)
        if not tables:
            kept_senses = [
                {families[k].name: s for k, s in table if families[k].plane} for table in under_the_law
            ]
            raise ValueError(
                f"{label} contradicts the Wronskian's sum {parents[0][1]} of its list "
                f"{names(families, under_the_law[0])}: the senses the sum keeps are {kept_senses}"
            )
        if len(tables) > 1:
            planes = sorted({families[out].name for out, _sense in tables[0] if families[out].plane})
            if family.plane:
                raise ValueError(
                    f"{row}: the senses of its plane records out {planes} are left free by its own sense: "
                    "several lists, and the law has no share among them"
                )
            raise ValueError(
                f"{label} is required: the plane records out {planes} of its one list {names(families, tables[0])} "
                "keep the Wronskian's sum 0 at (+, -) and at (-, +) alike, so which is the particle is not in the "
                "pairs; the key names one plane record out's sense, 1 or -1, and the rest are the sum's"
            )
        found[index] = replace(family, converts=tables[0], senses=tuple(sorted(senses.items())))
    return tuple(found)


def together(families: tuple[FamilyRule, ...], bodies: Sequence[Any], packets: Sequence[Any]) -> None:
    """The lists of every multiset the world can credit at one close, derived at load (The conversion, the reader's sentence of 2026-10-21; `loader/world.parse_world`): the gapped Pythagorean families of quanta laid, each up to its laid count, a body's counts over its parts and a packet's count as the generator read it (`loader/world.BodyRow`, `loader/packets.PacketRow`), two to MET quanta at a time, every plane parent at either sense and the real-line parents' declared senses; refused by name where several irreducible lists keep both conservations for one multiset, the law having no share among them (`listed`)."""
    counts: dict[int, int] = {}
    for family, count in [(b.family, sum(b.counts)) for b in bodies] + [
        (p.family, p.count) for p in packets
    ]:
        counts[family] = counts.get(family, 0) + int(count)
    laid = [
        k
        for k in candidates(families)
        if counts.get(k, 0) > 0 and gaussian(families[k].pair) is not None
    ]
    for size in range(2, MET + 1):
        for outs in combinations_with_replacement(laid, size):
            if any(outs.count(k) > counts[k] for k in set(outs)):
                continue
            planes = [at for at, k in enumerate(outs) if families[k].plane]
            declared = {out: sense for k in set(outs) for out, sense in families[k].senses}
            for choice in product((1, -1), repeat=len(planes)):
                senses = [0] * size
                for at, sense in zip(planes, choice, strict=True):
                    senses[at] = sense
                tables = listed(families, tuple(zip(outs, senses, strict=True)), declared)
                if len(tables) > 1:
                    raise ValueError(
                        f"the quanta {names(families, [(k, 0) for k in outs])} the world can credit at one close, at "
                        f"the senses {senses}, have several irreducible lists keeping the charge and the baryon: "
                        f"{[names(families, table) for table in tables]}; the law has no share among them"
                    )


def sense_at(board: Lattice, index: int, at: Node) -> int:
    """The arriving record's sense at the drawn Node, the sign of its first plane's Wronskian there, 1 or -1, 0 for a record of real lines or where the levels stand at 0: the anti-record is the same plane family at the opposite sense, and it converts by the same list with every sense turned."""
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


def line(board: Lattice, parents: Sequence[int], name: str, table: Table) -> dict[str, Any]:
    """The conversion line beside the credit's, labelled NODEDETECTOR: the interval, the records converted (one family's name, several joined with +, each one's count the credit line's), the region by name, the window drawn over, `into`, the families of the records out in the list's order, each up by one whole quantum laid at the credited Node, and their senses as laid; no Node, the lay lines carrying it."""
    families = reports.MET.join(board.families[k].name for k in parents)
    found = dict(
        zip(
            reports.REPORT_KEYS,
            (reports.CONVERSION, reports.MEASUREMENT, board.interval, families, name),
            strict=True,
        )
    )
    found[reports.CREDIT_KEYS[0]] = board.credit.window_of(board.interval)
    found[reports.INTO] = [board.families[out].name for out, _sense in table]
    found[reports.SENSES] = [sense for _out, sense in table]
    return found


def rows_at(board: Lattice, parents: Sequence[int], name: str, at: Node) -> Table:
    """The one list of the quanta credited at one Node: the parents' senses read there (`sense_at`; 1 for a plane whose Wronskian stands at 0 there, 0 for real lines), `listed` for the parents' rotations under the two conservations with the real-line parents' declared senses (one parent the conversion, the list the loader derived turned by the parent's sense; several the collision, the irreducible list), refused by name where several stand (the law has no share among them), () where none does, the plain credit standing; the identity asserted in the integers before any write."""
    families = board.families
    read: Parents = tuple(
        (k, (sense_at(board, k, at) or 1) if families[k].plane else 0) for k in parents
    )
    senses = {out: sense for k in parents for out, sense in families[k].senses}
    tables = listed(families, read, senses)
    if not tables:
        return ()
    if len(tables) > 1:
        raise RuntimeError(
            f"the quanta of {[families[k].name for k in parents]} credited at {name!r} at the interval "
            f"{board.interval} have several exact lists keeping the charge and the baryon: "
            f"{[names(families, table) for table in tables]}; the law has no share among them"
        )
    table = tables[0]
    assert exact([families[k].pair for k in parents], [families[out].pair for out, _sense in table])
    return table


def converted(board: Lattice, parents: Sequence[int], name: str, at: Node) -> list[tuple[int, int]]:
    """The records out of the quanta credited at one Node, the rows the conversion adds to the credit's list (`meeting.alone`, `meeting.met`): the one list at the Node (`rows_at`) with the conversion line written beside the credit's where it stands; the list lays each record out as one whole quantum at the credited Node by the count at its family's massless pair (`emission.laid_by_count`)."""
    table = rows_at(board, parents, name, at)
    if table and board.output is not None:
        board.output(line(board, parents, name, table))
    return list(table)


def birth_of(families: tuple[FamilyRule, ...], parent: int) -> list[Table]:
    """Matter's birth from light, the gapless meeting's own clause (the law's sentence on the owner's word of 2026-10-23): the lists two quanta of a gapless family [den, den] make at one Node, where the parents' own list is empty (a massless family is no record out, `candidates`): every plane family with a gap and a Pythagorean pair at the senses 1 and -1, the conjugate pair, whose product is the identity the two gapless points' product is ((num + i s)(num - i s) = den^2), the children's senses summing to 0 and the charge kept (`kept`); The conversion's exactness and its charge convention stay as written for every other parent (the sense the charge's sign, the point the same at both senses, the neutron's chain standing on it). The lists in order of the pair's gap den^2 - num^2, the lightest first; the threshold, the two quanta's two walls against the pair's two walls, is read by the act (`act.born_pair`)."""
    if families[parent].pair[0] != families[parent].pair[1]:
        return []
    found: list[Table] = []
    for k in candidates(families):
        family = families[k]
        if not family.plane or gaussian(family.pair) is None:
            continue
        table: Table = ((k, -1), (k, 1))
        if kept(families, ((parent, 0), (parent, 0)), table):
            found.append(table)
    return sorted(
        found, key=lambda table: families[table[0][0]].pair[1] ** 2 - families[table[0][0]].pair[0] ** 2
    )
