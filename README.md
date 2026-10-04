# Universe24

Universe24 is a three-dimensional event simulator, the implementation of Reality
Theory: a lattice of Nodes joined by Links through six Ports each, bounded
integer arithmetic and one local rule, Rule3. Every family of a universe file is a
record stepped by Rule3 from its own levels and its six neighbours'; the engine
holds no number of physics, every value comes from the run's files; only a
NodeReader's click is a measurement, and every other number a run writes is a
Lattice reading labelled so.

The repository holds the engine (`src/event_universe/`), the tools that lay, run,
gate and read a world (`tools/`) and the experiments that gate the engine
(`examples/events/`), each one folder with its design, its worlds, its blind
written before any run and its reading.

The paper that states the method and its one claim, with its supplement of
derivations, is in [paper/](paper/README.md) (`paper/general_formula/main.tex` and
`supplement.tex`, built by the scripts there); the documents it cites are
[docs/ALGEBRA.md](docs/ALGEBRA.md), [docs/ENGINE.md](docs/ENGINE.md) and
[docs/HIGHLIGHTS.md](docs/HIGHLIGHTS.md).

## Seeing the experiments

An experiment is one folder under `examples/events/`: its design (`design.json`,
every number with its reason), its universe file, its world files with the
generator's mode file beside each, its builder (`build_world.py`) and its blind
(`expectation.json`), written before any run and never edited after. Where the
folder holds a `blind_and_reading.md`, the reading stands there beside the blind;
a reading that misses the blind is written as a finding by name, and the blind is
not adjusted. Every reader prints the blind beside its reading and compares
nothing. File names in the table are relative to the experiment's folder.

| Experiment | What it shows | World files | Blind | Reader | Page |
| --- | --- | --- | --- | --- | --- |
| [two_slits](examples/events/two_slits/) | The click experiment, "fringes are clicks, because a person sees them": a packet of light through a wall with two gaps onto a screen of twelve NodeReader regions, the clicks per region read beside the blind's Huygens row. | `two_slits.json` | `expectation.json` | `tools/click_counts.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [bell](examples/events/bell/) | Bell as the engine's gate, "two simple worlds show the engine works": the pair family laid as one event on a chain, one beam to each side's region with its setting as its `basis`, S over the four worlds. | `bell_a_b.json`, `bell_a_b_prime.json`, `bell_a_prime_b.json`, `bell_a_prime_b_prime.json` | `expectation.json` | `tools/bell_gate.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [ghz](examples/events/ghz/) | The GHZ gate: the GHZ family's four real lines laid as one event on a square board, one beam to each of three sides' regions with its setting as its `basis` and its `pattern`, Mermin's M over the four worlds. | `ghz_x_y_y.json`, `ghz_y_x_y.json`, `ghz_y_y_x.json`, `ghz_x_x_x.json` | `expectation.json` | `tools/bell_gate.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [which_way](examples/events/which_way/) | The experiment of the heart: the two slits with a declared region at one gap backed by a face, three worlds from one design; the blind's comparison, the which-way world's screen row equals the one-gap world's within the draw's scatter and both differ from the two-gaps world's at the two slits' minima and maxima. | `which_way.json`, `one_gap.json`, `two_gaps.json` | `expectation.json`, read in `blind_and_reading.md` | the run's `credit` lines per region, asserted by `tests/test_the_draw.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [matter_alone](examples/events/matter_alone/) | World (i) of the families round, matter alone: one body of the matter family at rest on the rule's own universe on an open box, its rest rotation, tail, drift and form read as lattice readings (the world declares no NodeReader). | `pixel.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/body_rest.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [standing_body](examples/events/standing_body/) | The body round, part 1: one neutral body of the matter family at the centre of the open 25-cube, laid at the integer fixed point under its own paces, its drift, its share's deviation and its rotation read as lattice readings. | `standing_15.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/body_standing.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [shelved_ion](examples/events/shelved_ion/) | The click round's characterising experiment, the shelved ion's telegraph: one ion of three parts (S, P and D) declared a NodeReader at its one Node under two drives, with a counter about it, its counts per bin, its bright and dark periods and its switches; a finding by name, read beside its blind. | `shelved_ion.json`, `shelved_ion_control.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/telegraph.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [zeno](examples/events/zeno/) | The quantum Zeno world (the paper's S.59): one record of two parts (g, e) declared a NodeReader under a drive's pi pulse, reading its own parts n times over the run, one world per probe count n in {1, 2, 4, 8, 16}, the fraction of trials ending in e beside Itano's column. | `zeno_1.json`, `zeno_2.json`, `zeno_4.json`, `zeno_8.json`, `zeno_16.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/meeting_trials.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [zeno_pulsed](examples/events/zeno_pulsed/) | The pulsed quantum Zeno gate (the paper's S.59 under the window bounded by the lays' schedule): the Zeno world's body with a probe record laid whole at its own Node n times over the pi time, Itano's protocol of n pulses; a finding by name, read beside its blind. | `zeno_pulsed_1.json`, `zeno_pulsed_2.json`, `zeno_pulsed_4.json`, `zeno_pulsed_8.json`, `zeno_pulsed_16.json`, `zeno_pulsed_32.json`, `zeno_pulsed_64.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/meeting_trials.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [anticoincidence](examples/events/anticoincidence/) | One photon on two bodies, the anticoincidence (the paper's S.57): one light quantum laid as two packets toward two records declared NodeReaders, with a two-photon control, the takings at A alone, at B alone, at both and at neither, and alpha = P(both) / (P(A) P(B)). | `one_photon.json`, `two_photons.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/meeting_trials.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [resonance](examples/events/resonance/) | Test (vi): the born light's frequency read in the engine, a quantum given as a source in time at one Node and taken at a far Node by a taker at the same resonance or detuned; a finding by name, read beside its blind. | `resonant.json`, `detuned.json` | `expectation.json`, read in `blind_and_reading.md` | `tools/meeting_trials.py` and the folder's `read_world.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [neutron_conversion](examples/events/neutron_conversion/) | The neutron's conversion: a record of three real lines converted whole at its Node into the proton, the electron and the antineutrino at a declared rate, the counts, the senses, the shares, the rate and the back-in-time gate across the conversion. | `neutron_conversion.json` | `expectation.json`, read in `blind_and_reading.md` | the folder's `read_world.py` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [packet_giving](examples/events/packet_giving/) | The emitter NodeReader's step 5: the open board's giving as a packet along a drawn axis, read in the engine by a NodeReader at the derived reach; a finding by name, read beside its blind. | `packet_giving.json` | `expectation.json`, read in `blind_and_reading.md` | the folder's `build_world.py --read` | `tools/look/record.py`, then `tools/look/page.py --blind` |
| [pair_atom](examples/events/pair_atom/) | The pair of two bound records, a hypothesis under its own name, its world not run: two bound records are one record of two parts, the centre's part carrying the pair's whole rest and count and the relative part laid for its inertia alone about a pinned centre, so that the atom's bound modes hold with m* replaced by mu; the toy of two equal records at matter's pair, whose relative part the loader derives at the declared den, with the blind written beside it before any run. | `pair.json` (the toy universe), `positronium_toy.json` | `expectation.json`, read in `blind_and_reading.md` | none yet: the folder's `build_world.py` writes the universe, the world and the blind; the world loads (`load_world`), and its run and the beat's reading against mu / m* = 1 / 2 belong to the experimenter | `tools/look/record.py`, then `tools/look/page.py --blind` |

