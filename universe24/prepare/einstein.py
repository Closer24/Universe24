"""Initial data only: no function here is called during Engine evolution."""
from fractions import Fraction
import numpy as np
from universe24.layers.adm import FIELDS, COMPLEX_FIELDS, ArrayField, system, flat_data


def homogeneous_scalar(L, scale=4096, mass_squared=1):
    data = flat_data(L, scale)
    if mass_squared == 0:
        values = {'K00': Fraction(-1,16), 'K11': Fraction(-1,16), 'K22': Fraction(-1,32),
                  'phi': Fraction(0), 'Pi': Fraction(1,8)}
    elif mass_squared == 1:
        # 2*(Hx*Hy+Hx*Hz+Hy*Hz) = Pi^2 + phi^2, exactly.
        values = {'K00': Fraction(-1,16), 'K11': Fraction(-1,16), 'K22': Fraction(-17,256),
                  'phi': Fraction(1,8), 'Pi': Fraction(3,32)}
    else:
        raise ValueError('this preparation supports mass squared zero or one')
    for name, value in values.items():
        if (value*scale).denominator != 1:
            raise ValueError('scale does not exactly represent initial data')
        data[name][:] = int(value*scale)
    return data


def gauge_wave(L, scale=1<<24, amplitude=1/128, time=0):
    """Flat vacuum in a nontrivial harmonic chart; quantized initial data."""
    data = flat_data(L, scale)
    x = np.arange(L)[:, None, None]/L
    phase = 2*np.pi*(x-time)
    H = 1-amplitude*np.sin(phase)
    alpha = np.sqrt(H)
    values = {'g00': H, 'alpha': alpha, 'K00': -amplitude*np.pi*np.cos(phase)/alpha}
    for name, value in values.items():
        data[name][:] = np.rint(value*scale).astype(np.int64)
    return data


def numeric_fields(integer_data, scale):
    return {name: ArrayField(values.astype(float)/scale) for name, values in integer_data.items()}


def inhomogeneous_scalar(L=3, spatial_bits=24, curvature_bits=24, dark_matter=False, complex_matter=False):
    """Solve the implemented discrete Hamiltonian constraint before quantizing.

    gamma=psi^4 C, K=-k gamma, Pi=0 makes the discrete momentum equation
    identically zero in exact arithmetic. Newton solves H=0 and mean(log psi)=0
    for log psi and the constant k. The final k*gamma proportionality is encoded
    exactly using a common integer denominator; quantization leaves a measured
    Hamiltonian error. A positive lapse and constant shift specify the gauge.
    """
    if L < 3 or L % 2 == 0:
        raise ValueError('use an odd periodic side length to avoid central-stencil checkerboard null modes')
    N = L**3
    xyz = np.indices((L,L,L))/L
    phi = 1/8+sum(np.cos(2*np.pi*xyz[i]) for i in range(3))/256
    rho_dark = (1+np.cos(2*np.pi*xyz[0])*np.cos(2*np.pi*xyz[1])*np.cos(2*np.pi*xyz[2])/4)/512
    names = FIELDS+(COMPLEX_FIELDS if complex_matter else ())+(('rho_dark',) if dark_matter else ())
    # chi=0 and Pi_phi=0 give j_i=0 even with a spatially varying Pi_chi.
    # The two signs of Pi_chi create opposite U(1) charges on the same board.
    pi_chi = np.cos(2*np.pi*xyz[0])/32 if complex_matter else np.zeros_like(phi)
    lapse = 'geodesic' if dark_matter else 'harmonic'
    C = np.array([[1,1/8,1/16],[1/8,1,1/16],[1/16,1/16,1]], dtype=float)
    dx = Fraction(1,L)
    def fields(vector):
        conformal = np.exp(4*vector[:N].reshape(L,L,L))
        k = vector[-1]
        data = {name: np.zeros((L,L,L)) for name in names}
        for i in range(3):
            for j in range(i,3):
                data[f'g{i}{j}'] = conformal*C[i,j]
                data[f'K{i}{j}'] = -k*conformal*C[i,j]
        data['alpha'] = np.ones((L,L,L)) if dark_matter else 1+np.sin(2*np.pi*xyz[0])/128
        data['phi'] = phi
        if complex_matter:data['Pi_chi'] = pi_chi
        if dark_matter:data['rho_dark'] = rho_dark
        data['beta0'][:] = 1/32
        data['beta1'][:] = 1/64
        return {name:ArrayField(value) for name,value in data.items()}
    def residual(vector):
        _, constraints, _ = system(fields(vector), dx, 1, lapse=lapse)
        return np.r_[constraints['H'].data.ravel(), np.mean(vector[:N])]
    vector = np.r_[np.zeros(N), np.sqrt(np.mean(phi*phi+pi_chi*pi_chi+(2*rho_dark if dark_matter else 0))/6)]
    for iteration in range(12):
        current = residual(vector)
        if np.max(np.abs(current)) < 1e-12:
            break
        columns=[]
        for j in range(N+1):
            shifted=vector.copy();shifted[j]+=1e-6
            columns.append((residual(shifted)-current)/1e-6)
        correction=np.linalg.solve(np.array(columns).T,-current)
        vector += correction
    final_residual=float(np.max(np.abs(residual(vector))))
    if final_residual > 1e-10 or vector[-1] <= 0:
        raise ValueError('initial-data Newton solve did not converge to the expanding branch')
    # Every spatial metric component gets a common denominator 2^spatial_bits.
    spatial_scale=1<<spatial_bits; curvature_scale=1<<curvature_bits
    scale=spatial_scale*curvature_scale
    raw=fields(vector)
    integer_data={}
    k_integer=int(round(vector[-1]*curvature_scale))
    for name in names:
        if name.startswith('K'):
            continue
        numerator=np.rint(raw[name].data*spatial_scale).astype(np.int64)
        integer_data[name]=numerator.astype(object)*curvature_scale
        if name.startswith('g'):
            integer_data['K'+name[1:]]=-numerator.astype(object)*k_integer
    return integer_data,scale,{'newton_iterations':iteration,'unquantized_H_max':final_residual,
                               'constant_expansion':str(Fraction(k_integer,curvature_scale)),
                               'scope':'constrained inhomogeneous '+('complex scalar with opposite U(1) charges' if complex_matter else 'real scalar')+(' and pressureless dark dust' if dark_matter else '')+'; fixed periodic topology'}
