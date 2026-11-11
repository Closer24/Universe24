# Independent acceptance of the local complexity mechanisms

Production baseline: `7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`.
The isolated complexity work follows local snapshot `1e22b18`. No production
law changed. `experiments/cosmology/PROTOCOL.md` remains the acceptance rule;
`experiments/complexity/PROTOCOL.md` adds subgoals without weakening it.

**Result:** useful local mechanisms pass bounded causal tests. No candidate
passes the complete recurrent-complexity goal, and none derives Born sampling
or natural Bell statistics. The strongest demonstrated connection is retained
local information changing later messages and their concentration under a
fixed reversible law. A separately declared follow-up now joins the equality
sensor to the rotor and passes that narrow causal chain. It does not yet make
an integrated structural-stagnation-driven growing universe.

## What this reviewer actually executed

The read-only checker is `experiments/complexity/acceptance_audit.py`.
It recomputes the frozen structural diagnostics without calling the original
structural observer. It reconstructs exported laws with strict support,
re-executes their complete initial states, compares complete final states
and exported traces where available, and runs the full inverse. It uses the
existing Engine; it is not a separate scalar implementation of that Engine.

| Evidence | Independently executed scope |
| --- | --- |
| Adversarial controls | Four fresh baseline/periodic/scaled/no-message runs, replayed; a numerical counter; a visible-memory projection; noise/static-random diagnostics; C2 selection control |
| Local equality sensor | Five tensors/seeds, 40 updates each, all 205 saved complete snapshots; direct equality/input check, disconnected/label-swap controls and complete-state cones |
| Motif memory | 22 primary complete seeds/finals, 1,740 updates including the stopped off-domain case, plus four separately declared Boolean-encoding follow-ups of 80 updates each; matched local signal/history and read-disconnection checks; one-bit intervention cone |
| Reassembly rotor | Nine complete seeds/finals from `03-reassembly/verified/`, 1,440 updates; independently recomputed concentration, cycle times and original structure metrics; connected/disconnected memory interventions and cones |
| Organization across cycles | 18 cases, 540 updates and every exported full snapshot; all three sizes' no-read comparisons and cycle-3/cycle-6 primitive memory shapes |
| Additional organization interventions | Three same-law memory-only intervention pairs, 30 total updates; all saved full snapshots, final states, inverse, unchanged carrier histories and causal cones |
| Phase/Born comparison | Reconstructed all 83 branches and all 13 probability grids of 6,864 eligible pairs; independently checked 498 scalar quotient/readout calibrations |
| Separately declared sensor/rotor follow-up | 16 cases, 1,280 updates and all 1,296 complete snapshots; independent Boolean forward-map comparisons, matched history/disconnection controls, source independence, complete-state cones and original structural metrics |

Audit sequence correction: the initial peer scan executed the 22 primary
memory cases. My first peer-review comment prematurely counted the four
Boolean follow-ups, whose metadata lives in the aggregate report instead of
per-case reports. The scanner was corrected and all four were then actually
executed and rewound. The final peer report contains 26 memory cases and 2,060
updates, including independent a/b encoding comparisons and all other
a,b,r triples at every tick. The additional four are not silently treated as
part of the earlier 22-case execution.

For the phase experiment, the other agent's 498 Engine orbit/inverse checks
were source-inspected and their exported readouts independently checked; this
reviewer did not rerun those Engine orbits. That distinction is retained in
the machine-readable result. No full test-suite success from another PR is
counted as evidence that these new mechanisms meet a physics gate.

## Unchanged acceptance assertions

1. Detect compactness from the declared **reference** amplitudes, excluding
   message lanes. Require concentration of at least 3/4 in one face ball,
   then dispersal strictly below 1/2, before a new compact episode counts.
   The first compact episode is preparation. Require at least four later
   reassemblies. A channel named `ref` is not automatically the original
   physical/reference subsystem; the new rotor retains a message-density
   proxy, whose limited meaning must stay explicit.
