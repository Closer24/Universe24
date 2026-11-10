# Universe24

Universe24, initiated by **Alon Gonen**, tests whether physical behavior can
emerge from one local, discrete, reversible integer rule. It combines science
and philosophy of science: conceptual hypotheses are separated from proofs,
reproducible computations and physical evidence. It is a research model, not a
validated physical theory.

## The heart: one Rule3

One periodic cube contains 48 channels per node. Each channel stores two
integers and a remainder `(a,b,r)`, with `0 <= r < 6`. Sum the six signed
neighbor inputs from the same previous state, then apply:

```python
u = sum(sign * neighbor_b for sign, neighbor_b in six_inputs)
ell, r_next = divmod(2 * u + r, 6)
a_next = b
b_next = ell - a
```

**`num=den=1` everywhere.** This is the only forward evolution law.
The [scalar implementation](universe24/core/rule3.py) and
[synchronous executor](universe24/core/engine.py) are the core. Initial states
and one of eight supported coupling sign triples are chosen before the run;
the coupling then stays fixed. Components prepare initial data. Observers and
clock/gear drawings only read the resulting states.

## Code map

| Layer | Entry point | Responsibility |
| --- | --- | --- |
| Engine | [`universe24/core/`](universe24/core/) | Exact state, fixed coupling, Rule3 and inverse |
| Input and observation | [`universe24/experiments/`](universe24/experiments/), [`universe24/observation/`](universe24/observation/) | Initial/checkpoint data and passive arithmetic events |
| Reusable preparations | [`research/components/`](research/components/), [clock interfaces](docs/CLOCK_SELECTION.md) | Place compatible initial patterns on one board |
| Experiments | [`research/experiments/`](research/experiments/), [research index](research/README.md) | Controls, complete recordings and evidence |
| Presenter | [`research/presenter/`](research/presenter/) | Generic recorded-state clocks and gears |
| Verification | [`tests/`](tests/), [`research/reference/`](research/reference/) | Regression checks and independent mathematics |
| Candidate variant (ONE version) | [`research/metric_variant_v1/`](research/metric_variant_v1/README.md) | A separately named variant with its own engine, tensor layers and tests; the reference engine is unchanged |

The [architecture](docs/ARCHITECTURE.md) identifies the full execution boundary.
The [algebra guide](docs/ALGEBRA_AND_COMPOSITION.md) explains the coupling,
remainder, inverse, clock drawings and composition in detail.

### Candidate variant: the ONE version

Start reading with [FULL_PICTURE_FINAL.md](research/metric_variant_v1/full_picture_2026-11-10/FULL_PICTURE_FINAL.md),
the final synthesis (Study 36): everything through the clocks, the tensor and the Einstein approximation.

