# Clock links: exact algebra and the receiver boundary

This investigation starts from main
`4c494c1188f70eb8a677bf59765cc6e8571c6b88`, issue #45 and the one-system
contract in #40. It uses the existing 44-channel charged carrier as an input
port and reserves four additional retained channels for an on-site response
and one response for each positive face direction. It introduces no cosmic
age, copied clock, runtime ticket, optimizer or second metric. The supported
Engine and its fixed divisor remain unchanged.

## Stages and acceptance

1. Define clocks relationally using the existing two real carrier components,
   while keeping proper-time calibration an open physical test.
2. Express their face relations with exact signed polynomial identities.
3. Retain a reversible response to those relations in the same board.
4. Decode canonical events passively and test whether their counts have the
   desired physical meaning. A nonzero signal is not assumed to be a click.
5. Apply the structural/Born/Bell protocols only after this interface is fixed.
   Failure of those physical gates is retained, rather than inferred away
   from exact algebra or replay.

The board as a whole has one autonomous transition map. Calling it a clock
does not add a preferred physical time: an Engine update index is external
bookkeeping, not a retained state or a proper-time observable. A material
oscillator must still be compared with the sole metric at fixed endpoints.

## Signed phase relations

Write the existing carrier at adjacent nodes as

\[
 z_v=x+iy,\qquad z_w=p+iq,\qquad
 I_v=x^2+y^2,\quad I_w=p^2+q^2.
\]

The dot and oriented cross correlations are

\[
 C_{vw}=xp+yq,\qquad S_{vw}=xq-yp.
\]

They satisfy exact identities, including negative components:

\[
 C_{vw}^2+S_{vw}^2=I_vI_w,\qquad
 |z_v+z_w|^2=I_v+I_w+2C_{vw}.
\]

The signs must survive until addition. Counting clocks or taking the absolute
value of each correlation first loses destructive interference. Simultaneous
quarter-turns of both carriers leave these quantities unchanged; conjugation
preserves the dot correlation and reverses the cross correlation. These are
algebraic statements, not probability laws.

Bare comparisons at distinct nodes use a **declared fixed gauge**. Independent
local phase rotations change them: `(1,0),(1,0)` has coherent intensity 4,
whereas `(1,0),(0,1)` has coherent intensity 2 with the same two local
intensities. A gauge-covariant physical comparison needs a compatible parallel
transporter and a proof of its encoding. Existing vector-potential names alone
do not supply that proof. The present four-channel proposal does not add one.

## Four retained responses

The sources at node v are

\[
 F_0=|z_v|^2,\qquad
 F_k=|z_v+z_{v+e_k}|^2,\quad k=x,y,z.
\]

Each expression is a sum of degree-two monomials supported on the target and
at most one face neighbor. The source at each positive link also gives access
to negative-link information at its neighbor; no global reduction enters
evolution. These are node-owned response registers, not extra hidden link
registers.

For each response choose the fixed polynomial input `u=3F`. For every integer
F and every valid remainder r:

\[
 \operatorname{divmod}(6F+r,6)=(F,r),\qquad
 (a,b,r)\longmapsto(b,F-a,r).
\]

Thus all prior receiver information remains in the two-time state. The exact
inverse, once old carrier values are recovered, is

\[
 a=F-b_{\rm next},\qquad b=a_{\rm next},\qquad r=r_{\rm next}.
\]

There are no old-a input dependencies in these four polynomials. The retained
value b is **not** the instantaneous intensity after the first update; the
canonical quotient `ell=after.b+before.a` recovers F. Intensity is therefore a
transition readout, with all its finite-window and provenance requirements.
The extra allocation is exactly four channels, twelve integers per node;
with the existing 44 this totals 48 channels and 144 integers per node.
Neither allocation nor invertibility bounds their bit lengths.

## Why this does not yet produce Born clicks

All four responses preserve r, so every emitted response event is **C0**.
Selecting only C2 would discard this entire receiver signal. More generally,
the canonical event rule requires both nonzero quotient and a changed triple.
An even source F admits the stationary receiver `a=b=F/2`: F is positive but
the receiver emits no canonical event. Arbitrary receiver history also changes
future retained values without making them a probability sampler.

The independent rotating-carrier control makes this failure concrete. Give
the two carrier gears zero input and prepare

\[
 (a_\phi,b_\phi)=(-1,1),\quad
 (a_\chi,b_\chi)=(1,1).
\]

