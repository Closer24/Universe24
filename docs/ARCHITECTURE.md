# Architecture and strict execution boundary

## One universal node, not different node classes

The same source code and state type represent every node in the periodic cube. A node holds 48 `(a,b,r)` triples. Different initial conditions may produce sources, oscillators, interfering signals, prepared devices, and apparent detectors. These are **patterns**, never new runtime update types.

The user-facing command line is a generic executor and data-loader. It must not accept "run detector rule", "force click", "reset competitor", or "send cancellation" commands.

## Modules and their responsibilities

| Code | Role | May change automaton during a running experiment? |
| --- | --- | --- |
| `core/group_2o.py` | Construct exact 48-element group and spatial rotations | No, construction only |
| `core/coupling.py` | Derive constant signed neighbor tensor, check reciprocity | No, fixed before run |
| `core/state.py` | Validate and hold immutable complete channel state | No hidden mutation |
| `core/rule3.py` | The **sole** scalar forward state transition | **Yes, only here** |
| `core/engine.py` | Apply Rule3 to each channel from one old snapshot | Only by calling Rule3 |
| `experiments/config.py` | Read seed JSON; serialize full-state checkpoints | Not during evolution |
| `observation/clicks.py` | Report arithmetic event classes | **Never** |
| `observation/diagnostics.py` | Verify inverse and exact algebraic balance | **Never** |
| `__main__.py` | CLI: load, evolve, optionally observe and save | Only via engine |

## State flow

```text
JSON config (L, fixed signs, seed, steps)
  |
  v
Validated immutable initial State -- group(2O) --> fixed Coupling
  |                                              |
  +------------------- Engine.advance -----------+
                         |
             six signed spatial inputs
                         |
                     Rule3.forward
                         |
                   next full State
                         |
                +--------+----------+
                |                   |
                v                   v
          passive observer     inverse/balance audit
                |                   |
          JSONL output        diagnostics only
```

`Engine.advance` computes inputs from the complete old snapshot and returns a **new** `State`; all per-channel arithmetic takes place in `rule3.forward`. `Engine.rewind` uses the mathematical inverse for research and checkpoints, **not** as a second forward physical process.

## Sparse storage and complete state

The background `(0,0,2)` is a fixed point of Rule3 when all spatial inputs vanish; other stationary backgrounds with `a=b=0` and allowed `r` may be declared. States matching the background can be omitted in storage without erasing information: the same triple is defined for all omitted addresses.

The cube still contains `L³` nodes and `48 L³` channels, whether or not all of them are explicitly stored. The sparse representation is an implementation optimization, **not** physical disconnection or a deletion operation.

## Spatial neighbors and tensor indexing

The direction order is `(+x,-x,+y,-y,+z,-z)`. For every receiver channel and direction there is one nonzero signed tensor entry selecting a sender channel at the *adjacent spatial site*. `0` in a particular tensor element means "not that sender channel", **never "that direction is absent"**.

The six directional signed matrices are derived from three body-axis signs and the fixed group actions. They are reciprocal; negative spatial directions correspond to matrix transposes. All spatial positions wrap modulo `L`.

The group-theoretic 48 channels are internal labels, **not** 48 separate spatial neighbors.

## Reference execution vs physical time

The current software advances all channels synchronously for reproducibility. The global step index is a numerical reference and is **not** assumed to be a physical universal clock. Oscillatory states are possible *results* of Rule3. Independent physical event scheduling would require additional derivation and tests, not a per-node timer inserted into the code.

## Invariants to protect

See [AGENTS.md](../AGENTS.md). Every proposed change needs tests for exact six-port geometry, fixed coupling, full-state reversibility, read-only observations, and integer-only state. New physical interpretations belong in the research documentation, not in `core/rule3.py`.

## Interface example

```python
from universe24 import Channel, Coupling, Cube, Engine, State

cube = Cube(5)
engine = Engine(Coupling((1, -1, 1)))
initial = State(cube, cells={(2, 2, 2, 0): Channel(0, 2, 2)})
after_one_step = engine.advance(initial)
assert engine.rewind(after_one_step) == initial
```

The assertion is a mathematical invertibility test, not a detector observation.
