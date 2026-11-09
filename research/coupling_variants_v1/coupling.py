"""Candidate 2O-covariant six-port couplings, fixed before a run.

A ``VariantCoupling`` is an explicitly separate candidate variant (AGENTS.md),
never the reference model. It is a constant table on the same 48 channels and
the same periodic cube as the reference engine. For each spatial direction
``d`` in the engine order ``(+x,-x,+y,-y,+z,-z)`` and each channel ``g`` it
stores one port ``ports[d][g]`` and one weight ``weights[d][g]``, with exactly
the meaning of ``Coupling.ports`` and ``Coupling.weights`` in
``universe24/core/coupling.py``. The eight reference couplings are members.

The owner's constraint: the algebra of 2O stays in the initial tensor.
``VariantCoupling.validate`` therefore requires

* six direction rows of 48 Python integers (no bools);
* every ``ports[d]`` a permutation of the 48 channels (exactly one input from
  each of the six face neighbours) and every weight ``+1`` or ``-1`` (signed
  permutation matrices, as in docs/MODEL.md; a zero would delete a port and a
  larger magnitude would rescale Rule3's input);
* reciprocity, exactly as ``Coupling.validate``:
  ``ports[d^1][ports[d][g]] == g`` and ``weights[d^1][ports[d][g]] == weights[d][g]``;
* 2O covariance, the relation the reference coupling satisfies:
  ``ports[R(h)d][h*g] == h*ports[d][g]`` and ``weights[R(h)d][h*g] == weights[d][g]``
  for every ``h`` in 2O (``h*g`` the group product, ``R(h)`` its cube rotation).

Covariance holds exactly for the body-action tables ``ports[d][g] = g*B_u``,
``weights[d][g] = w_u`` with ``u = R(g)^-1 d``: the table is fixed by its
identity column, ``B_u = ports[u][e]`` and ``w_u = weights[u][e]``. Reciprocity
then pairs every body direction ``u`` with ``v = -R(B_u)^-1 u != u``; it needs
``B_v = B_u^-1`` and ``w_v = w_u``. The validated family therefore has 15
pairings of the six body directions, and for each pair 4 rotations x 2 lifts
(a z twist) x 2 signs: 15 * 16**3 = 61,440 labeled tables (``covariant_family``).
The axial pairing {+x,-x},{+y,-y},{+z,-z} gives the 4,096 tables of
docs/COUPLING_FAMILIES.md; ``m=(0,1,3)`` gives the eight reference tables.
"""
from __future__ import annotations

import cmath
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import product
import json
import re
from typing import Iterator

from universe24.core.coupling import Coupling
from universe24.core.group_2o import DIRECTIONS, QX, QY, QZ, group, rotate, rotate_inverse

CHANNELS = 48
IDENTITY_LABEL = 0
CENTRAL_LABEL = 14
COUPLING_FORMAT = "universe24-variant-coupling-v1"
SIGN_TRIPLES = tuple(product((1, -1), repeat=3))
AXIAL_PAIRS = ((0, 1), (2, 3), (4, 5))
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}")

Table = tuple[tuple[int, ...], ...]


def sign_text(signs) -> str:
    """``(1,-1,1) -> '+-+'``."""
    return "".join("+" if s > 0 else "-" for s in signs)


def _rows(rows, what: str) -> Table:
    if isinstance(rows, (str, bytes)) or len(rows) != 6:
        raise ValueError(f"{what} must have six direction rows (+x,-x,+y,-y,+z,-z)")
    out = []
    for row in rows:
        row = tuple(row)
        if len(row) != CHANNELS:
            raise ValueError(f"every {what} row must have {CHANNELS} entries")
        if any(type(v) is not int for v in row):
            raise TypeError(f"{what} entries must be Python integers")
        out.append(row)
    return tuple(out)


def _ints(values, n: int, what: str) -> tuple[int, ...]:
    values = tuple(values)
    if len(values) != n or any(type(v) is not int for v in values):
        raise ValueError(f"{what} must be {n} Python integers")
    return values


@lru_cache(maxsize=1)
def _rotated_directions() -> tuple[tuple[int, ...], ...]:
    """``[h][d]`` = index of the world direction R(h) e_d."""
    return tuple(tuple(DIRECTIONS.index(rotate(r, e)) for e in DIRECTIONS) for r in group().rotations)


@lru_cache(maxsize=1)
def _commutator_subgroup() -> frozenset[int]:
    """2T, the commutator subgroup of 2O (24 labels); the kernel of ``character``."""
    algebra = group()
    m, inv = algebra.multiplication, algebra.inverses
    sub = {m[m[a][b]][m[inv[a]][inv[b]]] for a in range(CHANNELS) for b in range(CHANNELS)}
    while True:
        closed = sub | {m[x][y] for x in sub for y in sub}
        if closed == sub:
            return frozenset(sub)
        sub = closed


