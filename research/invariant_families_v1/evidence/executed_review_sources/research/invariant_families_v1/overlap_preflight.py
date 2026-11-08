"""Independent static contract for the four-mask overlap; no native update calls."""
from collections import Counter
import hashlib,itertools,json,time
from pathlib import Path
from research.invariant_families_v1.reference import pattern
from research.component_review.audit import Snapshot
from research.reference.algebra import coupling,DIRECTIONS
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SHA='1c6851a118c1141e5ad983dc2c736f35a858d8c416a7e63caf04ba1ba4339e32'
PRODUCER='7efd85923de1b4d832d455ae8c5a2a1df5394b1c19c657d87bd1ffc20525ebd1'
WRAPPER='7912467c54893d2bfcbe7116675acb98995d132aa41e2770ad4a14c6a6840c95'
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def addresses():return list(itertools.product(range(4),range(4),range(4),range(48)))
def values(a):return pattern('period4',*a),pattern('internal',*a)
def initial(mask):
 return Snapshot(4,(0,0,2),{a:(0,int(mask[0])*values(a)[0]+int(mask[1])*values(a)[1],2) for a in addresses()})

def main():
 from research.invariant_families_v1 import overlap as producer
 p=json.loads(producer.PROTOCOL.read_text());assert H(producer.PROTOCOL)==SHA and H(producer.__file__)==PRODUCER and H(HERE/'overlap_budget.py')==WRAPPER;aa=addresses();cp=coupling((1,1,1));assert tuple(producer.CP.ports)==cp.ports and tuple(producer.CP.weights)==cp.weights;first={};seeds={}
 for a in aa:
  for j in (0,1):assert sum(cp.weights[d][a[3]]*values(tuple((a[k]+delta[k])%4 for k in range(3))+(cp.ports[d][a[3]],))[j] for d,delta in enumerate(DIRECTIONS))==4*values(a)[j]
 for mask in ('00','10','01','11'):
  expected=initial(mask);actual=producer.initial(mask);assert expected==Snapshot(4,tuple(actual.background),{a:tuple(v) for a,v in actual.cells.items()});seeds[mask]=[expected.at(a) for a in aa];first[mask]=[(v[1],*divmod(8*v[1]+2,6)) for v in seeds[mask]]
 assert all(all(v[2]==2 for v in s) for s in seeds.values());assert all(seeds['11'][k][1]-seeds['10'][k][1]-seeds['01'][k][1]+seeds['00'][k][1]==0 for k in range(len(aa)));D=[[first['11'][k][j]-first['10'][k][j]-first['01'][k][j]+first['00'][k][j] for k in range(len(aa))] for j in range(3)];expected=[1 if values(a)==(1,1) else -1 if values(a)==(-1,-1) else 0 for a in aa];assert D[0]==[0]*3072 and D[1]==expected and D[2]==[-6*x for x in expected];assert Counter(D[1])=={1:128,-1:128,0:2816}
 report=dict(passed=True,protocol_sha256=SHA,producer_sha256=PRODUCER,wrapper_sha256=WRAPPER,reviewer_sha256=H(__file__),reference_sha256=H(HERE/'reference.py'),new_native_forward_inverse_updates=0,full_initials_checked=4,addresses_per_initial=3072,first_counter_defect_counts=dict(Counter(D[1])),first_remainder_defect_counts=dict(Counter(D[2])),readout_review='All4 fixed controls, fullH12 data and unfiltered C, no prediction invented for later joint evolution. Native checkpoint precedes decoding. Whole producer20CPU and separate audit10CPU must be checked with startup included; no resource ceiling is silently increased.',cpu_seconds_including_imports=time.process_time())
 path=HERE/'evidence/overlap_independent_preflight.json'
 with path.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(report))
if __name__=='__main__':main()
