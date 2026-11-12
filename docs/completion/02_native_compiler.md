# A native nine-tick quotient and nonlinear lifting compiler

Researcher 2/8, 12 November 2026. Source base: PR #50,
`62202fdccdd9a40d5dbbec104de6f97d9587a999`. Coordination:
[work package](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810783316).
[Executed result](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810974963).
Executable: `validation/completion/native_compiler.py`; evidence:
`runs/completion/native_compiler.json`. No production runtime was changed.

## Achieved scope

There is now an actual fixed-six **nine-microtick nonlinear reciprocal
drift/kick compiler**, with an internal schedule and restored quotient work.
It uses **7 total channels, 21 retained integers/node, 41 monomials, degree
three and strict single-face support**. For the prepared work state, its
exact macro map is

\[
 S^*=S+\lfloor P/18\rfloor,\qquad
 P'=P+2F(S^*),\qquad S'=S^*.
\]

Here `S=a+b`, `P=6a+r` for each data channel. These coordinates are bijective:
`r=P mod 6`, `a=floor(P/6)`, `b=S-a`. They are a mathematical decoder;
the tensor does not read `r`, divide by 18, or call an external force routine.
Every actual update is the unchanged Engine and its fixed-six `divmod`.

This is a **finite k=1 arithmetic result**, not arbitrary-refinement or an
Einstein integrator. The nonlinear test potential is mechanical, and the
joint map can grow rapidly. No same-metric clock, metric positivity,
physical energy or GR constraint closure is inferred.

## Reciprocal nonlinear sector

For each positive x face edge `(i,j)`, choose

\[
 V_{ij}=\lambda(g_i+g_j)(\phi_j-\phi_i)^2.
\]

Both coordinates are dynamical. Its negative gradient supplies

\[
 F_{\phi_i,ij}=2\lambda(g_i+g_j)(\phi_j-\phi_i),\quad
 F_{\phi_j,ij}=-F_{\phi_i,ij},\quad
 F_{g_i,ij}=F_{g_j,ij}=-\lambda(\phi_j-\phi_i)^2.
\]

Forces at a node sum its two incident x edges. They are homogeneous quadratic;
mixed derivatives agree and the phi forces cancel on each edge. This yields
exact conservation of `sum P_phi` in the macro map. It is a uniform-field
shift charge, not established spacetime momentum. The field g is a stiffness
coordinate, not a retained Einstein metric; the cubic potential is not
globally positive.

## Step 1: a three-tick pure nonlinear kick

One internal fast clock c uses `u_c=3-3b_c`, prepared `a_c=b_c=0`. Its
`(a,b)` states are `(0,0),(0,1),(1,0)`, and its arbitrary remainder is fixed.
For a data channel j, use

\[
 u_j=-3b_j+b_cF_j(b).
\]

At clock phase one the baseline rotation has `b_j=-(a_j+b_j)=-S_j`.
Quadratic homogeneity gives `F(-S)=F(S)`. Write

\[
 Q_j=\left\lfloor\frac{2F_j(S)+r_j}{6}\right\rfloor,\quad
 r'_j=2F_j(S)+r_j-6Q_j.
\]

The three successive data pairs are
`(b,-a-b)`, `(-a-b,a+Q)`, `(a+Q,b-Q)`. Therefore
`S'=S`, `P'=P+2F(S)`. This closes the prior audit08 gap that a pure kick
was not one native microtick. No workspace is needed; c restores completely.
Adding `3*l*a_c*b_j` gives an integer drift `S'=S+l*a'` after the kick.
The clock-to-data old-a edges are acyclic.

## Step 2: quotient computation, copy and uncomputation

Use two shared clocks c,z and one workspace w per data channel d. Every
non-clock baseline is `-3b`. The slow clock is

\[
 u_z=-3b_z+b_c(9b_z+3)+3a_cb_z.
\]

At three-tick boundaries its `(a_z,S_z=a_z+b_z)` cycle is
`(0,0) -> (1,1) -> (-1,0) -> (0,0)`. Its full period is nine ticks and
its remainder is unchanged. Workspace and data tensors are

\[
 u_w=-3b_w-b_c(1-2a_z+b_z)(a_d+b_d),\qquad
 u_d=-3b_d-3a_ca_zb_w.
\]