[`research/metric_variant_v1/`](research/metric_variant_v1/README.md) is a separately named **candidate variant**, not
the reference model; the reference engine and everything in the table above are unchanged. The variant departs from
[AGENTS.md](AGENTS.md) only inside its own directory, in declared layers: many gear types per node, remainders
`0 <= r < D` with one divisor `D = 6Q`, tensors of rank at most 4 with on-site terms, dynamic links and fields, and
one-way terms that are declared with a written reason. Its current version, the **ONE version**, is one tensor, one
odd `Q`, one seed and one run; the sections [The local node](#the-local-node) to
[Follow-up research and recommendations](#follow-up-research-and-recommendations) below explain it, and
[ONE_EXPLAINED.md](research/metric_variant_v1/ONE_EXPLAINED.md) gives the long version.

Names such as "light", "gravity", "matter" or "cosmic clock" are labels on tensor blocks and states, not
identifications with physical particles or fields. Here `Q` is the divisor scale; it is unrelated to the signed account
`Q` of AGENTS.md item 12, and neither is established physical energy.

| Path in `research/metric_variant_v1/` | What it is |
| --- | --- |
| [`core/`](research/metric_variant_v1/core/) | The variant's engine. `Engine` runs Rule3 with one divisor on one tensor (inverse step and rewind are for audit only); `tensor.py` builds and validates the tensor (rank, B3 locality, acyclic two-time reads, one `Q`); `reciprocity.py` checks action = reaction |
| [`layers/one.py`](research/metric_variant_v1/layers/one.py) | `one_system()`, the ONE version: the package default plus the cosmic-clock block (the WIND hand). By default it is ONE v1, block-diagonal: the hand reads no matter, and no package gear reads the hand. The doublet-reads-the-hand coupling (Study 22) was rejected by the owner: matter must not read the clock; it also runs away (Study 30); it is kept as an explicit opt-in (`couple_doublet=True`) for the record |
| [`layers/system.py`](research/metric_variant_v1/layers/system.py) | `default_system()`, the package default: hands ON, FIX-i and GRAV-FIX A, composed from the layer blocks into one tensor |
| [`layers/electroweak.py`](research/metric_variant_v1/layers/electroweak.py) | The electroweak completion of the hands. It builds the graviweak block at FIX-i (`lam_H = lam_L = 0`: only the singlet-half hop reads the lapse). FIX-i removed the linear instability that made hands-ON bang runs run away; its price is an equivalence-principle debt for the doublet |
| [`layers/electroweak_b.py`](research/metric_variant_v1/layers/electroweak_b.py) | Route B: an exact local SU(2) × U(1)_Y with one U(2) link per face. Opt-in, OFF by default |
| [`layers/einstein.py`](research/metric_variant_v1/layers/einstein.py) | Study 28's Einstein layer, opt-in and DEFAULT OFF: `einstein_system(base=None, on=False, l0_beta=True)` returns the base unchanged unless `on=True`, which adds the harmonic-gauge linearised metric (ten components on the one cone) for the dark board L0. Tests in `tests/test_einstein.py`, demos in `demos/einstein/`, account in `NOTES_einstein.md` |
| [`layers/clockgen.py`](research/metric_variant_v1/layers/clockgen.py) | Study 34's clock law, an opt-in NEW LAW candidate, default OFF and window-limited: `one_system_clock(law="CG2", theta0_log2=21)` adds one designated, one-way, rank-3 on-site term per node, `u[metric.h00] += Θ·F`, so a cosmic turn reaches matter only through the lapse (`law="CG1"` is the additive contrast, `law="off"` is ONE v1). Valid only for L ≤ 6, A_c ≥ 840 and Θ0 = 2^21; not a size-independent law. Tests in `tests/test_clockgen.py`, account in `NOTES_clockgen.md` |
| other [`layers/`](research/metric_variant_v1/layers/) | The blocks of the one tensor: the 48-channel dark board L0, gauge links, Dirac matter, the E1 "light", the metric, lapse and β "gravity" gears, chirality and the choice gears |
| [`prepare/`](research/metric_variant_v1/prepare/) | Initial data only: the vacuum, the S2\* and J-pure bang seeds, the ONE seed |
| [`observe/`](research/metric_variant_v1/observe/) | Read-only observables: the click readout, the own-frame tick rule, ledgers, mirror and CPT-reversor audits, cosmic-clock views |
| [`demos/one/run_one.py`](research/metric_variant_v1/demos/one/run_one.py) | The ONE bang run. Its loop only calls `Engine.step`; every measurement reads the snapshots |
| [`tests/`](research/metric_variant_v1/tests/) | The package tests. `test_one.py` checks the ONE law, census, vacuum, rewind, ledgers and CPT reversor, that the run loop is Rule3 only, and that the history does not depend on the outcomes |
| [`full_picture_2026-11-10/`](research/metric_variant_v1/full_picture_2026-11-10/README.md) | The full-picture documents: [THE_ALGEBRA.md](research/metric_variant_v1/full_picture_2026-11-10/THE_ALGEBRA.md) (signed; the algebra step by step), GRAND_UNIFICATION.md, CHANNELS.md (signed; channel counts and constants) and SYSTEM_DESIGN_v8.md |
| [`README_v1_draft.md`](research/metric_variant_v1/README_v1_draft.md), [`NOTES_one.md`](research/metric_variant_v1/NOTES_one.md) | The detailed package description, which governs together with the code where documents differ, and the ONE version's account, tests and results |

## Run the engine

Python 3.11+; the engine uses only the standard library. From the repository root:

```sh
python -m universe24 --config examples/impulse.json --audit
python -m universe24 --config examples/signed_impulse.json --audit
```

For checkpoint/resume commands and **full research-test setup**, use
[Quickstart](docs/QUICKSTART.md). Research validation additionally needs its
pinned optional dependencies and restored evidence; those are not engine
runtime requirements.

## Run and compose building blocks

```sh
python -m research.experiments.run --spec research/experiments/examples/four_component_demo.json --output runs/my-four-components
```

Choose a fresh output directory. The runner prepares one board, executes Rule3
and exports recordings; it does not insert signals during evolution.
See [the component walkthrough](docs/COMPONENT_WALKTHROUGH.md),
[the assembly API](docs/COMPONENTS.md) and [current clock recipes](docs/CLOCK_SELECTION.md).
The composer rejects incompatible tensors, backgrounds and overlapping triples.

New [local clock, packet and remainder-register building blocks](docs/LOCAL_BUILDING_BLOCKS.md)
include period-five dimer/plaquette clocks, a period-six cube, an explicit
cooperative pair and scoped signal assemblies. Run three blocks on one board:

```sh
python -m research.experiments.run --spec research/component_families/examples/three_clocks.json --output runs/three-clocks
```

The [compact replay package](research/component_families/README.md) includes the
source-overlap single-read controls and the failed two-read composition test.

## Run the ONE version (candidate variant)

The variant needs numpy. Run it in a **copy** of the repository: the package tests and several package demos write JSON
into `research/metric_variant_v1/results/`. From the root of the copy:

```sh
python -m research.metric_variant_v1.demos.one.run_one --L 6 --bang jpure --rng 13 --tmax 1200 --out DIR --rewind
python -m unittest discover -s research/metric_variant_v1/tests -t .
```

The first command runs the ONE default (ONE v1, block-diagonal) on an `L = 6` cube from the J-pure bang seed for 1,200
updates. With `--rewind` it then applies the exact inverse 1,200 times, as an audit, and checks that the seed comes
back. Choose a fresh `DIR` for its output. ONE v1 is the version on which the pre-registered tests were run. Adding
`--couple` runs the rejected coupled build, which is kept for the record. The second command runs the package tests.
The [package description](research/metric_variant_v1/README_v1_draft.md) points each statement to its code and
evidence.

## View recorded experiments

```sh
python -m http.server 8000
```

Open [the nine-example Presenter](http://localhost:8000/research/invariant_families_v1/evidence/presenter_combined_v1/index.html),
select an experiment, use Play/Step and drag to rotate the cube. These recordings
are directly tracked. The [complete study inventory](research/invariant_families_v1/README.md#view-the-recordings)
also links older examples, whose archives require the documented restoration.
An HTML attachment preview may not execute JavaScript. Actual Safari/iPad
interaction remains unverified. See [Presenter help](docs/PRESENTER.md).

## Established results and open targets

- Full-state reversibility has a [mathematical derivation](docs/ALGEBRA_AND_COMPOSITION.md#rule3-and-its-inverse).
- A prepared local clock, guided signals and conditional responses have
  [explicit operating limits](docs/CLOCK_SELECTION.md).
- [Exact global patterns](research/invariant_families_v1/README.md) yield effective
  ratios 1, 1/2 and 2/3 under the unchanged rule; 48 native runs and four overlap
  controls were independently replayed. They are not localized particles.
- [Clock and gravity status](docs/GRAVITY_STATUS.md) separates the restricted
  two-preparation `4/5` recurrence-rate result, exact collective activity and
  continuity identities, and an autonomous guided clock link from the still
  unproved physical metric and Einstein dynamics.
- Autonomous complexity preference, unique retained approval, physical light,
  mass, forces and quantum measurement remain unproved. Failed controls remain
  in the [research record](research/README.md).

The [research proposal](docs/RESEARCH_PROPOSAL.md),
[degrees of freedom](docs/COUPLING_FAMILIES.md) and
[full research document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit)
separate hypotheses and unimplemented candidates from this engine.

### The ONE version (candidate variant, 10 November 2026)

These results concern [`research/metric_variant_v1`](research/metric_variant_v1/README.md), not the reference engine.
The labels are those of [the sections below](#the-local-node); the evidence is in
[NOTES_one.md](research/metric_variant_v1/NOTES_one.md) and the
[package description](research/metric_variant_v1/README_v1_draft.md).

- **The ONE default (ONE v1, block-diagonal), 1,200 updates on an `L = 6` cube from the J-pure seed** [NUMERIC;
  reproduced independently by the verifier]:
  - the run stays bounded, and the rewind of all 1,200 updates is exact across all six turns of the cosmic clock;
  - the cosmic ledgers (0 failures in 1,200 updates), the Rule3 click ledger `D·ell = K + r − r'` (0 failures in
    4,950,720 sampled checks) and the Lorenz constraint hold exactly; the Born ledger's largest deviation is
    `3.2·10⁻⁷`;
  - the turns come at t = 96, 289, 481, 672, 863 and 1054. Their spacing, about 192 updates, is an input (CHOSEN
    through the hand's constant `g_w`): it is checked, not predicted;
  - each turn starts a new seed that carries about 80 kB of new incompressible outcome record; the record grows
    linearly (39.6 kB to 437.9 kB), and every turn state is distinct;
  - no package gear reads the hand, so the package evolves bit-identically to the package alone;
  - with different token and load seeds the history (the hand, its reader gears, the choice record and every package
    gear) is bit-identical for all 1,200 updates while 98.2 % of the outcomes differ;
  - distances to the earlier bangs ("echoes") are kept as data, not as a success criterion.
- **Stability** [NUMERIC; Study 30, final, pre-registered]:
  - ONE v1, the default, shows no runaway in what could be run (J-pure at `L = 6` to t = 9,869, S2* at `L = 6` to
    1,200, J-pure at `L = 8` to 1,998 and at `L = 4` to 720), but it is not quiet: E1, then β and the metric grow
    slowly (pre-registered 4-bit onsets at t = 2,621, 2,931 and 6,752), E1 reaching the 32-bit bound by t ≈ 8,000; and
    the uniform lapse is not small (next item). ONE v1 rewinds are exact over 1,200 updates (`L = 6`, Study 22) and
    720 updates (`L = 4`, Study 30); every completed rewind was exact; the long-run rewinds were not completed;
  - its uniform lapse is neither small nor a bounded oscillation. At `L = 6` (J-pure) it rises as ≈ t² to +0.024 near
    t ≈ 4,150, crosses 0 near t ≈ 6,050, then accelerates negative: −0.070 at t = 8,000, −0.123 at 9,000 and −0.186 at
    9,869. Extrapolated, not run, |U| reaches 1/4 near t ≈ 10,500 [POST HOC]. With the S2* seed it is −0.037 at
    t = 1,200, faster than t²;
  - the cause is exact, by the summed Rule3 identity (0 failures): the `k = 0` lapse has no restoring force, and its
    net source changes sign [THEOREM + NUMERIC]. This is the main OPEN stability problem of the default; Study 34's
    clock law is a window-limited candidate fix (below);
  - the cosmic clock's quarter period scales as √N with the number of nodes N, as predicted (within 1 % at L = 4 and
    L = 8);
  - the rejected coupled build runs away at t = 1,554 (`L = 6`) and t = 666 (`L = 4`), the Higgs first. The coupling
    is the cause: the package alone and ONE v1 stay bounded on the same seed, and the rewind across the runaway is
    exact. Read after the fact [POST HOC]: the Higgs is driven 1:1 at the hand's frequency and ratchets up each cycle.
- **Study 34, an opt-in clock law** (signed by both sides; a NEW LAW candidate, default OFF): CG2 adds one designated,
  one-way term per node, `u[metric.h00] += Θ·F`. No matter gear reads Θ, and a turn reaches matter only through the
  lapse, as a common clock-rate pulse felt by every clock that reads the lapse. At `L = 6` (J-pure, to t = 8,900) it
  keeps |U| ≤ 4.1·10⁻³, also after v1's sign change near t ≈ 6,050, while v1 reaches −0.070 at t = 8,000; with S2* it
  turns the lapse back near t ≈ 1,004 (maximum |U| = 0.0197), while v1 reaches −0.0368 and accelerates [NUMERIC]. Its
  identity checks have 0 failures, its bits match v1's, and its rewinds are exact over 1,200 updates (`L = 6`, S2*),
  2,000 (`L = 4`), 400 and 1,000 [NUMERIC]. Both pre-registered absolute bounds (1.5·10⁻³ and 3·10⁻³) FAIL as worded.
  Limits: at `L = 8` the lapse is pumped (its extrema grow ×5.86, then ×7.07 per hand period); at `L = 4` the spring
  only halves the drift; L0 lumps are not held; the hand's turn intervals drift from 193 to 178 updates; M1 and M2
  still read Θ (an owner question) [NUMERIC]. Θ0 = 2^21 is CHOSEN (window-fitted, owner-approved), not forced, and the
  safe Θ0 scales as about 3.2·10⁶ × 216/L³; `h = 2^10` is forced by the band rule, and κ = 1 is CHOSEN. Theorems:
  through the lapse a turn can never fold or echo matter; "every clock reads the lapse" is IMPOSSIBLE at rank 4; an
  additive drive cannot bound the `k = 0` mode [THEOREM]. Safe as the default: NO; as an opt-in inside its window
  (L ≤ 6, A_c ≥ 840, Θ0 = 2^21): yes. It is a window-limited candidate, not a size-independent law, and ONE v1 stays
  the default.
- **The doublet-reads-the-hand coupling** (Study 22) was rejected by the owner: matter must not read the clock; it
  also runs away (Study 30); it is kept as an explicit opt-in for the record (`--couple`).
- **What is missing for Einstein.** The ONE version has Einstein's kinematics in the continuum limit and a
  Newtonian-level sourced lapse (see [The clocks](#the-clocks)). Missing:
  - the field equations themselves: an exactly conserved reciprocal source and an exact Bianchi identity are forbidden
    by theorem (G-NOGO-a, and the fixed kinetic coefficient of Rule3) [THEOREM];
  - the equivalence principle for the visible Dirac doublet, which neither feels nor sources the lapse at rest under
    FIX-i (a first-order debt) [NUMERIC; OPEN]; PPN β = 1 with hands ON, because no clock reads the β gear [NUMERIC];
  - the nine metric gears other than the lapse, which are uncoupled: no frame dragging, no constrained two-polarization
    waves and no radiation by the board's own matter [NUMERIC; OPEN];
  - light bending by the ONE content: no massless field reads the metric in the default (for test lights see Study 28
    below) [OPEN]; the free-fall magnitude read from clicks (off by 12 %) and the redshift in the package's own,
    non-static field (off by 34 %) [NUMERIC; OPEN];
  - the uniform lapse mode, which has no restoring force and drifts (above) [OPEN]; the strong field, where the clocks
    stop at a species-dependent `U` [DERIVED]; cosmological deceleration, which fails in the approved law [NUMERIC];
  - **Study 28, an opt-in Einstein layer** (signed by the builder and an independent verifier; DEFAULT OFF:
    `einstein_system(base=None, on=False, l0_beta=True)` in
    [`layers/einstein.py`](research/metric_variant_v1/layers/einstein.py), 17 tests, account in
    [NOTES_einstein.md](research/metric_variant_v1/NOTES_einstein.md)). What holds with the layer ON:
    - linearised Einstein in harmonic (de Donder) gauge for all ten metric components on the one cone, with exact
      lattice dispersion, in an integer DeWitt basis that adds no gear; it couples the diagonal sector of the dark
      board L0 only, reciprocally [THEOREM + NUMERIC];
    - two polarisations only on constraint-satisfying data, six in general, because the constraint is not imposed
      [THEOREM];
    - γ = 1 for dust is DERIVED inside the layer, given its board reader (a CHOSEN board form of ½hT); the DeWitt
      ghost sign makes the response to stress GR-like and isotropic. In the default, without the layer, γ = 1 stays
      CHOSEN;
    - β = 1 for L0, for static fields only, through a one-way read [DERIVED + NUMERIC]; with it, perihelion equals GR
      for L0 (4/3 of GR without it) [DERIVED + NUMERIC by quadrature; no board orbit was run];
    - on the board, with one-way test lights on the cone and a prescribed dust load: bending 2.08–2.16× and Shapiro
      2.02–2.06× the Newtonian value, the excess over 2 being the predicted second-order term [NUMERIC, pre-registered
      PASS]. No light of the ONE content reads the metric (E1 does not);
    - the source is not conserved: its time part changes by 44–82 % per update [NUMERIC], so sourced waves carry
      non-GR polarisations.

    Impossible [THEOREM]: the gauge-invariant Fierz–Pauli operator as the law; felt `h_0i` and any `h_ij` (i ≠ j) for
    second-order matter, at any rank; a conserved reciprocal source and an exact Bianchi identity, at any rank; spring
    and plaquette energy as sources (rank 5); gauge fields gravitating. The visible doublet stays uncoupled: on ONE v1 a
    grain wall (0.197 per unit Higgs), on the coupled build a rank wall; the FIX-i debt stays. Stability: the vacuum is
    unchanged and the rewind exact; with L0 matter the run is bounded for 400 updates at `L = 6`; the layer adds two
    uncompensated uniform drifts (`a2`, `a3`), and any run with L0 matter is limited by the base's uniform-lapse drift
    and the `U > 1/4` flip [NUMERIC + OPEN]. A board prediction that differs from GR: with `h_0i` walled off, two
    parallel co-moving light beams attract on the board, while in GR they do not [DERIVED, not run]. Verdict: the board
    holds Einstein's linearised equations (harmonic gauge, diagonal sector, dark board L0, non-conserved source); it
    does not hold the full Einstein equations.
- **What is missing for Bell.** With spacelike settings chosen independently of the seed, every CHSH value obeys
  `|S| <= 2` [THEOREM]; the board measures `S = 1.18–1.26`, against 2.07–2.42 in loophole-free experiments [NUMERIC].
  Missing:
  - any `S > 2` beyond the light cone. The only door is a law on the seed data (superdeterminism): a NEW LAW that is not
    recommended; over all seeds it allows `S = 4`, so it predicts nothing;
  - Tsirelson's bound `2√2` from the board: it follows only from four declared reader laws, which are inputs [THEOREM];
  - true entanglement, which needs a configuration space (a NEW LAW recorded for after Pauli), and fresh remainders for
    exact Born weights [OPEN];
  - **Study 27, Bell read the owner's way, with no freeze** (signed by both twins, no disagreement):
    - one quantum is BUILT exactly: one emission click, the wave on all paths, exactly one absorption click, exact
      Born counts, and an exact rewind from the final full state. "The light chooses the path that is going to be" is
      the emitting click's token, carried by the wave: a local hidden variable, which is enough for one quantum
      [BUILT];
    - with no freeze and a typical seed, Bell does NOT stand at spacelike separation: board locality and outcome
      independence give `S ≤ 2 + 6δ`, and typical seeds give `δ = 0` [THEOREM]. Exact runs over the whole seed class
      give `S = 5/4` with independent tokens and at most `S = 2` with a shared token [NUMERIC];
    - the owner's rule in its strongest form ("only confirmed histories, exactly one click per station") reaches
      `S = 2.4677` at `D = 30`, and at most 16√2/9 ≈ 2.514 in the continuum, but only by conditioning on a common
      effect of the source token and the settings (`δ = 0.28`) [BUILT + NUMERIC]. Read as a seed law this is
      superdeterminism, a NEW LAW, and it is fine-tuned: the allowed seeds are a fraction of at most `e^(−0.0214N)`
      [THEOREM]. Under it an asymmetric detector gives a 0.147 signal, so no-signalling is a theorem only where
      `S ≤ 2`; the correlation curve is not the quantum one, and Tsirelson's 2√2 is derived in no reading [THEOREM];
    - a forward confirmation makes every record that uses the far setting wait at least d/v, and with no freeze that
      wait is visible [THEOREM];
    - verdict: "Bell stands" is NOT met. By the owner's rule ("Bell only if exact"), Bell is recorded honestly as not
      solved.
- **Other open items:**
  - Masses [THEOREM; DATA; Study 35]: the form of the masses comes out of the clicks by itself, but the light values
    are data, about 39 bits for the leptons, written in as tensor integers (THEOREM K). OPEN: the click reading of the
    silent λ = 0 level; the doublet's dressing mechanism, diagnosed as about 89 % through its own weak current and
    11 % through the Higgs; and a stabilized flat-Higgs variant (the naive one fails).
  - Quarks are not connected [NUMERIC]: 228 of the 382 channels per node (the su2, su3 and u1 gauge layers) read nothing
    and are read by nothing, so the SU(3) field acts on no quark, and the quark link is not built. Only 127 channels
    form the connected physical core.
  - Families [THEOREM]: the node gives no natural family of three. Three families as copies are a NEW LAW build target
    that is not in the ONE version.
  - Pauli [THEOREM]: the exchange sign and Pauli exclusion are missing on one board. Pauli by orbital copies is a NEW LAW
    for a separate variant.
  - Route B, the exact local hypercharge, is built, opt-in and OFF [NUMERIC; OPEN]. Its photon reaches at most
    0.41 `c_Q`, so one light for every field is OPEN.

## What a click is (proposal)

A proposed reading, consistent with the engine contract: it adds no code and changes no state.
[`universe24/observation/clicks.py`](universe24/observation/clicks.py) implements it as a passive readout.

- A **click** is a channel update whose quotient `ell = (2*u + r) // 6` is non-zero (it equals
  `b_next + a`): the moment the channel's remainder "gear" overflows. No detector code exists; the
  click is the Rule3 step itself, read afterwards.
- Its **kind** is `u mod 3` (C0, C1, C2), computed as `((r_next - r) // 2) % 3`; its **size** is the
  quotient `ell`.
- **Time mirror:** running the board forward from the mirror image of a final state retraces the run,
  and the click log comes back in reverse order with kind and quotient negated: C1 and C2 swap, C0
  stays C0.
- **What clicks can and cannot tell:** nothing crosses hardware at rest without clicking, so light
  leaves a trace wherever it moves. But clicks fix only ratios of clock periods, so an observer needs a
  declared standard clock. Some state data never appear in any click (see the twins below).
- C2 is an arithmetic class, not a proven physical selection law. No click chooses an outcome: clicks
  record or reveal prepared data.

The frozen [click decoder](research/click_decoder_v1/) reads official click logs only.

## Algebra found on the board

Labels: **THEOREM** (proved, refereed), **EXHAUSTIVE** (checked in every case of a stated domain),
**REFEREED** (numbers reproduced by an independent referee). Proofs and referee reports are in the
research record, not in the engine.

- **Click mirror** [THEOREM; experiment E25]: `JR∘F∘JR = F⁻¹`. This is the time symmetry of a
  reversible deterministic system, not a quantum effect.
- **Click-invisible twins** [THEOREM; E25]: two states that differ only in the remainder `r` and
  `r + 1` (`r` even) have identical click logs forever. The click record does not fix the full state.
- **Head-on crossing of light** [EXHAUSTIVE]: two light pulses meeting head-on both pass, each delayed
  by exactly 4 updates, with no residue (768 straight-fibre and 38,400 corner cases).
- **C0 is a pure carry** [EXHAUSTIVE]: a C0 needs a push of at least 3, neither reads nor changes the
  gear, and is its own time mirror; a C0 never revealed gear data (0 of 829 cases).
- **The coupling is a fixed curved 2O connection** [REFEREED, under `+++`]: around every unit plaquette
  the channel frame turns by an order-3 permutation with no fixed point (120°). A closed fibre loop
  closes only when its total twist fixes its start channel. This curvature is built into the coupling,
  uniform and constant; it is not gravity.
- **Bell bound** [THEOREM]: with the light cone and independently prepared settings, every CHSH value
  read from clicks satisfies `|S| <= 2`. The board reaches 2, never more.
- **Exit law by counting** [THEOREM; E22]: in the CC8 router, `P(exit B) = N_B / 14` over the hidden
  phase. This is a Chinese-remainder counting law, a sawtooth in the device phase, not `cos²` and not
  the Born rule.
- **Taxicab fibre geometry** [REFEREED]: in the lattice's own addresses, lengths along staircase fibres
  are Manhattan lengths. A Riemannian metric exists only where the initial data write one.
- **Light slows light** [REFEREED]: light crossing a source's light stream is delayed in proportion to
  the flux density `r^-(d-1)`, the shape of Newton's field law, and the delay depends on the source's
  timing parity. No clock is slowed, and there is no free fall beyond contact drift. It is contact,
  not gravity.

The next five sections explain the ONE version of the candidate variant: its node, its algebra, its clocks, its seed
and tensor, and what needs follow-up research. Each claim carries a label, as in the signed
[THE_ALGEBRA.md](research/metric_variant_v1/full_picture_2026-11-10/THE_ALGEBRA.md): **THEOREM** (proved from the law),
**NUMERIC** (an exact integer computation), **DERIVED** (a short argument from those), **CHOSEN** (an input, a
convention or data), **NEW LAW** (an extension that changes the law's content and needs an explicit owner decision) or
**OPEN** (not established). The long version, with worked examples, is
[ONE_EXPLAINED.md](research/metric_variant_v1/ONE_EXPLAINED.md).

## The local node

**Reference engine** ([AGENTS.md](AGENTS.md), [model](docs/MODEL.md)): one elementary node per site of the periodic
cube `(Z/LZ)^3`, `L >= 3`, holding one board of 48 channels indexed by the group 2O. Every channel stores two
arbitrary-precision integers `a, b` and a remainder `r` in `0..5`, and receives exactly six spatial inputs, one from
each face neighbour; a zero entry of a signed matrix does not delete a port. The coupling is built from the fixed 2O body
actions `(0, 1, 3)` and three body-axis signs chosen before the run, and it stays constant.

**ONE version** (candidate variant): every site holds the same list of gears, each a triple `(a, b, r)` with
`0 <= r < D`: 382 gear types in ONE, 375 in the package default [NUMERIC]. Given the content, the symmetry fixes the size
of each sector [THEOREM]: 48 for the dark board L0 (the regular module of 2O, given a sign-free frame), 16 per charged
Dirac fermion, 4 for the Higgs, 2 / 4 / 8 / 18 per link (U(1) / SU(2) / U(2) / SU(3)), 10 for the metric and 128 per
family. Which sectors exist, how many copies there are, and the total are CHOSEN; today only 127 of the 382 gears form
the connected physical core [NUMERIC]. The node's algebra [THEOREM]: the 48 labels are the binary octahedral group 2O
over the Gaussian integers `Z[i]`. Acting on the left they are the frame and spin; acting on the right they are internal
(an exact internal SU(2) skeleton, Q8). The mirrors `O_h = Aut(2O)` act as its outer automorphism. The cube has one
orientation bit, and for Dirac matter `Γ5 = −PxPyPz` splits it into exactly two hands. All characters of the cube groups
are real, so the cube by itself makes SU(2)s, never U(1) or SU(3). Details:
[CHANNELS.md](research/metric_variant_v1/full_picture_2026-11-10/CHANNELS.md) and
[THE_ALGEBRA.md §2](research/metric_variant_v1/full_picture_2026-11-10/THE_ALGEBRA.md).

**Locality, a binding rule of the law:**

- every gear's input `u` is computed only from its own node and its six face neighbours [CHOSEN];
- every monomial of the tensor sits on one node or on the two ends of one face (B3); the builder rejects anything else,
  such as an edge or diagonal offset, a two-step offset, or a monomial that touches both `+e` and `−e` [CHOSEN; the
  rejection is enforced by the builder, THEOREM];
- every update reads only the complete previous snapshot [CHOSEN];
- the cosmic clock is not a non-local variable: it is one hand per node, joined to the hands of its six face neighbours
  by a rigid face term [NEW LAW, approved];
- so information moves at most one face per update, inside the board-causal (taxicab) cone [THEOREM]. The physical
  wave cone `c_Q ≈ 0.577` lies inside it. `c_Q` is the wave front of the common stencil, not a hard bound, so the law
  alone does not exclude influence between the two cones [THEOREM].

**Links make the geometry, not the neighbour graph:**

- the neighbour graph itself, the periodic cube with six faces per site, is a CHOSEN input;
- what passes between neighbours is set by the face (link) terms of the tensor. The face weights `Q − 1` of the common
  stencil give the one cone `c_Q² = (Q − 1)/(3Q)` [THEOREM, given the CHOSEN common stencil]. The gauge links carry the
  forces, one link per face per multiplet [THEOREM, forced by rank ≤ 4]. Gravity's link factor `1 − 4U`, together with
  the clock factor `1 − 2U`, gives the spatial metric `g_ij = (1 + 2U)δ_ij`, so γ = 1 comes through this CHOSEN factor
  [CHOSEN ⇒ DERIVED].

## The full algebra

Every gear of every node keeps the primitive of [the heart](#the-heart-one-rule3) and reads the same complete previous
snapshot; only the divisor and the input change:

```python
u = T(previous_snapshot)            # one fixed integer polynomial: rank <= 4, own node + one face link
ell, r_next = divmod(2 * u + r, D)  # one divisor D = 6Q for every gear, Q = 2**33 + 1 (odd)
a_next = b
b_next = ell - a
```

The ten-line summary of THE_ALGEBRA.md (§0), with its labels:

1. [CHOSEN] Space is the periodic cube `(Z/LZ)³`, `L ≥ 3`; every site holds the same list of gears; a gear holds
   `(a, b, r)`.
2. [CHOSEN] One divisor `D = 6Q`; one integer tensor `u` of rank ≤ 4: at most three factors from `v = (1, b, a)`, on the
   node and one face.
3. [THEOREM] One update, Rule3: `ell, r' = divmod(2u + r, D)`; `a' = b`; `b' = ell − a`. It is an exact bijection.
4. [CHOSEN] One seed: the vacuum `(0, 0, 3Q − 1)` everywhere plus a few non-vacuum integers. Each later turn of the
   cosmic clock starts a new seed, the full state at the turn (owner decision).
5. [THEOREM] Every gear is a clock: `b(t+1) + b(t−1) = 2u/D + ε` exactly, `|ε| < 1`, i.e. `M b(t) + ε` for the linear
   part; a mode with eigenvalue μ of `M` ticks at `cos w = μ/2`.
6. [THEOREM] A click is a carry of the remainder: `ell(t) = b(t+1) + b(t−1)`, and `D·Σ ell = Σ K + r(0) − r(T)` exactly.
7. [THEOREM] For the reciprocal part of the tensor (17,729 of the 18,553 live monomials) Rule3 is the discrete
   Euler–Lagrange equation of `L(x, y) = Φ(x) + Φ(y) − D x·y`, and there rank = degree of Φ. Reciprocity itself is a
   CHOSEN design rule, checked by the package; the 706 designated and 118 two-time monomials are not gradients.
8. [THEOREM] The node is the group 2O (48 channels) over `Z[i]`: acting on the left it is the frame and spin, on the right
   it is internal; the mirrors are its outer automorphism.
9. [DERIVED] Einstein's kinematics is in the tensor as the continuum limit of exact integer identities: one cone, given
   the one CHOSEN stencil; an exact equivalence-principle factor for every clock that reads the lapse (in the live FIX-i
   default only the dark board L0 reads it at rest, while the visible Dirac pair's rest clock neither feels nor sources
   it: a declared first-order debt); a γ = 1 weak-field metric via the CHOSEN link factor `1 − 4U` (the 1911 control
   gives γ = 0); local rotations. The dynamics is a Newtonian-level sourced scalar lapse plus designated one-way parts.
   The full Einstein equations are NOT reproduced, because Rule3 forbids, by theorem, an exact Bianchi identity and an
   exactly conserved reciprocal source.
10. [CHOSEN] What the cube fixes are forms (groups, sectors, hands, splits, cones); 3, `L`, `Q`, the weights and the seed
    are inputs.

Why `Q` is odd [THEOREM, given a CHOSEN demand]: the exact mirror flips the remainder by `R'(r) = D − 2 − r` (r even)
or `D − r` (r odd), and `R'` fixes a remainder only when `Q` is odd (exactly `3Q − 1` and `3Q`). So a vacuum fixed by
the exact mirror exists if and only if `Q` is odd.

## The clocks

- **Every gear is a clock** [THEOREM]: `b(t+1) + b(t−1) = 2u/D + ε`, and a mode with `M e = μ e`, `|μ| < 2`, ticks at
  `cos w = μ/2`. By hand [NUMERIC]: one gear with `u = 12b`, `Q = 5`, `D = 30`, started at `(0, 1, 14)`, clicks
  `1, 1, 0, −1, −1, 0` while its remainder walks 14, 8, 2, 2, 8, 14, and returns to its start after 6 updates.
- **A click is a carry** [THEOREM]: the remainder is a phase on a circle of `D` positions; each wrap emits `ell = ±1`,
  and every gear keeps the exact ledger `D·Σ ell = Σ K + r(0) − r(T)`. With a fresh uniform remainder a carry fires with
  probability exactly `K/D` (the Born count) [THEOREM]; whether the remainders are fresh is OPEN.
- **A particle's mass is its rest clock rate** [THEOREM]: a mode's mass is its rate at `k = 0`, read from the click
  record; a lone gear `u = m·b` has `cos w0 = m/D`. The node fixes the shape: the 1 + 2 split and the lattice-scale
  1:2:3 ladders of L0 are forced [THEOREM]. Study 35 (signed by both sides) asked whether masses come out of the
  clicks with nothing put in by hand:
  - with no mass entry the board makes 9 rest levels in the handed class, `cos w0 = λ/6` with λ ∈
    {0, 2, 4, 2 ± √2, 2 ± 2√2, 2 ± 2√3} (7 in the flat class), measured from the click record to within 7·10⁻⁸ of
    `arccos(λ/6)/2π`. They are the dark board's (L0) levels, all at the lattice scale: the lightest is 0.068 per
    update (THEOREM S), and the λ = 0 level is click-silent. Nothing light comes out by itself [THEOREM + NUMERIC];
  - identical clocks never split themselves (THEOREM E): a split needs a coupling integer or a seed amplitude, which
    are data, so a forced Koide relation among identical clocks is impossible [THEOREM];
  - the visible doublet's mass is the tensor integer `2yv = 4915·2^22` [DATA]. Its measured rest rate, 0.06548 per
    update, matches the formula's 0.06549, and changing the integer moves it [NUMERIC]. No vev is reached by the
    clocks: from `Φ = 0` the Higgs runs away, so the mass exists because the seed starts at `Φ = v`
    [THEOREM + NUMERIC];
  - the fairest form of "masses by themselves" [BUILT]: a massless clock riding a condensate in the seed gets a light
    rest rate with no mass entry, but its value is the coupling times the square of the seed amplitude [DATA];
  - verdict: the FORM of the masses comes out by itself; the light VALUES do not. They are information, about 39 bits
    for the leptons, which must be written in once, as tensor integers or as seed data [THEOREM K].
- **Gravity is a lapse that slows clocks and links**: a clock that reads the lapse `U` gets the factor `1 − 2U` on its
  mass entries and `1 − 4U` on its link entries [CHOSEN, approved law]; feeling and sourcing the lapse are two
  derivatives of one potential [THEOREM]. This gives Einstein's kinematics in the continuum limit and a
  Newtonian-level sourced lapse [DERIVED]; γ = 1 and the one cone come from CHOSEN ingredients (the link factor, the
  common stencil), and with the opt-in Einstein layer of Study 28 γ = 1 for dust becomes DERIVED given its board
  reader; the full field equations are NOT reproduced (G-NOGO-a, no exact Bianchi) [THEOREM]; and in the live default
  the visible Dirac doublet neither feels nor sources the lapse at rest, a first-order equivalence-principle debt
  [NUMERIC; OPEN].
- **The cosmic clock** [NEW LAW, approved: the WIND hand]: one hand Θ per node, turned by the choice events: its
  stiffness is the record Δ of the matched choice pairs. The hand reads no matter, and in the default (ONE v1) no
  package gear reads the hand [NUMERIC]: apart from the hand's own face terms, its only readers are the cosmic block's
  two reader gears M1 and M2, whose intensity loads the choice pairs. The doublet-reads-the-hand coupling was rejected
  by the owner, because matter must not read the clock. An opt-in clock law, Study 34's CG2 (default OFF, valid only
  for L ≤ 6), lets the hand act on the lapse alone, so that a turn reaches matter only as a common clock-rate pulse,
  never as an echo or a bang of matter [NEW LAW; THEOREM]. The bang at `t = 0` is the one exact CPT bang [NUMERIC];
  every later turn of the hand is a bang that starts a NEW seed, the complete state at the turn [CHOSEN, owner
  decision]. Three theorems fix what this means: a growing history has at most one exact bang, so later turns never
  return to the original seed (THEOREM D); the board's information is law + seed + ⌈log2 t⌉, and only the click record
  grows (THEOREM K); the choices time the turns and never cause a bang (THEOREM N).
- **The arrow of time is the record**: in the ONE run the click record grows by about 80 kB of new incompressible
  outcomes per aeon [NUMERIC]. Rule3 is a bijection, so nothing is lost [THEOREM].
- **No freeze** [THEOREM; owner decision]: no input can pause an oscillator, and no b-only rule of any degree makes a
  hold; the zero-time hold was dropped. Only the chosen path clicks, because one shared remainder overflows once
  [THEOREM]. That light executes the clicks is the owner's reading [CHOSEN].
- **Choice and determinism.** The owner's position, in contrast with a deterministic cellular-automaton reading of
  physics such as 't Hooft's: there is a choice for each click, so the universe is not deterministic [CHOSEN, the
  owner's reading]. The board facts: the click outcomes are set by free seed data (the tokens), which nothing else on
  the board fixes [CHOSEN: seed data]; with different tokens and loads the history stays bit-identical while 98 % of
  the outcomes differ [NUMERIC]; and given those data, Rule3 is an exact bijection [THEOREM]. So the final full state
  `(a, b, r)` and the seed determine each other; the click record alone does not, because the parity of `r` is inert
  (`K = 2u` is even): a seed and its parity-flipped copy give the same `a`, `b` and clicks [THEOREM].

## The initial conditions (seed) and the tensor

**The seed** [CHOSEN; data only, written by [`prepare/`](research/metric_variant_v1/prepare/)]: every gear starts at the
vacuum `(0, 0, 3Q − 1)`, plus a few non-vacuum integers. The minimal bang seed S2\* has exactly two of them; the J-pure
seed has 6,912 on 216 nodes. The ONE seed ([`prepare/one.py`](research/metric_variant_v1/prepare/one.py)) adds the hand
at rest at `Θ0`, including the remainder `3Q − 1`, a neutral packet, static Born loads and tokens; it is fixed by the
CPT reversor about the bang centre. Two declarations: the Born weights are seed data (the loads put them in), and
no-signalling holds in the matched seed sector, where the law preserves it and the seed initiates it. Each later bang is
a new seed: the complete state at the turn.

**The tensor** is built in seven steps and checked ten times
([details and a worked U(1) block](research/metric_variant_v1/ONE_EXPLAINED.md#the-initial-conditions-seed-and-the-tensor)):

1. split the content into blocks, all with one `Q`;
2. write one integer potential Φ per reciprocal block and take `u = ∂Φ/∂b` (action = reaction), so rank = degree of Φ:
   rank 4 is a quartic Φ, a cubic force [THEOREM];
3. store the deviation from the vacuum and remove the linear term, so the vacuum stays fixed [THEOREM];
4. keep every monomial on one node or one face link (B3 locality) [CHOSEN];
5. declare every term that is not a gradient of Φ one-way, with a written reason; it gives up Newton III [CHOSEN];
6. order the two-time (`a`) reads acyclically, which makes the staged exact inverse possible [THEOREM];
7. compose, then check: one `Q`; rank ≤ 4; B3; acyclic reads; reciprocity; a fixed vacuum; exact rewind; an exact CPT
   reversor on a seed; an all-`k` Bloch scan; integrality. Checks 1–8 do not imply a bounded history [THEOREM]; the
   Bloch scan separated the runs that ran away from those that stayed bounded [NUMERIC].

Census [NUMERIC]: the package default has 375 gear types, 18,553 monomials and 706 one-way designations, at rank 4;
the ONE default (v1) has 382 gear types, 18,592 monomials and 736 designations; the rejected coupled build, kept for
the record, has 27,040 monomials and 17,856 designations. Rank 4 is final: rank 5 was studied and rejected [CHOSEN;
Study 23].

## Follow-up research and recommendations

Study 34 (signed): the clock law CG2 is an opt-in NEW LAW candidate, default OFF, valid only inside its window (L ≤ 6,
A_c ≥ 840, Θ0 = 2^21). It holds the default's uniform lapse there, but it is not a size-independent law, so that
problem stays OPEN beyond the window (see Stability above). In ONE v1 the cosmic block's own two reader gears, M1 and
M2, still read the hand: an owner question.

The prioritized list, with reasons and recommendations, is
[FOLLOW_UP_RESEARCH.md](research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md).
Its top items, in priority order:

1. **A generic clock law: the cosmic hand acting on time itself (Study 34)** ([P1][fu-p1],
   [recommendation 1][fu-rec1]) [NUMERIC: CG2 holds the uniform lapse only for L ≤ 6; THEOREM: no fold or echo through
   time, "every clock reads the lapse" impossible at rank 4, an additive drive cannot bound `k = 0`; OPEN: a
   size-independent law]. CG2, one designated lapse term per node with no matter reading the clock, holds
   |U| ≤ 4.1·10⁻³ to t = 8,900 at `L = 6` at the CHOSEN Θ0 = 2^21, against ONE v1's +0.024 and −0.070; it is pumped at
   `L = 8`, only halves the drift at `L = 4`, and does not hold L0 lumps; the safe Θ0 scales as about
   3.2·10⁶ × 216/L³. Safe as default: NO; ONE v1 stays the default. Recommendation: a size-independent clock law, or
   Θ0(L) derived from seed data by a written rule; PASS means |U| ≤ 0.01 at L = 4, 6 and 8 over ≥ 10,000 updates on
   every seed, with exact rewinds and no change to the static-load field.
2. **The default's main open stability problem: the massless uniform (k = 0) lapse** ([P2][fu-p2],
   [recommendation 2][fu-rec2]) [THEOREM for the identity and masslessness; NUMERIC, Study 30; OPEN for a bounding
   law]. ONE v1 shows no runaway in what could be run, but it is not quiet, and its uniform lapse is not small
   (above). Name the block whose net source turns negative near t ≈ 3,000; measure, rather than extrapolate, the times
   to |U| = 0.1 and 0.25 for each L and seed, including an L0-rich seed; and complete the long rewinds that Study 30
   could not finish.
3. **Masses out of the clicks** ([P3][fu-p3], [recommendation 3][fu-rec3]) [THEOREM: only the nine dark lattice-scale
   levels come out by themselves; identical clocks cannot split themselves (THEOREM E), so a forced Koide relation is
   impossible; about 39 lepton bits must be written in (THEOREM K); CHOSEN: the visible values]. Work on Study 35's
   open items, the λ = 0 click reading, the dressing mechanism (about 89 % through the weak current) and a stabilized
   flat Higgs, under a strict information test: a mass counts as derived only if it needs fewer input bits than its
   precision demands, and moving the bits into the seed does not count.
4. **The rejected coupled build runs away** ([P4][fu-p4]) [NUMERIC; CHOSEN for the rejection]: ONE v1 as the code
   default, and the opt-in labelled "rejected; runs away".
5. **Visible matter does not feel gravity**, the FIX-i equivalence-principle debt ([P5][fu-p5],
   [recommendation 4][fu-rec4]) [NUMERIC; DERIVED for the trilemma; OPEN]. Study 28 found the needed lapse × Yukawa
   dressing inside the approved rank-4 kind, but at 0.197 per unit Higgs it is below the integer grain in ONE v1. The
   recommendation is an owner-approved integer re-parametrisation, checked against the three legs of the trilemma.
6. **Full Einstein, light bending, frame dragging and gravitational waves** ([P6][fu-p6]–[P8][fu-p8],
   [recommendation 5][fu-rec5]) [THEOREM: no exact form at rank 4, and no frame dragging for second-order matter at
   any rank; NUMERIC: Study 28's opt-in layer, with bending and Shapiro PASS]. The board predicts things GR does not:
   monopole radiation at twice the rest rate, and parallel light beams that attract [DERIVED, not run]. Next, on the
   opt-in layer, each with pre-registered pass bands: a Krein check at lattice k (the layer stays OFF if it fails),
   the drift law of its new uniform modes, the period-averaged source defect, monopole radiation, and the parallel
   versus antiparallel beam test.
7. **Remainder freshness, i.e. Born statistics** ([P9][fu-p9]) [OPEN]: a cheap read-only test of whether the board's
   outcome counts are binomial or deterministic rates (expected: sub-binomial).
8. **Bell, entanglement and Pauli; free choice versus determinism** ([P10][fu-p10]) [THEOREM: with no freeze and a
   typical seed, `S <= 2` exactly (Study 27); NEW LAW for any way past it]. `S > 2` appears only by discarding clicks
   or by a fine-tuned seed law, with no no-signalling theorem and no Tsirelson bound; one quantum is built exactly.
   True entanglement needs a separate configuration-space variant, after Pauli copies.

The list above follows the final, frozen FOLLOW_UP_RESEARCH.md.

The OPEN items recorded in the signed sources are: the full Einstein field equations (Study 28's opt-in layer reaches
the linearised equations for L0 only); the doublet's equivalence-principle debt; the uniform lapse mode, which has no
restoring force (the main open stability problem of the default); one light for every field; the freshness of the
remainders; Bell beyond the light cone (Study 27); the quark link, three families, Pauli copies and true entanglement.
[What is missing for Einstein and for Bell](#the-one-version-candidate-variant-10-november-2026) is listed in detail
above.

[fu-p1]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p1
[fu-p2]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p2
[fu-p3]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p3
[fu-p4]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p4
[fu-p5]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p5
[fu-p6]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p6
[fu-p8]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p8
[fu-p9]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p9
[fu-p10]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#p10
[fu-rec1]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#rec1
[fu-rec2]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#rec2
[fu-rec3]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#rec3
[fu-rec4]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#rec4
[fu-rec5]: research/metric_variant_v1/full_picture_2026-11-10/FOLLOW_UP_RESEARCH.md#rec5

## Contribute and cite

Read [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
Changes belong on a reviewed branch; the mathematical contract must remain
explicit. All project documentation is English. Licensed under [MIT](LICENSE).
Cite **Alon Gonen, Universe24 (software)** and the tested commit;
[CITATION.cff](CITATION.cff) contains the citation metadata.