The carrier rotates through four phases under the unchanged Engine. Its local
intensity stays 2 and its uniform face intensity stays 8. Prepare the local
receiver at `(1,1)` and each face receiver at `(4,4)`. Every response stays
stationary and emits **zero** canonical events for all steps. The full board
control is periodic and reversible. This also disproves an inference of
structural growth merely from linked clocks and repeated rotation.

The test control is six channels (two carrier inputs and four receivers) only
to isolate and independently check these equations. It is source-only
validation, not an alternative installed universe or proof about the complete
44-channel geometry. The full 48-channel adapter has its own audits.

## Reproduced checks

Run:

```bash
python -m validation.clock_links.algebra_audit --out runs/clock_links/algebra
```

The initial run reports:

| Check | Result |
| --- | --- |
| Signed dot/cross/coherent identities and common quarter-turn symmetry | 6,561 cases passed |
| Exact receiver inverse for signed F, histories and all six remainders | 5,586 cases passed |
| Full states compared with independent equation oracle | 64 passed |
| Complete rewinds, including 241-bit values | 9 passed |
| Strict face support and maximum degree | 0 violations, degree 2 |
| Observed canonical validation events | 6,842, all C0 |
| Positive intensity with zero receiver events | 8 steps × 27 nodes × 4 receivers |
| Independent local gauge invariance of the bare relation | Failed control retained |

Fresh machine-readable evidence is `runs/clock_links/algebra/algebra.json`,
including source and tensor hashes. The algebra audit does not use production
tensor evaluation to compute expected transitions. Its own scalar equations
calculate every output, including periodic boundary seams and signed arbitrary
receiver histories. It includes 100-bit and 120-bit carrier preparations.

This establishes exact local interference-response algebra and the retained
record interface. Physical clock calibration, a gauge-covariant charged link,
apparatus stress/backreaction, an exclusive Born selection mechanism,
unscreened Bell correlations and growth between bursts remain open.

## A precise obstruction, and what the next experiment must change

The failure is stronger than one bad count ratio. Let O be the complete
receiver-only canonical stream in a fixed one-update observation window and
let p be the proposed normalized intensity at two recipients. Whenever every
receiver source F is even, choose each receiver's allowed preparation as
`a=b=F/2`. Then O is empty, irrespective of those positive intensities. Choose
two different carrier preparations with different p but even F at every
receiver. Both produce exactly the same O. Therefore no deterministic decoder
`d(O, static_protocol)` can equal p for **all** such admissible seeds. The same
holds for a randomized decoder whose random law depends only on O and that
static protocol: its output distribution is identical for both inputs.

The algebra audit constructs two complete rotating controls with intensity
ratios 9:1 and 1:9 whose entire canonical streams are empty for eight updates.
This is a theorem about the explicitly prepared periodic control family. The
48-channel Born audit separately realizes the one-update receiver-only
obstruction on the actual geometry-carrier extension, using source vectors
`(3,1)` and `(1,1)` for ratios 10:2 and 2:10. It does not claim that the actual
44-channel carrier remains in the periodic control family.

Restricting preparation to reset-ready receivers removes this stationary
counterexample but does not establish Born selection: on one update, two
strictly positive intensities produce two receiver events, each counted once.
The quotient weights contain the intensity ratio; binary event support does
not. Any successful next model must define a restricted apparatus preparation
law, produce an exclusive outcome and test it on held-out amplitudes. Reading
the weights and invoking an external weighted sampler would assume the
missing probability law.

## Concrete four-slot successor interface

The next mechanism should **replace** the four read-only intensity receivers,
preserving this experiment as a control. It cannot append another apparatus.
One explicit allocation worth testing is:

| Spare field | Proposed physical role | Retained state |
| --- | --- | --- |
| X | Local reference-oscillator coordinate | `(a,b,r)` |
| Y | Its canonical conjugate quadrature | `(a,b,r)` |
| D | Reversible pointer coordinate | `(a,b,r)` |
| K | Pointer conjugate momentum | `(a,b,r)` |

No globally synchronized reference is required. Each reference is prepared
locally; carrier signals meet it only through the existing face transport.
Its phase is relational and its charge contribution is retained. A local
candidate interaction, stated here as a **continuum Hamiltonian proposal**,
is

\[
 H_{\rm app+int}=\frac{\omega}{2}(X^2+Y^2)+\frac{K^2}{2}
 +\frac{\lambda}{4}D^4-\frac{\mu}{2}D^2
 +gD(\phi X+\chi Y).
\]

