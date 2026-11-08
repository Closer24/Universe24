"""Package any valid Presenter bundle as one offline HTML file.

This module only validates and presents already determined trajectories. It
never supplies updates to the Universe24 engine.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_escape
import json
import os
from pathlib import Path
import re
import tempfile

from .export import MAX_BYTES, ResourceLimitError, validate_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f'Nonfinite JSON value: {value}')


def _new_file(path, raw):
    """Atomic create-if-absent, including on a competing writer's race."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.presenter-',
                                         suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _json_script(value):
    # A literal '<' can terminate a script element even inside a JS string.
    return json.dumps(value, ensure_ascii=True, separators=(',', ':'),
                      sort_keys=True, allow_nan=False).replace('<', '\\u003c')


def _script_source(text):
    # HTML parsing precedes JavaScript parsing, even inside JS comments/strings.
    # The local sources must not contain a literal closing script delimiter.
    if re.search(r'</script\b', text, re.IGNORECASE):
        raise ValueError('Local JavaScript contains an unsafe closing script delimiter')
    return text


def _replace_one(text, pattern, replacement, description):
    text, count = re.subn(pattern, lambda _match: replacement, text,
                          flags=re.IGNORECASE)
    if count != 1:
        raise ValueError(f'Expected exactly one {description}; found {count}')
    return text


