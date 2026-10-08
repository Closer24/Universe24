# Universe24

Universe24 is the clicks of one line of integer arithmetic: a cubic lattice of Nodes, two integer levels and a remainder per part of a field, stepped by one recurrence, Rule3, from a Node's present, past and six neighbours, reversibly and covariantly under the cube's 48. The lattice is read only through declared counting regions, NodeDetectors, its clicks the only measurements, each the meeting of the forward field with the transition read backward. From it follow, in lattice form, the Klein-Gordon equation with Schroedinger's slow limit, Planck's relation in the band's form and, under one assumption fixed by two measurements, the exponential weak-field metric; the lattice's own terms stand under their conditions, predictions where unread, bounded where read; Bell's and Greenberger-Horne-Zeilinger correlations follow from the declared counting rule; the misses are named, a decelerating cosmology among them. The paper has one claim: that Universe24 helps compute things in nature. It does not claim that nature is such a lattice.

## The aim

This repository is meant to be carried on. Its aim is a complete physics in integers: a world of one rule and its clicks that shows what nature shows, built experiment by experiment by the paper's method, a declared universe, a blind row written before the first run, the clicks against the measurement. What stands today is what the paper computes of nature, the hits and the misses alike; what is open is named below, and anyone may take a piece of it. The paper's one claim is that Universe24 helps compute things in nature, and the repository's aim is to make that claim wider, formula by formula.

## The paper

The paper, "Universe24: one simple rule, the formulas it shares with nature and adds" (Alon Gonen, 2026), submitted to Foundations of Physics, is in [paper/general_formula/](paper/general_formula/): `main.tex` with [`main.pdf`](paper/general_formula/main.pdf), `supplement.tex` with [`supplement.pdf`](paper/general_formula/supplement.pdf) (the supplementary material, Online Resource 1: the claims list and the algebraic steps of every derivation), the journal's abstract in `abstract_journal.txt`, the figures with the scripts that draw them and the check scripts beside them. The bibliography stands in each file, so either builds from the folder with the class in `sn/` on the input path, twice:

```bash
TEXINPUTS=sn: pdflatex main.tex && TEXINPUTS=sn: pdflatex main.tex   # the same for supplement.tex
```

## The law

[docs/ALGEBRA.md](docs/ALGEBRA.md) is the law of the lattice, one algebraic line per rule, the document the paper cites by the name of its section.

## The decisions

[docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) holds the decisions in force, one line each: every decision of the model owner that a line of the law or the engine rests on.

## The derivations

[tools/derivations/](tools/derivations/) holds the derivations of the law's numbers in Python, each from Rule3's line as the law states it and leaning on no run of the engine: its root is `rule3.py`, the line and its invariants transcribed sentence by sentence, and every other module imports it and derives its numbers from it; beside them stand the machine checks of the law's and the paper's theorems and identities (`proofs_inventory.json`, one row per statement with its check and its verdict). The documents gate of `tests/test_documents.py` holds every number of `tools/numbers.json` that carries a derivation rule to its function's output, to the digits named, and `tests/test_proofs_check_the_law.py` runs every check to its verdict; the folder's own [README](tools/derivations/README.md) states its rules and its inventory.

## The implementation

