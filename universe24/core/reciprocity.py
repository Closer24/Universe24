"""Reciprocity checker (design v5 §1b): every FORCE coupling is the gradient of Universe24 potential.

Static check of a Tensor (no state, no dynamics). The b-only part of the input (monomials of degree >= 1 whose
factors are all b) must satisfy

    u_t = s_t * dPhi/db_t        for one translation-invariant polynomial Phi(b),

with s_t the documented field sign of gear type t (GearType.sign, default +1). Equivalently the Jacobian S*J is
symmetric: action = reaction. Every gear with s = -1 must carry a justification (GearType.sign_why; enforced at
construction) and is LISTED in the report (``negative_sign_gears``): per S4-M2 all signs can be +1 under the
first-order inversion, so each -1 is a reviewed exception.

Method (exact, Fractions): a b-only monomial ``c * prod b`` of target t is the derivative of the potential monomial
P = {b_t(0)} + factors with respect to b_t(0); P is taken modulo translations. If n = multiplicity of b_t(0) in P,
the monomial implies phi_P = s_t * c / n. Phi exists iff, for every class P, all present monomials imply the SAME
phi_P and every partner (the derivative of P with respect to each distinct variable b_g(p) of P, a monomial of
target g with coefficient s_g * n_g * phi_P) is present with exactly that coefficient.

Monomials carrying ``designated_one_way: <justification>`` are excluded from the check (they are deliberately
non-reciprocal and say why). The check FAILS iff some undesignated b-only monomial lies in an inconsistent class.
Constants (degree 0) are gradients of linear potentials; monomials with an ``a`` factor are two-time reads and are
not force couplings in this sense; both are skipped and counted.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from fractions import Fraction

from .lattice import ZERO
from .tensor import Factor, Monomial, Tensor


def _sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _canon(variables):
    """Translation-canonical form of a multiset of (gear, offset) variables."""
    best = None
    for _, p in set(variables):
        shifted = tuple(sorted((g, _sub(o, p)) for g, o in variables))
        if best is None or shifted < best:
            best = shifted
    return best


@dataclass
class ReciprocityReport:
    ok: bool
    checked: int
    skipped_constants: int
    skipped_two_time: int
    designated: list = field(default_factory=list)       # [(monomial text, justification)]
    violations: list = field(default_factory=list)       # undesignated non-reciprocal monomials (text, reason)
    missing_partners: list = field(default_factory=list)  # (target name, factors text, expected coefficient)
    negative_sign_gears: list = field(default_factory=list)  # [(gear name, justification)] for every s = -1 gear

    def raise_if_failed(self):
        if not self.ok:
            raise AssertionError("non-reciprocal undesignated b-only couplings:\n" +
                                 "\n".join(f"  {m}: {why}" for m, why in self.violations[:50]))


def monomial_text(tensor: Tensor, m: Monomial) -> str:
    names = tensor.names
    fs = " * ".join(f"{f.field}[{names[f.gear]}]{f.offset}" for f in m.factors) or "1"
    return f"u[{names[m.target]}] += {m.coeff} * {fs}"


def check_reciprocity(tensor: Tensor) -> ReciprocityReport:
    names = tensor.names
    signs = [g.sign for g in tensor.gears]
    present: dict[tuple, int] = {}
    classes: dict[tuple, list] = defaultdict(list)
    n_const = n_two = 0
    designated = []
    for m in tensor.monomials:
        if m.degree == 0:
            n_const += 1
            continue
        if any(f.field != "b" for f in m.factors):
            n_two += 1
            continue
        why = tensor.is_designated(m)
        if why is not None:
            designated.append((monomial_text(tensor, m), why))
            continue
        present[(m.target, m.factors)] = m.coeff
        variables = [(m.target, ZERO)] + [(f.gear, f.offset) for f in m.factors]
        n = variables.count((m.target, ZERO))
        classes[_canon(variables)].append((m, Fraction(signs[m.target] * m.coeff, n)))
    violations, missing = [], []
    for cls, members in classes.items():
        phis = {phi for _, phi in members}
        reason = None
        if len(phis) != 1:
            reason = f"inconsistent potential coefficients {sorted(phis)} in class {cls}"
        else:
            phi = phis.pop()
            for g, p in sorted(set(cls)):
                rest = list((gg, _sub(o, p)) for gg, o in cls)
                rest.remove((g, ZERO))
                key = (g, tuple(sorted(Factor(gg, o, "b") for gg, o in rest)))
                n_g = sum(1 for v in cls if v == (g, p))
                expected = signs[g] * n_g * phi
                got = present.get(key, 0)
                if got != expected:
                    reason = reason or "partner monomial missing or with a different coefficient"
                    missing.append((names[g], " * ".join(f"b[{names[f.gear]}]{f.offset}" for f in key[1]) or "1",
                                    str(expected), got))
        if reason:
            for m, _ in members:
                violations.append((monomial_text(tensor, m), reason))
    checked = sum(len(v) for v in classes.values())
    negative = [(g.name, g.sign_why) for g in tensor.gears if g.sign == -1]   # justification enforced by GearType
    return ReciprocityReport(not violations, checked, n_const, n_two, designated, violations, missing, negative)
