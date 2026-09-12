# Configured neighbor topology

`configured-ports-v1` is an explicitly selected extension of the active
initialization-defined simulator. It changes the permitted neighbor graph;
it does not infer new forces, conservation laws or spatial dimensions.
The existing `cardinal-six-v1` contract remains the default when topology is
omitted. Historical research models retain their own geometry contracts.

## Immutable environment and bounded state

The topology supplies an ordered list of 2 through 26 distinct nonzero offsets.
Every offset has exactly three integer components from {-1,0,1}, and its negative
must also be present. A port identifies a travel offset, not a vector component
or the face from which a receiver is approached. Scalar fields still have one
component and vectors still have three. Port order is configured data and can
affect routing ties and indivisible allocation.

Reciprocal nonzero offsets occur in pairs, so the supported degree is even:
2, 4, 6, 8, and so on through 26. A bare count is insufficient; the offsets and
optional site pattern define which graph that count describes.

An optional site pattern selects residues modulo one or two. It is part of the
immutable environment, not a dynamic field or a filter applied after movement.
Every seed and materialized physical address must be a permitted site. All
configured offsets must preserve that site pattern. Periodic extents must
preserve it at the seam. Configured ports must not alias destinations or create
self-links through an undersized periodic box. Omitted-topology configurations
retain the existing small-domain behavior.

The optional top-level JSON `topology` object uses `model_id`, `offsets`,
`site_modulus` and `site_residues`. Its model ID is `configured-ports-v1`;
`offsets` is required. Omitting the site properties selects modulus 1 and the
single residue [0,0,0], permitting all integer sites. For BCC use modulus 2
with residues [0,0,0] and [1,1,1]. The run's `shape`, `boundary` and
`link_ticks` remain top-level configuration properties.

An immutable spatial-field baseline exists once per permitted site. Diagnostic
totals count the selected residues analytically, including incomplete residue
periods at open boundaries; excluded integer addresses contribute no baseline.

The environment is parsed once. Cells, carried records, pending transactions
and packets contain bounded values and identifiers, not copies of topology
definitions, formulas or expression trees. Port-indexed state has a fixed size
for the selected degree D, with D at most 26. Local update work is bounded by
D, the existing field/rule limits and the fixed resident capacity K. Host
scheduling and diagnostic costs may grow with the world; they are not physical
inputs to a local law.

Port-aware expression trees allow at most max(64, 8*D+16) nodes, with an absolute
maximum of 224 and the existing maximum depth 16. Expressions without port
context retain the 64-node bound. Each evaluated expression node still incurs
its declared modeled cost. Balanced sum trees allow norm checks to include all
26 outgoing owners without increasing expression depth. Each local rule still
has at most 32 assignments; independent fields may use separate ordered rules.

| Example | Offsets | Permitted residues modulo two | Connectivity in an even periodic box |
| --- | --- | --- | --- |
| Cartesian faces | Six signed unit axes | All sites | Connected |
| Full corner graph | Eight sign combinations of (1,1,1) | All sites | Four disconnected components |
| BCC sites | Eight sign combinations of (1,1,1) | (0,0,0), (1,1,1) | One component; one quarter of the full integer sites |
| FCC sites | Twelve permutations of (0,+/-1,+/-1) | (0,0,0), (0,1,1), (1,0,1), (1,1,0) | One component; one half of the full integer sites |
| Full cubic neighborhood | All 26 nonzero offsets in {-1,0,1} cubed | All sites | Connected |

Connectivity is a property to inspect, not an automatic promise for every
reciprocal list. In particular, a two-port graph need not connect a 3D box.
Edges drawn crossing between sites do not create an interaction node.

## Transport and causal timing

All selected ports use the run's common positive integer `link_ticks`. A packet
retains its payload, origin, chosen port and arrival time during transit. It is
owned by the link until completed delivery or escape. A completed arrival cannot
traverse another link in the same physical event. Carrier computation delay and
movement credit retain their existing contracts; neither can shorten a link.

Periodic wrapping preserves the port, signs, allocation/routing state and credit.
An open terminal link completes its full transit before adding its unchanged
payload to the escaped ledger. Crossing several boundary planes with one
diagonal packet is one escape, not multiple losses. An excluded interior site
is an invalid topology, not an implicit absorber or reflector.

In coordinate units, edge squared lengths can be 1, 2 or 3. Equal transit time
therefore does not mean equal Euclidean link speed when different lengths are
present. The causal guarantee is one selected graph edge per transit interval.
This extension supplies no common SI calibration, arbitrary-angle isotropy or
relativistic speed law. A diagonal hop is not a sequence of instantaneous
cardinal hops through intermediate nodes.

## Explicit routing policy

Explicit carried-record weights contain D nonnegative integers in port order.
For a direction provider on the configured topology, positive-dot affinity uses

```text
w_p = max(0, dot(direction, offset_p))
```

The transport object must explicitly select `direction_policy: "positive-dot"`
when it supplies `direction_field` or a `direction` expression for this model.

