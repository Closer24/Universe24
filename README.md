# Universe24

One local integer engine, one built-in signal/clock coupling, and a passive
click observer. Each node has six face ports over 48 retained channels. There
is no separately owned link memory: both endpoints refer to the same adjacency
and read their own internal directional state.

The implemented coupling lets a signal change a local clock phase, and that
phase changes subsequent signal transmission. The complete state rewinds
exactly. **This is a discrete transmission model, not yet an Einstein universe.**
A common metric, moving massive bodies, dark matter, gravitational waves and
Big-Bang dynamics have not been established under this one law.

## Run the single model

```bash
python -m pip install .
python -m universe24 prepare-model --size 7 --out runs/input
python -m universe24 run --bundle runs/input --steps 12 --out runs/output
python -m universe24 verify --run runs/output
python -m universe24 observe-clicks --clicks runs/output/clicks.jsonl.gz
```

Use new output paths. The default preparation has a signal plane at x=0, a
clock plane at x=2, and a retained coordinate counter. `--root 0..47` changes
the orientation. `--signal-sites`, `--memory-sites` and `--clock-sites` change
initial planes under the **same tensor**, not the update rule. The Python
`prepare_fields` API accepts complete spatial Boolean profiles.

The verified positive domain selects one orientation at a time. Every cube
orientation is supported separately; arbitrary simultaneous independent
six-direction populations are not proved. The six face groups are views of
the complete state, not six independently certified circuits.

## The gears and the clock

Each channel retains `(a,b,r)`: previous gear value, current gear value and
arithmetic remainder. The same update applies everywhere:

```python
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

`u` is a fixed integer polynomial of degree at most three. All outputs read the
same old snapshot; each monomial touches the target and at most one face edge.
There is no runtime solver, queue, reset, clipping, injection or discarded
history. Exactly 48 channels means 144 retained integers per node, including
the local coordinate counter. Integers can grow without a fixed bit limit.

The built-in tensor has 1,968 monomials and exact joint binary-octahedral
channel/cube covariance. Its prepared signal and clock values are encoded as
`b=1+bit`; the complete future histories and carries remain natural numbers.
The three Boolean roles are an incoming signal, memory and clock phase. Their
reversible collision conserves both clock-site occupation and free-plus-stored
signal. The clock-site locations themselves do not move or cluster. In the same
initial clock phase, bursts of 1, 2 and 3 occupied input updates retain stored
occupancy for 1, 2 and 3 updates. Further incoming ones pass during storage;
this is not a FIFO queue or proof of geometric link stretching.

A fixed polynomial gives a fixed arithmetic operation schedule per node. It
does **not** guarantee fixed CPU time: integer arithmetic cost depends on bit
length. A counter increasing by one is a prepared coordinate clock, not a
material proper clock and not proof of growing structural complexity.

See [the model equations](docs/MODEL.md), [node and click interfaces](docs/OBSERVATION.md),
[the execution contract](docs/ONE_SYSTEM.md) and [the physical acceptance criteria](docs/PHYSICS.md).

## Observe only clicks

The observer reads the standalone click file, without opening a bundle or
hidden state trace. Given explicit public initial channel histories, it can
reconstruct that channel. For the default root=0 counter (channel 4):

```bash
python -m universe24 observe-clicks --clicks runs/output/clicks.jsonl.gz \
  --channel 4 --nodes 343 --steps 12 --initial-a 1 --initial-b 2 \
  --out runs/counter-observation.json
```

These are arithmetic records, not calibrated photon counts. Stream completeness
is checked by separate full-state replay. The selected law has constant
remainders and emits only C0; C2 is an arithmetic class, not a third handshake
or an established quantum mechanism.

## Verification and scope

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m universe24.system.checks --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
python -m universe24 status
```

The suite checks the independent scalar oracle, exact inverse, arbitrary large
integers, all 48 symmetry actions, the Boolean collision/streaming domain,
positive histories, reciprocal phase feedback, conserved logical accounts,
bundle integrity and calibrated click-only reconstruction. The generic smoke
is an engine/I/O test, not a second physical model.

`verify --require-physics` deliberately fails while the physical criteria are
unresolved. A green software suite does not grant physical acceptance.

There is one installed CLI and one built-in model, in `universe24/model.py`.
Generic `prepare` still seals explicitly supplied complete tensors/seeds for
engine validation; it cannot grant a physics claim. `core/` contains the sole
Engine, `system/` the immutable bundle/run/replay path, `node.py` the passive
face interface and `observer.py` click-only inference.

Historical experiments, alternate model modules, tracked run outputs and the
experiment menu were removed from the current tree. Their original versions
remain in [Git history at 2d0ca44](https://github.com/Closer24/Universe24/tree/2d0ca44f9dbda7da2e97da439c9a11a92134fa14).
They are not combined as evidence for this law.
