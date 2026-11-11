# A local TT metric readout and a one-way link probe

This isolated experiment reconstructs a prepared travelling metric perturbation with an exact **linearized lattice Einstein operator** and makes a separate scalar probe respond through fixed local tensor coefficients. The two results do not yet establish one universal Einstein geometry: the metric pattern and the probe have different characteristic speeds, and reciprocal stress/backreaction is omitted. No default tensor or core update is changed.

The construction builds on [the exact integer curl-wave sector](LINEAR_SPIN2.md). Its runtime remains the existing scalar Rule3, with one fixed divisor and one fixed tensor. Internal phase registers, metric registers and probes all use that same update.

## From a curvature profile to a metric profile

Let $S f(z)=f(z+1)$ and $\delta_z=S-S^{-1}$. For a TT wave with macrostep duration $2\,dx$, choose the staggered curvature convention

$$
E=-\frac12 D_t^-D_t^+h=-\frac{\delta_z^2h}{8\,dx^2}.
$$

Here $D_t^+=(T-I)/(2dx)$, $D_t^-=(I-T^{-1})/(2dx)$ and the travelling macrostep has $T=S^2$. The stored magnetic-like variable is advanced by half a macrostep: $B=JSE$, where $J(p,q)=(-q,p)$ rotates the two polarisation components. Choosing the usual opposite-sign Weyl convention identifies the physical magnetic orientation with minus this stored $B$. The staggering and sign convention are declared before running.

On an odd periodic grid, $\delta_z^2$ has only the constant kernel. A zero-mean curvature profile can therefore be inverted once over rational numbers after fixing the metric's constant mode. This preparation is generally nonlocal; it is not an extra local update. Even grids also have a Nyquist kernel and require the corresponding compatibility condition. Alternatively, one can choose an integer metric profile first and derive its curvature by differences.

For the two zero-mean profiles in the curl experiment, clearing the rational denominator gives $M=7$ and

```
Hplus  = (120, -96, 24, -24, -16, 48, -56)
Hcross = (80, -32, 24, -32, -32, 24, -32)
```

They obey $\delta_z^2H=-8M E$ exactly. Set the physical perturbation to $h=H/(MP)$, with $P=4096$. The spatial TT matrix has eigenvalues $1$ and $1\pm\sqrt{H_+^2+H_\times^2}/(MP)$, all positive for these profiles. Exact translation preserves that bound for all time. This is a chosen weak-field preparation, not a dynamically enforced positivity condition for arbitrary seeds.

## The carrier can be decoded by local Rule3 registers

Run the same curl tensor on a pair whose electric-like profile is $H$. Its retained fields still have the fixed sign carrier described in the curl experiment. Add two node registers with zero input, prepared uniformly as

$$
(a_c,b_c)=(0,1),\qquad (a_s,b_s)=(-1,0).
$$

Their exact sequences are $c_t=(1,0,-1,0,\ldots)$ and $s_t=(0,1,0,-1,\ldots)$. Their remainders stay fixed. The local quadratic observable

$$
\mathsf H_t=c_t E_t-s_t J B_t
$$

then equals $S^tH$ at **every** microstep. In the plus-polarisation case used by the probe,

$$
F_t=c_t(E_t)_{xx}+s_t(B_t)_{xy},\qquad
h_{xx}=F_t/(MP),\quad h_{yy}=-h_{xx}.
$$

This is an identity of the prepared local registers. No phase callback, state overwrite or runtime tensor change is applied. A probe can read the product directly as tensor monomials.

The uniform phase preparation is an additional declared condition. These are internal phase registers, not observed physical clocks: their Rule3 quotient is always zero, so they emit **no official click records**. Consequently the metric polynomial is a board observable, not a reconstruction from the official stream alone. The computational step label has not been established as physical proper time.

## Which Einstein identities hold exactly

Take $h_{0\mu}=0$, $h_{zz}=0$ and the transverse plus/cross matrix above, with $h(t,z)=H(t+z)/(MP)$. Define commuting central differences $D_\mu=(S_{+\mu}-S_{-\mu})/2$ in unit lattice spacing. Then

$$
\operatorname{tr}h=0,\qquad D^ih_{ij}=0,\qquad
D_t^2h=D_z^2h.
$$

Substitution into the linearized Ricci operator gives $R^{(1)}_{\mu\nu}=0$ exactly. The linear Hamiltonian and momentum constraints also vanish with $K^{(1)}_{ij}=-D_th_{ij}/2$. The electric linearized Riemann component $R^{(1)}_{0i0j}=-D_t^2h_{ij}/2$ agrees with the original curvature profiles divided by $P$.

[The passive reconstruction check](../experiments/geometry/linear_metric_reconstruction.py) evaluates all sixteen Ricci components and the constraints on the full periodic spacetime profile, using exact integers. [Its evidence](evidence/linear_metric_reconstruction.json) states the operator convention. A square of a central first derivative uses a two-cell stencil; it is not the nearest-neighbour second difference at finite spacing. The two agree only in an appropriate smooth refinement limit.

