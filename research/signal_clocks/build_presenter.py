"""Package complete signal-clock records with the unchanged generic Presenter.

This adapter is an observer. It imports native checkpoints, validates full
transitions, and attaches predeclared readouts; it never evolves or edits a run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from research.presenter.build import build, _new_file
from research.presenter.export import bundle, from_trace, write_bundle


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def package(descriptor_path, output_directory):
    """Read an explicit descriptor and create a new standalone presentation.

    Paths in a descriptor are relative to the descriptor file. Every source
    must have an expected hash. A descriptor is presentation metadata, not a
    preregistration certificate: the research protocol remains separate.
    """
    descriptor_path = Path(descriptor_path).resolve()
    output = Path(output_directory).resolve()
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite presentation directory: {output}')
    started = time.process_time()
    raw = descriptor_path.read_bytes()
    descriptor = json.loads(raw)
    if descriptor.get('format') != 'universe24-signal-clock-presentation-v1':
        raise ValueError('Unsupported presentation descriptor format')
    if not descriptor.get('cases'):
        raise ValueError('At least one complete recorded case is required')
    protocol = descriptor_path.parent / descriptor['protocol']['path']
    if digest(protocol) != descriptor['protocol']['sha256']:
        raise ValueError('Protocol hash mismatch')
    sources = {str(protocol.resolve()): digest(protocol)}
    experiments = []
    for case in descriptor['cases']:
        case_protocol=case.get('protocol',descriptor['protocol'])
        case_protocol_path=descriptor_path.parent/case_protocol['path']
        if digest(case_protocol_path)!=case_protocol['sha256']:
            raise ValueError(f'Case protocol hash mismatch: {case["id"]}')
        sources[str(case_protocol_path.resolve())]=case_protocol['sha256']
        registered=case.get('registered_protocol',case_protocol)
        registered_path=descriptor_path.parent/registered['path']
        if digest(registered_path)!=registered['sha256']:
            raise ValueError(f'Registered protocol hash mismatch: {case["id"]}')
        if json.loads(registered_path.read_bytes())!=json.loads(case_protocol_path.read_bytes()):
            raise ValueError(f'Registered protocol semantics differ: {case["id"]}')
        sources[str(registered_path.resolve())]=registered['sha256']
        path = descriptor_path.parent / case['trace']
        if digest(path) != case['trace_sha256']:
            raise ValueError(f'Trace hash mismatch: {case["id"]}')
        sources[str(path.resolve())] = case['trace_sha256']
        experiment = from_trace(
            path, id=case['id'], title=case['title'],
            description=case.get('description', ''),
            readouts=case.get('readouts', []), view=case.get('view'),
        )
        experiment['provenance']['research_protocol_sha256'] = case_protocol['sha256']
        experiment['provenance']['protocol_copy_sha256'] = case_protocol['sha256']
        experiment['provenance']['registered_protocol_sha256'] = registered['sha256']
        experiment['provenance']['presentation_descriptor_sha256'] = hashlib.sha256(raw).hexdigest()
        experiment['provenance']['observational_scope'] = (
            'Recorded signal-triggered automaton experiment; no established physical light or time calibration'
        )
        experiments.append(experiment)
    data = bundle(experiments, title=descriptor.get('title', 'Signal-triggered clocks'))
    if descriptor_path.read_bytes() != raw:
        raise RuntimeError('Presentation descriptor changed while importing')
    for path, expected in sources.items():
        if digest(path) != expected:
            raise RuntimeError(f'Input changed while importing: {path}')
    output.mkdir(parents=True)
    data_path = output / 'experiments.json'
    write_bundle(data_path, data)
    html, build_manifest = build(data_path, output / 'Signal_Clocks.html')
    manifest = {
        'format': 'universe24-signal-clock-presentation-build-v1',
        'scope': 'Complete recorded states displayed by unchanged generic Presenter assets',
        'physical_light_claim': False,
        'descriptor_sha256': hashlib.sha256(raw).hexdigest(),
        'descriptor_path': str(descriptor_path),
        'protocol_sha256': descriptor['protocol']['sha256'],
        'input_sha256': sources,
        'builder_source_sha256': digest(__file__),
        'bundle_sha256': digest(data_path),
        'html_sha256': digest(html),
        'generic_build_manifest_sha256': digest(build_manifest),
        'experiments': [
            {'id': item['id'], 'frames': len(item['frames']),
             'verified_transitions': len(item['frames']) - 1,
             'initial_state_sha256': item['frames'][0]['state_sha256'],
             'coupling_fingerprint': item['coupling']['fingerprint'],
             'research_protocol_sha256':item['provenance']['research_protocol_sha256'],
             'protocol_copy_sha256':item['provenance']['protocol_copy_sha256'],
             'registered_protocol_sha256':item['provenance']['registered_protocol_sha256'],
             'readouts': item['readouts']}
            for item in experiments
        ],
        'elapsed_cpu_seconds': round(time.process_time() - started, 6),
    }
    _new_file(output / 'manifest.json', (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode())
    return html


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='Hash-pinned presentation descriptor')
    parser.add_argument('--output', type=Path, required=True, help='New output directory')
    args = parser.parse_args(argv)
    print(package(args.input, args.output))


if __name__ == '__main__':
    main()
