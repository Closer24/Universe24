"""The ONE translation-invariant tensor of rank <= 4 on v = (1, b, a), as a sparse unit-cell template.

The tensor is pure data: integers and gear names. It carries no physics and no branch; "light", "matter",
"gravity" are only names a user may give to gear types or blocks.

Unit cell
    An ordered list of gear TYPES. Every node of the periodic cube holds one gear of every type (translation
    invariance). A gear type has a ``name``, a readout ``label`` ("official" or "audit", owner decision OD1; used ONLY
    by the passive click readout, never by the dynamics) and an optional Yee ``link`` axis k in {0, 1, 2}: a link gear
    of the link (x, x + e_k) is stored at its base node x (metadata; the engine ignores it).

Monomial (one tensor entry, written for the gear of type ``target`` at a node x)
    ``(target, coeff, factors)`` with an integer ``coeff`` and at most THREE factors; a factor is
    ``(gear, offset, field)``: the value ``field`` in {"a", "b"} of the gear of type ``gear`` at node x + offset,
    offset in {0, +-e_x, +-e_y, +-e_z}. No factor = a constant entry. Degree <= 3 = rank <= 4 on v = (1, b, a).

The input of the gear of type t at node x is

    u_t(x) = sum over monomials m with target t of  coeff_m * prod_{f in m} field_f(gear_f, x + offset_f)

read from the SAME complete previous snapshot, and the gear runs Rule3 with K = 2u (coefficients are coefficients of
u, so K is even by construction).

Storage locality (theorem B3, enforced at construction)
    The target node (offset 0) and every factor offset must lie in {0, e} for ONE face direction e: a monomial lives
    on one or two neighboring storage sites. Edge offsets (1,1,0), diagonal offsets (1,1,1), longer offsets (2,0,0) and
    monomials touching three nodes (e.g. factors at +e_x and -e_x) raise ``LocalityError``.
    Including both geometric endpoints of link gears is a stronger condition: ``strict_support=True`` checks it.
    The default construction satisfies storage locality but contains terms spanning two geometric edges.

Two-time reads
    A factor with field "a" is a two-time read. The graph "gear g's a is read by gear t" must be ACYCLIC (a self-read
    is a cycle). Its layering is the STAGED inverse order: stage 0 = gear types whose input reads no a, stage s =
    gear types reading a only of gears in stages < s. Cyclic reads raise ``AcyclicityError``.

Canonical form
    Factors are sorted, monomials with the same target and the same factor multiset are merged (coefficients added),
    zero coefficients are dropped, monomials are sorted. ``to_dict``/``from_dict`` give the serialisable form
    documented in README.md.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Iterable, Sequence
from types import MappingProxyType

from .lattice import DIRECTIONS, ZERO, offset_tuple

FORMAT = "metric_variant_v1/tensor/1"
FIELDS = ("a", "b")
LABELS = ("official", "audit")
MAX_FACTORS = 3


class LocalityError(ValueError):
    """A monomial violates B3 (not on one node or one face link)."""


class AcyclicityError(ValueError):
    """Two-time (a) reads form a cycle: no staged exact inverse."""


@dataclass(frozen=True, slots=True)
class GearType:
    """name; readout label (OD1, readout only); Yee link axis (metadata); documented field sign s = +1/-1 used ONLY by
    the reciprocity checker (force blocks satisfy u = s * dPhi/db); s = -1 requires a justification ``sign_why``.
    None of these enters the dynamics."""
    name: str
    label: str = "official"
    link: int | None = None
    sign: int = 1
    sign_why: str = ""

    def __post_init__(self):
        if type(self.name) is not str or not self.name:
            raise ValueError("gear name must be a non-empty string")
        if self.label not in LABELS:
            raise ValueError(f"gear label must be one of {LABELS}, got {self.label!r}")
        if self.link is not None and (type(self.link) is not int or not 0 <= self.link < 3):
            raise ValueError("link must be None (node gear) or a Yee axis 0, 1, 2 (+x, +y, +z)")
        if self.sign not in (1, -1) or type(self.sign) is not int:
            raise ValueError("field sign must be +1 or -1")
        if type(self.sign_why) is not str:
            raise TypeError("sign_why must be a string")
        if self.sign == -1 and not self.sign_why.strip():
            raise ValueError(f"gear {self.name!r}: field sign -1 needs a justification (sign_why); per S4-M2 all signs "
                             "can be +1 under the first-order inversion, so every -1 must be explained")


@dataclass(frozen=True, slots=True, order=True)
class Factor:
    gear: int
    offset: tuple[int, int, int]
    field: str


@dataclass(frozen=True, slots=True)
class Monomial:
    target: int
    coeff: int
    factors: tuple[Factor, ...]

    @property
    def degree(self) -> int:
        return len(self.factors)

    @property
    def direction(self) -> int | None:
        """Face direction index (0..5) of the link this monomial lives on, or None if on-site."""
        return check_locality(f.offset for f in self.factors)


def check_locality(offsets: Iterable[tuple[int, int, int]]) -> int | None:
    """B3: all offsets (with the target at 0) in {0, e} for one face direction e. Returns e's index or None."""
    used = set()
    for off in offsets:
        off = offset_tuple(off)
        if off == ZERO:
            continue
        if off not in DIRECTIONS:
            kind = "edge" if sorted(map(abs, off)) == [0, 1, 1] else (
                "diagonal" if sorted(map(abs, off)) == [1, 1, 1] else "non-neighbour")
            raise LocalityError(f"offset {off} is a {kind} offset; only 0 and the six face offsets are legal (B3)")
        used.add(off)
    if len(used) > 1:
        raise LocalityError(f"monomial touches three nodes (offsets 0 and {sorted(used)}); B3 allows one node or "
                            "one face link")
    return DIRECTIONS.index(next(iter(used))) if used else None


