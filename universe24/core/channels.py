"""Construction-time channel ownership for a single fixed Rule3 tensor.

Each component owns a disjoint, retained interval. Composition rewrites every
target and factor by name; numeric indices never cross a component boundary.
Read ports expose existing values without adding a writer or an evolution rule.
"""
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np

from .engine import State
from .tensor import GearType, Tensor


@dataclass(frozen=True)
class Component:
    name: str
    tensor: Tensor
    purpose: str
    label: str | None = None


class ChannelAssembly:
    """Allocate once; never recycle, alias, or overwrite another owner's state.

    This is a direct sum, not a declaration of physical coupling. Coupled
    equations must already be present in the owning component's tensor.
    Components cannot write or read another component implicitly. This keeps
    experimental clocks and message receivers out of Einstein's source.
    """

    def __init__(self, components, *, max_channels=None):
        components = tuple(components)
        if not components:
            raise ValueError('at least one component is required')
        if max_channels is not None and (type(max_channels) is not int or max_channels < 1):
            raise ValueError('max_channels must be a positive integer')
        names, spans, gears, terms = set(), {}, [], []
        for component in components:
            name = component.name
            if type(name) is not str or not name.isidentifier():
                raise ValueError('component namespace must be an identifier')
            if name in names:
                raise ValueError(f'duplicate component owner {name!r}')
            if not isinstance(component.tensor, Tensor):
                raise TypeError('each component must supply a complete Tensor')
            names.add(name)
            start = len(gears)
            tensor = component.tensor
            local_names = tensor.names
            qualify = lambda local: name + '.' + local
            gears.extend(GearType(qualify(g.name), component.label or g.label,
                                  g.link, g.sign, g.sign_why) for g in tensor.gears)
            spans[name] = (start, len(gears))
            if max_channels is not None and len(gears) > max_channels:
                raise ValueError(f'channel budget exceeded: {len(gears)} > {max_channels}')
            for monomial in tensor.monomials:
                term = (qualify(local_names[monomial.target]), monomial.coeff,
                        tuple((qualify(local_names[f.gear]), f.offset, f.field)
                              for f in monomial.factors))
                why = tensor.is_designated(monomial)
                terms.append(term + ({'designated_one_way': why},) if why else term)
        self.components = components
        self.spans = MappingProxyType(spans)
        self.tensor = Tensor(gears, terms, strict_support=True)
        self._components = MappingProxyType({c.name: c for c in components})
        # Every retained channel has exactly one owner, including unused gears.
        self.owners = tuple(c.name for c in components for _ in c.tensor.gears)
        for m in self.tensor.monomials:
            if any(self.owners[f.gear] != self.owners[m.target] for f in m.factors):
                raise ValueError('undeclared cross-component access')

    def channel(self, owner, local_name):
        """Resolve an owner's symbolic address; reject raw numeric aliasing."""
        if type(local_name) is not str:
            raise TypeError('channel address must be a local symbolic name')
        component = self._components[owner]
        component.tensor.gear_index(local_name)
        return self.tensor.gear_index(owner + '.' + local_name)

    def read_port(self, owner, local_name):
        """A declared passive address, not a second writer or physical source."""
        index = self.channel(owner, local_name)
        return MappingProxyType({'owner': owner, 'channel': index,
                                 'name': self.tensor.names[index], 'access': 'read-only'})

    def pack(self, seeds):
        if set(seeds) != set(self.spans):
            raise ValueError('one complete seed is required for every component, with no extras')
        L = next(iter(seeds.values())).L
        for component in self.components:
            seed = seeds[component.name]
            if seed.L != L or seed.G != component.tensor.G:
                raise ValueError(f'seed shape does not match owner {component.name!r}')
        arrays = [np.concatenate([getattr(seeds[c.name], field).astype(object)
                                  for c in self.components], axis=0)
                  for field in ('a', 'b', 'r')]
        return State(L, *arrays)

    def extract(self, state, owner):
        if state.G != self.tensor.G:
            raise ValueError('state does not match the assembled channel count')
        first, stop = self.spans[owner]
        return State(state.L, *(getattr(state, f)[first:stop].copy() for f in ('a', 'b', 'r')))

    def manifest(self, *, include_channels=True):
        result = {'schema': 'Universe24-channels-v1', 'total_channels': self.tensor.G,
                  'integer_registers_per_node': 3 * self.tensor.G,
                  'allocation': 'disjoint retained intervals; no channel reuse',
                  'cross_component_dynamics': 'none; physical coupling is inside the Einstein component',
                  'components': [dict(owner=c.name, start=self.spans[c.name][0],
                                      stop=self.spans[c.name][1], channels=c.tensor.G,
                                      purpose=c.purpose, source_fingerprint=c.tensor.fingerprint)
                                 for c in self.components]}
        if include_channels:
            result['channels'] = [dict(index=i, name=g.name, owner=self.owners[i],
                                       label=g.label, link=g.link)
                                  for i, g in enumerate(self.tensor.gears)]
        return result
