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
        "retained_entries_per_channel": ["a", "b", "r"],
        "arithmetic": "exact integers; divmod(2*u+r, 6)",
        "locality": "target and at most one physical face edge per monomial",
        "accepted_physical_model": None,
        "full_physics_acceptance": "blocked",
        "restricted_research_results": {
            "native_massless_homogeneous_sector": "Exact sourced Einstein sampling on a declared complete-history domain",
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
