# Independent integration review

The reviewed base is `43b63f2`, which combines the earlier link-phase audit
with main's retained light-to-memory detector. This review also covers the
new node views, installed click-only observer and CLI, four source-only
collectors and historical-work archive.
It is independent of their builders: the checks below inspect storage and
polynomial structure directly, inspect saved collector results, and evaluate
the analytic reference separately. Full-suite and final merged-head checks
belong to the integrating maintainer's receipt.

## Disposition

The changes are suitable as passive node/observer interfaces, reproducible
research audits and preserved historical work. They do not supply one accepted law
that combines delayed light, a physical detector, ordinary matter, dark
matter and Einstein gravity. Promoting that physical claim would contradict
the recorded counterexamples.

No new Engine, hidden retained link bank, runtime metric controller or
research admission exemption was found. The working phase law and native
detector law remain different tensors. The attempted common tensor is
explicitly tested and fails its prepared physical domains.

| Requirement | Review result | Evidence and limit |
| --- | --- | --- |
| Six internal face views | Passed as an API/storage contract | Each view selects eight of the existing 48 channels; all 144 retained integers are covered once |
| One adjacency identity from both endpoints | Passed topologically | `EdgeRef` agrees across opposite ports and periodic seams; it holds no physical length or transit history |
| A single shared dynamical edge length | Not established | Endpoint port values may differ; equality of an edge identifier is not equality of a physical state |
| Exact homogeneous delayed light | Passed on the declared preparation | Phase tensor has 384 degree-at-most-three terms; the matched predecessor gives alternating move/hold transport |
| General directional interactions in the phase law | Failed as a claim about this law | Its channel dependency graph has 24 disconnected central-pair components; each has only its axial spatial offsets |
| Optical backreaction on the phase clock | Failed for this phase law | Pair subtraction removes every pair-sum variable from the contrast recurrence |
| Click-only calibrated memory readout | Passed in the declared sector | Inferred memory changes and accounts match the independent native detector audit, including release and no-light/unarmed controls |
| Unique hidden state from arbitrary clicks | Failed | Distinct stationary seeds have identical empty streams; different retained carries have identical nonempty observational payloads |
| Ordinary matter or dark matter identified | Blocked | Electromagnetic cancellation and internal clicks do not establish rest mass, stress, clustering or a particle classifier |
| Phase clock plus detector under one tested law | Failed for the tested composition | The 912-term common candidate leaves both component preparation sectors and produces negative values |
| Six edge lengths determine an Einstein metric | Failed | Equal six axial norms admit different spatial shear; lapse, shift and operational time are also not supplied |
| Gravitational-wave event geometry | Blocked | The independent TT target is a passive reference; the runs do not contain a calibrated proper-clock reflection experiment |

## Independent structural checks

The native flat-light polynomial has 48 separate single-channel dependency
components. The phase polynomial has 24 components of two central partners.
The native detector polynomial's channel graph is connected across all 48
labels. These facts were obtained by constructing an undirected dependency
graph from every monomial target and factor; a connected graph alone still
does not establish gravity or a successful joint physical sector.

For the phase law, let `p=b_g+b_bar` and `q=b_g-b_bar`. Subtraction gives

\[
q_{t+1}=-q_{t-1}-q_t+q_t(x+n_g)
        +q_t(x)^2[q_t(x-n_g)-q_t(x+n_g)].
\]

There is no `p` on the right-hand side. Thus changing the optical pair sum
cannot source the contrast in this law. This is stronger than merely not
having tested backreaction. It does not rule out a different admissible
coupling or a different physical interpretation.

The new node views retain references to the supplied complete `State` and
static indices. They add no evolving amplitudes, histories or buffers. Their
derived values are Python-integer tuples, and a view does not automatically
follow a subsequent Engine state. Independent enumeration verified port
reciprocity on every edge of a `3^3` cube. These are diagnostic views of
hidden state; they must not be presented as the operational observer's input.

## Observer boundary

