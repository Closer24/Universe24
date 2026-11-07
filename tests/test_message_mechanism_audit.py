"""Evidence-integrity tests deliberately forge self-consistent saved digests."""
import copy
from pathlib import Path
import unittest

from research.message_mechanism.audit import (
    audit_experiment, check_recorded_observations, digest, load,
    receiver_observations, snapshots,
)


class MessageMechanismAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.record = load(root/"research/message_mechanism/evidence/baseline_v1/records/packet-r42-on.json.gz")

    @staticmethod
    def rehash(experiment, index):
        frame = experiment["frames"][index]
        frame["state_sha256"] = digest({"side": experiment["side"],
            "background": experiment["background"], "cells": frame["cells"]})

    def test_rehashed_halo_corruption_rejected_by_independent_preparation(self):
        e = copy.deepcopy(self.record["experiment"])
        frame = e["frames"][0]
        row = next(row for row in frame["cells"] if row[1:3] != [64, 64])
        row[6] = (int(row[6])+2) % 6
        self.rehash(e, 0)
        with self.assertRaisesRegex(AssertionError, "Independent initial preparation mismatch"):
            audit_experiment(e, self.record["spec"])

    def test_rehashed_transition_corruption_rejected_by_matrix_oracle(self):
        e = copy.deepcopy(self.record["experiment"])
        e["frames"][1]["cells"][0][4] = str(int(e["frames"][1]["cells"][0][4])+1)
        self.rehash(e, 1)
        with self.assertRaisesRegex(AssertionError, "Matrix forward mismatch"):
            audit_experiment(e, self.record["spec"])

    def test_balanced_false_input_terms_rejected_even_with_unchanged_sum(self):
        record = copy.deepcopy(self.record)
        terms = record["detector_observations"]["receiver.node"]["trace"][0]["six_inputs"][0]
        terms[0]["b"] = str(int(terms[0]["b"])+1)
        terms[1]["b"] = str(int(terms[1]["b"])-1)
        measured = receiver_observations(snapshots(record["experiment"]), [48, 64, 64], (1, 1, 1))
        with self.assertRaisesRegex(AssertionError, "Six-term input mismatch"):
            check_recorded_observations(record, measured)


if __name__ == "__main__":
    unittest.main()
