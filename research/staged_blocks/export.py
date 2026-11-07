"""Package complete recorded outcomes in the unchanged generic Presenter.

python -m research.staged_blocks.export --input RECORD.json.gz --output NEW_DIR
Repeat --input to include multiple complete records or native Presenter bundles.
This is a read-only operation: no trajectory is generated or filtered here.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
from pathlib import Path

from research.experiments.run import write_json
from research.presenter.build import build
from research.presenter.export import (FORMAT, MAX_BYTES, MAX_CELLS, MAX_EXPERIMENTS,
                                       bundle, canonical, write_bundle)


def read_recordings(path):
    """Read unchanged native experiments from one complete research artifact."""
    path = Path(path)
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError("Input artifact exceeds the Presenter byte budget")
    if path.suffix == ".gz":
        # Bound the decompressed input rather than accepting an unlimited stream.
        with gzip.open(path, "rb") as handle:
            decoded = handle.read(MAX_BYTES + 1)
    else:
        decoded = raw
    if len(decoded) > MAX_BYTES:
        raise ValueError("Decoded artifact exceeds the Presenter byte budget")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate artifact member: " + key)
            result[key] = value
        return result

    def reject(value):
        raise ValueError("Nonfinite artifact number: " + value)

    data = json.loads(decoded, object_pairs_hook=unique, parse_constant=reject)
    if not isinstance(data, dict):
        raise ValueError("A recording artifact must be an object")
    if data.get("format") == FORMAT:
        experiments = data["experiments"]
    elif "experiment" in data:
        experiments = [data["experiment"]]
    elif "frames" in data and "coupling" in data:
        experiments = [data]
    else:
        raise ValueError("Artifact has no complete native Presenter recording")
    if not isinstance(experiments, list) or not experiments:
        raise ValueError("Artifact must contain at least one complete recording")
    return experiments, hashlib.sha256(raw).hexdigest()


def export_records(inputs, output, *, title="Staged building blocks — recorded outcomes"):
    """Validate every full state, then create a self-contained replay package.

    Inputs and experiment IDs must be unique. No frame, channel, remainder,
    arithmetic event or readout is removed or relabeled during presentation.
    """
    paths = [Path(path).resolve() for path in inputs]
    if not paths or len(set(paths)) != len(paths):
        raise ValueError("Supply distinct recording paths")
    output = Path(output)
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    experiments, provenance = [], []
    for path in paths:
        values, digest = read_recordings(path)
        experiments.extend(values)
        provenance.append({"path": str(path), "sha256": digest,
                           "experiments": [item.get("id") for item in values]})
    identifiers = [item.get("id") for item in experiments]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Duplicate experiment IDs; no recording is silently replaced")
    data = bundle(experiments, title=title)
    output.mkdir(parents=True, exist_ok=False)
    write_bundle(output / "experiments.json", data)
    html, _ = build(output / "experiments.json", output / "The_Presenter.html")
    for path, source in zip(paths, provenance):
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise RuntimeError("Input changed during packaging: " + str(path))
    result = {"format": "universe24-staged-presenter-v1", "inputs": provenance,
              "experiments": identifiers, "frames": sum(len(e["frames"]) for e in experiments),
              "html": html.name, "complete_recordings": True,
              "read_only": True, "browser_execution_verified": False,
              "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    write_json(output / "manifest.json", result)
    return result


def partition_experiments(experiments, *, title, max_cells=MAX_CELLS,
                          max_experiments=MAX_EXPERIMENTS):
    """Stable whole-experiment packing under the existing protected limits."""
    if type(max_cells) is not int or not 0 < max_cells <= MAX_CELLS:
        raise ValueError("Page cell budget cannot enlarge the protected Presenter limit")
    if type(max_experiments) is not int or not 0 < max_experiments <= MAX_EXPERIMENTS:
        raise ValueError("Page experiment budget cannot enlarge the protected Presenter limit")
    identifiers = [e.get("id") for e in experiments]
    if not experiments or len(set(identifiers)) != len(identifiers):
        raise ValueError("Supply nonempty recordings with distinct experiment IDs")
    # Exact canonical envelope size. Only complete experiment objects are packed.
    envelope = len((canonical(bundle([], title=title)) + "\n").encode("ascii"))
    pages, current, cells, encoded = [], [], 0, envelope
    for experiment in experiments:
        count = sum(len(frame["cells"]) for frame in experiment["frames"])
        size = len(canonical(experiment).encode("ascii"))
        if count > max_cells or envelope + size > MAX_BYTES:
            raise ValueError("One complete experiment exceeds a Presenter page: " + experiment["id"])
        separator = 1 if current else 0
        if current and (len(current) >= max_experiments or cells + count > max_cells
                        or encoded + separator + size > MAX_BYTES):
            pages.append(current)
            current, cells, encoded, separator = [], 0, envelope, 0
        current.append(experiment)
        cells += count
        encoded += separator + size
    if current:
        pages.append(current)
    return pages


def export_pages(inputs, output, *, title="Staged building blocks — recorded outcomes",
                 max_cells=MAX_CELLS, max_experiments=MAX_EXPERIMENTS):
    """Create deterministic standalone pages and a static complete inventory."""
    paths = [Path(path).resolve() for path in inputs]
    output = Path(output)
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    if not paths or len(set(paths)) != len(paths):
        raise ValueError("Supply distinct recording paths")
    experiments, provenance = [], []
    for path in paths:
        values, digest = read_recordings(path)
        experiments.extend(values)
        provenance.append({"path": str(path), "sha256": digest,
                           "experiments": [item.get("id") for item in values]})
    groups = partition_experiments(experiments, title=title, max_cells=max_cells,
                                   max_experiments=max_experiments)
    output.mkdir(parents=True, exist_ok=False)
    pages = []
    for index, group in enumerate(groups, start=1):
        filename = "The_Presenter.html" if index == 1 else f"The_Presenter_{index:03d}.html"
        bundle_path = output / f"experiments-{index:03d}.json"
        write_bundle(bundle_path, bundle(group, title=title))
        build(bundle_path, output / filename)
        pages.append({"number": index, "html": filename, "bundle": bundle_path.name,
                      "experiments": [e["id"] for e in group],
                      "frames": sum(len(e["frames"]) for e in group),
                      "complete_sparse_rows": sum(len(f["cells"]) for e in group for f in e["frames"])})
    sections = []
    for page, group in zip(pages, groups):
        rows = "".join("<li><strong>" + html.escape(e["title"]) + "</strong><br><code>" +
                       html.escape(e["id"]) + "</code> · " + str(len(e["frames"])) +
                       " complete states</li>" for e in group)
        sections.append('<section><h2><a href="' + page["html"] + '">Open The Presenter · Page ' +
                        str(page["number"]) + '</a></h2><ol>' + rows + '</ol></section>')
    index_html = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" '
                  'content="width=device-width,initial-scale=1"><title>' + html.escape(title) +
                  '</title><style>body{max-width:960px;margin:40px auto;padding:0 24px;font:18px system-ui;'
                  'line-height:1.5;color:#183740;background:#f3f1e9}a{color:#126968}section{padding:18px 0;'
                  'border-top:1px solid #b8c9c3}li{margin:12px 0}code{font-size:14px}</style><h1>The Presenter</h1>'
                  '<p>This static index lists every selected complete recording. Each linked page is a '
                  'self-contained interactive Presenter. Open it in a JavaScript-enabled browser. '
                  'An attachment preview may show only the inventory.</p><p>' + str(len(experiments)) +
                  ' recordings across ' + str(len(pages)) + ' page(s). No experiment or frame is split or '
                  'dropped. Page boundaries respect the unchanged viewer resource limits.</p>' +
                  "".join(sections) + '</html>')
    (output / "index.html").write_text(index_html, encoding="utf-8")
    for path, source in zip(paths, provenance):
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise RuntimeError("Input changed during packaging: " + str(path))
    result = {"format": "universe24-staged-presenter-pages-v1", "inputs": provenance,
              "experiments": [e["id"] for e in experiments], "pages": pages,
              "html": pages[0]["html"], "index": "index.html",
              "frames": sum(page["frames"] for page in pages),
              "page_limits": {"complete_sparse_rows": max_cells, "experiments": max_experiments,
                              "bytes": MAX_BYTES},
              "complete_recordings": True, "read_only": True, "browser_execution_verified": False,
              "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    write_json(output / "manifest.json", result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", default="Staged building blocks — recorded outcomes")
    parser.add_argument("--pages", action="store_true", help="Preserve all recordings across bounded standalone pages")
    args = parser.parse_args(argv)
    exporter = export_pages if args.pages else export_records
    print(json.dumps(exporter(args.input, args.output, title=args.title), indent=2))


if __name__ == "__main__":
    main()
