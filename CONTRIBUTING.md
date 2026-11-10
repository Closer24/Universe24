# Contributing to ONE

Read [AGENTS.md](AGENTS.md) and [the model](docs/MODEL.md). Submit a focused change on a branch, with the exact tensor configuration, seed, observation definition and validation commands needed to reproduce the result.

Preserve complete integer state traces for refactors. For mathematical changes, explain which assumptions changed and include an inverse proof or a precise limitation. A new tensor is a change to the model even if the scalar Rule3 function is unchanged.

Run the commands in [README](README.md#verification). Use `runs/` for generated output. Keep current claims separate from historical notes and optional experiments; a passing test of an expected failure is not evidence for the rejected physical claim.
