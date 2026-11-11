"""Passive matter-frame defects; no dynamic ratio geometry or clock apparatus."""
import numpy as np

from universe24.algebra.frame_matter import sampled
from universe24.core.lattice import lattice
from universe24.observe.frame48 import diagnostics as vacuum_diagnostics


def bank_values(state, bank='Y'):
    if state.G != 70 or bank not in ('X', 'Y'):
        raise ValueError('Extract a 70-channel frame component and select X or Y')
    start = 0 if bank == 'X' else 35
    return state.b[start:start+35].astype(object).copy()


def diagnostics(values, *, L, dx=1, mass_squared=1):
    _, constraints, matter = sampled(values, lattice(L), dx, mass_squared)
    peaks = {name: str(max(abs(v) for v in np.broadcast_to(row, (L**3,))))
             for name, row in constraints.items()}
    geometry = vacuum_diagnostics(values[:24], L=L, dx=dx)
    return {'peak_constraints': peaks,
            'all_discrete_constraints_zero': all(v == '0' for v in peaks.values()),
            'singular_nodes': geometry['singular_nodes'],
            'minimum_abs_det_B': geometry['minimum_abs_det_B'],
            'minimum_rho': str(min(matter['rho'])), 'maximum_rho': str(max(matter['rho'])),
            'negative_dust_nodes': int(np.count_nonzero(matter['rho_dark'] < 0)),
            'peak_energy_balance_defect': str(max(abs(v) for v in matter['energy_balance_defect'])),
            'peak_charge_balance_defect': str(max(abs(v) for v in matter['charge_balance_defect']))}
