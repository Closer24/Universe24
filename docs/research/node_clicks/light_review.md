# Independent review of the phase-gated light tensor

The phase-gated tensor is mechanically admissible and its documented
homogeneous move/hold theorem is correct. Its current dynamics do not provide
a shared Einstein metric or a common source law for light, matter, dark
matter and gravitational waves. These are interpretation blockers, not a
reason to discard the scoped research experiment or its negative controls.

The independent checks used source hashes captured before and after execution;
the reviewed head was `43b63f2f00525de580c92f20a05b83f74c99cc00`. The phase
tensor fingerprint was
`0d9a9a329b36cd43d388364d041fa6e32b6f963ed12e38698218883a6bb15116`.
Evidence and executable: `runs/light-review-new/results.json` and
`runs/light-review-new/review.py`. No production source was edited by this
review. Its readout checks do not feed the Engine.

## Passed mathematical checks

The law has exactly 48 node channels, 384 integer monomials, degree three,
one-face support and the required 2O covariance. All coefficients are multiples
of three, so every retained remainder is unchanged and the Rule3 quotient
equals `u/3` for every allowed remainder. No precision scaling is needed for
this particular law.

For `bar(g)=-g`, let `p=b_g+b_bar(g)` and `q=b_g-b_bar(g)`. Independent
elimination of the exact update gives, with `+/-` denoting neighbors along
`n_g`:

\[
p_{t+1}=-p_{t-1}+p_t+p_{t,+}
             +q_t^2(p_{t,-}-p_{t,+}),
\]

\[
q_{t+1}=-q_{t-1}-q_t+q_{t,+}
             +q_t^2(q_{t,-}-q_{t,+}).
\]

The second identity was checked against the Engine on arbitrary positive
integer histories with independently varied remainders. Exact inversion and
remainder retention passed. On the prepared homogeneous contrast sector,
`q_next=-q_old`, producing the stated four-cycle. With the matching optical
predecessor, the pair sum translates one face on odd updates and holds on
even updates. The closed-form positive-integer solution in the resonance
report is consistent with the update and its parity requirements.

Three independent amplitude interventions, `0`, `1` and `17`, were run for
32 updates each. Retained integers stayed positive, each preparation's
plane-field energy stayed constant, and all three complete contrast histories
were identical. These checks support the restricted theorem; they do not
expand its physical interpretation.

## Blocker: light cannot source this clock/geometry variable

The `q` equation above contains no `p`, exactly, on the entire integer state
space. This is stronger than a missing backreaction test: with the current
law, changing optical pair sums cannot affect the future contrast trajectory.
An intervention independently changed the pair sums in both histories while
holding both contrast histories fixed; the next contrast remained exactly
the same, while the full next state changed.

Because the native `E,B` readout sees pair sums and cancels central contrasts,
the candidate can influence optical transport in one direction without an
optical source term in the candidate clock dynamics. Identifying `q` or
`q^2` as physical geometry therefore does not produce a sourced Einstein
system. The separately tested reciprocal-force tensor does have an explicit
source interaction but retains its reported natural-domain failures; its
successes cannot be substituted into this tensor's proof.

Required repair: derive a single retained source/geometry coupling and an
independent source account, then prove or test its domain and stability. A
renaming of the passive contrast readout cannot supply the missing term.

## Blocker: the coupling separates into independent axial subsystems

The undirected channel-dependency graph of every nonzero monomial has exactly
24 connected components, each the two labels `{g,bar(g)}`. Both labels have
the same propagation direction. Their spatial factors lie only at the target
or its two neighbors on that axis. Thus the lattice further separates into
independent one-dimensional lines for each central pair.

There are no tensor terms coupling different propagation frames or different
face groups. A profile cannot transfer between differently directed channel
groups under this law. A six-face node view can accurately expose the storage
and adjacency, but it does not create such interactions. In particular, that
view alone supplies neither cross-direction scattering nor a demonstrated
deflection of light by a sourced metric.

The eight labels grouped under one face are propagation-frame labels, not an
assertion that each reads only that face. An amplitude labeled `+x` reads both
`+x` and `-x` neighbors. Opposite-face groups are distinct independent
components; their endpoint values need not define one shared edge delay.

Required repair: introduce justified cross-frame couplings under the existing
48-channel/2O/locality contract, and independently verify a shared endpoint
quantity and directional response. Merely adding topology wrappers changes
neither the tensor dependency graph nor these physical limits.

## Blocker: prepared transport speed is not yet a universal physical speed

On the selected light sector the average coordinate displacement is one face
per two updates. That is a result about this field preparation and the engine
step index. It does not establish a proper-time clock or identify the causal
speed of every retained disturbance.

An exact countercheck starts with the homogeneous zero-light preparation,
advances once to the optical hold phase, and perturbs one central pair at one
node by adding `1` to one `b` value and subtracting `1` from its partner. This
preserves the pair sum while adding `2` to the contrast. On the very next
update, the contrast disturbance reaches a neighboring node even though that
update is an optical hold. In the checked lattice it travels from node `21`
to node `5`, with contrast response `2`. All retained integers remain
positive, and both electromagnetic readouts remain unchanged.

This is not a claim of experimentally superluminal behavior: no operational
physical metric or material clock has been established. It is a counterexample
to equating the prepared half-speed with the universal causal speed of the
underlying tensor. Coarse-graining two engine updates into one optical step
also cannot be declared a physical clock without checking the other retained
sectors and the observer's records.

## Observer and optical-reference cautions

The resonance observer computes `E,B`, energy and Fourier norms from complete
states. These are legitimate validation diagnostics, but they are not what a
click-only observer directly measures. The canonical click includes a
quotient, not just a binary detection event. Central contrasts that cancel
from `E,B` are not thereby proven invisible in the arithmetic click stream,
and invisible electromagnetic readout is not evidence for dark matter.

The reported squared Fourier-mode growth factor `65` is a valid failure of
the declared pure time-reparameterized translation target at the registered
finite resolution. It is not a general no-go theorem for Maxwell fields in
time-dependent media or curved spacetime, and not a refinement study. The
resonance documentation already preserves this distinction.

The finite audit's preparation restrictions and failed spatial-clock controls
must remain visible. Independent testing and the explicit formulas support
publishing the source as a scoped research result. They do not support
promoting this law to a default model claimed to show matter, dark matter,
gravitational waves or Einstein event spacetime.
