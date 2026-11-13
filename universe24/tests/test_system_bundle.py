"""Adversarial input and complete-state checks for the supported execution boundary."""
import gzip
from dataclasses import replace
import hashlib
import json
import sys
from pathlib import Path
import tempfile
import unittest

from universe24.core.engine import Engine, State
from universe24.core.tensor import GearType, Tensor
from universe24.system.decoder import default_protocol
from universe24.system.bundle import (
    BundleError, canonical_bytes, create_bundle, load_bundle, read_json,
    save_bundle, state_from_data, tensor_from_data, validate_bundle,
)


def fixture(channels=48):
    tensor = Tensor([f"q{i}" for i in range(channels)],
                    [(i, 3, [(i, (0, 0, 0), "b")]) for i in range(channels)])
    a = [[(-1 if n % 2 else 1) * (2 ** 100 + n) for n in range(27)] for _ in range(channels)]
    b = [[n - 10 for n in range(27)] for _ in range(channels)]
    r = [[n % 6 for n in range(27)] for _ in range(channels)]
    seed = State(3, a, b, r)
    owners = [{"index": i, "name": g.name, "label": g.label,
               "owner": "test-fixture", "purpose": "mechanical test only"}
              for i, g in enumerate(tensor.gears)]
    return tensor, seed, owners


def bundle_fixture(channels=48):
    tensor, seed, owners = fixture(channels)
    return create_bundle(tensor, seed, channels=owners,
                         protocol=default_protocol(),
                         model={"id": "test", "version": "1", "domain": "mechanical fixture"})