These are linearized identities. For example, the continuum plus metric

$$
ds^2=-dt^2+[1+p(u)]dx^2+[1-p(u)]dy^2+dz^2,
\qquad u=t+z,
$$

has, in general,

$$
R_{uu}=\frac{p p''}{1-p^2}
+\frac{(p')^2(1+p^2)}{2(1-p^2)^2},
$$

which is nonzero at quadratic order. Thus the bounded TT profile does not solve the full nonlinear vacuum equations without additional geometric response. Nor does a passive metric reconstruction show that all matter measures that metric.

Carroll's [Lecture Notes on General Relativity](https://arxiv.org/pdf/gr-qc/9712019), section 6, supplies the continuum linearized curvature, TT gauge and geodesic-deviation framework. Maartens and Bassett's [Gravito-electromagnetism](https://arxiv.org/pdf/gr-qc/9704059), equations 2 and 32–35, supplies the Weyl-curl conventions. The exact difference identities and Rule3 realisation here are separate calculations for this experiment.

## A fixed diagonal link response

The probe experiment uses the plus profile only. Let $R=MP$, $Q=4R$, $D=6Q$ and $w=2R$. Two independent scalar probes have identical fixed input rules

$$
u_\chi=D\chi+w\sum_{y\sim x}(\chi_y-\chi_x)
-\frac{w}{2R}\sum_{y=x\pm e_i,\ i=x,y}
\sigma_i(F_x+F_y)(\chi_y-\chi_x),
$$

where $\sigma_x=1$ and $\sigma_y=-1$. The endpoint average is part of the fixed rule. Since $F=cE_{xx}+sB_{xy}$ is quadratic in registers, the metric correction to the input is cubic, hence tensor order four. Every monomial occupies one node or one face edge. All coefficients are integers because $w/(2R)=1$.

The corresponding probe link stiffness is $w(1\mp F/R)$ in the x/y directions. It is positive for the bounded profile. Because $F$ depends only on z, the six link weights sum to $6w$ exactly; each frozen input operator has spectrum in $[D-12w,D]=[0,D]$. This gives a frozen spectral margin, not an all-time bound for an evolving coefficient sequence.

The metric and phase registers receive no probe source. All 48 surviving one-way input monomials are explicitly designated as test-body terms. The remaining tensor passes reciprocity checking. Adding the omitted reciprocal terms would change the phase and TT evolution and would require a new constraint proof.

A cross-polarisation term $h_{xy}\Delta_x\chi\Delta_y\chi$ would touch three sites, so this direct scalar form violates the strict one-edge support requirement. That response is not included or silently approximated.

## What the actual official records show

Both runs use the same 23-gear, rank-four tensor: eighteen metric-pair gears, two internal phase registers, two probe gears and one independent rest-clock gear. Only the initial metric profile differs between the flat and wave preparations. The two probe seeds are coordinate-swapped plane pulses. Detectors are fixed before running at $(2,0,0)$ and $(0,2,0)$.

Over 84 updates, both histories preserve every asserted microstep metric identity, raw TT constraint and metric/phase remainder, and both rewind exactly. The full signed official quotient series are retained in [the evidence](evidence/phase_metric_probe.json).

| Check | Result |
|---|---|
|Official records per history|76,244|
|Internal phase-register official records|0|
|Flat x/y detector series|Identical|
|Wave x/y detector series|Different|
|Wave versus flat changed samples per detector|83 of 84|
|First changed detector sample|Update 2|
|Largest signed-quotient change|303 for x; 290 for y|
|First detector event|Update 2 in both histories|
|Independent rest-clock series|Identical|

The result demonstrates a fixed local metric-shaped influence on actual official probe records. It does not measure a calibrated geodesic or arrival-time shift: the first event occurs at the same update in both controls. Counting events alone also misses the response, since the total counts are equal.

In TT gauge $N=1$ and the shift is zero, so coordinate-fixed rest clocks have no first-order lapse change. Spatial propagation and relative separations are the relevant first-order tests. The unchanged independent clock is consistent with that target but does not prove the equivalence principle.

The most important remaining mismatch is quantitative: the exact metric pattern travels one site per update, whereas the scalar probe's flat long-wave speed satisfies $c_0^2=2w/D=1/6$. Therefore the combined model does not yet supply one common characteristic metric. Interpreting the probe stiffness as a continuum scalar action can define a different effective metric, but cannot remove this mismatch by renaming coordinates. General redshift, off-diagonal response, reciprocal gravity and nonlinear Einstein evolution remain separate requirements.

## Reproduction

```sh
python experiments/geometry/phase_metric_probe.py --out runs/geometry/phase_metric_probe.json
python experiments/geometry/linear_metric_reconstruction.py --out runs/geometry/linear_metric_reconstruction.json
```

Both outputs include the executing script's hash. The probe script uses the existing engine; the reconstruction script is passive exact algebra. Neither modifies the default implementation.
