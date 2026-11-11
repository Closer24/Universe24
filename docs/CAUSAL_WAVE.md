# Local wave, C2 memory and response

This optional model is based on main `ebe4b97e953845390a97ad284bfc0525ccc008d8`,
after the Einstein and owned-channel integration. Run:

```bash
python -m universe24 --L 3 --steps 1 --causal-wave --out runs/causal-wave --rewind
# Open runs/causal-wave/board.html; use the Local wave panel's microtick slider.
python -m unittest universe24.tests.test_causal_wave -v
```

The panel shows actual Engine snapshots and component audit clicks. Clicking a node
displays its retained memory triple, incoming packet lanes and response field.
At microtick zero there are initial conditions and no transition clicks.
The Einstein panel continues to show physical time and its own register
provenance. These two time coordinates are not identified.

## Fixed law

Nine gears are allocated to the `causal_wave` owner: six directed packet
lanes, one static detector marker, one memory and one response field. There are
26 additional monomials. The existing communication and optional transported
probe owners retain their channels and seeds. Input degree is at most two in the new block; the
composed ADM tensor retains its existing degree-three bound. All terms read
the complete old `b` snapshot on the target and at most one face neighbor.
No old-`a` dependency, runtime injection, gate callback, freeze mask, event
filter or global time input is added.

For each face direction `d`, the fixed inputs are:

```text
u_lane_d(x)   = 3 [b_lane_d(x-d) + b_lane_d(x+d)]
u_detector(x)= 6 b_detector(x)
u_memory(x)  = 2 b_detector(x) sum_d b_lane_d(x-d)
u_response(x)= 3 b_memory(x) + 3 sum_d b_response(x+d)
```

Every gear uses exactly `ell,r_next=divmod(2*u+r,6)`,
`a_next=b`, `b_next=ell-a`. The detector coupling and memory-to-response
coupling are designated one-way probe wiring, not a reciprocal force law.

`prepare_causal_wave` accepts signed integer packets and detector addresses,
constructs **both** previous and current packet snapshots, and preserves all
non-wave triples. It is initialization only. Packet preparation sets
`a_lane_d(x)=b_lane_d(x+d)`, so the recurrence implies exactly
`b_next_lane_d(x)=b_lane_d(x-d)`. All six directions, periodic boundaries and
signed big integers use the same law. This translation identity applies to
the prepared sector; arbitrary histories still evolve reversibly and are
never silently projected onto that sector.

The detector is prepared with `a=b=1` at selected addresses and `0` elsewhere.
Its law retains that spatial marker. Memory starts at `(a,b,r)=(0,0,2)`.
When the first unit packet reaches a marked receiver, `u=2`, hence
`ell=1`, `r_next=0`, and the memory becomes `(0,1,0)`. This is an actual
C2 transition: the triple changes, the quotient is nonzero, and the
residue difference is four modulo six. C2 means the existing arithmetic
class, not the third global update. At distance three it first occurs on
update three; the default side-three example first receives on update one.

After an isolated arrival, the memory's `(a,b)` follows
`(0,1),(1,0),(0,-1),(-1,0),(0,1)`. Information remains in the complete state.
The response field begins changing **one update after** the memory, because
it reads the old snapshot, and its effects then propagate through neighbor
reads. Removing only the memory-to-response term removes this response while
leaving the C2 and memory intact. No observer causes the response.

Later packet arrivals are processed by the same arithmetic. A quotient-zero
transition is not a changed-triple click, even if its residue changes. The panel
does not invent clicks to make every arrival a C2. The response field is an
integer wave prototype; boundedness or a positive conserved energy is not
claimed. Its possible magnitude growth is not evidence of growing complexity.
On later torus crossings, contributions can cancel the detector's local
`a,b` amplitudes. Information preservation is a property of the complete
reversible state, not a promise that one detector's amplitude stays nonzero.

## Causal bound and continuing activity

Inductively, a full-state perturbation can advance at most one face edge per
Engine update. The bound must start from **all** initially changed `a,b,r`
sites. For a prepared unit lane packet, the previous snapshot also occupies
the upstream site. The display uses that two-site support and periodic
Manhattan distance. This is a conservative computational cone, not an
Einstein metric-null cone or proof of Lorentz invariance.

Tests compare identical tensors with and without the packet, including
differences in complete states and full event records. Unrelated
background activity can click outside this packet's cone: it has its own
causal past. No node is frozen while waiting for the packet, and no unrelated
click is hidden. The marker merely specifies a local receiver in the seed.

## Information and integration

Exact inverse evolution covers **all** gears and remainders. The optional
model changes memory residues; main's full trace already supports them using
`Rule3-full-triples-delta-v2`: the initial complete seed, `a_next=b`, and sparse
changes to both `b` and `r`. This PR preserves that trace format and its existing
v1 compatibility. In the unified runtime, wave gears have audit labels and
their clicks are included in `component_events.jsonl.gz` and the wave frames;
`official_events.jsonl.gz` retains physical arithmetic events only. Standalone
wave tests use the same changed-triple predicate with official labels. Neither
label affects evolution. Frame values use hexadecimal
strings for unbounded integers.

The added block does not feed into ADM arithmetic. All Einstein registers,
fields, matter sources and constraints must remain exactly those of the
matched unmodified run; the runtime independently checks its complete
integer DAG and rewind. In particular, the Einstein compiler's finite-horizon
clock bank is **still present**. This PR does not replace those clocks with
distributed dependency scheduling. The new wave block itself has no clock
bank or copied age: its timing comes from packet arrival.

This is an executable implementation of delayed local C2 response and memory
on the integrated board. It is not quantum collapse, a Born/Bell derivation,
a complexity-maximizing selector, a metric-dependent physical light cone, or
recurrent cosmological bursts with cumulative complexity. None of these
unresolved goals is inferred from a C2 count, a repeated packet or large
integers.

Validation and current source hashes are recorded in
`docs/evidence/causal_wave.json`. Raw runs belong under `runs/`.