def build(input_path, output_path):
    """Validate an arbitrary bundle and create HTML plus a provenance manifest.

    Existing output files are never overwritten. The input JSON uses decimal
    strings for counters; ordinary JSON numbers are only bounded geometry and
    presentation/provenance metadata. No experiment identity is inspected here.
    """
    input_path, output_path = Path(input_path), Path(output_path)
    manifest_path = output_path.with_suffix(output_path.suffix + '.manifest.json')
    for path in (output_path, manifest_path):
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite {path}')
    if input_path.stat().st_size > MAX_BYTES:
        raise ResourceLimitError('Input bundle exceeds the 64 MiB byte budget')
    raw = input_path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ResourceLimitError('Input bundle exceeds the 64 MiB byte budget')
    data = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_object,
                      parse_constant=_reject_constant)
    verifier_paths = [HERE / 'export.py', *sorted((ROOT / 'universe24').rglob('*.py'))]
    verifier_sources = {str(path.relative_to(ROOT)): path.read_bytes() for path in verifier_paths}
    validate_bundle(data)
    asset_names = ('index.html', 'style.css', 'startup.js', 'data.js', 'app.js')
    sources = {name: (HERE / name).read_bytes() for name in asset_names}
    sources['build.py'] = Path(__file__).read_bytes()
    hashes = {f'research/presenter/{name}': sha256(content)
              for name, content in sources.items()}
    source_record = {
        'format': 'universe24-presenter-build-v1',
        'bundle_sha256': sha256(raw),
        'source_sha256': hashes,
        'verifier_source_sha256': {name: sha256(content)
                                  for name, content in verifier_sources.items()},
        'scope': 'Read-only replay; complete states verified with the Python sources identified here',
    }
    html = sources['index.html'].decode('utf-8')
    # This inventory remains readable when a file preview does not run scripts.
    # It describes embedded data; it is not an interactive or simulated control.
    inventory = ''.join(
        '<li><strong>' + html_escape.escape(experiment.get('title') or experiment['id']) +
        '</strong><span>' + str(len(experiment['frames'])) + ' recorded states · L = ' +
        str(experiment['side']) + '</span></li>' for experiment in data['experiments'])
    count = len(data['experiments'])
    html = _replace_one(
        html, r'<div\s+id="packaged-recordings">.*?</div>',
        '<div id="packaged-recordings"><p id="embedded-count">' + str(count) +
        ' recorded experiment' + ('s are' if count != 1 else ' is') +
        ' embedded in this file.</p><details class="startup-inventory" open>' +
        '<summary>Embedded recordings · static list</summary><ol id="embedded-recordings">' +
        inventory + '</ol></details></div>', 'static recording inventory')
    css = sources['style.css'].decode('utf-8')
    if re.search(r'</style\b', css, re.IGNORECASE):
        raise ValueError('Local CSS contains an unsafe closing style delimiter')
    html = _replace_one(
        html, r'<link\b(?=[^>]*\bhref=[\"\'](?:\./)?style\.css[\"\'])[^>]*>',
        '<style>\n' + css + '\n</style>', 'local stylesheet reference')
    for name in ('startup.js', 'data.js', 'app.js'):
        code = _script_source(sources[name].decode('utf-8'))
        embedded = '<script>\n' + code + '\n</script>'
        if name == 'app.js':
            embedded = ('<script id="presenter-build" type="application/json">' +
                        _json_script(source_record) + '</script>\n' +
                        '<script>globalThis.PRESENTER_BUNDLE=' +
                        _json_script(data) + ';</script>\n' + embedded)
        html = _replace_one(
            html, r'<script\b(?=[^>]*\bsrc=[\"\'](?:\./)?' + re.escape(name) +
            r'[\"\'])[^>]*>\s*</script\s*>', embedded,
            f'local {name} reference')
    if re.search(r'<script\b[^>]*\bsrc\s*=|<link\b[^>]*\brel=[\"\']stylesheet',
                 html, re.IGNORECASE):
        raise ValueError('Standalone HTML still contains an external script or stylesheet reference')
    # The supplied viewer uses inline canvas/SVG and system fonts. Reject newly
    # introduced resource tags or CSS loads rather than quietly packaging them.
    if re.search(r'<(?:img|iframe|audio|video|source|embed|object)\b[^>]*\b(?:src|data|poster)\s*=',
                 html, re.IGNORECASE) or re.search(r'@import\b|\burl\s*\(', css, re.IGNORECASE):
        raise ValueError('Standalone assets contain an unexpected external-resource mechanism')
    for name, original in sources.items():
        if (HERE / name).read_bytes() != original:
            raise RuntimeError(f'Source changed during packaging: {name}; retry with stable sources')
    if input_path.read_bytes() != raw:
        raise RuntimeError('Input bundle changed during packaging')
    for name, original in verifier_sources.items():
        if (ROOT / name).read_bytes() != original:
            raise RuntimeError(f'Verifier source changed during packaging: {name}')
    encoded = html.encode('utf-8')
    manifest = {
        **source_record,
        'html_sha256': sha256(encoded),
        'html_bytes': len(encoded),
        'bundle_bytes': len(raw),
        'experiments': [{
            'id': experiment['id'],
            'frames': len(experiment['frames']),
            'verified_transitions': len(experiment['frames']) - 1,
            'coupling_fingerprint': experiment['coupling']['fingerprint'],
            'initial_state_sha256': experiment['frames'][0]['state_sha256'],
            'final_state_sha256': experiment['frames'][-1]['state_sha256'],
        } for experiment in data['experiments']],
        'external_resource_tags': 0,
        'network_audit': 'Requires the separate browser acceptance report; not inferred from static packaging',
        'overwrites_existing_files': False,
    }
    # Finish all computation and validation before creating either deliverable.
    _new_file(output_path, encoded)
    _new_file(manifest_path, (json.dumps(manifest, ensure_ascii=True,
                                       sort_keys=True, indent=2) + '\n').encode('ascii'))
    return output_path, manifest_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True,
                        help='Any complete universe24-presenter-v1 JSON bundle')
    parser.add_argument('--output', type=Path, required=True,
                        help='New standalone HTML path; never overwritten')
    args = parser.parse_args(argv)
    try:
        output, manifest = build(args.input, args.output)
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        parser.exit(2, f'The Presenter: {exc}\n')
    print(json.dumps({'html': str(output), 'manifest': str(manifest)}))


if __name__ == '__main__':
    main()
