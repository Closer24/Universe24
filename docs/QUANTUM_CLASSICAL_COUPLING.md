# Quantum and classical coupling: claims, evidence and related work

This page states, as a scientific argument rather than as a contract, what the
repository's quantum and classical parts are, how they are joined, what has
been measured, and what has not. It is written for a reader who will judge the
work against the literature. Contracts remain in the linked owner documents.

## The hypothesis in one paragraph

The framework is called Reality Theory (Universe24). Space is a lattice of Nodes with six Links, one Link per tick, and every
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
| Opt-in [funded emission](CAUSAL_QUANTUM_SOURCES.md#opt-in-funded-envelope-emission): the wave pays for its field from its own stock | totals constant at 3000 with zero sources while the wave is live; 211 units paid into the field over fourteen ticks; after a capture the localized record holds the unspent stock and keeps paying; the only external term is the one retarded emission after the capture |
| An external classical field on one arm with the opt-in [field phase](CAUSAL_QUANTUM_SOURCES.md#opt-in-field-dependent-phase) | coil fields 0, 200, 400, 800 select phase exponents 0, 0, 1, 2 and move the capture probability from 0 to `576/3125` and `9216/15625`; the same field beside the far side of the source moves nothing |
| Full emission raised from 25 to 25000 units per tick at `phi = pi/2` and `phi = pi` | the recorded field departs from `amount x |a_S|^2` by less than one unit on every tick and the mean's relative departure falls as `1/amount`; exact on every tick at multiples of 625 |
| Source weight after a null result on the arm, default rule | the source Node keeps emitting 9 of 25 units: the retarded envelope is not renormalized to the conditional state |
| Same with the opt-in [null notices](CAUSAL_QUANTUM_SOURCES.md#opt-in-causal-null-notices) | the null Node sends `1/(1-p) = 25/9` through its Links; the source emits 25 of 25 from the next tick, and the next gate emits 9 and 16, the exact conditional Born weights; an output null two Links away reaches the source after two ticks |
| [Two nulls crossing on one tick](../examples/quantum/crossing_nulls.md), one excitation over three registers | the stale factors multiply to `390625/177489` where the conditional scale is `25/9`; the later Node by (tick, position) corrects itself from its own null record and the delivered factor, and every Node holds `25/9` two Links after the correction leaves; sequential nulls are exact with no correction |
| [Bonded pairs with a number source outside the world](../examples/bell-chsh/README.md) | a uniform outside stream gives S = 2.7911 and plus rates that move by less than 0.1 with the other end's setting; a biased stream keeps S = 2.7792 and moves Bob's plus rate by 0.6866 with Alice's setting: the only trace an outside source can leave is a signal, and it is measured |
| [Bell test in CHSH form on the phased-ray candidate](../examples/kerengonen-bell/README.md), same settings and combination as the quantum owner's | share rule `S = 826177/589824 = 1.4007`, equal to the local model's prediction `cos(a - b) / 2` averaged over the hidden phase; lottery clicks `386/279 = 1.38` from 8928 single-quantum pairs; plain field exactly 2; quantum owner 14/5 |

The [two-wing Bell test](../examples/quantum/bell_chsh.md) records, on the
same runner under `local-quantum-events-v2`:

| Observation | Result |
| --- | --- |
| Bell pair prepared at x = 12, 13, carried by configured SWAP gates to wings at x = 8 and x = 17, and read at both wings at tick 8 by arriving detector bodies | recorded correlations `3/5, 3/5, 4/5, -4/5` for Alice `Z, X` against Bob `(3Z +/- 4X)/5`; CHSH `14/5 = 2.8`, above the local bound 2, equal to the exact rational prediction |
| The same runs read for signalling | Alice's weights are `[4, 4]` for every Bob setting and Bob's marginal is `1/2` for every Alice setting; no Link signal can cross the nine Links between the wings inside the nine-tick run |
| 100 seeded coincidence trials per setting | estimated CHSH `74/25 = 2.96` from 400 runs, each writing its outcome codes into the classical detector records |
| Same layout with a dephasing channel on one member before separation | correlations `3/5, 3/5, 0, 0` and CHSH `6/5`: a classically correlated source stays inside the local bound |

Earlier experiments established the finite quantum owner itself: the same CHSH
value 14/5 computed directly on a two-register state, exact Born weights with
no random draw for certain outcomes, and phase-sensitive split and recombination
([quantum checks](../examples/quantum/run_physics_checks.py),
[many-contact experiment](../examples/quantum/many_contacts.md)).

## Two candidates for one-particle interference

Since the [Kerengonen phased-ray candidate](SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
was integrated, the repository holds two different mechanisms that produce
interference, and a reader should not confuse them.

- **Phased classical rays.** Whole integer quanta travel on straight rays that
  carry a phase step advanced once per Link; rays meeting at a Node combine by
  a fixed-point cosine of their phase difference, and the coherence gates what
  a screen absorbs. This is a local classical field. It reproduces a two-lamp
  fringe (centre 928 in phase, 0 with a half-turn offset), a Huygens slit, a
  single-quantum lottery and a de Broglie-like dependence of the fringe period
  on the emitter's momentum, all with configured integers.
- **The finite quantum owner.** Gaussian-integer amplitudes over lattice
  registers, unitary gates, Kraus instruments and conditional Born weights.
  It reproduces the two-arm fringe above and, unlike any local phased field,
  exact CHSH value 14/5 for two registers.

The boundary between them is sharp and is a result rather than a choice: a
local phased field cannot exceed the CHSH bound of 2, whatever its phase rule,
because it carries no joint state. Everything one excitation does at a screen
can be described by either candidate; entanglement, Bell violation and
causally delivered conditional collapse belong only to the quantum owner. The
[Bell test on both candidates](../examples/kerengonen-bell/README.md) is the
measurement that separates them: with the same four settings and the same
combination, the phased field gives `S = 1.4007` exactly, one half of the
quantum owner's `14/5` in every correlation, and the plain field gives exactly
2. The classical candidate is at or below the bound and the quantum owner is
above it, on the same lattice and the same runner.

The [ray Bell probe](../examples/bell-chsh/README.md) records local captures
beside a historical global-registry reference on the same comparison scale:

| Candidate | What decides the outcome | S |
| --- | --- | --- |
| Phased rays, share rule ([this experiment](../examples/kerengonen-bell/README.md)) | the coherent share of the source ray against a local reference | 1.40 exact |
| Phased rays, lottery | a local ticket at the coherent rate | 1.48 and 1.38 measured on the two probes, 1.41 predicted |
| Phased rays, threshold | deterministic: the whole ray when the share reaches one half | 2.00 exactly, the bound |
| Bonded rays | the bond registry, one bounded object for the world, answers the pair's joint outcome for both ends from one number per pair | 2.837 +- 0.015 at 4096 fresh pairs per correlation, four replicas; the registry alone 2.8269 +- 0.0010 at a million pairs; the law's expectation 724/256 = 2.828125; the first 1,024-pair run read 2.89 on correlated samples |
| Finite quantum owner | the joint conditional state, queried at each contact | 14/5 exact at 3-4-5 settings |

The first three are local models and stay at or below 2, as Bell's theorem
requires. The last two exceed it, and both do so through one shared object
that no Link carries: the bond registry, which the ray candidate declares as
the one exception to postulate 4, and the quantum owner's joint state. Which
of Bell's assumptions each candidate breaks is measured, not asserted. Write
`lambda` for everything fixed before the settings are chosen (the hidden
phase and the seed, the registry's number, or the prepared joint state), `a`
and `b` for the settings and `A` and `B` for the outcomes. Bell locality is
the factorization `P(A, B | a, b, lambda) = P(A | a, lambda) P(B | b, lambda)`,
which needs parameter independence (at fixed `lambda` no end's outcome
distribution moves with the other end's setting) and outcome independence (at
fixed `lambda` and settings the two outcomes are independent); measurement
independence is `rho(lambda | a, b) = rho(lambda)`. The
[causal probe](../examples/bell-chsh/README.md#which-assumption-of-bells-theorem-each-candidate-breaks)
runs the four setting pairs at every fixed `lambda` and counts how often an
outcome moves when only the other end's setting changes:

| Candidate | `lambda` | Measurement independence | Parameter independence | Outcome independence | S |
| --- | --- | --- | --- | --- | --- |
| Phased rays, lottery | the hidden phase and the detectors' seed | holds by construction: chosen before the settings, never read by them | holds, measured: `A` moves with `b` for 0 of 256 `lambda`, `B` with `a` for 0 of 256 | holds: two independent tickets | 1.48 |
| Phased rays, threshold | the hidden phase | holds by construction | holds, measured: 0 of 256 at either end | holds: deterministic in `lambda` and the local setting | 2 |
| Bonded rays | the registry's number, fixed at birth by the seed and the birth code | holds by construction: the same number serves every setting pair | **broken**, measured: `A` never moves with `b`; `B` moves with `a` for 0.72 of the `lambda` at `b'` (184 of 256; the law says `362/512 = 0.707`) | holds trivially: both outcomes are functions of `lambda` and the settings | 2.83 |
| Finite quantum owner | the prepared joint state | holds | holds: each end's marginal is the state's, whatever the other setting | **broken**: the joint conditional state | 14/5 |

The bonded ray is therefore a deterministic, measurement-independent,
parameter-dependent model: the end that answers second reads the first end's
setting through the registry. That is a nonlocal resource in Bell's sense,
and no wording about messages, energy or inventory makes it local. What the
probe's plus rates measure is no-signalling, which quantum mechanics also
satisfies while violating the inequality; no-signalling is not Bell locality.
The quantum owner breaks outcome independence instead, as quantum mechanics
does, and keeps parameter independence. A reader should therefore not take
the bonded ray as a local explanation of the Bell value; it is the classical
field's counterpart of the quantum owner's joint state, and what the registry
is remains the open question the postulate names
([the contract](SPATIAL_FIELDS.md#bonded-rays-bonded-ray-field-v1)).

## What is claimed

1. A single local update rule per Node, with a complex part and a real part,
   reproduces two-path interference at a detector and, at the same time,
   drives a classical field whose strength carries the interference term.
   With the opt-in field phase the classical field also shifts the fringe,
   so the two parts act on each other through local reads only.
2. Measurement-induced loss of interference follows from an actual local
   instrument on one arm, using only local state and Link-delivered inputs.
   No global wavefunction is read by any Node.
3. Collapse is causal in this model: a localization at one Node changes remote
   source envelopes only after the terminal notice has crossed the Links.
4. All of the above is exact, reproducible and integer; there is no
   floating-point step and no hidden normalization.

## What is not claimed

- **Not a derivation of the classical limit.** The classical field law, the
  mixer, the phase gate and the instrument are configured data. The emission
  side has a measured limit: as the amount grows the integer field becomes
  the continuous law `amount x |psi|^2` within one unit per tick. Nothing
  here shows that large amplitudes or frequent measurements reduce the
  quantum owner's own dynamics to the classical lattice dynamics; the
  [counting probe](../examples/quantum-classical/README.md) shows a dephased
  walk equal to the classical random walk, which is decoherence by
  configuration, not a limit.
- **Born-rule consistency after null results is closed for one excitation
  only.** Under the default rule the retained envelopes are a retarded,
  unnormalized approximation, measured as 9/25 above. The opt-in null notice
  carries the deciding Node's own factor `1/(1-p)` through Links and restores
  the exact conditional weights once it arrives, and two nulls that cross in
  flight are corrected by the later Node from its own record; this is local,
  causal and integer, and it is exact because a single excitation's
  conditional state is renormalized by factors known at the null Nodes. Before
  arrival the remote weights are stale, which is the candidate's prediction
  rather than a bug. Several excitations in one domain are not a numerical gap
  but a structural one: the candidate holds one carrier per domain and one
  amplitude per Node, and a two-carrier joint state has no local envelope. That
  extension would need each Node to carry its row of a two-particle amplitude
  with retarded gate notices, which is not built.
- **Back-action is a phase only.** With the opt-in field phase the classical
  field acts on the wave as an exact local phase read at the gate's schedule
  tick, an Aharonov-Bohm-like coupling. The field is not changed by the wave
  except through emission, no momentum or energy passes between them, and
  the coupling ratio `unit / vacuum` is configured, not derived.
- **Energy closure holds for the emission side only.** With funded emission
  the field is paid from the wave's own conserved stock, totals stay constant
  and the localized winner inherits the remainder; the retarded emission
  after a remote capture is the measured residual. The stock is bookkept by
  the quantum owner, not transported between modes, and the field returns
  nothing to it: absorption of the octant field by the wave is not modeled.
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

1. A local integer rule for several excitations in one domain whose post-null
   envelopes converge to the conditional weights, or a proof that no such rule
   exists. The single-excitation case is closed by the null notice and its
   crossing correction above; the two-carrier case needs a per-Node row of a
   two-particle amplitude and is the largest open gap.
2. The return path: the field now costs the wave what it emits, but nothing
   flows back. An absorption rule for the octant field by the wave, checked by
   the same interference experiment, would close the loop.
3. A classical-limit experiment for the dynamics: the emission side converges
   as measured above, but nothing shows the capture statistics of a coherent
   wave converging to the classical lattice dynamics of a localized record as
   the amplitude scale or the instrument rate grows.
4. A prediction that differs from standard quantum mechanics plus a classical
   field, at a scale where it could be checked.

Until at least one of these exists, the correct description of this work is
an exact, reproducible, local integer hybrid model with a measured
interference and decoherence behavior and a measured, explained departure
from conditional Born weights. The questions the framework raises beyond
these, with what a run could and could not decide about each, are kept on
the [hypotheses page](HYPOTHESES.md), apart from the results.