The observation functions consume only the saved canonical click stream.
The harness separately uses complete-state replay to certify provenance and
compare predictions; it does not pass those histories into the click-only
inference or feed its results into evolution.

Memory reconstruction has explicit calibration: the detector law, memory
channel, node address set, complete horizon, zero initial memory histories,
nonnegative amplitudes and constant carries. On that domain, a click gives
`M_t=Q_t-M_(t-2)`. On a quiet tick, either the triple is stationary or the
quotient vanishes. The known histories and nonnegativity make the alternatives
unambiguous. This includes a possible release with zero quotient and no
arithmetic click. It is not a general inverse of arbitrary latent state.

`run_id` and `event_id` are explicitly separated provenance in cross-run
comparisons. Quotients and all other recorded fields are retained. Nonempty
cross-run records are not claimed byte-identical when their IDs differ.
Recorded node coordinates are addresses, and update indices are not proper
time. An observer cannot establish completeness from an empty file alone.

A robustness issue found in review was corrected: concatenated records from
different runs can each be syntactically valid yet collide at the same memory
`(step,node)` key. The installed `universe24/observer.py` now rejects mixed
run/tensor provenance, duplicate keys, reordered records, duplicate JSON
fields and inconsistent signs. Exact decimal-string output handles retained
integers beyond Python's default digit conversion limit without changing that
global limit. The eight dedicated input/output contract tests cover these
cases and calibrated quiet-tick reconstruction; they do not claim new physics.

The new `observe-clicks` CLI accepts a standalone click file and optional
explicit memory calibration. Its two boundary tests patch complete-run replay
and bundle loading to raise exceptions, proving those paths are unnecessary
for observation. Partial calibration is rejected before opening input.
The CLI adds no callback to evolution and does not replace the complete-state
`detect` validation audit. Fresh observer evidence after this fix is collected
separately from the first observer run; older hashes are not rewritten.

## Concrete same-law failure

`runs/detector-clock-integration-20261113/results.json` records the candidate
`T_phase + T_detector - T_light`. It retains exactly 48 channels, has degree
three, passes 2O covariance and one-face support, and passes both independent
input oracles, saved replay, inverse steps and complete rewind.

Nevertheless, on the detector preparation its detector-sector condition
fails at step 1, and `b[14,0]` is `-1` at step 3. On the matched phase
preparation, delay and clock conditions fail at step 1 and `b[0,0]` is `-10`.
The separate eight-step component controls pass. These controls cannot be
combined into a successful common-law certificate.

The registered phase preparation requires nonzero contrast in every one of
24 central pairs, while the native detector preparation permits only its four
role rows. Those declared preparation sectors do not overlap. This is a
specific encoding/composition obstacle, not a theorem against all possible
48-channel couplings.

The same-phase-law matter audit separately finds negative retained entries
at step 3 under a localized contrast disturbance. Its positive localized
common pulse translates instead of supplying a demonstrated resting massive
object. The report correctly leaves mass/dispersion and gravitational
stress/clustering unestablished.

## Geometry reference and archive checks

The TT round-trip expression was independently evaluated against its
midpoint integral, with maximum discrepancy `2.7585e-11` for the registered
reference panel. This verifies the passive first-order target, not its
realization by the Engine. A homogeneous positive lapse is a change of time
coordinate in flat space; the microscopic `ceil(t/2)` move/hold count even
has plateaus and is not an invertible Lorentzian coordinate chart.

The historical archive contains no importable `.py` files. Its 1,455 tar
members all use relative paths without `..`; the archive is not extracted
into the installed package. Package discovery includes only `universe24*`
and excludes its tests, while the archived Python snapshots end in `.py.txt`.
Historical source, run receipts and omitted bulk-stream hashes are identified
as evidence of their original version, not upgraded current-schema runs.

Before publication of the final integration, register the node API in the
system/agenda documents, freeze the relevant source files, retain fresh
collector hashes, and run the required active unit suite plus generic
forward/replay smoke on the final integrated source. Those checks can certify
the software integration; the blocked physical rows above remain blocked.
