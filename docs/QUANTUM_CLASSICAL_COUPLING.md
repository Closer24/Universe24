# Quantum and classical coupling: claims, evidence and related work

This page states, as a scientific argument rather than as a contract, what the
repository's quantum and classical parts are, how they are joined, what has
been measured, and what has not. It is written for a reader who will judge the
work against the literature. Contracts remain in the linked owner documents.

## The hypothesis in one paragraph

Space is a lattice of Nodes with six Links, one Link per tick, and every
evolving quantity is a bounded integer. Ordinary matter and fields are
configured disturbances that move and interact by local rules. A quantum
excitation is not a second world: it is a finite joint state over at most
thirty lattice registers, evolved by explicit number-preserving Gaussian-integer
unitaries between neighboring registers and read by explicit local Kraus
instruments. The join is the [causal source candidate](CAUSAL_QUANTUM_SOURCES.md):
each participating Node retains a bounded complex envelope of the wave, that
envelope evolves only from frozen local and Link-delivered neighbor inputs, and
the Node emits the ordinary classical field at the configured full strength
times the local squared magnitude of that envelope. A local contact with a held
instrument can localize the excitation into an ordinary record; the resulting
cancellation of the other envelopes travels through Links with delay. The
exact conditional quantum state and its Born weights are kept by a separate
owner that is queried only at actual local contacts.

## What has been measured

The [two-arm interference experiment](../examples/quantum/causal_interference.md)
records, with exact integers on the canonical runner:

| Observation | Result |
| --- | --- |
| Capture weights at the output detector after a 3:4 split, a phase `phi` and inverse recombination | `[625, 0]`, `[337, 288]`, `[49, 576]`, `[337, 288]` for `phi = 0, pi/2, pi, 3pi/2`, equal to the exact rational prediction `288(1 - cos phi)/625` |
| Same experiment with a balanced Hadamard splitter (vacuum coefficient `1 + i`, scale 2) | capture probabilities 0, 1/2, 1, 1/2: full visibility inside the integer contract |
| Classical field emitted at the source Node after recombination | integer floor of `25 (337 + 288 cos phi)/625` with carried remainder: 25, 13.5, 2, 13.5 per tick |
| Same experiment with a held detector on one arm | the arm decision is `[9, 16]` for every `phi`; the output detector never receives a nonzero capture weight |
| Cancellation after a capture two Links away | the source Node emits once more and then stops |
| Source weight after a null result on the arm | the source Node keeps emitting 9 of 25 units: the retarded envelope is not renormalized to the conditional state |

Earlier experiments established the finite quantum owner itself: exact CHSH
value 14/5 for a two-register state, exact Born weights with no random draw for
certain outcomes, and phase-sensitive split and recombination
([quantum checks](../examples/quantum/run_physics_checks.py),
[many-contact experiment](../examples/quantum/many_contacts.md)).

## What is claimed

1. A single local update rule per Node, with a complex part and a real part,
   reproduces two-path interference at a detector and, at the same time,
   drives a classical field whose strength carries the interference term.
2. Measurement-induced loss of interference follows from an actual local
   instrument on one arm, using only local state and Link-delivered inputs.
   No global wavefunction is read by any Node.
3. Collapse is causal in this model: a localization at one Node changes remote
   source envelopes only after the terminal notice has crossed the Links.
4. All of the above is exact, reproducible and integer; there is no
   floating-point step and no hidden normalization.

## What is not claimed

- **Not a derivation of the classical limit.** The classical field law, the
  mixer, the phase gate and the instrument are configured data. Nothing here
  shows that large amplitudes or frequent measurements reduce the quantum
  owner to the classical lattice dynamics.
- **Not Born-rule consistency after null results.** After a null outcome the
  retained envelopes are a retarded, unnormalized approximation. The measured
  9/25 factor above is the size of this departure in the simplest case. A
  globally conditioned source would require nonlocal renormalization, which
  the model refuses by design; the gap is therefore a physical prediction of
  the candidate, not an implementation bug, and it is open whether any local
  rule can close it.
- **Not back-action.** The classical field does not act on the amplitudes.
  The coupling is one directional.
