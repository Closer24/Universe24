"""Independent rejection cases across sector proof and saved-run identity."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from universe24.core import Tensor
from universe24.core.lattice import ZERO
from validation.generic_couplings import sector
from validation.generic_couplings.runtime import run_runtime_pair


class GenericIntegrationReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reduction = sector.build_reduction()

    def test_mutated_raw_types_rejected_in_every_complete_bank(self):
        for full in (False, True):
            for field in ('a', 'b', 'r'):
                for invalid in (True, 0.5):
                    state = sector.prepare_seed()
                    if full:
                        state = sector.embed_state(self.reduction, state)
                    # Bypass the initial State validation, as mutable arrays
                    # can be modified after construction by a caller.
                    bank = getattr(state, field).astype(object)
                    bank[0, 0] = invalid
                    setattr(state, field, bank)
                    operation = sector.project_state if full else sector.embed_state
                    with self.subTest(full=full, field=field, invalid=invalid):
                        with self.assertRaises((TypeError, ValueError)):
                            operation(self.reduction, state)

    def test_mutated_shape_rejected_before_embedding_or_projection(self):
        for full in (False, True):
            for field in ('a', 'b', 'r'):
                state = sector.prepare_seed()
                if full:
                    state = sector.embed_state(self.reduction, state)
                setattr(state, field, getattr(state, field)[:, :-1])
                operation = sector.project_state if full else sector.embed_state
                with self.subTest(full=full, field=field):
                    with self.assertRaises((TypeError, ValueError)):
                        operation(self.reduction, state)

    def test_valid_same_sector_cannot_impersonate_pinned_source_run(self):
        source = self.reduction.full_tensor
        terms = list(source.monomials)
        # chi vanishes on the declared complete sector. This extra term is
        # therefore a valid restriction but a distinct off-sector law.
        terms.append(('projective.phi', 3,
                      (('projective.chi', ZERO, 'b'),)))
        different_source = Tensor(source.gears, terms, strict_support=True)
        different = sector.build_reduction(different_source)
        self.assertEqual(different.tensor, self.reduction.tensor)
        self.assertNotEqual(different.full_tensor.fingerprint,
                            self.reduction.full_tensor.fingerprint)
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'must-not-run'
            with patch('validation.generic_couplings.runtime.build_reduction',
                       return_value=different):
                with patch('validation.generic_couplings.runtime.run_bundle') as execute:
                    with self.assertRaisesRegex(ValueError, 'fingerprint'):
                        run_runtime_pair(destination, steps=1)
                    execute.assert_not_called()
            self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
