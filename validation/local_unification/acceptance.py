"""Independent scalar acceptance of the joined twelve-channel law.

No Engine evolution, candidate gate oracle or canonical decoder is called.
Every monomial, complete transition, algebraic inverse and arithmetic event is
recomputed using explicit scalar periodic indexing. Physical scope stays separate.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
from pathlib import Path
from validation.padding import sector_tensor
from universe24.core import exact_json
from universe24.system.bundle import load_bundle

SCHEMA = "universe24/local-unification/independent-acceptance/1"
PROFILE_NAMES = ("geometry.A.plus", "geometry.A.minus", "geometry.B.plus", "geometry.B.minus")
RAIL_NAMES = tuple(f"local_unification.{bank}.{rail}" for bank in ("A", "B")
                   for rail in ("record_plus", "record_minus", "carrier_plus", "carrier_minus"))

def _dump(value):
    return exact_json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def _hash(value):
    return hashlib.sha256(_dump(value).encode()).hexdigest()

def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result

def _read(text):
    def reject(value):
        raise ValueError(f"noninteger JSON input: {value}")
    return exact_json.loads(text, object_pairs_hook=_pairs, parse_float=reject, parse_constant=reject)

def _records(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                raise ValueError("blank saved record")
            yield _read(line)

def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} requires an exact integer >= {minimum}")
    return value

def _direction(value):
    value = tuple(value)
    if (len(value) != 3 or any(type(v) is not int for v in value)
            or sum(abs(v) for v in value) != 1):
        raise ValueError("one exact unit face direction is required")
    return value

def _coords(node, L):
    return node // (L*L), (node//L) % L, node % L

def _index(xyz, L):
    x, y, z = xyz
    return ((x % L)*L+(y % L))*L+z % L

def _shift(node, offset, L):
    xyz = _coords(node, L)
    return _index(tuple(xyz[i]+offset[i] for i in range(3)), L)

def validate_tensor(tensor, direction=(1, 0, 0)):
    """Compare every coefficient to an independently stated joined law."""
    direction = _direction(direction)
    tensor = sector_tensor(tensor, 12)
    if tensor.G != 12 or tuple(tensor.names) != RAIL_NAMES+PROFILE_NAMES:
        raise ValueError("acceptance requires the complete declared twelve-channel law")
    expected = {}
    def term(target, coefficient, factors):
        key = (target, tuple(sorted((gear, tuple(offset), "b") for gear, offset in factors)))
        expected[key] = expected.get(key, 0)+coefficient
    zero = (0, 0, 0)
    delta = ((1, (0, 3)), (-1, (0, 1, 3)), (-1, (0, 2, 3)),
             (-1, (1, 2)), (1, (0, 1, 2)), (1, (1, 2, 3)))
    for bank in (0, 1):
        source = 4*(1-bank)
        for rail, sign in enumerate((-1, 1, 1, -1)):
            target = 4*bank+rail
            term(target, 3, [(source+rail, zero)])
            for coefficient, inputs in delta:
                term(target, 3*sign*coefficient, [(source+i, zero) for i in inputs])
            velocity = 1 if rail in (0, 2) else -1
            orientation = velocity if bank == 0 else -velocity
            term(target, 3, [(source+rail, tuple(orientation*d for d in direction))])
    for target, source, rails, orientation in (
            (8, 10, (4, 6), -1), (9, 11, (5, 7), 1),
            (10, 8, (0, 2), 1), (11, 9, (1, 3), -1)):
        term(target, 9, [(source, zero)])
        term(target, -3, [(source, tuple(orientation*d for d in direction))])
        for rail in rails:
            term(target, -3, [(rail, zero)])
    actual = {(m.target, tuple(sorted((f.gear, f.offset, f.field) for f in m.factors))): m.coeff
              for m in tensor.monomials}
    if actual != {key: value for key, value in expected.items() if value}:
        raise ValueError("joined tensor differs from independent collision/source specification")
    return True

def _state(data, channels):
    if type(data) is not dict or set(data) != {"L", "a", "b", "r"}:
        raise ValueError("complete state fields required")
    L = _integer(data["L"], "L", 3)
    for field in ("a", "b", "r"):
        rows = data[field]
        if type(rows) is not list or len(rows) != channels:
            raise ValueError("missing state channels")
        for row in rows:
            if type(row) is not list or len(row) != L**3:
                raise ValueError("missing state nodes")
            if any(type(v) is not int or (field == "r" and not 0 <= v < 6) for v in row):
                raise ValueError("state contains noninteger values or illegal carry")
    return data

def scalar_input(tensor, current):
    """Literal polynomial evaluation with independent periodic indices."""
    L = current["L"]
    inputs = [[0]*(L**3) for _ in range(tensor.G)]
    indices = {offset: [_shift(n, offset, L) for n in range(L**3)]
               for offset in {f.offset for m in tensor.monomials for f in m.factors}}
    for monomial in tensor.monomials:
        for node in range(L**3):
            value = monomial.coeff
            for factor in monomial.factors:
                value *= current[factor.field][factor.gear][indices[factor.offset][node]]
            inputs[monomial.target][node] += value
    return inputs

def scalar_step(tensor, before):
    before = _state(before, tensor.G)
    inputs = scalar_input(tensor, before)
    L = before["L"]
    result = {"L": L, "a": [row[:] for row in before["b"]], "b": [], "r": []}
    for channel in range(tensor.G):
        next_b, next_r = [], []
        for node in range(L**3):
            quotient, remainder = divmod(2*inputs[channel][node]+before["r"][channel][node], 6)
            next_b.append(quotient-before["a"][channel][node])
            next_r.append(remainder)
        result["b"].append(next_b)
        result["r"].append(next_r)
    return result

def scalar_inverse(tensor, after):
    """Algebraic inverse for this law's b-only polynomial."""
    after = _state(after, tensor.G)
    if any(f.field != "b" for m in tensor.monomials for f in m.factors):
        raise ValueError("acceptance inverse is proved only for b-only inputs")
    L = after["L"]
    old = {"L": L, "a": [[0]*(L**3) for _ in range(tensor.G)],
           "b": [row[:] for row in after["a"]], "r": [[0]*(L**3) for _ in range(tensor.G)]}
    inputs = scalar_input(tensor, old)
    for channel in range(tensor.G):
        for node in range(L**3):
            z = 6*after["b"][channel][node]+after["r"][channel][node]-2*inputs[channel][node]
            carry = z % 6
            old["r"][channel][node] = carry
            old["a"][channel][node] = (carry-z)//6
    return old

