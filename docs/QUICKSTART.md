# Quickstart and command reference

The engine examples use **Python 3.11+** and the standard library. Commands run
from the repository root. Full research validation has additional setup below.

## 1. Verify the installation

```bash
python --version
python -m universe24 --help
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
mkdir -p runs
python -m universe24 --config examples/signed_impulse.json --steps 8 --events runs/run8.jsonl --output runs/run8.json --audit
```

- `runs/run8.jsonl` is a newline-delimited JSON stream of **passive arithmetic event observations**.
- `runs/run8.json` is the complete sparse retained state, together with the cube side, fixed coupling signs, completed step count and a coupling fingerprint.
- `runs/` is ignored by Git, so these outputs never appear as untracked files.
- The CLI refuses to overwrite either output and refuses to use the same path as its input.
- The printed `logged_arithmetic_events` field is **zero if no `--events` log was requested**, even if the trajectory contains events.

Each observation contains a step number, a four-part address `[x,y,z,channel]`, a `kind` (0, 1 or 2), the quotient, and the local states before/after. No observer sends instructions into the engine.

## 5. Resume the checkpoint

```bash
python -m universe24 --resume runs/run8.json --steps 4 --audit --output runs/run12.json
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

## Full research validation

Use a Git checkout (a shallow clone, `git clone --depth 1`, is enough): some tests
record the checkout's commit and status with `git`.
The engine has no third-party runtime dependencies, but research tests need the
pinned arithmetic and solver packages. Run this setup before the full suite:

```sh
python -m pip install -r research/clock_selection/requirements.txt -r research/clock_selection/requirements-solver.txt
python -m research.experiments.materialize_evidence
python -m research.clock_selection.archive materialize
python -m research.invariant_families_v1.verify_evidence
python -m unittest discover -s tests -v
python -m universe24 --config examples/impulse.json --audit
python -m universe24 --config examples/signed_impulse.json --audit
```

Restoration grows a fresh checkout from about 0.9 GB to about 3.0 GB, and the decoder's
set-A rerun below writes about 0.35 GB of logs under the ignored `runs/`, so allow about
3.5 GB of free disk. A virtual environment (`python -m venv .venv`, already ignored by
Git; activate it before `pip install`) keeps the pinned packages out of the system
interpreter. Node.js is optional: two presenter tests use it and are skipped without it.

The curated matter/light packages have their own verifiers (about 15 minutes together):
`python -m research.matter_light_experiments_v1.verify` (every experiment),
`python -m research.matter_light_blocks_v1.verify --quick` (all 346 blocks without
`--quick`), and the decoder's set-A rerun in
[its README](../research/click_decoder_v1/README.md#validation-one-score-table-v10-against-v11).
The first two print their usage with `--help`.

The materializers restore only declared, checksum-locked research evidence.
They do not overwrite live code or differing existing files. Restoration uses
local archive parts and requires disk space for complete recordings. The
[invariant-family evidence](../research/invariant_families_v1/README.md) is
already tracked directly. The [reliability bundle](RELIABILITY.md) describes
versioned test artifacts and independent reruns; its historical acceptance
counts describe those earlier runs, not the current suite size.

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
