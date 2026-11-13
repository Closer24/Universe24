# Universe24

One reversible integer engine, one finite-capacity coupling, and a passive
click-replay board. Each node has six face ports and 48 counted channels,
eight per face. The directional state lives inside the nodes; adjacent nodes
share an edge identity without a separate link memory or controller.

The current law makes transfer depend on occupation at both ends of an edge,
then turns channels toward other faces. It conserves total occupation and
rewinds exactly. **This implements local capacity feedback, not an established
Einstein universe or a universal load-balancing algorithm.** Some tested
preparations disperse better than free transport; others disperse worse.
Matter, dark matter, a shared spacetime metric and gravitational waves have
not been identified under this law.

The local [event-space energy and momentum audit](docs/ENERGY_MOMENTUM_CANDIDATE.md)
records a conservative candidate, its transport calibration, and its failed
overall load-distribution criterion. It has not replaced the installed law.

## What we are trying to build

The research goal is one local integer coupling in which finite node capacity
changes transport through six internal face gears. Events and causal transfers
define the candidate spacetime; an observer sees calibrated clicks. Host CPU
time and the saved update index are not assumed to be physical proper time.

We are testing whether the same rule can both distribute occupied capacity
and support conserved energy and momentum, operational clocks and a common
geometry reconstructed from propagation. Light, matter and dark matter would
have to emerge as distinguishable persistent dynamics under that rule, rather
than as branches selected by labels. Recovering Einstein geometry is a target
requiring causal, metric and field-equation tests, not an assumption of the
implementation.

| Status | Result or next criterion |
| --- | --- |
| Installed and tested | Positive integer preparation, exact reversal, six-face capacity feedback, scalar continuity and calibrated click replay |
| Local phase-routing candidate | Better average spreading in independent finite cohorts; the natural additive momentum account fails |
| Local momentum candidate | Conserved occupation and vector momentum linked to event transport in a restricted 24-independent-bit sector; spreading improvement is inconsistent |
| Next acceptance gate | One rule must satisfy conservation, causal transport and reliable spreading on declared independent controls |
| Still open | A shared evolving metric, material proper clocks, Lorentz behavior, Einstein equations and identified particle species |

The candidates are separate research results; their successes cannot be added
together as if one tensor achieved them all. Their reports are committed below;
prototype scripts and generated run outputs remain local in ignored `runs/`.
The installed model is the reproducible code shipped by this repository.

## Run from a concentrated preparation

```bash
python -m pip install .
python -m universe24 prepare-model --size 7 --radius 1 --out runs/input
python -m universe24 run --bundle runs/input --steps 24 --out runs/output
python -m universe24 verify --run runs/output
python -m universe24 board --run runs/output --out runs/board.html
```

Open `runs/board.html`. Use new output paths. The self-contained board shows
recorded node occupation, blocked capacity, all six faces, concentration,
integer magnitude bits and the fixed arithmetic work count. Its playback
controls select recorded frames; they do not run another physics engine.

`--pattern burst` is the default. The radius-1 seed fills all 48 slots at seven
central nodes and declares an asymmetric 30-slot boundary halo: total
occupation 366. The halo activates the capacity gate. It is prepared initial
data, not an emergent species. The default radius 0 has total occupation 54.
`--center x y z` translates the preparation; `--root 0..47` selects its frame.
`--pattern pulse` prepares one occupied slot; `--pattern vacuum` prepares none.
The Python `prepare_occupation` API accepts complete arbitrary Boolean fields
for all 48 channels. Every preparation uses the same tensor.

A necessary control is the symmetric burst:

```bash
python -m universe24 prepare-model --size 7 --radius 1 --no-halo --out runs/control-input
python -m universe24 run --bundle runs/control-input --steps 24 --out runs/control-output
python -m universe24 board --run runs/control-output --out runs/control-board.html
```

This central-pair-symmetric preparation never activates the three-slot gate;
its outward motion is exactly free transport. A spreading picture alone is
therefore insufficient evidence of adaptive distribution. Neither preparation
is a demonstrated cosmological Big Bang.

## Gears, capacity and exact conservation

Every channel retains `(a,b,r)` and follows the same update:

```python
ell, r_next = divmod(2*u + r, 6)
a_next = b
b_next = ell - a
```

The fixed integer polynomial `u` has degree at most three. All outputs read
one old snapshot, and each monomial touches the target and at most one face
edge. Exactly 48 channels means 144 retained integers per node. There is no
runtime queue, injection, clipping, discarded history or extra clock bank.

In the proved sector, `b=1+occupation`, with Boolean occupation. Four slots
form an edge quartet: two inside each endpoint. If three are occupied, the
edge stage holds them; otherwise it cyclically exchanges values across the
edge. A fixed onsite permutation then turns the channels. The gate is a
reversible conservative permutation, expanded into one **672-monomial tensor**
with exact joint binary-octahedral channel/cube covariance. All future and
past prepared values remain positive: `a,b` in `{1,2}`, carries in `1..5`.

