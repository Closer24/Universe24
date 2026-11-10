"""The only verifier of the curated experiments (one generic procedure, no per-experiment code).

    python -m research.matter_light_experiments_v1.verify E01_local_atom_twins     # one experiment
    python -m research.matter_light_experiments_v1.verify --all                    # every experiment
    python -m research.matter_light_experiments_v1.verify --fast                   # only runs marked fast
    python -m research.matter_light_experiments_v1.verify --all --keep DIR         # keep click logs and reports

For every run of an experiment's ``experiment.json``:

1. the initial data are checked: the init file's SHA-256, or the referenced published block's file SHA-256, or
   (for a run made from a composition: the experiment's ``composition.json``, or one of the composition files that the
   manifest declares under ``compositions``) the composition is regenerated with the registered generators
   (``research.matter_light_blocks_v1.registry``), optionally followed by ``rewind`` exact inverse steps (a preparation
   before t = 0, each step checked), and its initial-state digest compared; a run made only from a composition must
   record that digest, and a run that also names a file or block must have exactly that initial state;
2. the run is replayed with the unchanged ``Engine``, checking ``Engine.rewind`` at every update;
3. the official click log is written (the record format of ``python -m universe24 --events``) into a temporary
   directory, or under ``--keep`` (never overwriting);
4. the final full-state SHA-256 and the log SHA-256 are compared with the manifest;
5. the pinned decoder must be the frozen one: ``click_decoder_v1`` code hashes equal to the manifest's pin and to
   the decoder's ``FROZEN.json``; otherwise every check is reported as "decoder pending" (or "decoder changed");
6. each log is decoded by the frozen decoder (``decode``; declared detector probes through ``correlations``; a run
   that declares a projection ``layer`` is decoded on that declared subset of its official log, hash-checked) and
   every declared check is evaluated **on the decoder output only**;
7. a check that names a released decoder layer (``"layer"``, ``"call"``, ``"args"``) is evaluated on that layer's
   result for the official logs of its runs: the layers are a closed list (``LAYERS``), each frozen by its own
   ``FROZEN_<name>.json`` in ``research/click_decoder_v1`` and pinned by the manifest (``layers``).

The complete state is used only for integrity (inverse and hashes).  The verifier writes no state and prints one
JSON report; the exit status is 1 if any integrity step or any evaluable check fails.  Checks that the closed
vocabulary cannot express yet are reported as "not decodable" and keep the experiment out of "ready".

**Explicitly separate candidate variants** (AGENTS.md).  A manifest whose ``coupling`` is ``{"kind": "variant",
"label": "variant:<name>@<12 hex>", "fingerprint": "<64 hex>"}`` (the table's ``VariantCoupling.label`` and
``.fingerprint``, as in the blocks catalog) runs under that fixed table, never under the reference model.  Its data
files (``init``, ``block_file``, and the board files that ``compositions`` declares, since the registry composes
reference boards only) are ``universe24-variant-init-v1`` files, loaded only by
``research.coupling_variants_v1.from_dict`` (table rebuilt and validated, recorded fingerprint checked); each must hold
exactly the declared table, and a variant board file declares no controls.  Step 2 is then the variant runner,
``python -m research.coupling_variants_v1 --audit`` (in process): the ``VariantEngine`` with the exact inverse, the
local balance and the signed-account identity checked at every update.  Its event log, the official record format,
is the log that steps 4, 6 and 7 read; its summary (model, label, fingerprint, audited) is checked and reported.
A reference manifest takes none of these paths.
"""
from __future__ import annotations

import argparse
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import asdict
import cmath
import hashlib
import io
from itertools import product
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import time

from universe24.experiments import from_dict
from universe24.observation import clicks

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FORMAT = "matter_light_experiments_v1-experiment-1"
VARIANT_FORMAT = "universe24-variant-init-v1"          # research.coupling_variants_v1's init format
VARIANT_LABEL = re.compile(r"variant:[A-Za-z0-9][A-Za-z0-9._+-]{0,63}@([0-9a-f]{12})")
FINGERPRINT = re.compile(r"[0-9a-f]{64}")
OPS = ("eq", "ne", "lt", "le", "gt", "ge", "approx", "not_approx", "in", "len_eq", "len_ge", "same", "diff")
DERIVE = ("chsh", "alpha", "e_table", "covariant_curve", "best_chsh", "tlm", "plane_spectrum")
# released decoder layers (click_decoder_v1, each frozen by its FROZEN_<name>.json): the calls a check may use, and the
# number of official logs each call reads first (a one-log call reads the check's run, or each of its runs; a call of
# n > 1 logs reads "runs" = [a, b, ...] of length n, in that order)
LAYERS = {"log_symmetry_v1": {"mirror": 1, "best_tau": 1, "period": 1, "c_image": 1, "record_diff": 2},
          "beat_clock_v1": {"run_declared": 1}, "gr_observer_v1": {"run_declared": 1}}


# ------------------------------------------------------------------------------------------- data and hashes
def experiment_ids():
    return sorted(p.parent.name for p in HERE.glob("E*/experiment.json"))


def manifest(eid):
    data = json.loads((HERE / eid / "experiment.json").read_text(encoding="utf-8"))
    if data.get("format") != FORMAT or data.get("id") != eid:
        raise ValueError(f"{eid}: not a {FORMAT} manifest")
    return data


def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def state_sha256(state) -> str:
    """SHA-256 of a complete state (side, background, every non-background cell): the published verifier's rule."""
    blob = json.dumps([state.cube.side, list(state.background),
                       sorted([list(k), list(v)] for k, v in state.cells.items())], separators=(",", ":")).encode()
    return sha256_bytes(blob)


