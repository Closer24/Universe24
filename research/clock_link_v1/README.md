# Autonomous guided clock link

One initially active channel launches a phase front along a resting remainder
guide. The endpoint records arrival, reflects the front, and the source records
its return. The cycle repeats using only unchanged Rule3 and fixed `+++`
coupling. This supplies a prepared clock–signal–record–echo component, not
physical light, proper time, gravitational slowing or an Einstein metric.

The initial source is `(a,b,r)=(0,1,2)`. Channel 0 along the following D sites
starts at `(0,0,4)`; every other triple is `(0,0,2)`. There is no runtime source,
mirror, gate, reset or observer feedback. The exact full-board solution for
even D is in [PROOF.md](PROOF.md), including every zero-counter halo remainder.

For D=20 the source port emits C1 at transition 1, the endpoint sees C1 at 20
and reflects with C2 at 22, the source port sees C2 at 41, and the passive source
record changes at state 42. Another outward C1 follows at 43. The entire board
returns at 84; one full period contains two round trips. These are simulator
indices, not an operational physical clock calibration.

The source **counter pair** cycles every four updates, but its full triple also
stores echo parity. The source core has no native C events. The target readout
`a*a+b*b` stays 4 at states 22..61: 40 sampled states, 39 unchanged transitions.
The source parity stays 1 at states 42..83: 42 states, 41 unchanged transitions.
Both records later clear and repeat. The target remains driven by the guide.
Neither is permanent isolated memory, an accumulated tick count or collapse.

## Reuse the preparations

```python
from research.clock_link_v1 import assemble_clock_link

prepared = assemble_clock_link(distance=20, side=389)
states = list(prepared.engine.evolve(prepared.initial, 168))
assert len(states) == 169
assert states[84] == prepared.initial
```

`SourceClock`, `RestingCorridor` and `EchoBoundary` return ordinary immutable
Patches. `clock_link_parts` returns placements suitable for the existing strict
`finalize(BoardSpec(side), placements)`. Use distinct name prefixes when joining
assemblies. Origin and proper orientation transform both coordinates and channel
labels. The composer detects conflicting tensors, backgrounds and assignments;
successful construction alone does not prove later interaction behavior.

The factory requires even D>=14 and side>=D+3. For `terminated=False`, specify
a sufficiently long resting guide using `control_extent`, and side>=extent+3.
The default extent lies beyond the two-period audit horizon. All coordinates
must fit the board; no implicit wrapping is requested. `source_present=False`
gives stationary hardware. `delay=1` shifts the complete canonical trajectory
by one update; its raw state-zero parity is startup, not a returned echo.

## Fresh evidence and reproduction

Earlier local working files were removed by workspace maintenance. This package
reconstructs the preparation and proof and generates **new evidence** against
the unchanged core at base commit `37fe77be8f489ba722ac687ff544b3956352e62f`.
It does not claim that the earlier local receipts or original recordings have
been recovered. [results.json](results.json) identifies current source hashes,
complete initial states, all retained full-state hashes and every fixed readout.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m research.clock_link_v1.audit --output runs/clock-link-recheck.json
PYTHONDONTWRITEBYTECODE=1 python -m research.clock_link_v1.present --output runs/clock-link-presenter
```

Use a fresh output name. The audit fixes D=14,20,28, L=389,431, startup delays
0/1 and all source/endpoint masks: 48 configured cases. Active finite-guide
cases cover two full periods plus startup; long-guide controls use the same
duration without an assumed period. All have full native and independent
forward/inverse checks. Null cases
contain one actual transition and a fixed-point argument, not padded frames.
The delay labels coincide when the source is absent; the 48 configurations are
not asserted to be 48 distinct initial states.
The independent implementation derives routing from separate exact matrices and
imports no production engine, state, coupling, Rule3 or event classifier.
Every complete canonical state is also compared with the closed formula.
The joint run checks two separated, differently oriented links against their
separate evolutions, establishing coexistence rather than interaction.

The fresh main audit contains **4,244 complete states, 4,196 transitions,
4,064 recomputed native events, 2,092 complete closed-form comparisons and
24 paired-size comparisons**. The separate joint assembly adds 234 complete
states and 233 transitions. Every transition is checked forward and backward;
each complete run is also rewound to its initial state. These are new counts,
not numbers copied from the unavailable earlier local study.

Open `runs/clock-link-presenter/The_Presenter.html` in a browser that runs local
JavaScript. Five choices contain the canonical, delayed, absent-source,
long-guide and two-link recordings. Drag to rotate; use **View options → Focus
retained state** to enlarge the guide and **Look inside** for all 48 channels.
The second link uses source `(48,16,48)`, channel 4. The whole board is 3D, while
each prepared guide is a line. The HTML is generated by the existing generic
Presenter; attachment previews may not execute it. Packaging validation does
not certify Safari/iPad interaction or actual browser rendering.

## Next physical test

This link removes the need to insert an outgoing or return signal externally.
It does not establish light-triggered ticking for all clocks. A second calibrated
clock and an unambiguous internal accumulated-event record remain necessary for
relational rate measurements. Changing D changes the apparatus, not gravity.
The separate two-preparation 4-to-5 clock coincidence in
[einstein_clock_bricks_v1](../einstein_clock_bricks_v1/README.md) is a distinct
bounded result. Neither result supplies universal clock response or a metric.
