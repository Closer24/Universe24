"""Six-channel exact native massless scalar+dust FLRW volume sector.

Only the unchanged Engine advances retained state. Roots/logarithms belong to
the separate passive physical decoder. This is not the massive/general model.
Run: python -m validation.sourced_map.native
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PIN = "f4f64e062f07b3ca119eccf655df746be206908b"
NAMES = ("volume", "dust_charge", "scalar_charge", "reference_velocity", "scalar_offset", "proper_tick")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def exact_fraction(value, name):
    if type(value) not in (int, F):
        raise TypeError(f"{name} must be an exact Python int or Fraction")
    return F(value)


def exact_integer(value, name):
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact Python integer")
    return value


def native_tensor():
    terms = [(name, 6, ((name, ZERO, "b"),)) for name in NAMES]
    terms.append(("volume", 18, (("dust_charge", ZERO, "b"),)))
    return Tensor([GearType(name, label="audit") for name in NAMES], terms, strict_support=True)


@dataclass(frozen=True)
class NativeProgram:
    N: int
    tensor: Tensor

    @property
    def h(self):
        return F(1, self.N)


def build_native(N):
    exact_integer(N, "N")
    if N <= 0:
        raise ValueError("N must be positive; physical step is h=1/N")
    return NativeProgram(N, native_tensor())


def _program_check(program):
    if not isinstance(program, NativeProgram):
        raise TypeError("expected NativeProgram")
    exact_integer(program.N, "N")
    if program.N <= 0 or program.tensor.fingerprint != native_tensor().fingerprint:
        raise ValueError("program must carry the exact six-channel volume tensor and positive N")


def _domain(V, U, D, P, Uref, h):
    if D <= 0 or P == 0 or V <= 0:
        raise ValueError("declared mixed expanding chart requires D>0, P!=0, V>0")
    threshold = F(3, 2)*P*P
    if U <= 0 or U*U <= threshold or Uref <= 0 or Uref*Uref <= threshold:
        raise ValueError("current/reference velocity must lie above the positive scalar branch root")
    # Both retained volume slices belong to the declared expanding history.
    previous_V = V-h*U+F(3, 4)*D*h*h
    previous_U = U-F(3, 2)*D*h
    if previous_V <= 0 or previous_U <= 0 or previous_U*previous_U <= threshold:
        raise ValueError("retained previous physical slice leaves the expanding positive-volume chart")


def prepare_native(program, *, L=3, V=F(1), U=F(3), D=1, P=2, phi_ref=0, remainders=None):
    """Prepare complete past/current data; no future trajectory or projection.

    V,U may be rational provided 4N²V and 4NU are integral. D,P and phi_ref
    are exact integers in fixed declared units. The constraint is reported,
    not imposed or repaired by this function.
    """
    _program_check(program)
    exact_integer(L, "L")
    lat = lattice(L)
    V, U = exact_fraction(V, "V"), exact_fraction(U, "U")
    D, P, phi_ref = (exact_integer(value, name) for value, name in ((D, "D"), (P, "P"), (phi_ref, "phi_ref")))
    _domain(V, U, D, P, U, program.h)
    W, J = 4*program.N**2*V, 4*program.N*U
    if W.denominator != 1 or J.denominator != 1:
        raise ValueError("physical preparation is not exactly integral at the declared static scales")
    W, J = int(W), int(J)
    current = (W, D, P, J, phi_ref, 0)
    previous = (W-J+3*D, D, P, J, phi_ref, -1)
    a = np.asarray([[value]*lat.N for value in previous], dtype=object)
    b = np.asarray([[value]*lat.N for value in current], dtype=object)
    if remainders is None:
        r = np.asarray([[(node+gear) % 6 for node in range(lat.N)] for gear in range(6)], dtype=object)
    else:
        r = np.asarray(remainders, dtype=object)
        if r.shape != (6, lat.N) or any(type(value) is not int or not 0 <= value < 6 for value in r.flat):
            raise ValueError("provide a complete exact Python-integer remainder array of shape(6,L³), values0..5")
    state = State(L, a, b, r)
    read_conserved(program, state)
    return state


def read_conserved(program, state):
    """Decode current geometry/source coordinates from actual retained history.

    Does not recover V or U from elapsed ticks and the initial seed. Does not
    require the constraint to vanish, so off-constraint controls remain visible.
    Nonuniform carries are allowed; physical a,b fields must be homogeneous.
    """
    _program_check(program)
    if not isinstance(state, State) or state.G != 6 or state.N != state.L**3:
        raise ValueError("complete six-channel State required")
    for array in (state.a, state.b, state.r):
        if array.shape != (6, state.N):
            raise ValueError("state array shape differs from complete allocation")
        if any(isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) for value in array.flat):
            raise TypeError("all retained entries must be exact integers")
    if any(not 0 <= int(value) < 6 for value in state.r.flat):
        raise ValueError("invalid retained remainder")
    for array in (state.a, state.b):
        if any(any(int(value) != int(row[0]) for value in row) for row in array):
            raise ValueError("physical FLRW claim requires homogeneous full a,b fields")
    a, b = [int(value) for value in state.a[:,0]], [int(value) for value in state.b[:,0]]
    if any(a[i] != b[i] for i in range(1, 5)) or b[5]-a[5] != 1:
        raise ValueError("source/reference/offset histories must be frozen and proper-time counter must advance by one")
    W, D, P, reference, phi_ref, tick = b
    J = W-a[0]+3*D
    V, U, Uref = F(W, 4*program.N**2), F(J, 4*program.N), F(reference, 4*program.N)
    _domain(V, U, D, P, Uref, program.h)
    invariant = J*J-12*D*W-24*program.N**2*P*P
    return {"V": V, "U": U, "D": D, "P": P, "Uref": Uref,
            "phi_ref": phi_ref, "tau": F(tick, program.N), "invariant": invariant}


def scalar_step(state, *, source_coupling=True):
    """Independent direct scalar recurrence, no Tensor evaluation or plan."""
    a, b, r = (np.zeros((6, state.N), dtype=object) for _ in range(3))
    for node in range(state.N):
        for gear in range(6):
            u = 6*int(state.b[gear,node])
            if gear == 0 and source_coupling:
                u += 18*int(state.b[1,node])
            quotient, carry = divmod(2*u+int(state.r[gear,node]), 6)
            a[gear,node], b[gear,node], r[gear,node] = int(state.b[gear,node]), quotient-int(state.a[gear,node]), carry
    return State(state.L, a, b, r)


def _json_read(values):
    return {key: str(value) if isinstance(value, F) else value for key, value in values.items()}


def _peak_bits(state):
    return max(abs(int(value)).bit_length() for array in (state.a,state.b,state.r) for value in array.flat)


def audit_case(N, *, V=F(1), U=F(3), D=1, P=2, phi_ref=0, uniform_remainder=None):
    program = build_native(N)
    carries = None if uniform_remainder is None else [[uniform_remainder]*27 for _ in range(6)]
    seed = prepare_native(program, V=V, U=U, D=D, P=P, phi_ref=phi_ref, remainders=carries)
    state, engine = seed.copy(), Engine(program.tensor)
    initial = read_conserved(program, seed)
    require(initial["invariant"] == 0, "positive audit seed must satisfy the exact source constraint")
    steps = N//8
    require(N % 8 == 0 and steps >= 3, "audit requires >=3 steps ending at proper time1/8")
    trace = [seed.to_dict()]
    reads = [_json_read(initial)]
    peak = _peak_bits(seed)
    comparisons = 0
    for step in range(1, steps+1):
        old, before = state, read_conserved(program, state)
        state = engine.step(state)
        require(state.same_as(scalar_step(old)), "complete scalar register oracle differs")
        require(engine.inverse_step(state).same_as(old), "single-step complete inverse differs")
        require(np.array_equal(state.r, seed.r), "a legal carry was changed or discarded")
        after = read_conserved(program, state)
        expected_V = before["V"]+program.h*before["U"]+F(3,4)*D*program.h**2
        expected_U = before["U"]+F(3,2)*D*program.h
        require((after["V"],after["U"]) == (expected_V,expected_U), "independent physical macro oracle differs")
        require(after["invariant"] == 0, "exact physical constraint drifted")
        require(after["tau"] == F(step,N), "proper-time counter differs")
        require(state.b[0,0] != old.b[0,0], "volume failed to evolve nontrivially")
        for key in ("D","P","Uref","phi_ref"):
            require(after[key] == initial[key], "source/reference invariant changed")
        trace.append(state.to_dict())
        reads.append(_json_read(after))
        peak = max(peak,_peak_bits(state))
        comparisons += 3*6*state.N
    require(engine.rewind(state,steps).same_as(seed), "complete rewind differs")
    require(Tensor.from_dict(program.tensor.to_dict(),strict_support=True).fingerprint == program.tensor.fingerprint,
            "immutable tensor serialization changed")
    return {"N":N,"steps":steps,"proper_final_time":"1/8","P":P,"D":D,
            "initial_volume":str(V),"initial_velocity":str(U),"phi_ref":phi_ref,
            "carry_preparation":"all_six_at_each_channel" if uniform_remainder is None else uniform_remainder,
            "tensor_fingerprint":program.tensor.fingerprint,"complete_seed":seed.to_dict(),
            "complete_trace":trace,"readouts":reads,"scalar_integer_comparisons":comparisons,
            "all_step_inverses_and_full_rewind":True,"all_declared_carries_retained":True,
            "no_workspace_or_scheduler_channels":True,"exact_constraint_at_every_macro":True,
            "maximum_retained_bits":peak}


def negative_controls():
    program, results = build_native(24), {}
    def reject(name, callback):
        try:
            callback()
        except (ValueError,TypeError) as error:
            results[name] = {"status":"rejected","reason":str(error)}
        else:
            raise AssertionError(f"invalid input {name} accepted")
    reject("float_scale",lambda:build_native(24.0))
    reject("boolean_scale",lambda:build_native(True))
    reject("float_physical_seed",lambda:prepare_native(program,V=1.0))
    reject("nonintegral_scaled_seed",lambda:prepare_native(program,V=F(1,7)))
    reject("undeclared_zero_dust_chart",lambda:prepare_native(program,D=0))
    reject("undeclared_zero_scalar_chart",lambda:prepare_native(program,P=0))
    reject("negative_volume",lambda:prepare_native(program,V=-1))
    reject("past_slice_outside_chart",lambda:prepare_native(build_native(1)))
    reject("invalid_remainder",lambda:prepare_native(program,remainders=[[6]*27 for _ in range(6)]))
    seed=prepare_native(program)
    nonuniform=seed.copy();nonuniform.b[0,1]+=1
    reject("inhomogeneous_flrw_readout",lambda:read_conserved(program,nonuniform))
    source_history=seed.copy();source_history.a[1,0]+=1
    reject("source_history_not_frozen",lambda:read_conserved(program,source_history))
    # Move both volume histories: momentum unchanged, constraint genuinely nonzero.
    off=seed.copy();off.a[0]+=1;off.b[0]+=1
    engine=Engine(program.tensor)
    invariants=[read_conserved(program,off)["invariant"]]
    for _ in range(3):
        off=engine.step(off);invariants.append(read_conserved(program,off)["invariant"])
    require(invariants==[-12]*4,"off-constraint defect was changed or repaired")
    results["off_constraint_no_projection"]={"status":"preserved_nonzero_defect","invariant_by_step":invariants}
    # Delete the actual source response, retaining the same independently prepared source.
    broken=Tensor([GearType(name,label="audit") for name in NAMES],
                  [(name,6,((name,ZERO,"b"),)) for name in NAMES],strict_support=True)
    state=seed.copy();broken_engine=Engine(broken);defects=[]
    for _ in range(3):
        old=state;state=broken_engine.step(state)
        require(state.same_as(scalar_step(old,source_coupling=False)),"broken-law oracle differs")
        defects.append(read_conserved(program,state)["invariant"])
    require(all(value!=0 for value in defects),"source-disconnection negative did not fail")
    require(broken_engine.rewind(state,3).same_as(seed),"broken-law inverse failed")
    results["removed_dust_geometry_coupling"]={"status":"constraint_gate_failed_as_expected",
        "invariant_by_step":defects,"complete_rewind_still_passes":True}
    return results


def main():
    cases=[audit_case(N) for N in (24,48,96)]
    cases += [audit_case(24,P=-2,D=2,V=F(1,2),phi_ref=-1)]
    # A constrained scalar intervention at the same V=1,D=1: the scalar
    # charge changes from2 to22, so the physical constraint fixes U=27.
    cases += [audit_case(96,P=22,U=F(27))]
    cases += [audit_case(24,uniform_remainder=r) for r in range(6)]
    require(len({case["tensor_fingerprint"] for case in cases})==1,"resolution changed the tensor")
    paths=["validation/sourced_map/native.py","universe24/core/engine.py","universe24/core/tensor.py","universe24/core/lattice.py"]
    tensor=native_tensor()
    result={"schema":"universe24/sourced-map/native/1","source_pin":SOURCE_PIN,
        "status":"exact_native_massless_mixed_source_sector_passed","tensor":tensor.to_dict(),
        "allocation":{"channels":6,"retained_integer_entries_per_node":18,"terms":len(tensor),
            "degree":tensor.rank-1,"workspace_channels":0,"scheduler_channels":0,
            "proper_time_coordinate_channels":1,"reference_anchor_channels":2,
            "strict_single_face_support":not tensor.support_violations()},
        "names":NAMES,"cases":cases,"negative_controls":negative_controls(),
        "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
        "limits":["mass_squared=0 only; massive scalar cannot keep P conserved",
            "homogeneous expanding mixed scalar+dust chart only",
            "B,d,phi require declared passive root/log coordinate reconstruction",
            "proper_tick is a coordinate counter, not an independent operational clock",
            "no spatial gradients, general Einstein acceptance or detector claims"]}
    out=ROOT/"runs/sourced_map/native.json";out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"out":str(out),"status":result["status"],"allocation":result["allocation"],
        "cases":len(cases),"scalar_integer_comparisons":sum(c["scalar_integer_comparisons"] for c in cases),
        "maximum_retained_bits":max(c["maximum_retained_bits"] for c in cases)}))


if __name__=="__main__":
    main()
