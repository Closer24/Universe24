# Six face clocks, observable events, and the Einstein target

`validation/geodesic_link_audit.py` is a passive audit of existing canonical
phase-transport runs. It does not provide a reference metric to the Engine,
create another runtime, or promote arithmetic update indices to proper time.

## The observation boundary

The audit's observation function reads only `clicks.jsonl.gz`: address,
update index, arithmetic quotient, class and sign. Its two declared observation
addresses are `(3,0,0)` in the positive-x preparation and `(0,3,0)` in the
positive-y preparation. It compares the local quotient/class/sign histograms
on each update. The original channel-labelled records are retained in the
input; the histogram is an explicit coarse-graining, not an assertion that
all possible click observables agree.

A separate auditor replays each complete bundle and checks the exact prepared
phase tensor/seed identity. That integrity operation is not additional
information available to the click observer. No hidden field position, metric
or reconstructed particle path is used by the observation function.

The selected x/y preparations have identical local histograms over their
whole 64-update horizon. This is evidence of their homogeneous directional
symmetry. It is not a measured zero gravitational strain: these preparations
contain no declared gravitational-wave source, retained interferometer or
calibrated proper clock.

## An independent, finite-frequency null-round-trip target

In units `c=1`, take the weak plus-polarized transverse-traceless reference

\[
ds^2=-dt^2+[1+h(t-z)]dx^2+[1-h(t-z)]dy^2+dz^2,
\qquad h(s)=\epsilon\cos(\omega s).
\]

All following statements are to first order in `epsilon`. Fixed-coordinate
endpoint observers are freely falling in this gauge, and the beamsplitter
at the origin has `d tau=dt`. Let the two transverse arms have equal
coordinate length `D`. Integrating on the unperturbed outgoing and returning
null paths gives

\[
\delta T_x(t_0)=\frac12\int_{t_0}^{t_0+2D}h(t)dt,
\qquad \delta T_y=-\delta T_x,
\]

\[
\Delta\tau(t_0)=T_x-T_y
=\frac{\epsilon}{\omega}
 [\sin\omega(t_0+2D)-\sin\omega t_0].
\]

This retains the finite-frequency response; it does not replace the entire
flight by an instantaneous arm length. For `epsilon=0.01`, `omega=pi/8` and
`D=1`, `Delta tau(0)` is approximately `0.0180063263`. Emissions at different
phases give opposite differential signs. The audit independently compares
the analytic expression with midpoint integration and checks zero-amplitude
and zero-frequency limits. Its floating-point reference calculations never
enter a bundle or a tensor.

The nonzero tidal components in this convention are
`R_0x0x=-h''/2` and `R_0y0y=+h''/2`. In contrast, a spatially uniform positive
lapse `ds^2=-N(t)^2 dt^2+dx^2+dy^2+dz^2` is flat under `tau=integral N dt`.
A common change of clock rate is therefore insufficient evidence of curvature.

The phase-gated mechanism's transport count `ceil(t/2)` also has plateaus.
It is not an invertible smooth time-coordinate transformation and cannot
itself be inserted as a Lorentzian proper-time coordinate on every microscopic
update. A coarse clock interpretation needs its own apparatus and limit.

## Six lengths do not determine the required metric

The exact matrices

\[
h_0=\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix},
\qquad
h_1=\begin{pmatrix}1&1/2&0\\1/2&1&0\\0&0&1\end{pmatrix}
\]

both give squared length one for all six coordinate face vectors. Their
determinants are `1` and `3/4`, so both are positive definite. However, the
squared norm of `(1,1,0)` is `2` versus `3`, and the x/y angle cosine is `0`
versus `1/2`. The audit computes these facts in exact rational arithmetic.
Both examples are flat; the counterexample concerns missing shear information,
not a claim of detected curvature. Assuming orthogonal cube axes would select
a restricted diagonal metric rather than derive the missing data.

Temporal lapse/shift, causal orientation, endpoint clock calibration and
cross-face transport consistency also need an interpretation. A common
reciprocal delay does not by itself supply all spacetime metric components.

## Concrete coupling requirements

1. A shared geometric edge interpretation must be invariant under changing
   endpoint descriptions, while retaining all state inside the counted node
   channels. Node addresses and face labels supply topology, not distances.
2. The transported field and retained apparatus must follow the same inferred
   metric. A source must affect the geometric variables, with reciprocal
   stress/energy accounting and constraint preservation. The successful
   homogeneous phase sector does not establish this source response.
3. Directional tidal or shear data must be represented and propagate, with
   a compatible local connection. A synchronized scalar gear phase supplies
   neither the two tensor polarizations nor a curvature measurement.
4. Emission, reflection and reception must leave distinguishable retained
   records and be read through clicks. The observable target is the proper
   interval of the emitting observer between emission and reception, compared
   between arms. Changing an arbitrary coordinate length is not this test.
5. Check the declared same-law preparation against independent null and
   timelike predictions, including spatial refinement, source constraints
   and changes of coordinate description. Do not combine a phase-tensor
   success with a different detector-tensor success into one certificate.

Current main also contains `universe24/detection.py`: its internally armed
light-to-memory exchange is a useful retained-record precursor. It explicitly
does not establish a material proper clock, recoil stress or Einstein
backreaction, and it is a different tensor from the phase-gated transport.

The audit marks the identification of the homogeneous scalar gate with a
plus-polarized gravitational wave as **failed**. It marks an actual
source-coupled Einstein calculation, a retained proper-time interferometer,
and general wave response for other preparations as **not_tested**. General
physical event-geometry acceptance remains **blocked**. No quantitative
calibration between the passive reference and the arithmetic clicks is
asserted.

## Primary references and reproduction

The physical measurement boundary follows the proper-time treatment of
[Lee and Zurek, Physical Review D 111, 124037 (2025)](https://arxiv.org/abs/2408.03363).
The distinction between coordinate descriptions and the invariant flight
observable, including finite-wavelength effects, is also developed by
[Blaut, Classical and Quantum Gravity (2019)](https://arxiv.org/abs/1901.09956).
The specific sinusoidal reference and exact face-norm counterexample above
are explicit calculations in this audit, not results inferred from the
Universe24 dynamics.

```bash
python -m validation.geodesic_link_audit \
  --runs runs/light-link-resonance-20261113-v2 \
  --out runs/new-geodesic-link-audit
```

Run directories must be fresh. The command replays the two supplied canonical
runs, saves their identifiers and click-file hashes, freezes its source hashes,
and writes `geodesics.json` without mutating the input evidence.

The completed local collection is
`runs/geodesic-link-audit-20261113/geodesics.json`. Both 64-update canonical
runs replay under the current merged core; all 64 pairs of local histograms
agree. Analytic versus midpoint reference error is below `2.76e-11`.
This is an audit of existing histories, not an additional 128 newly evolved
steps and not a successful physical gravitational-wave run.
