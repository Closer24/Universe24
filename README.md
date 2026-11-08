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

## Contribute and cite

Read [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
Changes belong on a reviewed branch; the mathematical contract must remain
explicit. All project documentation is English. Licensed under [MIT](LICENSE).
Cite **Alon Gonen, Universe24 (software)** and the tested commit;
[CITATION.cff](CITATION.cff) contains the citation metadata.
