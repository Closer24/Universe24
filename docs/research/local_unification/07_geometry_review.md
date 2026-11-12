# Independent proof of the source-coupled null chart

This review concerns the same twelve-channel carrier/record/profile tensor,
not a detached geometry example. It distinguishes exact continuum identities,
the finite native causal domain, and execution evidence. Source code is
`validation/local_unification/geometry_review.py`; regressions are
`test_local_unification_geometry_review.py`.

## Geometry and physical normalization

In null coordinates \((u,v,y,z)\), let

\[
ds^2=-2R^{-1/2}du\,dv+R(dy^2+dz^2),\qquad R=f(u)+g(v)>0.
\]

The reviewer constructs the full metric inverse, Christoffel symbols, Ricci
tensor and Einstein tensor independently. Direct simplification gives

\[
G_{uu}=-f''/R,\qquad G_{vv}=-g''/R,\qquad
G_{\mu\nu}=0\ \hbox{otherwise},\qquad {\cal R}=0.
\]

All sixteen component residuals are checked, including off-diagonal and
transverse components. In units \(8\pi G=1\), choose nonnegative source profiles
\(n_+(u)=-f''(u)\), \(n_-(v)=-g''(v)\). The independently declared stress is
\(T_{uu}=n_+/R,T_{vv}=n_-/R\), rather than a source defined as “whatever the
Einstein tensor is.” Its raised components are \(T^{vv}=n_+(u)\) and
\(T^{uu}=n_-(v)\). All four covariant-divergence components vanish.

The future null vectors \(k_+=\sqrt R\,\partial_v\) and
\(k_-=\sqrt R\,\partial_u\) are null and affine geodesic vectors; all eight
acceleration components vanish. Physical time and longitudinal position are
\(t=(u+v)/2,x=(v-u)/2\), hence \(u=t-x,v=t+x\), with
\(g_{tt}=-2/\sqrt R\). The local orthonormal observer measures

\[
\rho=\frac{n_++n_-}{2\sqrt R},\qquad
j_x=\frac{n_+-n_-}{2\sqrt R}.
\]

Thus \(\rho\ge|j_x|\). Raw particle counts are not this curved-space density.
No global conserved physical energy is inferred from the discrete packet
account. Reversing the identification of null coordinates and calling a
spacelike coordinate time is explicitly rejected.

## Exact interpolation, not a finite-difference approximation

The centered cubic basis is

\[
B_3(s)=
\begin{cases}
(4-6|s|^2+3|s|^3)/6,&|s|<1,\\
(2-|s|)^3/6,&1\le|s|<2,\\
0,&|s|\ge2.
\end{cases}
\]

The reviewer differentiates these polynomials directly on six intervals and
checks the knots independently. With \(B_1(s)=\max(1-|s|,0)\),

\[
B_3''(s)=B_1(s+1)-2B_1(s)+B_1(s-1).
\]

Consequently a retained coefficient profile satisfies

\[
\frac{d^2}{dx^2}\sum_jF_jB_3(x-j)
=\sum_j(\Delta^2 F)_jB_1(x-j).
\]

If the exact integer constraint is \(\Delta^2F=-q\), the continuum source is
precisely \(\sum_jq_jB_1\), which is nonnegative for nonnegative rail occupancies.
These are B-spline coefficients, not samples through which the cubic curve
must interpolate. In particular \(B_3(0)=2/3\), not one. The identity is checked
on six polynomial intervals, forty-nine rational points including knots,
and forty-one reconstructions of a nonconstant independently integrated source.

The reconstructed potentials are \(C^2\), so the metric is \(C^2\) wherever
\(R>0\). The continuous sources are piecewise linear; conservation also holds
in the weak sense at their derivative knots. No delta-shell or squared-delta
interpretation is needed.

## Complete-history finite-chart theorem

For one plus-profile pair, the ideal characteristic map is

