# Frozen electric-ray preparation for the electron pilot

This is the pre-orbit source annex to
[the numerical pilot](PROTON_NEUTRON_ELECTRON_CANDIDATE.md). Physics approved this
source before any calibration or orbital world was run. Profile identity and
all orbital thresholds remain unchanged. This table is not retuned to a path.

Enumerate integer triples `(x,y,z)` in lexicographic ascending order, each
component from -16 through 16, retaining exactly
`225 < x*x + y*y + z*z <= 256`. There are **2930** distinct headings. The set is
closed under coordinate permutations and sign reversal; its vector sum is zero.
Authoring and transport use no floating point, root or trigonometric operation.

The SHA256 of the JSON array of these triples, serialized with separators
`(',', ':')`, no indentation, followed by one LF, is
`551f46ab5e5a05916c85ccf5328918dd0ec45f95d7e7f23758a5d3eaaee1bb70`.
The builder regenerates exactly this bounded immutable table and checks the hash.

| Setting | Frozen value |
| --- | --- |
| Transport | Existing plain `ray`, links metric, H=1, no attenuation, phase, claim, bond or self-exclusion |
| Ordered source | Existing source cursor starts at zero; first emission uses headings0 through292 |
| Emission | 293 unit-amplitude rays per source cycle, only from a bound positive constituent |
| Complete sweep | Ten source cycles; cursor advances293 modulo2930 |
| Local ray capacity | 4096 per Node/packet bank; existing overflow rejection stays enabled |
| Electric funding | Explicit external-source ledger; distinct from funded nuclear radiation |
| Calibration world | Open41-cubed, source at center, held nonreacting records; 84 completed model intervals |
| Calibration windows | Event ticks64 through73 and74 through83, ten ticks each |

An open straight ray never revisits a Node. For this stationary source, each
heading can therefore occupy a particular Node at most once at any instant,
so the electric resident-bank count is bounded by2930, below4096. In a41-cubed
box every outward ray exits after at most61 cardinal hops. At293 emissions per
tick this bounds live electric rays by17873. This is a conservative host-size
estimate, not an operation-cost measurement or a promise of runtime.

Read all calibration probes from completed `spatial_received` events. Their
`received_fields` indices are receiver faces; flip index with XOR1 to recover
the travel Port before computing signed flux. Missing receipts in a tick mean
zero newly arrived flux. No host read or computed coefficient feeds back during
the source-only run. Verify identical per-tick flux sequences in the two windows,
then retain the first complete-window mean as an exact integer ratio.

Probe the six radius8 axis points, `(6,6,0)`, `(4,4,4)`, and the positive-X
radius4 and16 points. Use the numerical profile's preregistered symmetry,
tangential and inverse-square acceptance; no extra spatial averaging or fitted
trajectory can replace these readouts. Set the single response coefficient to
`C=64/F8` only after positive repeatable F8 exists. Archive the source checksum,
window traces, exact numerator/denominator, angular verdict and source identity.

If the field gate fails, retain that failure and permit only the specified
single diagnostic main-world GIF under these unchanged parameters. A correction
requires a newly published source/law version before its own experiments.