The corresponding apparatus ports and reciprocal carrier forces are

\[
\begin{aligned}
 \dot X&=\omega Y+gD\chi,&
 \dot Y&=-\omega X-gD\phi,\\
 \dot D&=K,&
 \dot K&=\mu D-\lambda D^3-g(\phi X+\chi Y),\\
 \Delta\dot\Pi_\phi&=-gDX,&
 \Delta\dot\Pi_\chi&=-gDY.
\end{aligned}
\]

Every displayed right-hand side has integer-coefficient degree at most three
for integer parameters and is on-site. The interaction acts on the **existing
carrier momenta**, so apparatus history can change future carrier structure;
it is not an observer that only watches. The base 44 fields are still counted
once. Simultaneously rotating `(phi,chi)` and `(X,Y)` leaves the interaction
invariant. With the canonical conventions above, its continuum interaction
preserves

\[
 2(\phi\Pi_\chi-\chi\Pi_\phi)-(X^2+Y^2):
\]

the carrier contribution's derivative is
`2gD(chi X-phi Y)`, equal to the derivative of `X²+Y²`.
This is a useful reciprocal charge-accounting identity, **not** a conserved
quantity already proved for a Rule3 encoding.

The proposal is intentionally not installed or simulated as a second model.
The current staggered field encoding and the projective proposal are distinct:
adding these expressions directly to raw b updates would not establish the
claimed physical equations. Its first implementation gate must derive the
compatible complete temporal seed and fixed tensor through the existing
compiler/bundle interface. Metric dependence, apparatus energy/stress and the
interaction contribution must enter the same source accounting, or an explicit
small-backreaction approximation must be tested. The double-well term alone
does not imply a stable pointer; the interaction can be unstable outside its
bounded physical domain. A dissipative reset is forbidden. Any apparent
settling must preserve the information in the complete state.

The staged acceptance protocol is therefore concrete:

1. **Compile and account:** exactly 48 fields; one immutable tensor, exact
   inverse, all carries, strict face support, no source fields overwritten;
   compare the decoded equations and interaction charge/source terms with an
   independent oracle. Reject before physics tests if these fail.
2. **Relational clock and reciprocal response:** in a fixed calibrated flat
   case, verify the reference oscillation and its phase-sensitive interaction.
   Change only retained apparatus history at equal current carrier input and
   require a later carrier difference inside the causal cone; disconnect g
   and require that difference to disappear. Then compare proper time on the
   shared metric without case-specific retuning.
3. **Exclusive retained pointer:** predeclare a readout window and sign or
   basin predicate for D. Count every trial, including no outcome, competing
   outcomes and changes of result. Require one recorded outcome per accepted
   trial and finite-window persistence without resets. Full rewind must still
   recover the losing information. This is not yet wavefunction collapse.
4. **Born measure, not a sampler:** define the complete apparatus preparation
   measure independently of the tested amplitude ratio and detector settings.
   Measure the basins of the exclusive outcomes and their stability under
   evolution. Require their normalized measures to agree with intensity on
   held-out amplitudes, phases and window lengths, with all trials retained.
   If agreement requires tuning the preparation measure for each amplitude,
   the proposed derivation fails.
5. **Structure and Bell separately:** compare structural change with g=0,
   matched histories and periodic controls. For separated Bell settings,
   retain the independent-setting, causal, all-emission protocol. A common
   clock remains a shared variable; it does not itself change that protocol's
   local bound. Any change of assumptions must be explicit before testing.

### Check against the actual pinned compiler: full-source obstruction

The successor has now been checked against the **actual pinned**
`charged_positive` builder and `integer_staggered.compile_staggered` at
`49b896c795203914a939e465d6d39e5b99343259`. Its continuum degree count is
insufficient: retained sign factors and the Einstein source also count.
The compiler encodes
`y_next = y_previous + 2 dt f(y_current)` with one existing sign channel.
A cubic physical monomial survives within degree three only if
`delta_target + sum(delta_inputs) = 1 mod 2`.

The existing `phi`, `chi`, their momenta and the diagonal extrinsic-curvature
fields all have offset zero. There are 43 existing physical fields plus one
sign channel. Adding X,Y,D,K makes **47 physical fields + 1 sign = 48 total**,
with no spare auxiliary or stress register.