def _uses_composition(man) -> bool:
    """True if the manifest declares a composition or any run is made from one."""
    return bool(man.get("composition") or man.get("compositions")) or any("from_composition" in r for r in man["runs"])


# ---------------------------------------------------------------------- explicitly separate candidate variants
def variant_model(man):
    """``(label, fingerprint)`` of a variant manifest's table, ``coupling`` = ``{"kind": "variant", "label":
    "variant:<name>@<12 hex>", "fingerprint": "<64 hex>"}`` with the label's 12 hex the fingerprint's first 12; None
    for any other manifest (the reference path is unchanged)."""
    coupling = man.get("coupling") or {}
    if coupling.get("kind") != "variant":
        return None
    label, fingerprint = coupling.get("label"), coupling.get("fingerprint")
    found = VARIANT_LABEL.fullmatch(label) if isinstance(label, str) else None
    if set(coupling) != {"kind", "label", "fingerprint"} or found is None or not isinstance(fingerprint, str) \
            or not FINGERPRINT.fullmatch(fingerprint) or found.group(1) != fingerprint[:12]:
        raise ValueError("a variant manifest's coupling is {'kind': 'variant', 'label': 'variant:<name>@<12 hex>', "
                         "'fingerprint': '<64 hex>'}, the label ending in the fingerprint's first 12 hex")
    return label, fingerprint


def load_data(man, blob: bytes):
    """The experiment of an init or block file under the manifest's coupling: ``universe24.experiments.from_dict`` for a
    reference manifest; for a variant manifest a ``universe24-variant-init-v1`` file, loaded only by
    ``research.coupling_variants_v1.from_dict`` (the table is rebuilt and validated and its recorded fingerprint
    checked), whose table must be the manifest's: the same label and fingerprint, and not a reference table."""
    model = variant_model(man)
    data = json.loads(blob.decode("utf-8"))
    if model is None:
        return from_dict(data)
    if not isinstance(data, dict) or data.get("format") != VARIANT_FORMAT:
        raise ValueError(f"a variant manifest reads {VARIANT_FORMAT} files only")
    from research.coupling_variants_v1 import from_dict as variant_from_dict
    experiment = variant_from_dict(data)
    table = experiment.engine.coupling
    if not table.is_variant or (table.label, table.fingerprint) != model:
        raise ValueError(f"the file's table {table.label} is not the manifest's variant table")
    return experiment


def _variant_boards(eid, man):
    """``build(control=None, key=None)`` of a variant manifest: the board of the variant init file that the manifest
    declares as ``compositions[key]`` (no key: ``composition``), loaded by ``load_data``.  The same refusals as
    ``_composition`` (undeclared key, a file outside the experiment folder); a variant file declares no controls."""
    folder = (HERE / eid).resolve()
    cache = {}

    def build(control=None, key=None):
        if key is None:
            file = man.get("composition")
        elif key in (man.get("compositions") or {}):
            file = man["compositions"][key]
        else:
            raise ValueError(f"{eid}: composition {key!r} is not declared in the manifest")
        if not file:
            raise ValueError(f"{eid}: a composition run names no composition")
        path = (folder / file).resolve()
        if folder not in path.parents:
            raise ValueError(f"{eid}: composition file {file!r} is not inside the experiment folder")
        if control is not None:
            raise ValueError(f"{eid}: a variant board file declares no controls ({control!r})")
        if file not in cache:
            cache[file] = load_data(man, path.read_bytes())     # .engine (VariantEngine) and .initial
        return cache[file]
    return build


def replay_variant(engine, initial, steps, log_path: Path):
    """The variant runner on one run, in process: ``python -m research.coupling_variants_v1 --config <run>.variant.json
    --events <log> --output <run>.final.json --summary <run>.runner.json --audit`` (VariantEngine, exact inverse,
    local balance and signed-account identity at every update), the initial state written beside the log as a variant
    init file (never overwriting, reload-checked).  Returns ``replay``'s integrity data and the runner's summary."""
    from research.coupling_variants_v1 import read_checkpoint, write_init
    from research.coupling_variants_v1.__main__ import main as runner
    base = str(log_path)[:-len(".events.jsonl")] if str(log_path).endswith(".events.jsonl") else str(log_path)
    config, final, record = Path(base + ".variant.json"), Path(base + ".final.json"), Path(base + ".runner.json")
    write_init(config, engine.coupling, initial, steps)
    t0, err = time.time(), io.StringIO()
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            code = runner(["--config", str(config), "--events", str(log_path), "--output", str(final),
                           "--summary", str(record), "--audit"])
    except SystemExit as exc:                     # argparse refusals
        code = exc.code
    if code != 0:
        raise ArithmeticError(f"variant runner failed ({code}): {err.getvalue().strip()}")
    summary = json.loads(record.read_text(encoding="utf-8"))
    _, state, completed = read_checkpoint(final)
    if (summary.get("model"), summary.get("variant_fingerprint"), summary.get("audited"), completed) != \
            ("variant", engine.coupling.fingerprint, True, steps):
        raise ArithmeticError("the variant runner's summary is not an audited run of the model")
    return {"final_state_sha256": state_sha256(state), "log_sha256": sha256_bytes(log_path.read_bytes()),
            "clicks": summary["logged_arithmetic_events"], "seconds": round(time.time() - t0, 1),
            "side": initial.cube.side,
            "runner": {k: summary[k] for k in ("model", "coupling_label", "variant_fingerprint", "audited")}}


