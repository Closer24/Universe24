# Local clocks, packets and remainder registers

These are reusable **initial preparations** under `research.components`, separate
from experiments, the engine and the Presenter. They assign ordinary `(a,b,r)`
triples once. The unchanged engine then applies Rule3 to the entire board. No
component has a runtime method, alternative law, force, gate or click callback.

All preparations on this page require the existing **+++ coupling**, background
`(0,0,2)`, 48 channels per site, six neighbors and `num=den=1`. The full tensor is
checked before composition. Other sign templates remain valid model choices;
these particular behavioral contracts have not been generalized to them.

## Available components

| Factory | Prepared data | Established behavior and limit |
| --- | --- | --- |
| `CompactFiveClock(shape='dimer')` | Two core sites and ten halo sites, all channels | Exact isolated full-state period 5 |
| `CompactFiveClock(shape='plaquette')` | Four core sites and sixteen halo sites | Exact isolated full-state period 5 |
| `LocalizedSixClock()` | Eight cube sites and twenty-four halo sites | Exact isolated full-state period 6; six phases, six core remainders and two halo parities |
| `CooperativeClockPair()` | Two cubes and one explicitly shared halo | Joint period 6; either counter-masked constituent alone leaks into the shared halo at step 2 |
| `EvenPacketSource()` | Eight guide addresses and sixteen transverse remainder addresses | Complete packet translates one lattice site per update on its prepared periodic guide |
| `RemainderTarget()` | A complete twelve-site resting neighborhood with four special channels | Passive hardware; the downstream arrangement below scatters, then resets |
| `RegisterWriter()` + `SourceOverlapRegister()` | A packet with four explicit sockets filled by resting r0 hardware | Prepared source-overlap halo clearing, followed by a separately prepared read probe |

A separate [finite-guide clock-link package](../research/clock_link_v1/README.md)
adds data-only source, resting corridor and endpoint preparations. One local
source activates the guide, the endpoint returns a phase front, and the source
and endpoint retain cyclic parity records. This has its own declared domain
and fresh full-state audit; it does not repair the failed repeated-read register
below or establish arbitrary interaction between assembled links.

`phase`, `core_remainder`, `halo_parity`, presence flags and coordinates require
exact Python types. `active=False` on clocks removes counters **and retains the
prepared remainders**; it is a counter-mask control. `present=False` on the new
even packet restores guide r0 and transverse background r2, so the whole packet
is absent. The older `GuidedPacketSource` keeps its historical counter-mask
semantics. The two sources are distinct APIs.

## Compose several blocks

```python
from research.components import (
    BoardSpec, CompactFiveClock, LocalizedSixClock, place, finalize,
)

prepared = finalize(BoardSpec(41), [
    place(CompactFiveClock(shape="dimer"), at=(8, 8, 8), name="dimer"),
    place(CompactFiveClock(shape="plaquette", conjugated=True),
          at=(21, 21, 8), name="plaquette"),
    place(LocalizedSixClock(), at=(29, 12, 25), name="cube"),
])
states = list(prepared.engine.evolve(prepared.initial, 30))
assert states[-1] == prepared.initial
```

This is **one board and one update**, not three independently executed engines.
The complete prepared halos prevent counter activity escaping these isolated
blocks, and their supports are disjoint. The joint return time is 30, the least
common multiple of 5 and 6. The ordinary composer accepts general placements;
successful construction alone does not establish a new interaction behavior.

The same example is a generic JSON experiment:

```sh
python -m research.experiments.run --spec research/component_families/examples/three_clocks.json --output runs/three-clocks
python -m research.experiments.run --spec research/component_families/examples/even_packet.json --output runs/even-packet
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/runs/three-clocks/The_Presenter.html` in a browser.
Drag the cube to rotate it; choose channels to inspect their clocks and gears.
The display reads the complete saved state. A file attachment preview may not
execute JavaScript; it is not evidence that the experiment has no data.

Every new Patch recipe also works in the existing JSON runner. `at`, proper
orientation lift, explicit `wrap`, named ports and passive observations use the
same [component contract](COMPONENTS.md). Orientation changes both positions
and channel labels. No implicit wrapping, overwrite, tensor mixing or dynamic
component substitution is permitted.

## The algebra of the clocks

For an all-channel-uniform core whose sites have `k` core neighbors, the common
core input is `u=k*b`. With a counter-zero halo the scalar recurrence is

