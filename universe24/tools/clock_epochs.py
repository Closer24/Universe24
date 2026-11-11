"""Reproducible autonomous clock runs with passive, explicitly scoped readouts.

Only Engine.step advances the trajectory. A horizon or resource gate may stop
the loop after a complete update; neither changes a value, reseeds an epoch,
or chooses a branch. Crossings of a declared hand, echoes of selected reader
b values and exact recurrence of the complete seed are separate diagnostics.

Example: python -m universe24.tools.clock_epochs --steps 1000 --seed-divisor 16
         --out runs/clock-epochs/report.json
"""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Mapping
from fractions import Fraction
import json
import math
from pathlib import Path
import time

import numpy as np

from ..core import Engine, State, Tensor
from ..observe.one import state_hash
from ..observe.readout import official_clicks


def _positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive Python int")
    return value


def _indices(values, G, name, *, nonempty=False):
    try:
        result = tuple(values)
    except TypeError as exc:
        raise ValueError(f"{name} must be a sequence of gear indices") from exc
    if any(type(g) is not int or not 0 <= g < G for g in result):
        raise ValueError(f"{name} contains an invalid gear index")
    if len(set(result)) != len(result) or (nonempty and not result):
        raise ValueError(f"{name} must contain distinct{' nonempty' if nonempty else ''} gear indices")
    return result


def _sectors(tensor, sectors):
    if sectors is None:
        sectors = {}
        for g, name in enumerate(tensor.names):
            sectors.setdefault(name.split(".", 1)[0], []).append(g)
    if not isinstance(sectors, Mapping) or not sectors:
        raise ValueError("sector_indices must be a nonempty mapping")
    if any(type(name) is not str or not name for name in sectors):
        raise ValueError("sector names must be nonempty strings")
    groups = {name: _indices(sectors[name], tensor.G, name, nonempty=True)
              for name in sorted(sectors)}
    rows = [g for group in groups.values() for g in group]
    if sorted(rows) != list(range(tensor.G)):
        raise ValueError("sector_indices must partition all gear types exactly once")
    return groups


def _vector(state, rows, fields):
    return [int(value) for field in fields for value in getattr(state, field)[list(rows)].flat]


def _distance(current, reference):
    """Exact squared Euclidean distance to either sign of the reference."""
    denominator = sum(value * value for value in reference)
    if not denominator:
        return None
    positive = sum((left - right) ** 2 for left, right in zip(current, reference))
    negative = sum((left + right) ** 2 for left, right in zip(current, reference))
    return dict(numerator=min(positive, negative), denominator=denominator,
                sign=1 if positive <= negative else -1)


def _fraction(distance):
    return None if distance is None else Fraction(distance["numerator"], distance["denominator"])


def _hand_summary(state, gear):
    b = [int(value) for value in state.b[gear]]
    a = [int(value) for value in state.a[gear]]
    return dict(b_sum=sum(b), b_min=min(b), b_max=max(b), nodes=state.N,
                counter_bits=max(abs(value) for value in a + b).bit_length())


def _sector_maxima(state, sectors):
    # Python-int extrema avoid int64 abs(-2**63) overflow. Keeping sector
    # bounds prevents a large background hand from hiding another field's growth.
    return {name: max(max(int(getattr(state, field)[list(rows)].max()),
                          -int(getattr(state, field)[list(rows)].min()))
                      for field in ('a', 'b'))
            for name, rows in sectors.items()}


