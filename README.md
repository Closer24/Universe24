# Universe24

**The aim of Universe24 is to represent reality as it is, inside its own simulator, the engine: a lattice of Node-clocks stepped by one rule in whole numbers and read through clicks, a world that shows what nature shows.**

## What stands

The engine is **Tensor24**, `src/tensor24/`: three files of whole numbers lay a world, a loader turns them into arrays, every Node-clock steps by one act in every round, a runner repeats the rounds and writes a record, and a decoder reads the record into what nature shows. The parts, who may import whom and who works on which stand in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), the one document everything is gathered under (the owner's word of 2026-10-30, 09:5x UTC: everything under an architecture document, and work by it).

**The old engine is out.** `src/event_universe/`, its tests, its tools, its example worlds and its readings left the working tree of the branch tensor24-review on 2026-10-30 (the owner's word to the Boss, 09:3x UTC: "Yes, all of it now"; commits 4cb5359ce and 2c87a07ed), after his word to Animate at 09:2x UTC: "The old engine is out already; get updated from the Boss. Only the new engine matters. Arrange everything accordingly." It stands in git's history alone: this README and the documents as they were before the move are at commit c3532282b of the branch scribe-5. Version 4.0.0 on main (4326fecce) is the last release; the branch engine-5.0-test (dfeeb0561) is frozen.

## The law

The law is [docs/ALGEBRA.md](docs/ALGEBRA.md): the postulates at its head, then one bold line per rule, a changed line holding its new wording alone and the former clauses standing by name in its closing section. In short:

- **The Node-clock.** A Node-clock is one place of a cubic lattice with six Meshes to its six neighbours, one through each of its Spokes; the great clock is the lattice wrapped on every axis, a torus. Every Node-clock steps by the same one act in every round: one division with a carried remainder (Rule3) over one integer contraction of its own gears and its six Meshes' gears. It reads itself and its six Meshes and nothing else, forward and backward, and no special code and no specific law states a slowing, a grip, a sending, a receiving, a lengthening, a shortening or a freezing: those are the one act's own results (lines 90 and 92).
- **Whole numbers.** No float, no root, no circular function that makes a phenomenon happen, no table, no loop that makes a formula, no number beyond 0 and 1 in the code, and no division that is not Rule3's; the numbers stand in the three files (lines 96 to 102).
- **Nothing is declared.** No file names a particle, a mass or a coupling: every particle appears by itself in the clicks, and a mass is measured only in clicks (decisions 35 and 37, line 35).
- **The click.** The great clock reads itself, every Node-clock once per tick after the step; there are two kinds of click and no third, and a click credits a train's whole winding (**The two kinds of click**, line 35).

## Description of the system

The machine is a board of clocks: three space axes, a torus whose three sides the piece file gives, a Node-clock at every site with six neighbours, and time each Node-clock's own gear rate, so three dimensions of space and one of time. The description has two systems and a dictionary between them: the logical system is the clocks (each Node-clock a train of gears, the gears of neighbouring clocks meshing, the carry that makes every event, the time gear and gravity, the two kinds of clicks, what is kept), and the tensor system is the same machine as clean tensor (every quantity one of the five kinds of the cube's 24 turns, A1 the scalar, A2 the pseudoscalar, E, T1 the vector, T2 the shears; one act; the step on the mirrored state running it back exactly). The whole description is in [the engine's document](docs/ENGINE.md#description-of-the-system); the build told by the clock, the algebra and the physics is [docs/BIG_PICTURE.md](docs/BIG_PICTURE.md); the law's picture is **The picture over the postulates** in [docs/ALGEBRA.md](docs/ALGEBRA.md). Every solution is made and read by the principle of the clock and the gear (**How to think about solutions** in the law): the clock, the algebra and the physics, starting from the layer that is simplest, the physics after the clicks.

## Run it

Python 3.14 or later is required (`pyproject.toml`, `requires-python = ">=3.14"`). From a checkout's root:

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .   # the environment
python -I tools/tensor24_files.py                         # the three example files in examples/tensor24, checked: every departure named, exit 1 on one
python -I tools/tensor24_run.py examples/tensor24/universe.json examples/tensor24/piece.json examples/tensor24/setting.json record.jsonl   # the run: a record and its ledger
python -I tools/tensor24_decode.py record.jsonl            # the decoder's reading of a record (a ledger beside it may be named)
python tools/check.py                                      # the gates and the affected tests; --full runs the whole suite
```

A world is three files (`examples/tensor24/`): the universe (the integers den, full_rate and width, and the families: a name, its kinds, its part, its pinion), the piece (the board's three sides) and the setting (the gears laid, one row each, and the number of ticks); no file declares a particle, a mass or a coupling.

## The documents

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): the one document that tells the system and the one the work runs from: the parts, the Node-clock first, each told by the clock, the board and the clicks, with its algebra, home, test and status; who may import whom; the glossary.
- [docs/ALGEBRA.md](docs/ALGEBRA.md): the law: the postulates at its head, the decisions in force, one bold line per rule, each clause quoting the owner's words it stands on.
- [CHANGELOG.md](CHANGELOG.md): what changed since the new engine. `tools/derivations/open_items/`: the gate (`SCRIBE-GATE-1.md`), the keeper's records (`SCRIBE-OWNER-WORDS.md`, `SCRIBE-LAW-AUDIT-2.md`) and the derivations, two blind hands per question with their numbers; the law's text is the one place that is current.

The earlier documents (the engine's document, the big picture, the clock words, further research, follow-up papers, the decisions in force and the ledger) left the tree on 2026-10-30, the owner's word: one clean main, the architecture file and the algebra file; they stand in git at scribe-5 3b7fd1bd2.

## The papers

The papers are in [papers/](papers/), one folder each.

**The first paper, [papers/one_rule/](papers/one_rule/):** "Universe24: one simple rule, the formulas it shares with nature and adds" (Alon Gonen, 2026), archived as a preprint on Zenodo ([DOI 10.5281/zenodo.23297864](https://doi.org/10.5281/zenodo.23297864)), its software on Zenodo ([DOI 10.5281/zenodo.23190113](https://doi.org/10.5281/zenodo.23190113)) and at the tag [v1.1.0](https://github.com/Closer24/Universe24/tree/v1.1.0/paper): `Universe24_Paper.tex` with [`Universe24_Paper.pdf`](papers/one_rule/Universe24_Paper.pdf), `Universe24_Supplement.tex` with [`Universe24_Supplement.pdf`](papers/one_rule/Universe24_Supplement.pdf) (the supplementary material, Online Resource 1: the claims list and the algebraic steps of every derivation), the figures with the scripts that draw them (matplotlib, installed as the package's `papers` extra: `python -m pip install -e ".[papers]"`) and the check scripts beside them. What it reproduces in lattice form, the Klein-Gordon equation with Schroedinger's slow limit, Planck's relation in the band's form, the exponential weak-field metric under one assumption fixed by two measurements, frame dragging's form with no number put in, a black-hole shadow of radius 2 e m against the rings the Event Horizon Telescope read, the two slits' row and Bell's and Greenberger-Horne-Zeilinger correlations under the declared counting rule, and what it misses, each beside its measurement with its number, stand in the paper's Sections 5 to 8 and in the claims list of Online Resource 1; the derivation scripts behind its numbers stand in [tools/derivations/](tools/derivations/). The bibliography stands in each file, so either builds from the folder with the class in `sn/` on the input path, twice:

```bash
TEXINPUTS=sn: pdflatex Universe24_Paper.tex && TEXINPUTS=sn: pdflatex Universe24_Paper.tex   # the same for Universe24_Supplement.tex
```

**The time paper, [papers/spacetime_events/](papers/spacetime_events/):** "A discrete spacetime of events in whole numbers: why clocks slow, why nothing outruns light, and why time has a direction only where something was measured" (Alon Gonen, 2026): `Universe24_Discrete_Spacetime_of_Events_Paper.tex` with [`Universe24_Discrete_Spacetime_of_Events_Paper.pdf`](papers/spacetime_events/Universe24_Discrete_Spacetime_of_Events_Paper.pdf), archived as a preprint on Zenodo ([DOI 10.5281/zenodo.23297705](https://doi.org/10.5281/zenodo.23297705)), its [README](papers/spacetime_events/README.md), the run it reports under `run3d_fixed/` and its checks under `tools/`; [`build.sh`](papers/spacetime_events/build.sh) builds the PDF and runs the eight checks, stopping at the first failure. Every step runs back exactly, so no step has a direction of time; a direction appears only where a click is written, the paper's claim, and the one world's chart keeps it: the clicks have the arrow and the great clock none.

```bash
sh papers/spacetime_events/build.sh
```

## The law, the decisions and the derivations

[docs/ALGEBRA.md](docs/ALGEBRA.md) is the law of the lattice and holds the decisions in force, each clause quoting the owner's words it stands on. [tools/derivations/](tools/derivations/) holds the derivations: the hands' folders under `open_items/` (two blind hands on one question, a comparison by the Boss at each landing, the sentence that enters the law written verbatim from it), the conservation kit under `conservations/`, the toys under `toys/`; the documents' gates of `tools/documents_gates.py`, run by `tools/check.py`, hold the documents to the tree.

## Further research

What is open stands by name in section 5 of [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). A contribution that closes one starts from the law's line, as [CONTRIBUTING.md](CONTRIBUTING.md) says.

## Contributing

Contributions are welcome, through forks and pull requests. A physics change starts from the law's line in [docs/ALGEBRA.md](docs/ALGEBRA.md), on the owner's word, the old clause kept by name and dated, and every change runs `python tools/check.py`. The rules and the checks are in [CONTRIBUTING.md](CONTRIBUTING.md). An error in a derivation, a disagreement with a measurement or a reproduction that fails is reported through the issue template, as [CONTRIBUTING.md](CONTRIBUTING.md) describes.

## Licence and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and archived on Zenodo under the concept DOI [10.5281/zenodo.23466436](https://doi.org/10.5281/zenodo.23466436) (the releases from 3.0.0 on, resolving to the latest version; the versions 1.1.0 to 2.1.0 under the concept DOI [10.5281/zenodo.23190113](https://doi.org/10.5281/zenodo.23190113)), version 4.0.0 (main's tree of 0fcc0403d, the tag v4.0.0 the owner's push of 2026-10-25) under no version DOI, the engine 5.0 of this branch under test and no release, version 3.0.0 under [10.5281/zenodo.23466437](https://doi.org/10.5281/zenodo.23466437), version 2.1.0 under [10.5281/zenodo.23421502](https://doi.org/10.5281/zenodo.23421502), version 2.0.0 under [10.5281/zenodo.23289515](https://doi.org/10.5281/zenodo.23289515); cite it with [CITATION.cff](CITATION.cff). The author used a large language model (Claude, Anthropic, through Claude Code, 2026) as a tool under the author's direction for the computations, the derivations and their checks and the drafting of the text; the model is not an author, and the author reviewed every statement and takes full responsibility for the content.

## About the Author

Universe24 is an independent research project by **Alon Gonen**, founder of **Plus500** and **deFounder**.

- [deFounder website](https://defounder.ai)
- [Alon's Linktree](https://linktree.defounder.ai)
