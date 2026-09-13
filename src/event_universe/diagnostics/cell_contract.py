"""Legacy import path for the canonical NodeState diagnostic.

New code must import from ``event_universe.diagnostics.node_contract``. The word
``cell`` is retained here only for source compatibility and is not a separate
physical concept.
"""

from .node_contract import STATE_RECORDS, node_state_violations

cell_state_violations = node_state_violations

__all__ = ["STATE_RECORDS", "node_state_violations", "cell_state_violations"]
