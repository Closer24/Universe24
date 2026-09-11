# Generic field definitions and positive records

The Highlights document requires several fields in one cell, described by field
definitions rather than engine branches. `fields/definition.py` defines the
immutable contract; `fields/definitions.py` supplies usable adapters for existing
scalar and octant arithmetic. A generic bank owns transport and invokes the same
callbacks for every definition. These modules do not commit world state or
establish a new physical law.

## Stored representation

Each new field value uses two strictly positive integers `(magnitude, code)`.
Code 1 means zero and requires magnitude 1; code 2 means positive and code 3
negative. Zero is `(1,1)`, positive one `(1,2)` and negative one `(1,3)`. Both
extrema of the old signed physical range remain representable without extending
an individual register's bound. Booleans, out-of-range values and noncanonical
zero are rejected before use.

Each definition declares its encoding and validator. Scalar state has four
registers (encoded value and remainder); its packet has two. Octant state and
each packet have sixteen registers (eight populations), rejecting negative
decoded populations. Each of six response faces holds one encoded pair. Widths
count actual positive registers, not decoded values. Transient arithmetic reuses
the existing bounded integer laws.

This contract covers new field records and packets. Legacy particles, clocks,
momentum ledgers and sentinels have not been converted by these modules. The
whole simulator must not be described as positive-coded on this evidence alone.

## One definition, two local phases

| Property | Contract |
| --- | --- |
| `publish(old_state, source_count, phase)` | Six fixed outgoing packets; no mutation |
| `absorb(old_state, incoming, source_count, phase)` | One new fixed state and six encoded source-facing response values |
| `response(faces)` | A transient bounded working vector for the existing dynamics adapter |
| `source_rule`, `combination_rule`, `decay_rule` | Descriptions of operations actually selected by the callbacks |
| `propagation_rule`, `response_rule` | Explicit transport and local response meanings |
| `allowed_faces`, `allowed_directions` | Immutable codes 1 through 6; forbidden nonzero packets and responses are rejected |
| `response_unit` | Compatibility identifier checked before adding response vectors |

Face order is +x,-x,+y,-y,+z,-z. Incoming and response faces point toward the
supplying neighbor; outgoing direction codes describe travel. A field traveling
only along +x needs allowed faces `(1,2)` to receive through -x and send through
+x, with allowed directions `(1,)`. Its callback must actually generate only
those outputs; changing metadata does not silently rewrite the law.

Scalar publication sends the old scalar; absorption adds its occupancy source,
old division remainder and six delivered scalars. Octant publication adds the
occupancy source, then splits fixed sign sectors with the existing exact rule;
absorption sums received populations without adding the source again. Neither
adapter stores source identities, growing history or a mutable private cache.

Both factories use an explicit candidate response-input unit so the experimental
bank can add integer imbalances. This is a computational composition choice,
not a calibration showing equivalent physical strength. Different response-unit
identifiers must not be silently summed.

## Examples and limits

`scalar_definition(source_strength=7, denominator=7)` changes zero state and zero
incoming packets with one source to scalar 1, remainder 0. Publication still
contains the old value; the new value publishes next time.
`octant_definition(source_per_octant=3)` with one source and zero populations
publishes four units along each cardinal direction: four compatible octants
contribute one each. Old populations transfer once.

Definitions and widths are fixed at world construction. Adding a definition
must not require a field-name branch in core. For fixed field count, widths and
K, local work remains bounded; total host storage and runtime are separate.
Acceptance includes two field types coexisting and a third definition supplied
without changing the engine.

The initial runtime supports unit-length links only; other positive lengths
require an explicit unsupported-operation error. Publishing only once per long
link cycle would change persistent source behavior. No such shortcut or unbounded
queue is part of these definitions. Complete field/particle causal scheduling
and moving self-force remain independent acceptance requirements.

## Runtime and accounting

`GenericFaceSimulation(config, definitions=(scalar_definition(), octant_definition()))`
uses the same `FieldBank` for both definitions. The model identity is
`generic-positive-field-bank-v1-experimental`. Its optional `collisions=True`
selects the existing local pair law. Definition responses are added with bounded
working arithmetic before the shared full-vector particle response and exact
opposite local momentum exchange. No fake six-face record narrows that sum.

Each bank cell persists only definition state and six encoded response faces:
16 positive integers for scalar, 28 for octants, or 44 for both. Six fixed packets
per definition exist in the transient routing buffer, not as retained history.
Old/new proposal dictionaries and a three-component response snapshot are host
working buffers; the inherited six-value display/response snapshot and K-slot
eligibility buffer are also reported separately. No count implies constant total
host cost. Definitions and neutral records are immutable configuration overhead.

Sparse scheduling requires zero state, zero incoming packets and zero occupancy
to remain quiescent at every phase. Construction validates phase zero; purity and
all-phase quiescence remain obligations of an injected definition. All outgoing
and incoming packets, new state and response faces are validated before an atomic
bank commit. A failed later particle update still faults the enclosing world.

Particles use the previous local response, preserving the explicit candidate
schedule. The isolated generic octant case still develops a self-response residue;
no physics approval follows from multitype composition or positive coding. The
existing contention gate remains mandatory as well. `link_length=1` is currently
the only accepted length; larger positive values fail explicitly, and no silent
change to source frequency or particle transit is made.

The display's `field_faces` and `face_at` expose the first configured field only,
identified by `display_field_name`; `field_faces_by_name` exposes every field
separately. Scalar potential and octant population magnitude are not summed for
display. Physical response always invokes every definition's response callback.
