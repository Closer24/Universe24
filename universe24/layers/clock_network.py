"""Optional reciprocal clock network made entirely of fixed tensor entries.

The scalar Rule3 engine is unchanged. A master oscillator and sector oscillators
are joined by quadratic springs. Declared complete multiplets couple through
Phi_int = -lambda*c**2*(E-E0)/2, E=sum_i w_i*(b_i+v_i)**2.

The builder checks integer coefficients, locality and the inverse dependency
condition. It cannot infer a physical representation from names: invariance is
conditional on the caller's declared quadratic form being preserved by that
representation. In particular, a norm of electromagnetic gauge potentials is
not a gauge-invariant port. No synchronization, boundedness, gravity, quantum
entanglement or entropy preference follows merely from these constructions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..core.lattice import DIRECTIONS, ZERO
from ..core.tensor import GearType, Tensor


DEFAULT_SECTORS = ('core', 'su2', 'su3', 'u1', 'choice', 'cosmic')


@dataclass(frozen=True)
class InvariantPort:
    """A declared quadratic form on one complete node or oriented-link multiplet.

    ``shifts`` converts stored deviations to full fields. ``weights`` is an
    integer diagonal Gram matrix, not an assertion of Lorentz invariance.
    ``counterterm=None`` chooses sum(w_i*v_i**2), removing the vacuum contribution
    from the clock input. A user-specified integer counterterm is also allowed.
    Negative weights describe an indefinite form and carry no stability promise.
    """
    sector: str
    gears: tuple[str, ...]
    weights: tuple[int, ...] = ()
    shifts: tuple[int, ...] = ()
    coupling: int = 1
    counterterm: int | None = None
    description: str = ''


@dataclass(frozen=True)
class ClockNetwork:
    tensor: Tensor
    source_fingerprint: str
    source_gears: int
    namespace: str
    sectors: tuple[str, ...]
    ports: tuple[InvariantPort, ...]
    clock_coefficient: int
    spring: int
    spatial_spring: int

    def clock_index(self, sector: str = 'master') -> int:
        return self.tensor.gear_index(f'{self.namespace}.{sector}')

    @property
    def linear_clock_interval(self) -> tuple[int, int]:
        """Gershgorin bound for the clock block with all field ports removed."""
        largest_degree = self.spring * len(self.sectors) + 6*self.spatial_spring
        return self.clock_coefficient - 2*largest_degree, self.clock_coefficient


def _normal_port(port: InvariantPort, source: Tensor, sectors) -> InvariantPort:
    if not isinstance(port, InvariantPort) or port.sector not in sectors:
        raise ValueError('each port needs a declared sector')
    gears = tuple(port.gears)
    if not gears or len(set(gears)) != len(gears):
        raise ValueError('a port needs distinct complete-multiplet gear names')
    weights = tuple(port.weights) if port.weights else (1,)*len(gears)
    shifts = tuple(port.shifts) if port.shifts else (0,)*len(gears)
    if len(weights) != len(gears) or len(shifts) != len(gears):
        raise ValueError('weights and affine shifts must match the multiplet')
    if any(type(w) is not int or w == 0 for w in weights):
        raise ValueError('quadratic weights must be nonzero integers')
    if any(type(v) is not int for v in shifts):
        raise ValueError('affine shifts must be integers')
    if type(port.coupling) is not int or port.coupling <= 0:
        raise ValueError('port coupling must be a positive integer')
    if port.counterterm is not None and type(port.counterterm) is not int:
        raise ValueError('counterterm must be an integer or None')
    indices = [source.gear_index(n) for n in gears]
    axes = {source.gears[g].link for g in indices}
    if len(axes) != 1:
        raise ValueError('a port must occupy one node or one oriented physical link')
    E0 = sum(w*v*v for w,v in zip(weights,shifts)) if port.counterterm is None else port.counterterm
    return InvariantPort(port.sector,gears,weights,shifts,port.coupling,E0,port.description)


def build_clock_network(source: Tensor, ports: Sequence[InvariantPort], *,
                        sectors: Sequence[str] = DEFAULT_SECTORS,
                        spring: int, spatial_spring: int = 0,
                        clock_coefficient: int | None = None,
                        namespace: str = 'clocknet', label: str = 'official',
                        strict_support: bool = False) -> ClockNetwork:
    """Append clocks and reciprocal invariant-form couplings before a run.

    Link multiplets use (c_x**2+c_(x+e)**2)*(E_link-E0), with the corresponding
    response at both endpoints. Every ADDED monomial has single-edge physical
    support. ``strict_support=True`` additionally requires the source tensor to
    satisfy this condition; the unchanged default source does not.

    All added reads are old-b reads. Therefore an accepted source's old-a DAG
    stays acyclic, and the same staged Rule3 inverse remains valid. This is a new
    chosen tensor, not a derivation of its constants from Rule3.
    """
    if source.Q is None:
        raise ValueError('clock network needs a declared common Q')
    sectors = tuple(sectors)
    if (not sectors or len(set(sectors)) != len(sectors) or
        any(type(s) is not str or not s.isidentifier() or s == 'master' for s in sectors)):
        raise ValueError('sector names must be unique identifiers other than master')
    if type(namespace) is not str or not namespace.isidentifier():
        raise ValueError('namespace must be an identifier')
    if any(n.startswith(namespace+'.') for n in source.names):
        raise ValueError('clock namespace already exists')
    if type(spring) is not int or spring <= 0:
        raise ValueError('master-sector spring must be a positive integer')
    if type(spatial_spring) is not int or spatial_spring < 0:
        raise ValueError('spatial spring must be a nonnegative integer')
    D = 6*source.Q
    coefficient = D//2 if clock_coefficient is None else clock_coefficient
    if type(coefficient) is not int or not -D < coefficient < D:
        raise ValueError('free clock coefficient must be an integer strictly between -D and D')
    ports = tuple(_normal_port(p,source,sectors) for p in ports)
    gears = list(source.gears)
    indices = {}
    for sector in ('master',)+sectors:
        indices[sector] = len(gears)
        gears.append(GearType(f'{namespace}.{sector}',label))
    extra = []
    def add(target,coefficient,*factors):
        if coefficient:
            extra.append((target,coefficient,tuple((g,off,'b') for g,off in factors)))
    master = indices['master']
    for c in indices.values():
        add(c,coefficient,(c,ZERO))
        if spatial_spring:
            add(c,-6*spatial_spring,(c,ZERO))
            for e in DIRECTIONS:
                add(c,spatial_spring,(c,e))
    for sector in sectors:
        c = indices[sector]
        add(c,-spring,(c,ZERO)); add(c,spring,(master,ZERO))
        add(master,-spring,(master,ZERO)); add(master,spring,(c,ZERO))
    for p in ports:
        c = indices[p.sector]
        members = [source.gear_index(n) for n in p.gears]
        axis = source.gears[members[0]].link
        endpoints = (ZERO,) if axis is None else (ZERO,DIRECTIONS[2*axis])
        # One derivative at each incident link's endpoint, expressed from that
        # endpoint's storage coordinates. No term touches two different links.
        for endpoint in endpoints:
            back = tuple(-v for v in endpoint)
            vacuum_norm = sum(w*v*v for w,v in zip(p.weights,p.shifts))
            add(c,p.coupling*(p.counterterm-vacuum_norm),(c,ZERO))
            for g,w,v in zip(members,p.weights,p.shifts):
                lam = p.coupling*w
                add(c,-lam,(c,ZERO),(g,back),(g,back))
                add(c,-2*lam*v,(c,ZERO),(g,back))
                # u_g = s_g dPhi/db_g, with the documented source field sign.
                signed = lam*source.gears[g].sign
                add(g,-signed,(c,endpoint),(c,endpoint),(g,ZERO))
                add(g,-signed*v,(c,endpoint),(c,endpoint))
    # Prove locality of the additions independently of pre-existing violations.
    Tensor(gears,extra,Q=source.Q,strict_support=True)
    terms = []
    for m in source.monomials:
        term = (m.target,m.coeff,tuple((f.gear,f.offset,f.field) for f in m.factors))
        why = source.designations.get((m.target,m.factors))
        if why:
            term += ({'designated_one_way':why},)
        terms.append(term)
    tensor = Tensor(gears,terms+extra,Q=source.Q,strict_support=strict_support)
    return ClockNetwork(tensor,source.fingerprint,source.G,namespace,sectors,ports,
                        coefficient,spring,spatial_spring)


def one_invariant_ports(system, *, coupling: int = 1,
                        include_gauge_links: bool = False,
                        include_relays: bool = False) -> tuple[InvariantPort, ...]:
    """Explicit optional port catalogue for the current ONE construction.

    Uses complete known multiplets, including the jointly transforming 32-real
    weak doublet. Gauge-link and two-path full-field norms can be enabled; their
    affine shifts come from each gauge builder's declared X0. The EM potentials
    are deliberately absent: their Euclidean norm is not gauge invariant.

    Metric forms admit the cube signed-permutation action with link rebasing;
    full continuous spatial or Lorentz covariance of the dynamics is not asserted. Choice
    rings are internal engineered clocks, not spatial vectors. These declared
    forms do not repair symmetries already broken by other source couplings.
    """
    from .gauge import ALGEBRAS
    ports = []
    def node(sector,names,description,weights=(),shifts=()):
        ports.append(InvariantPort(sector,tuple(names),tuple(weights),tuple(shifts),coupling,
                                   description=description))
    node('core',[f'ref.{g.name}' for g in system.by_name('ref').gears],
         '48-component reference norm, invariant under its signed permutations')
    node('core',[f'{ns}.{g.name}' for ns in ('matter','matter2') for g in system.by_name(ns).gears],
         'complete 32-real weak species doublet norm; both members share one clock')
    metric = system.by_name('metric')
    diagonal = ('h00','hxx','hyy','hzz')
    spatial_off_diagonal = ('hxy','hxz','hyz')
    node('core',[f'metric.{n}' for n in diagonal+spatial_off_diagonal],
         'node part of positive spatial tensor Frobenius form; not Lorentz invariant',
         weights=(1,1,1,1,2,2,2))
    # The complete h0i vector is staggered over three link axes. Include every
    # axis with the same weight/clock and endpoint rule, not one preferred port.
    for axis in ('x','y','z'):
        node('core',[f'metric.h0{axis}'],
             'one axis of the complete staggered h0i vector orbit; all three axes included',weights=(2,))
    higgs = system.by_name('chiral')
    node('core',[f'chiral.{g.name}' for g in higgs.gears],
         'full Higgs quaternion norm',shifts=(higgs.params['v'],0,0,0))
    for ns in ('su2','su3','u1','wsu2'):
        block = system.by_name(ns)
        alg = ALGEBRAS[block.params['group']]
        sector = 'core' if ns == 'wsu2' else ns
        local = {g.name for g in block.gears}
        matter = [f'psi_{component}' for component in alg.mcomp]
        if all(n in local for n in matter):
            node(sector,[f'{ns}.{n}' for n in matter],f'complete {ns} matter norm')
        prefixes = (['Ux','Uy','Uz'] if include_gauge_links else [])
        prefixes += (['Pxy','Pxz','Pyx','Pyz','Pzx','Pzy'] if include_relays else [])
        for prefix in prefixes:
            names = [f'{prefix}_{component}' for component in alg.comp]
            node(sector,[f'{ns}.{n}' for n in names],f'full {ns}.{prefix} field norm',
                 shifts=[block.params['X0'].get(n,0) for n in names])
    for ns in ('arm1','arm2','router','exit'):
        node('choice',[f'{ns}.{g.name}' for g in system.by_name(ns).gears],
             f'complete internal {ns} clock/record norm; no spatial-vector interpretation')
    node('choice',['gate.F'],'scalar front register')
    node('cosmic',['cosmic.M1','cosmic.M2'],'complex reader norm; excludes large hand and static loads')
    return tuple(ports)
