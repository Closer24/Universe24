# A tested tensor candidate for finite-time load spreading

A frozen candidate now improves measured occupation distribution on independent
finite ensembles. It runs inside the unchanged Universe24 Engine. It is not
installed as the default law, and is not an Einstein or particle model.

The same 48 retained channels encode occupation and orientation. Within each
face, a four-slot gear rotates for odd occupation and holds its orientation
for even occupation. All occupied slots then hop to a neighbor, followed by a
fixed orientation turn. Holding refers to phase, not stalled edge traffic.
The composite map is F=O S C. A collision uses only channels sharing one face,
so both F and its inverse remain cubic with one-neighbor support.

For quartet (a,b,c,d), C0=d+(a-d)(b+c-2bc); cyclic relabeling supplies the
other outputs. This conditional rule is a fixed integer polynomial, not a
runtime scheduler. Its positive Rule3 embedding is u=6+3F(b-1)+3F_inverse(b-1),
with initial a=1+F_inverse(b-1). The compiled tensor has 768 monomials,
1,536 factor reads/multiplications and 48 divmods per node per update.
That is more symbolic work than the current 672-term law: distribution gains
are not claims of reduced host CPU work. The bounded load is occupied slots.

Tensor fingerprint:
1844f2d368c18f07cad106b9409fcf40e0a44afdcd9020c1dce92cf7424a40d6

## Independent results

Thirty-two admissible gates were searched using fixed training seeds. Selection
used mean integrated concentration relative to free transport plus a penalty
for worse cases. The selected parameters were frozen before fresh validation.

The reported observable is A=sum over updates of sum over nodes Q(node)^2.
Each case compares identical initial occupation and total Q; each law has its
own compatible inverse history. Percentage is the mean of per-case relative
A differences, not CPU time, a diffusion constant or an Einstein residual.

| Fresh cohort | Better / equal / worse than current law | Mean relative A |
| --- | --- | --- |
| L5, T30, sparse, 16 seeds | 12 / 1 / 3 | -2.4405% |
| L5, T30, dense, 16 seeds | 16 / 0 / 0 | -30.3907% |
| L7, T42, sparse, 8 new seeds | 7 / 0 / 1 | -2.5917% |
| L7, T42, dense, 8 new seeds | 8 / 0 / 0 | -30.0193% |

L5 uses seeds31000..31015, a2x2x2 patch and probabilities1/8,1/2. L7 uses
seeds41000..41007 and a3x3x3 patch with the same probabilities. Both cohorts
also pass the declared criteria against matched free transport, separately at
each density. All 96 candidate/current trajectories preserve positive values,
Q and exact rewind. Independent scalar parity and all48 symmetries pass.
Unfavorable cases are retained. This establishes a useful finite-domain
candidate, not universal or monotonic balancing.

A four-run causal control has zero initial interaction in complete a,b,r.
Phase interaction appears at update1 and actual aggregate node-load interaction
at update2. The free control remains zero. Routing changes are substantive.

A complete 343-node,24-update concentrated run preserves Q366 and emits20,452
canonical clicks. Saved forward replay, step inverse, full rewind and click
parity pass. All48 channel histories were separately reconstructed using only
clicks and explicit public initial calibration, then checked against Engine.

## Literature and limits

Reversible interacting cellular automata can exhibit diffusion, ballistic
transport or insulation depending on the state and measured observable:
[Medenjak, Klobas and Prosen (2017)](https://arxiv.org/abs/1705.04636).
That paper concerns conserved charge; it does not validate this occupation
rule. [Hanon and Boon (1997)](https://doi.org/10.1103/PhysRevE.56.6331)
use fluctuation spectra to distinguish a diffusive mode. These motivate
collision/transport construction and mode tests rather than a visual burst
alone. Our separate small Fourier screen shows final mode attenuation but
also rebounds, so it does not establish a diffusion coefficient.

The natural free-packet momentum proxy fails for the optimized gate too:
onsite word1010 changes (2,2,2) to (2,-2,-2), with Q2 conserved. Singleton
recurrence periods scale with box size; no material proper clock is identified.
The tested apparent compact triples separate by half the torus at larger
sizes. No bound matter, dark matter, Maxwell field, common metric or Einstein
field equation follows from calling their retained values numbers.

The candidate package contains the frozen source, exact polynomial proof,
search protocol and every training result, fresh tests, physics counterexamples,
and reproduction scripts. Current production edge-holding diagnostics must
not be applied to the new onsite phase mechanism without migration. In
particular, a symmetric burst's node loads can match free flow while its
channel state differs. The existing installed model and board remain unchanged.
