# Contributing to Universe24

This repository is a **research reference engine**. Contributions should increase reproducibility, mathematical clarity and test coverage without silently changing the model.

## Before changing code

Read [AGENTS.md](AGENTS.md), [the mathematical model](docs/MODEL.md), [architecture](docs/ARCHITECTURE.md), and [research status](docs/RESEARCH_STATUS.md).

## Non-negotiable default-model constraints

- Exactly **one board** per site; exactly **48 channels** per board.
- A periodic cube of side `L >= 3`; every channel has exactly **six spatial inputs**, no on-site coupling.
- The 48 labels and fixed coupling matrices are derived from `2O`.
- All state-changing dynamics use `(ell,r')=divmod(2*u+r,6), a'=b, b'=ell-a`, with no per-experiment law.
- The complete state, including `r`, is retained and invertible.
- Seeds and three body-axis signs are fixed before execution; no runtime rewriting or live injection.
- Observations, click categories, diagnostics and logs are **read-only**.

A scientifically interesting but incompatible rule is welcome only as an **explicitly separate model** with its own stated assumptions; it must not replace this reference engine without a declared model revision.

## Contribution checklist

1. State which mathematical or implementation claim is being tested.
2. Provide exact input configuration(s), baseline and controls, including failure cases.
3. Run `python -m unittest discover -s tests -v`.
4. Test exact one-step and multi-step inverse, all six spatial ports, signed coupling reciprocity, arithmetic with negative/large integers, and observer independence where applicable.
5. Explain whether a change affects the **law**, **static coupling**, **seed**, **external observation**, or **only documentation**.
6. Update the appropriate docs and report known scientific limitations.

## What belongs where?

- New seeds or experimental comparisons: `examples/` and documentation.
- External statistics, plots and additional click readouts: `observation/`, strictly read-only.
- Generic mathematical proof/audit tests: `tests/`.
- Node updates: only `core/rule3.py` for the **reference** law; any proposed new law must be a separately named variant.

## Reporting evidence

Do not describe a local oscillation as an atom, a pulse as a photon, an arithmetic event as an observed quantum measurement, or an exact balance identity as physical energy conservation without the relevant derivations and quantitative tests.

Document numerical seed, `L`, signs, steps, code version and a full-state checkpoint if appropriate. Event logs alone are insufficient to reconstruct full microscopic states.

## Reliability gate

Run the clean-source [reliability bundle](docs/RELIABILITY.md) before proposing
changes. It includes all unittest regressions and independently reconstructed
algebra/routing/evolution. Preserve protocol and source identities, explicit
negative outcomes, and first-difference artifacts. See the
[Hebrew instructions](docs/RELIABILITY.he.md) for the same acceptance contract.
Research reference code must not import production algebra or coupling tables.
Do not update expected output to hide a failed comparison. Any necessary change
to the core or click semantics requires a separate explicit review. All code
changes belong on a branch and in a PR; merging requires the initiator's approval.
