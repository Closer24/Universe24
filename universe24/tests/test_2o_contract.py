"""Exact polynomial symmetry and its full-state enforcement at the bundle boundary."""
from dataclasses import replace
import hashlib
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.algebra.group_2o import group, rotate
from universe24.core import Engine, State, Tensor, compose, reference_block
from universe24.core.symmetry import CONTRACT, SymmetryError, act, require_equivariant
from universe24.core.tensor import Factor, GearType, Monomial
from universe24.system.bundle import (
    BundleError, canonical_bytes, create_bundle, load_bundle, read_json, save_bundle, validate_bundle,
)
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run


def reference(signs=(1, -1, 1)):
    return compose(reference_block(signs))


def state(L=3, big=False):
    rng = np.random.default_rng(293)
    shape = (48, L ** 3)
    a, b = (rng.integers(-11, 12, size=shape).astype(object) for _ in range(2))
    if big:
        a[4, 1], b[11, 3] = -(1 << 100), 1 << 90
    return State(L, a, b, np.arange(48 * L ** 3).reshape(shape) % 6)


def bundle(tensor=None, model=None):
    tensor = reference() if tensor is None else tensor
    metadata = dict(id="symmetry-fixture", version="1", domain="mechanical test",
                    role="universe-candidate", symmetry=CONTRACT)
    if model is not None:
        metadata.update(model)
    channels = [dict(index=i, name=g.name, label=g.label, owner="fixture", purpose="test")
                for i, g in enumerate(tensor.gears)]
    return create_bundle(tensor, state(), channels=channels, protocol=default_protocol(), model=metadata)


class GroupActionTests(unittest.TestCase):
    def test_action_matches_independent_scatter_and_preserves_center_lifts(self):
        original, algebra = state(big=True), group()
        for k in range(48):
            transformed = act(original, k)
            for g, node in ((0, 0), (4, 1), (11, 3), (47, 26)):
                destination = original.lattice.index(*rotate(algebra.rotations[k], original.lattice.coords(node)))
                self.assertEqual(transformed.gear(algebra.multiplication[k][g], destination),
                                 original.gear(g, node))
            self.assertTrue(act(transformed, algebra.inverses[k]).same_as(original))
        central = act(original, algebra.central)
        self.assertFalse(central.same_as(original))
        for g in range(48):
            h = algebra.multiplication[algebra.central][g]
            for bank in ("a", "b", "r"):
                np.testing.assert_array_equal(getattr(central, bank)[h], getattr(original, bank)[g])

    def test_left_action_composition_for_every_group_pair(self):
        original, algebra = state(), group()
        transformed = [act(original, k) for k in range(48)]
        for k in range(48):
            for h in range(48):
                self.assertTrue(act(transformed[h], k).same_as(transformed[algebra.multiplication[k][h]]))

    def test_full_rule3_and_inverse_commute_for_both_signs_and_nonlinear_law(self):
        base = reference()
        algebra = group()
        cross_terms = [Monomial(g, 3, (
            Factor(g, (0, 0, 0), "b"),
            Factor(algebra.multiplication[g][1], rotate(algebra.rotations[g], (1, 0, 0)), "b"),
        )) for g in range(48)]
        nonlinear = Tensor(base.gears, list(base.monomials) + [
            Monomial(g, -2, (Factor(g, (0, 0, 0), "b"),) * 3) for g in range(48)
        ] + [Monomial(g, 5, ()) for g in range(48)] + cross_terms, strict_support=True)
        for tensor in (reference((1, 1, 1)), base, nonlinear):
            require_equivariant(tensor)
            engine = Engine(tensor)
            for L, big in ((3, False), (4, False), (3, True)):
                original = state(L, big)
                following, preceding = engine.step(original), engine.inverse_step(original)
                for k in range(48):
                    with self.subTest(terms=len(tensor), L=L, big=big, k=k):
                        transformed = act(original, k)
                        self.assertTrue(engine.step(transformed).same_as(act(following, k)))
                        self.assertTrue(engine.inverse_step(transformed).same_as(act(preceding, k)))