def _composition(eid, man):
    """``build(control=None, key=None)``: the prepared board of one composition of the experiment, the file that the
    manifest declares as ``compositions[key]`` (no key: the manifest's ``composition``), with one of its declared
    controls applied.  An undeclared key, a file outside the experiment folder or an undeclared control is refused;
    boards are cached per (file, control).  A variant manifest's board files are variant init files
    (``_variant_boards``)."""
    if (man.get("coupling") or {}).get("kind") == "variant":
        return _variant_boards(eid, man)
    from research.matter_light_blocks_v1.registry import apply_control, compose
    folder = (HERE / eid).resolve()
    specs, cache = {}, {}

    def build(control=None, key=None):
        if key is None:
            file = man.get("composition")
        elif key in (man.get("compositions") or {}):
            file = man["compositions"][key]
        else:
            raise ValueError(f"{eid}: composition {key!r} is not declared in the manifest")
        if not file:
            raise ValueError(f"{eid}: a composition run names no composition")
        path = (folder / file).resolve()
        if folder not in path.parents:
            raise ValueError(f"{eid}: composition file {file!r} is not inside the experiment folder")
        if file not in specs:
            specs[file] = json.loads(path.read_text(encoding="utf-8"))
        if (file, control) not in cache:
            spec = specs[file]
            if control is None:
                s = spec
            else:
                found = [c for c in spec.get("controls", []) if c["name"] == control]
                if len(found) != 1:
                    raise ValueError(f"{eid}: {file} declares {len(found)} controls named {control!r}")
                s = apply_control(spec, found[0])
            prepared, report = compose(s)
            bad = [k for k, v in report.items() if k.endswith("_ok") and v is False]
            if bad:
                raise ValueError(f"{eid}: composition assertions failed: {bad}")
            cache[(file, control)] = prepared
        return cache[(file, control)]
    return build


