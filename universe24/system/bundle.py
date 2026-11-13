"""Versioned, complete input for the single supported Rule3 execution path.

This boundary certifies mechanical admissibility, not Einstein/Born physics.
Every prepared bundle has exactly 48 complete (a,b,r) channels.
Model and protocol metadata are passive data; neither can inject an update.
"""
from __future__ import annotations

from dataclasses import dataclass
import gzip
import hashlib
import io
from pathlib import Path
import shutil
import tempfile

from universe24.core.engine import State
from universe24.core import exact_json
from universe24.core.tensor import FORMAT as TENSOR_FORMAT, Tensor
from universe24.core.symmetry import CONTRACT, require_equivariant
from universe24.system.decoder import validate_protocol

FORMAT = "universe24/system-bundle/2"
MAX_CHANNELS = 48
_FILES = ("tensor.json", "seed.json.gz", "channels.json", "protocol.json", "model.json")


class BundleError(ValueError):
    """An input does not satisfy the supported system contract."""


def pad_tensor(tensor: Tensor) -> Tensor:
    """Embed a preparation in 48 channels; append disconnected zero-input gears."""
    if not 1 <= tensor.G <= MAX_CHANNELS:
        raise BundleError(f"at most {MAX_CHANNELS} source channels; got {tensor.G}")
    data = tensor.to_dict()
    names = set(tensor.names)
    for index in range(tensor.G, MAX_CHANNELS):
        name = f"__idle_{index:02d}"
        while name in names:
            name += "_"
        names.add(name)
        data["gears"].append(dict(name=name, label="audit", link=None, sign=1, sign_why=""))
    return Tensor.from_dict(data, strict_support=True)


def pad_state(seed: State) -> State:
    """Append (0,0,0) channels without changing any original integer."""
    if not 1 <= seed.G <= MAX_CHANNELS:
        raise BundleError(f"at most {MAX_CHANNELS} source channels; got {seed.G}")
    checked = State(seed.L, seed.a, seed.b, seed.r)
    data = checked.to_dict()
    for bank in ("a", "b", "r"):
        data[bank].extend([[0] * seed.N for _ in range(MAX_CHANNELS - seed.G)])
    return State.from_dict(data)


def require_48_channels(tensor: Tensor, seed: State) -> None:
    """Fail loudly at execution/load boundaries; never repair a sealed input."""
    if tensor.G != MAX_CHANNELS or seed.G != MAX_CHANNELS:
        raise BundleError(f"exactly 48 channels required: tensor={tensor.G}, seed={seed.G}; "
                          "prepare a new bundle to add idle channels")


def _exact_json(value, path="metadata"):
    if value is None or type(value) in (str, int, bool):
        return
    if type(value) in (list, tuple):
        for i, item in enumerate(value):
            _exact_json(item, f"{path}[{i}]")
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for key, item in value.items():
            _exact_json(item, f"{path}.{key}")
        return
    raise BundleError(f"{path}: only exact JSON data is supported (encode ratios as strings)")


def canonical_bytes(value) -> bytes:
    """Stable UTF-8 JSON; float values, non-string keys and executable objects fail."""
    _exact_json(value)
    return exact_json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _compress(data: bytes) -> bytes:
    # GzipFile fixes OS=255 across Python/zlib versions (gzip.compress on 3.11
    # can delegate mtime=0 to zlib and emit a platform-dependent header).
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", filename="", mtime=0) as output:
        output.write(data)
    return stream.getvalue()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BundleError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _read_json(data: bytes):
    try:
        value = exact_json.loads(data, object_pairs_hook=_pairs)
        _exact_json(value)
        return value
    except (UnicodeError, ValueError) as exc:
        raise BundleError(f"invalid JSON: {exc}") from exc


def read_json(path):
    """Read exact JSON without duplicate keys, floats, NaN or implicit coercions."""
    return _read_json(Path(path).read_bytes())


def state_from_data(data) -> State:
    """Parse a complete raw seed without accepting hidden or omitted fields."""
    if type(data) is not dict or set(data) != {"L", "a", "b", "r"}:
        raise BundleError("seed must contain exactly L and every a,b,r array")
    return State.from_dict(data)


def tensor_from_data(data) -> Tensor:
    """Require canonical current-law data; reject extra fields or legacy formats."""
    if type(data) is not dict or data.get("format") != TENSOR_FORMAT:
        raise BundleError("only the current fixed-six tensor schema is supported")
    tensor = Tensor.from_dict(data, strict_support=True)
    if canonical_bytes(tensor.to_dict()) != canonical_bytes(data):
        raise BundleError("tensor must use its exact canonical schema")
    return tensor


