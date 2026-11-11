# Local messages instead of a carried cosmic clock

The explicit `reference_system(communication=True)` control communicates through six directed message
lanes. The Universe24 default includes this control alongside Einstein under separate channel ownership (see [UNIFIED_SYSTEM.md](UNIFIED_SYSTEM.md)). Its initial pulse is one declared preparation of outgoing messages at
one origin. Nodes respond to messages arriving across face edges. No node
stores a cosmic age, shared phase, master oscillator or copy of a Big Bang
clock. With no messages and the reference vacuum, this communication component is fixed; the Einstein component can still evolve.

This replaces the role proposed for a cosmic timing source. The retired
variable-divisor cosmic builders stay retired; they are not reactivated.
The optional reciprocal oscillator experiments in `clock_network.py` are
separate constructions and are not part of this communication model.

## Exact transport inside Rule3

For each direction `d` in `(+x,-x,+y,-y,+z,-z)`, a lane stores the ordinary
integer triple `(a_d,b_d,r_d)`. It is a message buffer with its retained
previous snapshot, not a clock. Choose the fixed linear input

    u_d(x) = 3 b_d(x-d) + 3 b_d(x+d).

Each term reads just one face neighbor. The scalar update remains exactly

    ell, r_next = divmod(2*u+r, 6)
    a_next = b
    b_next = ell-a.

Prepare the complete previous snapshot as `a_d(x)=b_d(x+d)`, with arbitrary
integer payloads in `b_d` and legal remainders. Since `2*u` is a multiple of
six, the quotient is `b_d(x-d)+b_d(x+d)` and `r_next=r`. Therefore

    b_next_d(x) = b_d(x-d),
    a_next_d(x) = b_d(x) = b_next_d(x+d).

The preparation relation is preserved in both directions. Messages translate
one face edge per update with no runtime injection, scheduling branch,
floating arithmetic or overwritten state. All signed integer payloads are
allowed, including overlapping messages that add within one lane. Separate
opposite lanes keep opposite traffic distinct. On a finite periodic lattice,
the prepared message sector returns after `L` updates; this recurrence is a
message returning around a loop, not an autonomous node oscillator. The
reference response need not have this period or remain bounded.

The prepared `a` snapshot for a localized outgoing packet occupies its previous
neighbor. This is explicit initial history, not instantaneous propagation from
an otherwise empty complete state. Arbitrary independent `a,b` values need not
translate one way; the ordinary reversible wave recurrence still runs, with
no projection back onto the prepared sector.

## Reception changes the local dynamics

The reference receiver `ref.R00` gets the six additional terms

    u_receiver(x) += 3 sum_d b_d(x-d).

This is an old-snapshot neighbor read inside the fixed tensor. A packet at
`x-d` changes the receiver at `x` in the same update that it arrives there.
The receiver then communicates through the original reference couplings.
A distant receiver cannot consult the origin, total network state or update
index. Removing these six terms is an explicit disconnected control: messages
still travel, but a reference vacuum no longer responds.

The choice of `R00` as a receiver is explicit wiring, not a symmetry or
physical-particle derivation. Reception is one-way: the reference does not
modify the lanes. The six terms carry nonreciprocity designations. This does
not claim conserved physical energy, acknowledgements, adaptive routing or
a reciprocal matter/geometry interaction. The six outgoing packets are
specified once in the seed; the runtime does not copy or broadcast them to
the entire board. Straight lanes cover their axis routes, not every lattice
site; reference responses can propagate beyond those routes.

## Construction and use

The standalone communication control has 54 gear types: 48 reference channels plus six message lanes.
It has 306 linear terms: 288 reference, 12 transport, six reception. Tensor
order is two and every term has strict single-edge support. The engine still
runs one synchronous reference update. Its update index remains simulation
bookkeeping; this change does not establish an asynchronous physical scheduler.

```bash
# Standalone local message preparation, reception and exact rewind
python -m universe24.demos.communication.run_communication --L 5 --tmax 20 --out runs/messages --tag messages --rewind

# Explicit previous fixed-six reference law and its original pulse preparation
python -m universe24.demos.communication.run_communication --model reference --L 3 --tmax 20 --out runs/reference --rewind

# Transport, reception, silence, finite influence, big integers and inverse
python -m unittest universe24.tests.test_communication -v

# Reproducible full tensors, seeds and trajectories for both constructions
python -m universe24.tools.export_fixtures runs/communication-fixtures
```

The pulse payload is three in each outgoing direction. `--bang none` prepares
no messages. `--bang standing` belongs to `--model reference` and is rejected
for communication. `--rng` is retained for the reference preparation; it does
not randomize the deterministic communication pulse, as recorded in metadata.

`*_messages.json.gz` records each edge's source, target, lane and integer
payload. This passive message log is distinct from `*_events.json.gz`, which
keeps the official arithmetic-click definition unchanged. `update` only locates
a record in the saved run; no tensor entry or reception reads it.

The old 48-channel reference is available as `reference_system(communication=False)`.
Its existing migration tests and 75-record, 20-update fixture continue to test
that exact construction. The communication control has a different tensor, seed and
trajectory. Original PR #29 evidence is in [local_communication.json](evidence/local_communication.json);
the older evidence has not been relabelled.
