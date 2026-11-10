"""layers/: TENSOR BLOCKS ONLY (no state, no dynamics, no observation).

Contract for every layer (stage 1 and later):
* one function per layer, ``build_<layer>(*, Q, <coupling constants>, <vacuum remainders>, name="<namespace>")``
  returning a ``core.tensor.Block``;
* the parameters are keyword-only and documented in the builder's docstring; the builder stores them in
  ``Block.params``. Q is the common divisor scale (D = 6Q for EVERY gear of the composed system); integer coupling
  constants are written into monomial coefficients (Q-scaled where the layer's convention says so); vacuum remainders
  go to ``Block.vacuum`` (local gear name -> r0) and are used only by prepare/;
* gear names are LOCAL (no '.'); ``compose`` qualifies them as "<namespace>.<gear>"; terms read other layers' gears by
  qualified name (e.g. "ref.R07", "em.A_x");
* force couplings must be reciprocal (u = s * dPhi/db, field sign s in GearType.sign); a deliberately one-way b-only
  term carries ``{"designated_one_way": "<justification>"}`` as its 4th element; ``core.reciprocity`` checks it;
* two-time (a) reads must stay acyclic (``Tensor.stages``);
* new layers are written in deviation form (their vacuum gear is (0, 0, r0) and every term targeting them vanishes
  when the layer's own gears are 0), so the vacuum is the reference board bit for bit;
* LINKS FROZEN convention (G9-c, dynamic base links): a layer that couples to the reference board through link
  gears takes its link couplings as keyword parameters (e.g. ``kappa``, ``lam``, ``beta``); with all of them 0 the
  composed run must equal today's board exactly and the link gears must stay at their vacuum.
  ``observe.audit.frozen_equivalence`` is the check every such layer must pass.
"""
from .reference import build_reference

__all__ = ["build_reference"]
