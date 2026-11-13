"""The single supported bundle-driven Universe24 command line."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def status():
    """Release claims, not a result inferred from a successful mechanical run."""
    return {
        "architecture": "one bundle -> one fixed tensor Engine -> one passive decoder",
        "maximum_channels_per_node": 48,
        "required_channels_per_node": 48,
        "preparation_padding": "none; supply all 48 channels explicitly",
        "required_symmetry": "2O-left-regular-cube/1; exact polynomial covariance for every supported model",
        "undeclared_model_role": "research; same mandatory symmetry checks as every other role",
        "retained_entries_per_channel": ["a", "b", "r"],
        "arithmetic": "exact integers; divmod(2*u+r, 6)",
        "locality": "target and at most one physical face edge per monomial",
        "accepted_physical_model": None,
        "full_physics_acceptance": "blocked",
        "installed_components": {
            "clock_collision48": "one fixed cubic signal/clock coupling; positive Boolean sector with retained coordinate counter",
            "node_face_views": "six internal directional views; no extra link state",
            "click_only_observer": "canonical clicks with optional explicit positive-history calibration",
        },
        "verified_sector": "one selected orientation at a time; arbitrary spatial Boolean profiles",
        "blockers": [
            "Simultaneous independent six-direction populations are not established",
            "State-dependent residence time does not establish a Lorentzian metric or Einstein equations",
            "Massive bodies, dark matter, gravitational waves and cosmological bang dynamics remain unproved",
            "The coordinate counter is not a material proper clock; structural complexity need not grow",
            "No Born/Bell mechanism or physical interpretation of a third click is established",
        ],
        "coordination": "https://github.com/Closer24/Universe24/issues/40",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status", help="Show the actual architecture and open physical gates")
    prepare = sub.add_parser("prepare", help="Validate complete input JSON files and seal one bundle")
    for name in ("tensor", "seed", "channels", "protocol", "model"):
        prepare.add_argument("--" + name, type=Path, required=True)
    prepare.add_argument("--out", type=Path, required=True)
    model = sub.add_parser("prepare-model", help="Prepare the one fixed signal/clock coupling")
    model.add_argument("--out", type=Path, required=True)
    model.add_argument("--size", type=int, default=7)
    model.add_argument("--root", type=int, default=0, help="2O orientation label, 0..47")
    model.add_argument("--signal-sites", nargs='*', type=int, default=[0])
    model.add_argument("--memory-sites", nargs='*', type=int, default=[])
    model.add_argument("--clock-sites", nargs='*', type=int, default=[2])
    model.add_argument("--counter-start", type=int, default=2)
    observe = sub.add_parser("observe-clicks", help="Observe a click file without opening hidden states or a bundle")
    observe.add_argument("--clicks", type=Path, required=True)
    observe.add_argument("--out", type=Path, help="Optional new observation JSON file")
    observe.add_argument("--channel", type=int, help="Explicit calibrated retained channel")
    observe.add_argument("--initial-a", type=int, help="Public uniform previous channel value")
    observe.add_argument("--initial-b", type=int, help="Public uniform current channel value")
    observe.add_argument("--nodes", type=int, help="Public node-address count, not physical volume")
    observe.add_argument("--steps", type=int, help="Declared complete observation horizon, not proper time")
    run = sub.add_parser("run", help="Run the complete saved seed through its immutable tensor")
    run.add_argument("--bundle", type=Path, required=True)
    run.add_argument("--steps", type=int, required=True)
    run.add_argument("--out", type=Path, required=True)
    verify = sub.add_parser("verify", help="Reexecute and rewind a saved run and check its decoded clicks")
    verify.add_argument("--run", type=Path, required=True)
    verify.add_argument("--require-physics", action="store_true",
                        help="Fail unless the independent physical acceptance gates are established")
    args = parser.parse_args(argv)
    try:
        if args.command in (None, "status"):
            result = status()
        elif args.command == "prepare-model":
            from universe24.model import make_model_bundle
            from universe24.system.bundle import save_bundle
            bundle = make_model_bundle(L=args.size, root=args.root,
                signal_sites=args.signal_sites, memory_sites=args.memory_sites,
                clock_sites=args.clock_sites, counter_start=args.counter_start)
            save_bundle(bundle, args.out)
            result = {"bundle_id":bundle.bundle_id, "channels":bundle.tensor.G,
                      "path":str(args.out), "model_contract":bundle.model_contract,
                      "physics_acceptance":"blocked"}
        elif args.command == "observe-clicks":
            from universe24.observer import inspect_click_file, reconstruct_channel_from_clicks
            calibration = (args.channel, args.nodes, args.steps, args.initial_a, args.initial_b)
            if any(value is not None for value in calibration) and any(value is None for value in calibration):
                raise ValueError('calibration requires --channel, --nodes, --steps, --initial-a and --initial-b together')
            result = inspect_click_file(args.clicks)
            if args.channel is not None:
                result['calibrated_channel'] = reconstruct_channel_from_clicks(
                    args.clicks, channel=args.channel, node_count=args.nodes,
                    steps=args.steps, initial_a=args.initial_a, initial_b=args.initial_b)
            if args.out is not None:
                with args.out.open('x', encoding='utf-8') as output:
                    json.dump(result, output, indent=2)
                    output.write('\n')
        elif args.command == "prepare":
            from universe24.system.bundle import (create_bundle, save_bundle, read_json,
                                                  tensor_from_data, state_from_data)
            bundle = create_bundle(
                tensor_from_data(read_json(args.tensor)),
                state_from_data(read_json(args.seed)),
                channels=read_json(args.channels), protocol=read_json(args.protocol),
                model=read_json(args.model))
            save_bundle(bundle, args.out)
            result = {"bundle_id": bundle.bundle_id, "channels": bundle.tensor.G,
                      "path": str(args.out), "physics_acceptance": "not_tested"}
        elif args.command == "run":
            from universe24.system.runtime import run_bundle
            result = run_bundle(args.bundle, args.out, args.steps)
        else:
            from universe24.system.runtime import verify_run
            result = verify_run(args.run)
            if args.require_physics:
                # Restricted research validators do not certify the general joint
                # model. A manifest or successful replay cannot grant this claim.
                result["full_physics_acceptance"] = "blocked"
                print(json.dumps(result, indent=2))
                parser.exit(1, "Einstein/clock/detector acceptance remains blocked; see issue #40.\n")
        print(json.dumps(result, indent=2))
        return result
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
