# Contributing to Universe24

Read [AGENTS.md](AGENTS.md) and [the system contract](docs/ONE_SYSTEM.md). Coordinate module interfaces and channel ownership on [issue #40](https://github.com/Closer24/Universe24/issues/40). Submit a focused change on a branch, with the exact tensor configuration, complete seed, decoder protocol and validation commands needed to reproduce the result.

Every active scalar update uses `divmod(2*u+r,6)`. Do not add a divisor parameter, hide one in tensor metadata, or introduce a per-channel numerator/denominator. Effective coefficient families need a declared encoding and proof.

Preserve complete integer state traces for refactors. For mathematical changes, explain which assumptions changed and include an inverse proof or a precise limitation. A new tensor is a change to the model even if the scalar Rule3 function is unchanged.

Run the commands in [README](README.md#verification-and-research). Use `runs/` for generated output. Keep proposals and independent references under the research/validation boundary, with no alternate supported runtime selectors. The bundle must reject allocations above 48 total channels. A passing test of an expected failure is not evidence for the rejected physical claim.
