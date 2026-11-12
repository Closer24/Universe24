"""Actual shared-law records, complete provenance and negative reader controls."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from universe24.core import DIRECTIONS, Engine, GearType, State, Tensor
from universe24.system.bundle import create_bundle
from universe24.system.runtime import run_bundle
from validation.local_unification.native import build_tensor, prepare_state
from validation.local_unification.records import (
    _bundle, collision_oracle, incoming_direction_from_record, inspect_saved_run,
    inspect_states, outcome, record_train, scalar_first_order,
)


def _history(direction=(1,0,0), *, coupled=True, stream_records=True):
    current = record_train(direction=direction)
    carries = np.asarray([[(g+n)%6 for n in range(343)] for g in range(8)],dtype=object)
    seed = prepare_state(current,7,direction,coupled=coupled,
                         stream_records=stream_records,remainders=carries)
    engine = Engine(build_tensor(direction,coupled=coupled,stream_records=stream_records))
    states = [seed]
    for _ in range(6):
        before=states[-1]
        after=engine.step(before)
        if not engine.inverse_step(after).same_as(before):
            raise AssertionError("full inverse failed")
        states.append(after)
    if not engine.rewind(states[-1],6).same_as(seed):
        raise AssertionError("full rewind failed")
    return states


class LocalUnificationRecordsTests(unittest.TestCase):
    def test_provenance_decoder_requires_ready_single_trial(self):
        for bits in ((1,0,1,0),(1,0,0,1)):
            result=collision_oracle(bits)
            self.assertEqual(incoming_direction_from_record(result),"plus" if bits[2] else "minus")
            self.assertEqual(collision_oracle(result),bits)
        self.assertEqual(outcome((0,0,0,0))["record"],"absent")
        self.assertEqual(outcome((1,1,1,1))["record"],"double")
        for non_trial in ((0,0,0,0),(1,1,1,1),(1,0,0,0),(0,1,0,1)):
            with self.assertRaises(ValueError):
                incoming_direction_from_record(non_trial)
        with self.assertRaises(ValueError):
            collision_oracle((True,0,0,1))

    def test_four_actual_encounters_all_orientations_and_record_lifetimes(self):
        for direction in DIRECTIONS:
            with self.subTest(direction=direction):
                states=_history(direction)
                report=inspect_states(states,direction=direction)
                self.assertEqual(report["created_inversion_record_steps"],[1,2,5,6])
                self.assertEqual(report["retained_used_particles_by_step"],[0,1,2,2,2,3,4])
                self.assertEqual(report["retained_record_particles_by_step"],[4]*7)
                self.assertEqual(len(report["detector_opportunities"]),6)
                self.assertTrue(all(row["last_verified_step"]==6 for row in report["record_lifetimes"]))
                self.assertEqual({int(v) for v in states[-1].r.flat},set(range(6)))

    def test_disconnect_and_no_renewal_keep_every_detector_opportunity(self):
        disconnected=inspect_states(_history(coupled=False),coupled=False)
        exhausted=inspect_states(_history(stream_records=False),stream_records=False)
        self.assertEqual(disconnected["created_inversion_record_steps"],[])
        self.assertEqual(exhausted["created_inversion_record_steps"],[1])
        self.assertEqual(len(exhausted["detector_opportunities"]),6)
        self.assertEqual(exhausted["record_lifetimes"][0]["stop_reason"],"carrier_free_hypothesis_ended")

    def test_incomplete_history_and_wrong_transition_rejected(self):
        states=_history()
        bad=states[0].copy(); bad.a[0,0]=1-int(bad.a[0,0])
        with self.assertRaisesRegex(ValueError,"complete history"):
            inspect_states([bad,*states[1:]])
        with self.assertRaises(ValueError):
            inspect_states([states[0],states[2]])
        with self.assertRaises(ValueError):
            record_train(direction=(True,0,0))

    def test_saved_runtime_identity_and_wrong_law_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"run"
            bundle=_bundle(direction=(1,0,0),coupled=True,stream_records=True)
            run_bundle(bundle,path,steps=6)
            report=inspect_saved_run(path)
            self.assertTrue(report["saved_runtime_verified"])
            self.assertEqual(report["tensor_hash"],bundle.tensor.fingerprint)
            self.assertEqual(report["created_inversion_record_steps"],[1,2,5,6])
            with self.assertRaisesRegex(ValueError,"exact declared shared tensor"):
                inspect_saved_run(path,coupled=False)

    def test_explicit_extended_prefix_reader_verifies_full_run(self):
        base=_bundle(direction=(1,0,0),coupled=True,stream_records=True)
        extended=Tensor(list(base.tensor.gears)+[GearType("record_reader.test_extra","audit")],
                        list(base.tensor.monomials)+[(8,6,[(8,(0,0,0),"b")])],strict_support=True)
        original=base.seed
        zero=np.zeros((1,original.N),dtype=object)
        seed=State(original.L,*[np.concatenate((getattr(original,f),zero),axis=0) for f in ("a","b","r")])
        channels=list(base.channels)+[{"index":8,"name":extended.names[8],"label":"audit",
                                        "owner":"negative_reader_control","purpose":"Reader-only zero spectator control"}]
        bundle=create_bundle(extended,seed,channels=channels,protocol=base.protocol,model=base.model)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"run";run_bundle(bundle,path,steps=6)
            with self.assertRaises(ValueError):
                inspect_saved_run(path)
            report=inspect_saved_run(path,allow_native_prefix=True)
            self.assertEqual(report["source_channels"],9)
            self.assertEqual(report["tensor_hash"],extended.fingerprint)
            self.assertEqual(report["native_prefix_hash"],base.tensor.fingerprint)
            self.assertEqual(report["created_inversion_record_steps"],[1,2,5,6])


if __name__ == "__main__":
    unittest.main()
