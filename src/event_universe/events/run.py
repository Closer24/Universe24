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
from event_universe.diagnostics.massive_record_margin import (
    check_body_conditions,
    check_margins,
    profile_check,
)
from event_universe.events.detector_law import DetectorLawSimulation
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
    keep_row_clicks: bool = False,
) -> Path:
    """Run `count` intervals of the world into the empty directory `output`;
    returns the path of `run.json`. A failing interval is recorded and raised.
    Optional initialization provenance is copied for output only, never physics.
    By default (the model owner, 2026-09-23, record 1296 of
    docs/LOG_2026-09-20.md) the per-row `click` lines of the measured events,
    a GameBoard diagnostic that is most of a long run's record by bytes, are
    left out of `events.jsonl` and `run.json` carries `omit_row_clicks` true
    so a reader knows the record is trimmed; `keep_row_clicks` (the runner's
    `--keep-row-clicks`) writes them and no such field, the record as it was
    before the option, byte for byte. Every other line is written either way.
    """
    initialization_metadata = copy.deepcopy(initialization_record)
    # massive-record-v1: the margin rule, a load-time check of every block
    # before the world runs (MASSIVE_RECORD.md section 11 item 4; a HOST
    # computation of the declaration, printed and recorded, never read by
    # the state); a declaration below the margin refuses the run here.
    margins = check_margins(world) if world.massive_record else []
    for reading in margins:
        for line in reading.lines():
            print(line)
        # a block seeded with an integer profile: the GAMEBOARD check that the
        # file's integers are the module's mode at the file's amplitude (a
        # comparison printed; no float enters the run's record)
        check = profile_check(world, reading.number)
        if check is not None:
            print(
                f"seed (GAMEBOARD): block {reading.number}: the declared profile against the margin "
                f"module's mode at the amplitude {check[1]}: the largest deviation {check[0]} units"
            )
    # The body's conditions exact in the initial state (the model owner's word
    # of 2026-09-24, 16:48Z): the seed on the bound mode at both levels and
    # the ramp against the relaxation time, on the engine as constructed,
    # before the first interval; a refusal here names the body and the Node.
    if margins and world.detector_law:
        for line in check_body_conditions(world, DetectorLawSimulation(world), margins):
            print(line)
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

        # detector-law-v1: the local detector law's own engine when the world
        # declares it; the ray law as built otherwise, unchanged.
        simulation = (
            DetectorLawSimulation(world, observer=record)
            if world.detector_law
            else NatureBeamSimulation(world, observer=record, keep_row_clicks=keep_row_clicks)
        )
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
        # The clock stamp (2026-09-22, the moving detector): the world key
        # as declared, written only when true; a record field, no
        # hypothesis (every other record byte for byte as it was).
        **({"clock_stamp": True} if world.clock_stamp else {}),
        # massive-record-v1 (2026-09-23): the world key `massive_record` as
        # declared, written only under the key (every other record byte for
        # byte); `massive-record-v1` under `hypotheses` when it is true.
        **(
            {"massive_record": True, "margin": [reading.to_record() for reading in margins]}
            if world.massive_record
            else {}
        ),
        # The host's record switch (2026-09-23): written on every record
        # whose per-row click lines were left out of `events.jsonl` (the
        # default), so that a reader of those lines knows the record is
        # trimmed, and absent under `--keep-row-clicks`; a host field, no
        # hypothesis, no key of the world (a kept record byte for byte as
        # it was before the option).
        **({"omit_row_clicks": True} if not keep_row_clicks else {}),
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
        # drive-b-v1 (2026-09-22): the world key `drive_b` as declared,
        # written only under the key (every other record byte for byte).
        **({} if not world.drive_b else {"drive_b": True}),
        # The row's flight in the age wall's set (optical-v1, 2026-09-21;
        # the law's own since 2026-09-22): the world's gamma and the flight
        # coefficient 1 + gamma, written for every world.
        "optical": {"gamma": world.optical, "flight_coefficient": world.flight_coefficient},
        # centred-step-v1 (2026-09-22): the world key `centred_step` as
        # declared, written only under the key (every other record byte for
        # byte).
        **({} if not world.centred_step else {"centred_step": True}),
        # flow-link-v1 (2026-09-22): the world key `flow_link` as declared,
        # written only under the key (every other record byte for byte).
        **({} if not world.flow_link else {"flow_link": True}),
        # atom-level-v1 (2026-09-22): the world key `atom_level` as declared,
        # written only under the key (every other record byte for byte).
        **({} if not world.atom_level else {"atom_level": True}),
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
                # The record kind's pair on the six-neighbour term and its
                # faces (`massive-record-v1`), written only in a world that
                # declares `massive_record` (light's kind [1, 1] and the
                # world's faces where the family declares none).
                **(
                    {
                        "pair": list(family.pair),
                        "faces": {
                            axis: "periodic" if wraps else "open"
                            for axis, wraps in zip(
                                ("x", "y", "z"), world.kind_periodic(index), strict=True
                            )
                        },
                    }
                    if world.massive_record
                    else {}
                ),
            }
            for index, family in enumerate(world.families)
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
        # issue #1086: what `balanced` covers (content alone; the momentum
        # books carry the blocks' held momentum and no transit or escape)
        "balanced_scope": "content alone (the momentum books are not accounted)",
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