def character(label: int) -> int:
    """The nontrivial one-dimensional character of 2O: +1 on 2T, -1 on the other 24 labels."""
    return 1 if label in _commutator_subgroup() else -1


def partner(u: int, action: int) -> int:
    """Body direction that answers body direction ``u`` through ``B_u``: ``-R(B_u)^-1 u``."""
    x = rotate_inverse(group().rotations[action], DIRECTIONS[u])
    return DIRECTIONS.index(tuple(-c for c in x))


# ------------------------------------------------------------ constructions
def body_action_tables(actions, body_weights) -> tuple[Table, Table]:
    """Tables of the 2O body-action construction (``universe24/core/coupling.py``).

    ``actions[u]`` is the 2O label (``universe24.core.group_2o.group()`` order)
    of the body action ``B_u`` and ``body_weights[u]`` its weight, for the body
    directions ``u`` in the order ``(+x,-x,+y,-y,+z,-z)``:
    ``ports[d][g] = g*B_u`` and ``weights[d][g] = body_weights[u]``, ``u = R(g)^-1 d``.
    """
    actions = _ints(actions, 6, "actions")
    body_weights = _ints(body_weights, 6, "body weights")
    if any(not 0 <= a < CHANNELS for a in actions):
        raise ValueError("actions must be 2O labels 0..47")
    algebra = group()
    ports, weights = [], []
    for direction in DIRECTIONS:
        row, weight = [], []
        for g, rotation in enumerate(algebra.rotations):
            u = DIRECTIONS.index(rotate_inverse(rotation, direction))
            row.append(algebra.multiplication[g][actions[u]])
            weight.append(body_weights[u])
        ports.append(tuple(row))
        weights.append(tuple(weight))
    return tuple(ports), tuple(weights)


def axial_actions(m) -> tuple[int, ...]:
    """2O labels of ``B_(+e_i) = Q_i^(m_i)``, ``B_(-e_i) = B_(+e_i)^-1`` (docs/COUPLING_FAMILIES.md)."""
    m = _ints(m, 3, "axial exponents m")
    if any(not 0 <= k < 8 for k in m):
        raise ValueError("axial exponents must lie in 0..7 (Z/8Z, not reduced modulo 4)")
    algebra = group()
    ids = {q: i for i, q in enumerate(algebra.quaternions)}
    out = []
    for generator, k in zip((QX, QY, QZ), m):
        b = algebra.power(ids[generator], k)
        out.extend((b, algebra.inverses[b]))
    return tuple(out)


def axial_tables(m, signs) -> tuple[Table, Table]:
    """The axial-action family; ``m=(0,1,3)`` is the reference construction."""
    signs = _ints(signs, 3, "signs")
    if any(s not in (-1, 1) for s in signs):
        raise ValueError("signs must be three +/-1 integers")
    return body_action_tables(axial_actions(m), tuple(s for s in signs for _ in (0, 1)))


def reference_tables(signs) -> tuple[Table, Table]:
    """The engine's own tables for one of the eight sign triples (copied, not re-derived)."""
    signs = tuple(signs)
    if signs not in SIGN_TRIPLES:
        raise ValueError("reference signs must be one of the eight +/-1 triples")
    c = Coupling(signs)
    return c.ports, c.weights


