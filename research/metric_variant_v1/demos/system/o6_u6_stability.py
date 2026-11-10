import sys, time, json, random
sys.path.insert(0, '/home/user/Universe24')
from datetime import datetime, timezone
from research.metric_variant_v1.layers.onematter import build_one_matter
from research.metric_variant_v1.core.tensor import compose
from research.metric_variant_v1.core.engine import Engine, State, OBJ
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.observe.onematter import OneMatterView
Q=(1<<29)+1; A=int(__import__("os").environ.get("U6_A", 1 << 14)); L=3
AMPS=tuple(int(x) for x in sys.argv[1:]) or (4000, 8000)
LAM=int(__import__("os").environ.get("U6_LAM", 4))
SPRING=__import__("os").environ.get("U6_SPRING", "frobenius")
om=build_one_matter(Q=Q, lam=LAM, A=A, kd=(1 << 27)//A, kw=(1 << 24)//A, spring=SPRING); T=compose(*om.blocks); E=Engine(T,Q); V=OneMatterView(T,Q,A)
out={}
for amp in AMPS:
    rng=random.Random(3)
    s=vacuum_state(T,Q,L,*om.blocks); a,b,r=s.a.astype(OBJ),s.b.astype(OBJ),s.r.astype(OBJ)
    for i,nm in enumerate(T.names):
        am = amp if nm.startswith("q") else 8
        a[i]=[rng.randint(-am,am) for _ in range(27)]; b[i]=[rng.randint(-am,am) for _ in range(27)]; r[i]=[rng.randrange(6*Q) for _ in range(27)]
    s=State(L,a,b,r)
    worst=0.0; series=[]; t0=time.time(); run=None
    A2=6*A*A
    for t in range(int(__import__("os").environ.get("U6_STEPS", 500))):
        s=E.step(s)
        n2=V.link_norm2(s); hi=max(int(v) for v in n2.ravel()); lo=min(int(v) for v in n2.ravel())
        dev=max(abs((hi/A2)**0.5-1),abs((lo/A2)**0.5-1)); worst=max(worst,dev)
        if t%50==49: series.append((t+1, round(dev,4), round(V.link_unitarity(s),4)))
        if (hi/A2)**0.5>4: run=t+1; break
    out[f"amp{amp}"]={"worst_frobenius_dev":worst,"runaway_at":run,"series(t,dev,unitarity_defect)":series,"seconds":round(time.time()-t0,1),"pyint_steps":E.stats["pyint_steps"]}
    print(amp, out[f"amp{amp}"], flush=True)
out["stamp_utc"]=datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")
json.dump(out, open('/home/user/Universe24/research/metric_variant_v1/results/system/O6_u6_stability_A' + str(A) + '_lam' + str(LAM) + '_' + SPRING + '_' + '_'.join(map(str, AMPS)) + '_T' + __import__('os').environ.get('U6_STEPS', '500') + '.json','w'), indent=1)
