"""One bounded-channel execution, complete replay and passive click pipeline.

Input bundles declare a law; this module never selects a second physical model
or substitutes a reference answer. Checksums provide corruption detection, not
authentication. Passing these execution checks does not establish Einstein or
quantum physics. Trace storage is external evidence, never an Engine input.
"""
from __future__ import annotations

from contextlib import contextmanager
import gzip
import hashlib
import io
from ..core import exact_json as json
from pathlib import Path

from ..core.engine import Engine, State
from .bundle import SystemBundle, load_bundle, save_bundle, validate_bundle
from .decoder import decode_transition, make_transition

RUN_SCHEMA = "universe24/system/run/1"
TRACE_FILE = "full_trace.jsonl.gz"
CLICK_FILE = "clicks.jsonl.gz"


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _hash(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


@contextmanager
def _writer(path):
    # Zero timestamp and no original filename make identical runs byte stable.
    with Path(path).open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as stream:
                yield stream


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _loads(line):
    def bad(value):
        raise ValueError(f"non-integer JSON number {value}")
    return json.loads(line, object_pairs_hook=_pairs, parse_float=bad, parse_constant=bad)


def _records(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                raise ValueError("blank trace/click record")
            yield _loads(line)


def _bits(state):
    return max((abs(int(value)).bit_length() for array in (state.a, state.b, state.r)
                for value in array.flat), default=0)


def _source_hashes():
    package = Path(__file__).resolve().parents[1]
    paths = ("core/engine.py", "core/tensor.py", "core/lattice.py", "core/exact_json.py",
             "system/bundle.py", "system/decoder.py", "system/runtime.py")
    return {name: _file_hash(package / name) for name in paths}


def _run_id(bundle, steps):
    return _hash({"schema": RUN_SCHEMA, "bundle_id": bundle.bundle_id, "steps": steps})


def _report(bundle, steps, run_id, final, bit_sizes, click_count, directory):
    return {
        "schema": RUN_SCHEMA,
        "run_id": run_id,
        "bundle_id": bundle.bundle_id,
        "tensor_hash": bundle.tensor.fingerprint,
        "steps": steps,
        "channels_per_node": bundle.tensor.G,
        "retained_integers_per_node": 3 * bundle.tensor.G,
        "nodes": final.N,
        "final_state_hash": _hash(final.to_dict()),
        "click_count": click_count,
        "maximum_integer_bits_by_step": bit_sizes,
        "trace_role": "external complete audit record; never fed into evolution",
        "source_hashes": _source_hashes(),
        "files": {name: _file_hash(directory / name) for name in (TRACE_FILE, CLICK_FILE)},
        "checks": {
            "bundle_contract": "passed",
            "complete_state_forward_replay": "passed",
            "complete_state_step_inverse": "passed",
            "complete_state_rewind_to_seed": "passed",
            "canonical_click_parity": "passed",
        },
        "acceptance_gates": {
            "A": {"status": "partial", "reason": "Run-specific mechanical checks passed; universal claims require the independent oracle and causal tests."},
            "B": {"status": "partial", "reason": "Canonical arithmetic click parity checked; an operational physical event map is not established."},
            "C": {"status": "not_tested", "reason": "No independently validated Einstein geometry supplied by the generic executor."},
            "D": {"status": "not_tested", "reason": "One execution is not a space/time/quantization convergence study."},
            "E": {"status": "not_tested", "reason": "No shared-metric physical clock or motion evidence established."},
            "F": {"status": "not_tested", "reason": "Arithmetic clicks do not establish a detector model, Born law or Bell result."},
        },
    }


def run_bundle(bundle: SystemBundle | str | Path, out: str | Path, steps: int) -> dict:
    """Execute a supplied complete bundle and save reproducible audit evidence.

    Refuses nonempty output directories. All evolution occurs in the unchanged
    Engine. A successful result is returned only after independent saved-input
    loading, full trace replay, exact rewind and saved-click comparison.
    """
    steps = _integer(steps, "steps")
    if not isinstance(bundle, SystemBundle):
        bundle = load_bundle(bundle)
    bundle = validate_bundle(bundle)
    directory = Path(out)
    if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
        raise ValueError("run output must be a new or empty directory")
    directory.mkdir(parents=True, exist_ok=True)
    save_bundle(bundle, directory / "bundle")
    # Re-read the exact saved inputs; avoid trusting mutable caller-owned data.
    bundle = load_bundle(directory / "bundle")
    run_id = _run_id(bundle, steps)
    engine = Engine(bundle.tensor)
    seed = bundle.seed
    current = seed.copy()
    bit_sizes = [_bits(current)]
    click_count = 0
    with _writer(directory / TRACE_FILE) as trace, _writer(directory / CLICK_FILE) as clicks:
        for step in range(1, steps + 1):
            after = engine.step(current)
            if not engine.inverse_step(after).same_as(current):
                raise ValueError(f"complete inverse failed at step {step}")
            record = make_transition(bundle.tensor, current, after, run_id=run_id, step=step)
            trace.write(_json(record) + "\n")
            for event in decode_transition(record, bundle.tensor, run_id=run_id):
                clicks.write(_json(event) + "\n")
                click_count += 1
            current = after
            bit_sizes.append(_bits(current))
    if not engine.rewind(current, steps).same_as(seed):
        raise ValueError("complete rewind did not recover seed")
    report = _report(bundle, steps, run_id, current, bit_sizes, click_count, directory)
    report_path = directory / "validation.json"
    report_path.write_text(_json(report) + "\n", encoding="utf-8")
    try:
        return verify_run(directory)
    except Exception:
        # Never leave a successful validation record after failed verification.
        report_path.unlink(missing_ok=True)
        raise


def verify_run(path: str | Path) -> dict:
    """Reject corrupt, incomplete or non-reproducible saved execution evidence.

    Recompute every transition from the bundled seed, including audit channels
    and remainders. Stream files so trace size does not become hidden runtime
    state. Report hashes are checked against recomputed values, not trusted.
    """
    directory = Path(path)
    report = _loads((directory / "validation.json").read_text(encoding="utf-8"))
    if not isinstance(report, dict) or report.get("schema") != RUN_SCHEMA:
        raise ValueError("unsupported run schema")
    steps = _integer(report.get("steps"), "steps")
    bundle = load_bundle(directory / "bundle")
    run_id = _run_id(bundle, steps)
    if report.get("run_id") != run_id or report.get("bundle_id") != bundle.bundle_id:
        raise ValueError("run/bundle identity mismatch")
    for name in (TRACE_FILE, CLICK_FILE):
        if report.get("files", {}).get(name) != _file_hash(directory / name):
            raise ValueError(f"run file checksum mismatch: {name}")
    engine = Engine(bundle.tensor)
    seed = bundle.seed
    current = seed.copy()
    bit_sizes = [_bits(current)]
    saved_clicks = iter(_records(directory / CLICK_FILE))
    count = 0
    seen_steps = 0
    missing = object()
    try:
        for step, record in enumerate(_records(directory / TRACE_FILE), start=1):
            if step > steps:
                raise ValueError("extra trace transition")
            after = engine.step(current)
            expected = make_transition(bundle.tensor, current, after, run_id=run_id, step=step)
            if _json(record) != _json(expected):
                raise ValueError(f"complete trace mismatch at step {step}")
            if not engine.inverse_step(after).same_as(current):
                raise ValueError(f"complete inverse failed at step {step}")
            for event in decode_transition(record, bundle.tensor, run_id=run_id):
                saved = next(saved_clicks, missing)
                if saved is missing or _json(saved) != _json(event):
                    raise ValueError(f"click stream mismatch at event {count + 1}")
                count += 1
            current = after
            bit_sizes.append(_bits(current))
            seen_steps = step
        if seen_steps != steps:
            raise ValueError("missing trace transition")
        if next(saved_clicks, missing) is not missing:
            raise ValueError("extra click event")
    finally:
        saved_clicks.close()
    if not engine.rewind(current, steps).same_as(seed):
        raise ValueError("complete rewind did not recover seed")
    expected_report = _report(bundle, steps, run_id, current, bit_sizes, count, directory)
    if _json(report) != _json(expected_report):
        raise ValueError("validation report disagrees with reproduced execution or source version")
    return expected_report
