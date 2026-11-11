"""Stable existing fingerprints plus arbitrarily large exact JSON integers."""
import hashlib
import json
import sys
import unittest

from universe24.core import exact_json
from universe24.core.tensor import Tensor


class ExactJsonTests(unittest.TestCase):
    def test_standard_compact_bytes_preserved(self):
        data = {"unicode": "שלום 🪐", "escape": 'a\n"b\\c', "z": [None, True, False, -17, 0, 2 ** 100],
                "a": {"gamma": (1, 2, 3)}}
        for sort_keys in (False, True):
            for ensure_ascii in (False, True):
                with self.subTest(sort_keys=sort_keys, ensure_ascii=ensure_ascii):
                    opts = dict(sort_keys=sort_keys, separators=(",", ":"), ensure_ascii=ensure_ascii)
                    encoded = exact_json.dumps(data, **opts)
                    self.assertEqual(encoded, json.dumps(data, **opts))
                    self.assertEqual(exact_json.loads(encoded), json.loads(encoded))

    def test_arbitrary_decimal_roundtrip_does_not_change_global_limit(self):
        before = sys.get_int_max_str_digits()
        values = [0, 1, -1, 10 ** 9 - 1, 10 ** 9, 10 ** 9 + 1, 10 ** 18,
                  2 ** 20000 + 17, -(2 ** 20000 + 17)]
        encoded = exact_json.dumps(values)
        self.assertGreater(len(encoded), 12000)
        self.assertEqual(exact_json.loads(encoded), values)
        self.assertEqual(sys.get_int_max_str_digits(), before)

    def test_reject_inexact_unsupported_and_circular_data(self):
        circular = []
        circular.append(circular)
        for data in (1.5, float("nan"), {1: "not string"}, object(), circular):
            with self.subTest(kind=type(data).__name__):
                with self.assertRaises((ValueError, TypeError)):
                    exact_json.dumps(data)
        for data in ("1.0", "1e2", "NaN", "Infinity"):
            with self.assertRaises(ValueError):
                exact_json.loads(data)

    def test_duplicate_hook_remains_available(self):
        def reject_duplicate(pairs):
            if len(dict(pairs)) != len(pairs):
                raise ValueError("duplicate")
            return dict(pairs)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            exact_json.loads('{"x":1,"x":2}', object_pairs_hook=reject_duplicate)

    def test_existing_tensor_fingerprints_are_unchanged(self):
        tensor = Tensor(["a", "b"], [("b", -123, [("a", (1, 0, 0), "b")])])
        expected_full = hashlib.sha256(json.dumps(tensor.to_dict(), sort_keys=True,
                                                  separators=(",", ":")).encode()).hexdigest()
        blob = [tensor.G, [[m.target, m.coeff, [[f.gear, list(f.offset), f.field] for f in m.factors]]
                           for m in tensor.monomials]]
        expected_dynamics = hashlib.sha256(json.dumps(blob, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(tensor.fingerprint, expected_full)
        self.assertEqual(tensor.dynamics_fingerprint, expected_dynamics)
        self.assertEqual(tensor.to_json(), json.dumps(tensor.to_dict(), separators=(",", ":")))

    def test_huge_tensor_coefficient_roundtrip_and_fingerprints(self):
        tensor = Tensor(["value"], [("value", -(2 ** 20000), [])])
        other = Tensor.from_json(tensor.to_json(), strict_support=True)
        self.assertEqual(other.monomials[0].coeff, -(2 ** 20000))
        self.assertEqual(other.fingerprint, tensor.fingerprint)
        self.assertEqual(other.dynamics_fingerprint, tensor.dynamics_fingerprint)


if __name__ == "__main__":
    unittest.main()
