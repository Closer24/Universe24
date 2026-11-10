"""Generic runner for variant init files; mirrors ``python -m universe24``.

The event log is the official passive JSONL (``universe24.observation.clicks``),
so a click decoder reads it unchanged. The printed summary always carries the
coupling label and fingerprint; keep it (``--summary``) beside every log.
"""
import argparse
from contextlib import ExitStack
from dataclasses import asdict
import json
from pathlib import Path
import sys

from universe24.observation import balance_residuals, clicks, expected_account_change, signed_account

from .config import checkpoint_data, load, read_checkpoint

EXECUTOR = "research.coupling_variants_v1.VariantEngine (Rule3 imported from universe24.core.rule3)"


def summary(engine, initial, state, completed, event_count, audited) -> dict:
    coupling = engine.coupling
    return {"model": "variant" if coupling.is_variant else "reference-equivalent",
            "coupling_label": coupling.label, "coupling_name": coupling.name,
            "variant_fingerprint": coupling.fingerprint,
            "reference_signs": None if coupling.is_variant else list(coupling.reference_signs),
            "reference_fingerprint": coupling.reference_fingerprint,
            "executor": EXECUTOR, "side": state.cube.side, "nodes": state.cube.node_count,
            "channels_per_node": 48, "completed_steps": completed,
            "stored_deviations": len(state.cells),
            "initial_signed_account": signed_account(initial),
            "final_signed_account": signed_account(state),
            "logged_arithmetic_events": event_count, "audited": audited}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m research.coupling_variants_v1",
                                     description="Explicitly separate candidate-coupling executor")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--config", type=Path, help="Variant init JSON (universe24-variant-init-v1)")
    source.add_argument("--resume", type=Path, help="Variant full-state checkpoint")
    parser.add_argument("--steps", type=int)
    parser.add_argument("--events", type=Path, help="Passive arithmetic event log, official JSONL")
    parser.add_argument("--output", type=Path, help="Final sparse full-state variant checkpoint")
    parser.add_argument("--summary", type=Path, help="Also write the printed summary to this file")
    parser.add_argument("--audit", action="store_true", help="Inverse and signed-balance audits")
    args = parser.parse_args(argv)
    try:
        if args.config:
            experiment = load(args.config)
            engine, initial, count = experiment.engine, experiment.initial, 0
            steps = experiment.steps if args.steps is None else args.steps
        else:
            if args.steps is None:
                parser.error("--steps is required with --resume")
            engine, initial, count = read_checkpoint(args.resume)
            steps = args.steps
        if type(steps) is not int or steps < 0:
            parser.error("--steps must be nonnegative")
        targets = [p.resolve() for p in (args.events, args.output, args.summary) if p is not None]
        inputs = [p.resolve() for p in (args.config, args.resume) if p is not None]
        if len(set(targets)) != len(targets) or any(p in inputs for p in targets):
            parser.error("Output paths must differ and not overwrite inputs")
        state = initial
        event_count = 0
        with ExitStack() as stack:
            log = stack.enter_context(args.events.open("x", encoding="utf-8")) if args.events else None
            record = stack.enter_context(args.summary.open("x", encoding="utf-8")) if args.summary else None
            for index in range(1, steps + 1):
                next_state = engine.advance(state)
                if args.audit:
                    if engine.rewind(next_state) != state:
                        raise ArithmeticError("Inverse failed")
                    if balance_residuals(state, next_state, engine):
                        raise ArithmeticError("Local balance failed")
                    if signed_account(next_state) - signed_account(state) != expected_account_change(state, engine):
                        raise ArithmeticError("Global signed-account identity failed")
                if log is not None:
                    for event in clicks(state, next_state, count + index):
                        log.write(json.dumps(asdict(event), separators=(",", ":")) + "\n")
                        event_count += 1
                state = next_state
            if args.output:
                with args.output.open("x", encoding="utf-8") as handle:
                    json.dump(checkpoint_data(state, engine, count + steps), handle, indent=1)
                    handle.write("\n")
            text = json.dumps(summary(engine, initial, state, count + steps, event_count, args.audit), indent=2)
            if record is not None:
                record.write(text + "\n")
        print(text)
        return 0
    except (OSError, ValueError, TypeError, ArithmeticError) as error:
        print(f"coupling_variants_v1: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