Their expanded monomials have degree at most three. Prepare `a_w=b_w=0`,
`r_w=kappa`, and both clocks' `a,b=0`. At the active middle tick of each
three-tick block, the workspace input is `e*a_d`, with successive
`e=1,0,-1`. The data's `a_d` stays fixed throughout these operations.

1. Compute: the first block puts
   `a_w=floor((2*a_d+kappa)/6)` in w and retains the exact remainder.
2. Copy: only the second block has `S_z=1`; its third tick adds `a_w` to
   data S without changing data a or r.
3. Uncompute: the third block subtracts the same `2*a_d` from `6*a_w+r_w`.
   Workspace returns exactly to `a_w=b_w=0,r_w=kappa`.

For `kappa=0` or 1 the copied value is exactly `floor(a_d/3)`, including
negative a. Since `P=6a+r` and `0<=r<6`, this equals `floor(P/18)`.
All other workspace remainders are also reversible and restored; they give
the explicitly audited biased quotient `floor((2a+kappa)/6)`.

The quotient-only tensor uses six channels for two data coordinates:
two data, two work, two clocks; 24 terms. No old-a dependency points back
from work to data: data reads **work b**, while work reads data a. A valid
old-a order is fast clock, slow clock, data, work.

## Step 3: combine the nonlinear force into the same immutable tensor

Simply gating a quadratic force with two clock factors would be quartic.
Instead add one retained pulse gear t. It has

\[
 u_t=3H,\quad
 H=2a_ca_z-2a_cb_z+a_c-b_cb_z+b_z.
\]

On the prepared nine-phase clock orbit, H is one at phases 6 and 8 and zero
elsewhere. With `a_t=b_t=0`, the fixed-six recurrence is
`b_t(next)=H-a_t`, so `b_t` is one **only at phase 7** and zero at all
other phases. All its remainder classes remain fixed. Thus t restores after
nine ticks. This materializes the gate with a quadratic clock polynomial.

Add `b_t*F_j(b)` to each data tensor. The kick occurs at phase 7, the middle
tick of the **uncompute** block. Workspace reads the complete old data
snapshot before that kick changes data a. Thus its inverse input equals its
original compute input. The copy has already changed S, so the kick sees
the drifted position. All work and scheduler state restore, leaving exactly
the macro map stated above. This is an actual single tensor, not a Python
composition of changing laws or an externally advanced schedule.

The complete macro inverse recovers `P=P'-2F(S')`, then
`S=S'-floor(P/18)`. All original a,b,r follow from the bijection. The
unchanged Engine also inverts every individual microtick on the complete
legal state space; the simple macro formula requires the declared clock and
workspace preparation. The tensor has no self-a read and remains strict-face
local even though the force spans an edge.

## Executed evidence

Run from repository root:

```bash
python -m validation.completion.native_compiler
```

The report records source and tensor SHA256 fingerprints.

| Audit | Actual checks |
|---|---|
| Three-tick potential/integer-drift tensor | 20 signed coupling/drift choices, 216 nodes containing every triple of remainder classes, six periods each; independent macro oracle, every inverse, full rewind and scheduler restoration |
| Nine-tick quotient-only tensor | Six workspace remainder preparations; signed data a from -108 to 108; all data/clock remainders; twelve periods / 108 ticks; complete work/clock restoration |
| Single-tensor nonlinear compiler | Couplings -2,-1,0,1,2, each with prepared-zero and mixed-six work remainders; 216 nodes, six periods / 54 ticks; exact independent force/quotient oracle, every inverse and full rewind |
| Algebra/validator controls | Reciprocal potential derivative, phi shift-charge balance; clock times cubic force rejected as degree four |

Rapid nonlinear growth is retained as a failure control, not hidden by the
inverse successes. For lambda=1 and mixed work remainders, the joint tensor's
boundary maximum complete-state bits are `3,6,10,18,33,64,127`. For lambda=2
they are `3,7,13,24,46,90,179`. No boundedness claim is made for this cubic
mechanical potential or for the nine-tick nonlinear integrator.

