# Signal input to an initially resting clock site

Status: 36 registered runs completed and independently replayed.
No registered quiet oscillator was created. This is a bounded negative result
for nine preparations tested on two cube sizes, not a general impossibility
claim about Rule3.

## Question and fixed preparation

The earlier successful writer–probe gates contain clocks that already
oscillate before the signal arrives. This study instead starts all 336 counter
pairs on a designated clock node and its six neighboring nodes at zero. A
single exact +X carrier then encounters the channel-2 center one site above
its guide. The tensor stays +++ and no runtime action changes the state.

The center remainder is 0, 2 or 4. Five non-guide halo recipients all start
with a common remainder of 0, 2 or 4; the guide-facing recipient retains its
required remainder 0 and the companion channel retains remainder 4. All
other regional triples are background. Each of the nine settings has a
complete-source-present and complete-source-absent preparation on sides 225
and 257. Absence restores the complete 24-address source footprint, not only
its counters.

The horizon is 80 updates. Exact incoming templates are checked before
contact. Acceptance requires a native first center activation with nonzero
input and arithmetic C, followed by a quiet protected orbit throughout
states 64–80. Every regional triple must repeat after four updates; only the
center may have nonzero counters, with `0 < |a|+|b| <= 2`; its remainder must
be constant and even. Every individual external contribution must vanish.
Unit, axis-amplitude-two and diagonal clocks are reported separately.

## Recorded outcome

All 36 complete recordings, source-equivalence checks and full inverses pass.
All 18 source-absent boards remain stationary. Every incoming-template control
is valid. No run was cut short, no record failed, and no captured native state
was left unobserved. The independent audit verified 2,916 full states and
2,880 transitions and inverses, every native checkpoint, first-activation and
hold observation, all pair decisions and the whole-workflow resource receipt.

The following outcomes occur on both registered cube sizes:

| Initial center remainder | Five other halo remainders | First center activation | Late states 64–80 |
|---|---|---|---|
| 0 | 0 | Native C2 at update 16 | Returns to rest |
| 0 | 2 | Native C2 at update 16 | Returns to rest |
| 0 | 4 | Native C2 at update 16 | Nonquiet, driven activity; every registered quiet-orbit condition fails |
| 2 | 0, 2 or 4 | None | Center remains at rest |
| 4 | 0, 2 or 4 | None | Center remains at rest |

In the six source-on runs with center remainder 0, actual input `u=-1` produces
`(a,b,r)=(0,0,0) -> (0,-1,4)` at update 16, with native C2 and quotient −1.
That is a real signal-caused transient activation. It is not the requested
persistent quiet clock. With halo remainder 0 or 2, the complete 336-triple
region later matches its stationary source-off counterpart. Information about
the signal is retained in the full reversible board, not certified as a local
clock record.

The registered result is **0/18 accepted source-on/off comparisons**, with
**0/9 settings** accepted on both sizes. The accepted class counts are unit 0,
axis-amplitude-two 0 and diagonal 0. A counter pair that happens to equal an
oscillator state at one instant does not meet the full-region, input-isolation
and persistence criteria.

## Evidence and resource accounting

All executable sources and the exact protocol were archived before capture.
Native full recordings were saved atomically before scientific observation;
complete case records and interruption handling preserve incomplete outcomes.
The independent initialization check reconstructed all 36 preparations and
all full source masks before execution.

The dedicated outer wrapper measured **67.78 seconds of whole-workflow CPU**
and **67.70 seconds of wall time**, including imports, preflight, capture,
inverses, observations, compression, Presenter serialization and archive
hashing. Recorded size before the final receipt was 25,284,097 bytes. The
180-CPU-second, 300-wall-second and 64-MiB limits all passed. All 18 selected
side-225 examples, including every matched source-off control, were exported
in nine complete two-experiment bundles.

- Protocol: [protocol_activation.json](protocol_activation.json)
- Complete results: [activation_v1/result.json](evidence/activation_v1/result.json)
- Initial independent check: [activation_preflight.json](evidence/independent_audit/activation_preflight.json)
- Independent full replay: [activation_v1.json](evidence/independent_audit/activation_v1.json)
- Whole-workflow receipt: [outer_budget.json](evidence/activation_v1/outer_budget.json)
- Native capture archive: [native_captures](evidence/activation_v1/native_captures)
- Presenter selection: [presenter_selection.json](evidence/activation_v1/presenter_selection.json)

## Separate post-capture multi-node check

After these trajectories were captured, an explicitly exploratory definition
was recorded before inspecting larger regions in the two center-0/halo-4
source-on cases. It fixed centered cubes of radii 1, 2 and 3, every channel at
every node, states 32–80 and candidate periods 1–16 with at least three complete
periods. Every state had to retain nonzero internal counters, and every
individual external term had to vanish across the full cubic boundary.

All **96** declared region/period tests fail. All six regions contain activity
throughout the window, but none repeats exactly at any tested period. External
terms are nonzero during 48, 42 and 29 of the 48 updates for radii 1, 2 and 3,
respectively, on both cube sizes. The analysis performed no forward or inverse
updates. It neither found a bounded multi-node clock candidate in these
windows nor changed the original activation verdict. Longer periods, larger
regions and different preparations remain outside this analysis.

- Exploratory definition: [protocol_activation_multinode_analysis.json](protocol_activation_multinode_analysis.json)
- Complete exploratory outcomes: [result.json](evidence/activation_multinode_exploration/result.json)

## Decision

Keep the already demonstrated prepared-clock phase gates separate from this
failed activation target. A possible later preparation-only study could vary
the five halo remainders independently instead of forcing them to be uniform,
with a new frozen protocol and the same unchanged Rule3. This result does not
justify adding a clock-creation rule or treating ongoing driven activity as a
quiet memory. No additional experiment is authorized by this suggestion.
