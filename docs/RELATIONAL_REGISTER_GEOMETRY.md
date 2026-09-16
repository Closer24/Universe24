# Identical one-way Registers and relational 3D geometry

## Status and source of the request

This design note records Alon Gonen's clarification of 16 September 2026:
space is a three-dimensional arrangement of identical one-way Registers;
length is measured by traversing the network and counting transitions, not by
the lengths of edges in a drawing. The arrangement must support calculations
on a discrete three-dimensional space.

This is documentation of the requested design, not a topology migration, a new
LocalRule, a minimal-register theorem or evidence that observed spacetime has
been recovered. It refines the geometry discussion in [issue 142](https://github.com/Closer24/Universe24/issues/142).
The [terminology](TERMINOLOGY.md), [architecture](ARCHITECTURE.md),
[postulates](../POSTULATES.md) and [simulator definitions](../SIMULATOR_DEFINITIONS.md)
retain their implementation authority.

## 1. Identical one-way building blocks

Use the same bounded state space, capacity and intrinsic update rule for every
Register. Abstractly, with a distinguished empty input/output value:

```text
(s_r_next, output_r) = F(s_r, input_r)
```

Each Register owns its private state, receives through one declared input and
emits through at most one declared output. An empty output can represent a
locally retained state under an explicitly defined rule. Identical Registers
need not have identical current states. Their spatial roles follow from wiring,
not from separate x-, y- or z-specific kinds of Register.

A Node remains the canonical name for a physical location. In the private-register
proposal it groups Registers; it does not automatically add another physical
substance, a hidden shared state, a mixer or a free computation step. Input and
output are roles of carried values, not new substances.

A one-way channel must not be silently reversed. Return propagation needs its
own permitted directed path. All physical updates remain bounded and integer;
changing the drawing does not authorize nonlocal reads or skipped transitions.

## 2. Distance comes from permitted transitions

For a directed path gamma, define its length as its number of elementary
transfers, not its number of drawn pixels:

```text
L(gamma) = number of directed transfers in gamma
 d_forward(A, B) = min L(gamma), over permitted paths A -> B
```

The empty path has length zero. If B is unreachable from A, the mathematical
distance is infinite. Symmetry is not automatic:

```text
d_forward(A, B) need not equal d_forward(B, A)
```

The unit being counted must be fixed: Register-to-Register transfers, not a
variable mixture of elementary transfers and contracted Node-to-Node paths.
A diagram may stretch or fold edges without changing this distance.

Route length and elapsed model time are different readouts when Registers can
wait or interactions take additional time. With unit-time transfers:

```text
elapsed_steps = transfer_steps + declared_local_wait_or_interaction_steps
```

Shortest-path calculations are mathematical definitions or external diagnostics.
A physical Register does not get a global path search, a global coordinate or
knowledge of undelivered remote state. A traversal measures the route actually
taken; it does not establish that no shorter route exists without further work.

## 3. What would establish a three-dimensional arrangement?

A three-dimensional drawing is insufficient. The permitted transfer and
interaction structure must provide three independent directions of large-scale
accessibility.

One sufficient construction uses bounded local groups with diagnostic addresses
(a, b, c) in Z^3. The groups provide directed paths to the six groups:

```text
(a + 1, b, c)    (a - 1, b, c)
(a, b + 1, c)    (a, b - 1, c)
(a, b, c + 1)    (a, b, c - 1)
```

The internal paths and any necessary routing interactions must actually be
permitted and have uniformly bounded positive cost in elementary steps. Paths
must concatenate: six separate fixed wires do not by themselves allow an
arrival to choose or coherently couple into its next direction. The group size
is bounded independently of the total network size. There must also be no
long-range shortcuts that bypass the intervening groups.

Under these conditions, the step distance between comparable group locations is
bounded above and below by constant multiples of the cubic-grid distance, up to
bounded within-group offsets. The number N(n) of accessible locations within n
steps consequently grows as Theta(n^3) on the infinite network, or at scales
below the boundaries of a finite test region. The cubic growth is a consequence
of this construction, not a sufficient definition of Euclidean geometry by
itself.

Coordinates label the construction for verification; local physical rules need
not read them. Six directions need not meet in a single Register. Bounded groups
of identical Registers may implement them, provided their actual local wiring,
state access and interactions meet the stated conditions.

This supplies a possible basis for discrete 3D calculations. It does not prove
Euclidean step distance, isotropic propagation, Lorentz symmetry or the geometry
inferred by physical detectors. Those require their own dynamics and readouts.

## 4. Why a network of uncoupled one-input/one-output Registers is not enough

Assume each Register has a single fixed predecessor, a single fixed successor
and no other interaction or state dependency. Components are chains or cycles.
Starting at one Register, at most n + 1 distinct Registers can be reached in n
forward transfers. Folding such a chain into a cube does not create another
physical connection.

Consequently, spatial access between different routes needs an explicit local
mechanism: for example, a jointly declared operation at a meeting of two
Registers, schematically:

```text
(s_1_next, s_2_next) = C(s_1, s_2)
```

This is a possible design extension, not an existing permission. A meeting has
two state dependencies even if each transport Register still has one input and
one output. If private-register rules forbid peer-state access and shared
mixing, C cannot be inserted under the name of geometry. Its locality, ownership,
capacity, timing and uniform implementation would first need an explicit
contract compatible with the user's requirements.

If all such interactions, routing changes and additional dependencies remain
forbidden, the fixed one-predecessor/one-successor network remains one-dimensional
in accessibility. The assertion that every Register is identical does not remove
this distinction.

## 5. Where 36 comes from

The conventional cubic description has six Ports:

```text
P = {+x, -x, +y, -y, +z, -z}
```

Choosing one private Register for every ordered entrance/exit pair gives:

```text
R[p, q], with p in P and q in P
number_of_route_registers = 6 * 6 = 36
```

Here p names the face through which a value enters and q the face through which
it leaves. For each entrance there are six exits:

| Route class | Exit relation | Count |
| --- | --- | ---: |
| Perpendicular turn | q is one of four Ports perpendicular to p | 6 * 4 = 24 |
| Straight continuation | q is the opposite Port to p | 6 * 1 = 6 |
| Return to the incoming neighbor | q equals p | 6 * 1 = 6 |
| Total | Every ordered pair | 36 |

For example, entrance +x and exit -x is straight travel through the Node;
entrance +x and exit +x returns to the same neighboring side. Removing diagonal
pairs R[p,p] removes the six return routes and leaves 30, not 36. Keeping only
perpendicular routes leaves 24.

All 36 Registers can have the same intrinsic structure and rule. Their entrance,
exit and successor wiring distinguish their roles. This full ordered-pair
representation provides explicit independent route state under the private
ownership design; 36 is not derived from three-dimensionality or from the
requirement that the Registers be identical.

### Implementation evidence checked on 16 September 2026

The [main-branch Node contract](https://github.com/Closer24/Universe24/blob/e5b5911ab13373e08345cf971a6ae8d7e9cb462e/docs/NODE_VECTOR_PROCESSOR.md)
still describes a six-Port lattice and explicitly separates direction count,
record capacity and interaction arity.

The unmerged [PR 144](https://github.com/Closer24/Universe24/pull/144), extending
[PR 141](https://github.com/Closer24/Universe24/pull/141), implements the cubic36
private-register candidate. Its [contact contract at the inspected revision](https://github.com/Closer24/Universe24/blob/eee75f5e748ff073c3801e9f87e7868e67b05e82/docs/PRIVATE_REGISTER_CONTACTS.md)
explicitly declares all 36 ordered pairs, adds straight and return routes to
the older 24 perpendicular routes, and gives the Node no mixer, action or delay.
It also describes the supplied inter-Register wiring as a permutation. These
are revision-specific implementation statements, not a timeless status claim.

The fact that this candidate exists does not establish that 36 is minimal. Nor
does its fixed permutation wiring alone prove the three-dimensional
accessibility conditions in section 3. The private transport and the broader
relational geometry target must not be conflated.

## 6. Route counts are not information-capacity proofs

Keep these quantities separate:

```text
neighbor count != directed channel count != ordered route count
               != independent state dimension != storage word count
```

A six-component input and a six-component output can be related by a 6 by 6
matrix. Its 36 entries are transformation coefficients, not automatically 36
independent dynamic states. Conversely, 36 independently occupied private
Registers cannot generally be replaced by six state slots merely because the
matrix has six rows. No such compression is authorized by this note.

Packing several inputs into one wider word does not reduce the information they
contain. Serializing simultaneous inputs can change modeled timing and which
values meet. A proposed representation change must preserve all relevant
independent states, coherent alternatives, ownership, capacities, interactions
and delays, or explicitly acknowledge a change in the model.

## Design statement

Space is represented by identical one-way Registers and their permitted local
connections. Route length is counted in elementary transfers. A Node groups
local Registers without adding an undeclared action. Three-dimensionality must
be demonstrated from the complete transfer and interaction network, not from a
cubic drawing or a count of 36 routes. No minimum Register count or reproduction
of observed spacetime is established by this note.