\[
h^A_+=h^B,\qquad h^B_+(x)=h^A(x-1).
\]

Species-summed directional occupancy has exactly the same map because the
collision preserves each directional total. Therefore
\(C^{A,B}=\Delta^2h^{A,B}+q^{A,B}\) swaps/translates under the ideal map.

The actual source-dependent native recurrence is

\[
h^A_+=3h^B-h^B(x-1)-q^B-h^A_-,\qquad
h^B_+=3h^A-h^A(x+1)-q^A-h^B_- .
\]

Preparing the complete old history by the ideal inverse makes each expression
equal its ideal next value minus the current constraint. Initially the
constraint holds on sites \(1,\ldots,L-2\); only the explicit periodic seams
violate it. A native source stencil has radius one per Engine tick. The ideal
constraint moves no faster than one site per two ticks. Induction shows:

- Actual and ideal current coefficients agree on
  \([n,L-1-n]\) at Engine tick \(n\).
- Current coefficients and their source constraints both agree on
  \([n+1,L-2-n]\).
- Cubic support two permits the more conservative readout interval
  \([n+3,L-4-n]\).

The minus sector has reversed shifts and the same bound. This is a theorem
about the full previous/current preparation, not just a current-slice
constraint. Adding a constant to the old profile can leave every current
constraint unchanged while invalidating the characteristic history; a
regression rejects that case even though complete Rule3 inversion still works.

At even tick \(2m\), summing the two banks gives exactly
\(F_{2m,j}=F_{0,j-m}\), \(G_{2m,j}=G_{0,j+m}\), with the same translations for
the source occupancies. Reindexing the spline sum proves that these states are
samples of one initial-profile solution,
\(R(m,x)=f_0(x-m)+g_0(x+m)\). The saved reviewer checks this original-anchor
identity separately from the slice constraints.

## All-continuous positivity and the periodic obstruction

For \(0\le t\le N/2\), the domain

\[
2t+3\le x\le L-4-2t
\]

keeps every required initial spline support inside the proved causal chart,
where \(N\) is the declared microtick horizon. Nonnegative partition-of-unity
weights give

\[
R(t,x)\ge
\min F^A_0+\min F^B_0+\min G^A_0+\min G^B_0>0 .
\]

The exact high-offset preparation satisfies this bound. It proves
nondegeneracy throughout the continuous domain, not only at sampled times.

On the entire periodic lattice,
\(\sum_j\Delta^2F_j=0\). Thus \(\Delta^2F=-q\), \(q\ge0\), implies \(q=0\)
everywhere. The nonzero-source construction is therefore a finite causal
chart and cannot be promoted to a global periodic Einstein universe. The
excluded seams and their possible later influence are part of the result.

## Execution and acceptance

`audit(out,run_dir=...,protocol=...)` joins the proofs to the actual saved
twelve-channel trajectory. It independently expands all twelve scalar
recurrences, checks contiguous full states and complete inverse preparation,
compares anchored macro coefficients, and reconstructs rational metric/source
samples using its own directly differentiated cubic basis. Tensor, bundle,
run and horizon identities are recorded.

The pure metric/source/spline audit passed locally before the execution
environment became unavailable. The subsequent saved-chart implementation,
regressions and exact-input guards were authored through the repository
connector and require the final source-pinned CI run; they are not retroactively
described as locally executed. The final validation ledger determines which
recovered-source checks completed.

This establishes, subject to the actual joined execution checks, a restricted
positive two-null-stream Einstein chart with retained source coefficients and
record-label scattering. It does not establish massive bodies, general
gravitational backreaction, operational clocks, global cosmological evolution
or sustained complexity growth.

Primary mathematical context: the centered cardinal construction and
difference identities are described by Carl de Boor,
https://pages.cs.wisc.edu/~deboor/toast/pages005.html . The particular metric,
source normalization, exact native identities, domain bounds and counterexamples
above are independently derived and checked here, not attributed to that source.