The repository also holds an implementation for building worlds, frozen before the odd write of the paper's Section 2.3; the two slits' run of Section 6 is its one run the paper reports, at the state the run's record names, on a universe with gravity off in all but name, so the run is the law's line as Section 2.2 states it, nothing of Section 5.1's vector sector rests on it, and no other claim of the paper does. Its code is `src/event_universe/`, its tests `tests/` and its document [docs/ENGINE.md](docs/ENGINE.md), the engine as the code holds it at the freeze. From a clone to the two slits' page, six commands from the checkout's root:

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .   # the environment: Python 3.14 and the package
PYTHONPATH=src python tools/run_inputs.py --out runs/two_slits examples/events/two_slits/two_slits.json   # the run, headless: one line per world with its verdict and intervals, the output file into --out
PYTHONPATH=src python tools/click_counts.py --world examples/events/two_slits/two_slits.json --output runs/two_slits/two_slits.output.json --expectation examples/events/two_slits/expectation.json   # the reading: the clicks per region beside the blind's row
PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json --intervals 130 --out runs/two_slits/two_slits.look.json   # the look: every family's arrays per interval, a lattice reading labelled so
PYTHONPATH=src python tools/look/page.py runs/two_slits/two_slits.look.json --blind examples/events/two_slits/expectation.json --out runs/two_slits/two_slits.look.html   # the page: the board frame by frame, the NodeDetectors' bars beside the dashed blind curve
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json   # the back-in-time gate: the world run forward and back, MATCH or the first difference by name
```

## The two slits' universe

[examples/events/two_slits/](examples/events/two_slits/) is the declared universe of the paper's Section 6: its design (`design.json`, every number with its reason), its world `two_slits.json` on the universe file `examples/events/light.json`, its blind row written before any run (`expectation.json`) and its reading beside the blind (`blind_and_reading.md`). The other folders under `examples/events/` are the worlds the implementation's tests load; no claim of the paper rests on them.

## What you can build with it

A world is a universe file and nothing else: the families with their bands and the holders they read, the bodies with their counts, the NodeDetectors as declared counting regions, the box's size and its axes, periodic, open or folded, and its walls with slits. The engine steps the file in bounded integers by the one line, Rule3; the clicks of the NodeDetectors are the measurement, and the look page draws every family's arrays frame by frame. Any experiment that can be declared as such a file and read through clicks can be run this way: a source, a wall with one slit or two or with any declared pattern of gaps, a body at rest (a moving body's lay is named in docs/ENGINE.md's section 10 as not built), light meeting matter. [docs/ENGINE.md](docs/ENGINE.md) states the file's rows (section 4), the output (section 5), how to run a world (section 6), how to add a family (section 7) and how to build an experiment with its blind row written before the first run (section 9); the two slits' folder is the worked example.

The paper's method does not need a run: [tools/derivations/](tools/derivations/) computes the law's numbers from Rule3's line alone, and a new formula of the law is derived the same way, its line in [docs/ALGEBRA.md](docs/ALGEBRA.md) first.

The directions open to anyone: a larger Gamma with the one-way face (the paper's Section 8.3, what a world closer to nature needs), larger boxes and longer runs, the computations the engine leaves undone (docs/ENGINE.md, section 10, a Big Bang world among them, named there as an opening for others), the bound bodies' numbers where the model misses nature (Section 8.1), the integer-step form of the stability theorem (Section 4.2), and the rendering of tools/look/. The lattice is the simple cubic lattice with the cube's group of 48 and the rule is Rule3: another lattice or another rule is a hypothesis under its own name, as [CONTRIBUTING.md](CONTRIBUTING.md) says.

## Open problems

What the model misses and what a world closer to nature needs are named in the paper, Section 8: 8.1 the misses, with their numbers, 8.2 what is put in, 8.3 what a world closer to nature needs. The computations the implementation leaves undone are named in [docs/ENGINE.md](docs/ENGINE.md), section 10 (the Zeno worlds not re-run at the frozen hash, the holders' swing under a body laid off the step's fixed point, the moving body's lay declared and not built). A contribution that closes one starts from the law's line, as [CONTRIBUTING.md](CONTRIBUTING.md) says.

## Contributing

Contributions are welcome, through forks and pull requests. A physics change starts from the law's line in [docs/ALGEBRA.md](docs/ALGEBRA.md) and passes the three tests, generic, vector and local, before it enters, and every change runs `python tools/check.py`. The rules and the checks are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and archived on Zenodo under the concept DOI [10.5281/zenodo.23190113](https://doi.org/10.5281/zenodo.23190113); cite it with [CITATION.cff](CITATION.cff). The author used a large language model (Claude, Anthropic, through Claude Code, 2026) as a tool under the author's direction for the computations, the derivations and their checks and the drafting of the text; the model is not an author, and the author reviewed every statement and takes full responsibility for the content.