def rewind_preparation(engine, state, k):
    """The state ``k`` exact inverse steps before ``state``: a preparation before t = 0, not a stage of the forward run.
    Every step is checked by advancing it again."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError(f"rewind must be a non-negative integer, not {k!r}")
    for step in range(1, k + 1):
        earlier = engine.rewind(state)
        if engine.advance(earlier) != state:
            raise ArithmeticError(f"exact rewind failed at preparation step {step}")
        state = earlier
    return state


def load_run(eid, man, run, composition=None):
    """(engine, initial, steps, integrity notes) for one run; raises on any hash mismatch."""
    notes = {}
    engine = initial = None
    steps = run.get("steps")
    if "init" in run or "block" in run:
        if "init" in run:
            path = HERE / eid / run["init"]
            want = run["init_sha256"]
        else:
            path = ROOT / run["block_file"]
            want = run["block_file_sha256"]
            if not path.exists() and run.get("pending_append"):
                raise ValueError(f"{eid}/{run['name']}: block {run['block']} is not published yet (pending the blocks "
                                 f"append: {run['pending_append']})")
        blob = path.read_bytes()
        if sha256_bytes(blob) != want:
            raise ValueError(f"{eid}/{run['name']}: file hash differs ({path.name})")
        exp = load_data(man, blob)
        engine, initial = exp.engine, exp.initial
        if exp.steps != steps:
            raise ValueError(f"{eid}/{run['name']}: file horizon {exp.steps} != manifest steps {steps}")
        notes["file_sha256"] = "ok"
    if "from_composition" in run:
        fc = run["from_composition"]
        prepared = composition(fc.get("control"), fc.get("composition"))
        k = fc.get("rewind", 0)
        start = rewind_preparation(prepared.engine, prepared.initial, k)
        if initial is None:
            engine, initial = prepared.engine, start
        elif start != initial or prepared.engine.coupling.fingerprint != engine.coupling.fingerprint:
            raise ValueError(f"{eid}/{run['name']}: composition does not regenerate the run's initial state")
        notes["composition"] = ("variant board file loaded" if variant_model(man) else "regenerated") + \
            ": equal initial state and coupling" + (f" ({k} exact rewinds)" if k else "")
        if "init" not in run and "block" not in run and not run.get("initial_state_sha256"):
            raise ValueError(f"{eid}/{run['name']}: a run made only from a composition must record initial_state_sha256")
    if initial is None:
        raise ValueError(f"{eid}/{run['name']}: run has no initial data")
    if run.get("initial_state_sha256") and state_sha256(initial) != run["initial_state_sha256"]:
        raise ValueError(f"{eid}/{run['name']}: initial-state hash differs")
    model = variant_model(man)
    if model is not None:                      # an explicitly separate candidate variant: its table, never a reference
        from research.coupling_variants_v1 import VariantEngine
        table = engine.coupling
        if not isinstance(engine, VariantEngine) or not table.is_variant or (table.label, table.fingerprint) != model:
            raise ValueError(f"{eid}/{run['name']}: the run's table is not the manifest's {model[0]}")
        return engine, initial, steps, notes
    signs = list(engine.coupling.body_signs)
    if man["coupling"].get("kind") != "reference" or list(man["coupling"]["signs"]) != signs:
        raise ValueError(f"{eid}/{run['name']}: coupling {signs} differs from the manifest")
    return engine, initial, steps, notes


def replay(engine, initial, steps, log_path: Path):
    """Native run, exact inverse at every update; writes the official click log; returns integrity data."""
    state, n, t0 = initial, 0, time.time()
    with log_path.open("x", encoding="utf-8") as handle:
        for t in range(1, steps + 1):
            nxt = engine.advance(state)
            if engine.rewind(nxt) != state:
                raise ArithmeticError(f"exact inverse failed at update {t}")
            for event in clicks(state, nxt, t):
                handle.write(json.dumps(asdict(event), separators=(",", ":")) + "\n")
                n += 1
            state = nxt
    return {"final_state_sha256": state_sha256(state), "log_sha256": sha256_bytes(log_path.read_bytes()),
            "clicks": n, "seconds": round(time.time() - t0, 1), "side": initial.cube.side}


# ------------------------------------------------------------------------------------------------- decoder
def decoder_status(man):
    """('frozen', module) if the pinned decoder is the frozen one, else (reason, None)."""
    pin = man.get("decoder") or {}
    if not pin.get("code_sha256"):
        return "decoder pending (no frozen decoder pinned in this manifest)", None
    try:
        from research import click_decoder_v1 as dec
        from research.click_decoder_v1 import decoder as dmod
    except ImportError:
        return "decoder pending (click_decoder_v1 not installed)", None
    frozen = dmod.HERE / "FROZEN.json"
    if not frozen.exists():
        return "decoder pending (click_decoder_v1 is not frozen)", None
    fp = dmod.code_fingerprint()
    if fp != pin["code_sha256"] or fp != json.loads(frozen.read_text(encoding="utf-8"))["code_sha256"]:
        return "decoder changed: re-validate all experiments", None
    if dec.VERSION != pin.get("version"):
        return "decoder changed: re-validate all experiments", None
    return "frozen", dec


def projection(run, side):
    """A run's declared projection layer (decoder README, 'Projection layers'), checked: ``{"name": label, "keep":
    {axis: coordinate}}`` with axes among x, y, z and integer coordinates on the board, plus the run's
    ``layer_sha256``; None if the run declares none."""
    layer = run.get("layer")
    if layer is None:
        return None
    keep = layer.get("keep") if isinstance(layer, dict) else None
    if not isinstance(layer, dict) or set(layer) != {"name", "keep"} or not isinstance(layer["name"], str) \
            or not layer["name"] or not isinstance(keep, dict) or not keep or not set(keep) <= {"x", "y", "z"} \
            or not all(type(v) is int and 0 <= v < side for v in keep.values()):
        raise ValueError(f"{run['name']}: a projection layer is {{'name': label, 'keep': {{axis: coordinate}}}}, "
                         f"axes x, y, z, coordinates 0..{side - 1}")
    if not isinstance(run.get("layer_sha256"), str):
        raise ValueError(f"{run['name']}: a projection layer needs its layer_sha256")
    return layer


def project_layer(log_path: Path, keep: dict) -> Path:
    """The records of an official log whose address has the declared coordinates (``keep``, e.g. {"y": 0, "z": 0}),
    verbatim and in log order, streamed into ``<log>.layer.jsonl`` (never overwriting).  It reads the official record
    form, ``"address":[x,y,z,g]`` (compact JSON; the log's SHA-256 is checked first)."""
    want = [("xyz".index(k), v) for k, v in keep.items()]
    out = Path(str(log_path) + ".layer.jsonl")
    with Path(log_path).open(encoding="utf-8") as fi, out.open("x", encoding="utf-8") as fo:
        for line in fi:
            j = line.index('"address":[') + 11
            addr = line[j:line.index("]", j)].split(",")
            if all(int(addr[i]) == v for i, v in want):
                fo.write(line)
    return out


def decode_run(dec, log_path, side, steps, run, detectors):
    """Decoder report of one log, plus the declared probes: one ``correlations`` call per probe (its detector and
    window), stored under report['probes'][name] = the decoder's detector entry.  A run that declares a projection
    ``layer`` is decoded on that projection of its official log, whose SHA-256 must be the run's ``layer_sha256``."""
    layer = projection(run, side)
    if layer:
        log_path = project_layer(log_path, layer["keep"])
        if sha256_bytes(log_path.read_bytes()) != run["layer_sha256"]:
            raise ValueError(f"{run['name']}: projection layer hash differs")
    events, info = dec.read_log(log_path)
    if layer:
        info = dict(info, path=log_path.name)
    spec = (detectors or {}).get("decode") if run.get("decode_detectors") else None   # declared correlation spec
    report = dec.decode(events, side=side, horizon=steps, log_info=info, detectors=spec,
                        layer=layer["name"] if layer else "native")
    probes = {}
    for p in run.get("probes", []):
        det = detectors["detectors"][p["detector"]]
        lo, hi = p["window"]
        out = dec.correlations(events, {"detectors": {p["name"]: det}, "window": [lo, hi], "bin": hi - lo + 1},
                               steps, side)
        probes[p["name"]] = out["detectors"][p["name"]]
    if probes:
        report["probes"] = probes
    return report


# ------------------------------------------------------------------------------------------- decoder layers
def layer_status(man, name):
    """('frozen', module) if ``name`` is a released decoder layer: its ``FROZEN_<name>.json`` names the layer's file
    in click_decoder_v1, and that file has the record's SHA-256 and the manifest's pin ``layers[name]``; otherwise
    (reason, None), and every check of that layer reports the reason.  The module is imported only after the match."""
    if name not in LAYERS:
        return f"decoder layer pending ({name!r} is not a released layer)", None
    try:
        from research.click_decoder_v1 import decoder as dmod
    except ImportError:
        return "decoder layer pending (click_decoder_v1 not installed)", None
    frozen = dmod.HERE / f"FROZEN_{name}.json"
    record = json.loads(frozen.read_text(encoding="utf-8")) if frozen.exists() else {}
    file = str(record.get("file", ""))
    if record.get("name") != name or Path(file).name != file or not file.endswith(".py") \
            or not (dmod.HERE / file).exists():
        return f"decoder layer pending ({name} is not released)", None
    pin = (man.get("layers") or {}).get(name)
    if not pin:
        return f"decoder layer pending (the manifest does not pin {name})", None
    sha = sha256_bytes((dmod.HERE / file).read_bytes())
    if sha != record.get("sha256") or sha != pin:
        return "decoder layer changed: re-validate", None
    import importlib
    return "frozen", importlib.import_module(f"research.click_decoder_v1.{file[:-3]}")


def layer_args(args, detectors):
    """The keyword arguments of a layer call: ``{"detectors": pointer}`` stands for a value of detectors.json (for
    example a beat-clock declaration); other values are passed as they are.  An argument that would write files is
    refused."""
    out = {}
    for key, value in (args or {}).items():
        if key.startswith("write"):
            raise ValueError(f"layer argument {key!r} would write files")
        if isinstance(value, dict) and set(value) == {"detectors"}:
            value = pointer(detectors or {}, value["detectors"])
        out[key] = value
    return out


def layer_calls(check):
    """The calls of a layer check, each a tuple of the runs whose official logs it reads first, in order: a one-log
    call reads the check's ``run``, or each of its ``runs`` (one call per run); a call of n > 1 logs reads ``runs`` =
    [a, b, ...] of length n in one call.  None if the check does not name its runs so."""
    n, runs = LAYERS[check["layer"]][check["call"]], check.get("runs")
    if "run" in check:
        return [(check["run"],)] if n == 1 and runs is None else None
    if not isinstance(runs, list) or not runs or not all(isinstance(r, str) for r in runs):
        return None
    if n == 1:
        return [(r,) for r in runs]
    return [tuple(runs)] if len(runs) == n else None


def _layer_key(runs, check):
    return tuple(runs), check["layer"], check["call"], json.dumps(check.get("args"), sort_keys=True)


def layer_values(checks, lstat, logs, detectors):
    """{call key: result} for the layer checks whose layer is frozen and whose runs replayed (``logs``: run name ->
    official log path).  A result is the JSON form of the call's return value, or the exception the call raised."""
    out = {}
    for check in checks:
        mod = lstat[check["layer"]][1]
        if mod is None or check.get("call") not in LAYERS[check["layer"]]:
            continue
        for runs in layer_calls(check) or ():
            key = _layer_key(runs, check)
            if key in out or not set(runs) <= set(logs):
                continue
            try:
                value = getattr(mod, check["call"])(*[str(logs[r]) for r in runs],
                                                    **layer_args(check.get("args"), detectors))
                out[key] = json.loads(json.dumps(value))
            except (ValueError, ArithmeticError, OSError, KeyError, IndexError, TypeError) as exc:
                out[key] = exc
    return out


def layer_result(check, lstat, values, names, detectors):
    """(result, decoded value) of one layer check (``names``: the selected runs), from ``layer_values``."""
    status, mod = lstat[check["layer"]]
    if mod is None:
        return status, None
    calls = LAYERS[check["layer"]]
    if check.get("call") not in calls:
        return f"not decodable: {check['layer']} has no call {check.get('call')!r}", None
    shape = layer_calls(check)
    if shape is None:
        n = calls[check["call"]]
        return ("not decodable: " + (f"{check['call']} reads one log: name its run (or runs)" if n == 1 else
                                     f"{check['call']} reads {n} logs: name them as runs, in order")), None
    if "derive" in check:
        return "not decodable: derives read decoder reports only", None
    if not _needed(check) <= names:
        return "skipped (runs not selected)", None
    got = [values.get(_layer_key(runs, check)) for runs in shape]
    for value in got:
        if value is None:
            return "fail: run did not replay", None
        if isinstance(value, Exception):
            return f"fail: layer call failed ({value.__class__.__name__}: {value})", None
    if len(shape[0]) == 1:                                   # one result per run, read like decoder reports
        return evaluate(check, {runs[0]: value for runs, value in zip(shape, got)}, detectors, None)
    joint = "+".join(shape[0])                               # one result of several logs, read like one report
    one = {**{k: v for k, v in check.items() if k != "runs"}, "run": joint}
    return evaluate(one, {joint: got[0]}, detectors, None)


# ------------------------------------------------------------------------------------------------- checks
def pointer(doc, ptr: str):
    """RFC 6901 JSON Pointer; raises KeyError/IndexError if absent."""
    if ptr == "":
        return doc
    cur = doc
    for raw in ptr.lstrip("/").split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(token)] if isinstance(cur, list) else cur[token]
    return cur


