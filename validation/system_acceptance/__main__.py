"""Run a fixed acceptance sequence; never select a production universe."""
import argparse
import json
from pathlib import Path

from .run import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = run(args.out)
    print(json.dumps({'report': str(args.out / 'acceptance.json'),
                      'software_execution': report['software_execution'],
                      'general_physical_acceptance': report['general_physical_acceptance'],
                      'same_law_recurrent_bursts_and_growth': report['same_law_recurrent_bursts_and_growth']},
                     indent=2))


if __name__ == '__main__':
    main()
