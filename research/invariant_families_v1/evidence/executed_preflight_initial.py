"""Independent prospective review; constructing initial boards does not evolve them."""
import hashlib,itertools,json,time
from pathlib import Path
from research.invariant_families_v1 import reference
from research.component_review.audit import Snapshot
from research.clock_selection.audit import native_digest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROTOCOL_SHA='f0340b86b689d681cc37cfd76e9e8617cd4f400ea1cb868fa94d00ff7471f523'
PRODUCER_SHA='556b7adc1bff1a0cefc420c9e796f3fa19e35059f04c1857c4289dd87487c6be'
BUDGET_SHA='8758a85953d0fd925fb7658a2c1d592adca7af2cdadf0f86ea1611fdb345eef4'
NAMES={'uniform':'uniform','spatial_period3':'period3','spatial_period4':'period4','internal_yy':'internal'}
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def planned():
 result=[]
 for name,r,(a,b) in itertools.product(NAMES,range(6),((0,1),(2,-1))):
  ref=NAMES[name];L=reference.side(ref);result.append(dict(id=f'{name}-L{L}-r{r}-a{a}-b{b}',pattern=name,side=L,**{'lambda':reference.eigenvalue(ref)},a=a,b=b,r=r,steps=18))
 return result


def expected_initial(case):return reference.state(NAMES[case['pattern']],case['a'],case['b'],case['r'])


def main():
 start=time.process_time();from research.invariant_families_v1 import run as producer
 assert H(HERE/'protocol.json')==PROTOCOL_SHA and H(HERE/'run.py')==PRODUCER_SHA and H(HERE/'budget.py')==BUDGET_SHA;p=json.loads((HERE/'protocol.json').read_text());cases=planned();assert cases==list(producer.cases(p));operator,negative=reference.operator_checks();internal=reference.internal_operator_family_checks();rows=[]
 for case in cases:
  seed=expected_initial(case);native=producer.initial(case,p);actual=Snapshot(case['side'],tuple(native.background),{a:tuple(v) for a,v in native.cells.items()});assert seed==actual
  trace,quotients=reference.orbit(NAMES[case['pattern']],case['a'],case['b'],case['r'],18);assert trace==producer.scalar_trace(case)
  for old,new,ell in zip(trace,trace[1:],quotients):
   a,b,r=old;assert reference.conjugate_remainder(reference.conjugate_remainder(r))==r;q,s=divmod(-2*case['lambda']*b+reference.conjugate_remainder(r),6);assert q==-ell and s==reference.conjugate_remainder(new[2]);recovered_r=(new[2]-2*case['lambda']*new[0])%6;recovered_ell=(2*case['lambda']*new[0]+recovered_r-new[2])//6;assert (recovered_ell-new[1],new[0],recovered_r)==old
  rows.append(dict(case=case,initial_native_sha256=native_digest(seed),complete_initial_equal=True,scalar_trace=[list(v) for v in trace],scalar_forward_inverse_and_J_equal=True))
 note=ROOT/'research/clock_selection/invariant_families_algebra.md';assert H(note)=='62d1572ac61cbce6a581ba663befb18bfe28058f066c61f75380686c8d49e170';report=dict(passed=True,new_native_forward_or_inverse_updates=0,registered_cases=len(rows),protocol_sha256=PROTOCOL_SHA,producer_sha256=PRODUCER_SHA,budget_wrapper_sha256=BUDGET_SHA,reviewer_sha256=H(__file__),reference_sha256=H(HERE/'reference.py'),reviewed_math_note_sha256=H(note),independent_math_review_sha256=H(HERE/'independent_math_review.md'),exact_pattern_operator_checks=operator,internal_operator_family_checks=internal,signed_same_pattern_negative_control=negative,cases=rows,scope='All48 complete initial boards and scalar traces independently constructed. The fixed+++ native batch tests6base remainders atj0, two seeds andH18, not arbitrary generalized6q remainders or signed native dynamics. Global periodic preparations; no no-wrap propagation claim. Complete native checkpoints precede decoding/observation; entire dedicated wrapper and child CPU are bounded. No overlap runs authorized by this preflight.',cpu_seconds=time.process_time()-start)
 out=HERE/'evidence/independent_preflight.json';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,cases=len(rows),operator_checks=len(operator),internal_identities=len(internal),cpu_seconds=report['cpu_seconds'])))
if __name__=='__main__':main()