def _canon(v):
    return json.dumps(v, sort_keys=True)


def _compare(op, target, value, tol=None):
    if op == "eq":
        return _canon(target) == _canon(value) or (isinstance(target, (int, float)) and isinstance(value, (int, float))
                                                   and target == value)
    if op == "ne":
        return _canon(target) != _canon(value)
    if op in ("lt", "le", "gt", "ge"):
        return {"lt": target < value, "le": target <= value, "gt": target > value, "ge": target >= value}[op]
    if op == "approx":
        return abs(target - value) <= tol
    if op == "not_approx":                # the complement of approx: |target - value| > tol
        return abs(target - value) > tol
    if op == "in":
        return any(_canon(target) == _canon(v) for v in value)
    if op == "len_eq":
        return len(target) == value
    if op == "len_ge":
        return len(target) >= value
    raise ValueError(op)


def station_fired(report, detectors, station) -> bool:
    """A station fires in a run iff the decoder reports >= 1 fired bin for any of its declared probes
    (``detectors.json`` 'stations' maps a station to probe names; each probe is one decoder ``correlations``
    call over its detector and window).  Reads decoder output only."""
    return any(report["probes"][p]["bins_fired"] > 0 for p in detectors["stations"][station])


RELABELLINGS = (("00", "01", "10", "11"), ("01", "00", "11", "10"), ("10", "11", "00", "01"), ("11", "10", "01", "00"))