class BundleTests(unittest.TestCase):
    def test_decimal_integers_beyond_interpreter_digit_limit_roundtrip(self):
        limit = sys.get_int_max_str_digits()
        huge = 2 ** 20000
        _, seed, owners = fixture()
        tensor = Tensor([f"q{i}" for i in range(48)],
                        [(i, huge, [(i, (0, 0, 0), "b")]) for i in range(48)])
        seed.a = seed.a.astype(object)
        seed.b = seed.b.astype(object)
        seed.a[0, 0], seed.b[1, 1] = -huge, huge + 1
        bundle = create_bundle(tensor, seed, channels=owners, protocol=default_protocol(),
                               model={"id": "huge", "version": "1", "domain": "mechanical fixture"})
        with tempfile.TemporaryDirectory() as tmp:
            path = save_bundle(bundle, Path(tmp) / "bundle")
            restored = load_bundle(path)
        self.assertTrue(restored.seed.same_as(seed))
        self.assertEqual(restored.tensor.monomials[0].coeff, huge)
        self.assertEqual(restored.bundle_id, bundle.bundle_id)
        engine = Engine(restored.tensor)
        self.assertTrue(engine.inverse_step(engine.step(restored.seed)).same_as(seed))
        self.assertEqual(sys.get_int_max_str_digits(), limit)

    def test_complete_deterministic_roundtrip_and_rewind(self):
        bundle = bundle_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first", Path(tmp) / "second"
            save_bundle(bundle, first)
            save_bundle(bundle, second)
            for file in first.iterdir():
                self.assertEqual(file.read_bytes(), (second / file.name).read_bytes())
            restored = load_bundle(first)
        self.assertEqual(restored.bundle_id, bundle.bundle_id)
        self.assertEqual(restored.tensor, bundle.tensor)
        self.assertTrue(restored.seed.same_as(bundle.seed))
        engine = Engine(restored.tensor)
        final = engine.run(restored.seed, 4)
        self.assertTrue(engine.rewind(final, 4).same_as(bundle.seed))
        self.assertEqual(set(bundle.seed.r.ravel()), set(range(6)))

    def test_all_retained_channels_need_owner(self):
        tensor, seed, owners = fixture()
        for invalid in (owners[:1], [owners[0], owners[0], *owners[2:]],
                        [owners[0], dict(owners[1], owner=""), *owners[2:]]):
            with self.subTest(invalid=invalid), self.assertRaises(BundleError):
                create_bundle(tensor, seed, channels=invalid, protocol=default_protocol(),
                              model={"id": "t", "version": "1", "domain": "test"})

    def test_reject_strict_physical_edge_violation(self):
        # Storage reads remain neighboring; the target's link endpoint creates a third node.
        tensor = Tensor([GearType("link", link=0)] + [f"q{i}" for i in range(1, 48)],
                        [("link", 1, [("link", (1, 0, 0), "b")])])
        _, seed, owners = fixture()
        owners[0]["name"] = "link"
        with self.assertRaisesRegex(BundleError, "strict_support"):
            create_bundle(tensor, seed, channels=owners, protocol=default_protocol(),
                          model={"id": "t", "version": "1", "domain": "test"})

    def test_reject_seed_shape_or_bad_remainder(self):
        bundle = bundle_fixture()
        for seed in (fixture(1)[1], State(3, bundle.seed.a, bundle.seed.b, [[6] * 27] * 48)):
            with self.assertRaises(BundleError):
                create_bundle(bundle.tensor, seed, channels=bundle.channels,
                              protocol=bundle.protocol, model=bundle.model)

    def test_snapshot_does_not_alias_mutable_inputs_or_outputs(self):
        tensor, seed, owners = fixture()
        original = seed.copy()
        protocol = default_protocol()
        bundle = create_bundle(tensor, seed, channels=owners, protocol=protocol,
                               model={"id": "t", "version": "1", "domain": "test"})
        identity = bundle.bundle_id
        seed.a[0, 0] = 0
        owners[0]["owner"] = "changed"
        protocol["version"] = "changed"
        bundle.seed.r[0, 0] = 5
        bundle.protocol["version"] = "other"
        self.assertTrue(bundle.seed.same_as(original))
        self.assertEqual(bundle.bundle_id, identity)

    def test_raw_seed_rejects_bool_float_and_hidden_state(self):
        source = bundle_fixture().seed.to_dict()
        for value in (True, 1.0):
            invalid = json.loads(json.dumps(source))
            invalid["a"][0][0] = value
            with self.assertRaises((ValueError, TypeError)):
                state_from_data(invalid)
        with self.assertRaises(BundleError):
            state_from_data(dict(source, hidden_clock=1))

    def test_validate_rechecks_mutated_raw_state(self):
        tensor, seed, owners = fixture()
        seed.a = seed.a.astype(object)
        seed.a[0, 0] = 2.5
        with self.assertRaises(BundleError):
            create_bundle(tensor, seed, channels=owners, protocol=default_protocol(),
                          model={"id": "t", "version": "1", "domain": "test"})

    def test_direct_dataclass_cannot_hide_seed_data(self):
        bundle = bundle_fixture()
        forged = replace(bundle, _seed_bytes=canonical_bytes(dict(bundle.seed.to_dict(), scratch=7)))
        with self.assertRaises(BundleError):
            validate_bundle(forged)

    def test_raw_tensor_cannot_hide_or_reinterpret_fields(self):
        data = bundle_fixture().tensor.to_dict()
        for invalid in (dict(data, hidden_clock=1), dict(data, format="metric_variant_v1/tensor/1", Q=1)):
            with self.assertRaises(BundleError):
                tensor_from_data(invalid)

    def test_reject_tamper_missing_file_and_manifest_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            for kind in ("tensor", "missing", "budget", "schema", "old-schema", "bool-divisor"):
                path = Path(tmp) / kind
                save_bundle(bundle_fixture(), path)
                if kind == "tensor":
                    (path / "tensor.json").write_text("{}")
                elif kind == "missing":
                    (path / "seed.json.gz").unlink()
                else:
                    manifest = read_json(path / "bundle.json")
                    if kind == "budget":
                        manifest["channel_count"] = 47
                    elif kind == "schema":
                        manifest["format"] = "universe24/system-bundle/99"
                    elif kind == "old-schema":
                        manifest["format"] = "universe24/system-bundle/2"
                    else:
                        manifest["law"]["strict_face_support"] = 1
                    (path / "bundle.json").write_bytes(canonical_bytes(manifest))
                with self.subTest(kind=kind), self.assertRaises(BundleError):
                    load_bundle(path)

    def test_rehashed_invalid_seed_still_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = save_bundle(bundle_fixture(), Path(tmp) / "bundle")
            seed = bundle_fixture().seed.to_dict()
            seed["r"][1][2] = -1
            encoded = gzip.compress(canonical_bytes(seed), mtime=0)
            (path / "seed.json.gz").write_bytes(encoded)
            manifest = read_json(path / "bundle.json")
            manifest["files"]["seed.json.gz"] = hashlib.sha256(encoded).hexdigest()
            (path / "bundle.json").write_bytes(canonical_bytes(manifest))
            with self.assertRaisesRegex(BundleError, "remainder"):
                load_bundle(path)

    def test_duplicate_keys_float_and_nan_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.json"
            for raw in ('{"x":1,"x":2}', '{"x":1.5}', '{"x":NaN}'):
                path.write_text(raw)
                with self.subTest(raw=raw), self.assertRaises(BundleError):
                    read_json(path)

    def test_unknown_protocol_and_calibration_rejected(self):
        bundle = bundle_fixture()
        for protocol in ({"version": "99"}, dict(default_protocol(), calibration="1/3")):
            with self.subTest(protocol=protocol), self.assertRaises(BundleError):
                create_bundle(bundle.tensor, bundle.seed, channels=bundle.channels,
                              protocol=protocol, model=bundle.model)

    def test_refuse_overwrite_and_symlink_member(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = save_bundle(bundle_fixture(), Path(tmp) / "bundle")
            with self.assertRaises(FileExistsError):
                save_bundle(bundle_fixture(), path)
            original = path / "tensor.json"
            original.rename(path / "other.json")
            original.symlink_to("other.json")
            with self.assertRaisesRegex(BundleError, "symlink"):
                load_bundle(path)


if __name__ == "__main__":
    unittest.main()