def inverse_stages(G: int, monomials: Iterable[Monomial]) -> tuple[tuple[int, ...], ...]:
    """Layer the gear types by their two-time (a) reads; raise AcyclicityError on a cycle."""
    deps = [set() for _ in range(G)]
    for m in monomials:
        for f in m.factors:
            if f.field == "a":
                deps[m.target].add(f.gear)
    done: set[int] = set()
    remaining = set(range(G))
    stages = []
    while remaining:
        ready = sorted(t for t in remaining if deps[t] <= done)
        if not ready:
            cyc = sorted(remaining)
            raise AcyclicityError(f"two-time (a) reads are cyclic among gear types {cyc}; no staged exact inverse")
        stages.append(tuple(ready))
        done.update(ready)
        remaining.difference_update(ready)
    return tuple(stages)


class Tensor:
    """Validated, canonical, immutable unit-cell tensor. See the module docstring."""

    __slots__ = ("gears", "monomials", "stages", "designations", "Q", "_index")

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Tensor is immutable; construct a new tensor before a run")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError("Tensor is immutable")

    def __init__(self, gears: Sequence, monomials: Iterable, designated_one_way: Iterable = (),
                 strict_support: bool = False, Q: int | None = None, q_lattice: Iterable[str] = ()):
        if Q is not None and (type(Q) is not int or Q < 1):
            raise ValueError("Q must be None or a positive int")
        self.Q = Q
        gear_list = []
        for g in gears:
            if isinstance(g, GearType):
                gear_list.append(g)
            elif isinstance(g, str):
                gear_list.append(GearType(g))
            elif isinstance(g, dict):
                gear_list.append(GearType(g["name"], g.get("label", "official"), g.get("link"), g.get("sign", 1),
                                          g.get("sign_why") or ""))
            else:
                raise TypeError(f"cannot read gear type {g!r}")
        if not gear_list:
            raise ValueError("a tensor needs at least one gear type")
        index = {}
        for i, g in enumerate(gear_list):
            if g.name in index:
                raise ValueError(f"duplicate gear name {g.name!r}")
            index[g.name] = i
        self.gears = tuple(gear_list)
        self._index = MappingProxyType(index)
        merged: dict[tuple[int, tuple[Factor, ...]], int] = {}
        designations: dict[tuple[int, tuple[Factor, ...]], str] = {}
        for raw in monomials:
            meta = None
            if not isinstance(raw, Monomial) and len(raw) == 4:
                raw, meta = tuple(raw[:3]), raw[3]
            m = self._parse(raw)
            key = (m.target, m.factors)
            merged[key] = merged.get(key, 0) + m.coeff
            if meta:
                designations[key] = _designation(meta)
        for item in designated_one_way:
            target, factors, why = item
            m = self._parse((target, 1, factors))
            designations[(m.target, m.factors)] = _designation({"designated_one_way": why})
        mons = [Monomial(t, c, fs) for (t, fs), c in merged.items() if c != 0]
        mons.sort(key=lambda m: (m.target, m.degree, m.factors))
        self.monomials = tuple(mons)
        live = {(m.target, m.factors) for m in mons}
        self.designations = MappingProxyType({k: v for k, v in sorted(designations.items()) if k in live})
        self.stages = inverse_stages(len(self.gears), self.monomials)
        q_lattice = tuple(q_lattice)
        if q_lattice:
            if self.Q is None:
                raise ValueError("q_lattice validation needs the tensor's Q")
            bad = self.q_lattice_violations(q_lattice)
            if bad:
                names = self.names
                raise ValueError(f"q_lattice: {len(bad)} term(s) targeting Q-lattice gears have a u-coefficient not = "
                                 f"0 mod Q = {self.Q}, e.g. target {names[bad[0].target]!r} coefficient {bad[0].coeff}")
        if strict_support:
            bad = self.support_violations()
            if bad:
                names = self.names
                raise LocalityError(
                    "strict_support: physical support (link gears span their link) exceeds one node or one face link "
                    f"for {len(bad)} monomial(s), e.g. target {names[bad[0].target]!r} with factors "
                    f"{[(names[f.gear], f.offset, f.field) for f in bad[0].factors]}")

    # ---------------------------------------------------------------- parsing / validation
    def gear_index(self, ref) -> int:
        if type(ref) is int:
            if not 0 <= ref < len(self.gears):
                raise ValueError(f"gear index {ref} out of range")
            return ref
        if isinstance(ref, str):
            try:
                return self._index[ref]
            except KeyError:
                raise ValueError(f"unknown gear {ref!r}") from None
        raise TypeError(f"gear reference must be a name or an index, got {ref!r}")

    def _parse(self, raw) -> Monomial:
        if isinstance(raw, Monomial):
            target, coeff, factors = raw.target, raw.coeff, raw.factors
        else:
            if len(raw) != 3:
                raise ValueError(f"monomial must be (target, coeff, factors), got {raw!r}")
            target, coeff, factors = raw
        t = self.gear_index(target)
        if type(coeff) is not int:
            raise TypeError(f"coefficient must be a Python int, got {coeff!r}")
        factors = tuple(factors)
        if len(factors) > MAX_FACTORS:
            raise ValueError(f"at most {MAX_FACTORS} factors (rank <= 4), got {len(factors)}")
        parsed = []
        for f in factors:
            if isinstance(f, Factor):
                gear, off, field = f.gear, f.offset, f.field
            else:
                if len(f) != 3:
                    raise ValueError(f"factor must be (gear, offset, field), got {f!r}")
                gear, off, field = f
            if field not in FIELDS:
                raise ValueError(f"factor field must be 'a' or 'b', got {field!r}")
            parsed.append(Factor(self.gear_index(gear), offset_tuple(off), field))
        check_locality(f.offset for f in parsed)
        return Monomial(t, coeff, tuple(sorted(parsed)))

    # ---------------------------------------------------------------- properties
    @property
    def G(self) -> int:
        return len(self.gears)

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(g.name for g in self.gears)

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(g.label for g in self.gears)

    @property
    def rank(self) -> int:
        """Rank on v = (1, b, a): max degree + 1."""
        return 1 + max((m.degree for m in self.monomials), default=0)

    @property
    def b_only(self) -> bool:
        return all(f.field == "b" for m in self.monomials for f in m.factors)

    @property
    def has_constant(self) -> bool:
        return any(m.degree == 0 for m in self.monomials)

    def __len__(self):
        return len(self.monomials)

    def __eq__(self, other):
        return (isinstance(other, Tensor) and self.gears == other.gears and self.monomials == other.monomials
                and self.designations == other.designations and self.Q == other.Q)

    def __hash__(self):
        return hash((self.gears, self.monomials))

    def same_dynamics(self, other: "Tensor") -> bool:
        """Equal indexed coefficient templates. Ignores Q as well as observer metadata;
        equal complete update laws also require equal engine divisors."""
        return isinstance(other, Tensor) and self.G == other.G and self.monomials == other.monomials

    def is_designated(self, m: Monomial) -> str | None:
        return self.designations.get((m.target, m.factors))

    def __repr__(self):
        return (f"Tensor(G={self.G}, monomials={len(self.monomials)}, rank={self.rank}, stages={len(self.stages)}, "
                f"Q={self.Q})")

    def census(self) -> dict:
        """Count entries on nodes vs on each face link (B3 census)."""
        out = {"node": 0, "link": 0, "by_degree": [0, 0, 0, 0]}
        for m in self.monomials:
            out["link" if m.direction is not None else "node"] += 1
            out["by_degree"][m.degree] += 1
        return out

    def q_lattice_violations(self, patterns: Iterable[str], Q: int | None = None) -> list[Monomial]:
        """Terms targeting a gear whose name matches one of ``patterns`` (fnmatch, e.g. "ref.*") with a u-coefficient
        not = 0 mod Q (default: the tensor's Q). An empty list is a sufficient termwise condition for
        preserving r mod Q. It is not necessary: integer-valued combinations may have divisible values
        without divisible coefficients. A rho_L0 reversor additionally needs b-only inputs or a separate
        proof for old-a reads; divisibility alone does not establish time-reversal symmetry."""
        from fnmatch import fnmatchcase
        Q = self.Q if Q is None else Q
        if Q is None:
            raise ValueError("no Q given")
        pats = tuple(patterns)
        hit = {i for i, g in enumerate(self.gears) if any(fnmatchcase(g.name, p) for p in pats)}
        return [m for m in self.monomials if m.target in hit and m.coeff % Q != 0]

    def physical_support(self, m: Monomial) -> list[tuple[int, int, int]]:
        """Nodes (relative to the target's storage node) touched by monomial m, a link gear occupying both ends of
        its Yee link."""
        pts = set()
        for gear, off in [(m.target, ZERO)] + [(f.gear, f.offset) for f in m.factors]:
            pts.add(off)
            k = self.gears[gear].link
            if k is not None:
                e = DIRECTIONS[2 * k]
                pts.add((off[0] + e[0], off[1] + e[1], off[2] + e[2]))
        return sorted(pts)

    def support_violations(self) -> list[Monomial]:
        """Diagnostic (stricter than the binding storage rule): monomials whose PHYSICAL support is not one node or
        one face link. A design fact to report, not a failure, unless the tensor is built with strict_support=True
        (opt-in, stage 0.1)."""
        bad = []
        for m in self.monomials:
            pts = self.physical_support(m)
            ok = len(pts) == 1 or (len(pts) == 2 and tuple(q - p for p, q in zip(*pts)) in DIRECTIONS)
            if not ok:
                bad.append(m)
        return bad

    # ---------------------------------------------------------------- serialisation
    def to_dict(self) -> dict:
        names = self.names

        def facs(fs):
            return [[names[f.gear], list(f.offset), f.field] for f in fs]
        return {
            "format": FORMAT,
            "Q": self.Q,
            "gears": [{"name": g.name, "label": g.label, "link": g.link, "sign": g.sign, "sign_why": g.sign_why}
                      for g in self.gears],
            "monomials": [[names[m.target], m.coeff, facs(m.factors)] for m in self.monomials],
            "designated_one_way": [[names[t], facs(fs), why] for (t, fs), why in self.designations.items()],
        }

    @classmethod
    def from_dict(cls, data: dict, strict_support: bool = False) -> "Tensor":
        if data.get("format") != FORMAT:
            raise ValueError(f"unknown tensor format {data.get('format')!r}")
        return cls(data["gears"], [(t, c, [(g, tuple(o), fl) for g, o, fl in fs]) for t, c, fs in data["monomials"]],
                   [(t, [(g, tuple(o), fl) for g, o, fl in fs], why)
                    for t, fs, why in data.get("designated_one_way", [])], strict_support=strict_support,
                   Q=data.get("Q"))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"))

    @classmethod
    def from_json(cls, text: str, strict_support: bool = False) -> "Tensor":
        return cls.from_dict(json.loads(text), strict_support=strict_support)

    @property
    def fingerprint(self) -> str:
        """sha256 of the full canonical form (dynamics + metadata)."""
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    @property
    def dynamics_fingerprint(self) -> str:
        """sha256 of G and indexed monomials; Q and metadata are excluded.
        Identify the complete law by (this hash, Q), or by the full fingerprint
        for a tensor that records Q. Kept unchanged for regression compatibility."""
        blob = [self.G, [[m.target, m.coeff, [[f.gear, list(f.offset), f.field] for f in m.factors]]
                         for m in self.monomials]]
        return hashlib.sha256(json.dumps(blob, separators=(",", ":")).encode()).hexdigest()