On the ordered cardinal-six list this reduces to the existing signed-axis
weights. A zero total affinity holds the record; it does not invent an available
direction. Weighted cyclic or balanced scheduling distributes actual hops using
the selected weights and their existing fixed-state policies. Scaling and
overflow remain explicit integer contracts; valid direction components do not
exempt derived dot products or stored routing weights from their own bounds.

For a reciprocal offset list, let M = sum_p offset_p outer_product offset_p.
Over a complete weight cycle, the displacement numerator is M*direction/2.
This is a derived diagnostic identity, not a matrix stored in each record.
Complete BCC8 and FCC12 lists have M=8I; the complete 26-port list has M=18I.
Their cycle displacement is parallel to the supplied direction, but its speed
still depends on direction and total affinity. Finite routing prefixes also
depend on ties and port order.

Arbitrary reciprocal lists need not have M proportional to I. Six face offsets
plus the pair +(1,1,1), -(1,1,1), with direction +X, produce mean displacement
(1,1/2,1/2) per hop. Thus affinity is a declared routing policy, not a promise
to reproduce every requested Cartesian velocity. Explicit weights remain the
way to select a different supported distribution; conservation of a stored
momentum register alone does not prove the correct relation between momentum
and displacement.

## Supported laws and explicit exclusions

Whole-record hold/move, extensive splitting, configured local field rules and
joint local field/carrier transactions use the selected ports. Local field
received/outgoing references range over all D indices. The received channels
are projections of delivered stock, not additional owners. Any directional
flux projection uses configured offset vectors and already delivered amounts;
it is not automatically a normalized continuum gradient.

The initial extension rejects configured topology with specialized outward
octant transport, specialized `spatial_couplings`, or native `event_program`.
Those mechanisms retain their cardinal-six assumptions until separately
generalized and validated. Eight historical population bins are not eight
neighbor ports. Rejection must be explicit during configuration/composition,
not silent fallback to the first six channels.

An existing local field law is not made physically topology-independent merely
because its operations parse. For transverse a and diagonal d=(1,1,1),
|d cross a| squared equals 3*|a| squared. Substituting d into the earlier
cardinal quarter-turn law would therefore break its norm/energy contract.
Topology-specific laws require explicit definitions and independent checks.

## Conservation and failure contract

Every field marked `conserved` retains its existing component-wise accounting:
actual resident plus in-flight and escaped/lost owners must match the initial
amount plus explicitly committed sources, with the applicable model ledgers.
Moving a whole record preserves its values. Splitting preserves each declared
extensive component, including signed amounts and retained remainders. It does
not generally preserve the sum of squared amplitudes.

Pair interactions remain transactions between co-located carried records, not
between geometrically crossing links. Configured pair momentum sums and energy
or norm expressions must hold before either replacement commits. Changing the
neighbor graph does not supply a different collision formula or contact normal.

For local fields, an invariant concerning transported inventory must include
retained stock and every relevant outgoing port. An expression containing only
the retained field is not the whole inventory after emission. Nonlinear energy
definitions additionally require a declared rule for merging amplitudes; global
energy conservation cannot be inferred from additive component accounting.
Joint delayed transactions revalidate against the actual local state at commit.

Invalid bounds, indices, shapes, capacities and invariants reject the failing
local proposal before partial ownership changes. Previously completed independent
events need not roll back. No world-wide momentum adjustment, energy repair,
silent clipping or float fallback is permitted.

## Independent acceptance requirements

[Topology invariant tests](../tests/test_topology_invariants.py) provide independent
examples; the existing integer, local-state, initialization, routing, spatial
transaction and runner gates remain applicable consumers.

- Default six-port configurations preserve actual states, routing phases, costs,
  transit and accounting, including existing small periodic domains.
- BCC8, FCC12 and cubic26 exercise ports beyond index five with real scalar and
  vector transport. An even 8-cube has 128 connected BCC sites and 256 connected
  FCC sites. Full corner connectivity remains four components of 128 sites.
- Resident and in-flight quantities are checked separately across multiple link
  times. Open diagonal escapes are counted once, and seams preserve full state.
- Nonzero co-located pair transactions preserve an independently specified
  momentum sum and energy/norm expression; an invalid transformation rejects
  atomically. Local-field checks include outgoing owners beyond port five.
- Integer limits and rejection tests cover dot-product weight growth, invalid
  coordinates/site membership, port references, capacity and arithmetic overflow.
- Renamed fields/types and translated configurations retain the same resolved
  laws. Cubic rotations are compared only with transformed topology/inputs and
  the declared routing-order limitations; arbitrary isotropy is not asserted.
- Unsupported specialized compositions fail explicitly. Recorded topology and
  actual packet destinations agree; display projection never supplies physics.

Passing these checks establishes the stated generic mechanisms and configured
invariants on the tested tree. It does not establish universal physical energy,
momentum, Maxwell dynamics or every law suggested by a field's name.
