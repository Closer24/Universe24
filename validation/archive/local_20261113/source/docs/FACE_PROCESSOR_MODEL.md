# Coupled face processor: fixed wiring, changing passage

One source-only candidate now combines shared face state, bidirectional
traffic feedback, actual one/two-update passage and a retained tick counter
in **one fixed tensor**, through the ordinary Engine and bundle runtime.
It does not establish Einstein gravity, a material proper clock, a restoring
spring or cosmological bangs.

## Generic architecture

A node has six `FacePort` views, one per physical neighbor. A port is an
oriented interface, not another topology node or an independently running
agent. Opposite ports reference the same independent `Link` state. The graph
still has L^3 nodes and 3L^3 undirected interfaces.

| Retained state | Channels per array cell |
| --- | ---: |
| Two internal signal modes for each of six node ports | 12 |
| Node tick counter | 1 |
| Two directional phase fields per independent interface | 6 |
| One transit stage per direction and interface | 6 |
| Total | 25 channels, 75 integers including histories and carries |

The two phases are components of one shared interface, not duplicate links.
Each endpoint's traffic updates a phase, and the two phases exchange, so
traffic can affect the other endpoint's subsequent processing. `FacePort`
adds no registers. The stage is counted memory; naming it a mechanism does
not remove that memory cost. There is no external queue, timer, reset,
runtime tensor change or separately advanced node.

## Local rule and fixed streaming

For outgoing Boolean values x,y and phase q, the local gate is:

```text
q=1: (x_out,y_out)=(x,y)
q=0: (x_out,y_out)=(y,x)
q_out=q XOR x XOR y
```

The inverse exchanges x,y when the current q is1, then applies the same
XOR. If x=y, exchange is immaterial; otherwise q flips and the inverse
recovers the forward exchange. This is a bijection on all eight inputs.

Fixed streaming delivers x_out to the neighbor's first mode in that update
and puts y_out into the retained transit stage. The *old* stage goes to the
neighbor's second mode, regardless of the phase. Updated phases exchange
within the interface. These operations define a reversible map F.

This is a construction-time description. Every real Engine output reads
the same old snapshot. F and F^-1 have degree at most three and strict
single-edge physical support. Their composition is compiled into the one
tensor; no intermediate callback or extra bank is executed.

## Exact natural domain and clock

Every Boolean value is stored as 1+bit. Prepare a=F^-1(b), with positive
remainders in {1,2,3,4,5}. On Boolean channels the compiler uses

```text
u=6+3*(F_bits(b-1)+F_bits^-1(b-1)).
```

Unchanged Rule3 produces the shifted F exactly and retains every carry.
The entire prepared Boolean board is invariant, including dense occupancy
and simultaneous opposite traffic. This is not a single-particle-only proof.
The independent counter uses u=6b and initial (a,b)=(1,2), hence
a_n=1+n and b_n=2+n. It is counted state in the same tensor. It measures
updates; its interpretation as material proper time remains unproved.

Coefficients are signed integers. Arbitrary positive histories outside the
prepared domain are not promised positive. Signed and arbitrary-size
integer states still retain the generic exact inverse.

## What the gear analogy means

Before-to-after always has the same Rule3 semantics. An additional "tooth"
means an additional processing stage before delivery, not a changed divisor,
a skipped update, slower computation or a demonstrated change of proper time.

| Phase | Input in first mode | Input in second mode |
| --- | ---: | ---: |
| q=1 | 1 update | 2 updates |
| q=0 | 2 updates | 1 update |

For the canonical first-mode probe, N=2-q. Changing q from1 to0 adds one
tick; changing it back removes that tick for subsequent admission. Quiet
q=1 interfaces provide N=1 for this reference probe.

**A single scalar N is not a universal interface metric for both modes.**
The generic object is a state-dependent local passage operator. A physical
model must explain or eliminate this mode dependence.

After admission into the transit stage, the value exits on the next update
under every phase and occupancy. A changing phase affects later admission,
not the stored value. Separate output modes preserve information when direct
and delayed signals arrive together. This is admission-selected passage,
not an arbitrarily stretchable in-flight trajectory. Delays above two updates
and restoring motion toward N=1 are not implemented.

## Primary literature and physical limits

The relevant generic architecture is local processing/scattering plus fixed
streaming and retained internal modes. Related quantum-walk constructions
recover curved-spacetime Dirac transport through selected local operators
and continuum-limit proofs. They use quantum amplitudes/unitaries; our
Boolean permutation is a separate classical construction.

* [Arrighi, Facchini and Forets](https://arxiv.org/abs/1505.07023): a test
  particle on a fixed lattice, using encoding/grouping, reproduces massive
  Dirac transport in 1+1 curved spacetime in the declared limit.
* [Arrighi and Facchini](https://arxiv.org/abs/1609.00305): extends the
  transport construction to 3+1 dimensions, representing metric information
  through local unitaries.
* [Arrighi, Di Molfetta and Facchini](https://quantum-journal.org/papers/q-2018-08-22-84/):
  finite choices of local coin operators control effective transport speed
  in a restricted massless limit.

These papers support a research route, not Einstein gravity for arbitrary
couplings or this tensor. Here passage is mode-dependent, rays stay on their
prepared axes, and no shared Lorentzian metric/source, stress tensor,
curvature evolution, material clock or convergence study is supplied.
Existing six-length/shear and clock counterexamples remain applicable to
their stated interpretations. No bounce or cosmological bang is established.

## Reproduction

```bash
python -m validation.face_transport --out runs/new-face-transport
python -m unittest universe24.tests.test_face_transport -v
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-face-smoke
python -m universe24 verify --run runs/new-face-smoke/run
```

The completed native panel contains 29 runs and 1,056 updates: quiet reference,
24 phase/direction/input-mode combinations, three dense cases and a 64-node,
256-update case. One tensor is used throughout. Every state matches an
independent circuit; every step matches an independent scalar Rule3 oracle
and rewinds. Tests enforce carries, positive values, payload count, counters
and unconditional release of every old transit stage. Upward and downward
canonical delay changes are measured, not assumed.

Evidence: `runs/face-transport-20261113/`; full regression and central
acceptance: `runs/face-transport-review-20261113/` and
`runs/face-transport-central-20261113/`. Mechanical successes do not promote
the general physical acceptance gate.

The final full suite passed **541 tests in 193.745 seconds**. Generic smoke
and supported replay passed. Fresh central acceptance reported software
execution passed and general physical acceptance blocked. Across the 29 face
runs, canonical passage costs increased 33,065 times and decreased 33,059
times; 64,942 occupied-stage releases were checked. Peak retained size was
9 bits, driven by the increasing counter, not unbounded payload growth.
