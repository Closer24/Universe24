"""Source-pinned worker setup, entered through the standard-library runpy runner."""

import pickle
import sys
from collections.abc import Mapping
from pathlib import Path


def initialize(namespace: Mapping[str, object]) -> None:
    source = namespace.get("_event_universe_source")
    serialized = namespace.get("_event_universe_planner")
    if not isinstance(source, str) or not isinstance(serialized, bytes):
        raise RuntimeError("worker setup requires an explicit source and immutable planner")
    source_path = Path(source).resolve()
    sys.path.insert(0, str(source_path))
    import event_universe

    if Path(event_universe.__file__).resolve().parent != source_path / "event_universe":
        raise RuntimeError("worker imported a different event_universe source")
    from event_universe import local_execution

    # These bytes originate only from the owner's composed immutable law.
    local_execution._worker_planner = pickle.loads(serialized)


if __name__ == "__event_universe_worker__":
    initialize(globals())
    # run_path returns its temporary namespace; imported modules are not shareable.
    globals().clear()
