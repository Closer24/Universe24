# Retained apparatus and passive clock-link observations

The apparatus is retained on the board. The reader is an external passive
description of its canonical arithmetic records. These are separate roles:
an observer file never decides an update, supplies randomness or repairs a
hidden state. All four added channels retain complete `(a,b,r)` and use the
existing fixed-six Engine.

For an integer phase-relation intensity `I`, the proposed apparatus input is
`u=3I`. Hence `ell=I`, `r_next=r`, `a_next=b`, `b_next=I-a`. The channel remembers
its history reversibly; its event, when one exists, has quotient `I` and class
C0. Selecting only C2 would discard every event of this apparatus.

## Static measurement protocol

`validation/clock_links/observer.py` accepts only canonical click records, a
static protocol and the run identity. It cannot receive a State, tensor
evaluator, RNG, expected result or callback. Its protocol declares:

- the tensor fingerprint, channel count, lattice size and complete run length;
- named detector ports, each a node and disjoint list of retained channels;
- consecutive windows that cover the entire declared run exactly.

The default protocol gives every computational microtick a window. These are
**arithmetic observation windows**, not physical emission trials or proper-time
ticks. Every detector/window appears in the report, including absence and
multiple events. All classes and quotient signs remain included. The reader
reports event count, counts by class/channel and signed/absolute sums of
*recorded* quotients separately.

Unknown selection settings, overlapping ports, incomplete windows, wrong
run/tensor identities, malformed indices, inconsistent coordinates, invalid
event identities, duplicate events and out-of-order records are rejected.
Incremental reading and offline reading return identical reports. Neither
operation retains mutable caller aliases.

## Information-loss counterexample

`ell=I` does **not** imply that the click stream reconstructs intensity. The
official stream requires a nonzero quotient **and a changed triple**. For
constant even intensity, prepare `a=b=I/2` and any fixed legal carry. Then the
triple remains unchanged and no click is emitted despite `I>0`.

The tests explicitly compare two complete, distinct retained states:

| Preparation | Local intensities | Apparatus state | Complete click stream |
| --- | --- | --- | --- |
| Zero carrier | 0, 0 | `a=b=0` | empty |
| Constant carriers 2 and 4 | 4, 16 | `a=b=2` and `a=b=8` | empty |

Both streams stay empty for all three checked updates, while both full states
remain distinct. Thus a reader must not replace every absent record with a
claim of zero hidden intensity. This ambiguity is a concrete many-to-one
observation boundary, not a proof of quantum collapse.

Likewise, fresh zeroed detector memories driven by intensities 9 and 1 each
produce one event on the first update. Quotients have ratio 9:1; event counts
have ratio 1:1. The observer does not convert quotient weights into a fabricated
random one-outcome trial. A separate detector mechanism would be required.

## Integrity and validation

Well-formed click records alone cannot prove that no event was lost. The reader
always reports this limitation and hashes its full input stream. The audit
harness `observer_audit.py` first calls the existing complete-run `verify_run`,
then creates its fixed protocol before opening the click file. Only the
records and static metadata enter the observer. Afterward it checks incremental
parity and verifies that the trace, clicks and run report were unchanged.

Seven focused tests cover ratio/count distinction, the stationary nonzero
counterexample, all three classes and multiple events, online/offline parity,
passivity/alias isolation, protocol/record corruption, and the unavoidable
missing-record limitation. The counterexample and parser tests use deliberately
small Engine fixtures; they are not promoted as a second physical runtime.

The integrated audit ran on the actual 48-channel bundle from the phase-link
team: 27 nodes and three complete updates. Full replay passed. The reader
counted **314 apparatus records across 81 node/window bins**; all 81 bins had
multiple events, with no single-event or empty bins in this preparation.
Incremental/offline parity passed and all saved-run file hashes were unchanged.
These bins group four apparatus ports at each node. Their multiplicity is not
by itself a quantum exclusivity test, because no physical emission/outcome
assignment has been established for those four ports. The separate Born audit
uses an explicitly declared two-detector trial for its count/weight comparison.
The protocol, full records-only report and source-hashed audit are in
`runs/clock_links/observer/`; fresh evidence is not substituted for historical
Born/complexity controls.

```bash
python -m unittest universe24.tests.test_clock_link_observer -v
python -m validation.clock_links.observer_audit \
  --run runs/clock_links/phase/run \
  --out runs/clock_links/observer
```

The proposed observer contract passes these software checks. Proper-clock
calibration, apparatus stress/backreaction, physical single-outcome detection,
Born probabilities and Bell correlations remain unestablished by this reader.