def covariant_family() -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Every reciprocal 2O-covariant unit-weight table, as ``(actions, body_weights)``.

    Exhaustive and duplicate-free: the first unpaired body direction ``u`` takes
    each of the 48 actions; ``v = partner(u, B_u)`` must differ from ``u`` and be
    unpaired, and receives ``B_u^-1``. This yields 40*24*8 = 7,680 action tuples
    (15 pairings x 8**3), each with 2**3 pair signs: 61,440 tables in all.
    """
    inverses = group().inverses

    def assign(actions):
        free = [u for u in range(6) if actions[u] is None]
        if not free:
            yield tuple(actions)
            return
        u = free[0]
        for b in range(CHANNELS):
            v = partner(u, b)
            if v == u or actions[v] is not None:
                continue
            actions[u], actions[v] = b, inverses[b]
            yield from assign(actions)
            actions[u] = actions[v] = None

    for actions in assign([None] * 6):
        pairs = pairing(actions)
        for signs in SIGN_TRIPLES:
            weights = [0] * 6
            for (u, v), s in zip(pairs, signs):
                weights[u] = weights[v] = s
            yield actions, tuple(weights)


def pairing(actions) -> tuple[tuple[int, int], ...]:
    """The sorted pairs ``(u, partner(u, B_u))`` of a body-action tuple."""
    return tuple(sorted({tuple(sorted((u, partner(u, a)))) for u, a in enumerate(actions)}))


def _canonical(construction) -> str:
    if construction is None or construction == "":
        return ""
    data = json.loads(construction) if isinstance(construction, str) else construction
    if not isinstance(data, dict) or "kind" not in data:
        raise ValueError("construction must be an object with a 'kind'")
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _derive(construction: str) -> tuple[Table, Table]:
    data = json.loads(construction)
    kind, keys = data["kind"], set(data) - {"kind"}
    if kind == "reference" and keys == {"signs"}:
        return reference_tables(data["signs"])
    if kind == "axial" and keys == {"m", "signs"}:
        return axial_tables(data["m"], data["signs"])
    if kind == "body_actions" and keys == {"actions", "weights"}:
        return body_action_tables(data["actions"], data["weights"])
    raise ValueError(f"unknown construction {construction}")


@lru_cache(maxsize=1)
def _reference_index() -> dict:
    return {reference_tables(s): s for s in SIGN_TRIPLES}


# ------------------------------------------------------------ the coupling
@dataclass(frozen=True, slots=True)
class VariantCoupling:
    """A validated, immutable 2O-covariant six-port table. ``construction`` is
    optional, re-checked provenance (canonical JSON); not part of the fingerprint."""

    name: str
    ports: Table
    weights: Table
    construction: str = ""

    def __post_init__(self):
        if type(self.name) is not str or not _NAME.fullmatch(self.name):
            raise ValueError("name must be 1-64 characters [A-Za-z0-9._+-], starting alphanumeric")
        object.__setattr__(self, "ports", _rows(self.ports, "ports"))
        object.__setattr__(self, "weights", _rows(self.weights, "weights"))
        object.__setattr__(self, "construction", _canonical(self.construction))
        self.validate()

    def validate(self):
        ports, weights = self.ports, self.weights
        for d in range(6):
            if sorted(ports[d]) != list(range(CHANNELS)):
                raise ValueError("Each directional coupling must be a signed permutation")
            if any(w not in (-1, 1) for w in weights[d]):
                raise ValueError("Weights must be +1 or -1 (no deleted or rescaled ports)")
            for g in range(CHANNELS):
                h = ports[d][g]
                if ports[d ^ 1][h] != g or weights[d ^ 1][h] != weights[d][g]:
                    raise ValueError("Nonreciprocal connection")
        multiplication, rotated = group().multiplication, _rotated_directions()
        for h in range(CHANNELS):
            left, turn = multiplication[h], rotated[h]
            for d in range(6):
                port, weight = ports[d], weights[d]
                image_port, image_weight = ports[turn[d]], weights[turn[d]]
                for g in range(CHANNELS):
                    if image_port[left[g]] != left[port[g]] or image_weight[left[g]] != weight[g]:
                        raise ValueError("Coupling is not 2O-covariant")
        if self.construction and _derive(self.construction) != (ports, weights):
            raise ValueError("Tables differ from their declared construction")

    # -- constructors (all stay inside the 2O algebra)
    @classmethod
    def reference(cls, signs=(1, 1, 1)) -> "VariantCoupling":
        """The reference table for one sign triple (for equivalence checks and as a base)."""
        ports, weights = reference_tables(tuple(signs))
        return cls(f"reference{sign_text(signs)}", ports, weights,
                   {"kind": "reference", "signs": list(signs)})

    @classmethod
    def axial(cls, name: str, m, signs=(1, 1, 1)) -> "VariantCoupling":
        """Axial-action family member: body actions ``Q_i^(m_i)`` in place of (0,1,3)."""
        ports, weights = axial_tables(m, signs)
        return cls(name, ports, weights, {"kind": "axial", "m": list(m), "signs": list(signs)})

    @classmethod
    def from_body_actions(cls, name: str, actions, body_weights) -> "VariantCoupling":
        """Any six body actions and six body weights (one ``covariant_family`` member)."""
        ports, weights = body_action_tables(actions, body_weights)
        return cls(name, ports, weights,
                   {"kind": "body_actions", "actions": list(actions), "weights": list(body_weights)})

    def with_body_weights(self, name: str, body_weights) -> "VariantCoupling":
        """Same ports, another sign pattern (equal signs on each answering pair)."""
        return VariantCoupling.from_body_actions(name, self.body_actions, body_weights)

    def z_twisted(self, name: str, twist) -> "VariantCoupling":
        """Multiply ``B_u`` by the central element z where ``twist[u] == 1``
        (a 360-degree twist of the port; both members of a pair must agree)."""
        twist = _ints(twist, 6, "twist")
        if any(t not in (0, 1) for t in twist):
            raise ValueError("twist entries must be 0 or 1")
        multiplication = group().multiplication
        actions = tuple(multiplication[b][CENTRAL_LABEL] if t else b for b, t in zip(self.body_actions, twist))
        return VariantCoupling.from_body_actions(name, actions, self.body_weights)

    def chi_gauged(self, name: str) -> "VariantCoupling":
        """Body weights ``character(B_u) * w_u``. For uniform backgrounds r in {2, 3} this
        coupling is conjugate to ``self`` by J on the 24 channels outside 2T
        (``gauge.chi_gauge_state``), on every side L: it gives no new dynamics."""
        return self.with_body_weights(name, tuple(character(b) * w for b, w in
                                                  zip(self.body_actions, self.body_weights)))

    # -- coordinates in the family
    @property
    def body_actions(self) -> tuple[int, ...]:
        """``B_u = ports[u][e]`` for u in (+x,-x,+y,-y,+z,-z)."""
        return tuple(self.ports[u][IDENTITY_LABEL] for u in range(6))

    @property
    def body_weights(self) -> tuple[int, ...]:
        return tuple(self.weights[u][IDENTITY_LABEL] for u in range(6))

    @property
    def pairs(self) -> tuple[tuple[int, int], ...]:
        """Which body directions answer each other (the axial pairing is (0,1),(2,3),(4,5))."""
        return pairing(self.body_actions)

    # -- identity and labels
    @property
    def fingerprint(self) -> str:
        blob = json.dumps([COUPLING_FORMAT, self.ports, self.weights], separators=(",", ":")).encode()
        return hashlib.sha256(blob).hexdigest()

    @property
    def reference_signs(self) -> tuple[int, int, int] | None:
        """The sign triple if the tables equal a reference coupling, else None."""
        return _reference_index().get((self.ports, self.weights))

    @property
    def is_variant(self) -> bool:
        return self.reference_signs is None

    @property
    def reference_fingerprint(self) -> str | None:
        signs = self.reference_signs
        return None if signs is None else Coupling(signs).fingerprint

    @property
    def label(self) -> str:
        """``reference:+-+`` for a reference table, else ``variant:<name>@<fingerprint[:12]>``."""
        signs = self.reference_signs
        if signs is not None:
            return f"reference:{sign_text(signs)}"
        return f"variant:{self.name}@{self.fingerprint[:12]}"

    # -- read-only linear algebra for band analysis
    def matrix(self, d: int) -> Table:
        """Signed 48x48 matrix P[d][g][h] (receiver g, sender channel h at x+e_d), as ``Coupling.matrix``."""
        if type(d) is not int or not 0 <= d < 6:
            raise ValueError("Direction must be 0..5")
        return tuple(tuple(self.weights[d][g] if h == self.ports[d][g] else 0
                           for h in range(CHANNELS)) for g in range(CHANNELS))

    def bloch_matrix(self, k) -> tuple[tuple[complex, ...], ...]:
        """``A(k) = sum_d exp(i k.e_d) P[d]``, k in radians per site, Hermitian by reciprocity.

        A plane wave ``b(x,h) = c_h exp(i k.x)`` has input ``u(x,g) = exp(i k.x) (A(k) c)_g``;
        in the large-amplitude regime an eigenvalue lambda gives cos(omega) ~ lambda/6.
        """
        k = tuple(float(c) for c in k)
        if len(k) != 3:
            raise ValueError("k must have three components")
        phases = [cmath.exp(1j * (k[0] * dx + k[1] * dy + k[2] * dz)) for dx, dy, dz in DIRECTIONS]
        rows = []
        for g in range(CHANNELS):
            row = [0j] * CHANNELS
            for d in range(6):
                row[self.ports[d][g]] += self.weights[d][g] * phases[d]
            rows.append(tuple(row))
        return tuple(rows)

    # -- serialization
    def to_json(self) -> dict:
        data = {"format": COUPLING_FORMAT, "name": self.name}
        if self.construction:
            data["construction"] = json.loads(self.construction)
        data["fingerprint"] = self.fingerprint
        data["ports"] = [list(row) for row in self.ports]
        data["weights"] = [list(row) for row in self.weights]
        return data

    @classmethod
    def from_json(cls, data: dict) -> "VariantCoupling":
        if not isinstance(data, dict):
            raise TypeError("Expected a JSON object for the coupling")
        allowed = {"format", "name", "construction", "fingerprint", "ports", "weights"}
        required = {"format", "name", "fingerprint", "ports", "weights"}
        if set(data) - allowed:
            raise ValueError(f"Unsupported coupling keys: {sorted(set(data) - allowed)}")
        if required - set(data):
            raise ValueError(f"Missing coupling keys: {sorted(required - set(data))}")
        if data["format"] != COUPLING_FORMAT:
            raise ValueError("Bad variant coupling format")
        coupling = cls(data["name"], data["ports"], data["weights"], data.get("construction"))
        if data["fingerprint"] != coupling.fingerprint:
            raise ValueError("Variant coupling fingerprint mismatch")
        return coupling
