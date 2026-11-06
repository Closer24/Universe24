# Universe24

An exact, generic Python reference engine for a **single-board reversible Rule3** cellular automaton. This is a mathematical research model, **not a validated theory of physics**.

## Model
- Spatial geometry: periodic cube of side `L >= 3`; coordinates modulo `L`.
- One 48-channel node per site. Channels are the elements of the binary octahedral group `2O`.
- Every channel stores two arbitrary-precision integers `(a,b)` and one remainder `r in 0..5`.
- Exactly six spatial neighbor inputs per channel, one from each direction `+x,-x,+y,-y,+z,-z`. **No on-site mixing or second board.**
- The fixed 2O coupling is represented by three signed 48x48 matrices and their transposes. Body signs are chosen only **before** the run, from `{-1,+1}^3`. Matrix entries are `-1,0,+1`.
- Sole update: `ell,r_next = divmod(2*sum_six_signed_inputs + r,6); (a_next,b_next)=(b,ell-a)`.
- All channels update from the same old snapshot.
- No per-node execution clock; the integer update index is a simulation reference, not operational physical time.
- Click classes are **external arithmetic readouts**. They do not alter, select, or veto anything in the simulation.

## Run
Python 3.11+; standard library only.

```bash
python -m unittest discover -s tests -v
python -m universe24 --config examples/impulse.json --audit
python -m universe24 --config examples/signed_impulse.json --audit --events events.jsonl --output final.json
python -m universe24 --resume final.json --steps 10 --audit
```

A JSON experiment specifies only `side`, `coupling_signs`, a stationary `background` (default `[0,0,2]`), sparse `seed_changes`, and `steps`.

## Structure
- `universe24/core/`: group 2O, signed six-neighbor tensor, immutable cube/state, Rule3 and explicit inverse, generic executor.
- `universe24/experiments/`: data-only initialization and full-state checkpoints.
- `universe24/observation/`: passive click classes and balance audits.
- `examples/`: prepared impulse and clock seeds.
- `tests/`: mathematical, execution, and separation tests.

## Limits
Exact inversion, finite group covariance and arithmetic identities do not establish energy, angular momentum, quantum probabilities, click selection, photons, matter or gravity. A measured click is not a runtime instruction. The optional signed tensor may not conserve the same signed total Q as the all-positive case.

See `AGENTS.md` for strict rules preventing experiment logic from altering the node dynamics.