def chsh_from_outcomes(outcomes, chsh):
    """Pure function.  ``outcomes``: {setting 'xy': [(a, b), ...]} with a, b = +-1, one pair per run (the runs of a
    setting are the declared values of the hidden variable, equal weights).  ``chsh``: the decoder's
    ``chsh(e_ab, e_ab', e_a'b, e_a'b')`` = E(a,b) - E(a,b') + E(a',b) + E(a',b').
    Returns E per setting, the marginals P(a=+1), P(b=+1) per setting, the four CHSH forms (the decoder's form under
    the four relabellings a <-> a', b <-> b' of the settings) and S = max |form|."""
    E, marg = {}, {}
    for setting, pairs in sorted(outcomes.items()):
        E[setting] = sum(a * b for a, b in pairs) / len(pairs)
        marg[setting] = [sum(a == 1 for a, _ in pairs) / len(pairs), sum(b == 1 for _, b in pairs) / len(pairs)]
    forms = [chsh(*(E[k] for k in r)) for r in RELABELLINGS]
    return {"E": E, "marginals": marg, "forms": forms, "S": max(abs(s) for s in forms),
            "marginals_all": sorted({v for pair in marg.values() for v in pair})}


def alpha_from_counts(N: int, N_A: int, N_B: int, N_AB: int):
    """Pure function: the Grangier-Roger-Aspect anticorrelation parameter alpha = N * N_AB / (N_A * N_B) of a
    declared family of N runs, from the decoder's per-run detector counts (N_A runs where A fired, N_B where B
    fired, N_AB where both fired).  alpha = 0: never both (exclusive); 1: independent; 2: always together when
    either fires.  None if N_A or N_B is 0 (undefined)."""
    if not (0 <= N_AB <= min(N_A, N_B) and max(N_A, N_B) <= N):
        raise ValueError("inconsistent counts")
    return {"N": N, "N_A": N_A, "N_B": N_B, "N_AB": N_AB, "alpha": (N * N_AB / (N_A * N_B)) if N_A and N_B else None}


# ---- pure derive functions proposed by r12 (WAVE 3); unit tests: r12/verifier_proposal/test_derive_proposal.py
TOL = 1e-12


def e_table(outcomes):
    """``outcomes``: {"thA,thB": [(a, b), ...]} with a, b = +-1, one pair per run (the declared hidden-variable values,
    equal weights). Returns E per setting pair, the marginals P(a=+1), P(b=+1), and the sorted set of marginal values."""
    E, marg = {}, {}
    for key, pairs in sorted(outcomes.items()):
        if not pairs:
            raise ValueError(f"no runs for setting {key}")
        E[key] = sum(a * b for a, b in pairs) / len(pairs)
        marg[key] = [sum(a == 1 for a, _ in pairs) / len(pairs), sum(b == 1 for _, b in pairs) / len(pairs)]
    return {"E": E, "marginals": marg, "marginals_all": sorted({v for m in marg.values() for v in m})}


def _matrix(E, N):
    return [[E[f"{i},{j}"] for j in range(N)] for i in range(N)]


def covariant_curve(E, N):
    """For a full N x N table of settings on Z_N (keys "thA,thB"): whether E depends only on Delta = thA - thB (mod N),
    the curve E(Delta), its discrete Fourier coefficients and their l1 norm (r12's criterion for covariant tables,
    program record), the agreement probabilities P(a = b | Delta) = (1 + E)/2, and the largest deviations from two
    reference curves (not claims): cos(2 pi Delta / N) and the triangle law 1 - 4 |Delta| / N (cyclic distance)."""
    m = _matrix(E, N)
    covariant = all(abs(m[i][j] - m[(i + 1) % N][(j + 1) % N]) <= TOL for i in range(N) for j in range(N))
    curve = [m[d % N][0] for d in range(N)]                    # E(Delta) with Delta = thA - thB
    coeff = [sum(curve[d] * cmath.exp(-2j * math.pi * k * d / N) for d in range(N)) / N for k in range(N)]
    cyc = [min(d, N - d) for d in range(N)]
    return {"covariant": covariant, "E_of_delta": curve,
            "fourier_abs": [round(abs(c), 12) for c in coeff], "fourier_l1": round(sum(abs(c) for c in coeff), 12),
            "P_same_of_delta": [(1 + e) / 2 for e in curve],
            "max_dev_from_cos": round(max(abs(curve[d] - math.cos(2 * math.pi * d / N)) for d in range(N)), 12),
            "max_dev_from_triangle": round(max(abs(curve[d] - (1 - 4 * cyc[d] / N)) for d in range(N)), 12)}


