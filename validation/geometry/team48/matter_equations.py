"""Research-only sourced first-order frame equations; no Engine update here.

Units c=8*pi*G=1, signature -+++, K_ab=-<nabla_a n,e_b>, Pi=n(phi).
The full 24-field Fermi-frame geometry plus complex scalar, normal dust and
optional independent source-free Maxwell field has 35 or 41 fields. All RHS
terms are of degree <=2, before any reversible integer encoding. Continuum
identities and constraints do NOT imply their discrete preservation.
"""
from fractions import Fraction as F

from universe24.algebra.frame_equations import FIELDS as GEOMETRY_FIELDS
from universe24.algebra.frame_equations import equations as vacuum_equations

AXES = range(3)
SCALARS = ('phi', 'chi')
SCALAR_FIELDS = tuple(name for field in SCALARS
                      for name in (field, f'Pi_{field}', *(f'Psi_{field}{a}' for a in AXES)))
DUST_FIELDS = ('rho_dust',)
MAXWELL_FIELDS = tuple(f'{field}{a}' for field in ('E', 'M') for a in AXES)
FIELDS = GEOMETRY_FIELDS + SCALAR_FIELDS + DUST_FIELDS
FIELDS_WITH_MAXWELL = FIELDS + MAXWELL_FIELDS


def epsilon(a, b, c):
    return 0 if len({a, b, c}) < 3 else ((b-a)*(c-a)*(c-b))//2


def equations(fields, partial, *, mass_squared=1, cosmological=0, maxwell=False):
    """Return RHS, constraints, diagnostic in the unrotated Fermi frame.

    partial(name,i) is a coordinate derivative, not a frame derivative. The
    scalar and Maxwell subsystems interact only through geometry. Scalar U(1)
    is global; it is not an electromagnetic charge/current in this model.
    rho_dust is normal-comoving, so dust itself has j_a=S_ab=0. Other fields
    carry nonzero energy flux and anisotropic stress.
    """
    mass_squared, cosmological = F(mass_squared), F(cosmological)
    rhs, constraints, ricci = vacuum_equations(fields, partial)
    B = [[fields[f'B{a}{i}'] for i in AXES] for a in AXES]
    K = [[fields[f'K{min(a,b)}{max(a,b)}'] for b in AXES] for a in AXES]
    trace = sum(K[a][a] for a in AXES)

    def gamma(a, b, c):
        return 0 if a == b else (1 if a < b else -1)*fields[f'G{min(a,b)}{max(a,b)}{c}']

    def direction(name, a):
        return sum(B[a][i]*partial(name, i) for i in AXES)

    def divergence(names):
        return sum(direction(names[a], a)-sum(gamma(b, a, a)*fields[names[b]]
                                             for b in AXES) for a in AXES)

    def curl(names, a):
        return sum(epsilon(a,b,c)*(direction(names[c],b)-sum(
            gamma(d,c,b)*fields[names[d]] for d in AXES)) for b in AXES for c in AXES)

    components = [(fields[name], fields[f'Pi_{name}'],
                   [fields[f'Psi_{name}{a}'] for a in AXES]) for name in SCALARS]
    pi2 = sum(pi*pi for _, pi, _ in components)
    psi2 = sum(v*v for _, _, psi in components for v in psi)
    potential = F(1,2)*mass_squared*sum(phi*phi for phi, _, _ in components)
    dust = fields['rho_dust']
    rho = F(1,2)*(pi2+psi2)+potential+dust
    momentum = [-sum(pi*psi[a] for _, pi, psi in components) for a in AXES]
    stress = [[sum(psi[a]*psi[b] for _, _, psi in components)
               + int(a==b)*(F(1,2)*(pi2-psi2)-potential) for b in AXES] for a in AXES]

    for name, (phi, pi, psi) in zip(SCALARS, components):
        gradient_names = [f'Psi_{name}{a}' for a in AXES]
        rhs[name] = pi
        rhs[f'Pi_{name}'] = divergence(gradient_names)+trace*pi-mass_squared*phi
        for a in AXES:
            rhs[f'Psi_{name}{a}'] = direction(f'Pi_{name}', a)+sum(K[a][b]*psi[b] for b in AXES)
            constraints[f'gradient_{name}{a}'] = psi[a]-direction(name,a)
        for a in AXES:
            for b in range(a+1,3):
                constraints[f'curl_{name}{a}{b}'] = direction(gradient_names[b],a)-direction(gradient_names[a],b)-sum(
                    (gamma(c,b,a)-gamma(c,a,b))*psi[c] for c in AXES)
    rhs['rho_dust'] = trace*dust

    rho_em = F(0)
    if maxwell:
        en, mn = [f'E{a}' for a in AXES], [f'M{a}' for a in AXES]
        electric, magnetic = [fields[n] for n in en], [fields[n] for n in mn]
        rho_em = F(1,2)*sum(e*e+m*m for e,m in zip(electric,magnetic))
        rho += rho_em
        for a in AXES:
            momentum[a] += sum(epsilon(a,b,c)*electric[b]*magnetic[c] for b in AXES for c in AXES)
            rhs[en[a]] = curl(mn,a)+trace*electric[a]-sum(K[a][b]*electric[b] for b in AXES)
            rhs[mn[a]] = -curl(en,a)+trace*magnetic[a]-sum(K[a][b]*magnetic[b] for b in AXES)
            for b in AXES:
                stress[a][b] += int(a==b)*rho_em-electric[a]*electric[b]-magnetic[a]*magnetic[b]
        constraints['Gauss_E'], constraints['Gauss_M'] = divergence(en), divergence(mn)

    stress_trace = sum(stress[a][a] for a in AXES)
    for a in AXES:
        for b in range(a,3):
            rhs[f'K{a}{b}'] -= stress[a][b]-F(1,2)*int(a==b)*(stress_trace-rho)+int(a==b)*cosmological
    constraints['H'] -= 2*rho+2*cosmological
    for a in AXES:
        constraints[f'M{a}'] -= momentum[a]
    return rhs, constraints, {'rho':rho,'momentum':momentum,'stress':stress,
                              'rho_maxwell':rho_em,'potential':potential,'ricci':ricci,
                              'charge':fields['phi']*fields['Pi_chi']-fields['chi']*fields['Pi_phi']}
