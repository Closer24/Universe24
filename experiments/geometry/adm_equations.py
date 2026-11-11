"""Full nonlinear ADM + real Klein-Gordon equations, c=kappa=1.

K_ij=-(partial_t-L_beta)gamma_ij/(2 alpha), Pi=n^mu partial_mu phi.
Six metric and six curvature evolution equations, scalar pair, harmonic
lapse, prescribed time-independent shift, Hamiltonian and momentum constraints.
No symmetry reduction. Central spatial differences on a periodic cube.
"""
from fractions import Fraction
import numpy as np
from experiments.geometry.integer_circuit import Circuit

AXES = range(3)
PAIRS = tuple((i, j) for i in AXES for j in AXES if i <= j)
FIELDS = tuple([f'g{i}{j}' for i, j in PAIRS]+[f'K{i}{j}' for i, j in PAIRS]
               +['alpha', 'phi', 'Pi']+[f'beta{i}' for i in AXES])


def d(value, axis, dx):
    plus = tuple(1 if k == axis else 0 for k in AXES)
    minus = tuple(-v for v in plus)
    return (value.shift(plus)-value.shift(minus))/(2*dx)


def dd(value, i, j, dx):
    # Use the same commuting derivative as in d(Gamma), including i==j.
    # This is a consistent second-order, two-hop stencil. Prefer odd boards:
    # composed central differences have checkerboard null modes on even boards.
    return d(d(value, i, dx), j, dx)


def matrix(fields, prefix):
    return [[fields[f'{prefix}{min(i,j)}{max(i,j)}'] for j in AXES] for i in AXES]


def inverse3(g):
    a, b, c = g[0]
    _, e, f = g[1]
    _, _, k = g[2]
    cof = [[e*k-f*f, c*f-b*k, b*f-c*e],
           [c*f-b*k, a*k-c*c, b*c-a*f],
           [b*f-c*e, b*c-a*f, a*e-b*b]]
    determinant = a*cof[0][0]+b*cof[0][1]+c*cof[0][2]
    return [[v/determinant for v in row] for row in cof], determinant


