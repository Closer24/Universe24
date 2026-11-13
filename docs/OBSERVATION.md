# Nodes, face transmissions and observable clicks

`NodeView(state,index)` exposes a complete node and six `FacePort` objects.
Each face groups eight existing channel labels in +x,-x,+y,-y,+z,-z order.
A port and its neighbor's opposing port refer to one `EdgeRef`. Its base
coordinate is an identity convention, not ownership. Each endpoint retains
its own state; a passive view cannot update it or create an edge-length bank.
Views are snapshots: construct a new view for a new Engine state.

`b` is the current gear state; `a` is its prior value and `r` its retained
remainder. A face-specific transmission rule must emerge from the fixed
polynomial over these rows. The current implementation proves a signal/clock
circuit for each orientation separately. The six port groups do not prove
six independent simultaneous circuits or a scalar common length per edge.

## The observer boundary

The external observer reads canonical arithmetic clicks, never hidden metric
fields, seeds or full traces. `inspect_click_file` reports recorded addresses,
channels, classes and quotients. These addresses and update indices do not
become distances and proper times by being present in a record.

`reconstruct_channel_from_clicks` additionally takes a channel, node-address
count, complete horizon, and explicit initial a and b histories. Histories
may be positive integer scalars or complete positive integer arrays. Under
the selected coupling and constant-carry positive domain:

- a recorded quotient gives `next = quotient - old`;
- a quiet update requires `old == current == next`;
- an impossible missing record or nonpositive inferred value is rejected.

All outputs are derived from those public inputs. Large integers are serialized
as decimal strings without changing the process-wide integer digit limit.
The CLI supports uniform scalar initial histories; the Python API also supports
arrays. No arbitrary latent state is inferred without calibration.

A file alone cannot prove that every valid event was retained. It detects
malformed, duplicate, mixed-provenance and out-of-order records, and some
calibration inconsistencies. Full completeness is checked by independent
replay of the saved run. Cross-run comparison excludes only run/event identity;
quotients, signs, channels, addresses and all other observation payload remain.

Arithmetic classes follow `(r_next-r) mod 6 = 2*(u mod 3)`: C0, C1 and C2
mean remainders 0,2,4 respectively on emitted events. They are not first,
second and third handshakes. The built-in law emits only C0. No photon count,
Born rule or Bell conclusion is attached to them.
