"""End-to-end checkpoint/CLI contract, using temporary files only.

These are finite regression cases, not an all-state proof of reversibility.
"""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data, from_dict, read_checkpoint

ROOT = Path(__file__).resolve().parents[1]
SIGNS = tuple(product((-1, 1), repeat=3))


def config(signs=(1, 1, 1)):
    return {
        "side": 3,
        "coupling_signs": list(signs),
        "steps": 7,
        "seed_changes": [
            {"position": [0, 0, 0], "channel": 0, "state": [2, -3, 1]},
            {"position": [2, 1, 0], "channel": 14, "state": [-1, 4, 4]},
            {"position": [1, 2, 2], "channel": 47, "state": [0, 1, 5]},
        ],
    }


class CheckpointRoundtripTests(unittest.TestCase):
    def cli(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, "-m", "universe24", *map(str, args)],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    @staticmethod
    def events(path):
        return [json.loads(line) for line in path.read_text().splitlines()]

    def test_cli_split_runs_match_continuous_state_and_absolute_events(self):
        """Eight sign triples, two splits, seven updates: 16 split runs."""
        for signs in SIGNS:
            with self.subTest(signs=signs), TemporaryDirectory() as directory:
                path = Path(directory)
                source = path / "seed.json"
                source.write_text(json.dumps(config(signs)))
                full, full_events = path / "full.json", path / "full.jsonl"
                full_result = self.cli("--config", source, "--output", full,
                                       "--events", full_events, "--audit")
                continuous = json.loads(full.read_text())
                events = self.events(full_events)
                self.assertTrue(events, "Fixture must exercise event serialization")
                self.assertEqual(json.loads(full_result.stdout)["completed_steps"], 7)
                initial = from_dict(config(signs)).initial
                _, final, _ = read_checkpoint(full)
                self.assertNotEqual(final, initial, "Do not mask resume errors at a recurrence")
                for split in (2, 5):
                    mid = path / f"mid{split}.json"
                    first_events = path / f"first{split}.jsonl"
                    resumed = path / f"resumed{split}.json"
                    second_events = path / f"second{split}.jsonl"
                    self.cli("--config", source, "--steps", split, "--output", mid,
                             "--events", first_events, "--audit")
                    self.cli("--resume", mid, "--steps", 7 - split, "--output", resumed,
                             "--events", second_events, "--audit")
                    self.assertEqual(json.loads(resumed.read_text()), continuous)
                    left, right = self.events(first_events), self.events(second_events)
                    self.assertEqual(left + right, events)
                    self.assertTrue(all(1 <= event["step"] <= split for event in left))
                    self.assertTrue(all(split < event["step"] <= 7 for event in right))

    def test_serialization_all_signs_backgrounds_and_large_integers(self):
        for signs, remainder in product(SIGNS, range(6)):
            with self.subTest(signs=signs, remainder=remainder), TemporaryDirectory() as directory:
                engine = Engine(Coupling(signs))
                state = State(Cube(3), Channel(0, 0, remainder), {
                    (0, 2, 1, 0): Channel(-(10**100), 10**103 + 1, remainder),
                    (2, 0, 2, 47): Channel(0, -1, (remainder + 1) % 6),
                })
                path = Path(directory) / "checkpoint.json"
                data = checkpoint_data(state, engine, 23)
                path.write_text(json.dumps(data))
                restored_engine, restored, steps = read_checkpoint(path)
                self.assertEqual(restored, state)
                self.assertEqual(restored_engine.coupling.fingerprint, engine.coupling.fingerprint)
                self.assertEqual(steps, 23)
                self.assertEqual(restored_engine.advance(restored), engine.advance(state))

    def test_zero_step_resume_preserves_complete_checkpoint(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)
            experiment = from_dict(config())
            source, target = path / "in.json", path / "out.json"
            source.write_text(json.dumps(checkpoint_data(experiment.initial, experiment.engine, 9)))
            self.cli("--resume", source, "--steps", 0, "--output", target)
            self.assertEqual(json.loads(source.read_text()), json.loads(target.read_text()))

    def test_malformed_checkpoints_are_rejected(self):
        experiment = from_dict(config())
        valid = checkpoint_data(experiment.initial, experiment.engine, 2)
        invalid = []
        for key in valid:
            item = deepcopy(valid)
            del item[key]
            invalid.append(("missing_" + key, item))
        for key, value in (("format", "universe24-checkpoint-v999"),
                           ("coupling_fingerprint", "0" * 64),
                           ("completed_steps", -1), ("completed_steps", True),
                           ("completed_steps", 1.5)):
            item = deepcopy(valid)
            item[key] = value
            invalid.append((str((key, value)), item))
        extra = deepcopy(valid)
        extra["unrecognized"] = 1
        invalid.append(("extra_field", extra))
        duplicate = deepcopy(valid)
        duplicate["experiment"]["seed_changes"].append(deepcopy(duplicate["experiment"]["seed_changes"][0]))
        invalid.append(("duplicate_address", duplicate))
        for remainder in (-1, 6, True):
            item = deepcopy(valid)
            item["experiment"]["seed_changes"][0]["state"][2] = remainder
            invalid.append(("bad_remainder_" + str(remainder), item))
        with TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            for label, item in invalid:
                with self.subTest(case=label):
                    path.write_text(json.dumps(item))
                    with self.assertRaises((TypeError, ValueError)):
                        read_checkpoint(path)
            path.write_text('{"format":')
            with self.assertRaises(json.JSONDecodeError):
                read_checkpoint(path)
            self.cli("--resume", path, "--steps", 1, expected=2)

    def test_malformed_initial_config_is_rejected(self):
        invalid = [
            {}, {"side": 2}, {"side": True}, {"side": 3, "steps": -1},
            {"side": 3, "steps": True}, {"side": 3, "coupling_signs": [1, 0, 1]},
            {"side": 3, "runtime_injection": "forbidden"},
            {"side": 3, "background": [1, 0, 2]},
        ]
        for position, channel in (([3, 0, 0], 0), ([0, 0, 0], 48)):
            invalid.append({"side": 3, "seed_changes": [
                {"position": position, "channel": channel, "state": [0, 1, 2]}]})
        for item in invalid:
            with self.subTest(config=item), self.assertRaises((TypeError, ValueError)):
                from_dict(item)

    def test_cli_never_overwrites_inputs_or_existing_outputs(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)
            source, output, events = path / "seed.json", path / "out.json", path / "events.jsonl"
            original = json.dumps(config())
            source.write_text(original)
            output.write_text("retain this output")
            events.write_text("retain this event log")
            for args in (("--output", source), ("--events", source),
                         ("--output", output), ("--events", events),
                         ("--output", path / "same", "--events", path / "same")):
                with self.subTest(args=args):
                    self.cli("--config", source, "--steps", 0, *args, expected=2)
            self.assertEqual(source.read_text(), original)
            self.assertEqual(output.read_text(), "retain this output")
            self.assertEqual(events.read_text(), "retain this event log")


if __name__ == "__main__":
    unittest.main()