def run_epochs(tensor: Tensor, seed: State, *, steps: int,
               hand_indices=(), reader_indices=(), sector_indices=None,
               max_counter_bits: int = 256,
               max_seconds: float | None = None, sample_every: int = 100,
               echo_threshold=(1, 20), record_symbols: bool = False) -> dict:
    """Run a fixed tensor from an explicit seed and return a compact JSON report.

    Indices and all observer parameters are frozen before the first update.
    Sectors are a disjoint complete partition (default: gear-name namespaces).
    The per-update symbol of each sector is sign(sum of signed quotients of
    its official click records), in {-1,0,1}; zero can mean cancellation or no
    records. Symbol counts/transitions are always retained; the full symbol
    series is opt-in. No raw snapshots or tensor dumps are written.

    A hand is the sum of b over the selected gears and all nodes. A crossing
    requires opposite nonzero signs; a zero plateau postpones the crossing
    until the opposite sign appears. Initial departure from zero is not one.
    Reader echoes are strict-left, weak-right local minima of squared distance
    to either sign of initial reader b, below the declared rational threshold.
    A zero reader seed has no normalized echo diagnostic. Exact recurrence is
    checked against the ENTIRE initial (a,b,r) state at every completed update.
    Neither a crossing nor a b echo implies that full state has recurred.

    Resource gates only terminate. A first over-limit update is retained,
    observed and included in completed_steps and exact rewind. A wall budget
    covers forward execution/observations, not the mandatory rewind audit.
    """
    if not isinstance(tensor, Tensor) or not isinstance(seed, State):
        raise TypeError("expected a Tensor and a State")
    _positive_integer(steps, "steps")
    _positive_integer(max_counter_bits, "max_counter_bits")
    _positive_integer(sample_every, "sample_every")
    if type(record_symbols) is not bool:
        raise ValueError("record_symbols must be a bool")
    if max_seconds is not None and (type(max_seconds) not in (int, float)
                                   or not math.isfinite(max_seconds) or max_seconds <= 0):
        raise ValueError("max_seconds must be finite and positive or None")
    if (not isinstance(echo_threshold, (tuple, list)) or len(echo_threshold) != 2
            or any(type(v) is not int or v < 1 for v in echo_threshold)):
        raise ValueError("echo_threshold must be a positive integer numerator/denominator pair")
    threshold = Fraction(*echo_threshold)
    engine = Engine(tensor)
    # Validate remainder domain and gear count before making a run snapshot.
    if seed.G != tensor.G or int(seed.r.min()) < 0 or int(seed.r.max()) >= engine.D:
        raise ValueError("seed gear count or remainder domain does not match the tensor/divisor")
    hands = _indices(hand_indices, tensor.G, "hand_indices")
    readers = _indices(reader_indices, tensor.G, "reader_indices")
    sectors = _sectors(tensor, sector_indices)
    names = tuple(sectors)
    sector_of = {g: name for name, group in sectors.items() for g in group}
    # The caller's seed is never mutated; all further changes come from Rule3.
    initial = seed.copy()
    state = initial
    indices = np.arange(tensor.G)
    initial_hash = state_hash(initial, indices)
    b_reference = _vector(initial, readers, ("b",))
    ab_reference = _vector(initial, readers, ("a", "b"))
    initial_hand = sum(_vector(initial, hands, ("b",))) if hands else None
    last_nonzero_sign = (initial_hand > 0) - (initial_hand < 0) if hands else 0
    last_nonzero_step = 0
    hand_tracks = {}
    for g in hands:
        summary = _hand_summary(initial, g)
        total = summary["b_sum"]
        hand_tracks[g] = dict(initial=summary, final=summary,
                              peak_counter_bits=summary["counter_bits"], zero_crossings=[],
                              last_sign=(total > 0) - (total < 0), last_step=0)
    crossings, echoes, recurrences, samples = [], [], [], []
    recent = [(0, _distance(b_reference, b_reference), _distance(ab_reference, ab_reference))]
    counts = {name: 0 for name in names}
    quotient_sums = {name: 0 for name in names}
    kind_counts = {name: [0, 0, 0] for name in names}
    symbol_counts = {name: Counter({-1: 0, 0: 0, 1: 0}) for name in names}
    symbol_transitions = {name: [[0] * 3 for _ in range(3)] for name in names}
    previous_symbols = None
    symbols = [] if record_symbols else None
    initial_sector_max = _sector_maxima(initial, sectors)
    final_sector_max = initial_sector_max.copy()
    peak_sector_max = initial_sector_max.copy()
    peak_bits = initial.max_abs().bit_length()
    completed = 0
    stop_reason = "initial_counter_bit_limit" if peak_bits > max_counter_bits else "requested_horizon"
    start = time.monotonic()
    if stop_reason == "requested_horizon":
        for tick in range(1, steps + 1):
            next_state = engine.step(state)
            completed = tick
            bits = next_state.max_abs().bit_length()
            peak_bits = max(peak_bits, bits)
            final_sector_max = _sector_maxima(next_state, sectors)
            for name in names:
                peak_sector_max[name] = max(peak_sector_max[name], final_sector_max[name])
            events = official_clicks(engine, state, next_state, tick)
            tick_sums = {name: 0 for name in names}
            tick_counts = {name: 0 for name in names}
            for gear, quotient, kind in zip(events.gear, events.quotient, events.kind):
                name = sector_of[int(gear)]
                counts[name] += 1
                tick_counts[name] += 1
                quotient_sums[name] += int(quotient)
                tick_sums[name] += int(quotient)
                kind_counts[name][int(kind)] += 1
            tick_symbols = [(tick_sums[name] > 0) - (tick_sums[name] < 0) for name in names]
            for j, name in enumerate(names):
                symbol_counts[name][tick_symbols[j]] += 1
                if previous_symbols is not None:
                    symbol_transitions[name][previous_symbols[j] + 1][tick_symbols[j] + 1] += 1
            previous_symbols = tick_symbols
            if symbols is not None:
                symbols.append(tick_symbols)
            hand_sum = sum(_vector(next_state, hands, ("b",))) if hands else None
            for g, track in hand_tracks.items():
                summary = _hand_summary(next_state, g)
                track["final"] = summary
                track["peak_counter_bits"] = max(track["peak_counter_bits"], summary["counter_bits"])
                total = summary["b_sum"]
                if total:
                    sign = (total > 0) - (total < 0)
                    if track["last_sign"] and sign != track["last_sign"]:
                        track["zero_crossings"].append(dict(
                            step=tick, direction="up" if sign > 0 else "down",
                            zero_plateau_steps=tick - track["last_step"] - 1))
                    track["last_sign"], track["last_step"] = sign, tick
            if hands and hand_sum:
                sign = (hand_sum > 0) - (hand_sum < 0)
                if last_nonzero_sign and sign != last_nonzero_sign:
                    crossings.append(dict(step=tick, direction="up" if sign > 0 else "down",
                                          hand_sum=hand_sum, previous_nonzero_step=last_nonzero_step,
                                          zero_plateau_steps=tick - last_nonzero_step - 1))
                last_nonzero_sign, last_nonzero_step = sign, tick
            bd = _distance(_vector(next_state, readers, ("b",)), b_reference)
            abd = _distance(_vector(next_state, readers, ("a", "b")), ab_reference)
            recent.append((tick, bd, abd))
            if len(recent) == 3:
                left, middle, right = recent
                ldist, mdist, rdist = (_fraction(item[1]) for item in recent)
                if mdist is not None and mdist < threshold and mdist < ldist and mdist <= rdist:
                    echoes.append(dict(step=middle[0], reader_b_distance=middle[1],
                                       reader_ab_distance=middle[2]))
                recent.pop(0)
            if next_state.same_as(initial):
                recurrences.append(tick)
            sample = dict(step=tick, counter_bits=bits, hand_sum=hand_sum,
                          reader_b_distance=bd, reader_ab_distance=abd,
                          sector_counter_maxima=final_sector_max.copy(),
                          official_counts=tick_counts, official_symbols=dict(zip(names, tick_symbols)))
            if tick == 1 or tick % sample_every == 0:
                samples.append(sample)
            state = next_state
            if bits > max_counter_bits:
                stop_reason = "counter_bit_limit"
                break
            if max_seconds is not None and time.monotonic() - start >= max_seconds:
                stop_reason = "forward_wall_budget"
                break
        if completed and (not samples or samples[-1]["step"] != completed):
            samples.append(sample)
    forward_seconds = time.monotonic() - start
    rewind_start = time.monotonic()
    recovered = engine.rewind(state, completed)
    rewind_seconds = time.monotonic() - rewind_start
    epochs = []
    for direction in ("up", "down"):
        times = [crossing["step"] for crossing in crossings if crossing["direction"] == direction]
        epochs.extend(dict(direction=direction, start=a, end=b, updates=b - a)
                      for a, b in zip(times, times[1:]))
    epochs.sort(key=lambda row: (row["start"], row["direction"]))
    result = dict(
        schema="universe24-clock-epochs-v1", model_status="diagnostic; no derived physics claim",
        law=dict(tensor_fingerprint=tensor.fingerprint,
                 dynamics_fingerprint=tensor.dynamics_fingerprint, D=6,
                 G=tensor.G, rank=tensor.rank, monomials=len(tensor.monomials)),
        initial_state=dict(L=initial.L, hash=initial_hash, hash_format="universe24-state-values-v2"),
        parameters=dict(steps=steps, max_counter_bits=max_counter_bits, max_seconds=max_seconds,
                        sample_every=sample_every, record_symbols=record_symbols,
                        echo_threshold=[threshold.numerator, threshold.denominator],
                        hand_indices=list(hands), reader_indices=list(readers),
                        sector_indices={name: list(group) for name, group in sectors.items()}),
        completed_steps=completed, observed_steps=completed, stop_reason=stop_reason,
        peak_counter_bits=peak_bits, final_state_hash=state_hash(state, indices),
        sector_counter_bounds={name: dict(initial=initial_sector_max[name],
                                          final=final_sector_max[name],
                                          peak=peak_sector_max[name]) for name in names},
        exact_rewind=recovered.same_as(initial), caller_seed_unchanged=seed.same_as(initial),
        forward_seconds=forward_seconds, rewind_seconds=rewind_seconds,
        hand_zero_crossings=crossings, same_direction_hand_epochs=epochs,
        hand_gears={tensor.names[g]: dict(gear_index=g, initial=track["initial"], final=track["final"],
                                          peak_counter_bits=track["peak_counter_bits"],
                                          zero_crossings=track["zero_crossings"])
                    for g, track in hand_tracks.items()},
        reader_b_echoes=echoes, exact_full_seed_recurrence_steps=recurrences,
        official_records=sum(counts.values()), official_records_by_sector=counts,
        signed_official_quotient_sum_by_sector=quotient_sums,
        click_kind_counts_by_sector=kind_counts,
        symbols=dict(definition="sign of summed signed official quotient per sector per update",
                     alphabet=[-1, 0, 1], sector_order=list(names),
                     counts={name: [symbol_counts[name][value] for value in (-1, 0, 1)] for name in names},
                     transition_counts=symbol_transitions, series=symbols),
        samples=samples,
        semantics=dict(
            forward="Only Engine.step; frozen tensor and explicit seed; no runtime injections or epoch resets.",
            bits="Maximum absolute a/b counter bit length; remainder values are bounded by D.",
            crossings="Opposite nonzero signs of the summed selected hand b; zero plateaus delay recognition.",
            echoes="Strict-left/weak-right local minima below threshold of sign-equivalent reader b squared distance; final endpoint is not tested.",
            distances="Exact numerator/denominator; zero reference norm disables the corresponding distance.",
            recurrence="Exact equality of all a,b,r to the initial state at every completed update; other pairs are not searched.",
            clicks="Official stream plus tensor official labels; record counts differ from signed quotient weight.",
            symbols="Zero includes both no-record updates and cancellation; these symbols are not entropy, complexity or entanglement.",
            budget="Termination only, after complete observed updates; mandatory exact rewind is outside forward wall budget.",
            interpretation="Hand epochs and reader echoes are not cosmological bangs, full-state cycles, proper time, collapse or optimized complexity."))
    return result