def _text(value, context):
    if type(value) is not str or not value.strip():
        raise BundleError(f"{context} must be a nonempty string")


def _check_metadata(tensor, channels, protocol, model):
    if type(channels) not in (list, tuple) or len(channels) != tensor.G:
        raise BundleError("channels must account for every retained tensor channel exactly once")
    required = {"index", "name", "owner", "purpose", "label"}
    for index, channel in enumerate(channels):
        if type(channel) is not dict or not required <= set(channel):
            raise BundleError(f"channel {index} needs {sorted(required)}")
        if type(channel["index"]) is not int or channel["index"] != index:
            raise BundleError("channel indices must be ordered, unique and contiguous")
        if channel["name"] != tensor.names[index] or channel["label"] != tensor.labels[index]:
            raise BundleError(f"channel {index} name/label does not match tensor")
        _text(channel["owner"], f"channel {index} owner")
        _text(channel["purpose"], f"channel {index} purpose")
        dependencies = channel.get("readout_dependencies", [])
        if type(dependencies) is not list or any(d not in tensor.names for d in dependencies):
            raise BundleError(f"channel {index} has an unknown readout dependency")
    if type(protocol) is not dict:
        raise BundleError("protocol must be a mapping")
    try:
        validate_protocol(protocol)
    except ValueError as exc:
        raise BundleError(str(exc)) from exc
    if type(model) is not dict:
        raise BundleError("model must be a mapping")
    for key in ("id", "version", "domain"):
        _text(model.get(key), f"model.{key}")
    for name, value in (("channels", channels), ("protocol", protocol), ("model", model)):
        _exact_json(value, name)


def model_contract(tensor: Tensor, model: dict) -> dict:
    """A candidate must certify the declared action; unclassified inputs are research.

This static declaration selects no engine or evolution rule. It cannot grant
physical acceptance. The model file is already part of the sealed input hash.
"""
    role = model.get("role", "research")
    if role not in ("research", "universe-candidate"):
        raise BundleError("model.role must be research or universe-candidate")
    symmetry = model.get("symmetry")
    if symmetry is not None and symmetry != CONTRACT:
        raise BundleError(f"unsupported model.symmetry; expected {CONTRACT}")
    if role == "universe-candidate" and symmetry != CONTRACT:
        raise BundleError(f"universe-candidate requires model.symmetry={CONTRACT}")
    if symmetry is not None:
        try:
            require_equivariant(tensor)
        except ValueError as exc:
            raise BundleError(str(exc)) from exc
    return {"role": role, "symmetry": symmetry,
            "status": "passed" if symmetry else "not_declared"}


@dataclass(frozen=True)
class SystemBundle:
    """Immutable serialized inputs; mutable readouts are returned as independent copies.

    Construct with :func:`create_bundle`; save/run paths revalidate all inputs.
    Hashes establish content identity and corruption detection, not authorship.
    """

    tensor: Tensor
    _seed_bytes: bytes
    _channels_bytes: bytes
    _protocol_bytes: bytes
    _model_bytes: bytes

    @property
    def seed(self) -> State:
        return state_from_data(_read_json(self._seed_bytes))

    @property
    def channels(self) -> tuple[dict, ...]:
        return tuple(_read_json(self._channels_bytes))

    @property
    def protocol(self) -> dict:
        return _read_json(self._protocol_bytes)

    @property
    def model(self) -> dict:
        return _read_json(self._model_bytes)

    @property
    def model_contract(self) -> dict:
        return model_contract(self.tensor, self.model)

    def _files(self) -> dict[str, bytes]:
        return {
            "tensor.json": canonical_bytes(self.tensor.to_dict()),
            "seed.json.gz": _compress(self._seed_bytes),
            "channels.json": self._channels_bytes,
            "protocol.json": self._protocol_bytes,
            "model.json": self._model_bytes,
        }

    @property
    def manifest(self) -> dict:
        return {
            "format": FORMAT,
            "channel_count": self.tensor.G,
            "retained_integers_per_node": 3 * self.tensor.G,
            "lattice": {"kind": "periodic-cube", "L": self.seed.L},
            "law": {"divisor": 6, "max_degree": 3, "strict_face_support": True},
            "tensor_hash": self.tensor.fingerprint,
            "inverse_stages": [list(stage) for stage in self.tensor.stages],
            "files": {name: _digest(data) for name, data in self._files().items()},
        }

    @property
    def bundle_id(self) -> str:
        return _digest(canonical_bytes(self.manifest))


