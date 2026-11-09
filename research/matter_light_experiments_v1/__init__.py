"""Curated matter/light experiments: data, cards and one generic verifier (see README.md).

    from research.matter_light_experiments_v1 import experiment, experiment_ids
    for run in experiment("E01_local_atom_twins"):
        print(run["name"], run["role"], run["steps"])    # run["engine"], run["initial"]; nothing evolves here

Loading checks the data hashes (and regenerates composition runs); it never runs a board.
"""
from __future__ import annotations


def experiment_ids():
    from .verify import experiment_ids as ids
    return ids()


def experiment(eid: str):
    """Every run of one experiment as {name, role, engine, initial, steps}; nothing is evolved."""
    from .verify import _composition, _uses_composition, load_run, manifest
    man = manifest(eid)
    comp = _composition(eid, man) if _uses_composition(man) else None
    out = []
    for run in man["runs"]:
        engine, initial, steps, _ = load_run(eid, man, run, comp)
        out.append({"name": run["name"], "role": run["role"], "engine": engine, "initial": initial, "steps": steps})
    return out


__all__ = ["experiment", "experiment_ids"]
