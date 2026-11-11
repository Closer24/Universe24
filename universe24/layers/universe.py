"""One allocated tensor: Einstein physics plus isolated research components."""
from dataclasses import replace

from universe24.core import compose
from universe24.core.channels import ChannelAssembly, Component
from universe24.layers.reference_model import reference_system
from universe24.prepare.reference_model import reference_seed
from universe24.observe.communication import incoming_messages


PROPERTY_GROUPS = {
    'spatial_metric': ('g00', 'g01', 'g02', 'g11', 'g12', 'g22'),
    'extrinsic_curvature': ('K00', 'K01', 'K02', 'K11', 'K12', 'K22'),
    'coordinate_gauge': ('alpha', 'beta0', 'beta1', 'beta2'),
    'complex_scalar': ('phi', 'Pi', 'chi', 'Pi_chi'),
    'dark_dust': ('rho_dark',),
}


class UniverseProgram:
    """Assemble before running. No runtime injection, projection or scheduling.

    Message and probe state is independent of Einstein's physical source.
    The probe has its own test metric and a failed general common-metric gate;
    it must be explicitly selected and never supplies the event-board metric.
    """

    def __init__(self, einstein, parameters, *, communication=True,
                 probe_experiment=False, max_channels=None):
        if type(communication) is not bool or type(probe_experiment) is not bool:
            raise TypeError('component selections must be booleans')
        self.einstein = einstein
        self.parameters = dict(parameters)
        self.communication = communication
        self.probe_experiment = probe_experiment
        parts = [Component('einstein', einstein.tensor,
                           'coupled ADM metric, scalar matter and dark dust')]
        self.message_system = None
        if communication:
            self.message_system = reference_system(communication=True)
            message_tensor = compose(*self.message_system.blocks, strict_support=True)
            parts.append(Component('communication', message_tensor,
                                   'six transport lanes and 48 reference receiver channels; no gravitational source', 'audit'))
        if probe_experiment:
            from universe24.layers.transported_probe import build
            parts.append(Component('probe_experiment', build(),
                                   '26-channel independent test chart; general common-metric gate failed', 'audit'))
        self.assembly = ChannelAssembly(parts, max_channels=max_channels)
        self._mapped = replace(einstein, tensor=self.assembly.tensor,
                               names={wire: 'einstein.' + name for wire, name in einstein.names.items()})

    def __getattr__(self, key):
        return getattr(self._mapped, key)

    def prepare(self, L, integer_inputs):
        seeds = {'einstein': self.einstein.prepare(L, integer_inputs)}
        if self.communication:
            tensor = self.assembly.components[1].tensor
            seeds['communication'], _ = reference_seed(self.message_system, tensor, L)
        if self.probe_experiment:
            from universe24.prepare.transported_probe import prepare
            tensor = self.assembly.components[-1].tensor
            seeds['probe_experiment'] = prepare(tensor, L=L)
        return self.assembly.pack(seeds)

    def channel_manifest(self, *, include_channels=True):
        manifest = self.assembly.manifest(include_channels=include_channels)
        fields = self.parameters['fields']
        manifest['physical_fields_per_event'] = len(fields)
        manifest['property_groups'] = {group: [f for f in members if f in fields]
                                       for group, members in PROPERTY_GROUPS.items()}
        manifest['field_readouts'] = {}
        for step in range(self.parameters['steps'] + 1):
            for name in fields:
                key = f'{step}.{name}'
                value = self.outputs[key]
                manifest['field_readouts'][key] = {
                    part: dict(coefficient_hex=format(term.coefficient, 'x'),
                               channel=None if term.wire is None else self.tensor.gear_index(self.names[term.wire]),
                               register=None if term.wire is None else self.names[term.wire],
                               ready_microtick=0 if term.wire is None else self.ready[term.wire])
                    for part, term in (('numerator', value.num), ('denominator', value.den))}
        manifest['field_alias_policy'] = (
            'Physical outputs are read-only expressions. Equal subexpressions may share immutable retained wires; '
            'no physical field or component writes a shared output slot.')
        manifest['probe_common_metric_validated'] = False if self.probe_experiment else None
        return manifest

    def observe_components(self, before, after, tick, clicks):
        """Read only; computational events are not particles or Einstein null cones."""
        rows = {'microtick': tick, 'components': {}}
        for component in self.assembly.components[1:]:
            lo, hi = self.assembly.spans[component.name]
            selected = (clicks.gear >= lo) & (clicks.gear < hi)
            kinds = clicks.kind[selected]
            rows['components'][component.name] = {
                'changed_triple_clicks': int(selected.sum()),
                'classes': {str(k): int((kinds == k).sum()) for k in (0, 1, 2)}}
        if self.communication:
            rows['messages'] = incoming_messages(before, self.tensor, namespace='communication.comm')
        if self.probe_experiment:
            from universe24.observe.transported_probe import sample
            rows['probe'] = sample(self.assembly.extract(after, 'probe_experiment'),
                                   self.assembly.components[-1].tensor, tick)
            rows['probe']['independent_test_metric'] = True
            rows['probe']['general_common_metric_validated'] = False
        return rows
