"""Records-only detector windows and their unavoidable information loss."""
import copy
import unittest

from universe24.core.engine import Engine, State
from universe24.core.tensor import GearType, Tensor
from universe24.system.decoder import decode_transition, make_transition
from validation.clock_links.observer import (ClickObserver, make_protocol,
                                             observe_clicks, validate_protocol)


def detector_control(amplitudes=(3, 1), stationary=False):
    """Constant carrier ports and reversible squared-input recorders, test only."""
    gears = [GearType("carrier0", label="audit"), GearType("carrier1", label="audit"),
             GearType("detector0", label="audit"), GearType("detector1", label="audit")]
    terms = [(i, 6, [(i, (0, 0, 0), "b")]) for i in (0, 1)]
    terms += [(i + 2, 3, [(i, (0, 0, 0), "b")] * 2) for i in (0, 1)]
    tensor = Tensor(gears, terms, strict_support=True)
    values = list(amplitudes) + ([x * x // 2 for x in amplitudes] if stationary else [0, 0])
    if stationary and any(x * x % 2 for x in amplitudes):
        raise ValueError("stationary detector preparation requires even intensity")
    seed = State(3, [[x] * 27 for x in values], [[x] * 27 for x in values], [[0] * 27 for _ in values])
    return tensor, seed


def records_for(tensor, seed, steps=1):
    engine, state, records = Engine(tensor), seed.copy(), []
    for step in range(1, steps + 1):
        after = engine.step(state)
        records.extend(decode_transition(make_transition(tensor, state, after,
                                                         run_id="observer-test", step=step), tensor))
        state = after
    return records, state


class ClockLinkObserverTests(unittest.TestCase):
    def protocol(self, tensor, steps=1, **kwargs):
        return make_protocol(tensor_hash=tensor.fingerprint, L=3, channel_count=tensor.G,
                             expected_steps=steps, detectors=[
                                 {"id": "A", "node": 0, "channels": [tensor.G - 2]},
                                 {"id": "B", "node": 0, "channels": [tensor.G - 1]}], **kwargs)

    def test_intensity_ratio_does_not_equal_event_probability(self):
        tensor, seed = detector_control()
        records, _ = records_for(tensor, seed)
        report = observe_clicks(records, self.protocol(tensor), run_id="observer-test")
        self.assertEqual([row["event_count"] for row in report["trials"]], [1, 1])
        self.assertEqual([row["signed_quotient_sum"] for row in report["trials"]], [9, 1])
        self.assertEqual(report["outcome_counts"], {"none": 0, "single": 2, "multiple": 0})
        self.assertTrue(all(row["by_kind"] == {"C0": 1, "C1": 0, "C2": 0}
                            for row in report["trials"]))

    def test_no_record_cannot_reconstruct_nonzero_stationary_intensity(self):
        tensor, dark = detector_control((0, 0), stationary=True)
        _, bright = detector_control((2, 4), stationary=True)
        dark_records, dark_after = records_for(tensor, dark, 3)
        bright_records, bright_after = records_for(tensor, bright, 3)
        self.assertNotEqual(dark.to_dict(), bright.to_dict())
        self.assertEqual(dark_records, bright_records)
        self.assertEqual(bright_records, [])
        self.assertTrue(dark.same_as(dark_after))
        self.assertTrue(bright.same_as(bright_after))
        report = observe_clicks(bright_records, self.protocol(tensor, 3), run_id="observer-test")
        self.assertEqual(report["outcome_counts"]["none"], 6)

    def test_online_offline_passivity_and_no_mutable_aliases(self):
        tensor, seed = detector_control()
        saved_seed = seed.to_dict()
        records, final = records_for(tensor, seed, 4)
        saved_records = copy.deepcopy(records)
        protocol = self.protocol(tensor, 4)
        reader = ClickObserver(protocol, run_id="observer-test")
        protocol["detectors"][0]["channels"][0] = 0
        for step in range(1, 5):
            reader.consume(e for e in records if e["step"] == step)
        offline = observe_clicks(iter(records), self.protocol(tensor, 4), run_id="observer-test")
        self.assertEqual(reader.report(), offline)
        exposed = reader.report()
        exposed["protocol"]["windows"][0]["stop"] = 100
        self.assertEqual(reader.report(), offline)
        self.assertEqual(seed.to_dict(), saved_seed)
        self.assertEqual(records, saved_records)
        self.assertTrue(Engine(tensor).rewind(final, 4).same_as(seed))

    def test_all_classes_and_multiple_events_remain_visible(self):
        tensor = Tensor([GearType(f"d{i}", label="audit") for i in range(3)],
                        [(0, 3, []), (1, 4, []), (2, 5, [])])
        seed = State(3, [[0] * 27] * 3, [[0] * 27] * 3, [[0] * 27] * 3)
        records, _ = records_for(tensor, seed)
        protocol = make_protocol(tensor_hash=tensor.fingerprint, L=3, channel_count=3,
                                 expected_steps=1, detectors=[{"id": "combined", "node": 0,
                                                              "channels": [0, 1, 2]}])
        row = observe_clicks(records, protocol, run_id="observer-test")["trials"][0]
        self.assertEqual(row["outcome"], "multiple")
        self.assertEqual(row["by_kind"], {"C0": 1, "C1": 1, "C2": 1})

    def test_reject_corruption_reorder_and_wrong_run_even_outside_detector(self):
        tensor, seed = detector_control()
        records, _ = records_for(tensor, seed)
        bad_streams = [records + [records[0]], list(reversed(records))]
        for key, value in (("run_id", "other"), ("tensor_hash", "0" * 64),
                           ("schema", "future"), ("quotient", True), ("xyz", [1, 1, 1])):
            bad = copy.deepcopy(records)
            bad[-1][key] = value
            bad_streams.append(bad)
        for bad in bad_streams:
            with self.assertRaises(ValueError):
                observe_clicks(bad, self.protocol(tensor), run_id="observer-test")

    def test_protocol_covers_every_window_and_rejects_selection(self):
        tensor, _ = detector_control()
        good = self.protocol(tensor, 3)
        changes = [lambda p: p.update(classes=["C2"]),
                   lambda p: p["windows"].pop(1),
                   lambda p: p["windows"][1].update(start=1),
                   lambda p: p["windows"][-1].update(stop=2),
                   lambda p: p["detectors"][0]["channels"].append(2),
                   lambda p: p.update(channel_count=49),
                   lambda p: p.update(expected_steps=True)]
        for change in changes:
            bad = copy.deepcopy(good)
            change(bad)
            with self.assertRaises(ValueError):
                validate_protocol(bad)

    def test_missing_valid_events_require_independent_replay(self):
        tensor, seed = detector_control()
        records, _ = records_for(tensor, seed)
        complete = observe_clicks(records, self.protocol(tensor), run_id="observer-test")
        truncated = observe_clicks(records[1:], self.protocol(tensor), run_id="observer-test")
        self.assertEqual(truncated["stream_completeness"], "requires independent complete-run replay")
        self.assertNotEqual(complete["input_record_sha256"], truncated["input_record_sha256"])
        self.assertEqual(truncated["trials"][0]["outcome"], "none")


if __name__ == "__main__":
    unittest.main()
