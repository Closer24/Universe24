"""Legacy test path for the canonical NodeState contract.

The filename is retained because repository check selection still references it.
It is not a second physical vocabulary.
"""

from tests import test_node_state_contract as canonical


def test_legacy_path_runs_canonical_node_state_contract():
    canonical.test_nodes_and_pending_transactions_remain_formula_free_through_delivery()
    canonical.test_unknown_state_owners_require_explicit_review()
    canonical.test_declared_state_fields_cannot_hide_optional_laws_in_unexercised_slots()
    canonical.test_legacy_cell_names_are_aliases_not_physical_types()
