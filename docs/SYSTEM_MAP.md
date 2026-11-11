# Current system map

The 0.5.0 consolidation adds disjoint channel ownership, local communication and explicit probe experiments; see [UNIFIED_SYSTEM.md](UNIFIED_SYSTEM.md) and [fresh validation](evidence/universe24_unification.json). The physical Einstein metric remains the sole metric of the main event board.

## Integrated Einstein event board

The default is now `python -m universe24`: nonlinear ADM, complex scalar matter with opposite U(1) charges and geodesic dark dust. All updates use the fixed-six Engine; the metric, stress and event records come from the same retained state. See [equations](INTEGER_ADM.md), [events and matter conventions](UNIVERSE24_EVENTS.md), and [commands](../README.md).

The reference baseline and fixed-six research results below remain controls; they no longer describe the CLI default. Retired variable-divisor calibrations stay retired.


The system consists of a fixed storage graph, a local integer coupling tensor,
a complete seed, and one scalar Rule3 operation. The default construction has
48 group-labelled channels. Optional experiments can declare different
channel sets without introducing a second engine.

## Generic transition and inverse

For each channel retain `(a,b,r)` with integer `a,b` and `0 <= r < 6`.
Evaluate the fixed polynomial input from the same complete old snapshot, then
apply

    quotient, r_next = divmod(2*u+r, 6)
    a_next = b
    b_next = quotient-a.

Recover old `b` from new `a`. In the declared acyclic old-history order,
compute the old input, recover `r=(r_next-2*u)%6`, and then recover
`a=(2*u+r-r_next)//6-b_next`. This proves reversibility of the retained state;
it does not prove stability or physical conservation.

## Where communication occurs

Every monomial is a local read. The strict condition counts the target and
both endpoints of every physical link gear; all participating vertices must
lie on one node or one face edge. A path of several updates may communicate
farther through successive local reads. A single update does not let every
node read every other node.

The default reference matrices route channels to six neighboring sites.
They do not automatically make all representation sectors interact or make
all structures form bound systems. Use the live inventory tool to inspect
actual dependencies of a selected tensor.

## Preparation, evolution and observation

| Module | Role |
|---|---|
| `layers/` | Compile fixed integer tensor entries before the run |
| `prepare/` | Set complete integer `a,b,r` arrays before the run |
| `core/` | Evaluate local inputs and apply the shared scalar operation |
| `observe/` | Read snapshots and produce passive records |
| `tools/` | Run declared protocols and report exact evidence |
| `experiments/` | Optional constructions with separate assumptions |

An official click requires a nonzero quotient and a changed complete local
triple. Missing events can hide stationary nonzero quotients. An event-only
decoder therefore needs explicit assumptions and retained initial information.
A click classification never selects a future state or supplies a new force.

## Scope of the current physical claims

The finite group, tensor order, local reads and inverse are mathematical
properties. The [geodesic example](PPWAVE_OPERATIONAL_ROUTE.md) supplies one
restricted connection to a continuum solution, with a declared calibration.
It does not make all board coordinates physical spacetime, all cycles proper
clocks, or all emitted records particle detections.

The former field/cosmic assembly is historical. Its component inventory,
force normalization and detector claims do not describe the new default.
See [research status](RESEARCH_STATUS.md), [the algebra](MODEL.md), and the
[archive](archive/pre-fixed-six/README.md).
