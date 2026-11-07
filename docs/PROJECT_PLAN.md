# Universe24 research program: decisions and acceptance gates

Baseline date: 2026-11-07. Source: `ed1556e202eb0f3cc60342c75d44012c2eeb71c3`.
[Claim register](CLAIMS.md) · [source/code comparison](SOURCE_AUDIT.md) ·
[algebra](ALGEBRA_AUDIT_2026-11-07.md) · [independent review](INDEPENDENT_REVIEW_2026-11-07.md) ·
[first experiment](SIGNAL_MEMORY_EXPERIMENT.md) · [physics gates](PHYSICS_GATES.md).

## Objective and candidate boundary

Determine whether observed physics can be derived from one local, discrete,
reversible dynamics. A theorem about this automaton is not an observation of
nature. A successful engineered seed is not evidence of spontaneous emergence.
Negative results have the same evidential standing as successful constructions.

Candidate `U24-P013+++` uses positive body signs `(1,1,1)`; candidate
`U24-P013+-+` uses `(1,-1,1)`. Other sign triples require distinct IDs. The
positive candidate is the engine default and the initial mechanism testbed.
The choice is methodological, not evidence that it is physically preferred.
Every run records the actual tensor fingerprint, not merely the candidate name.

The nonnegotiable contract is one periodic cubic grid, one 48-channel board per
site, six spatial neighbors, exact `(a,b,r)` with `a,b` unbounded integers and
`0 <= r < 6`, and only

    ell, r_next = divmod(2*u + r, 6)
    a_next, b_next = b, ell - a

All outputs read the same old snapshot. Coupling is fixed before initialization.
Preparation optimization is outside evolution. Observers, inverse audits,
symmetry comparisons, scores, clicks and checkpoint tools never write a running
state. No force, gate, latch, reset, path deletion or adaptive coefficient may be
inserted. A structural change gets a new candidate, its own proof and regression
suite; it never silently changes the reference core.

## First publishable research target: a prepared signal–clock–record assembly

`M1-prepared` asks one question: can spatially transmitted activation of a
prepared local counter pattern autonomously write a locally readable record
for at least **32 consecutive reference updates**?

Definitions are fixed in the protocol before simulation:

- **Signal:** a seed-dependent activation front with ordered remote arrivals.
  The source is present only in the initial preparation; later injection is
  forbidden. An activation front need not be a rigidly translating particle.
- **Clock:** an exact local recurrent counter pattern with a declared period
  and phase map, checked for at least eight complete period-four cycles while
  connected to the guide. Local recurrence is distinct from recurrence of the
  whole cube and from an autonomous physical time standard.
- **Memory:** a fixed local function of retained `(a,b,r)` that distinguishes
  the arrived and no-source preparations continuously for the declared window.
  Its storage must remain inside the full evolving state.
- **Click:** a passive local transition of that memory from ready to recorded.
  An external log reports it; the log is neither the memory nor an instruction.
- **Persistence:** at least 32 consecutive post-arrival states; later autonomous
  reset is permitted only if explicitly measured and reported. No claim of
  permanent or irreversible memory follows.

Accept the bounded construction only with exact arrival/readout tests, a
no-source control, complete-state inverse, at least two cube sizes, a held-out
preparation fixed before testing, and explicit boundary and perturbation tests.
Source-only and broken-guide controls distinguish a prepared propagation
mechanism from free propagation. Report every control, including failures.
The artifact includes seeds, frozen protocol, executable runner, results,
initial/final full-state checkpoints, retained-state traces, and source hashes.
An independently repeated run must agree on deterministic fields.

`M1-robust` is a separate extension: success in a declared perturbation family,
phase/input range and component-composition matrix. Do not retrospectively
weaken its criterion after discovering a failure. `S2` separately seeks an exact
finite-support moving pattern `W^T(S)=translate_delta(S)` on the **complete**
state, with `delta != 0` and no torus-circuit artifact. Neither is required to
rename the prepared front as a particle.

## Component interface catalogue

All environments use a declared cube, background, coupling and observation
region. Off-path channels retain their ordinary Rule3 updates. Interface values
are observed patterns, never simulator commands.

| Component | Preparation / environment | Input → output | Latency and operating range | Composition test |
|---|---|---|---|---|
| Local clock | A11 pair g0=(-1,-1,0), g14=(1,1,4), background (0,0,2) | initial phase → phase cycle | exact period 4 in tested isolated preparation; no general phase tolerance yet | nearby pair becomes joint period 5; test phase/distance grid |
| Prepared front | source pair plus finite receiver guide in M1 protocol | initial source present/absent → ordered activation | predicted receiver j arrival t=j; only fixed tested guide family | detector at multiple positions; missing receiver, intersecting guides |
| Local record | prepared receiver g0=(0,0,4), g14=(0,0,0) | front → changed local remainder bit | predicted finite window j <= t < 2(N+1)-j for even N | observe the same local bit while connected to clock and guide |
| Clock influence | two clocks with declared separation/phase | one initial phase choice → second clock trace | not yet a reusable port; scan d=1..8, phases 0..3 | compare isolated and joint full-state evolutions |
| Effective clutch | two initial apparatus states, identical fixed coupling and input family | control preparation + signal → changed transmitted readout | future task; must quote leakage and input interval | require same detector/readout in open/closed preparations; no runtime switch |
| Bound assembly / breakup | two or more prepared motifs and endogenous carrier | encounter → persistent joint structure or separation | future task; declare spatial radius and 64-update survival window | join and breakup must both emerge under uninterrupted forward Rule3 |

