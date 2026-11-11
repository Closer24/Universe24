"""Quadratic Einstein-Maxwell charged-scalar/dust candidate in temporal gauge.

Use D_mu Phi = partial_mu Phi - g A_mu J Phi, J(phi,chi)=(-chi,phi),
and F_i0=E_i. A0,A1,A2 here are SPATIAL frame components, not A_time;
the temporal potential is fixed to zero. Xi are gauge-covariant gradients.
This is classical charged matter, not Dirac matter or annihilation dynamics.
"""
from fractions import Fraction as F

from . import matter_equations as neutral

AXES = range(3)


def rename(name):
    return name.replace('Psi_', 'Xi_')


FIELDS = tuple(rename(name) for name in neutral.FIELDS_WITH_MAXWELL)+tuple(f'A{a}' for a in AXES)


def equations(fields, partial, *, coupling=1, mass_squared=1, cosmological=0):
    """Return closed degree<=2 RHS, explicit constraints, and diagnostics.

    No gradient or Gauss constraint is projected after an Engine update.
    The only electromagnetic current is the scalar's covariant Noether current;
    dust remains neutral and normal-comoving.
    """
    g = F(coupling)
    aliases = {name: fields[rename(name)] for name in neutral.FIELDS_WITH_MAXWELL}
    rhs, constraints, diagnostic = neutral.equations(
        aliases,lambda name,a:partial(rename(name),a),
        mass_squared=mass_squared,cosmological=cosmological,maxwell=True)
    rhs = {rename(name):value for name,value in rhs.items()}
    B = [[fields[f'B{a}{i}'] for i in AXES] for a in AXES]
    K = [[fields[f'K{min(a,b)}{max(a,b)}'] for b in AXES] for a in AXES]
    potential = [fields[f'A{a}'] for a in AXES]
    scalar = [fields['phi'],fields['chi']]
    pi = [fields['Pi_phi'],fields['Pi_chi']]
    xi = [[fields[f'Xi_{name}{a}'] for a in AXES] for name in ('phi','chi')]

    def gamma(a,b,c):
        return 0 if a == b else (1 if a<b else -1)*fields[f'G{min(a,b)}{max(a,b)}{c}']

    def direction(name,a):
        return sum(B[a][i]*partial(name,i) for i in AXES)

    charge = -g*diagnostic['charge']
    current = [g*(scalar[0]*xi[1][a]-scalar[1]*xi[0][a]) for a in AXES]
    for component,name in enumerate(('phi','chi')):
        # J acting on a two-vector: component0=-component1, component1=component0.
        other,sign = 1-component,(-1 if component == 0 else 1)
        rhs[f'Pi_{name}'] -= g*sum(potential[a]*sign*xi[other][a] for a in AXES)
        for a in AXES:
            rhs[f'Xi_{name}{a}'] += -g*potential[a]*sign*pi[other]+g*fields[f'E{a}']*sign*scalar[other]
            constraints[f'gradient_{name}{a}'] += g*potential[a]*sign*scalar[other]
        for a in AXES:
            for b in range(a+1,3):
                faraday = sum(neutral.epsilon(a,b,c)*fields[f'M{c}'] for c in AXES)
                constraints[f'curl_{name}{a}{b}'] += (-g*potential[a]*sign*xi[other][b]
                    +g*potential[b]*sign*xi[other][a]+g*faraday*sign*scalar[other])
    for a in AXES:
        rhs[f'A{a}'] = sum(K[a][b]*potential[b] for b in AXES)-fields[f'E{a}']
        rhs[f'E{a}'] -= current[a]
        curl_a = sum(neutral.epsilon(a,b,c)*(direction(f'A{c}',b)-sum(
            gamma(d,c,b)*potential[d] for d in AXES)) for b in AXES for c in AXES)
        constraints[f'magnetic_potential{a}'] = fields[f'M{a}']-curl_a
    constraints['Gauss_E'] -= charge
    diagnostic.update(electric_charge=charge,electric_current=current,
                      scalar_electromagnetically_gauged=True)
    return rhs,constraints,diagnostic
