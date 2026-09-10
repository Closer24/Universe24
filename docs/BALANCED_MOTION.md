# Balanced motion candidate and self-force investigation

Base: upstream `76676d48ffbe7fc53913f4d26464921cb20f72df`.
Candidate: `scalar-field-v12-balanced-motion`, exposed as `BalancedSimulation`
in `event_universe.api`. Baseline Simulation and the frozen reference retain
v10 behavior. This candidate fixes grouped movement; it is not an accepted
self-force correction and is not made the default.

## Feature contract

| Part | Contract |
| --- | --- |
| Law | Interleave cardinal steps using integer prefix counts; retain the shared speed budget |
| Local inputs | Momentum vector, movement budget, phase; supplied from the current particle |
| Evolving state | Existing budget and phase only; no new particle or cell registers |
| Parameters | Existing positive c_units; no angle-dependent or speed-dependent special law |
| Derived values | Absolute component weights, their sum, and hierarchical prefix counts |
| Outputs | Zero or one cardinal hop, updated phase and budget |
| Bounds | Momentum L1 sum must fit one positive 32-bit register; products checked as 64-bit work |
| Consistency | Fixed momentum from phase zero gives bounded coordinate error, exact cycle counts and the original hop rate |
| Tests | All 342 nonzero signed vectors with components -3 through 3, scale equivalence, invalid values, register boundaries, and rendered engine cases |

For hop index n and weights a,b,c with total T, the x count is floor(n*a/T).
The other n-floor(n*a/T) hops are distributed between y and z using the same
integer construction. Three absolute values, fixed arithmetic and at most two
axis decisions are needed. Local work and memory do not grow with elapsed time,
world extent or particle count. The existing phase stores n modulo T. This
retains exact full-cycle counts. There is no history replay, source identity map
or global input to the movement rule.

For constant momentum and phase initially zero, the x coordinate error is less
than one lattice cell; the y/z errors are less than two cells. The bound applies
to hop counts in an unwrapped chart with no blocked moves. It is not an exact
Euclidean line, exact rotational symmetry, a proof for changing momentum, or a
physical velocity definition. Coordinate priority remains explicit. A momentum
change reuses the phase modulo its new total; the fixed-direction proof does not
claim a smooth transition under arbitrary external forces.

## Reproduction and acceptance

`PYTHONPATH=src python tools/check_diagonal_motion.py` produces all five runs
through the existing full 3D GIF/HTML renderer, plus JSON measurements. It exits
1 if either the corrected movement or isolated-source requirement fails. No
failure is converted to an expected pass or suppressed through a tolerance.
The old no-field control is expected to reveal the grouped-axis defect and is
excluded only from acceptance of the new candidate.

| Run | Result |
| --- | --- |
| Legacy, source off, p=(600,400,0), cap=1000, 30 ticks | Displacement (30,0,0); wrong direction despite unchanged momentum |
| Balanced, source off, same momentum, 30 ticks | Displacement (18,12,0); momentum unchanged; bounded staircase error |
| Balanced, source=64, same momentum, 30 ticks | Same displacement and unchanged momentum in this short maximum-rate run |
| Balanced, source=64, p=(6,4,0), cap=12, force_den=1 | Fails at tick 3: momentum becomes (6,3,0) |
| Balanced, source=64, p=(1,1,0), cap=12, force_den=1 | Fails at tick 8: momentum becomes (1,-1,0) |

All shown local impulses retain opposite field impulses; total momentum staying
constant does not excuse self-force. The last two runs stop on the first impulse
and are labelled FAIL. These results prevent accepting the full requested fix.
The passing fast case must not be generalized to other speeds or long durations.

## Why self-force is still open

The adapter supplies the raw gradient of the combined scalar field. The current
turning policy discards its dominant-axis component; it does not calculate the
particle's own contribution. In particular, a parallel gradient (-6,-4,0) at
momentum (600,400,0) becomes (0,-4,0), which is not a parallel projection.

Rotating that filter would not identify self-field. With only combined local
scalar samples, a correction cannot generally distinguish a self contribution
from an external contribution producing the same samples. Simply erasing the
local field, disabling a source, using a one-particle count, or increasing the
force denominator would hide the defect or erase real interactions. None is used.

A full cure needs a separately specified local field/source coupling whose
self-response cancels by construction, or a justified fixed-size local state
extension that actually retains sufficient information. No such general law is
established by this change. It must pass low-speed and off-axis isolated tests,
external-field response tests, and the end-to-end LOCALITY-1 review before being
accepted. This investigation does not authorize nonlocal shadow-field inputs.
