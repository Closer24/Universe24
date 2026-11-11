# Migration to the one-system interface

Version 0.6 intentionally removes the oversized default run and the runtime
model menu. `python -m universe24` now reports the architecture and open physical
gates. It does not generate an accepted physical universe: such a construction
has not yet been established under the 48-channel contract.

| Previous entry point | Current role/location |
| --- | --- |
| `python -m universe24 --case ...`, `--probe-experiment`, `--causal-wave`, `--no-communication`, `--plan`, `--max-channels` | Removed from the public CLI; no budget override or alternate component selector |
| `universe24.runtime.run` and `replay_trace` | Historical finite-horizon ADM validation in `validation.adm_reference` |
| `universe24.demos.*` | Source-only controls in `validation.demos.*` |
| `universe24.tools.*` | Source-only audits in `validation.tools.*` |
| `experiments.*` and `experiments/` | Independent checks and proposal reproductions in `validation.*` and `validation/` |
| Complete validated tensor/seed input | `universe24.system.bundle.create_bundle`, `save_bundle`, `load_bundle` |
| Supported forward run and reconstruction | `universe24.system.runtime.run_bundle`, `verify_run` |
| Supported click records | `universe24.system.decoder` |

The `validation` tree is available from a source checkout and excluded from the
installed wheel. Historical construction helpers in `layers`, `prepare` and
`observe` remain for equation/negative-control tests; they are not supported
alternate model entry points and do not bypass the bundle's mandatory budget.
They cannot produce a physical acceptance certificate.

All supported input tensors must use the current tensor schema and strict
physical edge support. Seeds contain exactly `L`, `a`, `b`, `r`. Channel records
contain `index`, `name`, `label`, `owner` and `purpose`; the complete sequence must
match every tensor channel. Model metadata requires `id`, `version` and `domain`.
The current protocol is exactly:

```json
{"version":"universe24/arithmetic-click/1"}
```

No threshold, physical calibration or alternate decoder is implemented under
that protocol. Unknown settings fail rather than being silently ignored.
Initial physical constraints remain the responsibility of a proposed
preparation and its independent validation.

Saved runs pin source hashes. Verify with the same source revision; changing
code or tensor/seed/protocol data requires fresh evidence. Hashes establish
content integrity, not authenticity. Historic evidence is preserved unchanged
and cannot be relabeled as a current result. Ordinary canonical tensor hashes
are unchanged by the arbitrary-size integer JSON transport.

Mechanical forward/reverse tests and decoder checks are implemented. Physical
gates C–F remain unestablished; `verify --require-physics` exits unsuccessfully.
See [ONE_SYSTEM.md](ONE_SYSTEM.md) for exact scope and the remaining derivation.