2. At every successive reassembly, the original site-sign, edge-sign and
   three-observation persistence vector must be componentwise nondecreasing,
   with at least one strict increase each time and nonzero persistence.
   Multiplying all amplitudes cannot satisfy this requirement. Full-state
   recurrence rules out strict growth of a single-valued state score on that
   same return.
3. A fixed-law initial-history intervention must change later communication,
   with differences inside the cone of the **complete** changed initial
   footprint. A matched disconnected control must remove the relevant effect.
   The feedback must also change later reference reassembly, not just a
   message value. A separate matched test must attribute triggering to lack
   of structural development. Equality of two local samples alone is weaker.
4. Rewind every retained a,b,r register through every completed update.
   Resource stops occur after complete steps; no clipped counters, reseeding,
   observation-driven coefficients or hidden branch selection is accepted.
5. To call a new statistic useful organization, fix its definition and
   parameters before the candidate runs and test predictive or intervention
   utility on held-out cases, including shuffled/noisy controls. Do not replace
   a failed original metric after seeing the results. Raw diversity and even
   persistence are necessary diagnostics in some constructions, not sufficient
   definitions of useful physical complexity.

The checker records `pass`, `fail` and `unknown` separately. Missing causal,
organization or quantum evidence stays unknown and cannot yield success.
An observed failure at the declared horizon remains a failure for that test;
it is not a proof against all longer runs or different fixed laws.

## Adversarial controls

The L=7 periodic shell produces ten actual reassemblies at updates
6,13,20,27,34,41,48,55,62,69. Every vector is (6,6,0), so recurrence passes
and cumulative structure fails. Doubled amplitude gives identical normalized
fingerprints and the same vectors. The L=5 communication baseline has no
reference reassembly in this fresh 70-update control; no messages also fails.

A genuine fixed-six local counter reaches b=49 from b=1 in 48 updates,
raising its bit length from 1 to 6. Its normalized spatial fingerprint is
unchanged and it never disperses: no structural growth or new burst.
Independent random 16-component sign fields attain 125 site-pattern types
but zero three-sample persistence. A fixed random field attains 125 persistent
types but supplies neither growth nor demonstrated predictive organization.
These last two are explicitly measurement-only controls, not Engine models.

Under the zero-input law, (a,b,r)=(0,1,2) becomes (1,0,2) and rewinds exactly.
The visible b memory is gone, but the complete information is retained.
Conversely, retaining an unused record is not enough: later behavior must
actually depend on it.

The C2 stress control still gives S=3/2 when every emission is included and
S=4 after retaining 2/8 per setting. Selecting favorable classifications or
new patterns does not establish a physical complexity, Born or Bell law.

## Mechanism scoreboard

| Mechanism | Passing subgoal | Failed or unknown obligation |
| --- | --- | --- |
| Boolean local no-change sensor | Same-amplitude history equality changes an alarm and then causal messages; label swap and disconnect controls pass | **Fail** as a general structural-stagnation detector: period-two input stays "changing" without structural growth. Reassembly attribution unknown |
| Motif-parity memory | At old tick 4, identical complete local A/B/probe/receiver/readout but opposite retained bit gives actual readout -1/+1 at tick 5; removing memory read removes the difference | **Fail** as unbounded accumulating memory: the finite parity subsystem recurs. Off-binary global scaling breaks the proof and can trigger a resource stop; whole readout is not proved bounded |
| Boolean rotor | Memory affects messages at update 2 only when routing is connected; later L=5 density concentration episodes change; amplitude remains bounded | **Fail** for original cumulative structure in all nine runs. Its retained density follows message occupancy, not the independent reference physics. Structural-stagnation attribution unknown |
| Three-phase spatial memory | Different memory persists across exact carrier returns and changes later response in some declared interventions; no-read leaves complete memory/carriers identical | **Fail** for sustained growth/feedback: cycle-3 and cycle-6 primitive memory shapes match at all sizes; carriers ignore memory. The L=5 memory intervention produces no response difference within its declared five updates |
| Phase-pair algebra | Signed predeclared phase correlations equal coherent intensity on the declared grid; all exported scalar readouts checked | **Fail** for tested unsigned complexity weights and nontrivial postweighting of a fixed state. The detector follows min(1,q/3), so normalized exclusive Born selection remains absent |

