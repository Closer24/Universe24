# Independent review: what conservation fixes and what it leaves open

The reviewed object is **one eight-channel native Bianchi-I law**, with a
homogeneous massless scalar and positive comoving dust. Two retained constants
are the diagonal eigenvalues of the mixed shear tensor; their negative sum is
the third eigenvalue. They are not the spatial momentum covector of a probe.
The unchanged Engine advances all 24 integers per node, including old histories
and the six possible carry values. The other reports share this exact tensor,
and share one complete seed at each declared resolution.

The continuum solution family is established physics. The contribution here is
its complete native integer embedding and its independently verified execution.
No uniqueness theorem, spatially general Einstein law, massive scalar extension
or operational detector follows from this result.

## Independent source and recurrence checks

This reviewer implements its own scalar Rule3 oracle and physical projection;
it does not call the common force or scalar oracle. Write

\[
W=4N^2V,\qquad J=b_W-a_W+3D,\qquad U=J/(4N).
\]

The complete native map gives

\[
W_+=W+J+3D,\qquad J_+=J+6D.
\]

The frozen source/shear histories and all carries remain retained. Consequently

\[
J^2-12DW-24N^2\left(P^2+\sum_i S_i^2\right)
\]

is exactly invariant. Dividing by the static constant \(16N^2\) yields

\[
Q=U^2-3DV-\frac32\left(P^2+\sum_iS_i^2\right).
\]

The independent code proves the physical finite step

\[
V_+=V+hU+\frac34Dh^2,\quad U_+=U+\frac32Dh,\quad h=1/N,
\]

and compares all retained registers against the actual Engine. Three seeds
include signed scalar/shear values, a shifted time origin and a second
nonzero anisotropy. Every microstep inverse and complete rewind is checked.

The source test is separate from the invariant test. Using
\(H_i=(U/3+S_i)/V\), the reviewer independently obtains

\[
G_{00}-\rho=\frac{Q}{3V^2},\qquad
G_{ii}/a_i^2-p=\frac{Q}{3V^2},
\]

with \(\rho=P^2/(2V^2)+D/V\) and \(p=P^2/(2V^2)\), and checks scalar,
dust and shear evolution. The metric researcher separately derives all
curvature components from the generic diagonal metric. These are algebraic
identities of the declared continuum interpolation, whose sample values are
exactly supplied by the native map; numerical logs and roots are passive
diagnostic evaluations, not exact rational retained metric components.

## Conservation alone does not select the law or its clock

For every constant \(\alpha\), the family

\[
V_+=V+\alpha hU+\frac34D(\alpha h)^2,\qquad
U_+=U+\frac32D\alpha h
\]

preserves \(Q,D,P,S_i\). Yet its derivative is \(\alpha\) times the prescribed
vector field. At \(\alpha=0\), all these charges are conserved while geometry
is frozen despite positive matter density. At \(\alpha\ne1\), a change of
time parameter requires a corresponding lapse change. With unit lapse and
proper interval \(h\) fixed, the source equations select \(\alpha=1\).
This counterexample concerns the physical flow family; it does not assert
that every member already has the same integer embedding.

An additional negative control actually executes the shared Engine and tensor:
only the retained time-marker slope is changed from one to two. The source
and constraint remain correct and the entire state rewinds, but the claimed
marker interval is twice the dust proper interval. The physical preparation
validator rejects it. At three steps the source time is \(1/8\), while the
incorrect marker says \(1/4\). Conservation and reversibility do not eliminate
the need to calibrate a physical clock.

The clock lane derives a more useful positive relation from the same state:
\(\tau_{\rm source}=(J-J_{\rm ref})/(6DN)\). This reads retained source history
and the reference velocity, without reading the tick marker or an external
step number. It is an exact elapsed comoving dust time in the chosen chart.
It does not create a transported detector or autonomous material record.

## A precise positive uniqueness statement

Within this reduced homogeneous sector, conservation does fix the discrete
update once the proper-time kinematics and expanding branch are declared.
Assume D, P and S remain fixed, \(Q_+=Q\), and require

\[
V_+-V=\frac h2(U_++U),\qquad U_++U>0.
\]

The exact factorization is

\[
0=Q_+-Q=(U_++U)\left(U_+-U-\frac32Dh\right).
\]

