# Universe24

**Could reality be built from integers?** Universe24 is a research project initiated by **Alon Gonen** to investigate whether one simple, local, reversible rule could underlie the complexity of physical reality.

This repository provides the **MIT-licensed reference engine for one specific mathematical candidate**: an integer-valued cellular automaton with **Rule3**, 48 group-labelled channels per site and a fixed signed spatial coupling. **The broader scientific proposal and the present code are not the same thing.**

> **Research status:** This repository is a mathematical and computational research prototype, **not a validated physical theory**. No derivation of photons, atoms, quantum measurement, physical energy, angular momentum, gravity, or the Born rule is claimed.

**Start here:** [Full research proposal (Google Docs)](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit?usp=drivesdk) · [Research proposal: concise guide](docs/RESEARCH_PROPOSAL.md) · [מדריך בעברית](docs/README.he.md) · [Quickstart](docs/QUICKSTART.md) · [Mathematical model](docs/MODEL.md) · [Architecture](docs/ARCHITECTURE.md) · [Experiments](docs/EXPERIMENTS.md) · [Click observations](docs/OBSERVATION.md) · [Research status](docs/RESEARCH_STATUS.md) · [Contributor rules](AGENTS.md)

## The research question — beyond this code

The premise being tested is that **space, time, waves, matter and observed measurement events might be emergent behaviors of exact integer states**, rather than separately programmed kinds of objects. Each elementary node would obey the **same local law**; different initial patterns and interactions would produce different large-scale phenomena.

The project works in **two directions**: derive requirements from known physics and measured detector events, then build explicit candidate dynamics and compare their predictions with those requirements. A central research question is whether internal recurrent patterns could act as clocks and whether interactions could produce persistent, exclusive detector records — without adding a detector-specific command.

The broader proposal also asks whether coherent interference, entanglement, physical conservation laws, stable matter and spacetime geometry can be recovered. It investigates, but does **not assert**, a possible relationship between realized histories and *structured complexity*. These are **open research goals**, not features already implemented in the engine.

**Three distinctions for new readers:**

1. **Proposal ≠ established physics.** The [living scientific document](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit?usp=drivesdk) describes postulates, competing hypotheses, earlier variants and quantitative targets.
2. **Mathematical candidate ≠ all proposed mechanisms.** The code implements the single-board, six-spatial-neighbor Rule3 candidate. The historical Clockwork G and alternative H9a are comparisons, not hidden extra stages.
3. **Arithmetic event ≠ physical detector click.** The three external remainder classes are bookkeeping on completed transitions. The engine has **no built-in history chooser or cancellation gate**.

For the full framing, what is derived and what remains open, read the [concise proposal summary](docs/RESEARCH_PROPOSAL.md) before the technical sections below. The Google Doc may require access permissions from its owner.

## The entire model in brief

| Component | Fixed design |
| --- | --- |
| Space | Periodic cubic lattice `(Z/LZ)^3`, one parameter `L >= 3` |
| Elementary node | **One board**, 48 channels labelled by `2O` |
| Channel state | `(a, b, r)`: two arbitrary-precision integers and a remainder in `0..5` |
| Per-channel input | **Six spatial neighbors**, exactly one channel from each face direction |
| Coupling | Fixed signed tensor derived from the 48-element group; entries `-1, 0, +1` |
| Adjustable setup | Cube side, fixed body-axis signs, initial seed, reference run length, external outputs |
| Dynamics | **Rule3 only**, with `num = den = 1` |
| Observation | Three *arithmetic event classes* `C0, C1, C2`, logged externally |
| Clock | Global update count is a **simulation index**, not a physical clock |

Let `u[x,g]` be the sum of the six **signed** current-counter inputs. Every channel executes the same exact update:

```text
ell, r_next = divmod(2*u[x,g] + r[x,g], 6)
a_next     = b[x,g]
b_next     = ell - a[x,g]
```

All new states use the *same old global snapshot*. There is no runtime detector logic, adaptive routing, second board, per-channel coefficient, on-site edge, state reset, or click-triggered rule.