The conserved account is

\[
Q(x)=\sum_{g=0}^{47}(b_g(x)-1),\qquad 0\leq Q(x)\leq48.
\]

Each node's change in Q equals its signed edge currents. Both neighbors
influence those currents. A four-run causal control confirms that downstream
occupation changes aggregate transported load, beyond unconditional turning.
There are no light/matter/dark-matter branches in the update rule.

The fixed work schedule is 672 monomial evaluations, 1,440 factor reads and
multiplications, and 48 Rule3 divmods per node per update. This sector does not
make integers grow with traffic. Occupied transport capacity, integer bit
length and CPU cost are different quantities; Q is not yet physical energy.
The finite reversible sector recurs, so concentration and structural complexity
cannot be strictly monotonic forever.

## What the runs establish

A 24-update, size-7 radius-1 run conserves all 366 occupied slots. At updates
0, 5 and 12, occupied-node support is 25, 137 and 32 respectively; concentration
falls and then rises. This is redistribution with reconcentration.

Two prescribed comparisons against unconditional edge flow with the same
onsite turning expose the limits:

| Preparation and window | Lower concentration | Higher concentration |
| --- | --- | --- |
| 16 sparse side-3 cubes, size 7, update 8 | 13 | 3 |
| 16 denser side-2 cubes, size 5, integrated updates 1..30 | 5 | 11 |

The detailed domains and equations are in [MODEL.md](docs/MODEL.md).
[LOAD_DISTRIBUTION.md](docs/LOAD_DISTRIBUTION.md) compares the construction with
backpressure, conservative computation, Regge calculus and Jacobson's work.
Those papers do not identify computational congestion with Einstein gravity.
Scalar Q conservation does not establish momentum or stress-energy
conservation; a natural free-carrier momentum proxy fails at a blocked
collision. An isolated carrier takes one edge per update but follows a
three-axis microscopic turning path. It is not yet a Maxwell photon.

## The observer sees clicks

```bash
python -m universe24 observe-clicks --clicks runs/output/clicks.jsonl.gz
```

The standalone observer inspects only canonical arithmetic records. With
explicit initial `a,b` calibration it can reconstruct a channel. The board
uses all 48 calibrated channels from the sealed initial bundle plus the saved
clicks and validation provenance; it never reads `full_trace` or advances an
Engine. Public initial calibration is disclosed, not inferred from silence. The board
checks the exact tensor and the initial forward-sector relation before
reconstructing the recorded history.

The update index orders saved events; it is not a measured proper clock.
The current tensor emits only C0. C2 is an arithmetic class, not a third
handshake or a quantum mechanism. These clicks are not calibrated photon
counts. See [OBSERVATION.md](docs/OBSERVATION.md).

## Verification and repository scope

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m universe24.system.checks --out runs/system-smoke
python -m universe24 verify --run runs/system-smoke/run
python -m universe24 status
```

Tests cover the independent scalar Engine oracle, inverse, arbitrary large
integers, all 48 symmetries, all 16 edge words, positive prepared histories,
node continuity, causal feedback, symmetric null control, immutable bundles,
and calibrated click-only board reconstruction. The generic smoke is an
Engine/I/O check, not a second physical model.

`verify --require-physics` deliberately fails while the criteria in
[PHYSICS.md](docs/PHYSICS.md) remain unresolved. Green software checks do not
change that result. The [execution contract](docs/ONE_SYSTEM.md) describes the
shared state budget and immutable replay.

There is one installed CLI, one Engine in `core/`, and one built-in model in
`model.py`. Generic `prepare` seals complete explicit tensors/seeds for Engine
validation; it does not grant physical acceptance. Generated runs remain
ignored. Historical experiments and tracked outputs were removed from the
current tree; their sources remain in [Git history at
2d0ca44](https://github.com/Closer24/Universe24/tree/2d0ca44f9dbda7da2e97da439c9a11a92134fa14).
The previous independent-face clock law remains in [revision
2659ad8](https://github.com/Closer24/Universe24/tree/2659ad887f874eb67e15c57e5ebf8dead8c12f95).
Its E/B and residence-time results do not transfer to this replacement law.

A later [local-rule audit](docs/LOCAL_RULE_AUDIT.md) exhaustively checks the
existing edge-gate class and records why greedy equalization is not an
automatic reversible or Einstein-compatible extension.

A subsequent [phase-routing candidate](docs/PHASE_ROUTING_CANDIDATE.md)
passes independent finite load-distribution comparisons in the same Engine;
it is documented separately from the installed law and its diagnostics.
