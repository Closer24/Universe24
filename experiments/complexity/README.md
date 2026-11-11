# Local complexity mechanisms

These are optional research tensors and passive auditors. They do not change
production evolution. Read [PROTOCOL.md](PROTOCOL.md) before interpreting a
passing subgoal, and [the synthesis](../../docs/COMPLEXITY_MECHANISMS.md) for
the results and failures. The original recurrent-burst acceptance gates remain
unchanged.

Under [issue #40](https://github.com/Closer24/Universe24/issues/40), these
research candidates are not additional supported runtimes. The total accepted
system budget includes every apparatus channel; adding the 31-channel toy to
the 44-channel geometry proposal would exceed the 48-channel cap. This branch
uses the pinned baseline source layout. The separate integration migration to
`validation/` must explicitly update these harness imports and CI commands.

From the repository root, reproduce the declared grids:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python -m experiments.complexity.local_stagnation --out runs/complexity-research/01-stagnation
python -m experiments.complexity.structural_memory --out runs/complexity-research/02-memory
python -m experiments.complexity.reassembly_feedback --out runs/complexity-research/03-reassembly/verified
python -m experiments.complexity.cycle_organization --out runs/complexity-research/04-organization
python -m experiments.complexity.complexity_born --out runs/complexity-research/05-born
python -m experiments.complexity.sensor_rotor --out runs/complexity-research/07-sensor-rotor
```

Then independently replay the saved evidence and recompute the gates:

```sh
python -m experiments.complexity.acceptance_audit --out runs/complexity-research/06-acceptance
python -m experiments.complexity.acceptance_audit --stagnation runs/complexity-research/01-stagnation --out runs/complexity-research/06-acceptance/stagnation-independent
python -m experiments.complexity.acceptance_audit --born runs/complexity-research/05-born/report.json --out runs/complexity-research/06-acceptance/born-independent
python -m experiments.complexity.acceptance_audit --peer-root runs/complexity-research --out runs/complexity-research/06-acceptance/peers-independent
python -m experiments.complexity.acceptance_audit --sensor-rotor runs/complexity-research/07-sensor-rotor --out runs/complexity-research/06-acceptance/joint-independent
python -m experiments.complexity.summarize --out runs/complexity-research/summary.json
```

The last command checks source provenance and collects a compact evidence
index. It does not execute dynamics or independently validate report claims;
the preceding replay commands do that. Complete tensors, seeds, finals and
available traces are saved under `runs/`, including failed controls and
resource stops. The CI artifact retains those files. The committed evidence
index records the source hashes and report hashes from the documented local
run; gzip timestamps can change archive hashes when reproducing equivalent
states.

The joint experiment is an explicitly declared follow-up to the separate
sensor/rotor runs. Alarm disconnection keeps the rotor's earlier memory
routing active. A retained density equal to message occupancy is not the
independent reference board required by the original cosmology protocol.