The positive factor excludes the spurious branch \(U_+=-U\), leaving uniquely

\[
U_+=U+\frac32Dh,\qquad V_+=V+hU+\frac34Dh^2.
\]

This is exactly the implemented native map. Thus conserved source/shear data,
the quadratic constraint and a specified proper-time midpoint relation reduce
the update to a unique explicit affine-acceleration rule. The midpoint relation,
clock normalization and positive branch are additional assumptions; conservation
alone does not derive them. This is a uniqueness statement **inside this map
class**, not uniqueness of Einstein gravity or of a general Universe24 tensor.

## Computational cost and domain

The exact iterates satisfy

\[
W_n=W_0+nJ_0+3Dn^2,\qquad J_n=J_0+6Dn.
\]

For the declared expanding preparation, all retained registers are bounded by
\(C(n+1)^2\) for an explicit seed-dependent integer \(C\). Bit length therefore
grows as \(O(\log(n+1)+\log N)\). An independent 256-step run checks the exact
formula, scalar oracle, every inverse and rewind. The native lane also executes
4096 steps. At fixed proper time \(1/8\), the N=24,48,96 runs use 13,15,17 bits
and have exactly equal physical \(V=2185/768\), \(U=67/16\).

This cost improvement applies to the new massless anisotropic family. PR60's
projective spinor model contains a **massive** scalar; its exponential bit growth
has not been repaired by substituting a different matter model.

The chart requires positive dust, nonzero scalar momentum, positive volume and
an expanding current and previous slice. The retained source/shear values are
integers in fixed units; physical volume/velocity are rational only when the
declared static scaling is integral. There is no claim of representing every
real Bianchi-I initial condition exactly.

## Review-discovered diagnostic bug

The initial passive integral used a single `log1p` expression for both signs of
\(U-U_{\rm ref}\). On a valid backward-reference diagnostic chart near the
positive square-root branch, rounding could turn its argument into exactly
\(-1\), producing an infinite integral and a degenerate numerical metric.
The reproducer uses N=\(10^{160}\), V=1, U=\(10^{80}\), Uref=U+1 at 60-digit
precision. This deliberately off-constraint state is a legal diagnostic input;
it must remain visibly off constraint, not be repaired or accepted as physical.

The owner fixes this by swapping the current/reference arguments for negative
increments, using the positive-increment `log1p` expression, and negating the
result. Exact rational differences are formed before numerical conversion. The
review compares the resulting finite value with an independent 240-digit
logarithm expression and requires relative error below \(10^{-55}\).
The tensor and default complete seed are unchanged.

## Evidence boundaries

The review requires fresh SHA-256 source hashes from all five other audits and
joins tensor, complete seed, N and actual step count across native execution,
saved runtime, metric, covector diagnostics and clocks at each resolution.
The separate Noether face tensor is explicitly excluded from sourced Einstein
acceptance. Its own carry-inclusive continuity law is a useful arithmetic
result. The nonuniform same-tensor negative has a different complete seed:
pointwise Q=0 coexists with a nonzero spatial momentum constraint. This is
evidence of the remaining spatial obligation, not a spatial Einstein solution.

Covector/geodesic quadrature is passive diagnostic work and retains no moving
probe. Its convergence and norm identities do not certify a material worldline
or apparatus. Finite-precision metric checks likewise do not replace the exact
symbolic source/metric derivation.

## Primary readings and reproduction

- Khalatnikov and Kamenshchik, [A generalisation of the Heckmann-Schucking
  cosmological solution](https://arxiv.org/pdf/gr-qc/0301022), section 2,
  equations 14-23, and section 3, equations 27-31: the anisotropy constants and
  dust/stiff-matter volume solution motivate this coordinate choice. The paper
  uses its own normalization; this audit independently checks ours.
- Noether, [Invariant Variation Problems](https://arxiv.org/pdf/physics/0503066),
  section 1 theorems I/II and the relativity example, section 2 equations 11-13:
  conservation identities are tied to a specified variational problem and its
  symmetries. They are not a unique prescription for every dynamical map.

After the other five audits have produced fresh evidence:

```sh
python -m validation.conservation_closure.review
```

Source: `validation/conservation_closure/review.py`.
Evidence: `runs/conservation_closure/review.json`.
