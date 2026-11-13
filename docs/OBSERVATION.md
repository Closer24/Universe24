# Nodes, face transmissions and observable clicks

`NodeView(state,index)` exposes a complete node and six `FacePort` objects.
Each face groups eight existing channel labels in +x,-x,+y,-y,+z,-z order.
A port and its neighbor's opposing port refer to one `EdgeRef`. Its base
coordinate is an identity convention, not ownership. Each endpoint retains
its own state; a passive view cannot update it or create an edge-length bank.
Views are snapshots: construct a new view for a new Engine state.

`b` is the current gear state; `a` is its prior value and `r` its retained
remainder. In the selected positive domain all 48 current rows encode live
occupation as `b=1+z`. Eight slots per face give capacity 48 per node. A
quartet shared by two endpoints holds its values during the edge stage when
exactly three slots are occupied; otherwise its values rotate across the edge.
The fixed onsite permutation then turns channels between faces. The whole
update is one fixed cubic polynomial. There are no static markers, extra
clock counters or dynamically retained link lengths.

`face_load_profile` reports occupation, empty capacity and the current gate
condition from a snapshot. Its `held_occupation` includes both three-slot
blocked quartets and four-slot saturated quartets, reported separately as
`blocked_quartets` and `saturated_quartets`. A full quartet is unchanged as a
word even though the gate's cyclic permutation still applies; identical bits
cannot identify individual carriers. `moving_occupation` is transferable
occupation in open quartets before the onsite turn. These labels are capacity
diagnostics, not measured particle waiting times, material species or metric
lengths. Signed edge currents give an exact node-occupation continuity check.

## The observer boundary

`inspect_click_file` reads canonical arithmetic clicks without opening seeds,
full traces or hidden metric fields. It reports recorded addresses, channels,
classes and quotients. These addresses and update indices do not become
distances and proper times by being present in a record. Reconstruction is a
separate operation requiring explicit public initial calibration.

`reconstruct_channel_from_clicks` takes a channel, node-address count, complete
horizon, and explicit initial a and b histories. Histories may be positive
integer scalars or complete positive integer arrays. Under the selected
coupling and constant-carry positive domain:

- a recorded quotient gives `next = quotient - old`;
- a quiet update requires `old == current == next`;
- an impossible missing record or nonpositive inferred value is rejected.

All outputs are derived from those public inputs. An occupied channel can be
quiet, so its initial value cannot in general be discovered from an unaided
click file. Large integers are serialized as decimal strings without changing
the process-wide integer digit limit. The `observe-clicks` CLI supports uniform scalar
initial histories; the Python reconstruction API also supports arrays. No
arbitrary latent state is inferred without calibration. The current model has
no E/B field API: the previous law's transverse-plane and straight-axis results
do not apply to this tensor.

A file alone cannot prove that every valid event was retained. It detects
malformed, duplicate, mixed-provenance and out-of-order records, and some
calibration inconsistencies. Full completeness is checked by independent
replay of the saved run. Cross-run comparison excludes only run/event identity;
quotients, signs, channels, addresses and all other observation payload remain.

Arithmetic classes follow `(r_next-r) mod 6 = 2*(u mod 3)`: C0, C1 and C2
mean remainders 0,2,4 respectively on emitted events. They are not first,
second and third handshakes. The built-in tensor's coefficients are multiples
of three, so carries are constant and emitted events are only C0. A fixed
channel triple emits no event; in the positive sector every nonquiet triple
has a positive quotient. No photon count, Born rule or Bell conclusion is
attached to these records.

## The passive board

```bash
python -m universe24 board --run runs/output --out runs/board.html
```

The board reads the saved run report, sealed initial bundle and canonical
click file. Complete initial a,b,r are explicitly public calibration. It
checks the selected tensor identity, raw a,b in {1,2}, positive carries in 1..5
and the initial inverse-history relation `a=1+F_inverse(b-1)`. Evaluating that
relation validates the public preparation; it does not generate future frames.
All subsequent channel histories come from the calibration and click quotients,
without opening the full transition trace or calling Engine. Run provenance
and the click checksum are also checked. Checksums
and record counts detect inconsistency with the saved report; they do not
independently establish completeness. Run `verify` for the separate full replay.

The resulting self-contained HTML contains precomputed recorded frames.
Playback and slice controls select those frames; browser code never evolves a
second model. The display shows node occupation, transferable/held occupation,
empty capacity, arithmetic clicks, each selected node's six faces, occupied
support and concentration. Fixed symbolic work and integer magnitude bits are
reported separately. All these measurements are passive readouts.

The displayed preparation metadata exposes the burst's seeded halo, radius,
frame, center and total occupation. Disabling the halo supplies the symmetric
free-transport control. A visually spreading burst alone cannot establish
capacity feedback. The recorded index orders updates; the lattice drawing is
an address map, not an inferred Einstein event geometry. Concentration can
rise again. Ordinary matter, dark matter, Einstein geometry and gravitational
waves remain explicitly unestablished. Isolated vacuum transport is identified
only at that operational level, not as a demonstrated photon.
