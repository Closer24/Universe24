# Light, restoring motion and link-delay audit

This investigation uses current main `3285c11fcde949774f9db5f80fecd696dbbd0039`
(native 48-channel light). It does not silently port the older 25-channel
face-processor proposal across the current schema-3 admission boundary.

The executable is `validation/light_link_resonance.py`. Every candidate is a
complete bundle executed by the existing Engine and saved-run runtime. The
installed light tensor and Engine are unchanged. Different candidate laws are
controls, not combined evidence for one physical universe.

## What the current source actually implements

There are 48 node channels in the left regular representation of 2O, with
144 retained integers per node. Eight channel labels point along each of the
six cube directions. There is currently no independent undirected edge object
holding a single physical length shared by its endpoints.

For label `g`, `n_g`, `e_g`, `m_g` are the rotated propagation, electric and
magnetic axes. The installed law is

\[
u_g(x)=3[b_g(x-n_g)+b_g(x+n_g)].
\]

With prepared `a_g(x)=b_g(x+n_g)`, Rule3 transports the profile by one face
per tick. The existing passive readouts are `E=sum e_g b_g` and
`B=sum m_g b_g`. This is a flat, axis-aligned plane-wave sector, not a photon
detector or a coupled Einstein solution.

Let `bar(g)` be the central partner `-g`. Both partners have identical
`(n,e,m)`. Define passive variables

\[
p_g=b_g+b_{\bar g},\qquad q_g=b_g-b_{\bar g}.
\]

The field readout sees `p`, while the central contrast `q` cancels. Neither
variable is extra retained state. Signed differences are compatible with
strictly positive retained `a,b,r`.

## A restoring cycle alone does not lengthen the optical path

The first candidate adds a central restoring interaction:

\[
u_g=6b_g+h\Delta_{n_g}b_g+k(b_{\bar g}-b_g),\qquad h=k=3.
\]

For spatially homogeneous contrast and equal partner remainders,
`q_next=-q_old`. Preparing `(q_old,q)=(0,1)` gives
`1,0,-1,0,1,...`, with conserved `q^2+q_old^2=1`. A tentative positive
readout `1+q^2` expands and contracts through `2,1,2,1,2,...`. Squaring also
removes the sign change under exchange of the central partners; `q` itself
is not a scalar geometric length.

The light still travels at exactly one face per tick: this restoring motion
is invisible to `E,B`. Merely naming `1+q^2` a length therefore does not give it
geometric meaning. The oscillation also is not a dissipative relaxation; an
isolated reversible law needs stored momentum/history to return.

An alternating spatial contrast is an essential negative control. With
`h=k=3`, its high-frequency mode satisfies `q_next=-4q-q_old` and grows. The
homogeneous four-cycle is not a stability certificate for arbitrary seeds.

## Why a naive varying wave coefficient fails the declared optical target

A second family couples pair sums and contrasts through the edge expression

\[
V_{g,x}=\frac{\lambda}{2}q_g(x)^2
           [p_g(x+n_g)-p_g(x)]^2.
\]

The polynomial includes the negative gradient with respect to both endpoint
amplitudes. The probe control omits the `q` force; the reciprocal control
includes it. These are explicitly distinct tensors. All terms have degree at
most three and use at most one physical face edge. The expression is a way to
derive reciprocal forces, not a claim that this Rule3 integrator exactly
conserves `V` plus a physical energy.

For `h=1,k=3,lambda=1` and homogeneous `q`, the probe reduces to

\[
p_{t+1}-2p_t+p_{t-1}
 =v_t^2\Delta_n p_t,\qquad v_t^2=(1+2q_t^2)/3.
\]

The declared comparison is Maxwell propagation under a **homogeneous change
of time parameter**, with fixed spatial geometry and no source. In units
`c=1`, `ds^2=-v(t)^2 dt^2+dx^2+dy^2+dz^2` has characteristic fields
`F_+(t,x)=F_+(0,x-integral v dt)`, so Fourier magnitudes are constant. For
smooth `v`, eliminating the other Maxwell field gives