def best_chsh(E, N):
    """max over all N^4 setting quadruples (a0, a1, b0, b1) of |E(a0,b0) + E(a0,b1) + E(a1,b0) - E(a1,b1)| (this covers
    every relabelling); also the TLM value at the maximising quadruple."""
    m = _matrix(E, N)
    best, arg = -1.0, None
    for a0, a1, b0, b1 in product(range(N), repeat=4):
        s = abs(m[a0][b0] + m[a0][b1] + m[a1][b0] - m[a1][b1])
        if s > best + TOL:
            best, arg = s, (a0, a1, b0, b1)
    a0, a1, b0, b1 = arg
    return {"S_max": round(best, 12), "settings": list(arg),
            "TLM_at_best": tlm(m[a0][b0], m[a0][b1], m[a1][b0], m[a1][b1])["TLM"]}


def tlm(e00, e01, e10, e11):
    """Tsirelson-Landau-Masanes value for unbiased correlators: the largest of the four CHSH-type arcsine sums
    |asin E00 + asin E01 + asin E10 + asin E11 - 2 asin E_xy|. A quantum (and every local) box has TLM <= pi; the PR
    box has 2 pi."""
    s = [math.asin(max(-1.0, min(1.0, v))) for v in (e00, e01, e10, e11)]
    vals = [abs(sum(s) - 2 * s[i]) for i in range(4)]
    v = max(vals)
    return {"TLM": round(v, 12), "bound": round(math.pi, 12), "quantum_consistent": v <= math.pi + 1e-9}


def plane_spectrum(counts):
    """Discrete Fourier magnitudes of a list of per-plane click counts (a screen), and the fringe period: the
    smallest period p dividing the number of planes with counts[z + p] == counts[z] for all z."""
    n = len(counts)
    coeff = [abs(sum(counts[z] * cmath.exp(-2j * math.pi * k * z / n) for z in range(n))) / n for k in range(n)]
    period = next(p for p in range(1, n + 1) if n % p == 0 and all(counts[(z + p) % n] == counts[z] for z in range(n)))
    return {"fourier_abs": [round(c, 9) for c in coeff], "period": period,
            "dark_planes": [z for z in range(n) if counts[z] == 0]}


def derive(name, check, reports, detectors, dec):
    """The closed list of derived quantities: pure functions of decoder outputs (station outcomes from the
    decoder's ``correlations``; S through the decoder's own ``chsh``).  Setting keys: ``chsh`` uses "xy" (e.g. "01");
    ``e_table``, ``covariant_curve``, ``best_chsh`` and ``tlm`` use "thA,thB" (e.g. "0,1"); see README.md."""
    if name == "chsh":
        outcomes = {setting: [(1 if station_fired(reports[n], detectors, "A") else -1,
                               1 if station_fired(reports[n], detectors, "B") else -1) for n in names]
                    for setting, names in check["runs"].items()}
        return chsh_from_outcomes(outcomes, dec.chsh)
    if name in ("e_table", "covariant_curve", "best_chsh", "tlm"):
        outcomes = {setting: [(1 if station_fired(reports[n], detectors, "A") else -1,
                               1 if station_fired(reports[n], detectors, "B") else -1) for n in names]
                    for setting, names in check["runs"].items()}
        table = e_table(outcomes)
        if name == "e_table":
            return table
        if name == "tlm":
            E = table["E"]
            return tlm(E["0,0"], E["0,1"], E["1,0"], E["1,1"])
        return (covariant_curve if name == "covariant_curve" else best_chsh)(table["E"], int(check["N"]))
    if name == "plane_spectrum":
        return plane_spectrum([pointer(reports[check["run"]], p) for p in check["pointers"]])
    if name == "alpha":
        names = check["runs"]
        fa = [station_fired(reports[n], detectors, "A") for n in names]
        fb = [station_fired(reports[n], detectors, "B") for n in names]
        return alpha_from_counts(len(names), sum(fa), sum(fb), sum(a and b for a, b in zip(fa, fb)))
    raise ValueError(name)


def evaluate(check, reports, detectors, dec):
    """'pass' / 'fail' / 'not decodable: ...' for one declared check."""
    if check.get("not_decodable"):
        return "not decodable: " + check["not_decodable"], None
    op = check["op"]
    if op not in OPS:
        return f"not decodable: unknown op {op}", None
    try:
        if "derive" in check:
            if check["derive"] not in DERIVE:
                return f"not decodable: unknown derive {check['derive']}", None
            target = pointer(derive(check["derive"], check, reports, detectors, dec), check["pointer"])
        elif "pointers" in check:
            target = [pointer(reports[check["run"]], p) for p in check["pointers"]]
        elif "runs" in check:
            target = [pointer(reports[r], check["pointer"]) for r in check["runs"]]
        else:
            target = pointer(reports[check["run"]], check["pointer"])
    except (KeyError, IndexError, TypeError) as exc:
        return f"fail: pointer not found ({exc.__class__.__name__}: {exc})", None
    if op == "same":
        ok = len({_canon(t) for t in target}) == 1
    elif op == "diff":                   # two report values: target[1] - target[0] == value (signed)
        if not isinstance(target, list) or len(target) != 2:
            return "not decodable: diff needs exactly two pointers or runs", target
        ok = target[1] - target[0] == check.get("value")
    else:
        ok = _compare(op, target, check.get("value"), check.get("tol"))
    return ("pass" if ok else "fail"), target


# ---------------------------------------------------------------------------------------------------- main
def _needed(check):
    """Names of the runs a check reads."""
    needed = {check["run"]} if "run" in check else set()
    if isinstance(check.get("runs"), list):
        needed |= set(check["runs"])
    elif isinstance(check.get("runs"), dict):
        needed |= {n for names_ in check["runs"].values() for n in names_}
    return needed