\[
 (\ell,r')=\operatorname{divmod}(2kb+r,6),\qquad (a',b')=(b,\ell-a).
\]

For the cube, `k=3`, so `ell=b`, `r'=r`, and `(a,b)` follows
`(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0)`. A halo site has one core neighbor.
Writing `P_t=sum_{j<t} b_j`, its remainder is `h+2*P_t`. Choose `h` so this
quantity stays in `0..5`; its quotient remains zero, so halo counters stay zero.
The factory computes that allowed interval and selects the requested parity.
Every exterior site has zero counter input and stays fixed. This proves the
complete cycle, including remainders, for the declared isolated preparation.

The period-five core triples are:

| Phase | Dimer (`k=1`) | Plaquette (`k=2`) | Halo r |
| --- | --- | --- | --- |
| 0 | `(0,1,4)` | `(0,1,2)` | 0 |
| 1 | `(1,1,0)` | `(1,1,0)` | 2 |
| 2 | `(1,-1,2)` | `(1,-1,4)` | 4 |
| 3 | `(-1,-1,0)` | `(-1,-1,0)` | 2 |
| 4 | `(-1,0,4)` | `(-1,0,2)` | 0 |

Substitution into the same Rule3 proves each row and its return. The exact
conjugation `J(a,b,r)=(-a,-b,4-r+2*(r mod 2))` also transforms the halo. Counter
sign reversal alone is insufficient. No family-specific `num/den` is installed.

In the cooperative pair, opposite cube phases produce opposite `b` values at
the four shared halo sites. Their input sum vanishes, and shared r2 stays fixed.
The other halo sites use r0 or r4. Superposing two isolated cube factories would
instead request conflicting halo triples and is correctly rejected. The joint
factory makes the shared preparation explicit. This proves a prepared
cooperative cycle, not spontaneous binding, attraction or preference for
complexity.

For +++ the mathematical density `q=3*(b-a)+floor(r/2)-1` obeys
`q'-q=u-6*b`. Summing over the periodic board gives an exactly conserved total
relative to the background. This bookkeeping quantity is **not established
electric charge**, and a clock period is not a physical mass.

## Guided scatterer

```python
from research.components import assemble_scatterer
prepared = assemble_scatterer(side=129, gap=12)
```

This returns one `PreparedBoard` with actual `initial`, `ports` and `manifest`.
At sides 129 and 145, gap 12, the four initially resting downstream r0 channels
produce three complete packets: the original forward packet, a forward packet
delayed by six sites, and a reflected packet. Whole states 24 through 48 equal
the stationary guide and reset target plus all three 24-address packets. Each
packet includes every transverse remainder and has an exact isolated one-step
translation. The source-only controls remain one complete translating packet.

`source_present=False` is true absence, giving a stationary all-counter-zero
board with either target mask. Historical source-off remote-study controls
retained 24 source remainder entries; they are not these new absence controls.
The publication includes the original source-present/target-present and
source-present/target-absent trajectories at both sizes. True absence is checked
by the exact zero-counter stationarity identity and tests.

The target resets and has no retained remote memory in this experiment. Three
lattice packets are not three established photons or a physical energy law.
Other gap, size, translation and interaction choices require their own tests.

## Source-overlap register and one controlled read

```python
from research.components import assemble_remainder_register
prepared = assemble_remainder_register(
    side=233, probe_delays=(28,), writer_present=True,
    probes_present=(True,), translation=(3, 2, -1), wrap=True,
)
```

All packets, guides, register hardware and the optional distant reference clock
are prepared before step zero. The helper returns **one `PreparedBoard`**, whose
manifest and ports describe the final translated assembly. No separate
untranslated manifest is returned as if it represented the final board.

All four register addresses overlap the writer's **initial transverse remainder
halo**. Departure clears resting `(0,0,0)` to `(0,0,2)`; the local quotient is
zero and there is no register C event during writing. Source absence keeps the
same separately owned register hardware. This is source-overlap clearing, not
an arriving remote signal writing a disjoint detector.

The later orthogonal read probe supplies the same `u=-1` in both histories:

| Stored triple | Next triple | Quotient | Native observation |
| --- | --- | --- | --- |
| `(0,0,0)`, unwritten | `(0,-1,4)` | -1 | C2 |
| `(0,0,2)`, written | `(0,0,0)` | 0 | No C |

The positive output means **unwritten**. r4 is transient after reading the
unwritten state, not the stored written value. Other events elsewhere on the
board are retained; this is not globally exclusive selection or collapse.

All four writer/probe masks at `(L,delay,translation)=(233,28,(3,2,-1))` and
`(257,31,(-2,3,1))` pass the fixed single-read contract. The complete 576-triple
local region restores to its own pre-read state at every state 51..56. The
separate period-six reference supplies local C-event ordinals 17 and 19 at the
two first reads; assigning them uses simulator ordering, not physical distant
clock synchronization.

**Two-read composition currently fails.** The full eight-mask test at L337,
delays `(28,60)`, retains six passing single/no-probe controls and two failing
dual-probe cases. With both probes present, the complete second incoming
template fails at states 50..52. At scheduled read 57 the stored r0/r2 is correct but actual
`u=0`, not -1. A coincidental no-C bit is not a valid second read. Local region
restoration still passes. Arbitrary packet trains, repeated-read memory,
disjoint remote writing and quantum measurement are not established.

## Reproduce and extend

The [compact evidence package](../research/component_families/README.md) ships
31 original audited preparations, 1,671 full-state hashes and 1,640 transitions.
Every initial triple, fixed coupling, background, horizon, original record hash
and readout definition is retained. Replaying regenerates every complete state,
checks an independent matrix-derived gather/inverse, and reassesses positive and
negative fixed observations. It does not claim all 553 local study recordings
are shipped.

The next decisive work is a **disjoint remote writer** and isolation of later
read inputs from earlier scattered outputs, using only new initial preparations
under the same fixed law. Construction validity and behavioral acceptance must
continue to be tested separately.