\[
\partial_t^2 F-(\dot v/v)\partial_t F=v^2\partial_x^2 F.
\]

Changing only the spatial coefficient omits the history term. The discrete
probe is checked against the constant-magnitude characteristic requirement;
no derivative of the discontinuous tick sequence is used. At `L=4`, the
exact squared Fourier magnitude of the `k=pi/2` mode is multiplied by `65`
after twelve ticks. This is a failure of this interpretation and this tensor.
It is not a theorem that amplitudes must remain constant in all curved
spacetimes, all time-dependent media, or all Maxwell discretizations.

The probe's light preparation uses `3^13` as an explicit finite-horizon
precision scale; it is not an indefinite precision theorem. Including the
reciprocal light-to-contrast force produces negative retained values in the
registered small and large preparations. Nothing is clipped or reset.

## A working matched-phase transport mechanism on a restricted domain

The positive control uses a different cubic tensor:

\[
u_g(x)=3\{b_{\bar g}(x)+b_g(x+n_g)
       +q_g(x)^2[b_g(x-n_g)-b_g(x+n_g)]\}.
\]

It contains 384 monomials, all 48 explicit channels, and passes exact 2O
coefficient covariance. Every coefficient is a multiple of three, so Rule3
retains every initial remainder. There is no clock callback, runtime tensor
change, division by a changing length, or extra buffer.

With spatially uniform contrast, the same four-cycle persists. Its square
`s_t=q_t^2` alternates `1,0,1,0,...`. Pair sums satisfy

\[
p_{t+1}+p_{t-1}
 =p_t+s_t p_t(x-n_g)+(1-s_t)p_t(x+n_g).
\]

Prepare the optical part of both histories equal, because the previous tick
was a hold. Then the exact solution moves one face on odd numbered updates
and holds on even numbered updates. After `t` updates the profile is shifted
by `ceil(t/2)` faces. Both transverse fields follow this same shift. Their
discrete plane-field energy and Fourier magnitudes are unchanged.

For an arbitrary nonnegative integer profile `f`, a single prepared partner
pair obeys the explicit solution

\[
b_g(t,x)=\frac{2B+1+t+q_t}{2}+f(x-\lceil t/2\rceil n_g),
\]
\[
b_{\bar g}(t,x)=\frac{2B+1+t-q_t}{2}+f(x-\lceil t/2\rceil n_g),
\]

with matching `a=b(t-1)` and constant remainder `1`. All other pairs have
`f=0`. The numerators are even, so these are integers; for `B>=1`, all
retained entries remain strictly positive for all future ticks. The uniform
pair-sum drift cancels from `E,B`. Stored bit growth on this prepared sector
is logarithmic in elapsed ticks and profile amplitude, rather than a hidden
second state bank.

This proves an exact reversible move/hold mechanism on a homogeneous clock
sector. It does **not** prove physical expansion or contraction of an edge.
After the first move, successive arrivals one edge farther apart are two
ticks apart; this is a constant average transport speed of one half, not
evidence that an independently measured edge length is oscillating.
Nor is the integer step count already a material clock's proper time.

Two negative controls remain mandatory: an unmatched initial light history
loses the exact move/hold solution, and a spatially alternating clock contrast
leaves the natural-number domain. Spatial clock synchronization is a
preparation restriction, not an external synchronization operation during
evolution. No accepted optical-to-geometry backreaction is supplied by this
positive control.

## What a physical shared link still requires

1. One edge quantity `w_xy=w_yx`, computed consistently from the complete
   endpoint states without an uncounted edge bank. Eight oriented amplitudes
   per face are not themselves that shared quantity. If different channels
   assign different delays, a universal metric has not been established.
2. Transport and retained clock phase derived together, with the correct
   predecessor relation. The successful control demonstrates why simply
   multiplying the spatial terms by a varying coefficient is insufficient.
3. A restoring/source law that remains stable for nonuniform preparations
   and responds to the transported field, with an independent source and
   energy account. A fixed tensor may generate changing state; the tensor
   coefficients need not change at runtime.