def scalar_clicks(before, after, tensor, run_id, step):
    """Independent canonical construction; never calls decoder.py."""
    for node in range(before["L"]**3):
        for channel in range(tensor.G):
            old = tuple(before[field][channel][node] for field in ("a", "b", "r"))
            new = tuple(after[field][channel][node] for field in ("a", "b", "r"))
            quotient = new[1]+old[0]
            if quotient == 0 or old == new:
                continue
            turn = (new[2]-old[2]) % 6
            if turn not in (0, 2, 4):
                raise ValueError("illegal remainder parity change")
            identity = {"run_id": run_id, "tensor_hash": tensor.fingerprint,
                        "step": step, "node": node, "channel": channel}
            yield {"schema": "universe24/arithmetic-click/1", "event_id": _hash(identity),
                   **identity, "xyz": list(_coords(node, before["L"])),
                   "gear": tensor.names[channel], "label": tensor.labels[channel],
                   "quotient": quotient, "kind": ("C0", "C1", "C2")[turn//2],
                   "sign": 1 if quotient > 0 else -1}

def _collision(row):
    if row == (1, 0, 0, 1):
        return (0, 1, 1, 0)
    if row == (0, 1, 1, 0):
        return (1, 0, 0, 1)
    return row

def inspect_history(states, direction=(1, 0, 0), *, protocol=None):
    """Collision, positive balances, source constraints and macro transport."""
    direction = _direction(direction)
    if not states:
        raise ValueError("complete history required")
    L = states[0]["L"]
    N = L**3
    axis = next(i for i, d in enumerate(direction) if d)
    coordinate = [(_coords(node, L)[axis] if direction[axis] > 0 else L-1-_coords(node, L)[axis])
                  for node in range(N)]
    plus = [_shift(n, direction, L) for n in range(N)]
    minus = [_shift(n, tuple(-d for d in direction), L) for n in range(N)]
    steps = len(states)-1
    if protocol is not None:
        for key in ("L", "microsteps", "ticks_per_macro", "interior_coordinate", "receiver_coordinate"):
            _integer(protocol.get(key), f"protocol {key}")
        _direction(protocol.get("direction", ()))
        if (protocol.get("L") != L or protocol.get("microsteps") != steps
                or tuple(protocol.get("direction", ())) != direction
                or protocol.get("ticks_per_macro") != 2):
            raise ValueError("source protocol does not match exact saved run")
        center = protocol.get("interior_coordinate")
        if protocol.get("receiver_coordinate") != center:
            raise ValueError("source chart and detector coordinates differ")
        if steps % 2 or not steps+3 <= center <= L-1-(steps+3):
            raise ValueError("readout lies outside finite causal chart")
    else:
        center = L//2
    receiver = next(n for n in range(N) if coordinate[n] == center)
    collisions, energy, momentum, populations = [], [], [], []
    balances = constraints = macro_checks = 0
    for tick, state in enumerate(states):
        _state(state, len(state["a"]))
        if len(state["a"]) not in (12, 48):
            raise ValueError("expected 12-sector or 48-channel history")
        if any(value != 0 for field in ("a", "b", "r") for row in state[field][12:] for value in row):
            raise ValueError("nonzero idle research channel")
        if state["L"] != L or any(v not in (0, 1) for row in state["b"][:8] for v in row):
            raise ValueError("packet domain or lattice changed")
        b = state["b"]
        nplus = [sum(b[g][n] for g in (0, 2, 4, 6)) for n in range(N)]
        nminus = [sum(b[g][n] for g in (1, 3, 5, 7)) for n in range(N)]
        populations.append((nplus, nminus))
        energy.append(sum(nplus)+sum(nminus))
        momentum.append(sum(nplus)-sum(nminus))
        if any(np_+nm < abs(np_-nm) for np_, nm in zip(nplus, nminus)):
            raise AssertionError("positive packet-energy inequality failed")
        for node in range(N):
            collision = _collision(tuple(b[g][node] for g in range(4)))
            for rail in range(4):
                source = plus[node] if rail in (0, 2) else minus[node]
                if state["a"][rail][node] != b[4+rail][source]:
                    raise ValueError("first old packet bank is outside invariant sector")
                if state["a"][4+rail][node] != collision[rail]:
                    raise ValueError("second old packet bank is outside invariant sector")
        if protocol is not None:
            for node in range(N):
                if not tick+1 <= coordinate[node] <= L-2-tick:
                    continue
                for row, rails in ((8, (0, 2)), (9, (1, 3)), (10, (4, 6)), (11, (5, 7))):
                    defect = b[row][plus[node]]-2*b[row][node]+b[row][minus[node]]
                    if defect+sum(b[g][node] for g in rails):
                        raise ValueError("same-state source constraint failed inside causal chart")
                    constraints += 1
        if not tick:
            continue
        before = states[tick-1]["b"]
        for node in range(N):
            expected = _collision(tuple(before[g][node] for g in range(4, 8)))
            if tuple(b[g][node] for g in range(4)) != expected:
                raise ValueError("collision differs from independent permutation")
            for rail in range(4):
                incoming = minus[node] if rail in (0, 2) else plus[node]
                if b[4+rail][node] != before[rail][incoming]:
                    raise ValueError("source rail violates declared transport")
            oldE = sum(before[g][node] for g in range(8))
            oldP = sum((1 if g % 4 in (0, 2) else -1)*before[g][node] for g in range(8))
            rightE = before[0][node]+before[2][node]-before[1][plus[node]]-before[3][plus[node]]
            leftE = before[0][minus[node]]+before[2][minus[node]]-before[1][node]-before[3][node]
            rightP = before[0][node]+before[2][node]+before[1][plus[node]]+before[3][plus[node]]
            leftP = before[0][minus[node]]+before[2][minus[node]]+before[1][node]+before[3][node]
            if nplus[node]+nminus[node]-oldE+rightE-leftE:
                raise AssertionError("local energy balance failed")
            if nplus[node]-nminus[node]-oldP+rightP-leftP:
                raise AssertionError("local momentum balance failed")
            balances += 2
        incoming = tuple(before[g][receiver] for g in range(4, 8))
        outgoing = tuple(b[g][receiver] for g in range(4))
        collisions.append({"step": tick, "incoming": list(incoming), "outgoing": list(outgoing),
                           "selection": incoming == (1, 0, 0, 1) and outgoing == (0, 1, 1, 0)})
        if tick >= 2:
            oldplus, oldminus = populations[tick-2]
            if nplus != [oldplus[n] for n in minus] or nminus != [oldminus[n] for n in plus]:
                raise AssertionError("macro directional free-stream theorem failed")
            macro_checks += 2*N
    if len(set(energy)) != 1 or len(set(momentum)) != 1:
        raise AssertionError("global packet accounts changed")
    return {"detector": receiver, "selected_steps": [c["step"] for c in collisions if c["selection"]],
            "all_detector_opportunities": collisions, "energy_by_tick": energy,
            "momentum_by_tick": momentum, "exact_local_balances": balances,
            "interior_source_checks": constraints, "macro_stream_comparisons": macro_checks}

def audit_saved_run(run_dir, *, protocol=None, out=None):
    """Only one actual twelve-channel saved history supplies all evidence."""
    run_dir = Path(run_dir)
    bundle = load_bundle(run_dir/"bundle")
    direction = (1, 0, 0) if protocol is None else tuple(protocol["direction"])
    validate_tensor(bundle.tensor, direction)
    report = _read((run_dir/"validation.json").read_text())
    steps = _integer(report.get("steps"), "steps", 1)
    run_id = _hash({"schema": "universe24/system/run/1", "bundle_id": bundle.bundle_id, "steps": steps})
    if (report.get("schema") != "universe24/system/run/1" or report.get("run_id") != run_id
            or report.get("bundle_id") != bundle.bundle_id or report.get("tensor_hash") != bundle.tensor.fingerprint
            or report.get("channels_per_node") != 48 or report.get("nodes") != bundle.seed.N):
        raise ValueError("saved report is not bound to complete joined bundle")
    for name in ("full_trace.jsonl.gz", "clicks.jsonl.gz"):
        if hashlib.sha256((run_dir/name).read_bytes()).hexdigest() != report.get("files", {}).get(name):
            raise ValueError("saved evidence checksum differs")
    current = bundle.seed.to_dict()
    states = [current]
    saved_clicks = iter(_records(run_dir/"clicks.jsonl.gz"))
    missing = object()
    comparisons = clicks = count = 0
    for count, record in enumerate(_records(run_dir/"full_trace.jsonl.gz"), 1):
        if type(record) is not dict:
            raise ValueError("transition record must be a mapping")
        _integer(record.get("step"), "transition step", 1)
        _state(record.get("before"), 48)
        if (count > steps or record.get("step") != count or record.get("run_id") != run_id
                or record.get("tensor_hash") != bundle.tensor.fingerprint
                or record.get("schema") != "universe24/transition/1"
                or set(record) != {"schema", "run_id", "tensor_hash", "step", "before", "after"}
                or record.get("before") != current):
            raise ValueError("noncontiguous or mixed complete trace")
        after = _state(record["after"], 48)
        if after != scalar_step(bundle.tensor, current):
            raise ValueError(f"independent scalar forward mismatch at step{count}")
        if scalar_inverse(bundle.tensor, after) != current:
            raise ValueError(f"independent scalar inverse mismatch at step{count}")
        comparisons += 2*3*48*current["L"]**3
        for expected_click in scalar_clicks(current, after, bundle.tensor, run_id, count):
            saved = next(saved_clicks, missing)
            if saved is missing or _dump(saved) != _dump(expected_click):
                raise ValueError("independently reconstructed canonical click differs")
            clicks += 1
        states.append(after)
        current = after
    if count != steps or next(saved_clicks, missing) is not missing:
        raise ValueError("missing transitions or extra click records")
    if clicks != report.get("click_count") or _hash(current) != report.get("final_state_hash"):
        raise ValueError("saved report disagrees with final state or clicks")
    ledger = inspect_history(states, direction, protocol=protocol)
    result = {"schema": SCHEMA, "tensor_hash": bundle.tensor.fingerprint,
              "bundle_id": bundle.bundle_id, "run_id": run_id, "seed_hash": _hash(states[0]),
              "steps": steps, "channels_per_node": 48, "nodes": bundle.seed.N,
              "scalar_forward_inverse_register_comparisons": comparisons,
              "independent_canonical_clicks": clicks, "complete_contiguous_history": True,
              "complete_legal_carry_classes": sorted({v for row in states[0]["r"] for v in row}),
              "ledger": ledger, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": {"same_law_mechanical_history": "passed",
                        "same_state_discrete_source_chart": "passed" if protocol is not None else "not_tested",
                        "Einstein_components": "separate geometry_review proof required",
                        "global_periodic_positive_null_source": "impossible in this profile ansatz",
                        "generic_bound_massive_body": "not supplied by free-streaming total density",
                        "indefinite_monotone_Boolean_organization": "impossible on finite invariant sector",
                        "operational_material_proper_time_clock": "not established"}}
    if out is not None:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(exact_json.dumps(result, sort_keys=True)+"\n")
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/acceptance.json"))
    args = parser.parse_args(argv)
    protocol = None if args.protocol is None else _read(args.protocol.read_text())
    result = audit_saved_run(args.run, protocol=protocol, out=args.out)
    print(exact_json.dumps({key: result[key] for key in
        ("run_id", "steps", "scalar_forward_inverse_register_comparisons", "independent_canonical_clicks")}))

if __name__ == "__main__":
    main()