def _designation(meta) -> str:
    if not isinstance(meta, dict) or set(meta) != {"designated_one_way"}:
        raise ValueError("term metadata must be {'designated_one_way': '<justification>'}")
    why = meta["designated_one_way"]
    if type(why) is not str or not why.strip():
        raise ValueError("designated_one_way needs a non-empty justification")
    return why


class TensorBuilder:
    """Incremental construction; every term is validated (B3, names, fields, coefficient) when it is added."""

    def __init__(self):
        self._gears: list[GearType] = []
        self._names: dict[str, int] = {}
        self._terms: list[tuple] = []

    def gear(self, name: str, label: str = "official", link: int | None = None, sign: int = 1,
             sign_why: str = "") -> str:
        if name in self._names:
            raise ValueError(f"duplicate gear name {name!r}")
        self._names[name] = len(self._gears)
        self._gears.append(GearType(name, label, link, sign, sign_why))
        return name

    def term(self, target, coeff: int, *factors, designated_one_way: str | None = None) -> None:
        probe = Tensor(self._gears, [])          # validates against the gears declared so far
        probe._parse((target, coeff, factors))   # raises on any illegal entry
        t = (target, coeff, tuple(factors))
        if designated_one_way is not None:
            t = t + ({"designated_one_way": _designation({"designated_one_way": designated_one_way})},)
        self._terms.append(t)

    def extend(self, block: "Block") -> None:
        for g in block.gears:
            self.gear(g.name, g.label, g.link, g.sign, g.sign_why)
        for t in block.terms:
            self._terms.append(tuple(t))

    def build(self, strict_support: bool = False, Q: int | None = None) -> Tensor:
        return Tensor(self._gears, self._terms, strict_support=strict_support, Q=Q)


