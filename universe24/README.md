# ONE implementation and research records

The current entry point, installation, defaults and validation commands are in the [repository README](../README.md). The current mathematical specification is [docs/MODEL.md](../docs/MODEL.md). The [system map](../docs/SYSTEM_MAP.md) gives the module inventory, actual interconnections, proof assumptions and physical limitations.

All runtime code in this directory belongs to ONE. `ref` / L0 denotes the 48-gear algebraic block inside ONE; it does not select another engine. `core/engine.py` is the sole forward engine.

`NOTES*`, manifests, draft reports, `results/`, patches and `full_picture_2026-11-10/` preserve research provenance. They include superseded hypotheses, rejected parameter choices, old command paths and numerical negative results. Read their stated configuration and horizon; do not treat them as the current default specification. The serialized identifier `metric_variant_v1/tensor/1` is retained for evidence compatibility, not as a separate runtime.