def create_bundle(tensor: Tensor, seed: State, *, channels, protocol, model) -> SystemBundle:
    """Validate source data, append idle channels to 48 and detach caller mutation."""
    if not isinstance(tensor, Tensor) or not isinstance(seed, State):
        raise BundleError("tensor and seed must be Tensor and State instances")
    if not 1 <= tensor.G <= MAX_CHANNELS:
        raise BundleError(f"at most {MAX_CHANNELS} total retained channels per node; got {tensor.G}")
    try:
        tensor = Tensor.from_dict(tensor.to_dict(), strict_support=True)
        # Revalidate raw arrays, rather than coercing them through State.to_dict().
        seed = State(seed.L, seed.a.copy(), seed.b.copy(), seed.r.copy())
    except (TypeError, ValueError) as exc:
        raise BundleError(str(exc)) from exc
    if seed.G != tensor.G:
        raise BundleError("complete seed channel count differs from tensor")
    if bool((seed.r < 0).any()) or bool((seed.r >= 6).any()):
        raise BundleError("every retained remainder must be an integer in 0..5")
    _check_metadata(tensor, channels, protocol, model)
    model_contract(tensor, model)
    source_count = tensor.G
    tensor, seed = pad_tensor(tensor), pad_state(seed)
    channels = list(channels) + [
        dict(index=i, name=tensor.names[i], label="audit", owner="system-padding",
             purpose="Disconnected zero-initialized idle channel; full (a,b,r) retained")
        for i in range(source_count, MAX_CHANNELS)
    ]
    require_48_channels(tensor, seed)
    return SystemBundle(tensor, canonical_bytes(seed.to_dict()), canonical_bytes(channels),
                        canonical_bytes(protocol), canonical_bytes(model))


def validate_bundle(bundle: SystemBundle) -> SystemBundle:
    """Revalidate even a directly constructed dataclass before trusting its certificate."""
    if not isinstance(bundle, SystemBundle):
        raise BundleError("expected a SystemBundle")
    require_48_channels(bundle.tensor, bundle.seed)
    return create_bundle(bundle.tensor, bundle.seed, channels=bundle.channels,
                         protocol=bundle.protocol, model=bundle.model)


def save_bundle(bundle: SystemBundle, path) -> Path:
    """Write a complete directory atomically; never overwrite an existing nonempty run."""
    bundle = validate_bundle(bundle)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise FileExistsError(f"refusing to overwrite {path}")
    temporary = Path(tempfile.mkdtemp(prefix=f".{path.name}-", dir=path.parent))
    try:
        for name, data in bundle._files().items():
            (temporary / name).write_bytes(data)
        (temporary / "bundle.json").write_bytes(canonical_bytes(bundle.manifest))
        temporary.replace(path)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return path


def load_bundle(path) -> SystemBundle:
    """Check declared bytes, schema and independently recomputed mechanical certificate."""
    path = Path(path)
    try:
        for name in ("bundle.json", *_FILES):
            if (path / name).is_symlink():
                raise BundleError(f"bundle member {name} must not be a symlink")
        manifest = _read_json((path / "bundle.json").read_bytes())
        if type(manifest) is not dict or manifest.get("format") != FORMAT:
            raise BundleError("unsupported bundle format")
        hashes = manifest.get("files")
        if type(hashes) is not dict or set(hashes) != set(_FILES):
            raise BundleError("manifest must identify exactly the five complete input files")
        files = {}
        for name in _FILES:
            data = (path / name).read_bytes()
            if hashes[name] != _digest(data):
                raise BundleError(f"hash mismatch for {name}")
            files[name] = data
        tensor_data = _read_json(files["tensor.json"])
        tensor = tensor_from_data(tensor_data)
        seed_data = _read_json(gzip.decompress(files["seed.json.gz"]))
        seed = state_from_data(seed_data)
        require_48_channels(tensor, seed)
        bundle = create_bundle(tensor, seed,
                               channels=_read_json(files["channels.json"]),
                               protocol=_read_json(files["protocol.json"]),
                               model=_read_json(files["model.json"]))
        if canonical_bytes(manifest) != canonical_bytes(bundle.manifest):
            raise BundleError("manifest certificate differs from validated inputs")
        return bundle
    except BundleError:
        raise
    except (OSError, EOFError, TypeError, ValueError, KeyError) as exc:
        raise BundleError(f"invalid or incomplete bundle: {exc}") from exc
