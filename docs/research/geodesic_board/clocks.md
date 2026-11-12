# Clock port on the board's massive45 law

The board now has a clock diagnostic on its own explicitly massive corrected
full-frame tensor. This closes the different-tensor handoff in issue #40; it
does not establish an operational clock.

## Exact identity and actual execution

`validation/geodesic_board/clock_audit.py` uses the shared `run.build_program`
and `run.prepare_seed`, with mass squared 1, time step 1/32, space step 1/4,
45 channels and 889 terms. The default tensor fingerprint is
`fbbf8f9b4128563e786ff0b57069fe18320698451c0ac9acb0c947c568cfc617`.
The source starts at B=identity, K=-identity, phi=2, dust amplitude=1,
with all six carry classes, and is evolved through the existing Engine.

Four actual updates on 27 nodes pass an independent literal integer oracle,
complete inverse, and a nontrivial integer quarter-turn of the complex field.
Both complete states are related by this rotation at every saved slice;
geometry, stress sources, and the local invariants below agree. The largest
retained integer is 186 bits. This is global phase equivariance, not a proof
of lattice local-gauge closure.

For each saved node, define

\[
I=\phi^2+\chi^2,\quad S=\phi\Pi_\phi+\chi\Pi_\chi,\quad
P^2=\Pi_\phi^2+\Pi_\chi^2,\quad Q=\phi\Pi_\chi-\chi\Pi_\phi.
\]

The exact algebraic check is `I P²-S²=Q²`. In the homogeneous continuum
subsystem, the actual equation convention gives

\[
\dot I=2S,\qquad \dot S=P^2+\mathrm{tr}(K)S-m^2I,
\qquad \dot Q=\mathrm{tr}(K)Q.
\]

For radial data Q=0 and positive oscillator energy, a local phase diagnostic is

\[
\theta=\tfrac12\arg\big((m^2I-P^2)-2imS\big),\qquad
\dot\theta=m-\frac{\mathrm{tr}(K)mS}{m^2I+P^2}.
\]

The source tests the derivative identity symbolically, including the general
Q-dependent denominator before restricting to radial data. Expansion affects
this phase rate. On the actual short board trajectory, the principal phase
is approximately 0, 0.0312398, 0.0596037, 0.0854476, 0.109078 at times
0, 1/32, 1/16, 3/32, 1/8. In this synchronous homogeneous fixture, normal
proper time equals coordinate time; theta/m does not equal that time.
No full period or retained phase-winding counter exists in this run.

The flat circular control has constant I despite nonzero internal rotation.
Zero source has undefined oscillator phase, and a massless field has no
mass-defined period. These controls prevent promoting intensity peaks to a
universal proper-time clock. A general charged field is not covered by the
radial phase formula.

## Three remaining channels: useful proposal and obstruction

The live selection work in [issue #45](https://github.com/Closer24/Universe24/issues/45#issuecomment-6810740360)
proposes a homogeneous neutral pointer q,p and one record channel: 45+2+1=48.
Its interaction energy is `g q I`, and its harmonic energy is `omega² q²/2`.
This is cubic in the source variables and therefore avoids the earlier
quartic double-well source obstruction. It is not attached to this board law.

The local audit independently checks the next obstacle. Including the scalar
mass energy, minimization over q gives

\[
V_{\min}(I)=\tfrac12m^2I-\frac{g^2I^2}{2\omega^2}.
\]

For nonzero g and positive omega squared, this is unbounded below as I grows.
A finite-amplitude validity domain and escape controls are necessary. q,p
alone also lack the three gradients of a transported real scalar; adding
those to corrected45 requires 50 channels before a record. Thus a homogeneous
oscillator source is not yet general apparatus with spatial momentum balance.
The companion audit records these as open constraints, not rejection of all
possible pointer designs.

## Reproduction and handoff

```bash
python -m validation.geodesic_board.run --out runs/clock-shared-run
python -m validation.geodesic_board.clock_audit \
  --board runs/clock-shared-run/board_data.json \
  --out runs/clock-shared-run/clock-audit.json
```

The board audit rejects a different tensor fingerprint rather than borrowing
clock evidence across laws. All phases are passive diagnostics; they add zero
retained channels and never feed the Engine. Operational ticks, moving-clock
calibration, redshift and click-only proper time remain unimplemented.

## Primary sources and their limited role

- Michael S. Turner, [Coherent scalar-field oscillations in an expanding
  universe](https://doi.org/10.1103/PhysRevD.28.1243), Phys. Rev. D 28, 1243
  (1983). The paper analyzes classical homogeneous scalar oscillations and
  their expansion-dependent energy scaling. It motivates checking the
  expansion correction; it does not validate this integer discretization.
- Alexander R. H. Smith and Mehdi Ahmadi, [Quantum clocks observe classical
  and quantum time dilation](https://arxiv.org/abs/1904.12390), Nature
  Communications 11, 5360 (2020), [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7584645/).
  Their operational quantum clock has internal degrees, a Hamiltonian and a
  covariant time observable. Those quantum ingredients and conditional
  probabilities are assumptions of their framework, not consequences of
  Universe24's passive I/S diagnostic.