def system(fields, dx=Fraction(1), mass_squared=Fraction(1), cosmological=Fraction(0), lapse='harmonic'):
    """The same equations can construct a circuit or evaluate passive readouts.

    Central differences of Christoffels give a consistent Ricci approximation;
    symmetrization removes its O(dx^2) antisymmetric product-rule defect.
    """
    dx, mass_squared, cosmological = map(Fraction, (dx, mass_squared, cosmological))
    dark_matter = 'rho_dark' in fields
    if lapse not in ('harmonic','geodesic') or (dark_matter and lapse!='geodesic'):
        raise ValueError('normal-comoving pressureless dust requires geodesic slicing')
    g, K = matrix(fields, 'g'), matrix(fields, 'K')
    alpha, phi, Pi = (fields[name] for name in ('alpha', 'phi', 'Pi'))
    beta = [fields[f'beta{i}'] for i in AXES]
    inv, determinant = inverse3(g)
    dg = [[[d(g[i][j], c, dx) for j in AXES] for i in AXES] for c in AXES]
    gamma = [[[sum(inv[k][l]*(dg[i][l][j]+dg[j][l][i]-dg[l][i][j]) for l in AXES)/2
               for j in AXES] for i in AXES] for k in AXES]
    ricci_raw = [[sum(d(gamma[k][i][j], k, dx)-d(gamma[k][i][k], j, dx)
        + sum(gamma[k][i][j]*gamma[l][k][l]-gamma[k][i][l]*gamma[l][j][k] for l in AXES)
        for k in AXES) for j in AXES] for i in AXES]
    ricci = [[(ricci_raw[i][j]+ricci_raw[j][i])/2 for j in AXES] for i in AXES]
    mixed_K = [[sum(inv[i][j]*K[j][k] for j in AXES) for k in AXES] for i in AXES]
    trace_K = sum(mixed_K[i][i] for i in AXES)
    gradient = [d(phi, i, dx) for i in AXES]
    da = [d(alpha, i, dx) for i in AXES]
    grad_squared = sum(inv[i][j]*gradient[i]*gradient[j] for i in AXES for j in AXES)
    V = mass_squared*phi*phi/2
    rho_dark = fields['rho_dark'] if dark_matter else Fraction(0)
    rho = (Pi*Pi+grad_squared)/2+V+rho_dark
    momentum_density = [-Pi*v for v in gradient]
    stress = [[gradient[i]*gradient[j]+g[i][j]*((Pi*Pi-grad_squared)/2-V)
               for j in AXES] for i in AXES]
    stress_trace = sum(inv[i][j]*stress[i][j] for i in AXES for j in AXES)
    advect = lambda v: sum(beta[k]*d(v, k, dx) for k in AXES)
    dbeta = [[d(beta[k], i, dx) for i in AXES] for k in AXES]
    def lie(tensor, i, j):
        return advect(tensor[i][j])+sum(tensor[k][j]*dbeta[k][i]+tensor[i][k]*dbeta[k][j] for k in AXES)
    def hessian(value, gradient_value, i, j):
        return dd(value, i, j, dx)-sum(gamma[k][i][j]*gradient_value[k] for k in AXES)
    rhs = {}
    for i, j in PAIRS:
        rhs[f'g{i}{j}'] = -2*alpha*K[i][j]+lie(g, i, j)
        rhs[f'K{i}{j}'] = (-hessian(alpha, da, i, j)
            + alpha*(ricci[i][j]+trace_K*K[i][j]-2*sum(K[i][k]*mixed_K[k][j] for k in AXES))
            # For a minimally coupled real scalar this is exactly
            # S_ij - gamma_ij*(S-rho)/2; avoids an inverse-metric cancellation.
            - alpha*(gradient[i]*gradient[j]+(V+rho_dark/2)*g[i][j])
            - cosmological*alpha*g[i][j]+lie(K, i, j))
    rhs['alpha'] = (-alpha*alpha*trace_K if lapse=='harmonic' else alpha*0)+advect(alpha)
    rhs['phi'] = alpha*Pi+advect(phi)
    rhs['Pi'] = (alpha*(sum(inv[i][j]*hessian(phi, gradient, i, j) for i in AXES for j in AXES)
                        + trace_K*Pi-mass_squared*phi)
                 +sum(inv[i][j]*da[i]*gradient[j] for i in AXES for j in AXES)+advect(Pi))
    for i in AXES:
        rhs[f'beta{i}'] = fields[f'beta{i}']*0
    if dark_matter:
        # u_dark=n, pressure=0, D_i alpha=0: covariant rest-mass conservation.
        rhs['rho_dark'] = alpha*trace_K*rho_dark+advect(rho_dark)
    curvature = sum(inv[i][j]*ricci[i][j] for i in AXES for j in AXES)
    constraints = {'H': curvature+trace_K*trace_K
        -sum(mixed_K[i][j]*mixed_K[j][i] for i in AXES for j in AXES)-2*rho-2*cosmological}
    for i in AXES:
        constraints[f'M{i}'] = (sum(d(mixed_K[j][i], j, dx)
            +sum(gamma[j][j][k]*mixed_K[k][i]-gamma[k][j][i]*mixed_K[j][k] for k in AXES)
            for j in AXES)-d(trace_K, i, dx)-momentum_density[i])
    # All spacetime metric components and T come from the evolving fields.
    g4 = [[None]*4 for _ in range(4)]
    g4[0][0] = -alpha*alpha+sum(g[i][j]*beta[i]*beta[j] for i in AXES for j in AXES)
    for i in AXES:
        g4[0][i+1] = g4[i+1][0] = sum(g[i][j]*beta[j] for j in AXES)
        for j in AXES:
            g4[i+1][j+1] = g[i][j]
    gradient4 = [alpha*Pi+sum(beta[i]*gradient[i] for i in AXES)]+gradient
    kinetic = (-Pi*Pi+grad_squared)/2+V
    stress4 = [[gradient4[i]*gradient4[j]-g4[i][j]*kinetic for j in range(4)] for i in range(4)]
    stress4[0][0] += rho_dark*alpha*alpha  # T_dark= rho_dark n_cov n_cov, n_cov=(-alpha,0,0,0).
    return rhs, constraints, {'g4': g4, 'T4': stress4, 'rho': rho, 'det_gamma': determinant,
                              'Ricci3': ricci, 'trace_K': trace_K}


