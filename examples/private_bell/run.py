"""Run private36 detector parity and a stratified CHSH integration probe."""

import argparse
import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from time import perf_counter
from types import MappingProxyType

from prepare import prepare

import event_universe
from event_universe.core.spatial_state import TICKET_MODULUS
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.diagnostics.private_render import frame
from event_universe.fields.bonds import BondRegistry
from event_universe.integration.private_contacts import CaptureRecord, captured_result, prepare_capture
from event_universe.runner import source_fingerprint


@dataclass(frozen=True)
class PreparedLocal:
    results: object
    owner: object
    records: tuple

    def commit(self):
        self.owner.records.extend(self.records)


class FixedLocalContacts:
    """Negative control: each end returns a fixed local answer without a registry."""

    def __init__(self, bindings):
        self.bindings = bindings
        self.records = []

    def prepare(self, tick, inputs):
        results, records = {}, []
        for local in inputs:
            detector = self.bindings.get(local.key)
            if detector is not None:
                request = prepare_capture(local.state, local.datum, detector)
                outcome = 1 if request.end == 1 else -1
                results[local.key] = captured_result(request, outcome)
                records.append(
                    CaptureRecord(
                        tick, local.key, request.pair_id, request.end, request.setting, outcome
                    )
                )
        return PreparedLocal(MappingProxyType(results), self, tuple(records))

    def canonical_state(self):
        return (tuple(self.records),)

    def report(self):
        return {"oracle_calls": 0, "numbers": 0, "answered_endpoints": len(self.records)}


def run_case(document, strategy, mode, output, fingerprint):
    output.mkdir(parents=True, exist_ok=False)
    world, ticks = prepare(document, strategy=strategy)
    if mode == "fixed_local":
        world.contacts = FixedLocalContacts(world.contacts.bindings)
    contacts = world.contacts
    hashes, frames, inventory = [], [], []
    step_seconds = 0.0
    failure = None
    for tick in range(ticks + 1):
        hashes.append(hashlib.sha256(repr(world.canonical_state()).encode()).hexdigest())
        frames.append(frame(world, contacts.bindings))
        inventory.append(
            len(world.transport.inputs)
            + len(world.transport.channels)
            + sum(bool(unit.state.codes) for node in world.nodes.values() for unit in node.units)
        )
        if tick < ticks:
            started = perf_counter()
            try:
                world.step()
            except Exception as error:
                failure = error
                break
            finally:
                step_seconds += perf_counter() - started
    records = [asdict(record) for record in contacts.records]
    metadata = {
        "model": document["profile"] + "/" + mode,
        "shape": document["shape"],
        "boundary": document["boundary"],
        "link_ticks": 1,
        "status": "completed" if failure is None else "failed",
        "error": None if failure is None else str(failure),
        "source_sha256": fingerprint,
        "strategy": strategy,
        "registers_per_node": 36,
        "captures": records,
        "quantum": contacts.report(),
        "inventory_per_tick": inventory,
        "work": world.work_report(),
        "step_seconds": step_seconds,
        "scope": "Two preconfigured endpoint tokens; terminal local captures. Shared quantum owner is explicit; no splitting or complete entity/coupling migration.",
    }
    render_disturbances(frames, output / "run.html", metadata)
    (output / "input.json").write_text(json.dumps(document, indent=2) + "\n")
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "events.jsonl").write_text(
        "".join(json.dumps(asdict(event)) + "\n" for event in world.events)
    )
    (output / "state_hashes.json").write_text(json.dumps(hashes) + "\n")
    if failure is not None:
        raise failure
    if inventory != [2] * (ticks + 1) or len(records) != 2 or world.transport.channels:
        raise ValueError("both original tokens must have exactly one terminal owner")
    if [record.tick for record in contacts.records] != [3, 3]:
        raise ValueError("this fixture must capture only on the actual tick-three arrivals")
    outcomes = {record.end: record.outcome for record in contacts.records}
    if mode == "shared_bond":
        oracle = BondRegistry(document["seed"], 64, tuple(document["number_stream"]))
        for record in contacts.records:
            if record.outcome != oracle.draw(record.pair_id, record.setting, record.end):
                raise ValueError("private36 answer differs from the configured shared-pair law")
        if contacts.report()["numbers"] != 1 or contacts.report()["oracle_calls"] != 2:
            raise ValueError("one pair needs one number and two endpoint requests")
    return {"hashes": hashes, "outcomes": [outcomes[1], outcomes[2]], "metadata": metadata}


def chsh(cells):
    correlations = []
    marginals = []
    for samples in cells:
        count = len(samples)
        correlations.append(Fraction(sum(a * b for a, b in samples), count))
        marginals.append(
            [str(Fraction(sum(pair[end] == 1 for pair in samples), count)) for end in (0, 1)]
        )
    value = abs(correlations[0] - correlations[1] + correlations[2] + correlations[3])
    return {
        "correlations": list(map(str, correlations)),
        "S": str(value),
        "S_decimal": float(value),
        "positive_marginals": marginals,
        "samples_per_setting": len(cells[0]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=64)
    args = parser.parse_args()
    if args.samples < 4 or args.samples > 256 or args.samples % 4:
        parser.error("samples must be a multiple of four from four to 256")
    if (
        Path(event_universe.__file__).resolve()
        != args.source.resolve() / "src/event_universe/__init__.py"
    ):
        parser.error("the imported engine must match --source; set PYTHONPATH explicitly")
    document = json.loads(args.input.read_text())
    prepare(document)
    fingerprint = source_fingerprint()
    args.output.mkdir(parents=True, exist_ok=False)
    reports, worlds, parity_checks = {}, 0, 0
    for mode in ("shared_bond", "fixed_local"):
        cells = []
        for cell, settings in enumerate(((0, 8), (0, 24), (16, 8), (16, 24))):
            samples = []
            for sample in range(args.samples if mode == "shared_bond" else 1):
                configured = deepcopy(document)
                configured["detectors"][0]["setting"], configured["detectors"][1]["setting"] = settings
                configured["number_stream"] = [((2 * sample + 1) * TICKET_MODULUS) // (2 * args.samples)]
                runs = {
                    strategy: run_case(
                        configured,
                        strategy,
                        mode,
                        args.output / mode / f"{cell}-{sample}-{strategy}",
                        fingerprint,
                    )
                    for strategy in ("dense", "sparse")
                }
                worlds += 2
                if runs["dense"]["hashes"] != runs["sparse"]["hashes"]:
                    raise ValueError("dense and sparse complete state differ at a recorded tick")
                parity_checks += len(runs["dense"]["hashes"])
                samples.append(runs["sparse"]["outcomes"])
            cells.append(samples)
        reports[mode] = chsh(cells)
    if Fraction(reports["fixed_local"]["S"]) > 2:
        raise ValueError("the independent endpoint control exceeds its local bound")
    if source_fingerprint() != fingerprint:
        raise ValueError("source changed during the experiment")
    report = {
        "profile": document["profile"],
        "source_sha256": fingerprint,
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "worlds": worlds,
        "per_tick_parity_checks": parity_checks,
        "per_tick_parity": True,
        "results": reports,
        "sampling": "Deterministic uniform midpoint coverage of one bounded number, reused for all four setting pairs. Finite quadrature, not an independent random sample or a confidence interval.",
        "limits": "Fixed settings; explicit shared nonlocal quantum resource. The fixed-local capture control has no quantum owner and returns +1/-1 at its own endpoints. No physical Bell-local derivation or complete matter/coupling claim.",
    }
    (args.output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
