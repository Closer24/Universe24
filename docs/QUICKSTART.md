# Quickstart and command reference

This tutorial uses **Python 3.11+**, the standard library, and the source tree as-is. Commands below run from the repository root.

## 1. Verify the installation

```bash
python --version
python -m unittest discover -s tests -v
```

An optional editable install is supported by `pyproject.toml`, but is **not required** for `python -m universe24`.

## 2. Run an impulse

```bash
python -m universe24 --config examples/impulse.json --audit
```

This starts from uniform `(0,0,2)` and sets channel 0 at the center to `(0,2,2)`. The engine evolves every channel for the number of reference steps specified in the JSON file. It prints a JSON summary.

`--audit` runs extra *read-only validation*: reverse one update, check local Rule3 identities, and check the global signed-account change identity. It does **not** change the forward trajectory.

## 3. Compare a signed coupling

```bash
python -m universe24 --config examples/signed_impulse.json --audit
```

The example differs by the **fixed pre-run** body signs `[1,-1,1]`. This changes the chosen structural model but never adapts couplings at runtime. The `[1,1,1]` reference remains available.

## 4. Write external observations and a checkpoint

```bash
python -m universe24 --config examples/signed_impulse.json --steps 8 --events run8.jsonl --output run8.json --audit
```

- `run8.jsonl` is a newline-delimited JSON stream of **passive arithmetic event observations**.
- `run8.json` is the complete sparse retained state, together with the cube side, fixed coupling signs, completed step count and a coupling fingerprint.
- The CLI refuses to overwrite either output and refuses to use the same path as its input.
- The printed `logged_arithmetic_events` field is **zero if no `--events` log was requested**, even if the trajectory contains events.

Each observation contains a step number, a four-part address `[x,y,z,channel]`, a `kind` (0, 1 or 2), the quotient, and the local states before/after. No observer sends instructions into the engine.

## 5. Resume the checkpoint

```bash
python -m universe24 --resume run8.json --steps 4 --audit --output run12.json
```

This advances the stored **full state** for four additional Rule3 reference steps. It does *not* reverse the physical trajectory. Do not resume an `events.jsonl` file; event logs are incomplete projections of the state.

## 6. Override only allowed inputs

```bash
python -m universe24 --config examples/clock.json --steps 30 --audit
```

`--steps` overrides the `steps` in the JSON for the current invocation. The run uses the same single-board core for clocks, waves, detector preparations, and every other seed.

## Complete CLI options

| Option | Meaning |
| --- | --- |
| `--config FILE` | Load a data-only initial experiment JSON |
| `--resume FILE` | Load a saved full-state checkpoint; mutually exclusive with `--config` |
| `--steps N` | Nonnegative forward steps; required with `--resume` |
| `--audit` | Check inverse and algebraic balance without changing the state |
| `--events FILE` | Create a **new** read-only arithmetic event log in JSONL |
| `--output FILE` | Create a **new** full-state checkpoint in JSON |
| `-h`, `--help` | Show built-in help |

## Troubleshooting

| Symptom | Explanation |
| --- | --- |
| `No module named universe24` | Run from the repository root, or install the package in your environment |
| `File exists` | Output paths use exclusive creation; choose a new name |
| `side must be an integer >=3` | The cube requires six distinct neighbor sites |
| Invalid coupling signs | Exactly three integers, each `+1` or `-1`, are required |
| `Unsupported keys` | JSON experiments are **data-only**, and unknown instructions are rejected |
| Large runtime or memory | A sparse state can grow through six-neighbor propagation; `L³ × 48` is the full state size |
| No event log despite changing states | Use `--events`; arithmetic events are filtered, and some changes affect only remainders |

See [Experiments](EXPERIMENTS.md), [Architecture](ARCHITECTURE.md), and [Research status](RESEARCH_STATUS.md).
