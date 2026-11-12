from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import GearType, State, Tensor
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle
from validation.local_unification import contracts as c


class LocalUnificationContractTests(unittest.TestCase):
    def test_allocation_rejects_disconnected_and_duplicate_ownership(self):
        tensor = Tensor(["record", "carrier"],
                        [(0, 3, [(1, (0, 0, 0), "b")]),
                         (1, 3, [(0, (1, 0, 0), "b")])], strict_support=True)
        roles = {"record": [0], "carrier": [1]}
        report = c.allocation(tensor, roles, [("record", "carrier"), ("carrier", "record")])
        self.assertEqual(report["retained_integers_per_node"], 6)
        for bad in ({"record": [0], "carrier": [0, 1]},
                    {"record": [False], "carrier": [1]}, {"record": [0]}):
            with self.assertRaises(ValueError):
                c.allocation(tensor, bad)
        detached = Tensor(["record", "carrier", "geometry"],
                          [(0, 3, [(1, (0, 0, 0), "b")]),
                           (1, 3, [(0, (1, 0, 0), "b")]),
                           (2, 6, [(2, (0, 0, 0), "b")])], strict_support=True)
        with self.assertRaisesRegex(ValueError, "disconnected"):
            c.allocation(detached, {**roles, "geometry": [2]}, [("record", "geometry")])

    def test_complete_coordinate_covariance_and_input_types(self):
        tensor = Tensor(["a", "b"], [(0, 3, [(1, (1, 0, 0), "b")]),
                                     (1, 3, [(0, (-1, 0, 0), "b")])], strict_support=True)
        arrays = [np.asarray([[k + g - n for n in range(27)] for g in range(2)], dtype=object)
                  for k in (2, 7)]
        carries = np.asarray([[(g + n) % 6 for n in range(27)] for g in range(2)], dtype=object)
        seed = State(3, *arrays, carries)
        matrices = c.signed_permutations()
        self.assertEqual(len(set(matrices)), 48)
        for matrix in matrices:
            c.covariance(tensor, seed, matrix)
        for bad in (((True, 0, 0), (0, 1, 0), (0, 0, 1)),
                    ((1, 0, 0), (1, 0, 0), (0, 0, 1))):
            with self.assertRaises(ValueError):
                c.transform_state(seed, bad)
        linked = Tensor([GearType("link", "audit", link=0)], [], strict_support=True)
        with self.assertRaises(ValueError):
            c.transform_tensor(linked, matrices[0])

    def test_evidence_rejects_mixed_seed_horizon_and_stale_source(self):
        tensor = Tensor([GearType("clock", "audit")], [(0, 3, [(0, (0, 0, 0), "b")])])
        state = State(3, np.zeros((1, 27), dtype=object), np.ones((1, 27), dtype=object),
                      np.asarray([[n % 6 for n in range(27)]], dtype=object))
        channels = [{"index": 0, "name": "clock", "label": "audit", "owner": "control",
                     "purpose": "Mechanical run identity fixture"}]
        bundle = create_bundle(tensor, state, channels=channels, protocol=default_protocol(),
                               model={"id": "identity-fixture", "version": "1", "domain": "mechanical"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "proof.py"
            source.write_text("proof_version = 1\n")
            directory = root / "run"
            run_bundle(bundle, directory, 2)
            options = {"source_paths": ["proof.py"], "source_root": root}
            identity = c.run_identity(directory, **options)
            evidence = c.make_evidence(identity, "mechanical", "passed", {"control": "exact"})
            physical = c.make_evidence(identity, "physics", "blocked", {"reason": "not supplied"})
            joined = c.join_evidence(directory, [evidence, physical],
                                     required_claims=["mechanical", "physics"], **options)
            self.assertEqual(joined["physical_acceptance"], "not_granted")
            self.assertEqual(joined["claims"][1]["status"], "blocked")
            for field, value in (("seed_hash", "f" * 64), ("steps", 3),
                                 ("tensor_hash", "e" * 64), ("steps", True)):
                changed = copy.deepcopy(evidence)
                changed["identity"][field] = value
                with self.assertRaises(ValueError):
                    c.join_evidence(directory, [changed], required_claims=["mechanical"], **options)
            with self.assertRaises(ValueError):
                c.join_evidence(directory, [evidence], required_claims=["mechanical", "physics"], **options)
            source.write_text("proof_version = 2\n")
            with self.assertRaisesRegex(ValueError, "stale-source"):
                c.join_evidence(directory, [evidence], required_claims=["mechanical"], **options)
            with self.assertRaises(ValueError):
                c.make_evidence(identity, "bad", "passed", {"implicit_float": 0.5})

    def test_actual_native_family_and_disconnected_geometry(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = c.audit(temporary)
        self.assertEqual(result["allocation"]["channels"], 8)
        self.assertEqual(result["signed_coordinate_transformations"], 48)
        self.assertTrue(result["disconnected_geometry_claim_rejected"])
        self.assertLess(result["same_fixed_tensor_transformations"], 48)
        self.assertEqual(result["physical_acceptance"], "not_granted")


if __name__ == "__main__":
    unittest.main()
