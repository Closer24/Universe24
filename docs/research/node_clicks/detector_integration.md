# A common phase-clock and detector coupling: explicit composition check

This audit asks whether the two currently successful restricted mechanisms
already form one 48-channel system: matched-phase delayed light transport
and retained light-to-memory exchange. It does not join their separate
successful runs into a combined physical claim.

Source: `validation/detector_clock_integration.py`.

## The registered common candidate

Let `T_P` be the 384-term cubic phase law in
`validation/light_link_resonance.py`, `T_D` the installed 624-term quadratic
detector law, and `T_L` the installed 96-term free light law. The natural
substitution attempt is

\[
T_C=T_P+(T_D-T_L).
\]

This replaces the detector's free light input with the phase-gated input,
while keeping the detector's selector and exchange interactions. It is one
fixed tensor using the same 48 channels, rather than concatenated state
banks. After combining monomials it contains 912 terms, has degree three,
uses at most one face edge per monomial, and passes exact
`2O-left-regular-cube/1` covariance.

The existing Engine advances all states. No clocks are externally updated,
no amplitudes are clipped, and the division rule and retained carries are
unchanged. `NodeView` groups each state into six internal face views; both
endpoints reference the same adjacency without creating a second edge state.
That topology check supplies no physical length or proper-time measurement.

## The preparation sectors are not interchangeable

The matched-phase preparation has contrast `q_g=b_g-b_-g=+/-1` in every one
of the 24 central pairs. Therefore each pair has at least one occupied
channel row: at least 24 rows are nonzero somewhere in the current bank.

The installed detector's declared sector permits only four role rows:
light, memory, arming and selector. All other rows must be zero. Its selector
is uniformly one and arming occupancy is Boolean.

These two declared preparation sectors have empty intersection at the
registered initial phase. Combining their tensors does not supply a new
common invariant preparation. Adding the phase background to the detector
also changes its selector and arming state, so it is not a harmless clock
offset.

This is a statement about these particular prepared sectors. It is not an
impossibility theorem for every 48-channel clock/detector encoding.

## Four registered finite runs

All cases use `L=5`. The detector preparation has light at coordinate 0,
arming at coordinate 3, root label 0 and unit amplitude. The phase preparation
has the existing matched predecessor, bias 1, and unit binomial amplitude.

| Case | Tensor | Preparation | Updates | Required diagnostic |
| --- | --- | --- | --- | --- |
| Detector control | `T_D` | Installed detector | 8 | Exact capture, retained memory, release, conserved role account |
| Phase control | `T_P` | Matched phase | 8 | Exact alternating move/hold field translation and natural values |
| Composition on detector seed | `T_C` | Installed detector | 4 | Whether detector sector and natural values survive |
| Composition on phase seed | `T_C` | Matched phase | 3 | Whether clock sector, delay and natural values survive |

Every saved update is compared against both an independent grouped-input
formula and the independent scalar monomial evaluator. Every complete step
is inverted and the final state is fully rewound. Forward replay and exact
source hashes are checked. Physical diagnostics cannot feed the Engine.

The saved samples include the first negative retained value, the first loss
of each preparation invariant, role-memory amplitude, and the passive
delayed-field comparison. The role quadratic account outside the detector
sector is only a diagnostic; it is not asserted to be conserved energy.

The installed detector's full-state interpretation is used here solely as
an independent validator. It is not offered as the click-only observer;
that observer is examined separately in `observer.md`.

## What the failure requires fixing

The common tensor is algebraically admitted, but it does not retain both
component invariants. Its phase terms act on the same rows that the detector
uses as Boolean selectors, arming fields and memory. The detector terms also
act on the rows that carry the central contrast. Those interactions cannot
be inferred to preserve either sector simply because each component does so
under its own law.

Another tempting construction, multiplying the detector's quadratic
exchange `arming*amplitude` by the existing quadratic phase gate `q^2`,
produces a degree-four monomial. It violates the current degree-three budget
before any simulation is run. An admissible future construction needs a
single invariant preparation and a jointly derived reversible map, with
counted clock, selector and memory roles and a compatible inverse within
the locality and polynomial-degree limits. A linear Boolean timing field
could avoid that particular degree-four product, but its invariant encoding
within the same regular 48 channels remains to be established.

Memory capture is a retained amplitude transfer with a dimensionless
quadratic account. It does not establish massive matter, a proper material
clock, recoil, gravitational source stress or dark matter. Neither successful
component supplies Einstein geodesics or gravitational waves by itself.

## Reproduction

```bash
python -m validation.detector_clock_integration --out runs/new-detector-clock-integration
```

Fresh evidence is saved in
`runs/detector-clock-integration-20261113/results.json`. The report distinguishes
passed mechanics and component controls from failed naive composition,
blocked common-coupling acceptance, and untested material/Einstein physics.

The completed four-run panel contains **23 forward updates**, all with exact
grouped and scalar oracle agreement, replay and rewind. Results:

- The detector control records 25 captures, 25 releases and 150 no-transfer
  opportunities. Its light-plus-memory account remains exactly 25 at every
  saved step; the maximum retained bit length is 3.
- The phase control preserves its matched clock sector and exact delayed
  fields through all eight steps, with nonnegative integers and at most
  4 bits. Its separately computed detector-role account is not conserved;
  that account is not an energy invariant of the phase law.
- The common candidate on the detector seed leaves the detector sector at
  step 1 and first produces a negative retained value at step 3
  (`b[14,0]=-1`).
- The common candidate on the phase seed loses the phase sector and exact
  field delay at step 1, when `b[0,0]=-10`. It reaches 25 bits within the
  registered three-step horizon.

The failed fields are retained in full. There is no clipping, discarded
trial, or substitution of a separately successful law after the failure.