## Get started

Requirements: **Python 3.11+**. Running from the repository requires **no third-party Python packages**.

```bash
git clone https://github.com/Closer24/Universe24.git
cd Universe24

python -m unittest discover -s tests -v
python -m universe24 --config examples/impulse.json --audit
```

For an example with signed couplings and read-only event logging:

```bash
python -m universe24 --config examples/signed_impulse.json --audit --events events.jsonl --output final.json
python -m universe24 --resume final.json --steps 10 --audit
```

**Note:** Output files passed to `--events` or `--output` must not already exist. Delete or choose a different output filename before another run. The `--resume` option takes a **full-state checkpoint**, not an event log; it performs additional *forward* Rule3 updates.

For a complete command reference and a minimal seed example, see [Quickstart](docs/QUICKSTART.md). For all supported input fields, see [Experiments](docs/EXPERIMENTS.md).

## What may vary between experiments?

**Before the run:** the single cube side `L`; one of eight fixed body-axis sign combinations (`[+1,+1,+1]` reproduces the positive reference coupling); the initial values of the channels; and the number of reference steps.

**During the run:** no experiment code may change Rule3, coupling signs, graph topology, node state, or scheduling semantics. Every evolution step is computed only by the generic engine.

**Outside the run:** observers may count and classify arithmetic transitions, inspect states, export event logs, and check the mathematical inverse and balance identities. Observations do not feed back into the state.

## Repository map

```text
universe24/
  core/
    group_2o.py       exact 2O construction, multiplication, rotations
    coupling.py       fixed signed six-direction 48×48 coupling
    state.py          immutable state on the periodic cube
    rule3.py          sole scalar forward law and its inverse
    engine.py         pure reference executor; same-snapshot updates
  experiments/
    config.py         JSON seeds and full-state checkpoints
  observation/
    clicks.py         external C0/C1/C2 arithmetic event classification
    diagnostics.py    exact audit and algebraic accounting
  __main__.py         CLI
examples/             impulse, signed impulse, prepared clock
tests/                automated contract tests
docs/                 model, usage, architecture, observation, research status
AGENTS.md             non-negotiable development constraints
CONTRIBUTING.md       safe modification and review process
```

## What has and has not been established?

- The specification defines an exact, reversible full-state update; the source includes inversion and algebraic contract tests.
- The signed coupling is a choice made **before** simulation, not an evolving field. The model retains six spatial ports even when a matrix entry is zero.
- The three `Ck` labels are **modulo-three classes of remainder transitions**. `C2` is **not** an automatically selecting detector click.
- A passive output `Click` record is an analysis object written outside the automaton; it is **not** an internal memory cell.
- Mathematical reversibility, finite cube symmetry and balance identities do not establish physical conservation of energy/angular momentum or quantum measurement.
- Candidate detector selection, autonomous cancellation, robust protected records, physical time and empirical predictions remain open research.

See [Research status and acceptance criteria](docs/RESEARCH_STATUS.md) before interpreting numerical patterns as physics. For the wider scientific agenda, including its ten foundational postulates, experimental benchmarks and the conditional complexity-selection idea, see [the research summary](docs/RESEARCH_PROPOSAL.md) and [the full Google Doc](https://docs.google.com/document/d/1NDPfeFj9vldgb0RMSSvx2lBSmOo__E-F3t2cZwfjOjI/edit?usp=drivesdk).

## Collaboration and license

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before changing any code. Proposals that alter the mathematical primitive or topology must be identified as **separate model variants**, not silently merged into Rule3.

Licensed under the repository's [MIT License](LICENSE).

## Author and citation

**Alon Gonen** is credited as the originator of the Universe24 research project. This repository records the current computational implementation; contributions to particular files or later research should be credited separately.

If you use or discuss the Universe24 code, cite **Alon Gonen, *Universe24* (software), GitHub: https://github.com/Closer24/Universe24**. See [CITATION.cff](CITATION.cff) for the machine-readable citation. Cite a specific commit SHA when reproducibility matters. This citation does not imply that the proposed physical interpretation has been established.
