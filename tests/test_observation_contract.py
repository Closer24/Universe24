"""Passive observers preserve state and retain the declared arithmetic semantics."""
from dataclasses import FrozenInstanceError
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.core.rule3 import forward
from universe24.observation import (
    balance_residuals, classify, clicks, expected_account_change, signed_account,
)

ROOT = Path(__file__).resolve().parents[1]
SIGNS = tuple(product((-1, 1), repeat=3))


class ObservationContractTests(unittest.TestCase):
    def test_scalar_classifier_matches_declared_input_formula(self):
        """1134 actual transitions, including all remainder/input classes."""
        for a, b, r, u in product((-2, 0, 3), (-2, 0, 3), range(6), range(-10, 11)):
            old = Channel(a, b, r)
            new = forward(old, u)
            quotient = (2 * u + r) // 6
            expected = (u % 3, quotient) if quotient != 0 and old != new else None
            self.assertEqual(classify(old, new), expected, (old, u, new))

    def test_readout_guards_hide_changes_and_stationary_nonzero_quotients(self):
        for old, u in ((Channel(1, 0, 2), 0), (Channel(0, 0, 2), 1)):
            new = forward(old, u)
            self.assertNotEqual(new, old)
            self.assertEqual(new.b + old.a, 0)
            self.assertIsNone(classify(old, new))
        stationary = Channel(1, 1, 2)
        unchanged = forward(stationary, 6)
        self.assertEqual(unchanged, stationary)
        self.assertEqual(unchanged.b + stationary.a, 2)
        self.assertIsNone(classify(stationary, unchanged))

    def test_observers_and_audits_cannot_mutate_states(self):
        for signs in SIGNS:
            engine = Engine(Coupling(signs))
            old = State(Cube(3), cells={
                (0, 0, 0, 0): Channel(2, -3, 1),
                (2, 1, 0, 14): Channel(-1, 4, 4),
                (1, 2, 2, 47): Channel(0, 1, 5),
            })
            for t in range(1, 8):
                new = engine.advance(old)
                before_copy, after_copy = dict(old.cells), dict(new.cells)
                first, second = list(clicks(old, new, t)), list(clicks(old, new, t))
                self.assertEqual(first, second)
                self.assertEqual([e.address for e in first], sorted(e.address for e in first))
                self.assertEqual(balance_residuals(old, new, engine), {})
                self.assertEqual(signed_account(new) - signed_account(old), expected_account_change(old, engine))
                self.assertEqual(engine.rewind(new), old)
                self.assertEqual(dict(old.cells), before_copy)
                self.assertEqual(dict(new.cells), after_copy)
                self.assertEqual(engine.advance(old), new)
                if first:
                    with self.assertRaises(FrozenInstanceError):
                        first[0].step = 0
                with self.assertRaises(TypeError):
                    old.cells[(0, 0, 0, 0)] = Channel(0, 0, 2)
                old = new

    def test_cli_events_and_audit_do_not_change_final_state(self):
        for signs in SIGNS:
            with self.subTest(signs=signs), TemporaryDirectory() as directory:
                path = Path(directory)
                source = path / "seed.json"
                source.write_text(json.dumps({
                    "side": 3, "coupling_signs": signs, "steps": 7,
                    "seed_changes": [
                        {"position": [0, 0, 0], "channel": 2, "state": [3, -2, 1]},
                        {"position": [2, 2, 2], "channel": 14, "state": [0, 4, 4]},
                    ],
                }))
                checkpoints = []
                for observed in (False, True):
                    target = path / f"final-{observed}.json"
                    command = [sys.executable, "-m", "universe24", "--config", str(source), "--output", str(target)]
                    if observed:
                        command += ["--events", str(path / "events.jsonl"), "--audit"]
                    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    checkpoints.append(json.loads(target.read_text()))
                self.assertEqual(*checkpoints)

    def test_observation_rejects_incompatible_states_and_invalid_step(self):
        old = State(Cube(3))
        for new in (State(Cube(4)), State(Cube(3), Channel(0, 0, 3))):
            with self.assertRaises(ValueError):
                list(clicks(old, new, 1))
        for step in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                list(clicks(old, old, step))
        with self.assertRaises(ValueError):
            classify(Channel(0, 0, 2), Channel(0, 0, 3))


if __name__ == "__main__":
    unittest.main()
