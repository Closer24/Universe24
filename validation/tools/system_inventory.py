"""Read-only dependency census of the fixed canonical tensor.

A missing directed path rules out influence for every seed and every number of
updates. A present path only permits influence: coefficients can cancel on a
particular state, or a subsystem may stay unexcited. Offsets are forgotten here;
this is not a geometric causal cone or evidence for a physical interaction.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from universe24.core.tensor import build
from universe24.layers.reference_model import reference_system
from .physics_gate import reachable_gears


def components(vertices, edges):
    """Deterministic weak components, including isolated vertices."""
    adjacent = {v: set() for v in vertices}
    for source, target in edges:
        adjacent[source].add(target)
        adjacent[target].add(source)
    remaining = set(vertices)
    result = []
    while remaining:
        todo = [min(remaining)]
        seen = set(todo)
        while todo:
            for target in adjacent[todo.pop()] - seen:
                seen.add(target)
                todo.append(target)
        remaining -= seen
        result.append(sorted(seen))
    return result


def inventory(tensor):
    """Derive connectivity from live merged monomials, never from field names.

    Names are used solely to aggregate the report. All reachability calculations
    use gear indices; aggregation can join otherwise disconnected gear types.
    """
    names = tensor.names
    namespace = [name.split('.', 1)[0] for name in names]
    groups = sorted(set(namespace))
    edges = {(f.gear, m.target) for m in tensor.monomials for f in m.factors}
    ns_edges = {(namespace[a],namespace[b]) for a,b in edges if namespace[a]!=namespace[b]}
    reads = Counter()
    fields = Counter()
    for m in tensor.monomials:
        for f in m.factors:
            if namespace[f.gear] != namespace[m.target]:
                reads[(namespace[f.gear],namespace[m.target])] += 1
            fields[f.field] += 1
    summaries = []
    for ns in groups:
        indices = {g for g,n in enumerate(namespace) if n == ns}
        reachable = reachable_gears(tensor,indices)
        summaries.append(dict(name=ns,gear_types=len(indices),
            official_types=sum(tensor.gears[g].label=='official' for g in indices),
            physical_link_types=sum(tensor.gears[g].link is not None for g in indices),
            input_monomials=sum(m.target in indices for m in tensor.monomials),
            reads_from=sorted(a for a,b in ns_edges if b==ns),
            writes_to=sorted(b for a,b in ns_edges if a==ns),
            can_reach_namespaces=sorted({namespace[g] for g in reachable} - {ns})))
    gear_components = components(range(tensor.G),edges)
    return dict(schema='universe24-system-inventory-v1',
        dynamics_fingerprint=tensor.dynamics_fingerprint,tensor_fingerprint=tensor.fingerprint,
        D=6,
        gear_types=tensor.G,retained_integer_counters_per_node=2*tensor.G,
        retained_remainders_per_node=tensor.G,rank=tensor.rank,
        monomials=len(tensor.monomials),designations=len(tensor.designations),
        census=tensor.census(),factor_reads_by_field=dict(sorted(fields.items())),
        inverse_stage_sizes=[len(s) for s in tensor.stages],
        strict_physical_support_violations=len(tensor.support_violations()),
        namespaces=summaries,
        cross_namespace_factor_reads=[dict(source=a,target=b,occurrences=n)
                                      for (a,b),n in sorted(reads.items())],
        independent_namespace_groups=components(groups,ns_edges),
        gear_dependency_components=[dict(size=len(c),gears=[names[g] for g in c]) for c in gear_components],
        interpretation=dict(
            independent_groups='No live monomial reads between groups, in either direction; they evolve independently.',
            present_path='Possible structural influence only; does not prove excitation, strength or physics.',
            rank='One output index plus at most three input factors; not a 4D spacetime metric.',
            namespace_grouping='Reporting convenience only; gear components can be finer than namespace groups.'))


def reference_inventory():
    system = reference_system()
    result = inventory(build(*system.blocks))
    # Raw terms may cancel or merge on composition. Do not sum these to obtain
    # the live monomial census or pretend each survives independently.
    result['builder_blocks'] = [dict(name=b.name,declared_gear_types=len(b.gears),
                                     raw_terms=len(b.terms),description=b.doc)
                                for b in system.blocks]
    return result


def default_inventory():
    from fractions import Fraction
    from universe24.layers.adm import compile_adm
    from universe24.layers.universe import UniverseProgram
    from universe24.prepare.einstein import inhomogeneous_scalar
    _, scale, _ = inhomogeneous_scalar(3, complex_matter=True, dark_matter=True)
    program, parameters = compile_adm(complex_matter=True, dark_matter=True,
                                      scale=scale, dx=Fraction(1, 3))
    program = UniverseProgram(program, parameters)
    result = inventory(program.tensor)
    result['physical_model'] = 'Einstein + complex Klein-Gordon + geodesic dark dust'
    result['physical_fields'] = parameters['fields']
    result['physical_steps'] = parameters['steps']
    result['engine_microticks'] = program.ticks
    result['channel_allocation'] = program.assembly.manifest(include_channels=False)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default='runs/system-inventory.json')
    args=parser.parse_args()
    result=default_inventory()
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('gear_types','rank','monomials','independent_namespace_groups')},indent=2))


if __name__=='__main__':
    main()
