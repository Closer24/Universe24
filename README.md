# Universe24

**The paper:** [Universe24_Paper.pdf](paper/Universe24_Paper.pdf) · [supplement, Online Resource 1](paper/Universe24_Supplement.pdf) · [Zenodo DOI 10.5281/zenodo.23190113](https://doi.org/10.5281/zenodo.23190113)

Universe24 is the clicks of one line of integer arithmetic: a cubic lattice of Nodes, two integer levels and a remainder per part of a field, stepped by one recurrence, Rule3, from a Node's present, past and six neighbours, reversibly and covariantly under the cube's 48. The lattice is read only through declared counting regions, NodeDetectors, its clicks the only measurements, each the meeting of the forward field with the transition read backward. From it follow, in lattice form, the Klein-Gordon equation with Schroedinger's slow limit, Planck's relation in the band's form and, under one assumption fixed by two measurements, the exponential weak-field metric; the lattice's own terms stand under their conditions, predictions where unread, bounded where read; Bell's and Greenberger-Horne-Zeilinger correlations follow from the declared counting rule; the misses are named, a decelerating cosmology among them. The paper has one claim: that Universe24 helps compute things in nature. It does not claim that nature is such a lattice.

## The aim

This repository is meant to be carried on. Its aim is a complete physics in integers: a world of one rule and its clicks that shows what nature shows, built experiment by experiment by the paper's method, a declared universe, a blind row written before the first run, the clicks against the measurement. What stands today is what the paper computes of nature, the hits and the misses alike; what is open is named below, and anyone may take a piece of it. The paper's one claim is that Universe24 helps compute things in nature, and the repository's aim is to make that claim wider, formula by formula.

## In plain words

Suppose nature is discrete: space is made of Nodes, and between one Node and the next nothing moves faster than light. The distance between Nodes is then smaller than anything measured, so a cubic centimetre holds an astronomical number of them. No centre can know the state of all of them and decide for all of them; each Node must act on its own, by a rule of its own, seeing only itself and its six neighbours. That rule is what this repository holds: one line of integer arithmetic, with no free parameter.

The rule, Rule3, is this. A Node holds a few bounded integers: its level now, its level one interval before, and a remainder. At every interval it computes its next level in five steps: it takes the levels of its six neighbours, each with a weight; adds its own level with a weight of its own; subtracts its level of the interval before; adds the remainder it carried; and divides the sum by a fixed integer. The quotient is the new level; the remainder stays at the Node for the next interval. Because the remainder is kept, nothing is lost, and the rule is exactly reversible: a world run backward returns its past exactly.

The weights are not chosen by hand. They come from the family's pair of integers (one pair for light, one for a massive family) and from the Node's paces, the rate of its clock against its neighbours' through the Links; the differences of pace between Nodes are what gravity is here. At the vacuum's paces the rule reduces to a discrete wave equation, and from that line the paper derives its formulas: the ones nature shows and the ones it adds.

A world is read only through clicks: declared counting regions, NodeDetectors, whose counts are the one measurement. The paper's one claim is that this rule helps compute things in nature, and every number it prints is reproduced by a script in this repository.

## The paper

The paper, "Universe24: one simple rule, the formulas it shares with nature and adds" (Alon Gonen, 2026), archived on Zenodo and at the tag v1.1.0, is in [paper/](paper/): `Universe24_Paper.tex` with [`Universe24_Paper.pdf`](paper/Universe24_Paper.pdf), `Universe24_Supplement.tex` with [`Universe24_Supplement.pdf`](paper/Universe24_Supplement.pdf) (the supplementary material, Online Resource 1: the claims list and the algebraic steps of every derivation), the journal's abstract in `abstract_journal.txt`, the figures with the scripts that draw them and the check scripts beside them. The bibliography stands in each file, so either builds from the folder with the class in `sn/` on the input path, twice:

```bash
TEXINPUTS=sn: pdflatex Universe24_Paper.tex && TEXINPUTS=sn: pdflatex Universe24_Paper.tex   # the same for Universe24_Supplement.tex
```

## The law

[docs/ALGEBRA.md](docs/ALGEBRA.md) is the law of the lattice, one algebraic line per rule, the document the paper cites by the name of its section.

## The decisions

[docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md) holds the decisions in force, one line each: every decision of the model owner that a line of the law or the engine rests on.

## The derivations

[tools/derivations/](tools/derivations/) holds the derivations of the law's numbers in Python, each from Rule3's line as the law states it and leaning on no run of the engine: its root is `rule3.py`, the line and its invariants transcribed sentence by sentence, and every other module imports it and derives its numbers from it; beside them stand the machine checks of the law's and the paper's theorems and identities (`proofs_inventory.json`, one row per statement with its check and its verdict). The documents gate of `tests/test_documents.py` holds every number of `tools/numbers.json` that carries a derivation rule to its function's output, to the digits named, and `tests/test_proofs_check_the_law.py` runs every check to its verdict; the folder's own [README](tools/derivations/README.md) states its rules and its inventory.

## The implementation

The repository also holds an implementation for building worlds, the engine: on main the engine V2 (the next section), and at the tag v1.1.0 the paper's engine, frozen before the odd write of the paper's Section 2.3; the two slits' run of Section 6 is the tag's one run the paper reports, at the state the run's record names, on a universe with gravity off in all but name, so the run is the law's line as Section 2.2 states it, nothing of Section 5.1's vector sector rests on it, and no other claim of the paper does. Its code is `src/event_universe/`, its tests `tests/` and its document [docs/ENGINE.md](docs/ENGINE.md), the engine as the code holds it on main, with the tag's known issues in its section 10. From a clone to the two slits' page, six commands from the checkout's root:

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .   # the environment: Python 3.14 and the package
PYTHONPATH=src python tools/run_inputs.py --out runs/two_slits examples/events/two_slits/two_slits.json   # the run, headless: one line per world with its verdict and intervals, the output file into --out
PYTHONPATH=src python tools/click_counts.py --world examples/events/two_slits/two_slits.json --output runs/two_slits/two_slits.output.json --expectation examples/events/two_slits/expectation.json   # the reading: the clicks per region beside the blind's row
PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json --intervals 130 --out runs/two_slits/two_slits.look.json   # the look: every family's arrays per interval, a lattice reading labelled so
PYTHONPATH=src python tools/look/page.py runs/two_slits/two_slits.look.json --blind examples/events/two_slits/expectation.json --out runs/two_slits/two_slits.look.html   # the page: the board frame by frame, the NodeDetectors' bars beside the dashed blind curve
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json   # the back-in-time gate: the world run forward and back, MATCH or the first difference by name
```

To run the engine the paper reports, take the tag v1.1.0 (or the source archive of the Zenodo record 10.5281/zenodo.23202100); main carries the engine in progress, changed only by pull requests that enter a line of the law with its three tests.

## The engine V2

The engine on main, V2, is Rule3 and nothing else: every act on a level is Rule3's one carried division with the remainder kept, and what remains is a coefficient's single division or a search by comparing integers. In plain words: the shears that turned a record are gone, the rotation act is gone, no square root is taken anywhere, no sine or cosine is called, no table is read; the phase of a charged record lives on the Links as a pair of Rule3 lines turned one fixed angle at a time, and gravity's odd lines ride the same fold. Three tests keep it so: no root anywhere, no shear and no rotation act, and a table that lists every division in the engine with its kind and fails on any new one. Momentum is conserved at a click: Rule3 conserves a lattice momentum exactly, and at a click the taker is given one whole piece's momentum by a twist of its lines, the loss booked by name where a declared instrument cannot carry it; the click has two receivers, the piece's source folded back by the same twist and booked with its recoil; what a body measures of another in two-way clicks never exceeds c, Lorentz's composition exactly. The paper's engine is the tag v1.1.0, unchanged; what changed from it, version by version, is in [CHANGELOG.md](CHANGELOG.md), and the open items stand by name in [docs/ENGINE.md](docs/ENGINE.md), section 10.

The next step is the time paper, the arrow of time as the detector's record, its blind and its run.

## The two slits' universe

[examples/events/two_slits/](examples/events/two_slits/) is the declared universe of the paper's Section 6: its design (`design.json`, every number with its reason), its world `two_slits.json` on the universe file `examples/events/light.json`, its blind row written before any run (`expectation.json`) and its reading beside the blind (`blind_and_reading.md`). The other folders under `examples/events/` are the worlds the implementation's tests load; no claim of the paper rests on them.

## What you can build with it

A world is a universe file and nothing else: the families with their bands and the holders they read, the bodies with their counts, the NodeDetectors as declared counting regions, the box's size and its axes, periodic, open or folded, and its walls with slits. The engine steps the file in bounded integers by the one line, Rule3; the clicks of the NodeDetectors are the measurement, and the look page draws every family's arrays frame by frame. Any experiment that can be declared as such a file and read through clicks can be run this way: a source, a wall with one slit or two or with any declared pattern of gaps, a body at rest, light meeting matter. [docs/ENGINE.md](docs/ENGINE.md) states the file's rows (section 4), the output (section 5), how to run a world (section 6), how to add a family (section 7) and how to build an experiment with its blind row written before the first run (section 9); the two slits' folder is the worked example.

The paper's method does not need a run: [tools/derivations/](tools/derivations/) computes the law's numbers from Rule3's line alone, and a new formula of the law is derived the same way, its line in [docs/ALGEBRA.md](docs/ALGEBRA.md) first.

The directions open to anyone: a larger Gamma with the one-way face (the paper's Section 8.3, what a world closer to nature needs), larger boxes and longer runs, the computations the engine leaves undone (docs/ENGINE.md, section 10, a Big Bang world among them, named there as an opening for others), the bound bodies' numbers where the model misses nature (Section 8.1), the integer-step form of the stability theorem (Section 4.2), and the rendering of tools/look/. The lattice is the simple cubic lattice with the cube's group of 48 and the rule is Rule3: another lattice or another rule is a hypothesis under its own name, as [CONTRIBUTING.md](CONTRIBUTING.md) says.

## Open problems

What the model misses and what a world closer to nature needs are named in the paper, Section 8: 8.1 the misses, with their numbers, 8.2 what is put in, 8.3 what a world closer to nature needs. The computations the implementation leaves undone are named in [docs/ENGINE.md](docs/ENGINE.md), section 10 (the Zeno worlds not re-run at the frozen hash, the holders' swing under a body laid off the step's fixed point, the engine V2's open items). A contribution that closes one starts from the law's line, as [CONTRIBUTING.md](CONTRIBUTING.md) says.

## Contributing

Contributions are welcome, through forks and pull requests. A physics change starts from the law's line in [docs/ALGEBRA.md](docs/ALGEBRA.md) and passes the three tests, generic, vector and local, before it enters, and every change runs `python tools/check.py`. The rules and the checks are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence and citation

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and archived on Zenodo under the concept DOI [10.5281/zenodo.23190113](https://doi.org/10.5281/zenodo.23190113); cite it with [CITATION.cff](CITATION.cff). The author used a large language model (Claude, Anthropic, through Claude Code, 2026) as a tool under the author's direction for the computations, the derivations and their checks and the drafting of the text; the model is not an author, and the author reviewed every statement and takes full responsibility for the content.
