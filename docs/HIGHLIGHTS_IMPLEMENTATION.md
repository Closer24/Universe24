# Highlights implementation coverage

What the repository implements of [Highlights](HIGHLIGHTS.md), as of
2026-09-19, the evening, the day the engine of the law of events became the
one engine ([migration](MIGRATION.md)). The dated coverage records of
2026-09-12 to 2026-09-19 (the old engine's, then the shadow engine's) are in
git (this file at any earlier commit). This document records what is
implemented; it is not evidence that a physical law holds.

| Highlights | Implemented | Where | Test |
| --- | --- | --- | --- |
| 3.1 Discrete local space | The cubic lattice, a Node's six Ports in Port order, the open board (what leaves is escaped with its momentum); a closed board is refused | `core/lattice.py`; `events/transit.py` (`walk`); `events/world.py` | `test_event_transit` (a), `test_event_worlds` (e) |
| 3.3, 5.1 One N for the world; "nothing is accumulated on the way" | The phase circle of N steps with its cosine and sine tables in bounded integers; an event in transit does not turn; a measured event's phase turns by its content over K off its clock | `core/phase.py`; `events/transit.py`; `events/engine.py` (`_release`) | `test_event_transit` (a), `test_event_clock` (b) |
| 5.4 The law of events: one thing, the event; seven exits; nothing kept at a Node | Every event created at its next place from its record each interval, at a neighbour or here; no register, remainder, parked share or draw; a single unit whole by its momentum | `events/engine.py`, `events/transit.py`, `events/mixing.py` | `test_node_mixing` (f, h), `test_event_transit` |
| 5.4 point 24 read under the law of events: the sides from the vectors | The 3B_h rule on the coherent sum, the squared leaving amplitudes, whole units by the largest remainder with the ties in the tick's Port order, a group with no whole going by its momentum, the momentum carried with the units | `events/mixing.py` (`mix_arrivals`, `apportion_carried`, `tie_order`) | `test_node_mixing` |
| 5.4 "The event carries it; the next event is delayed" | The suspension a count on the arrivals, derived once on arrival from the free families' sizes, the larger count kept when events join a waiting slot; a measured event's count derived when spent, its clock not ticking meanwhile | `events/transit.py` (`suspend`, `cycle`); `events/engine.py` (`_suspend`, `_release`) | `test_event_suspension` |
| 5.4 "every clock tick there is self-creation"; the clock is the count of self-creations | The age of a measured event; the release, the lamp, the phase, the step and the electric push read off it by whole division (`by_clock`), no remainder | `events/engine.py` | `test_event_clock` |
| 5.4 matter is a measured event; measurement is the merging of records; the tables | A measured event's table per family (`read`, `measure`, `rerelease`, `pass`); the click one per unit; what comes home created again, not counted as content; the push by the momentum carried, the third law by the symmetry of the fields for a free family and by the recoil for a paid one | `events/engine.py` (`_meet`, `_push`, `_release`) | `test_event_worlds` (a, c), `test_event_clock` (c) |
| 5.4 "There are detectors by sensitivity"; "every detector must state its sensitivity" | A detector a named set of measured events with a threshold; every response of a detector's Node gated by its threshold (`read`, `measure`, `rerelease`; a smaller bundle passes, a release reads no threshold); the record's measurements per detector and per Node | `events/world.py` (`detectors`); `events/engine.py` (`_meet`, `detectors`); `events/run.py` | `test_detector_sensitivity`, `test_event_worlds` (d, e) |
| 5.4 "Approve the phase window as a declared width of a detector, and of the emitter too" | One generic key, `phase_window`, a setting on the circle of N steps and the half circle centred on it (d = (phase - s) mod N below N / 4 or from 3 N / 4): on a table entry (`{"rule": ..., "phase_window": s}`, any rule but `pass`) the response after the threshold only to a bundle whose phase at the Node falls in it, a bundle outside it passing with a `pass` record; on a lamp a release only at the self-creations whose clock phase falls in it, the clock and the phase turning regardless; the phase read on every measurement record; the string form of a table entry still accepted | `events/world.py` (`_table_entry`, `_lamp`); `events/transit.py` (`phase_at`); `events/engine.py` (`in_window`, `_meet`, `_pass`, `_release`, `_event`) | `test_phase_window` |
| 5.4 the declared widths | ρ (`release`), K, N, `suspension`, `quantum` per paid family, the detectors' thresholds and the phase windows; nothing else free in the engine; the precisions (32nds, 256) are not choices | `events/world.py` | `test_event_worlds` (e), `test_phase_window` (c) |
| 3.15 Exact invariants at every event | The books per family (measured: initial, measured, current, spent, escaped; transit: initial, released, current, escaped, absorbed) balanced at every tick; the momentum reported on the measured events, in transit and escaped; the charge summed | `events/engine.py` (`books`) | every engine test asserts the books |
| 6 Evidence | A run's record (`run.json` with `law`, the world's keys, the books per tick, the measured events, the detectors), the input as read, the events and the state Node by Node | `events/run.py`; `snapshot_writer.py`; `runner.py` | `test_event_worlds` (e) |

Not implemented, open in Highlights 5.4 and 5.5: the Bell setup (A2) and
polarization as worlds and tables; a decay as a table on a measured event;
the mass ladder of hypothesis 12 under this law; the research runs on open
boards, to be made when wanted and registered in [EXPERIMENTS.md](EXPERIMENTS.md).
The engine of the law of the shadow and what it kept (parked ninths, the wait
as a hold, the remainders, the register of `quantum`) are deleted with it
([migration](MIGRATION.md)).
