# Gauge and spatial-link integration review

The gauge additions are suitable as source-only controls inside the existing
Universe24 execution system. They do not supply a combined propagating field,
spatial Einstein source, detector or recurrent-growth universe. No code defect
requiring correction was found in this focused review.

The reviewed integration base is `a94dff2fd2343c15ff2d0f7f4f7a4287fa4ff7c6`.
The new central collector was still under final integration, so this review
does not claim its full run or the entire repository suite passed.

## Executed evidence

`python -m unittest universe24.tests.test_gauge_loop -v` passed all 19 tests.
This includes independent expanded scalar oracles, signed large integers,
all legal carries, full-state gauge covariance, inverse/replay, the saved
collector, malformed preparation rejection, changed trace bytes with a
recomputed file hash, and retained physical counterexamples. The tests used
fresh temporary output and did not replace committed evidence.

A separate 60-update experiment on an L=5 prepared dynamic sign sector changed
one charged component in the complete preparation. Every difference throughout
the run remained at node zero in the same edge triplet, channels 1, 2 and 3.
This independently confirms the documented absence of successive-edge
transport of evolving information. Changing the passive plaquette is not a
propagation test.

| Construction | Channels | Terms | Degree | Strict support violations |
| --- | ---: | ---: | ---: | ---: |
| Static Z4 interference | 7 | 22 | 2 | 0 |
| Dynamic Z2 edge exchange | 10 | 19 | 2 | 0 |
| Local carrier-record source chart, comparison only | 12 | 80 | 3 | 0 |

The respective tensor fingerprints are:

- Static: `137127058fd2ca21227af88b45b0b2991bf4fb68abbeb82d95e131f99723b7c2`.
- Dynamic: `fecff94d212980372d34d67a377cee316e2a46884227477bbcb7ae314f98894e`.
- Local source: `109a254ecfe53a42785a9a5a545b2eee928c4857402e38a41bf39c388dc6b5cd`.

## Exact scope

Each construction uses the same production Engine and all retained `(a,b,r)`
triples. Link endpoint support is included in the locality checks. Multi-edge
Wilson loops are passive readouts and never enter an update monomial.

The static law has four-port matter transport and a neutral intensity reader.
Its links stay Gaussian units only on the declared equal-history preparation.
Its full-state local Z4 action transforms both histories and sends a negated
component's carry to `5-r`. The observed intensities four and zero are exact
two-path results. They are neither normalized probabilities nor calibrated
binary detector outcomes. The reader has no reciprocal influence. The
homogeneous matter recurrence gives `1,3,11,41`; the unstable root is
`2+sqrt(3)`.

The dynamic law prepares `a=F^-1(b)` for
`F(chi,eta,U)=(eta,U*Y,chi*Y)` with a retained stationary neighboring sign `Y`.
The tuple `(chi,eta,U*Y)` cycles, proving `F^3=id`. Compiling
`u=3(F+F^-1)` therefore preserves this full prepared sector and every carry.
Charged registers affect links and links affect another charged register,
but all evolving information remains inside each edge triplet. A
state-defined complexity cannot increase strictly indefinitely on this
period-three sector. Covariance on arbitrary integer states is stronger
than, and distinct from, this restricted normalized-link theorem.

The historical countercontrols remain necessary: normalized two-history
complex links can drift to norm squared five; bare charge changes while the
carry-aware identity still holds; an old 20-channel loop tensor violates
strict support; raw charged C1/C2 labels can exchange under a local gauge
transformation. None of these counterexamples is silently removed by the
new finite-group constructions.

## Integration decision and remaining research

Integrate the controls and their exact scope in the single acceptance command.
Keep separate run and tensor identities. The central collector must reject a
join of static-wave evidence, dynamic-link evidence and local-source evidence.
The code now has an explicit such rejection; its complete run is a separate
coordinator validation obligation.

A direct sum would fit the channel budget but would remain disconnected.
Adding arbitrary cross terms would invalidate the existing domain, covariance
and source proofs. No validated coupling currently transfers the gauge energy
or momentum into the twelve-channel chart, and no shared operational metric
or retained calibrated detector is supplied.

Further research requires one bounded propagating reciprocal wave/link law,
electric/Gauss and energy-stress accounts, controlled physical limits, and a
source-and-detector coupling proven on the same complete state. Repeated bangs
and structural growth require additional same-law evidence. These remain
research requirements after software integration and issue closure.

## Reviewed source hashes

| File | SHA256 |
| --- | --- |
| `validation/gauge_loop/model.py` | `fec256835d21a21afd048b3ffaf8fd5d71bfb3afcc06b7d71a163106d681e216` |
| `validation/gauge_loop/dynamic.py` | `f66854c898dee3c85c005069ee0d256d6ea8e2aa8862b5410e0e4347d19a958b` |
| `validation/gauge_loop/audit.py` | `9e8d1b53325a939ab5cbac2260a017d41db36970344de407a88e37949e2d108f` |
| `validation/gauge_loop/obstructions.py` | `addf35606fff5d873cacd78fdeeefa58e0a70c60c83f283bd01a6d03613013bf` |
| `universe24/tests/test_gauge_loop.py` | `d99bdf86af81b4ce3d6cfb8331ed767b7b1e2d47719c2e09ee2d0099d84dad6e` |