class PolynomialCertificateTests(unittest.TestCase):
    def test_coefficient_target_and_offset_defects_are_detected(self):
        tensor = reference()
        first, *rest = tensor.monomials
        f = first.factors[0]
        defects = (replace(first, coeff=first.coeff + 1),
                   replace(first, target=(first.target + 1) % 48),
                   replace(first, factors=(replace(f, offset=(0, 0, 0)),)))
        for defect in defects:
            with self.subTest(defect=defect), self.assertRaisesRegex(SymmetryError, "covariance failed"):
                require_equivariant(Tensor(tensor.gears, [defect, *rest]))

    def test_48_is_insufficient_and_unsupported_metadata_cannot_claim_action(self):
        with self.assertRaisesRegex(SymmetryError, "covariance failed"):
            require_equivariant(Tensor([f"g{i}" for i in range(48)], [(0, 1, ())]))
        for count in (47, 49):
            with self.assertRaisesRegex(SymmetryError, "exactly 48"):
                require_equivariant(Tensor([f"g{i}" for i in range(count)], []))
        for replacement, message in ((GearType("link", link=0), "node channels"),
                                     (GearType("hidden", label="audit"), "passive labels")):
            gears = list(reference().gears)
            gears[0] = replacement
            with self.assertRaisesRegex(SymmetryError, message):
                require_equivariant(Tensor(gears, []))


class CandidateBoundaryTests(unittest.TestCase):
    def test_candidate_certificate_survives_saved_run_and_replay(self):
        candidate = bundle()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run"
            report = run_bundle(candidate, path, 2)
            self.assertEqual(verify_run(path), report)
            self.assertEqual(load_bundle(path / "bundle").model_contract,
                             dict(role="universe-candidate", symmetry=CONTRACT, status="passed"))
            self.assertEqual(report["model_contract"], candidate.model_contract)
            self.assertEqual(report["acceptance_gates"]["C"]["status"], "not_tested")
            for file in ("core/symmetry.py", "algebra/group_2o.py"):
                self.assertIn(file, report["source_hashes"])

    def test_research_is_not_automatically_a_candidate(self):
        tensor = Tensor(reference().gears, [(0, 1, ())])
        research = bundle(tensor, dict(role="research", symmetry=None))
        self.assertEqual(research.model_contract, dict(role="research", symmetry=None, status="not_declared"))
        with self.assertRaisesRegex(BundleError, "covariance failed"):
            bundle(tensor)
        # A research law may voluntarily declare and satisfy the same action.
        self.assertEqual(bundle(model=dict(role="research")).model_contract["status"], "passed")

    def test_missing_or_unknown_contract_fails(self):
        for model in (dict(symmetry=None), dict(symmetry="2O"), dict(role="universe")):
            with self.subTest(model=model), self.assertRaises(BundleError):
                bundle(model=model)

    def test_forged_candidate_is_rejected_before_any_output(self):
        candidate = bundle()
        forged = replace(candidate, tensor=Tensor(candidate.tensor.gears, [(0, 1, ())]))
        with tempfile.TemporaryDirectory() as tmp:
            for operation in (validate_bundle, lambda b: save_bundle(b, Path(tmp) / "bundle"),
                              lambda b: run_bundle(b, Path(tmp) / "run", 1)):
                with self.assertRaisesRegex(BundleError, "covariance failed"):
                    operation(forged)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_rehashed_model_cannot_promote_asymmetric_research(self):
        research = bundle(Tensor(reference().gears, [(0, 1, ())]), dict(role="research", symmetry=None))
        with tempfile.TemporaryDirectory() as tmp:
            path = save_bundle(research, Path(tmp) / "bundle")
            model = dict(research.model, role="universe-candidate", symmetry=CONTRACT)
            data = canonical_bytes(model)
            (path / "model.json").write_bytes(data)
            manifest = read_json(path / "bundle.json")
            manifest["files"]["model.json"] = hashlib.sha256(data).hexdigest()
            (path / "bundle.json").write_bytes(canonical_bytes(manifest))
            with self.assertRaisesRegex(BundleError, "covariance failed"):
                load_bundle(path)
