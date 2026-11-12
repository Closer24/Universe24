"""Native first-order centered quotient pipeline; exact Engine audit.

The currently certified scheduler has period nine and division depths one/two.
The polynomial force is prepared once; no runtime quotient/force callback runs.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
from math import lcm
from pathlib import Path
import hashlib
import json

import numpy as np
import sympy as s

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def clock9():
    names = ('native.fast', 'native.slow')
    fast, slow = names
    terms = [(fast, 3, ()), (fast, -3, ((fast,ZERO,'b'),)),
        (slow,-3,((slow,ZERO,'b'),)),
        (slow,9,((fast,ZERO,'b'),(slow,ZERO,'b'))),
        (slow,3,((fast,ZERO,'b'),)),
        (slow,3,((fast,ZERO,'a'),(slow,ZERO,'b')))]
    # Derive the finite preparation orbit with independent scalar arithmetic.
    aa, bb = [0,0], [0,0]
    records = []
    for _ in range(9):
        records.append((aa[0],bb[0],aa[1],bb[1]))
        uu = [3-3*bb[0], -3*bb[1]+9*bb[0]*bb[1]+3*bb[0]+3*aa[0]*bb[1]]
        aa, bb = bb, [uu[j]//3-aa[j] for j in range(2)]
    assert aa == bb == [0,0]
    addresses = ((fast,'a'),(fast,'b'),(slow,'a'),(slow,'b'))
    products = [()] + [(i,) for i in range(4)] + list(combinations_with_replacement(range(4),2))
    matrix = s.Matrix([[s.prod(row[i] for i in term) for term in products] for row in records])
    _, pivots = matrix.rref()
    basis = matrix[:,list(pivots)]
    assert basis.det() in (-1,1)
    return names, tuple(terms), addresses, tuple(products), tuple(pivots), basis.inv()


def pulse_terms(name, values):
    """Exact integer quadratic preparation of a complete period-nine pulse."""
    _, _, addresses, products, pivots, inverse = clock9()
    target = s.Matrix([values[(j+1)%9]+values[(j-1)%9] for j in range(9)])
    coefficients = inverse*target
    assert all(c.q == 1 for c in coefficients)
    return [(name, 3*int(c), tuple((addresses[i][0],ZERO,addresses[i][1])
             for i in products[p])) for p,c in zip(pivots,coefficients) if c]


@dataclass(frozen=True)
class NativeProgram:
    tensor: Tensor
    fields: tuple
    depth: int
    amplitude: int
    force_multiplier: int
    copy_divide: bool
    pulses: tuple
    sign_index: int
    work_start: int
    copy_phase: int

    @property
    def dt(self):
        return F(self.force_multiplier*self.amplitude, 2*3**(self.depth+int(self.copy_divide)))


def build(fields, equation_builder, *, depth=2, amplitude=3, copy_divide=True):
    """Compile any rational onsite quadratic first-order vector field.

    This law implements a rounded centered first-order update, not the previous
    second-order potential drift/kick. Its convergence budget is separate.
    """
    fields = tuple(fields)
    if type(depth) is not int or depth not in (1,2):
        raise ValueError('Only quotient depths one and two have a certified period-nine scheduler')
    if type(amplitude) is not int or amplitude <= 0 or type(copy_divide) is not bool:
        raise ValueError('Positive integer preparation amplitude and boolean copy flag required')
    if not fields or len(fields) != len(set(fields)):
        raise ValueError('Unique nonempty field names required')
    symbolic = dict(zip(fields,s.symbols('x:'+str(len(fields)))))
    result = equation_builder(symbolic)
    if set(result) != set(fields):
        raise ValueError('The equation builder must define exactly every declared field')
    polys = [s.Poly(s.expand(result[name]), *symbolic.values()) for name in fields]
    if any(p.total_degree() > 2 for p in polys):
        raise ValueError('This counted pipeline accepts degree at most two')
    coefficients = [c for p in polys for c in p.coeffs()]
    if any(not c.is_Rational for c in coefficients):
        raise ValueError('Force coefficients must be exact rational constants')
    multiplier = lcm(*(int(c.q) for c in coefficients))
    names = ['native.'+name for name in fields]
    data_names = names[:]
    work_start = len(names)
    names += [f'native.work.{level}.{name}' for level in range(depth) for name in fields]
    clock_names, clock_terms, *_ = clock9()
    names += list(clock_names)
    sign_name = 'native.sign'; names.append(sign_name)
    sign_index = names.index(sign_name)
    copy_phase = 4*((depth+3)//4)
    pulses = []
    for level in range(depth):
        values = [0]*9
        values[level] = 1
        values[4*depth-3*level] = -1
        pulses.append((f'native.gate.{level}', tuple(values)))
    copy_values = tuple(int(j == copy_phase) for j in range(9))
    pulses.append(('native.copy',copy_values))
    names += [name for name,_ in pulses]
    if len(names) > 48:
        raise ValueError(f'Complete allocation exceeds48 channels: {len(names)}')
    terms = list(clock_terms)
    for name, values in pulses:
        terms += pulse_terms(name, values)
    for i,name in enumerate(fields):
        for powers, coeff in polys[i].terms():
            degree = sum(powers)
            factors = [('native.gate.0',ZERO,'b')]
            if degree == 1:
                factors.append((sign_name,ZERO,'a'))
            factors += [(data_names[j],ZERO,'b') for j,power in enumerate(powers) for _ in range(power)]
            terms.append((f'native.work.0.{name}',int(multiplier*coeff)*amplitude**(2-degree),tuple(factors)))
        for level in range(1,depth):
            terms.append((f'native.work.{level}.{name}',1,
                ((f'native.gate.{level}',ZERO,'b'),(f'native.work.{level-1}.{name}',ZERO,'b'))))
        delay = copy_phase-(depth-1)
        # Free work rotations after its only compute pulse.
        layer = 'b' if delay % 2 else 'a'
        orient = 1 if delay % 4 in (1,2) else -1
        terms.append((data_names[i],orient*(1 if copy_divide else 3),
            (('native.copy',ZERO,'b'),(sign_name,ZERO,'b'),(f'native.work.{depth-1}.{name}',ZERO,layer))))
    tensor = Tensor([GearType(name,label='audit') for name in names],terms,strict_support=True)
    return NativeProgram(tensor,fields,depth,amplitude,multiplier,copy_divide,
                         tuple(pulses),sign_index,work_start,copy_phase)


def prepare(program, previous, current, *, L=3, work_remainder=3):
    n, nodes = len(program.fields), L**3
    previous, current = np.asarray(previous,dtype=object), np.asarray(current,dtype=object)
    if previous.shape != (n,nodes) or current.shape != (n,nodes):
        raise ValueError('Complete scaled integer slices are required')
    if type(work_remainder) is not int or not 0 <= work_remainder < 6:
        raise ValueError('Workspace remainder must be a legal retained integer')
    aa = np.zeros((program.tensor.G,nodes),dtype=object); bb=aa.copy()
    aa[:n], bb[:n] = -previous, current
    aa[program.sign_index]=1;bb[program.sign_index]=1
    rr = np.array([[(g+j)%6 for j in range(nodes)] for g in range(program.tensor.G)],dtype=object)
    rr[n:n*(program.depth+1)] = work_remainder
    for name,values in program.pulses:
        g=program.tensor.names.index(name); aa[g]=values[-1];bb[g]=values[0]
    return State(L,aa,bb,rr)


def decoded(program,state):
    n=len(program.fields);sa=int(state.a[program.sign_index,0]);sb=int(state.b[program.sign_index,0])
    assert sa in (-1,1) and sb in (-1,1)
    assert np.all(state.a[program.sign_index]==sa) and np.all(state.b[program.sign_index]==sb)
    return -sb*state.a[:n].astype(object),sa*state.b[:n].astype(object)


def quadratic_einstein(values, *, dust_energy=F(1)):
    v,p,momentum,r,tau = (values[name] for name in ('v','P','Pi','r','T'))
    return {'v':-F(3,2)*v*p,'P':-r*r-dust_energy*v,
            'Pi':-v*r,'r':v*momentum-F(3,2)*p*r,'T':v}


def macro_expected(program,state,equation_builder):
    """Independent reduced oracle: force arithmetic and quotient stages only."""
    n=len(program.fields);oldprev,oldnow=decoded(program,state)
    sb=int(state.b[program.sign_index,0]);out=np.empty_like(oldnow);carry=np.empty_like(oldnow)
    for node in range(state.N):
        values={name:F(int(oldnow[i,node]),program.amplitude) for i,name in enumerate(program.fields)}
        force=equation_builder(values)
        for i,name in enumerate(program.fields):
            initial=program.force_multiplier*program.amplitude**2*force[name]
            assert initial.denominator == 1
            value=int(initial)
            for level in range(program.depth):
                value=(2*value+int(state.r[program.work_start+level*n+i,node]))//6
            quotient,remainder=divmod(2*(1 if program.copy_divide else 3)*sb*value+int(state.r[i,node]),6)
            out[i,node]=oldprev[i,node]+sb*quotient;carry[i,node]=remainder
    return oldnow,out,carry


def sourced_audit():
    fields=('v','P','Pi','r','T')
    program=build(fields,quadratic_einstein,depth=2,amplitude=3,copy_divide=True)
    # Constrained instantaneous values; second-slice preparation is Euler Taylor
    # from initial data, not an injected future solution or a constraint reset.
    current_values={'v':F(1),'P':F(-2),'Pi':F(0),'r':F(2),'T':F(0)}
    initial_force=quadratic_einstein(current_values)
    def rounded(value):return (2*value.numerator+value.denominator)//(2*value.denominator)
    current=np.array([[rounded(program.amplitude*current_values[name])]*27 for name in fields],dtype=object)
    previous=np.array([[rounded(program.amplitude*(current_values[name]-program.dt*initial_force[name]))]*27 for name in fields],dtype=object)
    seed=prepare(program,previous,current,work_remainder=3)
    engine=Engine(program.tensor);state=seed;rows=[]
    for macro in range(1,7):
        expected=macro_expected(program,state,quadratic_einstein)
        for _ in range(9):
            before=state;state=engine.step(state)
            assert engine.inverse_step(state).same_as(before)
        old,now=decoded(program,state)
        assert np.array_equal(old,expected[0]) and np.array_equal(now,expected[1])
        assert np.array_equal(state.r[:5],expected[2])
        for g in range(5,program.tensor.G):
            if g!=program.sign_index:
                for arr,initial in zip((state.a,state.b,state.r),(seed.a,seed.b,seed.r)):
                    assert np.array_equal(arr[g],initial[g])
        values={name:F(int(now[i,0]),program.amplitude) for i,name in enumerate(fields)}
        constraint=-F(3,4)*values['P']**2+F(1,2)*(values['Pi']**2+values['r']**2)+values['v']
        rows.append({'macro':macro,'lambda':str(macro*program.dt),
            'fields':{name:str(value) for name,value in values.items()},
            'constraint':str(constraint),'positive_volume':values['v']>0,
            'max_bits':max(abs(int(v)).bit_length() for arr in (state.a,state.b,state.r) for v in arr.flat)})
    assert engine.rewind(state,54).same_as(seed)
    assert any(row['constraint']!='0' for row in rows)
    return {'status':'passed_mechanics_failed_exact_constraint','channels':program.tensor.G,
        'degree':program.tensor.rank-1,'dt':str(program.dt),'amplitude':program.amplitude,
        'dust_energy':'1','tensor_sha256':program.tensor.fingerprint,
        'nodes':27,'macros':6,'microticks':54,'macro_oracle_and_full_rewind':True,
        'complete_workspace_restored':True,'rows':rows,
        'exact_constraint_preservation':'failed','fixed_time_refinement':'not_tested'}


def audit():
    rows=[]
    fields=('x','y')
    def force(z):return {'x':2*z['x']*z['y']-3*z['y']+2,'y':-z['x']**2+z['x']}
    for depth in (1,2):
      for divide in (False,True):
       program=build(fields,force,depth=depth,amplitude=3,copy_divide=divide)
       for carry in range(6):
        previous=np.array([[j%7-3 for j in range(27)],[(j//3)%7-3 for j in range(27)]],dtype=object)
        current=np.array([[j%5-2 for j in range(27)],[(j//5)%5-2 for j in range(27)]],dtype=object)
        seed=prepare(program,previous,current,work_remainder=carry)
        engine=Engine(program.tensor);state=seed;peak=0
        # A single macro has large enough signed data to exercise every rounding branch.
        oldprev,oldnow=decoded(program,state)
        n=len(fields);sa=int(state.a[program.sign_index,0]);sb=int(state.b[program.sign_index,0])
        out=np.zeros_like(oldnow)
        rr=np.zeros_like(oldnow)
        for node in range(27):
            physical={name:F(int(oldnow[i,node]),program.amplitude) for i,name in enumerate(fields)}
            f=force(physical)
            for i,name in enumerate(fields):
                value=int(program.force_multiplier*program.amplitude**2*f[name])
                for _ in range(depth):value=(2*value+carry)//6
                inp=(1 if divide else 3)*sb*value
                quotient,remainder=divmod(2*inp+int(state.r[i,node]),6)
                out[i,node]=oldprev[i,node]+sb*quotient;rr[i,node]=remainder
        for tick in range(9):
            old=state;state=engine.step(state)
            assert engine.inverse_step(state).same_as(old)
            peak=max(peak,max(abs(int(v)).bit_length() for arr in (state.a,state.b,state.r) for v in arr.flat))
        prev,now=decoded(program,state)
        assert np.array_equal(prev,oldnow) and np.array_equal(now,out)
        assert np.array_equal(state.r[:n],rr)
        for g in range(n,program.tensor.G):
            if g!=program.sign_index:
                for arr,initial in zip((state.a,state.b,state.r),(seed.a,seed.b,seed.r)):
                    assert np.array_equal(arr[g],initial[g]),(g,program.tensor.names[g])
        assert engine.rewind(state,9).same_as(seed)
        rows.append({'depth':depth,'copy_divide':divide,'work_remainder':carry,
            'channels':program.tensor.G,'degree':program.tensor.rank-1,'macro_oracle':True,
            'complete_workspace_and_pulses_restored':True,'full_rewind':True,
            'peak_bits':peak,'dt':str(program.dt),'tensor_sha256':program.tensor.fingerprint})
    sourced=build(('v','P','Pi','r','T'),quadratic_einstein,depth=2,amplitude=3)
    return {'status':'passed_native_first_order_depth_one_two', 'rows':rows,
            'actual_sourced_first_order_system':sourced_audit(),
            'sourced_quadratic_allocation':{'channels':sourced.tensor.G,'degree':sourced.tensor.rank-1,
                'tensor_sha256':sourced.tensor.fingerprint,'dt':str(sourced.dt)},
            'not_established':['fixed-time sourced refinement','constraint preservation',
                'depth3_and_higher_scheduler','cubic_spinor_force_compilation'],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    result=audit();path=ROOT/'runs/unified_law/03_native_scheduler.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
