# External clicks: arithmetic event classification, not a measurement law

## Conceptual boundary

**All clicks are reported outside the evolving automaton.** There is no internal click list, click trigger, measurement gate, or observer-controlled reset. A user-facing record is a readout of a transition that Rule3 already produced. The observation layer cannot change channel state.

The term **arithmetic event** is deliberately used for currently implemented readouts. Claiming a physical detector click requires a derived detector mechanism and a stable, operational measurement definition.

## Three remainder-transition classes

For one channel, Rule3 is:

```text
ell, r' = divmod(2u + r, 6)
a' = b
b' = ell - a
```

Write `r=2 theta + epsilon`, with `theta in {0,1,2}` and `epsilon in {0,1}`. Since `2u` is even, parity `epsilon` is preserved. Thus

```text
theta' = (theta + u) mod 3
kind   = (theta' - theta) mod 3 = u mod 3
```

The three labels are:
- `C0`: `kind=0`, no shift in remainder's three-position sector.
- `C1`: `kind=1`, a shift by one sector position.
- `C2`: `kind=2`, a shift by two sector positions.

A *candidate arithmetic event* is emitted only if (1) the quotient is nonzero, and (2) the complete channel triple changes. Algebraically `ell=b'+a`. The event is then assigned exactly one of the three labels.

In this code, `kind` is recorded as the integer 0, 1 or 2.

## Why these are not physical types yet

The same `C2` transition can arise during an ordinary oscillator and during a prepared competitor interaction; it does **not** intrinsically mean "the winning choice". A `C1` transition can also be part of a winning response. Remainder-transition classes do not determine detector readiness, robust event storage, statistics, or energy transfer.

An atomic-like local event does not automatically perform a choice among paths. A **detector-like** pattern would have to perform a genuine interaction which makes outcomes exclusive under the fixed Rule3 dynamics. Only after that could an external observer classify its output.

## How observation is implemented

`observation/clicks.py` compares the complete states before and after one already-computed step. It derives the quotient and remainder class, then yields immutable `Click` readouts. The command-line runner optionally saves such readouts to JSONL through `--events`.

A JSONL record contains: `step`, `address` (three spatial coordinates plus a channel index), `kind`, `quotient`, `before` and `after`. For example, an event may look like:

```json
{"step":1,"address":[1,2,3,0],"kind":2,"quotient":1,"before":[0,0,2],"after":[0,1,0]}
```

This is a **format illustration**, not a claim that the above event arises from a named example seed.

Observation is incomplete by design: channels with `ell=0` may still change their remainder or previous counter, and omitted events retain important information. **Never** treat `events.jsonl` as a complete reversible state representation.

## Cancellation and history

A subsequent wave can prevent a prepared candidate from reaching a later confirmation condition, or reversibly change an existing transient representation. No fixed-law reversible evolution can literally delete the distinction between two different full past states while preserving exact invertibility. Cancellation claims must specify whether they concern **future confirmation**, **temporary internal representation**, or **already emitted external events**.

## Needed for a real detector hypothesis

An explicit prepared detector structure, local readiness, candidate/confirmation separation, an internal dynamics that protects an outcome from competing signals, quantitative mapping to observed statistics and correct conservation accounting. All of this must emerge from Rule3 and the fixed coupling; the observation code may only report what happened.
