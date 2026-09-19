# Adding a physical feature

The goal is a law that can be understood, tested and replaced independently of
the world using it. The binding sources are the [definitions](../SIMULATOR_DEFINITIONS.md)
and [architecture](ARCHITECTURE.md). The active schema and the laws a world
selects are in [the law of the ray](RAY_LAW.md) and [the engine's bookkeeping](ENGINE.md)
(the generic disturbance contract, DISTURBANCES.md, was deleted on 2026-09-19);
candidate identities and physical names belong in the world file. This
procedure does not change those rules.

## 1. Write a contract before code

Complete this table in the change description. A new configuration system is not
required for every feature.

| Part | What to define |
| --- | --- |
| Law | Local mathematical operation and assumptions; differences from the current model |
| Inputs | Names, meaning, units, integer bounds and the local source of each input |
| Evolving state | Values retained between updates, their owner and fixed size |
| Parameters | Constants for the run, meaning, source, ranges and rational representation |
| Derived values | Values calculated from inputs rather than stored as a second source of truth |
| Outputs | Fixed result or update proposal, including remainders and momentum exchange as required |
| Consistency contracts | Relations between values, read/write order, bounds and errors |
| Tests | Numerical inputs, independently established expected results and edge cases |

An explicit input is not necessarily a physically independent variable. A value
and remainder depend on the denominator; speed derived from momentum is not
another freely configurable parameter. Document and validate these relations
instead of maintaining conflicting representations of the same quantity.

## 2. Separate responsibilities

- `fields/`: shared calculations as functions or components with
  immutable parameters. Inputs and outputs are explicit. No world, entire Config,
  scenario identity or mutable globals. Evolving state, including remainders,
  enters as input and leaves as output; it is not hidden inside a law object.
- `core/`: fixed state contracts, addresses, scheduling, validation and commits.
  Extending state requires an explicit decision. Never add growing per-source or
  per-node maps.
- Initialization data selects active disturbance fields, types and expressions.
  Extend the validated generic expression/transport primitives only when needed;
  never use field-name branches or arbitrary Python loading as configuration.
- Configuration and API: parameter values and assembly. Reuse existing configuration
  when suitable. A generic component receives only required parameters or a small
  generic parameter record. A value that changes during a run is state or input,
  not a hidden constant.
- `runner`: initial conditions and execution. `diagnostics/`: measurements
  and display only. Measurement results must not feed back to repair the world.

Separation does not require a separate function for every scalar. Keep operations
sharing an atomic contract together, such as particle impulse and opposite field impulse.

## 3. Existing example: shared integer arithmetic

`core/integer.py` owns generic calculations such as `signed_divrem`, `ceil_div`
and `reduced_ratio`. A call takes bounded integer inputs and returns bounded
integer results with explicit errors; it does not read a world, a configuration
or a field name. Configured laws in initialization data select which
calculations run and with which parameters. The law can be checked without
running a world:

| Calculation | Input | Expected result |
| --- | --- | --- |
| `signed_divrem` | 7, 3 | quotient 2, remainder 1 |
| `signed_divrem` | -7, 3 | quotient -2, remainder -1 |
| `ceil_div` | 15, 7 | 3 |
| `reduced_ratio` | 6, 4 | 3, 2 |

This demonstrates the separation of a reusable calculation from its selection,
not a proven law of nature.

## 4. Test the separation

1. Generic law: numerical examples, remainders, zero, promised symmetries, invalid
   input and overflow. Also change a parameter while keeping inputs fixed.
2. Specific model: verify its declared component and parameter choices and their
   expected result. Comparing the output only with another call to the same formula is insufficient.
3. Integration: replace a law through the interface without rewriting the engine
   or copying formulas; verify timing, locality and momentum exchange as contracted.
4. Regression: preserve the baseline model. Different physical behavior needs an
   explicit model identity and separate results. Never alter a recorded baseline to pass a test.

Follow the AGENTS.md quality gates with the project Python 3.14 runtime.
Standard runs and tests are headless. Only an explicit visualization request
enables frame capture and rendered output. Pure local-function tests need no
world run. Add expected
results to the [test map](TEST_EXPECTATIONS.md). Write all comments and documentation
in English under the repository language rule in AGENTS.md.

## 5. Check extension limits

The active generic schema supports its bounded scalar/vector fields and
configured local rules; it does not allow unbounded state or arbitrary code.
Before adding a new value kind or coupling primitive,
check the state and scheduling contract and its capacity/error behavior. Postulate and schema changes must be explicit,
documented and tested within user authorization. Static checks enforce some
boundaries; code review also checks hidden dependencies and external state that
static analysis cannot fully prove or exclude.
