# Highlights implementation coverage

What the repository implements of [Highlights](HIGHLIGHTS.md), as of
2026-09-19, the day the old engine was deleted and the field-only engine of
the law of the shadow became the one engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted)).
The dated coverage records of 2026-09-12 to 2026-09-18, one per reconciliation
of the specification with the code of the old engine, are in git (this file at
any commit before 2026-09-19). This document records what is implemented; it
is not evidence that a physical law holds.

| Highlights | Implemented | Where | Test |
| --- | --- | --- | --- |
| 3.1 Discrete local space | The cubic lattice, a Node's six Ports in Port order, the open board (what leaves is escaped with its momentum); a closed board is refused | `core/lattice.py`; `shadow/layer.py` (`walk`); `shadow/world.py` | `test_field_only` (a), `test_family_turns` (c) |
| 3.3, 5.1 Every ray is a wave ray, one N for the world | The phase circle of N steps with its cosine and sine tables in bounded integers; the phase turn in flight per family (`phase_turn`): light by its quantum over K on every Link walked, the same everywhere, the remainder per family (round 8, S5); a free family not at all; the old rule by the cell's amount kept as a choice | `core/phase.py`; `shadow/layer.py`; `shadow/world.py` | `test_field_only` (g), `test_family_turns` |
| 5.4 point 24, the Node mixes the six; point 22, the remainder rule | The mixing kernels over one family's arrays: the 3B_h rule on the coherent sum, the largest remainder in ninths, the parked shares and their release at nine, the momentum carried with the shares | `shadow/mixing.py`; `shadow/layer.py` (`cycle`) | `test_node_mixing` |
| 5.4 The law of the shadow: only shadows and events | Matter as content held at Nodes; every ray a whole quantum in flight; an event a whole quantum at held content, met by the family's table (`read`, `keep`, `rerelease`, `pass`), the own number sunk; the release at the world's rate, a lamp spending; the push by content and charge; the step by the accumulators at most once in two intervals; the books per family exact at every tick; the readings (shells, cube flux) | `shadow/engine.py`; `shadow/world.py` | `test_field_only` (a) to (h) |
| 5.4 One speed, and what is seen (2026-09-19) | Every transfer one Link per interval; all slowness a stay at a Node: the wait as intervals owed per whole unit of size read, for held content (its clock and release) and for light in flight (a hold per Node), at the world's `wait_per_quantum` | `shadow/engine.py` (`_read_wait`); `shadow/layer.py` (`charge_wait`) | `test_field_only` (e) |
| 3.19, 5.4 The Detector: a click is an absorption | A mark is held content whose table keeps a family; a click is the absorption of a whole quantum of it, per number, the rest waiting in the holder's register (`quantum`, 1 by default); Born by counting, no draw | `shadow/engine.py` (`_meet`); `shadow/world.py` | `test_family_quantum`, `test_field_only` (d) |
| 5.4 the declared widths (2026-09-19) | ρ (`release`), K, N, `wait_per_quantum`, `phase_turn` and `quantum` per family; nothing else free in the engine; the precisions (32nds, 256, ninths) are not choices | `shadow/world.py` | `test_family_turns`, `test_family_quantum`, `test_configuration_validation` |
| 3.15 Exact invariants at every event | The books per family (held: initial, absorbed, current, spent, escaped, pending; shadows: initial, released, current, escaped, absorbed) balanced at every tick, the momentum on held content alone, the charge summed | `shadow/engine.py` (`books`) | `test_field_only` (a), `test_family_quantum` |
| 6 Evidence | A run's record (`run.json` with `law`, the world's keys, the books per tick, the contents), the input as read, the events and the state Node by Node | `shadow/run.py`; `snapshot_writer.py`; `runner.py` | `test_field_only` (f) |

Not implemented, open in Highlights 5.4 and 5.5: the
Bell setup (A2) and polarization as worlds and tables; a decay as a table on
held content; the mass ladder of hypothesis 12 under this law; the research
runs on open boards (E11, A5s, A6, A1, E9), to be made when wanted and
registered in [EXPERIMENTS.md](EXPERIMENTS.md).
