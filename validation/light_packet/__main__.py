"""Prepare light inputs or audit saved runs; all advancement uses the main runtime."""
import argparse
import json
from pathlib import Path

from .model import export_inputs, make_bundle
from .audit import collect, inspect


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prepare = sub.add_parser('prepare-inputs')
    prepare.add_argument('--out', type=Path, required=True)
    prepare.add_argument('--size', type=int, default=41)
    prepare.add_argument('--steps', type=int, default=24)
    prepare.add_argument('--geometry', choices=('flat', 'fast', 'step'), default='flat')
    prepare.add_argument('--order', type=int, default=12)
    prepare.add_argument('--center', type=int, default=10)
    prepare.add_argument('--interface', type=int, default=14)
    audit = sub.add_parser('audit')
    audit.add_argument('--out', type=Path, required=True)
    saved = sub.add_parser('inspect')
    saved.add_argument('--run', type=Path, required=True)
    saved.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == 'prepare-inputs':
        bundle = make_bundle(L=args.size, steps=args.steps, geometry=args.geometry,
                             order=args.order, center=args.center, interface=args.interface)
        export_inputs(bundle, args.out)
        result = {'raw_inputs': str(args.out), 'tensor_hash': bundle.tensor.fingerprint,
                  'channels': bundle.tensor.G, 'general_physical_acceptance': 'blocked'}
    elif args.command == 'audit':
        result = collect(args.out)
        result = {'report': str(args.out / 'light_packet.json'), 'physical_gates': result['physical_gates']}
    else:
        if args.out.exists():
            parser.error('refusing to overwrite existing evidence')
        result = inspect(args.run)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
        result = {'report': str(args.out), 'click_count': result['click_count'],
                  'physical_gates': result['physical_gates']}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
