# Exact metric-source and checkerboard audit

This note concerns the existing scalar `metric.h00` stencil and selected saved
histories. It does not identify the register with an operational spacetime
metric. No source file or default coefficient was changed.

## 1. Exact equation, including retained remainders

Write `F=b_h00`, `A=a_h00`, `R=r_h00`, and collect every non-free-stencil
input into `J`. With the periodic six-neighbor Laplacian

$$
\Delta F_x=\sum_{y\sim x}(F_y-F_x),\qquad
u_x=DF_x+w\Delta F_x+J_x,
$$

the actual Rule3 equation is

$$
D(F'_x-2F_x+A_x)=2w\Delta F_x+2J_x+R_x-R'_x. \tag{1}
$$

For the default, `w=Q−1`, `D=6Q`. After the exact resolution lift by `M`,
`D_new=M D` and `w_new=M(Q−1)`; replacing the latter by `Q_new−1` would change
the embedded source law.

The six periodic shifts are permutations, hence `sum_x ΔF_x=0`. Define the
bookkeeping quantity

$$
p=D\sum_x(F_x-A_x)+\sum_xR_x.
$$

Then

$$
\boxed{p'-p=2\sum_xJ_x.} \tag{2}
$$

This is an exact integer ledger, not a physical-energy identification. It
separates coherent source accumulation from a supposed irreversible rounding
loss. For a retained history of `T` updates,

$$
2\sum_{n=0}^{T-1}\sum_xJ_{n,x}=p_T-p_0. \tag{3}
$$

The endpoint audit uses this identity to infer the cumulative total source;
it does not claim to reevaluate every intervening polynomial.

A *complete static* metric state has `A=F'=F` and `R'=R`, so (1) requires
`w ΔF+J=0` at each site. In particular `sum J=0` is necessary on the periodic
board. An indefinitely bounded finite-board orbit also requires the long-time
average total source to vanish, by (2). These conditions are necessary, not
sufficient for stability or for a gravitational solution.

The available background register satisfies `u_B=D B`. Preparing `a_B=b_B`
therefore holds it fixed and gives a time-independent term `−B` in `J`.
It can cancel a selected instantaneous or averaged source, but cannot cancel
an arbitrary changing source merely because it canceled the initial value.
Recomputing a global average and replacing `B` during evolution would add an
undeclared nonlocal controller and is not an admissible repair.

## 2. Actual source terms

The default reciprocal first-order matter lapse differentiates

$$
\Phi_{\rm lapse}=-\frac1{2P}\sum_xF_x\Phi_{{\rm site},x}
 -\frac1{2P}\sum_{\langle xy\rangle}(F_x+F_y)\Phi_{{\rm link},xy}.
$$

Therefore its total source is

$$
\sum_xJ_x^{\rm matter}
=-\frac1{2P}\sum_x\Phi_{{\rm site},x}
 -\frac1P\sum_{\langle xy\rangle}\Phi_{{\rm link},xy}.
$$

The site form contains the signed matrix `W0`, and the entire source is a
quadratic expression in the current `b` snapshot. It is neither a positive
mass density nor an exactly conserved complete-state energy by definition.
Its time variation is visible in the saved data.

The optional metric clock port adds `−λ C_metric² F` for `h00`. This is an
extra oscillator-stiffness term, not the construction of an Einstein source
or Bianchi identity. Reference and second-matter sources are also present in
the tensor but vanish in the selected dormant preparations.

The [committed evidence](evidence/metric_source_audit.json) includes the exact
snapshot decomposition, tensor and state hashes, node-ledger residuals and
source sums. These snapshots belong to the preparations in
[the clock research record](CLOCK_RESEARCH.md); the audit does not add a new
long-run physical claim.

| Preparation and update | Mean F | Current mean source acceleration `2 sum J/(DN)` | Cumulative mean source acceleration |
|---|---:|---:|---:|
| Original L3, 1600 | −647280.111111 | −4.12171607 | −1.19541330 |
| Original L3, 2180 | −2994756.518519 | −89.85997033 | −3.80924961 |
| Low16 L4, 10000 | 8781.796875 | 0.0001807703 | 0.0001897829 |
| Connected S64 L3, 5000 | 596.481481 | 0.0001680439 | 0.0000835000 |
| Connected S64 L4, 5000 | 2023.359375 | 0.0002139005 | 0.0001692409 |

The original and low16 snapshots have zero background, reference and
second-matter source. Their nonzero uniform source is the first matter
sector. At connected L4 update 5000, the clock-port contribution to the mean
source acceleration is only `−7.99224e−11`, versus `+0.00021390058` from
matter. The direct portal is not the dominant uniform source in that snapshot.

The observed one-step integer acceleration can differ substantially from the
source contribution because of `R−R'`. For example low16 L4 at update 10000
has actual mean acceleration `1/64`; the remainder contribution is
`0.0154442297`. All node, uniform and even-grid checkerboard ledger residuals
are exactly zero, and each independently computed next snapshot exactly
rewinds. This is no proof of physical conservation.

## 3. The checkerboard is a separate mode

On even `L`, set `ε_x=(−1)^(x+y+z)`, `C=sum εF`, and `J_pi=sum εJ`.
The mean checkerboard amplitude quoted below is `C/N`, with `N=L³`.
Because `sum ε ΔF=−12 C`, equation (1) gives

$$
D(C'+C_{\rm previous})-2\beta_\pi C
=2J_\pi+\sum_x\epsilon_x(R_x-R'_x),\qquad
\beta_\pi=D-12w. \tag{4}
$$

For the unscaled default, `β_pi=−D+12`. The remainder-free homogeneous
recurrence has roots on the unit circle, not a repeated root at `−1`.
Nevertheless this linear calculation omits the full remainder force.

At saved low16 L4 updates 10000 and 33000 the direct source projection
`J_pi` is exactly zero. The earlier checkerboard amplitude is
`18345.421875`, with a maximum residual of `78.78125` after removing the
uniform and checkerboard parts; the later values are recorded in the JSON.
At those specific transitions, the remainder term alone supplies the
inhomogeneous part of (4). This does not prove `J_pi=0` at every intervening
step, nor that rounding alone explains every mode of the full system.

## 4. Exact long-lived checkerboard drift in the free stencil

There is a stronger arithmetic observation. Restrict an even cube to a state
constant on each parity sublattice. Denote the two counter values by `b_+`
and `b_-`. The six neighbors of each parity all have the opposite value, so
the exact reduced input is

$$
u_+=6b_++6(Q-1)b_-,\qquad
u_-=6b_-+6(Q-1)b_+.
$$

This is an invariant restriction of the existing free metric tensor, not a
new update. Put `r0=D/2−1`, `b_+(0)=B`, `b_-(0)=−B`,
`a_+(0)=−B+v`, `a_-(0)=B−v`, and both initial remainders equal to `r0`.
As long as the following residues remain within `[0,D−1]`, exact Rule3 gives

$$
b_+(t)=(-1)^t(B+vt),\qquad b_-(t)=-b_+(t),
$$

$$
r_+(2k)=r_0-24vk,\qquad
r_+(2k+1)=r_0+24B+24vk,\qquad
r_-(t)=2r_0-r_+(t). \tag{5}
$$

To prove this, substitute `b_-=-b_+`, obtaining
`2u_+=−2D b_++24b_+`. If `r_++24b_+` stays in range, the quotient is exactly
`−2b_+`, so `b'_+=−2b_+−a_+`. Its solutions include the displayed alternating
linear form, and summing `24b_+` yields the displayed residues. The negative
parity recurrence gives the opposite quotient and complementary residue.
This also proves invariance of the reduction.

For `v=0` and `|24B|≤r0`, the **complete state has period dividing two**; for
`B≠0` its minimal period is two. Thus the
remainder-free detuned frequency is not the exact frequency of these integer
preparations.

For `v=1`, `B=512`, `Q=2^33+1`, the inequalities hold for at least
`2,147,482,625` updates. The amplitude then grows exactly as `512+t` through
that interval despite the free linear eigenvalue being inside its oscillatory
band. This is an algebraic finite-interval statement, not an assertion of
unbounded growth after the residues reach their boundaries.

[The public reproducer](../experiments/geometry/carry_locked_metric.py) runs
four actual reduced histories for 1,000,000
updates and 1,000,000 inverse updates each. It independently checks the first
32 complete updates against `Engine` on a four-cubed board. Three `v=0`
preparations (`B=512,18345,289784`) preserve their amplitudes exactly. The
`B=512,v=1` preparation reaches amplitude `1,000,512`. All rewind exactly.
These results and all reduced seeds/final states are included in the committed
evidence. The million-update runs use the proved two-sublattice reduction;
they are not million-update runs of the full default field tensor. Reproduce
them from a checkout with:

```bash
python experiments/geometry/carry_locked_metric.py --steps 1000000 --out runs/carry-locked-metric/report.json
```

## 5. What a repair would actually require

* For a static periodic target, build a locally justified, conserved source
  and compatible background/initial constraints, then prove the zero-mode
  balance. A fitted initial subtraction only controls the fitted preparation.
* If uniform geometry is intended to evolve, derive an operational scale
  factor, source conservation and gravitational constraints. Drift of `h00`
  alone is not a cosmological expansion or bounce.
* Reserve a meaningful wave-band margin before adding couplings, and test
  actual integer dynamics on even boards. The exact resolution lift alone
  preserves the old orbits and cannot remove their carry-locked drift.
* Show stability over the declared amplitudes, remainder phases and velocity
  perturbations. A smooth-wave eigenvalue estimate omits examples (5).

These are mathematical requirements and construction options. None establishes
the full Einstein equations, quantum entanglement or an entropy/complexity
selection principle for the current model.

The carry-locked example lies at the fast lattice corner. It does not refute
a separately proved smooth, low-frequency continuum limit. It shows that
the admissible amplitudes, initial velocities, remainder phases and
perturbations of such a limit must be controlled explicitly; free linear
band membership does not control the complete integer state space.
