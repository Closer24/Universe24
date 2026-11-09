"""Registered block generators: compositions regenerate published blocks from tracked code only."""
import ast
import json
from pathlib import Path
import sys
import unittest

from universe24.experiments import from_dict
from research.matter_light_blocks_v1 import verify as V
from research.matter_light_blocks_v1.registry import (BLOCKS, FORMAT, apply_control, compose, d1_main_spec,
                                                      d1_skeleton_spec, init_data)

REGISTRY = Path(__file__).resolve().parents[1] / "research" / "matter_light_blocks_v1" / "registry"


class RegisteredCompositions(unittest.TestCase):
    def test_compositions_regenerate_published_blocks(self):
        base = d1_main_spec(100)
        cases = (("d1_local_atom_L100", base), ("d1_local_atom_L200", d1_main_spec(200, tiles=2)),
                 ("d1_control_no_seed_L100", apply_control(base, base["controls"][0])),
                 ("d1_skeleton_atom_spin_clocks_L160", d1_skeleton_spec(160)))
        for name, spec in cases:
            with self.subTest(block=name):
                prepared, report = compose(spec)
                engine, initial, steps, _ = V.load(name)
                self.assertEqual(prepared.initial, initial)
                self.assertEqual(prepared.engine.coupling.fingerprint, engine.coupling.fingerprint)
                self.assertTrue(report.get("slot_clocks_silent_ok"))
                if "junction_classes" in spec["assertions"]:
                    self.assertTrue(report["junction_classes_ok"])
                data = init_data(prepared, steps)
                self.assertEqual(from_dict(json.loads(json.dumps(data))).initial, initial)

    def test_controls_are_masks_and_preconditions_are_checked(self):
        base = d1_main_spec(100)
        names = {c["name"] for c in base["controls"]}
        self.assertEqual(names, {"no_seed", "no_cores", "B0_phase0"})
        no_cores = apply_control(base, next(c for c in base["controls"] if c["name"] == "no_cores"))
        self.assertFalse(any(p["name"].startswith("core") for p in no_cores["placements"]))
        board = {"side": 100, "signs": (-1, 1, 1), "background": (0, 0, 2)}
        with self.assertRaises(ValueError):
            BLOCKS["light_line@1"]({**board, "side": 99}, length=99)
        with self.assertRaises(ValueError):
            BLOCKS["slot_clock@1"](board, state=(1, 1, 2))
        with self.assertRaises(ValueError):
            BLOCKS["spin_ring_z@1"]({**board, "signs": (1, 1, 1)})
        with self.assertRaises(ValueError):
            BLOCKS["slow_glider@1"]({**board, "background": (0, 0, 4)}, start=6)
        variant = json.loads(json.dumps(base))
        variant["board"]["coupling"]["variant"] = {"label": "variant:x@000000000000"}
        with self.assertRaises(ValueError):
            compose(variant)
        self.assertEqual(base["format"], FORMAT)

    def test_registry_imports_no_working_folder(self):
        allowed = set(sys.stdlib_module_names) | {"universe24", "research"}
        for path in REGISTRY.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    with self.subTest(file=path.name, module=node.module):
                        self.assertIn(node.module.split(".")[0], allowed)
                        if node.module.startswith("research"):
                            self.assertIn(node.module, {"research.components"})
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertIn(alias.name.split(".")[0], allowed - {"research"})


if __name__ == "__main__":
    unittest.main()