4. Operational comparison of emitted and received signals using a retained
   material clock, followed by metric, constraint and refinement checks.
   Spatial angles/shear and spacetime lapse/shift are not determined by six
   independently named delays.

The appropriate natural reference for alternating geometrical distances is
tidal strain in a gravitational wave. LIGO's arms lengthen and shorten in
opposite directions, producing different return phases. The physical
observable is a signal's round-trip time measured by the observer's clock,
not a spring variable or an arbitrary coordinate distance. This motivates a
future bidirectional operational test; it is not evidence that these tensors
already reproduce that effect.

For example, a weak plus-polarized wave in transverse-traceless coordinates
has, to first order, `g_xx=1+h(t-z/c)` and `g_yy=1-h(t-z/c)`, with
`g_tt=-c^2`. Over an edge short compared with the wave's variation scale,
the outgoing null travel times are approximately `dx*sqrt(1+h)/c` and
`dy*sqrt(1-h)/c`. Their opposite changes are a directional metric response.
The homogeneous move/hold control has neither this directional strain nor
a retained observer producing its round-trip proper-time record. It must
not be presented as a successful gravitational-wave simulation.

Primary sources:

- [LIGO: gravitational-wave stretching and return-time differences](https://www.ligo.caltech.edu/page/faq).
- [Blaut, 2019: gauge-independent interferometer response](https://arxiv.org/abs/1901.09956).
- [Lee and Zurek, 2025: proper-time observables](https://arxiv.org/abs/2408.03363).

## Reproduction and evidence

```bash
python -m validation.light_link_resonance --out runs/new-light-link-resonance
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-light-link-smoke
python -m universe24 verify --run runs/new-light-link-smoke/run
```

The audit registers twelve installed-light cases, twelve matched-phase cases
(six directions times two polarizations), and seven other positive/negative
controls. For every candidate it checks an independently derived force on
every saved step, the scalar monomial oracle on the first two steps, complete
forward replay, each inverse step and full rewind. Source hashes are frozen
for the whole collector. Outcomes and the first nonpositive retained value
are reported without filtering failed cases.

Fresh full evidence: `runs/light-link-resonance-20261113-v2/results.json`.

The completed panel contains **31 runs and 917 forward updates**, with exact
saved replay. The twelve matched-phase preparations each run for 64 updates
(768 updates total), retain strictly positive integers, preserve their
plane-field energy, and use at most 6 bits per stored integer on these seeds.
All candidate runs match the independent force oracle; complete inverse and
rewind pass even for the intentionally unstable laws. The active software
suite passes **117 tests** (40.238 seconds), the generic six-step scalar/replay
smoke passes, and an additional CLI verify of `phase-0-1-1` passes.

| Registered control | Measured outcome |
| --- | --- |
| Installed light, 12 directions/polarizations | Exact one-face translation and plane-field energy |
| Homogeneous restoring cycle | Period four; light unchanged |
| Spatially alternating restoring cycle | First nonpositive retained value at tick 3; 19-bit maximum over 10 ticks |
| Naive optical coefficient | Exact mode squared-norm ratio 65 after 12 ticks; 25-bit maximum |
| Reciprocal coupling, small preparation | First negative value at tick 2; 34-bit maximum over 4 ticks |
| Reciprocal coupling, large preparation | First negative value at tick 1; 121-bit maximum over 3 ticks |
| Matched-phase transport, 12 preparations | All 64-step histories have exact move/hold transport and positive integers |
| Matched-phase transport, spatial clock perturbation | First negative value at tick 3; 13-bit maximum over 4 ticks |
| Matched-phase transport, wrong predecessor | Exact transport and plane-energy checks fail; integers remain positive |

The first collection directory is preserved as an incomplete attempt: its
observer mixed NumPy fixed-width and Python big integers while squaring a
large contrast. The observer was corrected to Python-integer arithmetic and
the full panel rerun in the fresh v2 directory. No Engine arithmetic or
scientific gate was changed to pass that correction.

The general dynamic Einstein/source and photon-detection gates remain
unestablished. This source-only audit introduces no installed default model,
no new runtime interface and no research tests in the active unit suite.