The three organization intervention results are retained without cherry
picking: response differs at ticks [2,3] for L=3, never within the declared
window for L=5, and [3,4,5,6,7] for L=7. Carrier histories remain identical
in all three. This is useful history dependence in a restricted apparatus,
not a proof that more remembered structure monotonically improves function.
Those response differences include the retained a history: the b-only
differences occur at [2] for L=3 and [3,5,7] for L=7. The complete retained
record is the acceptance object, not only its currently visible b slice.

The phase kernel incorporates a specific harmonic geometry and signed
interference. Its success is conditional on that choice; it does not explain
why a universe prefers that coupling or larger unsigned complexity. A
complexity-dependent physical change of state must be distinguished from
postweighting a fixed state's outcomes. Bell-local factorization and setting
independence remain separate premises, unaffected by calling the shared past
one large clock.

## Reproduction and handoff

First run the five mechanism owners' commands in their reports. Then:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.acceptance_audit --out runs/complexity-research/06-acceptance
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.acceptance_audit --stagnation runs/complexity-research/01-stagnation --out runs/complexity-research/06-acceptance/stagnation-independent
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.acceptance_audit --born runs/complexity-research/05-born/report.json --out runs/complexity-research/06-acceptance/born-independent
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.acceptance_audit --peer-root runs/complexity-research --out runs/complexity-research/06-acceptance/peers-independent
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m experiments.complexity.acceptance_audit --sensor-rotor runs/complexity-research/07-sensor-rotor --out runs/complexity-research/06-acceptance/joint-independent
```

Each final audit output records SHA-256 hashes for the checker, Engine/core,
candidate scripts and protocols under `auditor_provenance`. These are the
files present at actual execution, not an assertion that a later modified
source generated an older output.

## Separately declared sensor/rotor follow-up

The follow-up was declared in issue comment 6802247405 before execution.
Its 31-gear degree-three law retains the sensor domain and controls the
reversible local rotor through the retained alarm. All 16 complete exported
trajectories and inverses replayed, and the Boolean forward map was checked
independently at each step. Messages and retained memory stay binary; the
retained density equals their occupancy sum and stays in 0..2. The former
scalar message wire stays zero. Initial message occupancy stays fixed.

Across all eight matched static/alternating source pairs, local source and
control amplitudes match. Connected pairs first differ in message b at update
2 and retained density b at update 3. Disconnecting the alarm from the rotor
removes both differences. Complete source histories are unaffected by that
disconnection or the memory intervention. Complete differences stay inside
the cone from the complete changed initial support; this was checked for
648 history-pair snapshots and another 648 memory-intervention snapshots.

This establishes a composed **local input history → alarm → scattering →
later density** mechanism within the declared prepared domain. It does not
establish a generic detector of lack of structural progress, independent
reference physics or growing organization. All 16 runs still fail the
unchanged componentwise-growth/persistence criterion. The next decisive
obligation is to connect a structural history feature to the independent
reference subsystem, then pass at least four growing persistent reassemblies
with frozen metrics, held-out organization controls and complete rewind.

Issue discussion: [independent controls and handoff](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802149206).
The [executed peer cross-review](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802346724)
records which artifacts were replayed and the retained negative cases.
The [sensor/rotor result and review request](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802440059)
was checked separately as described above; the initial failed acceptance
criteria were not changed to accommodate its positive subgoal.
The [final independent follow-up and explicit count correction](https://github.com/Closer24/Universe24/issues/17#issuecomment-6802525908)
records the later successful Boolean replays and joint audit.
