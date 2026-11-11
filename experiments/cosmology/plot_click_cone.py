"""Render saved exact click/cone observations; no evolution or feedback."""
from pathlib import Path
from collections import Counter
import argparse
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('runs/click-cone/SUMMARY.json'))
    parser.add_argument('--out',type=Path,default=Path('runs/click-cone/diagnostics.svg'))
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                         'svg.fonttype':'none','svg.hashsalt':'click-cone-v1'})
    fig,axes=plt.subplots(2,2,figsize=(12,7),layout='constrained')
    case=data['cases']['communication'];rows=case['samples'];x=[r['update'] for r in rows]
    axes[0,0].plot(x,[r['C2'] for r in rows],color='#b85b22',lw=2)
    axes[0,0].set(title='Local messages: C2 events continue',ylabel='Official C2 records per update',xlabel='Engine update')
    axes[1,0].plot(x,[r['site_pattern_types'] for r in rows],color='#266b99',lw=2,label='Distinct site sign patterns')
    axes[1,0].plot(x,[r['persistent_pattern_types'] for r in rows],color='#555',ls='--',label='Three-observation persistence')
    axes[1,0].set(title='The measured structural proxy plateaus',ylabel='Pattern types',xlabel='Engine update',ylim=(-4,135))
    axes[1,0].legend(fontsize=8)
    for ax in axes[:,0]:
        ax.axvline(15,color='#777',ls=':',lw=1)
    axes[0,0].text(.04,.92,'L=5, payload=3; dashed line: update 15',transform=axes[0,0].transAxes,fontsize=9)
    cone=data['cones']['single_reference_site']
    points=Counter((p['update'],p['distance']) for p in cone['C2_points'])
    ax=axes[0,1]
    ax.fill_between([0,4],[0,0],[0,4],color='#d7e9f4',alpha=.65)
    ax.plot([0,4],[0,4],color='#266b99',ls='--',label='One-edge-per-update bound')
    for (t,d),count in points.items():
        ax.scatter([t],[d],s=30+9*count**.5,color='#b85b22',zorder=3)
        ax.annotate(str(count),(t,d),xytext=(6,-3),textcoords='offset points',fontsize=8)
    ax.set(title='Changed C2 events stay inside the cone',xlabel='Engine update',ylabel='Distance from perturbed site',xlim=(-.1,4.6),ylim=(-.2,4.5),xticks=range(5),yticks=range(5))
    ax.legend(fontsize=8,loc='upper left')
    ax.text(.04,.68,'Labels count affected sites\nL=9; single-site preparation change',transform=ax.transAxes,fontsize=8)
    cycle=data['cases']['periodic_C2'];rows=cycle['samples'];x=[r['update'] for r in rows]
    ax=axes[1,1]
    ax.step(x,[r['C2']/cycle['L']**3 for r in rows],where='mid',color='#b85b22',label='C2 records per node')
    ax.step(x,[r['site_pattern_types'] for r in rows],where='mid',color='#266b99',ls='--',label='Site sign-pattern types')
    for t in cycle['full_state_returns']:ax.axvline(t,color='#888',ls=':',lw=1)
    ax.set(title='C2-only control: same full state every 3 updates',xlabel='Engine update',ylabel='Counts',xticks=range(0,13,3),ylim=(-.1,1.5))
    ax.legend(fontsize=8,loc='upper right')
    for ax in axes.flat:
        ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False)
    fig.suptitle('C2 follows local dynamics; it does not certify cumulative structure',fontsize=15)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.out,metadata={'Date':None})
    args.out.write_text('\n'.join(line.rstrip() for line in args.out.read_text().splitlines())+'\n')
    fig.savefig(args.out.with_suffix('.png'),dpi=150)


if __name__=='__main__':main()