@dataclass(frozen=True)
class Block:
    """One layer's tensor block: gear types (LOCAL names) + the terms that target them.

    terms: ``(target, coeff, factors)`` or ``(target, coeff, factors, {"designated_one_way": "<why>"})``; gear
    references are local names (prefixed by ``name`` in ``compose``) or qualified names "<namespace>.<gear>" of
    other blocks. ``vacuum``: local gear name -> vacuum remainder r0 (initial data for prepare/; the vacuum gear is
    (0, 0, r0)). ``params``: the documented parameters the builder was called with. ``name=None``: names are global
    and used as given (no namespace). ``Q``: the divisor scale the block was built with (layer builders MUST set it;
    None only for blocks without Q-dependent entries); compose / Engine / vacuum_state assert ONE Q.
    """
    gears: tuple[GearType, ...]
    terms: tuple[tuple, ...]
    name: str | None = None
    vacuum: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    doc: str = ""
    Q: int | None = None          # the Q the block was built with (None: no Q-scaled entry); ONE Q is enforced

    def qualify(self, ref):
        if not isinstance(ref, str):
            raise TypeError("blocks reference gears by name")
        if self.name is None or "." in ref:
            return ref
        return f"{self.name}.{ref}"


def reference_names(prefix: str = "R") -> tuple[str, ...]:
    return tuple(f"{prefix}{g:02d}" for g in range(48))


