"""Integration helpers for the gravity layer (NEW file; manager/integrator questions C3, C4, E1 current, 10:5x).
Tensor blocks only; the frozen layers/gravity.py is imported read-only.

C3 - Universe24 LAPSE RULE. h-bar^{00} has two implementations: the metric block's WAVE gear (metric.h00, sourced reciprocally
by build_lapse) and OD2's rounding-free ACCUMULATOR (od2.h00, slaved to the harmonic condition; Sum_x h00 exactly
frozen, so the closed-board k = 0 obstruction F4 is handled by the prepared R-a background + the k = 0 offset). A system
must use exactly Universe24 of them as THE lapse, and every matter species reads that one:
  * lapse="wave": metric (10 gears) + build_lapse(field="metric.h00") [reciprocal: Newton III exact] + beta on it.
    No OD2 block. (Closed board: the uniform mode grows ~ t^2 (F4); use for static/short demos.)
  * lapse="od2": OD2 (hij F-gears + h0i, h00 accumulators) + build_lapse_oneway(field="od2.h00") [designated: the
    accumulator must stay rounding-free; energy enters through the prepared Hamiltonian-constraint data (R-a) and the
    stress chain] + beta on od2.h00. NO metric block (OD2 already contains hij; its 0-mu components ARE the
    accumulators). This is the closed-board-legal default.
  Never both: the metric block's h00/h0i duplicate OD2's and would be a second lapse on the same rest clock.
C4 - od2_hop_stress_scaled: the OD2 stress with a DIVISOR (coefficient kappa * c / divisor, exact or ValueError).
E1 - dressed_link_potential: the lapse-dressed transport bilinear per link, lambda_link * c b_t(x) b_s(x+e) with
  lambda_link = 1 - c_link (F_x + F_y)/P (exactly the factor build_lapse applies); its F-dependent part is
  degree 3 (F b b), so as a SOURCE (e.g. of E1's A) it is a rank-4 entry (OD4 ruling applies).
"""
from __future__ import annotations
from fractions import Fraction
from typing import Sequence
from ..core.tensor import Block
from . import gravity as gr
ONEWAY_LAPSE_WHY = 'one-way lapse read of the OD2 accumulator h00 (THE lapse when OD2 is on): the accumulator must stay rounding-free (exact harmonic constants); matter energy enters through the prepared Hamiltonian-constraint data (R-a) and the stress chain, not as a direct source'

def build_lapse_oneway(*, P: int, field: str, matters: Sequence[gr.MatterSpec], gamma: str='GR', name: str='lapse') -> Block:
    """The universal lapse factors (clock on mass entries, link on transport entries; same coefficients as
    build_lapse) as a Universe24-WAY single-time read of ``field`` (designated): no source into the field."""
    specs = [gr._resolve_carriers(m) for m in matters]
    pot = gr.lapse_potential(field, P, specs, gamma)
    only = [s.q(g) for s in specs for g in s.gears]
    terms = gr.gradient_terms(pot, only=only, designation=ONEWAY_LAPSE_WHY, what='oneway lapse')
    return Block((), tuple(terms), name=name, params={'P': P, 'field': field, 'gamma': gamma, 'oneway': True, 'matters': tuple((m.name for m in matters))}, doc='one-way universal lapse read (THE lapse = OD2 accumulator h00)')

def od2_hop_stress_scaled(ns: str, spec: gr.MatterSpec, kappa: int, divisor: int) -> list:
    """C4: od2_hop_stress with coefficient kappa * c / divisor (c the hop weight); every coefficient must be an integer
    (ValueError otherwise). Off-diagonal components carry the extra 1/2 as in od2_hop_stress."""
    if type(divisor) is not int or divisor < 1:
        raise ValueError('divisor must be a positive int')
    out = []
    for i in range(3):
        for j in range(i, 3):
            comp = gr.comp_name(i, j)
            for t, s, ax, c in spec.hops:
                if ax not in (i, j):
                    continue
                coeff = Fraction(kappa * c, divisor * (1 if i == j else 2))
                if coeff.denominator != 1:
                    raise ValueError(f'od2 stress: kappa*c/(divisor*{(1 if i == j else 2)}) = {coeff} is not an integer')
                if coeff:
                    out.append((comp, int(coeff), ((spec.q(t), (0, 0, 0), 'b'), (spec.q(s), gr.AXES[ax], 'b'))))
    return out

def gravity_blocks(*, P: int, k: int, matters: Sequence[gr.MatterSpec], lapse: str='od2', stress_spec: gr.MatterSpec | None=None, stress_kappa: int=1, stress_divisor: int=1, beta: bool=True) -> list[Block]:
    """C3 builder flag: the gravity blocks with Universe24 lapse (see the module docstring)."""
    if lapse == 'wave':
        blocks = [gr.build_metric(), gr.build_lapse(P=P, field='metric.h00', matters=matters)]
        field = 'metric.h00'
    elif lapse == 'od2':
        stress = () if stress_spec is None else od2_hop_stress_scaled(stress_spec.name, stress_spec, stress_kappa, stress_divisor)
        blocks = [gr.build_od2(stress=stress), build_lapse_oneway(P=P, field='od2.h00', matters=matters)]
        field = 'od2.h00'
    else:
        raise ValueError("lapse must be 'wave' or 'od2'")
    if beta:
        blocks.append(gr.build_beta(P=P, k=k, field=field, matters=matters))
    return blocks

def dressed_link_potential(spec: gr.MatterSpec, field: str, P: int, gamma: str='GR') -> list:
    """E1 question: the lapse-dressed transport bilinears of one matter species, per link (x, x + e_axis), as potential
    monomials (coeff, [(gear, offset), ...]): c b_t(x) b_s(x+e) [free] and -c_link c (F_x + F_y)/P b_t(x) b_s(x+e)
    [dressing, degree 3]. Contract with the charge structure (J') to obtain the dressed link current. Generic hops only
    (difference-form Laplacian transport carries no charge current)."""
    _, c_link = gr.lapse_factors(spec.order, gamma)
    out = []
    for t, s, ax, c in spec.hops:
        e = gr.AXES[ax]
        mono = [(spec.q(t), (0, 0, 0)), (spec.q(s), e)]
        out.append((Fraction(c), mono))
        out.append((-c_link * Fraction(c) / P, [(field, (0, 0, 0))] + mono))
        out.append((-c_link * Fraction(c) / P, [(field, e)] + mono))
    return out