The initial audit attempts exposed two **validation implementation** errors:
NumPy `divmod` does not support these object arrays, and in-place addition
into an int64 copy rejected object results. The passive oracle now explicitly
uses Python-integer object arrays and separate `//` and `%`. These were fixed
without changing Engine. A repository AST guard also required renaming a
local proof-loop variable `Q`; the mathematical notation and guard were not
changed. The final command completes successfully with all negative controls.
The attempted pytest invocation was unavailable because pytest is not
installed. The repository's native command
`python -m unittest universe24.tests.test_fixed_divisor_contract -v` passed
both tests after the final source changes.

## What refinement is proved, and what is not

For the **potential-only** subflow, take position resolution `A=3^k`,
physical x=S/A, physical p=P/(2A^3), and h=1/A. Quadratic homogeneity gives
exactly `p'=p+h F(x)`, with x fixed. At T=1, N=A periods, the implementation
measured:

| A | Actual microticks | Maximum retained bits | Exact potential-flow error |
|---|---:|---:|---:|
| 3 | 9 | 7 | 0 |
| 9 | 27 | 12 | 0 |
| 27 | 81 | 17 | 0 |
| 81 | 243 | 22 | 0 |
| 243 | 729 | 26 | 0 |

The tensor is identical across these tests. No dynamic denominator is stored.
Because S is fixed and P grows linearly in period count, the arithmetic bit
bound is logarithmic in count for fixed initial S; in this fixed-T refinement
it is O(log A). This proves a refinable nonlinear **subflow**, not the full
coupled dynamics: changing the clock's time label alone is insufficient.

For the full quadratic-force/integer-drift ansatz with x=S/A and p=P/R,
matching the leading physical equations forces
`h=2*k*A^2/R` and `h=l*R/(6A)`, hence
`h^2=l*k*A/3`, for nonzero integer force multiplier k and drift l. Thus
positive h cannot tend to zero while A tends to infinity in that ansatz.
For the new quotient drift `floor(P/18)`, the relation improves only to
`h^2=k*A/9`. The finite k=1 quotient is useful but does not remove the
arbitrary-refinement obstruction. This is a theorem about the stated
representation, not all multi-tick compilers or long-wave sectors.

A concrete next primitive is a deeper prepared quotient
`floor(a/3^m)`, computed serially, copied, then uncomputed in reverse. This
would make drift `floor(P/(6*3^m))`. It must preserve all intermediate
remainders and include an internally verified longer pulse schedule. Neither
arbitrary m nor a constant-workspace implementation is supplied here. A
straight chain uses at least m work channels per data coordinate; its clock
allocation is additional. No claim that an arbitrary m fits 48 is justified.

The implemented generic two-clock quotient plus materialized nonlinear gate
uses `2*n+3` channels for n data coordinates. It fits at most 22 such
coordinates within 48. Applying it directly to all 44 first-order data
fields of corrected45 would require 91 channels, before any other apparatus.
A reduction to canonical pairs would need an explicit transformation and
shared action; it cannot be assumed from two histories. This seven-channel
primitive is therefore **not appended to or substituted into corrected45**.

## Connection to the time-stability result and primary literature

The [independent temporal analysis](https://github.com/Closer24/Universe24/issues/40#issuecomment-6810874307)
proves/executed stable native linear transport refinement and identifies an
exact projective Fourier instability. That linear law and this nonlinear
compiler are different tensors. The next connection must establish one
shared schedule, one matter/geometry action, the complete channel budget and
uniform error/stability bounds before their results can be combined.

Original texts read this round:

* Calderbank, Daubechies, Sweldens and Yeo,
  [Wavelet Transforms That Map Integers to Integers](https://cm-bell-labs.github.io/who/wim/papers/integer.pdf),
  sections 3.3–3.4, especially the forward/inverse lifting formulas on
  pp.23–25. They motivate triangular recomputation and reversible scaling.
  Their arbitrary filter rounding is not an Engine operation; the nine-tick
  construction above provides its own specific allowed quotient.
* Rein and Tamayo, [JANUS](https://arxiv.org/pdf/1704.07715), sections
  2.1–2.2, equations 3–5. Recomputing the same rounded force enables
  bitwise inversion of split updates. Its floating force evaluation and
  external timestep multiplication cannot be inserted here as callbacks.

The old research reports 01 and 08 were read before construction. The
three/nine-tick identities, phase materialization and tests above are our
explicit derivations, not conclusions attributed to those papers. Full
nonlinear Einstein refinement and shared operational clocks remain blocked.