All sixteen possible apparatus offset assignments were compiled locally with
`dt=dx=g=omega=mu=1`, `lambda=2`. The even lambda removes any fractional
increment ambiguity: the quartic failure below is a degree rejection.

| Compiler input | Accepted offsets | Tensor result |
| --- | --- | --- |
| Apparatus ports and reciprocal carrier-momentum forces only | 8 of 16; requires `delta_K+delta_D=1` | 48 channels, 604 terms, degree 3, no face-support violation |
| Also add cubic interaction potential `gD(phi X+chi Y)` to the diagonal K source in the existing scalar-potential form | 2 of 16: `(delta_X,delta_Y,delta_D,delta_K)=(0,0,1,0)` or `(1,1,0,1)` | 48 channels, 610 terms, degree 3, no face-support violation |
| Also include pointer potential `lambda D^4/4` in that source | 0 of 16 | Rejected: `Staggered compiler only accepts RHS degree at most3` |

All passing variants read old-a only from the already retained sign channel.
The middle row checks polynomial feasibility, **not** a derivation of the full
apparatus stress tensor. In the repository's actual scalar-potential source
formula, `rho=V`, `S_ab=-V delta_ab` contributes `-V` to every diagonal K
equation. Thus the proposed double-well has a degree-four Einstein source
even though its pointer force is cubic. This cannot be repaired by a sign
offset or by relabeling the potential as an observer. Reference/pointer energy,
momentum, stress and electromagnetic charge/current also need compatible
source and constraint definitions; the unchanged charged builder currently
includes only the original scalar current in Maxwell evolution and Gauss.

Consequently the proposed four-slot double-well is **not ready to build as a
fully sourced shared-metric apparatus**. The immediate next design gate is to
find a bounded, reciprocal pointer model whose complete source compiles, or
prove a degree-lowering retained encoding and recover budget elsewhere. The
obvious extra field `Z=D^2` would raise the count to 49 and additionally needs
an exact two-slice invariant proof; imposing it by reset would violate the
contract. Dropping apparatus stress can only support an explicitly scoped
test-apparatus approximation, with an independently checked error bound; it
cannot pass the requested full-source gate.

Local feasibility evidence is under `runs/clock_links/nextport/`:
`check_compiler.py` enumerates the offsets against the pinned builder and
`compiler_feasibility.json` records all accepts/rejections and compiler-source
hashes. This calculation does not change the frozen 48-channel observer
tensor or the algebra audit.

To reproduce the decisive compilation counts, run this self-contained check
from the source tree at the stated pin (all imports come from that checkout):

```bash
python - <<'PY'
from itertools import product
from experiments.geometry.team48.integer_staggered_audit import candidate
from experiments.geometry.team48.integer_staggered import compile_staggered
base, builder = candidate()
extra = ('app_X', 'app_Y', 'app_D', 'app_K')
names = base.fields + extra
fixed = dict(zip(base.fields, base.phase_offsets))
for mode in ('ports_only', 'cubic_potential', 'quartic_potential'):
    accepted, rejected = [], set()
    def equations(f, derivative):
        out = dict(builder(f, derivative)[0])
        X, Y, D, K = (f[name] for name in extra)
        phi, chi = f['phi'], f['chi']
        out.update(app_X=Y+D*chi, app_Y=-X-D*phi,
                   app_D=K, app_K=D-2*D**3-phi*X-chi*Y)
        out['Pi_phi'] -= D*X
        out['Pi_chi'] -= D*Y
        if mode != 'ports_only':
            potential = D*(phi*X+chi*Y)
            if mode == 'quartic_potential':
                potential += D**4/2
            for axis in range(3):
                out[f'K{axis}{axis}'] -= potential
        return out
    for offsets in product((0, 1), repeat=4):
        try:
            program = compile_staggered(names, equations,
                phase_offsets={**fixed, **dict(zip(extra, offsets))})
            accepted.append(offsets)
            assert program.tensor.G == 48
            assert not program.tensor.support_violations()
        except ValueError as error:
            rejected.add(str(error))
    print(mode, len(accepted), accepted, sorted(rejected))
PY
```

The expected accepted counts are 8, 2 and 0. For the last case every rejection
is the physical RHS degree limit, before sign assignment can repair anything.
The calculation deliberately stops at construction: no unsupported physical
source is passed off as a run or accepted Einstein solution.

The successor therefore supplies reciprocal interface equations and a
specific tested obstruction, not a promoted model. Pointer persistence, Born
basin measures, structural growth and Bell behavior remain unestablished.
