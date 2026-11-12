"""Smooth fixed-domain constrained preparation and independent metric oracle.

Research preparation/validation only. No observer feeds the Engine. The
integer seed uses exact Fraction Taylor arithmetic and integer square roots;
floating conversion occurs only in the explicitly separate diagnostic oracle.
"""
from fractions import Fraction as F
from math import isqrt
import numpy as np

PI = F('3.14159265358979323846264338327950288419716939937510')


def sine_rational(x):
    """Forty Taylor terms on [-pi,pi]; truncation < 1e-78 here."""
    while x > PI:
        x -= 2*PI
    while x < -PI:
        x += 2*PI
    term = total = x
    for k in range(1, 40):
        term *= -x*x / ((2*k)*(2*k+1))
        total += term
    return total


def nearest(value):
    return (2*value.numerator + value.denominator)//(2*value.denominator)


def smooth_integer_seed(names, n=8, resolution=2**24):
    """One periodic x-row on physical [0,1), exact common denominator Q.

    phi=sin(2*pi*x)/16, Pi=2, B=I, K=diag(0,2+phi,2+phi),
    Xi_x=D_h(phi), d=floor(Q*sqrt(k^2-2-Xi_x^2/2))/Q.
    H is nonnegative and <=4*max(d_cont)/Q. M and scalar-gradient
    constraints vanish exactly, even after phi quantization. The d rounding
    is preparation only; its loss is recorded, never performed at runtime.
    """
    if n < 4 or n % 4 or type(resolution) is not int or resolution <= 0:
        raise ValueError('n must be a positive multiple of four; Q a positive integer')
    names = tuple(names)
    values = np.zeros((len(names), n), dtype=object)
    f = dict(zip(names, values))
    q = resolution
    for axis in range(3):
        f[f'B{axis}{axis}'][:] = q
    phi = np.asarray([nearest(q*sine_rational(2*PI*F(j,n))/16)
                      for j in range(n)], dtype=object)
    psi = (n//2)*(np.roll(phi,-1)-np.roll(phi,1))
    k = 2*q+phi
    density_numerator = k*k-2*q*q-psi*psi//2
    if not all(int(p)%2 == 0 for p in psi):
        raise AssertionError('even derivative numerators required')
    if not all(v > 0 for v in density_numerator):
        raise AssertionError('positive dust initial data required')
    f['phi'][:] = phi
    f['Pi_phi'][:] = 2*q
    grad = 'Xi_phi0' if 'Xi_phi0' in f else 'Psi_phi0'
    f[grad][:] = psi
    f['K11'][:] = k
    f['K22'][:] = k
    if 'dust_amplitude' not in f:
        raise ValueError('This common-Q helper is for the signed-square dust field')
    d = np.asarray([isqrt(int(v)) for v in density_numerator],dtype=object)
    f['dust_amplitude'][:] = d
    defects = [F(2*(int(r)-int(a)**2),q*q) for r,a in zip(density_numerator,d)]
    momentum = [-F(2*int(v),q) for v in psi]
    return values, {'domain':[0,1], 'nodes_x':n, 'dx':str(F(1,n)),
                    'common_denominator':q, 'profile':'sin(2*pi*x)/16',
                    'pi_phi':2, 'k':'2+phi', 'minimum_dust_density':str(min(F(int(v)**2,q*q) for v in d)),
                    'initial_H_peak_exact':str(max(defects)),
                    'initial_M0_peak_exact':'0', 'initial_gradient_peak_exact':'0',
                    'initial_abs_jx_peak':str(max(abs(v) for v in momentum)),
                    'quantization':'exact rational Taylor profile, nearest phi integer, integer sqrt dust; preparation only',
                    'continuum_sine_error_bound':'1e-49 before field quantization',
                    'fundamental_seed_arithmetic':'exact integers/Fractions/isqrt'}


def diagnostic_fields(names, numerators, denominator):
    """Convert read-only decoded ratios to float solely for numerical QA."""
    d = np.broadcast_to(np.asarray(denominator,dtype=object), (np.asarray(numerators).shape[1],))
    return {name:np.asarray([float(F(int(v),int(w))) for v,w in zip(row,d)])
            for name,row in zip(names,numerators)}


def literal_metric_constraints(fields, dx):
    """Independent warped-metric ADM observer for diagonal plane symmetry.

    ds3^2 = b^-2 dx^2+c^-2(dy^2+dz^2), K_frame=diag(k,l,l).
    R=-4 C''/C-2(C'/C)^2, C=1/c, prime=b*d/dx.
    Uses no production frame connection, curvature, stress, or constraint code.
    This observer is deliberately different from the frame-connection stencil.
    """
    f={n:np.asarray(v,dtype=float) for n,v in fields.items()}
    b,c,k,l=(f[n] for n in ('B00','B11','K00','K11'))
    for name in ('B01','B02','B12','K01','K02','K12'):
        if name in f and np.max(np.abs(f[name]))>1e-12:
            raise ValueError('plane-diagonal oracle used outside supported sector')
    if not (np.allclose(f['B22'],c,rtol=0,atol=1e-12) and np.allclose(f['K22'],l,rtol=0,atol=1e-12)):
        raise ValueError('transverse isotropy required')
    def D(v):return (np.roll(v,-1)-np.roll(v,1))/(2*float(dx))
    C=1/c
    Cprime=b*D(C)
    Csecond=b*D(Cprime)
    ricci=-4*Csecond/C-2*(Cprime/C)**2
    pi=f['Pi_phi']; psi=f.get('Xi_phi0',f.get('Psi_phi0'))
    rho=0.5*(pi*pi+psi*psi)+f['dust_amplitude']**2
    momentum=-pi*psi
    H=ricci+4*k*l+2*l*l-2*rho
    M=-2*b*D(l)+2*(Cprime/C)*(k-l)-momentum
    gradient=psi-b*D(f['phi'])
    g_metric=-Cprime/C
    torsion=f['G011']-g_metric
    return {'H_linf':float(np.max(np.abs(H))), 'M0_linf':float(np.max(np.abs(M))),
            'gradient_linf':float(np.max(np.abs(gradient))),
            'connection_metric_linf':float(np.max(np.abs(torsion))),
            'metric_det_min':float(np.min(1/(b*b*c**4))),
            'B_diag_min':float(min(np.min(b),np.min(c))),
            'dust_density_min':float(np.min(f['dust_amplitude']**2)),
            'Ricci_scalar_linf':float(np.max(np.abs(ricci))),
            'matter_momentum_linf':float(np.max(np.abs(momentum))),
            'all_finite':bool(all(np.all(np.isfinite(a)) for a in (H,M,gradient,torsion,rho)))}