- **Not energy closure.** Field emission draws from finite configured
  allowances; there is no field-plus-matter energy that is conserved.
- **Not a continuum or asymptotic result.** Every table is a finite lattice at
  a finite number of ticks.
- **Not quantum electrodynamics, gravity, spin, statistics or many-body
  dynamics.** One conserved inventory per domain, at most thirty registers.

## Related work and where this sits

The model combines ideas from several existing lines. A reader should know
them; the novelty claimed here is the specific combination and its exact
integer realization, not any of the parts.

- **Discrete and cellular-automaton physics.** Fredkin and Toffoli,
  *Conservative logic*, Int. J. Theor. Phys. 21, 219 (1982), and
  't Hooft, *The Cellular Automaton Interpretation of Quantum Mechanics*
  (Springer, 2016), argue that deterministic local integer dynamics can
  underlie quantum behavior. This repository shares the lattice, locality and
  integer commitments, but does not claim that its quantum owner emerges from
  the classical rule: it is a separate finite state coupled to it.
- **Lattice-gas and lattice Boltzmann methods.** Frisch, Hasslacher and
  Pomeau, Phys. Rev. Lett. 56, 1505 (1986); Succi, *The Lattice Boltzmann
  Equation* (Oxford, 2001). These derive continuum equations from discrete
  local collisions on a lattice. The repository's six-Link transport and
  outward field splitting are of this family. The [inverse-square probe](../examples/inverse-square/README.md)
  and the [local Maxwell experiment](../examples/maxwell/README.md) are its
  continuum-limit tests, with recorded partial results and blockers.
- **Quantum cellular automata and quantum lattice gases.** Bialynicki-Birula,
  Phys. Rev. D 49, 6920 (1994); Meyer, J. Stat. Phys. 85, 551 (1996);
  Arrighi, Natural Computing 18, 885 (2019). These evolve amplitudes by local
  unitaries on a lattice, which is what the repository's gate schedule does,
  with the restriction to Gaussian-integer matrices with a common scale.
- **Semiclassical and hybrid quantum-classical dynamics.** Coupling a
  classical field to `|psi|^2` is the mean-field or Møller-Rosenfeld idea
  (Rosenfeld, Nucl. Phys. 40, 353 (1963); Diósi, Phys. Lett. A 105, 199
  (1984)). Recent hybrid theories with stochastic classical sectors include
  Oppenheim, Phys. Rev. X 13, 041040 (2023). The repository's source rule is a
  retarded, local, integer version of mean-field coupling with no back-action.
  Its 9/25 departure after a null result is the price of refusing nonlocal
  renormalization; the hybrid literature pays that price differently.
- **Collapse and decoherence.** Ghirardi, Rimini and Weber, Phys. Rev. D 34,
  470 (1986); Bassi et al., Rev. Mod. Phys. 85, 471 (2013); Zurek, Rev. Mod.
  Phys. 75, 715 (2003). The repository does not add a spontaneous collapse
  term. Localization occurs only at configured local instruments, and its
  effect on remote sources is causal. The which-path result above is standard
  decoherence by a real detector, realized with only local inputs.
- **Histories and causal structure.** Griffiths, J. Stat. Phys. 36, 219
  (1984); Bombelli, Lee, Meyer and Sorkin, Phys. Rev. Lett. 59, 521 (1987).
  The immutable event spacetime with dependency edges, used for both ordinary
  and quantum events, is closer to these than to a state-vector picture.

## What would make this a physics result

1. A rule, local and integer, under which the post-null envelope converges to
   the conditional weight, or a proof that no such rule exists. Either closes
   the largest open gap.
2. Field back-action on amplitudes with a stated conserved quantity, tested by
   the same interference experiment.
3. A classical-limit experiment: increasing amplitude scale or instrument rate
   and measuring convergence of capture statistics to the classical lattice
   dynamics of a localized record.
4. A prediction that differs from standard quantum mechanics plus a classical
   field, at a scale where it could be checked.

Until at least one of these exists, the correct description of this work is
an exact, reproducible, local integer hybrid model with a measured
interference and decoherence behavior and a measured, explained departure
from conditional Born weights.
