"""Fail on any supported allocation other than 48 explicit complete channels."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from universe24.core import Engine, State, Tensor
from universe24.system.bundle import (
    BundleError, canonical_bytes, create_bundle, load_bundle, save_bundle, validate_bundle,
)
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.system_smoke import scalar_step


def source(count):
    names = [f"g{i}" for i in range(count)]
    tensor = Tensor(names, [(i, 3, [(i, (0, 0, 0), "b")]) for i in range(count)])
    seed = State(3, [[n-13+i for n in range(27)] for i in range(count)],
                 [[n*n-7-i for n in range(27)] for i in range(count)],
                 [[(n+i) % 6 for n in range(27)] for i in range(count)])
    owners = [dict(index=i, name=g.name, label=g.label, owner="fixture", purpose="test")
              for i, g in enumerate(tensor.gears)]
    return tensor, seed, owners


def prepared(count=48):
    tensor, seed, owners = source(count)
    return create_bundle(tensor, seed, channels=owners, protocol=default_protocol(),
                         model=dict(id="allocation-test", version="1", domain="mechanical"))


class Exactly48Tests(unittest.TestCase):
    def test_every_incomplete_allocation_and_49_are_rejected(self):
        for count in (*range(1, 48), 49):
            with self.subTest(count=count), self.assertRaisesRegex(BundleError, "exactly 48"):
                prepared(count)

    def test_all_144_registers_preserve_scalar_dynamics_carries_and_inverse(self):
        bundle = prepared()
        self.assertEqual(bundle.tensor.G, 48)
        self.assertEqual(bundle.seed.G, 48)
        self.assertEqual(len(bundle.channels), 48)
        self.assertEqual(bundle.manifest['retained_integers_per_node'], 144)
        self.assertEqual(validate_bundle(bundle).bundle_id, bundle.bundle_id)
        current = expected = bundle.seed
        engine = Engine(bundle.tensor)
        for _ in range(3):
            current = engine.step(current)
            expected = scalar_step(bundle.tensor, expected)
            self.assertTrue(current.same_as(expected))
        self.assertTrue(engine.rewind(current, 3).same_as(bundle.seed))

    def test_incomplete_sealed_input_is_rejected_before_output(self):
        tensor, seed, owners = source(2)
        forged = replace(prepared(), tensor=tensor, _seed_bytes=canonical_bytes(seed.to_dict()),
                         _channels_bytes=canonical_bytes(owners))
        with tempfile.TemporaryDirectory() as tmp:
            for operation in (validate_bundle, lambda b: save_bundle(b, Path(tmp)/'bundle'),
                              lambda b: run_bundle(b, Path(tmp)/'run', 1)):
                with self.assertRaisesRegex(BundleError, 'exactly 48'):
                    operation(forged)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_saved_run_retains_and_replays_all_144_registers_per_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_bundle(prepared(), Path(tmp)/'run', 3)
            self.assertEqual(report['channels_per_node'], 48)
            self.assertEqual(report['retained_integers_per_node'], 144)
            self.assertEqual(load_bundle(Path(tmp)/'run/bundle').seed.G, 48)
            self.assertEqual(verify_run(Path(tmp)/'run'), report)