From a clone to the two slits' page, six commands from the checkout's root:

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .   # the environment: Python 3.14 and the package
PYTHONPATH=src python tools/run_inputs.py --out runs/two_slits examples/events/two_slits/two_slits.json   # the run, headless: one line per world with its verdict and intervals, the output file into --out
PYTHONPATH=src python tools/click_counts.py --world examples/events/two_slits/two_slits.json --output runs/two_slits/two_slits.output.json --expectation examples/events/two_slits/expectation.json   # the reading: the clicks per region beside the blind's row
PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json --ticks 130 --out runs/two_slits/two_slits.look.json   # the look: every family's arrays per interval, a lattice reading labelled so
PYTHONPATH=src python tools/look/page.py runs/two_slits/two_slits.look.json --blind examples/events/two_slits/expectation.json --out runs/two_slits/two_slits.look.html   # the page: the board frame by frame, the NodeReaders' bars beside the dashed blind curve
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json   # the back-in-time gate: the world run forward and back, MATCH or the first difference by name
```

The same path holds for every row with its own files: `tools/run_inputs.py` takes
several worlds by name (never a glob over a folder, which takes the mode files),
`tools/bell_gate.py --outputs` reads a gate's four output files together, and a
reader of trials or of a body (`tools/meeting_trials.py --world --design
--expectation`, `tools/body_rest.py`, `tools/body_standing.py`) steps the world
itself. The run's output folder, the look and the page are built outside the
repository's tracked files from the run's output and are not committed.

The three documents: [the law](docs/ALGEBRA.md), one algebraic line per rule;
[the engine](docs/ENGINE.md), the input files, the interval, the output, how to
run a world and how to build an experiment; [the decisions](docs/HIGHLIGHTS.md),
one line each. Contributors start with [AGENTS.md](AGENTS.md) and
[CONTRIBUTING.md](CONTRIBUTING.md).

To build an experiment of your own (a universe file, a world, its blind written
first, the run and its reading), follow the engine's section
[How to build an experiment](docs/ENGINE.md#9-how-to-build-an-experiment), the
recipe as the shipped folders have it. Before a pull request, follow
[CONTRIBUTING.md](CONTRIBUTING.md) and run `python tools/check.py`.

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and
archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746); cite it with
[CITATION.cff](CITATION.cff).
