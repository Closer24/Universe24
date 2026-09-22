"""A run of the Beam Law: the artifacts the runner writes for it.

`execute_nature_beam_run` steps a parsed world and preserves the input
(`initialization.json`), the events (`events.jsonl`: the measurements per
measured event, family and number with the push taken, the clicks with their
phase and content, the detectors' records per interval, the steps, the clicks
on the open faces), the final state (`state.json`, the measured events, the
detectors with the face detectors and every Node with rays, written Node by
Node through `snapshot_writer`) and the record (`run.json`: the law's marker
`beam-v1`, the world's keys, the books per completed tick with the
conservation flag, the per-tick lines of the measured content, the content in
transit and the momentum, the measured events' final states, the detectors'
measurements with their records and the face detectors', and the escapes).
`tools/run_series.py` reads the same keys of `run.json` as for any run
(`status`, `completed_ticks`, `elapsed_seconds`, `audit`,
`conserved_at_every_completed_tick`).
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from pathlib import Path

from event_universe import __version__
from event_universe.events.engine import NatureBeamSimulation
from event_universe.events.world import BEAM_LAW, NatureBeamWorld
from event_universe.snapshot_writer import write_snapshot


def execute_nature_beam_run(
    world: NatureBeamWorld,
    source: bytes,
    output: Path,
    fingerprint: str,
    count: int,
    *,
    initialization_record: dict[str, object] | None = None,
) -> Path:
    """Run `count` intervals of the world into the empty directory `output`;
    returns the path of `run.json`. A failing interval is recorded and raised.
    Optional initialization provenance is copied for output only, never physics.
    """
    initialization_metadata = copy.deepcopy(initialization_record)
    (output / "initialization.json").write_bytes(source)
    audit: list[dict[str, object]] = []
    measured_content: list[list[int]] = []
    transit_content: list[list[int]] = []
    momentum: list[dict[str, object]] = []
    failure: Exception | None = None
    completed = 0
    started = time.perf_counter()
    # The record's stream buffered by the megabyte: a run writes a record
    # line per event, tens of thousands of short writes.
    with (output / "events.jsonl").open("w", encoding="utf-8", buffering=1 << 20) as stream:

        def record(event: dict[str, object]) -> None:
            """Write one event line to `events.jsonl`."""
            stream.write(json.dumps(event) + "\n")

        simulation = NatureBeamSimulation(world, observer=record)
        try:
            for _ in range(count):
                simulation.step()
                books = simulation.books()
                audit.append(books)
                families = books["families"]
                assert isinstance(families, dict)
                measured_content.append(
                    [int(families[family.name]["measured"]["current"]) for family in world.families]
                )
                transit_content.append(
                    [int(families[family.name]["transit"]["current"]) for family in world.families]
                )
                momentum.append(dict(books["momentum"]))  # type: ignore[call-overload]
                if not books["balanced"]:
                    raise ValueError(f"{BEAM_LAW}: the books do not close at tick {simulation.tick}")
                completed += 1
        except Exception as error:  # noqa: BLE001 - recorded, then raised
            failure = error
        with (output / "state.json").open("w", encoding="utf-8") as state_stream:
            write_snapshot(simulation, state_stream)
            state_stream.write("\n")
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": fingerprint,
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "law": BEAM_LAW,
        "model": world.model_id,
        "shape": list(world.shape),
        "boundary": world.boundary,
        "K": world.K,
        "N": world.phase_steps,
        "release": list(world.release),
        "suspension": list(world.suspension),
        "width": world.width,
        "age_bound": world.age_bound,
        # The turn by momentum (the model owner's decision of 2026-09-20 on
        # Bohr): h when the world declares it, and then the identity of the
        # hypothesis beside the law, `bohr-v1`; `columns-v1` when the
        # world declares a column beyond `charge` or a lifetime
        # (`NatureBeamWorld.hypotheses`).
        "action": world.action,
        # The meeting (2026-09-20): the world key as declared, false by
        # default; `meeting-v1` under `hypotheses` when it is true.
        "meeting": world.meeting,
        # The massive rows (2026-09-21): the world key as declared, false by
        # default; `massive-rows-v1` under `hypotheses` when it is true.
        "massive_rows": world.massive_rows,
        # The binding that costs content (2026-09-20): `binding-v1` under
        # `hypotheses` when a measured event holds a paid family at load or
        # gave one during the run (no key; `NatureBeamSimulation.hypotheses`).
        "hypotheses": simulation.hypotheses,
        # The crossing rule's report (2026-09-21, BEAM_LAW note 48): the
        # Links a body crossed in the interval right after another of its
        # Links, where the rule's one-per-crossing count is not proved.
        "fast_steps": simulation.fast_steps,
        # The covariant readings (2026-09-21, `covariant-readings-v1`): the
        # key's declaration and the run's report, written only under the
        # key (every other record byte for byte as it was).
        **({} if world.covariant is None else {"covariant_readings": simulation.covariant_report()}),
        # The row's flight in the age wall's set (optical-v1, 2026-09-21;
        # the law's own since 2026-09-22): the world's gamma and the flight
        # coefficient 1 + gamma, written for every world.
        "optical": {"gamma": world.optical, "flight_coefficient": world.flight_coefficient},
        # The drive the body's step ran under (2026-09-22, the line drive
        # the law's drive, record 972; DEFAULT.md section (a)): "line", the
        # law's, or "per_axis", the drive of history under the world key
        # `per_axis_drive` (then also written as declared, and the identity
        # `per-axis-drive-v1` under `hypotheses`). A record without the
        # field is one from before that day and was read under the
        # per-axis drive.
        "drive": "per_axis" if world.per_axis_drive else "line",
        **({} if not world.per_axis_drive else {"per_axis_drive": True}),
        # centred-step-v1 (2026-09-22): the world key `centred_step` as
        # declared, written only under the key (every other record byte for
        # byte).
        **({} if not world.centred_step else {"centred_step": True}),
        # flow-link-v1 (2026-09-22): the world key `flow_link` as declared,
        # written only under the key (every other record byte for byte).
        **({} if not world.flow_link else {"flow_link": True}),
        # The world's columns in order, (name, sign): gravity, charge, the
        # declared names; every family's `columns` below is aligned with it.
        "columns": [{"name": name, "sign": sign} for name, sign in world.columns],
        "directions": [list(vector) for vector in world.directions],
        "families": [
            {
                "name": family.name,
                "quantum": family.quantum,
                "charge": list(family.charge),
                "columns": [
                    {"name": column.name, "value": list(column.value), "sign": column.sign}
                    for column in family.columns
                ],
                "phase": family.phase,
                # The integer as declared, or since the amplitude law the pair
                # [n, d] (the phase per interval of age).
                "phase_per_link": family.declared_phase_per_link,
                # The age at which the family's rays click on the border
                # `lifetime` (None: the family lives forever).
                "lifetime": family.lifetime,
                # The family's hand (`hand-v1`), written only in a world
                # that declares a hand or an axis somewhere (every other
                # record byte-identical).
                **({"hand": family.hand} if world.handed else {}),
                # The family's flag `massive` and the magnitude p of its
                # label (`massive-rows-v1`), written only in a world that
                # declares `massive_rows`.
                **(
                    {"massive": family.massive, "momentum_magnitude": family.momentum_magnitude}
                    if world.massive_rows
                    else {}
                ),
            }
            for family in world.families
        ],
        "numbers": {
            str(index + 1): {
                "position": list(entry.position),
                "family": world.families[entry.family].name,
                "span": list(entry.span),
                "phase_by_momentum": entry.phase_by_momentum,
                # The clock trigger of the transformation as declared (the
                # weak force, 2026-09-20), None without one.
                "become": (
                    None
                    if entry.become is None
                    else {
                        "at": entry.become.at,
                        "into": world.families[entry.become.into].name,
                        "products": [
                            [world.families[f].name, amount, content]
                            for f, amount, content in entry.become.products
                        ],
                        "crowd": entry.become.crowd,
                    }
                ),
                # The axial record (`hand-v1`) as declared, the heading's
                # vector or None; written only in a world with a hand.
                **(
                    {
                        "axis": (
                            None
                            if entry.axis is None
                            else [int(v) for v in world.directions[entry.axis]]
                        )
                    }
                    if world.handed
                    else {}
                ),
            }
            for index, entry in enumerate(world.measured)
        },
        "status": "failed" if failure else "completed",
        "error": str(failure) if failure else None,
        "requested_ticks": count,
        "completed_ticks": completed,
        "tick": simulation.tick,
        "elapsed_seconds": time.perf_counter() - started,
        "conserved_at_every_completed_tick": all(bool(entry["balanced"]) for entry in audit),
        "audit": audit,
        "measured_content": measured_content,
        "transit_content": transit_content,
        "momentum": momentum,
        "measured": simulation.contents(),
        "detectors": simulation.detectors(),
        "escaped": [
            {
                "family": family.name,
                "amount": simulation.ledger.escaped_amount(index),
                "content": simulation.ledger.escaped_content(index),
                # The family's own escaped momentum (since 2026-09-20; until
                # then the world's total was written into every line).
                "momentum": simulation.ledger.escaped_momentum(index),
            }
            for index, family in enumerate(world.families)
        ],
        "display": "none",
    }
    if world.recorded:
        # The amplitude law's world: the list of gathers (the clicks of the
        # world), the records open at the end and the layer's line.
        metadata["world"] = list(simulation.layer.gathers)
        metadata["open"] = simulation.layer.open_records()
        metadata["layer"] = simulation.layer.report()
    if initialization_metadata is not None:
        metadata["initialization_resolution"] = initialization_metadata
    path = output / "run.json"
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    if failure is not None:
        raise failure
    return path
