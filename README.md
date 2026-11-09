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

The [architecture](docs/ARCHITECTURE.md) identifies the full execution boundary.
The [algebra guide](docs/ALGEBRA_AND_COMPOSITION.md) explains the coupling,
remainder, inverse, clock drawings and composition in detail.

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

## Contribute and cite

Read [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
Changes belong on a reviewed branch; the mathematical contract must remain
explicit. All project documentation is English. Licensed under [MIT](LICENSE).
Cite **Alon Gonen, Universe24 (software)** and the tested commit;
[CITATION.cff](CITATION.cff) contains the citation metadata.
