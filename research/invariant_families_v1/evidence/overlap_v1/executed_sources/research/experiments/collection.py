"""Lossless paged recordings for one reusable Presenter, with a static index.

This packaging code only reads complete saved trajectories. It neither searches
for outcomes nor chooses which cases to omit. Every declared case is required.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import tempfile
import time

from research.presenter.export import (bundle, canonical, from_trace, write_bundle,
                                       validate_bundle, MAX_CELLS, MAX_EXPERIMENTS, MAX_BYTES)
from research.presenter.build import _new_file
from .run import write_json

ROOT = Path(__file__).resolve().parents[2]
FORMAT = 'universe24-replay-collection-v1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _path(base, value):
    path = (base/value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Collection sources must be inside this research repository')
    return path


def _read_descriptor(path):
    raw = path.read_bytes()
    descriptor = json.loads(raw)
    if descriptor.get('format') != 'universe24-signal-clock-presentation-v1':
        raise ValueError('Unsupported complete-trace presentation descriptor')
    default_protocol = descriptor['protocol']
    for case in descriptor['cases']:
        protocol = case.get('protocol', default_protocol)
        protocol_path = _path(path.parent, protocol['path'])
        if sha(protocol_path) != protocol['sha256']:
            raise ValueError('Protocol hash changed: '+str(protocol_path))
        source = _path(path.parent, case['trace'])
        if sha(source) != case['trace_sha256']:
            raise ValueError('Complete trace hash changed: '+str(source))
        options = {'id':case['id'], 'title':case['title'], 'description':case.get('description',''),
                   'readouts':case.get('readouts',[]), 'view':case.get('view')}
        if source.suffix == '.gz':
            with tempfile.TemporaryDirectory(prefix='presenter-trace-', dir=ROOT/'runs') as temp:
                unpacked = Path(temp)/'states.jsonl'
                unpacked.write_bytes(gzip.decompress(source.read_bytes()))
                experiment = from_trace(unpacked, **options)
        else:
            experiment = from_trace(source, **options)
        experiment['provenance'].update({'research_protocol_sha256':protocol['sha256'],
                                         'presentation_descriptor_sha256':hashlib.sha256(raw).hexdigest()})
        yield experiment, source, protocol_path
    if path.read_bytes() != raw:
        raise RuntimeError('Presentation descriptor changed during packaging')


def _read_portables(group, base):
    for relative in group['portable_files']:
        source = _path(base, relative)
        raw = source.read_bytes()
        data = json.loads(raw)
        validate_bundle(data)
        if not data['experiments']:
            raise ValueError('Declared complete portable recording is empty')
        native = source.parent/'states.jsonl.gz'
        if not native.exists():
            native = source.parent/'states.jsonl'
        for experiment in data['experiments']:
            # Preserve original labels/readouts and full provenance; collection
            # status is stated outside the numerical recording in the index.
            yield experiment, native if native.exists() else source, None
        if source.read_bytes() != raw:
            raise RuntimeError('Portable recording changed during packaging')


def _archive_recording(source, destination):
    raw = source.read_bytes()
    if source.suffix == '.gz':
        encoded = raw
        decoded = gzip.decompress(raw)
    else:
        decoded = raw
        encoded = gzip.compress(raw, compresslevel=6, mtime=0)
    _new_file(destination, encoded)
    if gzip.decompress(destination.read_bytes()) != decoded:
        raise ValueError('Archived full recording does not decode identically')
    return {'original_path':str(source.relative_to(ROOT)), 'original_sha256':hashlib.sha256(raw).hexdigest(),
            'decoded_sha256':hashlib.sha256(decoded).hexdigest(),
            'archive_sha256':hashlib.sha256(encoded).hexdigest(), 'decoded_bytes':len(decoded),
            'archive_bytes':len(encoded)}


def package(config_path, output):
    config_path, output = Path(config_path).resolve(), Path(output).resolve()
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    if config.get('format') != FORMAT or not isinstance(config.get('groups'), list):
        raise ValueError('Unsupported replay collection configuration')
    if output.exists():
        raise FileExistsError('Collection output must be a new directory')
    output.mkdir(parents=True)
    (ROOT/'runs').mkdir(exist_ok=True)
    catalog = bundle([])['catalog']
    report = {'format':FORMAT, 'configuration_sha256':hashlib.sha256(config_raw).hexdigest(),
              'groups':[], 'experiments':0, 'frames':0, 'full_recordings':[],
              'limits':{'max_experiments':MAX_EXPERIMENTS,'max_stored_cells':MAX_CELLS,'max_bundle_bytes':MAX_BYTES},
              'scope':'All declared complete recordings, including failed hypotheses and controls; no trajectory filtering.'}
    identifiers = set()
    started = time.monotonic()
    for group in config['groups']:
        identifier = group['id']
        if not re.fullmatch(r'[a-z0-9-]+', identifier) or identifier in identifiers:
            raise ValueError('Collection group IDs must be distinct safe names')
        identifiers.add(identifier)
        if ('descriptor' in group) == ('portable_files' in group):
            raise ValueError('A group must select one descriptor or a list of portable files')
        entries = _read_descriptor(_path(config_path.parent, group['descriptor'])) if 'descriptor' in group else _read_portables(group, config_path.parent)
        directory = output/identifier
        directory.mkdir()
        batch, cells, byte_estimate, number = [], 0, 0, 0
        info = {'id':identifier,'title':group['title'],'status':group['status'],'parts':[], 'experiments':0, 'frames':0}
        seen = set()
        def flush():
            nonlocal batch,cells,byte_estimate,number
            if not batch:
                return
            number += 1
            filename = f'part-{number:03d}.json'
            target = directory/filename
            data = {'format':'universe24-presenter-v1','title':group['title']+f' · part {number}',
                    'catalog':catalog,'experiments':batch}
            write_bundle(target, data)
            info['parts'].append({'file':str(target.relative_to(output)), 'sha256':sha(target),
                                  'experiments':len(batch),'frames':sum(len(e['frames'])for e in batch),
                                  'stored_cells':cells,'bytes':target.stat().st_size,
                                  'case_ids':[e['id']for e in batch]})
            batch,cells,byte_estimate = [],0,0
        for experiment, native, protocol in entries:
            if experiment['id'] in seen:
                raise ValueError('Duplicate case in collection group')
            seen.add(experiment['id'])
            stored = sum(len(f['cells']) for f in experiment['frames'])
            size = len(canonical(experiment))
            if stored > MAX_CELLS or size > MAX_BYTES-100000:
                raise ValueError('A single full recording exceeds the Presenter budget; cannot silently truncate')
            if batch and (len(batch)>=MAX_EXPERIMENTS or cells+stored>400000 or byte_estimate+size>48000000):
                flush()
            batch.append(experiment)
            cells += stored
            byte_estimate += size
            index = info['experiments']
            archive = directory/'recordings'/f'{index:04d}.json.gz'
            retained = _archive_recording(native, archive)
            retained.update({'group':identifier,'case_id':experiment['id'],
                             'file':str(archive.relative_to(output)),'frames':len(experiment['frames'])})
            if protocol is not None:
                target = directory/'protocols'/(sha(protocol)+'.json')
                if not target.exists():
                    _new_file(target, protocol.read_bytes())
                retained['protocol'] = str(target.relative_to(output))
            report['full_recordings'].append(retained)
            info['experiments'] += 1
            info['frames'] += len(experiment['frames'])
        flush()
        if not seen:
            raise ValueError('A declared research family has no complete recordings')
        if 'expected_experiments' in group and info['experiments'] != group['expected_experiments']:
            raise ValueError('Recorded case count differs from the declared complete family')
        report['groups'].append(info)
        report['experiments'] += info['experiments']
        report['frames'] += info['frames']
        print(json.dumps({'group':identifier,'experiments':info['experiments'],'parts':len(info['parts'])}),flush=True)
    if config_path.read_bytes() != config_raw:
        raise RuntimeError('Collection definition changed during packaging')
    main = _path(config_path.parent, config['main_html'])
    _new_file(output/'The_Presenter.html', main.read_bytes())
    report['main_html_sha256'] = sha(main)
    report['elapsed_seconds'] = time.monotonic()-started
    write_json(output/'manifest.json', report)
    sections = []
    for info in report['groups']:
        rows = ''.join('<li><a href="'+html.escape(part['file'])+'">Part '+str(i+1)+'</a> · '+str(part['experiments'])+' experiments · '+str(part['frames'])+' full states</li>' for i,part in enumerate(info['parts']))
        sections.append('<section><h2>'+html.escape(info['title'])+'</h2><p>'+html.escape(info['status'])+'</p><ul>'+rows+'</ul></section>')
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>The Presenter · Complete research collection</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#19333d;background:#f3f0e8;max-width:960px;margin:48px auto;padding:0 24px}a{color:#087f83}h1,h2{line-height:1.2}section{background:#fffcf6;border:1px solid #d9dfd6;border-radius:14px;padding:24px;margin:24px 0}.note{color:#596f73}li{margin:8px 0}</style></head><body>'
            '<h1>The Presenter</h1><p>Complete research recordings, assembled from the same integer states and replayed by one generic viewer.</p>'
            '<p><a href="The_Presenter.html">Open selected examples in The Presenter</a></p>'
            '<p>To inspect another family, save one numbered JSON part below, open The Presenter in a browser, and choose <strong>Open experiment</strong> to import that file. Then use its Experiment selector. Every part preserves every stored channel and remainder; nothing is sampled away.</p>'
            '<p class="note">Selected examples are not the complete evidence. The families below include negative results and all declared controls. An attachment preview that blocks JavaScript cannot play the cube; the static index remains usable. Canvas/DOM checks are not an iPad browser validation.</p>'
            ''.join(sections)+'<p><a href="manifest.json">Full provenance, checksums and exact compressed-recording paths</a></p></body></html>')
    _new_file(output/'index.html',page.encode('utf-8'))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=package(args.config,args.output)
    print(json.dumps({'experiments':report['experiments'],'frames':report['frames'],'seconds':report['elapsed_seconds']},indent=2))
