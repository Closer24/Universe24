"""Repository-wide guard against restoring a configurable divisor scale."""
import ast
import inspect
from pathlib import Path
import unittest

from universe24.core import Engine, Tensor
from universe24.layers.reference_model import reference_system
from universe24.core.tensor import compose

ROOT = Path(__file__).resolve().parents[2]


class FixedDivisorContractTests(unittest.TestCase):
    def test_runtime_sources_have_no_scale_parameter_or_attribute(self):
        failures = []
        for directory in (ROOT/"universe24", ROOT/"experiments"):
            for path in directory.rglob("*.py"):
                if "tests" in path.parts:
                    continue
                tree = ast.parse(path.read_text(), filename=str(path))
                for node in ast.walk(tree):
                    bad = ((isinstance(node, ast.arg) and node.arg in ("Q", "Q_DEFAULT"))
                           or (isinstance(node, ast.Name) and node.id in ("Q", "Q_DEFAULT"))
                           or (isinstance(node, ast.Attribute) and node.attr == "Q")
                           or (isinstance(node, ast.keyword) and node.arg == "Q"))
                    if bad:
                        failures.append(f"{path.relative_to(ROOT)}:{node.lineno}")
        self.assertEqual(failures, [])

    def test_default_law_has_only_fixed_six_arithmetic(self):
        self.assertEqual(list(inspect.signature(Engine).parameters), ["tensor"])
        system = reference_system()
        tensor = compose(*system.blocks)
        engine = Engine(tensor)
        self.assertEqual(engine.D, 6)
        self.assertFalse(hasattr(system, "Q"))
        self.assertFalse(hasattr(tensor, "Q"))
        self.assertFalse(hasattr(engine, "Q"))
        self.assertNotIn("Q", tensor.to_dict())
        self.assertEqual(Tensor.from_dict(tensor.to_dict()), tensor)
        with self.assertRaises(TypeError):
            Engine(tensor, 2)
        with self.assertRaises(AttributeError):
            engine.D = 12


if __name__ == "__main__":
    unittest.main()