A full-state device that blocks arbitrary nonzero net input is excluded by the
algebraic obstruction. A selective **effective** clutch for a bounded input
alphabet remains a legitimate task. Report where the hidden input information
resides whenever a projected signal disappears.

## Work queue and owners

Owners are roles with bounded delegated audits; the project lead signs off on
claims after inspecting evidence or independently rerunning them. These are
compute ceilings, not estimates of completed work or scheduled background jobs.
Any ceiling reached without a result is `inconclusive-budget`, not impossibility.

| ID / owner | One question and deliverable | Compute ceiling | Success | Failure | Continue / decision |
|---|---|---|---|---|---|
| A0 / algebra | Does the implemented map satisfy the contract? Proof notes + exact algebra/dense audit | 120 CPU s, 256 MB | constructive two-sided inverse; zero discrepancies | one valid counterexample | fix implementation only if proof requires it; rerun all affected checks |
| R0 / independent review | Can another execution reproduce baseline claims? Logs + source manifest | 120 CPU s | existing suite/audits and exact reflection report agree | mismatch or unpinned source | isolate mismatch before new claims |
| M1 / computational search | Does A11 yield a 32-update local record? Frozen experiment + checkpoints | 120 CPU s initial, 300 wall s, bounded active-state cap in runner | all declared nominal predicates and controls | missing activation, early loss, inverse mismatch | accept only bounded domain; analyze failed controls |
| M2 / search + review | Is the record robust/composable? Perturbation matrix and retained-state trace | 600 CPU s, <=256 preparations, <=128 updates, <=200k active channels/run | >=95% exact success on prespecified admissible perturbations, all controls pass | lower rate or leakage outside range | restrict demonstrated domain; new protocol version for repair |
| S2 / search | Is there a compact mobile full-state pattern? Exact shift certificate or search log | 600 CPU s, <=4096 seeds, <=64 updates, radius <=4, counters -2..2 | exact translation plus held-out size, no wrapping | no witness in finite class | negative only for searched domain; enlarge one bound at a time |
| C1 / search | Can clocks transmit a declared phase input? Phase/distance transfer table | 300 CPU s, 128 seeds, 64 updates | reproducible causal dependence with functioning output clock | interaction destroys output cycle or depends on wrap | redesign seed, not update law |
| K1 / algebra + search | Can apparatus state selectively suppress a fixed signal alphabet? Transmission/leakage table | 600 CPU s, <=128 paired cases, <=128 updates | open >=90%, closed <=10% detections over fixed ensemble, inverse exact | no separation or hidden runtime control | full-state disconnection is not a fallback target |
| B1 / search | Can a bound motif form and later separate? Two forward trajectories + inverse | 600 CPU s, <=256 seeds, <=128 updates | bounded separation persists >=64 updates; a second prepared input induces breakup | no stable joint structure in class | retain failures; modify only preparation first |
| X1 / physics | Does a fixed cooperation score predict selected records on unseen seeds? Preregistered ensemble and result | see PHYSICS_GATES; maximum 600 CPU s pilot | beats declared null with uncertainty bound | chance/null-equivalent or opposite trend | reject operational hypothesis, not redefine score |
| P1 / physics | Does an effective law predict unseen click trajectories? Residual/error report | 600 CPU s pilot, <=64 runs, <=256 updates | frozen law meets prespecified held-out error | frequency fit only or failed residual | no physical name; add diagnostics before interpretation |

Priorities: A0/R0 → M1 → M2/C1. S2 and K1 are bounded exploratory tasks;
physics claims require the independent gates. Do not run the entire queue
unattended or claim completion from this plan.

## Two directions of reverse engineering

From board to clicks: find a pattern, specify its full-state encoding and
interaction neighborhood, derive its response, freeze a local observation map,
then compare independent preparations and connected components.

From clicks to board: fix the desired detection, timing, record lifetime and
null outcomes first. Derive necessary state-distinguishability, causal distance,
retained-information and resource requirements; test whether existing patterns
satisfy them. A local many-to-one readout is not invertible reconstruction of the
underlying board. Neither direction licenses fitting readouts after outcomes.

Preparation search has a training set. Each selected preparation is then run
without intervention on declared validation seeds and sizes. A change of score,
threshold, duration or observable starts a newly identified protocol. Store the
old failures and the rationale for the change.

## Reproducibility and decisions

Every result must identify: candidate ID; upstream source commit and experiment
script hash; exact coupling fingerprint; complete initialization or deterministic
generator and random seed; cube side; background; boundaries; number of updates;
observation formula and version; all thresholds; search/validation split; compute
use; full-state inverse scope; and success/failure/inconclusive status. Save
initial/final checkpoints and enough state traces to verify local readouts.
Only event logs are insufficient. New evidence belongs under `research/`,
regressions under `tests/`, proof/protocol/decision documents under `docs/`.
The core stays unchanged unless a narrowly identified, tested correction is
necessary to implement the same mathematics.

Each decision entry contains **proved / observed / failed / next discriminating
test**, scope and links. Finite testing does not become a proof for all states.
A research release requires an independent rerun and a claims table that includes
negative controls. No claim of photons, matter, collapse or gravity is licensed
by naming a channel, representation or arithmetic event.

If M1 fails, first isolate preparation, routing and finite-boundary effects.
If the proposed behavior contradicts a theorem, state the minimal changed
assumption in a separate candidate proposal; do not modify the reference.
If M1 succeeds narrowly, prioritize retention robustness and coupled operation
before wider physical interpretation. The current session's actual decision is
recorded in [DECISIONS.md](DECISIONS.md).
