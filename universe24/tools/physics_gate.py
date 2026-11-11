"""Structural dependency utility and explicit retirement of an old physical gate.

Reachability is a necessary graph condition, not evidence of a physical force.
The former field/cosmic gate was calibrated for a retired variable-divisor model.
"""

def reachable_gears(tensor, sources):
    """Over-approximate possible dependencies; absence proves no causal path.

    Forget spatial offsets and include both old-a and old-b reads. Retained local
    state cannot create a missing inter-gear dependency. Presence alone does not
    prove an excited signal or a physical interaction.
    """
    edges = [set() for _ in tensor.gears]
    for m in tensor.monomials:
        for factor in m.factors:
            edges[factor.gear].add(m.target)
    seen = set(sources)
    todo = list(seen)
    while todo:
        for target in edges[todo.pop()]:
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return seen



def run(*args, **kwargs):
    raise NotImplementedError(
        "The former field/cosmic physical gate is retired; its observables are "
        "absent from the fixed-six reference default. No physical pass is implied."
    )


def main():
    try:
        run()
    except NotImplementedError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
