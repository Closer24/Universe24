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
            "native_light_stream48": "48-channel 2O-covariant light tensor; exact axis-aligned transverse plane-wave sector on flat spacetime",
            "light_memory48": "Retained, reversible light-to-memory exchange with a conserved excitation account; photon calibration remains open",
            "node_face_views": "Six passive internal face views of existing state; shared adjacency identities add no link memory or metric",
            "click_only_observer": "Reads canonical clicks; memory reconstruction requires explicit zero-memory, nonnegative-sector calibration",
        },
        "restricted_research_results": {
            "native_massless_homogeneous_sector": "Exact sourced Einstein sampling on a declared complete-history domain",
            "native_anisotropic_massless_sector": "Exact homogeneous Bianchi I source and source-clock invariant; moving probes remain passive",
            "massive_homogeneous_spinor_sector": "Exact decoded constraint and finite-time convergence; costly integers and finite-step dust drift",
            "joint_bursts_and_complexity_growth": "Not established by the separate recurrent-activity controls",
        },
        "blockers": [
            "No validated <=48-channel coupled geometry, matter and apparatus encoding",
            "General spatial Einstein constraints and convergent refinement unproved; restricted homogeneous sectors are separate research results",
            "Shared-metric operational clocks and detector physics unproved",
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
    light = sub.add_parser("prepare-light", help="Prepare the native 48-channel 2O light component")
    light.add_argument("--out", type=Path, required=True)
    light.add_argument("--size", type=int, default=13)
    light.add_argument("--axis", choices=('x', 'y', 'z'), default='x')
    light.add_argument("--sign", type=int, choices=(-1, 1), default=1)
    light.add_argument("--polarization", choices=('x', 'y', 'z'))
    light.add_argument("--center", type=int, default=4)
    light.add_argument("--order", type=int, default=4)
    light.add_argument("--amplitude", type=int, default=1)
    detector = sub.add_parser("prepare-detector", help="Prepare retained light-to-memory exchange in 48 channels")
    detector.add_argument("--out", type=Path, required=True)
    detector.add_argument("--size", type=int, default=13)
    detector.add_argument("--root", type=int, default=0, help="2O orientation label, 0..47")
    detector.add_argument("--light-position", type=int, default=2)
    detector.add_argument("--arm-position", type=int, default=7)
    detector.add_argument("--amplitude", type=int, default=1)
    detector.add_argument("--unarmed", action="store_true", help="Prepare the same tensor without an arming pulse")
    detect = sub.add_parser("detect", help="Replay a detector run and read retained capture/release records")
    detect.add_argument("--run", type=Path, required=True)
    detect.add_argument("--out", type=Path, required=True, help="New observation JSON file")
    observe = sub.add_parser("observe-clicks", help="Observe a click file without opening hidden states or a bundle")
    observe.add_argument("--clicks", type=Path, required=True)
    observe.add_argument("--out", type=Path, help="Optional new observation JSON file")
    observe.add_argument("--memory-channel", type=int, help="Explicit calibrated detector-memory channel")
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
        elif args.command == "prepare-detector":
            from universe24.detection import make_detector_bundle
            from universe24.system.bundle import save_bundle
            bundle = make_detector_bundle(L=args.size, root=args.root, light_position=args.light_position,
                                          arm_position=args.arm_position, amplitude=args.amplitude,
                                          armed=not args.unarmed)
            save_bundle(bundle, args.out)
            result = {"bundle_id": bundle.bundle_id, "channels": bundle.tensor.G,
                      "path": str(args.out), "model_contract": bundle.model_contract,
                      "physics_acceptance": "not_tested"}
        elif args.command == "detect":
            from universe24.detection import observe_detector_run
            report = observe_detector_run(args.run)
            with args.out.open('x', encoding='utf-8') as output:
                json.dump(report, output, indent=2)
                output.write('\n')
            result = {key: value for key, value in report.items() if key not in ('events', 'accounts')}
            result['observation_file'] = str(args.out)
        elif args.command == "observe-clicks":
            from universe24.observer import inspect_click_file, reconstruct_memory_from_clicks
            calibration = (args.memory_channel, args.nodes, args.steps)
            if any(value is not None for value in calibration) and any(value is None for value in calibration):
                raise ValueError('memory calibration requires --memory-channel, --nodes and --steps together')
            result = inspect_click_file(args.clicks)
            if args.memory_channel is not None:
                result['calibrated_memory'] = reconstruct_memory_from_clicks(
                    args.clicks, memory_channel=args.memory_channel,
                    node_count=args.nodes, steps=args.steps)
            if args.out is not None:
                with args.out.open('x', encoding='utf-8') as output:
                    json.dump(result, output, indent=2)
                    output.write('\n')
        elif args.command == "prepare-light":
            from universe24.light import make_light_bundle
            from universe24.system.bundle import save_bundle
            bundle = make_light_bundle(L=args.size, axis='xyz'.index(args.axis), sign=args.sign,
                                       polarization=None if args.polarization is None else 'xyz'.index(args.polarization),
                                       center=args.center, order=args.order, amplitude=args.amplitude)
            save_bundle(bundle, args.out)
            result = {"bundle_id": bundle.bundle_id, "channels": bundle.tensor.G,
                      "path": str(args.out), "model_contract": bundle.model_contract,
                      "physics_acceptance": "not_tested"}
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
