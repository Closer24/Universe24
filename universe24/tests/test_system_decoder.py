"""Independent observation contracts, including incomplete and corrupt streams."""
import copy
import hashlib
import json
import unittest

from universe24.core import exact_json
from universe24.core.engine import Engine, State
from universe24.core.tensor import GearType, Tensor
from universe24.system.decoder import (decode_trace, decode_transition, default_protocol,
                                      make_transition, summarize_clicks, validate_protocol,
                                      verify_click_records)


class DecoderTests(unittest.TestCase):
    def setUp(self):
        self.tensor = Tensor([GearType("signal"), GearType("memory", label="audit")],
                             [(0, 2, []), (1, -5, [])], strict_support=True)
        self.engine = Engine(self.tensor)
        self.seed = State(3, [[i - 13 for i in range(27)], [0] * 27],
                          [[0] * 27, [1] * 27],
                          [[i % 6 for i in range(27)], [5] * 27])

    def trace(self, steps=4):
        state = self.seed.copy()
        records = []
        for step in range(1, steps + 1):
            after = self.engine.step(state)
            records.append(make_transition(self.tensor, state, after, run_id="test", step=step))
            state = after
        return records

    def test_online_offline_and_independent_engine_agree(self):
        records = self.trace()
        online = [event for record in records for event in decode_transition(record, self.tensor)]
        offline = decode_trace(json.loads(json.dumps(records)), self.tensor, run_id="test",
                               expected_steps=4, initial_state=self.seed)
        self.assertEqual(online, offline)
        for record in records:
            before, after = (State.from_dict(record[key]) for key in ("before", "after"))
            existing = self.engine.clicks(before, after, step=record["step"]).rows()
            new = decode_transition(record, self.tensor)
            actual = [(e["step"], tuple(e["xyz"]), e["channel"], int(e["kind"][1:]),
                       e["quotient"], e["label"]) for e in new]
            self.assertEqual(actual, existing)
        self.assertEqual({e["label"] for e in online}, {"official", "audit"})
        self.assertEqual({e["sign"] for e in online}, {-1, 1})
        self.assertEqual({e["kind"] for e in online}, {"C1", "C2"})

    def test_passivity_and_no_mutable_alias(self):
        before = self.seed.copy()
        after = self.engine.step(before)
        saved_before, saved_after = before.copy(), after.copy()
        record = make_transition(self.tensor, before, after, run_id="x", step=1)
        events = decode_transition(record, self.tensor)
        events[0]["xyz"][0] = 999
        self.assertTrue(before.same_as(saved_before))
        self.assertTrue(after.same_as(saved_after))
        record["before"]["a"][0][0] = 999
        self.assertTrue(before.same_as(saved_before))

    def test_zero_signal_and_many_to_one_boundary(self):
        tensor = Tensor(["quiet"], [])
        engine = Engine(tensor)
        for residue in (0, 2, 5):
            seed = State(3, [[0] * 27], [[0] * 27], [[residue] * 27])
            events = decode_transition(make_transition(tensor, seed, engine.step(seed),
                                                       run_id="same", step=1), tensor)
            self.assertEqual(events, [])
        self.assertEqual(summarize_clicks([])["events"], 0)

    def test_zero_quotient_changed_triple_is_not_click(self):
        tensor = Tensor(["quiet"], [])
        seed = State(3, [[3] * 27], [[0] * 27], [[0] * 27])
        after = Engine(tensor).step(seed)
        self.assertFalse(seed.same_as(after))
        self.assertEqual(decode_transition(make_transition(tensor, seed, after,
                                                           run_id="same", step=1), tensor), [])

    def test_nonzero_quotient_unchanged_triple_is_not_click(self):
        tensor = Tensor(["fixed"], [(0, 6, [])])
        seed = State(3, [[1] * 27], [[1] * 27], [[0] * 27])
        after = Engine(tensor).step(seed)
        self.assertTrue(seed.same_as(after))
        self.assertEqual(decode_transition(make_transition(tensor, seed, after,
                                                           run_id="same", step=1), tensor), [])

    def test_c0_and_arbitrary_precision_quotients(self):
        tensor = Tensor(["big"], [(0, 3 * 10 ** 90, [])])
        seed = State(3, [[0] * 27], [[0] * 27], [[0] * 27])
        event = decode_transition(make_transition(tensor, seed, Engine(tensor).step(seed),
                                                  run_id="big", step=1), tensor)[0]
        self.assertEqual(event["quotient"], 10 ** 90)
        self.assertEqual(event["kind"], "C0")

    def test_missing_duplicate_reordered_or_truncated_transitions(self):
        records = self.trace()
        bad_traces = [records[:-1], records[1:], [records[0]] + records,
                      [records[1], records[0]] + records[2:]]
        for bad in bad_traces:
            with self.subTest(bad_steps=[r["step"] for r in bad]), self.assertRaises(ValueError):
                decode_trace(bad, self.tensor, run_id="test", expected_steps=4)
        bad = copy.deepcopy(records)
        bad[1]["before"]["a"][0][0] += 1
        with self.assertRaises(ValueError):
            decode_trace(bad, self.tensor, run_id="test", expected_steps=4)

    def test_empty_trace_requires_declared_zero_steps(self):
        self.assertEqual(decode_trace([], self.tensor, run_id="test", expected_steps=0,
                                      initial_state=self.seed), [])
        with self.assertRaises(ValueError):
            decode_trace([], self.tensor, run_id="test", expected_steps=1)

    def test_bad_versions_hashes_identity_values_and_shapes(self):
        record = self.trace(1)[0]
        for key, value in (("schema", "future"), ("tensor_hash", "wrong"),
                           ("run_id", "other"), ("step", True), ("step", 1.0)):
            bad = copy.deepcopy(record)
            bad[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                decode_transition(bad, self.tensor, run_id="test")
        for field, value in (("a", 0.0), ("a", False), ("r", 6), ("r", -1)):
            bad = copy.deepcopy(record)
            bad["before"][field][0][0] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                decode_transition(bad, self.tensor)
        for mutation in (lambda r: r["before"]["a"].pop(),
                         lambda r: r["before"]["b"][0].pop(),
                         lambda r: r.update(extra="hidden"),
                         lambda r: r["after"]["a"][0].__setitem__(0, 77)):
            bad = copy.deepcopy(record)
            mutation(bad)
            with self.assertRaises(ValueError):
                decode_transition(bad, self.tensor)

    def test_saved_click_completeness_and_corruption(self):
        expected = decode_transition(self.trace(1)[0], self.tensor)
        verify_click_records(copy.deepcopy(expected), expected)
        bad_streams = [expected[:-1], expected + [expected[0]], list(reversed(expected))]
        for key, value in (("quotient", False), ("kind", "C0"), ("event_id", "wrong"),
                           ("schema", "future"), ("sign", 1.0)):
            bad = copy.deepcopy(expected)
            bad[0][key] = value
            bad_streams.append(bad)
        for bad in bad_streams:
            with self.assertRaises(ValueError):
                verify_click_records(bad, expected)

    def test_protocol_rejects_unknown_calibrations_and_filtering(self):
        validate_protocol(default_protocol())
        for invalid in ({}, {"version": "future"},
                        {**default_protocol(), "calibration": 3},
                        {**default_protocol(), "classes": ["C2"]}):
            with self.subTest(protocol=invalid), self.assertRaises(ValueError):
                validate_protocol(invalid)

    def test_mutated_state_arrays_are_validated_before_serialization(self):
        for dtype, value in ((float, -12.9), (bool, True)):
            before = self.seed.copy()
            after = self.engine.step(before)
            before.a = before.a.astype(dtype)
            before.a[0, 0] = value
            with self.subTest(dtype=dtype), self.assertRaises(ValueError):
                make_transition(self.tensor, before, after, run_id="test", step=1)
            with self.assertRaises(ValueError):
                decode_trace([], self.tensor, run_id="test", expected_steps=0,
                             initial_state=before)

    def test_unbounded_coefficients_states_and_event_identity(self):
        big = 2 ** 20000 + 17
        tensor = Tensor(["big"], [(0, 3 * big, [])])
        seed = State(3, [[big] * 27], [[-big] * 27], [[5] * 27])
        after = Engine(tensor).step(seed)
        record = make_transition(tensor, seed, after, run_id="huge", step=big)
        events = decode_transition(record, tensor)
        self.assertEqual(events[0]["quotient"], big)
        self.assertEqual(events[0]["step"], big)
        restored = exact_json.loads(exact_json.dumps(record))
        self.assertEqual(decode_transition(restored, tensor), events)
        verify_click_records(exact_json.loads(exact_json.dumps(events)), events)

    def test_normal_event_hash_keeps_standard_json_bytes(self):
        event = decode_transition(self.trace(1)[0], self.tensor)[0]
        identity = {key: event[key] for key in ("run_id", "tensor_hash", "step", "node", "channel")}
        expected = hashlib.sha256(json.dumps(identity, sort_keys=True,
                                             separators=(",", ":"), ensure_ascii=True).encode("ascii")).hexdigest()
        self.assertEqual(event["event_id"], expected)


if __name__ == "__main__":
    unittest.main()
