# Eight reviews: algebra, clocks and a route toward compact Einstein dynamics

Research baseline: PR #47, `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
Coordination: [issue #40](https://github.com/Closer24/Universe24/issues/40);
operational clocks: [issue #41](https://github.com/Closer24/Universe24/issues/41).
Eight distinct researchers worked in two waves, followed by independent
coordinator checks. Every specialist inspected original paper sections and
equations. Each report distinguishes those published results from new local
proofs, measured controls and proposed work.

**No complete 48-channel Einstein/matter/apparatus solution is established.**
The useful outcome is an equation-level route, several executable algebraic
ingredients, and a newly exposed formulation obstacle. All new code is
source-only validation; the production Engine, supported interface and
existing decoder authorities are unchanged.

## Recommended route

Derive one local gravity–matter law with compatible discrete identities and
a well-behaved evolution formulation, then compile its updates into the
native integer dynamics with a complete storage and scheduling proof.
Read clocks from the dynamics of that same matter and metric. These are
three linked constructions, with separate acceptance tests.

The immediate formulation candidate restores the full frame and adds
constraint terms to its precompiled equations. The temporal candidate uses
the existing Rule3 integer position/momentum coordinates rather than a
growing projective denominator. Their composition has **not** been compiled
or proved to fit 48. The 45-channel formulation candidate still uses the
old projective time encoding for its mechanical audit.

## Three obstacles that change the next implementation

### 1. The current projective cost is structural

For the actual positive preparation in PR #47,

\[
D_{n+1}=C D_n^d-D_{n-1},\quad C\ge2,\ d\in\{2,3\},\quad D_{-1}=0,\ D_0\ge2,
\]

induction gives `D[n+1] >= D[n]^d` and therefore `D[n] >= D[0]^(d^n)`.
The number of bits grows at least exponentially in the number of completed
updates. This bound is independent of how small the physical matter fields
are. A slower scheduler does not change the bound per completed update.

The protected pairs retain a nonzero Wronskian
`W=p_n q_(n-1)-p_(n-1) q_n`. Their common divisor divides this fixed W.
Consequently unlimited size cannot be cancelled by dividing all current
numerators by a presumed growing common factor. Arbitrary unrecorded
normalization also loses invertibility.

These are statements about the current encoding. They do not rule out a
different reversible representation. See [review 6](06_algebra_obstructions.md).

### 2. A continuum product rule cannot simply be retained on sampled fields

For the finite pointwise algebra, the idempotent site basis gives
`D(e_j)=2 e_j D(e_j)` if ordinary Leibniz holds. Componentwise this forces
every entry of D to zero. A nonzero ordinary derivative cannot satisfy that
rule for all sampled fields.

An exact face identity is available, with `T` the neighbor shift:

\[
\Delta(fg)=(Tf)\Delta g+g\Delta f,\qquad\Delta=T-I.
\]

Its cubic counterpart also uses one face and at most three input factors.
This permits compatible face fluxes. It does not supply a complete discrete
Einstein/Bianchi identity. Changing a diagnostic to use a convenient product
rule would not repair the old dynamics.

The one-channel actual Engine control keeps its prepared periodic sum at125;
the matched same-point chain-rule control changes125 to−775 immediately.
The conserving control still grows from2 to136bits in four updates.
Conservation and bit stability are different requirements.
See [review 2](02_discrete_bianchi.md).

### 3. The present frame formulation has a directional hyperbolicity defect

An exact frozen-coefficient analysis of the actual frame equations around
`B=I, K=G=0` finds zero-eigenvalue Jordan chains. For the reduced20-field
system they occur in the y,z and oblique directions, despite their absence
in the x-direction test. The full24-field equations also have this defect.
The coordinator independently reconstructed the principal matrices directly
from the existing equation builders; a second specialist checked them too.

This is a failure of strong hyperbolicity of that full first-order,
off-constraint continuum formulation at the tested background. It is not a
claim that every constrained solution or every finite run diverges. It means
the present planar tests do not establish robust multidimensional evolution.

The investigated correction changes the equations by terms that vanish on
the continuum constraint surface:

\[
\Delta\dot K_{ab}=\tfrac12(R_{ba}-R_{ab}),\qquad
\Delta\dot G_{abc}=-\tfrac14(\delta_{ac}M_b-\delta_{bc}M_a).
\]

For the full frame, the flat-background corrected symbol has real speeds
`0, +/-|n|, +/-|n|/sqrt(2), +/-|n|/sqrt(8)` and an explicit square-free
annihilating-polynomial check. The same shortcut applied to the reduced
triangular frame fails an oblique-direction control. Full-frame restoration
requires45 projective channels with the stated matter content, before added
apparatus. It does not inherit the triangular protected44 determinant proof.
These corrections are compiled changes of law, not runtime state projection.

See [review 7](07_hyperbolic_stability.md) and its precise domains and tests.
This does not prove nonlinear Einstein constraints, a stable time integrator,
positive metric or efficient long-duration integer evolution.

## Constructive ingredients already checked

| Ingredient | Exact or measured result | Remaining obligation |
| --- | --- | --- |
| Native integer coordinates | `q=b`, `p=6(b-a)+r`; for `u=6q+F(q)`, `p'=p+2F(q)`, `q'=q+floor(p'/6)`. Bijection with no extra channel. | Compile nonseparable gravitational kinetics and arbitrary refinement. The tensor cannot read r as an ordinary factor, and self-a reads are forbidden. |
| Long restricted native controls | One-channel oscillator:600updates,11bits. Prepared 1D wave:1,000updates,21bits, exact transport and rewind. | The wave has compatible two-slice preparation. A zero-mode control grows; a cubic force reaches6,785bits in8updates. No general boundedness follows. |
| Compatible matter work | Six-channel scalar/background control: exact polarized energy change equals face flux plus coefficient work; gradient identity also holds. | Its autonomous coefficients have no reciprocal Einstein response. The polarized energy is not positive on arbitrary two-time data. |
| Reciprocal local force primitive | Two fields can receive forces from the same edge potential, within cubic one-face support. | A reciprocal coefficient is not automatically a metric; positivity, Einstein equations and energy accuracy need separate proofs. |
| Matter clock readout | Existing scalar fields supply `I=phi^2+chi^2` and `S=phi*Pi_phi+chi*Pi_chi`; rational global phase rotation leaves the tested massive44 trajectory's geometry and these invariants unchanged. | Three updates do not establish a period. Moving clocks, redshift and click-only records are untested. Circular motion has constant I; the massive proposal does not apply to the massless baseline. |

The native position/momentum identity is not new physical momentum by
definition. It exposes a computational coordinate system. Its floor is the
existing fixed-six operation, not permission for a new runtime division.
The direct scaling `x=q/S` requires force coefficient
`3 h^2 c_d / S^(d-1)` for a degree-d physical force, which fails generic
integer refinement. Multi-tick arithmetic with retained carries and uncompute
is a research candidate, not an implemented compiler.

## Why the literature is useful without supplying a ready-made import

The individual reports cite original equations, assumptions and caveats.
Representative connections are:

- [Earn–Tremaine](https://ms.mcmaster.ca/earn/pdfs/EarnTrem1992_PhysicaD_ExactHamiltonianMaps.pdf)
  and [JANUS](https://arxiv.org/pdf/1704.07715): reversible lattice integration.
  Their general force/rounding procedures are not automatically allowed by
  the fixed cubic integer tensor.
- [Di Bartolo–Gambini–Pullin](https://arxiv.org/pdf/gr-qc/0404052): exact
  mimetic results in a linearized domain; generic consistent discretization
  uses implicit multipliers and mixed-time constraints.
- [Kur–Glasser](https://arxiv.org/pdf/2202.02486): discrete Palatini/local
  Lorentz symmetry. Its cubical holonomy uses a multi-edge loop and diagonal
  vertex; treating curvature as a free cubic symbol hides storage and degree.
- [Glasser–Qin](https://arxiv.org/pdf/1910.12395): gauge-compatible splits
  preserve a momentum map. A generic split does not acquire that property
  from reversibility alone.
- [Gundlach–Martin-Garcia](https://arxiv.org/pdf/gr-qc/0604035) and
  [Buchman–Bardeen](https://arxiv.org/pdf/gr-qc/0301072): the evolution
  formulation and gauge must be analyzed, including off-constraint modes.
  The present frame equations are not a transcription of WEBB.
- [Brown–Kuchar](https://arxiv.org/pdf/gr-qc/9409001) and the clock papers in
  review5: material reference time has physical fields, energy and domain
  assumptions. A computational phase is not a free physical clock.

## Next construction, with falsifying gates

1. **Choose the corrected geometric variables and evolution law.** Check
   the symbol in every direction, the constraint propagation operator,
   nontrivial backgrounds and source principal terms. Maintain explicit
   negative controls for the triangular reduction and old law.
2. **Derive gravity and matter exchange together.** Require a compatible
   discrete identity `C_d(next)=A(state) C_d(state)`, or a stated controlled
   defect bound, and a map to the independently reconstructed continuum
   constraints. Include metric work and charge/Gauss balance. An invariant
   with an unrelated continuum limit does not pass.
3. **Compile the temporal law without projective exponential cost.** Start
   with a nonlinear reciprocally coupled restricted sector. Count every
   field, intermediate, scheduler and undo register within48. Require integer
   coefficients, degree<=3, one-face support and complete inverse including
   nonzero remainders. A clock multiplied by a cubic term is degree4 unless
   a different factorization is proved.
4. **Predeclare independent physical tests.** Use the same physical endpoint;
   refine space, time and seed quantization separately and jointly. Include
   arbitrary propagation directions, constraint perturbations, metric
   degeneracy, nonlinear blow-up, energy/work and a measured bit-cost budget.
   Keep the other team's preregistered #47 family as independent evidence,
   not as evidence for a different law that has not run.
5. **Close the apparatus allocation.** Prefer validated degrees of freedom
   already present in the matter model. A new three-dimensional real scalar
   in the existing first-order scheme needs five fields;44+5 exceeds48.
   A no-added-channel diagnostic is not an autonomous retained detector.
   Test mass/phase/amplitude controls, moving observers, redshift and a
   decoder that uses only its declared operational records.

No step above may silently add a second metric, numerical runtime solve,
state projection, hidden bank or unrecorded reduction. Restricted successes
remain useful even when they do not meet all general gates.

## Reports and reproduction

| Review | Report |
| --- | --- |
| 1 — Native integer algebra | [Integer algebra](01_integer_algebra.md) |
| 2 — Compatible geometry/Bianchi | [Discrete Bianchi](02_discrete_bianchi.md) |
| 3 — Variational constraints and clocks | [Variational clocks](03_variational_clocks.md) |
| 4 — Matter Noether/work | [Matter conservation](04_matter_noether.md) |
| 5 — Operational clock candidate | [Matter clocks](05_operational_clocks.md) |
| 6 — Mathematical obstructions | [Obstructions and escapes](06_algebra_obstructions.md) |
| 7 — Hyperbolicity and correction | [Evolution formulation](07_hyperbolic_stability.md) |
| 8 — Compiler feasibility/cross-review | [Compiler synthesis](08_compiler_synthesis.md) |

Run the independent checks from the source checkout:

```bash
python -m validation.research_eight.run_all
```

Fresh evidence and logs go to `runs/research_eight/`; the aggregate manifest
records command status and source hashes. Expected physical failures are
assertions that a regression check must retain. A green audit manifest is
not general Einstein, clock, detector or combined48 acceptance.

The coordinator compared all189 imported runtime/team48 source blobs against
the pinned remote research tree: no mismatches or missing files. The patch
adds only research documentation, source-only audits and their CI. Results
from external parallel teams are linked in #40 and are not counted as runs
performed by these eight reviewers.
