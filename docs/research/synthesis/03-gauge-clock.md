# Projective carrier, gauge transport and clock handoff

Research base: PR47 `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
Scope: exact algebra and actual small Engine runs. This does not replace the
active old-law apparatus work on issue45, or establish an operational clock.

## Denominator-aware interface

Write the current complex carrier as `z_x=(P_phi,x+i P_chi,x)/D`, on PR47's
proved uniform positive-denominator domain. The existing sign-phase reader
cannot decode this law. Define `N_xy=|P_x+P_y|^2` on one face. An appended
audit receiver with `u=3 N_xy` obeys

```
ell = receiver.b_after + receiver.a_before = N_xy
r_after = r_before
I_xy = ell / D_before^2.
```

The passive division is necessary: the quotient itself is an encoding-scale
dependent integer. Using `D_after` yields a different physical quantity.
Even the correct weight is not a binary detector frequency or proper time.
This bridge reads full before/after states: it is not a click-only reconstruction
of the denominator. A records-only receiver protocol needs a separately declared
scale certificate; absence of a receiver event still cannot establish zero intensity.

The new script appends one such receiver to the actual protected projective44
source, creating 45 channels. This is a one-way fixed-gauge test apparatus,
not a changed physical law or reciprocal matter stress. Three steps on 27
nodes preserve every original 44-channel register exactly relative to the
unmodified source run. All 81 receiver transitions match an independent
rational coherent-intensity calculation, all six carries are covered, and the
complete state rewinds. Using the after-snapshot denominator fails 80 nonzero
readouts. Largest retained integers after the three updates: 23, 70, 214 bits.
The heterogeneous scalar preparation is off Einstein constraints.

## Gauge-covariant algebra that fits the cubic edge rule

The bare overlap changes under independent local phase rotations. For
`z_x=z_y=1`, rotating only `z_y` to `i` changes coherent intensity 4 to 2.
For a normalized link `U_xy`, the transported expression
`|z_x+U_xy z_y|^2` is invariant under
`z_x -> g_x z_x`, `z_y -> g_y z_y`,
`U_xy -> g_x U_xy conjugate(g_y)`.
This is an algebra identity, not a claim that PR47's full source dynamics is
exactly gauge covariant. 10,000 signed/rational examples verify the identity
and common-rotation invariance, including zero carriers.

Let `U=(L_r+i L_i)/D`, with the extra invariant
`L_r^2+L_i^2=D^2`. Define `C=P_phi,x P_phi,y+P_chi,x P_chi,y`
and `S=P_phi,x P_chi,y-P_chi,x P_phi,y`. Then

```
N_transport = D (|P_x|^2+|P_y|^2) + 2 (L_r C-L_i S)
I_transport = N_transport / D^3.
```

Every numerator monomial is cubic and supported on one physical face edge.
A standalone six-channel static prepared-link control executes this exact
numerator in the real Engine: 27 nodes, all carries, strict support and exact
inverse pass. It uses `D=5`, link numerators `(3,4)` and `u=6b` for stationary
source/link channels. This is not a dynamical gauge field or a second product
runtime. Direct Euler rotation of a unit link by a step 1/4 has norm squared
17/16, so normalization does not follow from calling the link a phase.

## Allocation and the next constructive target

| Construction | Total channels | What is missing |
| --- | ---: | --- |
| Projective44 plus two link components on one axis plus one receiver |47| Dynamical normalized link, reciprocal coupling |
| Projective44 plus two link components on each of three axes plus one receiver |51| Exceeds48; reject this direct append |
| Replace existing three frame potentials A with six link components; one receiver |48| Complete rederivation of the source/gauge law |

The last row is a feasible arithmetic ledger, **not an implemented encoding**.
Existing `A0,A1,A2` are spatial frame potentials, not unitary links; their
Maxwell, covariant-gradient and stress equations cannot be silently reused.
An aggregate receiver can sum three face numerators while each monomial
remains on one face. Direction-resolved retained receivers would cost more.
The 51 count is not a universal lower bound: alternate encodings or proven
reuse may exist.

Before allocating new channels, derive a reversible polynomial link update
that preserves normalization and a discrete Gauss identity, then rederive
charged-current/stress coupling. Standard plaquette products touch multiple
edges and generally require staging not present in this ledger. No hidden
workspace, runtime rational normalization or implicit solve is allowed.
A Cayley phase `(1-t^2+2it)/(1+t^2)` is exact but rational; clearing its
denominator and proving a complete reversible update remain additional work.

## Clock criterion and literature boundary

[Ipp and Müller (2018), sections 3–4, equations 48–50 and 100–105](https://doi.org/10.1140/epjc/s10052-018-6323-x)
provide a primary lattice-gauge example connecting link transformations,
discrete gauge symmetry and Gauss conservation. Their variational implicit
schemes are not automatically permitted Universe24 updates; their link and
plaquette formulas identify concrete algebra and locality obligations.

[Rovelli (2002), sections II–III and V](https://arxiv.org/pdf/gr-qc/0110035)
distinguishes clock readings from predicted relations between readings,
including satellite/base comparisons. This motivates a falsifiable apparatus
test rather than identification of update number with clock time.

Our exact flat-metric control has a coordinate interval 1 and velocity 3/5:
rest proper interval 1, moving proper interval 4/5. Equal imposed coordinate
phase increments would fail this comparison. This is a kinematic reference,
not a simulated material clock. PR47's comoving lapse-one `n*h` is a geometric
time label; a carrier frequency must independently reproduce moving/rest
proper-time ratios, signal transport and backreaction before clock acceptance.
Neither source paper proves that this project meets those requirements.

## Reproduction and status

```
python -m validation.synthesis.gauge_clock_bridge --out runs/synthesis/gauge_clock_bridge.json
```

JSON records the source pin, source/audit hashes, command, exact control
counts, observed bit lengths and scoped limits. Passed: passive scale bridge,
restricted transport identity and mechanical inverse. Not tested/established:
full gauge covariance, dynamical unitary links, reciprocal apparatus stress,
proper-clock calibration, Born/Bell or complexity selection.
