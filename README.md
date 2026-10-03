# Universe24

Universe24 is a three-dimensional event simulator, the implementation of Reality
Theory: a GameBoard of Nodes joined by Links, bounded integer arithmetic and one
local rule, Rule3. Every family of the universe file is a record stepped by Rule3
from its own levels and its six neighbours'; only a NodeReader's click is a
measurement, and every other number a run writes is a GameBoard reading labelled so.

The repository holds the engine (`src/event_universe/`), the tools that lay, run,
gate and read a world (`tools/`), and the worlds that gate the engine:

- the two slits, `examples/events/two_slits/two_slits.json`: a packet of light
  through a wall with two gaps onto a screen of twelve regions, its blind
  expectation `expectation.json` beside it, read by `tools/click_counts.py`;
- Bell, `examples/events/bell/bell_a_b.json` and its three sisters: the pair
  family, two real lines of light laid as one event on a chain, one beam to each
  side's region with its setting as its `basis`, the blind `expectation.json`
  beside them (S = 478 / 169 exactly), read by `tools/bell_gate.py`;
- the GHZ gate, `examples/events/ghz/ghz_x_y_y.json` and its three sisters: the
  GHZ family, four real lines of light laid as one event on a square board, three
  beams to three regions with their settings as their `basis` and their declared
  `pattern`, the blind `expectation.json` beside them (M = -4 exactly, local
  realism at most 2), read by the same `tools/bell_gate.py`; the back-in-time
  gate, `tools/back_in_time.py`, says MATCH on every world;
- and the families round's worlds, each one family's act on the rule's own
  rows, each folder its `design.json`, its `build_world.py` and its blind
  `expectation.json` written first from the advisor's numbers:
  `examples/events/matter_alone/` (matter alone: the compact pixel on the open
  25-cube, the rest rotation, the tail and the drift); the body's world is read by `tools/body_rest.py`, a
  GameBoard reading of a body's rotation, tail, centroid and well and of every
  held row's level along the axes from its centre, and of the regions' field lines
  from a run's output;
- and the shelved ion's telegraph, `examples/events/shelved_ion/`, the click
  round's characterising experiment declared before any run: one ion of three
  modes as the parts of one record (the shape [3, 2], the labels S, P and D), two
  drives as two holders of the sign circulating as plane waves on a periodic box,
  the two giving rates declared and one counter about the ion, with its
  `design.json` (every integer with its reason) and its blind `expectation.json`
  (the counts per bin bimodal, the bright periods exponential at the Zeno-limited
  shelving rate, the dark periods at the declared return rate; the control
  unimodal); run on the night of 2026-10-03 with the ion a record declared a
  NodeReader at its one Node (`src/event_universe/meeting.py`), both worlds
  refused inside the run by the amplitude bound, the reading beside the blind in
  its `blind_and_reading.md` (`tools/telegraph.py`), a finding by name;
- the quantum Zeno world, `examples/events/zeno/`, and the anticoincidence
  world, `examples/events/anticoincidence/` (the paper's S.59 and S.57): one
  record of two parts declared a NodeReader at one Node under a drive's pi
  pulse, reading its own parts n times, and two such records on either side of
  one light quantum, each with its design, its blind written before any run and
  its `blind_and_reading.md`, read by `tools/meeting_trials.py` over the
  design's seeds.
- the which-way world, `examples/events/which_way/`, the experiment of the heart:
  the two slits with a declared region at one gap backed by a face, three worlds
  from one design with the blind written before any lay, read beside it in its
  `blind_and_reading.md` and asserted by `tests/test_the_draw.py`.
- the resonance world, `examples/events/resonance/`, test (vi): the born light's
  frequency, a quantum given as a source in time at one Node over the lifetime at
  the transition's declared resonance and read at a far Node, beside a taker at
  the same resonance and one detuned, with the blind written before any lay and
  the reading in its `blind_and_reading.md`.

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

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .
PYTHONPATH=src python tools/run_inputs.py --out runs/first examples/events/two_slits/two_slits.json
PYTHONPATH=src python tools/click_counts.py --world examples/events/two_slits/two_slits.json --output runs/first/two_slits.output.json --expectation examples/events/two_slits/expectation.json
PYTHONPATH=src python tools/run_inputs.py --out runs/bell examples/events/bell/bell_a_b.json examples/events/bell/bell_a_b_prime.json examples/events/bell/bell_a_prime_b.json examples/events/bell/bell_a_prime_b_prime.json
PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/bell/expectation.json --outputs runs/bell/bell_a_b.output.json runs/bell/bell_a_b_prime.output.json runs/bell/bell_a_prime_b.output.json runs/bell/bell_a_prime_b_prime.output.json
PYTHONPATH=src python tools/run_inputs.py --out runs/ghz examples/events/ghz/ghz_x_y_y.json examples/events/ghz/ghz_y_x_y.json examples/events/ghz/ghz_y_y_x.json examples/events/ghz/ghz_x_x_x.json
PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/ghz/expectation.json --outputs runs/ghz/ghz_x_y_y.output.json runs/ghz/ghz_y_x_y.output.json runs/ghz/ghz_y_y_x.output.json runs/ghz/ghz_x_x_x.output.json
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json
PYTHONPATH=src python examples/events/matter_alone/build_world.py --modes
PYTHONPATH=src python tools/body_rest.py --expectation examples/events/matter_alone/expectation.json examples/events/matter_alone/pixel.json
```

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and
archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746); cite it with
[CITATION.cff](CITATION.cff).
