"""Fail on any supported allocation other than exactly 48 retained channels."""
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


def prepared(count):
    names = [f"g{i}" for i in range(count)]
    # Deliberately collide with the first appended idle name.
    names[0] = f"__idle_{count:02d}"
    tensor = Tensor(names, [(names[0], 3, [(names[0], (1, 0, 0), "b")])])
    seed = State(3, [[n-13 for n in range(27)] for _ in names],
                 [[n*n-7 for n in range(27)] for _ in names],
                 [[n % 6 for n in range(27)] for _ in names])
    owners = [dict(index=i, name=g.name, label=g.label, owner="fixture", purpose="test")
              for i, g in enumerate(tensor.gears)]
    bundle = create_bundle(tensor, seed, channels=owners, protocol=default_protocol(),
                           model=dict(id="padding-test", version="1", domain="mechanical"))
    return tensor, seed, bundle


class Exactly48Tests(unittest.TestCase):
    def test_every_source_size_preserves_dynamics_carries_and_inverse(self):
        for count in range(1, 49):
            with self.subTest(count=count):
                tensor, seed, bundle = prepared(count)
                self.assertEqual(bundle.tensor.G, 48)
                self.assertEqual(bundle.seed.G, 48)
                self.assertEqual(len(bundle.channels), 48)
                self.assertEqual(bundle.manifest['retained_integers_per_node'], 144)
                self.assertEqual(len(set(bundle.tensor.names)), 48)
                self.assertEqual(validate_bundle(bundle).bundle_id, bundle.bundle_id)
                current, expected = bundle.seed, seed
                engine = Engine(bundle.tensor)
                for _ in range(3):
                    current = engine.step(current)
                    expected = scalar_step(tensor, expected)
                    for bank in ('a', 'b', 'r'):
                        self.assertTrue((getattr(current, bank)[:count] == getattr(expected, bank)).all())
                        self.assertFalse((getattr(current, bank)[count:] != 0).any())
                self.assertTrue(engine.rewind(current, 3).same_as(bundle.seed))
                self.assertEqual(tensor.G, count)  # caller-owned construction is unchanged

    def test_unpadded_sealed_input_is_rejected_before_output(self):
        tensor, seed, bundle = prepared(2)
        forged = replace(bundle, tensor=tensor, _seed_bytes=canonical_bytes(seed.to_dict()),
                         _channels_bytes=canonical_bytes(list(bundle.channels[:2])))
        with tempfile.TemporaryDirectory() as tmp:
            for operation in (validate_bundle, lambda b: save_bundle(b, Path(tmp)/'bundle'),
                              lambda b: run_bundle(b, Path(tmp)/'run', 1)):
                with self.assertRaisesRegex(BundleError, 'exactly 48'):
                    operation(forged)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_saved_run_retains_and_replays_all_144_registers_per_node(self):
        _, _, bundle = prepared(6)
        with tempfile.TemporaryDirectory() as tmp:
            report = run_bundle(bundle, Path(tmp)/'run', 3)
            self.assertEqual(report['channels_per_node'], 48)
            self.assertEqual(report['retained_integers_per_node'], 144)
            self.assertEqual(load_bundle(Path(tmp)/'run/bundle').seed.G, 48)
            self.assertEqual(verify_run(Path(tmp)/'run'), report)

    def test_49_source_channels_fail(self):
        with self.assertRaisesRegex(BundleError, '48.*49'):
            prepared(49)
