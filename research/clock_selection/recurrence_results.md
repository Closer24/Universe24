# Returning carriers, exact periods and a bounded long follow-up

The verified result is finite internal recirculation of an initially prepared
carrier on a periodic guide. The studies do not establish an apparatus that
tries alternatives until it invents a successful route. The continuing L50/L54
examples are exact closed whole-board orbits. The unresolved L48/L52 examples
were extended through32 return opportunities and did not recover the declared
joint carrier after its loss.

## Short study and exact closure

The [frozen short protocol](recurrence_protocol.json) specifies20 complete
preparations: cube sides48,50,52,54, four matched packet/clock counter masks per
size, and one pristine whole-guide control per size. All remainders remain in
the counter-mask controls. The first source is prepared once; nothing is
reinjected. Each horizon is `2*L+40` updates.

The carrier predicate compares all48 channels, both counters and remainders in
the complete periodic6×3×3 template. A returned carrier must match at every
intermediate state from the previous outlet to its new incoming window. The
clock hold compares all336 triples of its seven-node region and verifies
individual external terms, not only their sum. All raw C events and complete
states are retained.

The [independent audit](evidence/independent_audit/recurrence_v1.json) confirms
20 records,2860 states and2840 transitions, including every full-state rewind.
All four pristine translations pass. Six scheduled returns are genuine under
the frozen local transport predicate: one each for L48/L52 and two each for
L50/L54. Later output is absent for the former and present for the latter.
All six eligible phase predictions agree. Zero stronger clock-conditioned
gates pass, because the packet-only comparator does not supply a valid incoming
carrier. That is an invalid comparator, not proof of rejection by a clock.

A [postanalysis of existing recordings](evidence/recurrence_period_diagnostic/result.json)
found complete initial-state closure for the L50/L54 joint cases. The
[independent exact-state certificate](evidence/recurrence_period_diagnostic/independent_check.json)
checks every input hash and every recorded shifted overlap, without using the
producer's period function. It confirms `S50=S0` and `S54=S0` respectively.
For a fixed deterministic map F, `F^p(S0)=S0` implies
`S(t+p)=F^t(F^p(S0))=F^t(S0)=S(t)` for all later t. The retained whole-board
state therefore repeats, not just one visible clock. More laps cannot produce
a previously absent full-state decision in those same preparations.

## Registered long study

The [separate long protocol](recurrence_long_protocol.json), SHA-256
`735da2e80a97e778a6629f9d3f0bf07bbca40b9a428fc3d660790a69f44621cd`,
extends only the unresolved L48/L52 families. It retains all four original
counter masks at each size, for8 runs, through `32*L+40` updates. There is one
initial encounter plus32 fixed return opportunities. No output window changes.

The longer study deliberately strengthens initial-carrier identity: the exact
template must hold at every state from the initial outlet at24 through the
current arrival. One-lap transport is reported separately. Thus a pattern that
disappears and later reappears cannot silently become the same initial carrier.
A separate prospective diagnostic searches every native frame and every X
origin on the declared guide for the same complete +X template. It does not
search arbitrary orientations, hidden channels or other object definitions.
Absence from that scan is absence of this template, not absence of all signals
or all microscopic information.

| Verified observation | L48 | L52 |
| --- | --- | --- |
| Complete updates |1576|1704|
| Initial outlet carrier |Present|Present|
| Later scheduled outputs,32 opportunities |All absent|All absent|
| Continuous returns of the original carrier |First return only|First return only|
| Exact +X template reappears on the declared guide after loss |No|No|
| Joint whole-board repeated state within the horizon |None found|None found|
| Packet-only counter-ablation full-board period |1200|1404|
| Null / clock-only full-board period |1 /4|1 /4|
| Strict clock-conditioned gate |Not established|Not established|

The [independent long audit](evidence/independent_audit/recurrence_long_v1.json)
replays all8 records,13,128 complete states and13,120 transitions. It independently
checks every scheduled cycle, initial continuity, all-frame/all-X scan,
whole-board periods, complete native bundles and inverse. The packet-only long
periods belong to the declared remainder-defect controls; they do not rescue
the invalid comparator for an approval claim. No full repeat in a finite joint
trace excludes only a period or repeat within that trace, not all future
recurrence.

The corrected capture used82.19 CPU seconds and40,992,620 retained bytes, within
the registered300 CPU seconds/600 wall seconds/128 MiB ceilings. All35 archived
source files match the executed live sources. An initial infrastructure attempt
stopped before any transition because a short-study frame limit was inherited.
Its zero-record failure and exact source are retained under
`evidence/recurrence_long_v1/`. The
[recording correction receipt](evidence/recurrence_long_recording_correction.json)
shows the single change to set `max_frames=registered_steps+1`, with an initial-
state equality regression. The corrected scientific records are under
`evidence/recurrence_long_v1_corrected/`; the protocol and observations did not
change.

## Reproduce and inspect

From the repository root, use new output directories:

```sh
python -m research.clock_selection.recurrence --output runs/recurrence-new
python -m research.clock_selection.recurrence_long --output runs/recurrence-long-new
python -m research.clock_selection.run present \
  --input runs/recurrence-long-new/native/long-ring-L48-11.json \
  --output runs/recurrence-long-presenter
```

The [short Presenter package](evidence/presenter_recurrence_v1/index.html)
contains eight complete controls at L50/L54. The
[long package](evidence/presenter_recurrence_long/index.html) contains all eight
complete long controls across bounded pages; no frame is dropped or split out
of an experiment. It displays the recorded clocks, counters, remainders and raw
events without evolving or selecting the board.

The next useful mechanism needs a new, explicitly prepared way to retain or
regenerate a functional trial carrier while internal state changes. Extending
the already closed or failed families alone supplies no current evidence of
preferred complexity, unique-route approval or spontaneous construction.
