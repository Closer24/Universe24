# One execution and state contract

There is one supported CLI (`python -m universe24`), one built-in coupling
(`model.py`), and one Engine. Preparation seals a complete immutable bundle;
execution saves transitions and passive canonical clicks; verification checks
reexecution, inverse and every record. Trace files never feed the dynamics.

1. Every channel uses exactly `ell,r_next=divmod(2*u+r,6); a_next=b; b_next=ell-a`.
2. Exactly 48 explicit channels retain `(a,b,r)` at each node: 144 integers,
   including scheduling, memories and clocks. No padding, hidden link queue,
   edge history, discarded carry or extra dynamically evolving workspace.
3. Updates are synchronous from one complete old snapshot. The tensor has
   integer coefficients and degree at most three. Each monomial has target plus
   at most one face edge support. No diagonal reads or runtime callback.
4. Every supported schema-3 bundle obeys `2O-left-regular-cube/1`. Old-a
   dependency acyclicity and transitivity exclude old-a reads for this action.
   See [the exact algebra](COUPLING_ALGEBRA.md).
5. Tensor, seed, exhaustive ownership, protocol and model metadata are bound
   by hashes. Execution rejects corruption and recomputes the law certificate.
   A model name, role or user-supplied physics label grants no acceptance.
6. Raw engine arithmetic supports arbitrary signed integers. The selected
   built-in preparation proves a narrower future-positive six-face Boolean
   domain. These are different assertions.
7. Fixed operation count does not bound integer bit growth or wall-clock cost.
   Run reports expose integer costs. Global update index orders computation;
   it is not a privileged physical proper time inferred from observations.

The six node ports group eight regular channels each by direction. An edge
reference identifies the same periodic adjacency from either endpoint; it
adds no dynamical state or shared metric length. Channel grouping does not
force each polynomial to read exclusively that port, while the current proved
sector runs all six directional circuits simultaneously. Each uses three live
Boolean fields plus five retained marker bits; the circuits do not exchange
signals between faces. See [the observer contract](OBSERVATION.md).

One physical interpretation must ultimately use the same tensor, seed domain,
source accounts and metric for every retained subsystem. Separate tensors'
successes cannot be pooled. The current physical criteria in [PHYSICS.md](PHYSICS.md)
remain blocked where stated; `verify --require-physics` fails accordingly.

Generated local runs belong under ignored `runs/`. Historical experiments and
tracked outputs are absent from the current tree; the README pins their Git
history. Engine tests and the independent scalar oracle remain active. Run
full unittest discovery and `python -m universe24.system.checks` after
structural changes, and review the final diff before publishing.