def compile_adm(*, steps=1, dt=Fraction(1, 64), dx=Fraction(1), scale=4096,
                mass_squared=Fraction(1), cosmological=Fraction(0), method='euler',
                dark_matter=False, lapse=None):
    """Compile a chosen finite physical horizon before any Engine step.

    Workspace is retained, not erased. Extending the horizon requires a larger
    prebuilt circuit; this is not a bounded-memory perpetual gravity automaton.
    """
    if type(steps) is not int or steps < 1 or type(scale) is not int or scale < 1:
        raise ValueError('positive integer steps and scale required')
    dt, dx = Fraction(dt), Fraction(dx)
    if dt <= 0 or dx <= 0 or method not in ('euler', 'midpoint'):
        raise ValueError('positive dt/dx and euler or midpoint required')
    circuit = Circuit()
    lapse = ('geodesic' if dark_matter else 'harmonic') if lapse is None else lapse
    names = FIELDS+(('rho_dark',) if dark_matter else ())
    state = {name: circuit.input(name, scale) for name in names}
    outputs = {}
    for step in range(steps+1):
        rhs, constraints, diagnostic = system(state, dx, mass_squared, cosmological, lapse)
        outputs.update({f'{step}.{name}': v for name, v in state.items()})
        outputs.update({f'{step}.constraint.{name}': v for name, v in constraints.items()})
        outputs.update({f'{step}.rhs.{name}': v for name, v in rhs.items()})
        for i in range(4):
            for j in range(i, 4):
                outputs[f'{step}.metric.{i}{j}'] = diagnostic['g4'][i][j]
                outputs[f'{step}.stress.{i}{j}'] = diagnostic['T4'][i][j]
        outputs[f'{step}.det_gamma'] = diagnostic['det_gamma']
        if step == steps:
            break
        if method == 'midpoint':
            middle = {name: state[name]+dt*rhs[name]/2 for name in names}
            rhs, _, middle_diagnostic = system(middle, dx, mass_squared, cosmological, lapse)
            outputs[f'{step}.midpoint.minor1'] = middle['g00']
            outputs[f'{step}.midpoint.minor2'] = middle['g00']*middle['g11']-middle['g01']*middle['g01']
            outputs[f'{step}.midpoint.minor3'] = middle_diagnostic['det_gamma']
            outputs[f'{step}.midpoint.alpha'] = middle['alpha']
        outputs.update({f'{step}.update_rhs.{name}': v for name,v in rhs.items()})
        state = {name: state[name]+dt*rhs[name] for name in names}
    program = circuit.compile(outputs)
    parameters = dict(steps=steps, dt=str(dt), dx=str(dx), scale=scale,
                      mass_squared=str(Fraction(mass_squared)), cosmological=str(Fraction(cosmological)), method=method,
                      dark_matter=dark_matter,lapse=lapse,fields=list(names))
    return program, parameters


class ArrayField:
    """Passive numerical/reference algebra; never a source of Engine updates."""
    def __init__(self, data):
        self.data = np.asarray(data)

    def _value(self, other):
        if isinstance(other, ArrayField):
            return other.data
        return float(other) if self.data.dtype != object else other

    def __add__(self, other): return ArrayField(self.data+self._value(other))
    __radd__ = __add__
    def __neg__(self): return ArrayField(-self.data)
    def __sub__(self, other): return ArrayField(self.data-self._value(other))
    def __rsub__(self, other): return ArrayField(self._value(other)-self.data)
    def __mul__(self, other): return ArrayField(self.data*self._value(other))
    __rmul__ = __mul__
    def __truediv__(self, other): return ArrayField(self.data/self._value(other))
    def __rtruediv__(self, other): return ArrayField(self._value(other)/self.data)
    def shift(self, offset):
        return ArrayField(np.roll(self.data, tuple(-v for v in offset), axis=(0, 1, 2)))


def flat_data(L, scale=4096):
    result = {name: np.zeros((L, L, L), dtype=np.int64) for name in FIELDS}
    for name in ('g00', 'g11', 'g22', 'alpha'):
        result[name][:] = scale
    return result