def prepare_baseline(*, L=3, rng_seed=13, seed_kind="pulse", seed_divisor=1):
    """Construct the unchanged default law and an explicitly declared initial seed.

    The optional divisor truncates only initial reference a,b towards zero;
    all remainders and tensor coefficients are left unchanged.
    This happens before the first update and is a seed control, not dynamics.
    """
    _positive_integer(seed_divisor, "seed_divisor")
    from ..core.tensor import compose
    from ..layers.one import one_system
    from ..prepare.one import one_seed

    system = one_system()
    tensor = compose(*system.blocks)
    seed, preparation = one_seed(system, tensor, L, bang=seed_kind, rng_seed=rng_seed)
    source_hash = state_hash(seed, np.arange(tensor.G))
    rows = list(range(tensor.G))
    if seed_divisor != 1:
        seed = seed.copy()
        for field in ("a", "b"):
            array = getattr(seed, field)
            for g in rows:
                array[g] = [int(value) // seed_divisor if value >= 0
                            else -((-int(value)) // seed_divisor) for value in array[g]]
    return tensor, seed, dict(builder="one_system() default, no additional coupling", L=L,
                              rng_seed=rng_seed, seed_kind=seed_kind,
                              seed_divisor=seed_divisor, scaled_gear_indices=rows,
                              scaling="initial reference a,b truncated towards zero; r unchanged",
                              source_seed_hash=source_hash, seed_report=preparation)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--L", type=int, default=3)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--rng", type=int, default=13)
    parser.add_argument("--seed-kind", choices=("pulse", "standing", "none"), default="pulse")
    parser.add_argument("--seed-divisor", type=int, default=1)
    parser.add_argument("--max-counter-bits", type=int, default=256)
    parser.add_argument("--max-seconds", type=float)
    parser.add_argument("--sample-every", type=int, default=100)
    parser.add_argument("--record-symbols", action="store_true")
    parser.add_argument("--out", default="runs/clock-epochs/report.json")
    args = parser.parse_args(argv)
    tensor, seed, preparation = prepare_baseline(L=args.L, rng_seed=args.rng,
                                                 seed_kind=args.seed_kind,
                                                 seed_divisor=args.seed_divisor)
    result = run_epochs(tensor, seed, steps=args.steps,
                        hand_indices=[0],
                        reader_indices=list(range(tensor.G)),
                        max_counter_bits=args.max_counter_bits, max_seconds=args.max_seconds,
                        sample_every=args.sample_every, record_symbols=args.record_symbols)
    result["preparation"] = json.loads(json.dumps(preparation))
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("completed_steps", "stop_reason", "peak_counter_bits", "exact_rewind")}, indent=2))
    return result


if __name__ == "__main__":
    main()
