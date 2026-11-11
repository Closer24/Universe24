"""Plot saved observations only; never produce or modify an engine state."""
from pathlib import Path
import argparse
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('runs/recurrent-bursts/verified-grid'))
    parser.add_argument('--out',type=Path,default=Path('runs/recurrent-bursts/diagnostics.svg'))
    args=parser.parse_args(argv)
    datasets=[json.loads((args.input/name/'report.json').read_text())
              for name in ('baseline_L5','periodic_control')]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','svg.hashsalt':'recurrent-bursts-v1'})
    fig, axes=plt.subplots(2,2,figsize=(11,6.5),layout='constrained')
    colors=('#266b99','#b85b22')
    titles=('Current communication model, L=5','Exact periodic-shell control, L=7')
    for col,(data,color,title) in enumerate(zip(datasets,colors,titles)):
        rows=[row for row in data['samples'] if row['update']<=70]
        times=[row['update'] for row in rows]
        concentration=[int(row['compact_ball_mass'])/int(row['reference_mass'])
                       if int(row['reference_mass']) else float('nan') for row in rows]
        axes[0,col].plot(times,concentration,color=color,lw=2)
        axes[0,col].axhline(.75,color='#555',ls='--',lw=1,label='compact threshold')
        axes[0,col].axhline(.5,color='#aaa',ls=':',lw=1,label='dispersed threshold')
        axes[0,col].set(title=title,ylim=(0,1.05),ylabel='Reference mass in one face ball')
        axes[0,col].legend(fontsize=8,loc='lower right')
        axes[1,col].plot(times,[row['site_pattern_types'] for row in rows],color=color,lw=2,
                         label='Distinct nonzero site sign patterns')
        axes[1,col].plot(times,[row['persistent_pattern_types'] for row in rows],color='#555',ls='--',
                         label='Patterns fixed for three observations')
        axes[1,col].set(xlabel='Computational update',ylabel='Pattern types',ylim=(0,None))
        axes[1,col].legend(fontsize=8,loc='best')
        for ax in axes[:,col]:
            ax.grid(alpha=.15)
            ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Message recurrence does not establish cumulative complexity',fontsize=15)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.out,metadata={'Date':None})
    if args.out.suffix == '.svg':
        args.out.write_text('\n'.join(line.rstrip() for line in args.out.read_text().splitlines())+'\n')
    fig.savefig(args.out.with_suffix('.png'),dpi=150)


if __name__=='__main__':
    main()