def reference_block(Q: int = 1, body_signs=(1, 1, 1), prefix: str = "R", label: str = "official") -> Block:
    """The 48 reference channels as a tensor block, read from the repo's own coupling (no constant copied by hand).

    Uses the SENDER form of the fixed L0 matrices: the sender gear g at node x
    adds weights[d][g] * b to the receiver gear ports[d][g] at node x + e_d. Written for the receiver at node y, its
    factor is the b of gear g at offset -e_d with coefficient Q * weights[d][g] (Q-scaling theorem: D = 6Q, entries
    x Q, remainders x Q). Gear type g carries the 2O label g of universe24.algebra.group_2o.
    """
    from universe24.algebra.coupling import Coupling  # exact construction-time algebra
    from universe24.algebra.group_2o import DIRECTIONS as REF_DIRECTIONS

    if type(Q) is not int or Q < 1:
        raise ValueError("Q must be a positive int")
    if tuple(REF_DIRECTIONS) != DIRECTIONS:
        raise AssertionError("direction order differs from universe24")
    c = Coupling(tuple(body_signs))
    names = reference_names(prefix)
    terms = []
    for d, e in enumerate(REF_DIRECTIONS):
        back = (-e[0], -e[1], -e[2])
        for g in range(48):
            terms.append((names[c.ports[d][g]], Q * c.weights[d][g], ((names[g], back, "b"),)))
    return Block(tuple(GearType(n, label) for n in names), tuple(terms), Q=Q)