def verify(eid, fast=False, keep=None):
    man = manifest(eid)
    detectors = json.loads((HERE / eid / man["detectors"]).read_text(encoding="utf-8")) if man.get("detectors") else None
    composition = _composition(eid, man) if _uses_composition(man) else None
    status, dec = decoder_status(man)
    out = {"id": eid, "runs": [], "checks": [], "decoder": status, "ok": True}
    reports = {}
    selected = [r for r in man["runs"] if r.get("fast") or not fast]
    live = [c for c in man["checks"] if not c.get("not_decodable")]
    wanted = set().union(set(), *[_needed(c) for c in live if "layer" not in c])       # runs the decoder must read
    layer_checks = [c for c in live if "layer" in c]
    lstat = {name: layer_status(man, name) for name in sorted({c["layer"] for c in layer_checks})}
    logs, values = {}, {}
    variant = (man.get("coupling") or {}).get("kind") == "variant"     # its runs replay through the variant runner
    if variant:
        out["coupling"] = man["coupling"]
    with tempfile.TemporaryDirectory() as tmp:
        logdir = Path(keep) / eid if keep else Path(tmp)
        logdir.mkdir(parents=True, exist_ok=True)
        for run in selected:
            row = {"name": run["name"], "role": run["role"]}
            try:
                engine, initial, steps, notes = load_run(eid, man, run, composition)
                log = logdir / f"{run['name']}.events.jsonl"
                got = (replay_variant if variant else replay)(engine, initial, steps, log)
                row.update(notes)
                row.update({k: got[k] for k in ("clicks", "seconds")})
                if variant:
                    row["runner"] = got["runner"]
                row["final_state"] = "ok" if got["final_state_sha256"] == run["final_state_sha256"] else "DIFFERS"
                row["log"] = "ok" if got["log_sha256"] == run["log_sha256"] else "DIFFERS"
                if row["final_state"] != "ok" or row["log"] != "ok":
                    out["ok"] = False
                logs[run["name"]] = log
                if dec is not None and run["name"] in wanted:      # only runs that a decodable check reads
                    reports[run["name"]] = decode_run(dec, log, got["side"], steps, run, detectors)
                    if keep:
                        path = logdir / f"{run['name']}.report.json"
                        with path.open("x", encoding="utf-8") as handle:
                            json.dump(reports[run["name"]], handle, indent=1, sort_keys=True)
            except (ValueError, ArithmeticError, OSError) as exc:
                row["error"] = f"{exc.__class__.__name__}: {exc}"
                out["ok"] = False
            out["runs"].append(row)
        values = layer_values(layer_checks, lstat, logs, detectors)     # while the official logs exist
    names = {r["name"] for r in selected}
    for check in man["checks"]:
        needed = _needed(check)
        row = {"claim": check["claim"], "text": check["text"]}
        if "layer" in check:
            row["layer"], row["call"] = check["layer"], check.get("call")
        if check.get("not_decodable"):
            row["result"] = "not decodable: " + check["not_decodable"]
        elif "layer" in check:
            row["result"], target = layer_result(check, lstat, values, names, detectors)
            if row["result"].split(":")[0] in ("pass", "fail"):
                row["decoded"] = target
            if row["result"].startswith("fail"):
                out["ok"] = False
        elif dec is None:
            row["result"] = status
        elif not needed <= names:
            row["result"] = "skipped (runs not selected)"
        elif any(n not in reports for n in needed):
            row["result"] = "fail: run did not replay"
            out["ok"] = False
        else:
            row["result"], target = evaluate(check, reports, detectors, dec)
            row["decoded"] = target
            if row["result"].startswith("fail"):
                out["ok"] = False
        out["checks"].append(row)
    out["summary"] = {k: sum(1 for c in out["checks"] if c["result"].startswith(k))
                      for k in ("pass", "fail", "not decodable", "decoder", "skipped")}
    if lstat:
        out["layers"] = {name: status_ for name, (status_, _) in lstat.items()}
    out["ready"] = out["ok"] and dec is not None and out["summary"]["pass"] == len(man["checks"]) \
        and man.get("verdict", {}).get("result") in ("CONFIRMED", "PARTLY")
    return out


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m research.matter_light_experiments_v1.verify", allow_abbrev=False,
        description="Replay the curated experiments natively with the exact inverse and evaluate every declared check "
                    "on the frozen click decoder's report; prints one JSON report.",
        epilog="Exit status: 0 if every selected experiment is ok, 1 if an integrity step or an evaluable check fails "
               "or an experiment is unknown, 2 for a usage error.")
    p.add_argument("ids", nargs="*", metavar="EXPERIMENT",
                   help="experiment folders to verify (default: every experiment folder present)")
    p.add_argument("--all", action="store_true", help="every experiment folder present (the default without names)")
    p.add_argument("--fast", action="store_true",
                   help="replay only the runs marked fast; checks that read other runs are skipped, so an experiment "
                        "with slower runs is not ready")
    p.add_argument("--keep", metavar="DIR",
                   help="keep the click logs and decoder reports under DIR/<id>, never overwriting")
    return p


def main(argv=None) -> int:
    args = _parser().parse_args(sys.argv[1:] if argv is None else argv)
    unknown = sorted(set(args.ids) - set(experiment_ids()))
    if unknown:
        raise SystemExit(f"unknown experiment(s): {unknown}")
    keep = args.keep
    ids = args.ids or experiment_ids()
    results = [verify(eid, fast=args.fast, keep=keep) for eid in ids]
    print(json.dumps({"experiments": results, "ok": all(r["ok"] for r in results)}, indent=1, default=str))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
