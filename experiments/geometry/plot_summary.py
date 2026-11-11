"""Plot only committed numerical evidence; no trajectory changes or fitted values."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import numpy as np

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-prefix',type=Path,default=root/'runs/geometry/clock_geometry_summary')
args=parser.parse_args()
args.out_prefix.parent.mkdir(parents=True,exist_ok=True)
clock=json.loads((root/'docs/evidence/metric_clock_gate.json').read_text())
conformal=json.loads((root/'docs/evidence/conformal_metric.json').read_text())
pairs=next(c for c in clock['cases'] if c['F']==128)['relational_clock_pairs']
fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
fig.patch.set_facecolor('#fafbfc')
for ax in axs:
    ax.set_facecolor('#fafbfc')
    ax.spines[['top','right']].set_visible(False)
    ax.grid(axis='y',alpha=.2,zorder=0)
values=[abs(p['minus_one'])*1e6 for p in pairs]
axs[0].bar(range(len(pairs)),values,color=['#187f77' if p['pass'] else '#c65c3d' for p in pairs],zorder=3)
axs[0].set_yscale('log');axs[0].set_ylim(.2,2500)
axs[0].axhline(10,color='#5a6370',linestyle='--',label='Declared tolerance: 10 ppm')
axs[0].set_xticks(range(len(pairs)),[f"{p['A']} / {p['B']}" for p in pairs],rotation=30,ha='right')
axs[0].set_xlabel('Clock coefficient pair')
axs[0].set_ylabel('Absolute double-ratio deviation (ppm)')
axs[0].set_title('Current scalar clock gate: finite-frequency mismatch\nU = 1/64; 32,768 exact updates',loc='left',fontsize=11,pad=15)
for i,v in enumerate(values):axs[0].text(i,v*1.18,f'{v:.3g}',ha='center',fontsize=9)
axs[0].legend(frameon=False,loc='upper left',fontsize=8)

N=[r['parameters']['N'] for r in conformal['results']]
for j,color in enumerate(('#276ba6','#854aa8')):
    errors=[abs(r['clock_ratios'][j]['relative_ratio_error']) for r in conformal['results']]
    axs[1].loglog(N,errors,'o-',color=color,label=f'Scalar clock {j+1}',lw=2)
axs[1].set_xticks(N,[str(n) for n in N])
axs[1].xaxis.set_minor_locator(NullLocator())
axs[1].set_xlabel('Temporal refinement N (a separate fixed tensor per N)')
axs[1].set_ylabel('Relative deviation from rate ratio 2')
axs[1].set_title('Separate conformal construction: measured convergence\nTwo backgrounds; complete exact rewinds',loc='left',fontsize=11,pad=15)
axs[1].legend(frameon=False,fontsize=9)
fig.suptitle('Clock observations constrain a proposed geometry',fontsize=16,x=.04,ha='left')
fig.text(.04,-.035,'Different constructions. These tests do not establish the nonlinear Einstein equations or a gravitational-wave detector.',fontsize=9,color='#4b5563')
fig.savefig(args.out_prefix.with_suffix('.svg'),bbox_inches='tight',metadata={'Date':None})
fig.savefig(args.out_prefix.with_suffix('.png'),bbox_inches='tight',dpi=160)

