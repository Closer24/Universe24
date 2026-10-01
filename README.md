# Universe24

Universe24 is a three-dimensional event simulator, the implementation of Reality
Theory: a GameBoard of Nodes joined by Links, bounded integer arithmetic and one
local rule, Rule3. Every family of the universe file is a record stepped by Rule3
from its own levels and its six neighbours'; only a detector's click is a
measurement, and every other number a run writes is a GameBoard reading labelled so.

The repository holds the engine (`src/event_universe/`), the tools that lay, run,
gate and read a world (`tools/`), and the two worlds that gate the engine:

- the two slits, `examples/events/two_slits/two_slits.json`: a packet of light
  through a wall with two gaps onto a screen of twelve regions, its blind
  expectation `expectation.json` beside it, read by `tools/click_counts.py`;
- Bell, `examples/events/bell/bell_a_b.json` and its three sisters: the pair
  family, two real lines of light laid as one event on a chain, one beam to each
  side's region with its setting as its `basis`, the blind `expectation.json`
  beside them (S = 478 / 169 exactly), read by `tools/bell_gate.py`; the
  back-in-time gate, `tools/back_in_time.py`, says MATCH on every world.

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
PYTHONPATH=src python tools/back_in_time.py --intervals 40 examples/events/two_slits/two_slits.json
```

Universe24 is released under the [MIT License](LICENSE), copyright Alon Gonen, and
archived on Zenodo under the concept DOI
[10.5281/zenodo.22738746](https://doi.org/10.5281/zenodo.22738746); cite it with
[CITATION.cff](CITATION.cff).
