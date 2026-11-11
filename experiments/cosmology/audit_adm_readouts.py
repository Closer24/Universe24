"""Post-hoc passive bounds on saved ADM physical readouts, not a ref-board test.

Uses outward-rounded reported density extrema to bound a radius-one face ball.
No source field, tensor, state or acceptance threshold is changed.
"""
from pathlib import Path
from fractions import Fraction
from math import inf, nextafter
import argparse
import json


def audit(report):
    parameters=report['parameters']
    L=parameters['L']
    if L < 3 or not parameters.get('dark_matter'):
        raise ValueError('requires the declared dark-matter cube with L >= 3')
    samples=report['samples']
    if not samples or [s['step'] for s in samples] != list(range(len(samples))):
        raise ValueError('complete ordered physical snapshots starting at zero required')
    scale=parameters['scale']
    # Initial fields are integer/scale. With this bound, a reported exact zero
    # cannot be a nonzero initial numerator lost to floating underflow.
    initial_zero_resolvable=type(scale) is int and 0 < scale <= 2**1022
    frozen_zero={k for k in ('beta0','beta1','beta2')
                 if initial_zero_resolvable and samples[0]['field_ranges'][k]==[0.0,0.0]}
    rows=[]
    histories=[]
    for sample in samples:
        low,high=sample['field_ranges']['rho_dark']
        if not 0 < low <= high < inf:
            raise ValueError('positive finite density extrema required')
        lower=Fraction.from_float(nextafter(low,-inf))
        upper=Fraction.from_float(nextafter(high,inf))
        if lower <= 0:
            raise ValueError('density lower bound is not strictly positive')
        fraction=7*upper/(L**3*lower)
        signs=[]
        for name in parameters['fields']:
            lo,hi=sample['field_ranges'][name]
            if lo>0: sign=1
            elif hi<0: sign=-1
            elif lo==hi==0 and (name in frozen_zero or
                 (sample['step']==0 and initial_zero_resolvable)): sign=0
            else: sign=None
            signs.append(sign)
        uniform=all(s is not None for s in signs)
        signature=tuple(signs) if uniform else None
        count=int(any(signs)) if uniform else None
        histories.append(signature)
        persistent=(count if uniform and len(histories)>=3 and
                    all(s==signature for s in histories[-3:]) else 0 if uniform else None)
        rows.append({'physical_step':sample['step'],
                     'dust_ball_fraction_upper_bound':str(fraction),
                     'dust_ball_fraction_upper_bound_float':float(fraction),
                     'every_dust_ball_below_dispersed_threshold':fraction<Fraction(1,2),
                     'uniform_joint_field_sign_pattern':uniform,
                     'site_sign_pattern_types':count,
                     'edge_sign_pattern_types':count,
                     'persistent_sign_pattern_types_across_three_snapshots':persistent})
    return {'scope':'Post-hoc bounds on sampled physical dust and field signs; separate from the ref.* burst protocol.',
            'physical_snapshots':len(rows),'samples':rows,
            'four_reassemblies_established':False if all(r['every_dust_ball_below_dispersed_threshold'] for r in rows) else None,
            'complete_information_recovery':report['complete_rewind_exact'],
            'between_snapshot_reassemblies':'not resolved by these snapshots',
            'limitations':[f'{len(rows)} sampled physical states; events between them remain unresolved.',
                          'Field sign patterns are only the declared structural proxy; they do not capture all geometric variation.',
                          'Microticks compute a finite DAG; they are not additional completed physical time steps.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path)
    parser.add_argument('--out',type=Path,default=Path('runs/einstein-review/physical-readout-audit.json'))
    args=parser.parse_args()
    result=audit(json.loads(args.report.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
