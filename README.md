# Universe24

Universe24 is a three-dimensional event simulator, the implementation of Reality
Theory: a GameBoard of Nodes joined by Links, bounded integer arithmetic and one
local rule, Rule3. Every family of the universe file is a record stepped by Rule3
from its own levels and its six neighbours'; only a detector's click is a
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
- and the rotation round's look, `examples/events/like_or_unlike/`: two bodies of
  the charged family on a chain, like or unlike senses, under the holder of the
  sign's declared act `rotation`, with the neutral and the plain controls and the
  blind `expectation.json` written first, a GameBoard reading of the bodies'
  drifts by `tools/body_drift.py` and no measurement;
- and the families round's five worlds, each one family's act on the rule's own
  rows, each folder its `design.json`, its `build_world.py` and its blind
  `expectation.json` written first from the advisor's numbers, to be run once on
  the finished engine: `examples/events/matter_alone/` (matter alone: the compact
  pixel on the open 25-cube and the cloud on the 41-cube, the rest rotation, the
  tail and the drift), `examples/events/matter_and_gravity/` (the massless row's
  rest about a pixel in levels, 3 G(r) s, on its own universe with gravity at the
  level weight 10), `examples/events/matter_and_binding/` (two pixels twelve Links
  apart, Yukawa's range, the beat and the parting, the field lines of two regions),
  `examples/events/charge/` (a charged body's Wronskian sourcing the holder of the
  sign at the level weight 1, like and unlike senses under the plain read) and
  `examples/events/light_and_charge/` (a packet of light along a tube past a
  neutral and past a charged pixel onto a screen of regions, the arrival and the
  delay by the content's index, the sign's 0, read by `tools/click_counts.py`); the
  bodies' worlds are read by `tools/body_rest.py`, a GameBoard reading of a body's
  rotation, tail, centroid and well and of every held row's level along the axes
  from its centre, and of the regions' field lines from a run's output.

The three documents: [the law](docs/ALGEBRA.md), one algebraic line per rule;
[the engine](docs/ENGINE.md), the input files, the interval, the output and how
to run a world; [the decisions](docs/HIGHLIGHTS.md), one line each. Contributors
start with [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
python3.14 -m venv .venv && source .venv/bin/activate && python -m pip install -e .
PYTHONPATH=src python tools/run_inputs.py --out runs/first examples/events/two_slits/two_slits.json
PYTHONPATH=src python tools/click_counts.py --world examples/events/two_slits/two_slits.json --output runs/first/two_slits.output.json --expectation examples/events/two_slits/expectation.json
PYTHONPATH=src python tools/run_inputs.py --out runs/bell examples/events/bell/bell_a_b.json examples/events/bell/bell_a_b_prime.json examples/events/bell/bell_a_prime_b.json examples/events/bell/bell_a_prime_b_prime.json
PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/bell/expectation.json --outputs runs/bell/bell_a_b.output.json runs/bell/bell_a_b_prime.output.json runs/bell/bell_a_prime_b.output.json runs/bell/bell_a_prime_b_prime.output.json
PYTHONPATH=src python tools/run_inputs.py --out runs/ghz examples/events/ghz/ghz_x_y_y.json examples/events/ghz/ghz_y_x_y.json examples/events/ghz/ghz_y_y_x.json examples/events/ghz/ghz_x_x_x.json
PYTHONPATH=src python tools/bell_gate.py --expectation examples/events/ghz/expectation.json --outputs runs/ghz/ghz_x_y_y.output.json runs/ghz/ghz_y_x_y.output.json runs/ghz/ghz_y_y_x.output.json runs/ghz/ghz_x_x_x.output.json
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json
PYTHONPATH=src python tools/body_drift.py --expectation examples/events/like_or_unlike/expectation.json examples/events/like_or_unlike/like.json examples/events/like_or_unlike/unlike.json examples/events/like_or_unlike/uncharged_pair.json examples/events/like_or_unlike/alone_first.json examples/events/like_or_unlike/alone_second.json examples/events/like_or_unlike/uncharged_alone_first.json examples/events/like_or_unlike/uncharged_alone_second.json examples/events/like_or_unlike/like_plain.json examples/events/like_or_unlike/unlike_plain.json
for f in matter_alone matter_and_gravity matter_and_binding charge light_and_charge; do PYTHONPATH=src python examples/events/$f/build_world.py --modes; done
PYTHONPATH=src python tools/body_rest.py --expectation examples/events/matter_alone/expectation.json examples/events/matter_alone/pixel.json examples/events/matter_alone/cloud.json
PYTHONPATH=src python tools/body_rest.py --expectation examples/events/matter_and_gravity/expectation.json examples/events/matter_and_gravity/well.json
PYTHONPATH=src python tools/run_inputs.py --out runs/binding examples/events/matter_and_binding/pair.json && PYTHONPATH=src python tools/body_rest.py --expectation examples/events/matter_and_binding/expectation.json --output runs/binding/pair.output.json examples/events/matter_and_binding/pair.json
PYTHONPATH=src python tools/body_rest.py --expectation examples/events/charge/expectation.json examples/events/charge/charged_body.json examples/events/charge/like.json examples/events/charge/unlike.json
PYTHONPATH=src python tools/run_inputs.py --out runs/light examples/events/light_and_charge/free.json examples/events/light_and_charge/through_neutral.json examples/events/light_and_charge/through_charged.json && for w in free through_neutral through_charged; do PYTHONPATH=src python tools/click_counts.py --world examples/events/light_and_charge/$w.json --output runs/light/$w.output.json --expectation examples/events/light_and_charge/expectation.json; done
```

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and
archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746); cite it with
[CITATION.cff](CITATION.cff).