def reference_block_receiver_form(Q: int = 1, body_signs=(1, 1, 1), prefix: str = "R") -> Block:
    """Same block from the RECEIVER form of the L0 matrices (gear h reads weights[d][h] * b of gear ports[d][h]
    at y + e_d). Used only as an independent consistency check of reference_block."""
    from universe24.algebra.coupling import Coupling
    from universe24.algebra.group_2o import DIRECTIONS as REF_DIRECTIONS

    c = Coupling(tuple(body_signs))
    names = reference_names(prefix)
    terms = []
    for h in range(48):
        for d, e in enumerate(REF_DIRECTIONS):
            terms.append((names[h], Q * c.weights[d][h], ((names[c.ports[d][h]], tuple(e), "b"),)))
    return Block(tuple(GearType(n) for n in names), tuple(terms), Q=Q)


def compose(*blocks: Block, strict_support: bool = False, q_lattice: Iterable[str] = ()) -> Tensor:
    """Merge blocks into ONE tensor. Gear order = block order, then the block's gear order. A block with a namespace
    ``name`` gets qualified gear names "<name>.<gear>"; its terms' local references are qualified the same way and
    qualified references ("other.gear") cross layers. Names must be unique; unknown references raise.
    ``strict_support=True`` (opt-in) also rejects entries whose physical support exceeds one link."""
    declared = {blk.Q for blk in blocks if blk.Q is not None}
    if len(declared) > 1:
        raise ValueError(f"ONE divisor: blocks were built with different Q {sorted(declared)}")
    gears, terms, spaces = [], [], set()
    for blk in blocks:
        if blk.name is not None:
            if type(blk.name) is not str or not blk.name or "." in blk.name:
                raise ValueError(f"bad namespace {blk.name!r}")
            if blk.name in spaces:
                raise ValueError(f"duplicate namespace {blk.name!r}")
            spaces.add(blk.name)
            for g in blk.gears:
                if "." in g.name:
                    raise ValueError(f"local gear name {g.name!r} of block {blk.name!r} must not contain '.'")
        for g in blk.gears:
            gears.append(GearType(blk.qualify(g.name), g.label, g.link, g.sign, g.sign_why))
        for t in blk.terms:
            target, coeff, factors = t[0], t[1], t[2]
            q = (blk.qualify(target), coeff, tuple((blk.qualify(f[0]), f[1], f[2]) for f in factors))
            terms.append(q + tuple(t[3:]))
    return Tensor(gears, terms, strict_support=strict_support, Q=declared.pop() if declared else None,
                  q_lattice=q_lattice)


def build(*blocks: Block, strict_support: bool = False, q_lattice: Iterable[str] = ()) -> Tensor:
    """Alias of compose (kept for blocks without namespace)."""
    return compose(*blocks, strict_support=strict_support, q_lattice=q_lattice)


def vacuum_map(*blocks: Block) -> dict:
    """Qualified gear name -> vacuum remainder, from the blocks' ``vacuum`` data (initial data only)."""
    out = {}
    for blk in blocks:
        for local, r0 in blk.vacuum.items():
            out[blk.qualify(local)] = r0
    return out
