"""Construct the compact sourced research tensor, with a hard 48-gear budget.

There is one shared geometric frame and genuine source terms, not a direct
sum of isolated metrics. This is still the audited leapfrog candidate, whose
nonlinear constraint, nondegeneracy and integer-refinement gates are open.
"""
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from experiments.geometry.team48 import geometry_triangular as geometry
from experiments.geometry.team48 import matter_equations as matter
from experiments.geometry.team48 import matter_charged as charged
from experiments.geometry.team48 import matter_dust_square as square
from experiments.geometry.team48 import geometry_positive_pairs as positive
from experiments.geometry.team48 import integer_staggered as staggered
from experiments.geometry.team48.integer_sign_lift import compile_quadratic, invariant_summary


@dataclass(frozen=True)
class Candidate:
    program: object
    model: str
    blocks: tuple

    def manifest(self):
        tensor = self.program.tensor
        paired = self.model == 'charged_positive'
        result = staggered.invariant_summary(self.program) if paired else invariant_summary(self.program)
        result.update(model=self.model, budget=48, available_channels=48-tensor.G,
                      monomials=len(tensor.monomials), fingerprint=tensor.fingerprint,
                      metric_owners=1, separate_communication_channels=0,
                      padding_allocated=False, default_runtime_changed=False,
                      full_nonlinear_einstein_gate=False,
                      constraints_preserved=False,
                      arbitrary_integer_refinement=False,
                      positive_geometry_on_nonzero_wronskian_sector=paired,
                      nonzero_wronskian_requires_computational_second_mode=paired,
                      blocks=[{'name': name, 'channels': len(fields),
                               'indices': [tensor.gear_index('field.'+field) for field in fields]}
                              for name, fields in self.blocks],
                      phase_index=0,
                      channels_by_index=list(tensor.names))
        return result


def build(model='charged', *, dt=1, dx=1, mass_squared=0, cosmological=0,
          coupling=1):
    """Construction only; no external numerical solve or evolution callback."""
    if model not in ('scalar_dust', 'maxwell', 'charged', 'charged_positive'):
        raise ValueError('model must be scalar_dust, maxwell, charged or charged_positive')
    for value in (mass_squared, cosmological, coupling):
        if isinstance(value, (float, bool)):
            raise TypeError('Use exact rational source parameters')
    mass_squared, cosmological, coupling = map(Fraction, (mass_squared, cosmological, coupling))
    if mass_squared < 0:
        raise ValueError('This matter model requires nonnegative mass_squared')
    maxwell = model != 'scalar_dust'
    is_charged = model.startswith('charged')
    paired = model == 'charged_positive'
    selected_geometry = positive if paired else geometry
    scalar_fields = tuple(charged.rename(name) for name in matter.SCALAR_FIELDS) if is_charged else matter.SCALAR_FIELDS
    blocks = [('geometry', selected_geometry.FIELDS), ('complex_scalar', scalar_fields),
              ('normal_dust_amplitude', ('dust_amplitude',))]
    if maxwell:
        blocks.append(('maxwell', matter.MAXWELL_FIELDS))
    if is_charged:
        blocks.append(('spatial_potential', tuple(f'A{a}' for a in range(3))))
    names = tuple(name for _, fields in blocks for name in fields)
    if paired:
        names = positive.replace_fields(square.FIELDS_CHARGED)

    def equations(fields, partial):
        parameters = {'coupling': coupling} if is_charged else {'maxwell': maxwell}
        return selected_geometry.equations(fields, partial, fermi_equations=square.equations,
                                  base_equations=charged.equations if is_charged else matter.equations,
                                  mass_squared=mass_squared, cosmological=cosmological,
                                  **parameters)

    program = (staggered.compile_staggered(names, equations, phase_offsets=positive.phase_offsets(names), dt=dt, dx=dx)
               if paired else compile_quadratic(names, equations, dt=dt, dx=dx))
    if program.tensor.G > 48:
        raise ValueError('The compact candidate exceeds its declared 48-channel budget')
    return Candidate(program, model, tuple(blocks))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/team48/candidate')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    reports = [build(model).manifest() for model in ('scalar_dust', 'maxwell', 'charged', 'charged_positive')]
    (args.out/'channels.json').write_text(json.dumps(reports, indent=2)+'\n')
    print(json.dumps([{key: row[key] for key in ('model', 'channels', 'available_channels',
                                               'monomials', 'full_nonlinear_einstein_gate')}
                      for row in reports], indent=2))
