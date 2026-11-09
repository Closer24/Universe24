# Matter and light building blocks (published set)

338 **data-only initial preparations** from the matter/light research program.
Each one is an official init file: complete initial cells, background, one of the
eight fixed sign triples, and a horizon. Every block was replayed with the
unchanged native `Engine`, with the exact inverse `Engine.rewind` checked at every
update, before it was published. Nothing here is an engine, a rule change, a
detector that writes into a run, or a runtime method. After t = 0 only Rule3 acts.

Names such as "light", "matter", "atom", "lamp", "spinor-class" and "charge" are
**candidate names for click patterns and exact accounts of this model**. They
are not claims about physical photons, mass, spin-1/2, electric charge or energy
(AGENTS rules 10 and 12).

## Quick use

```sh
python -m research.matter_light_blocks_v1.verify --list            # all blocks, group, file
python -m research.matter_light_blocks_v1.verify fiber_x_packet     # replay and check one block
python -m research.matter_light_blocks_v1.verify --quick            # every non-heavy block
python -m research.matter_light_blocks_v1.verify                    # all 338 (about 2 minutes)
python -m universe24 --config research/matter_light_blocks_v1/blocks/light/fiber_x_packet.json --audit
```

```python
from research.matter_light_blocks_v1 import load, names
engine, initial, steps, entry = load("d1_local_atom_L100")
print(entry["what"], entry["signature"], entry["limits"])
```

`verify.py` uses only `universe24` and the standard library.

## Registered generators and compositions

[`registry/`](registry/README.md) holds the registered parametric data generators (for example
`matter_line@1`, `guide_net@1` and `phase_gate@2`; the full list is in the registry README), the
registry metadata, composition data, and a composer for compositions (`u24-composition-v1`). They
rebuild prepared networks from placements, so an experiment can ship a short composition instead
of large init files. Twelve published blocks (four D1 blocks and eight guide blocks) regenerate
exactly from tracked code.

## What is shipped

| group | blocks | examples |
|---|---:|---|
| light | 26 | `fiber_x_packet` (light candidate on a gauged fibre, click-front speed 1 site/update), `exact_front_111_box` (exact (111) front, C0 clicks only), `diag_sheet` |
| matter at rest | 31 | exact confined families, `B10_breather`, `B14_breather`, robust X12, lamps |
| moving matter | 20 | guided gliders at speeds 1/3 … 1, `planar_glider_100` (exact planar translator at speed 1/2 in the quiet vacuum: a board-wide sheet, not a localized object), crystal SLOW movers |
| atoms | 74 | `atom_trap_d6`, `atom_trap_d10` (a light packet between two dark cores, level 2d+4) with controls, period-shifted pairs, `d1_local_atom_L100` |
| spin | 13 | `spinor_screw`, `spin720_ring`, `spinor_ring_r09` (360° image after one lap, return after 720°), `spin_module_pure4pairs_L80` |
| charge | 44 | sign rules at contact, static charges, charge bookkeeping of Big-Bang seeds |
| clocks and gravity | 41 | Einstein networks, `charge_cavity_D10`, `created_atoms_as_clocks_R7`, `einstein_created_instruments_L240` |
| interaction and detectors | 55 | phase gates, 1-bit records, track detectors, trap spectroscopy |
| media | 6 | `crystal_light_and_matter` (one (−,+,+) crystal carrying light candidates at click-front speed 1 and matter candidates at 1/3) |
| seeds (big bang) | 28 | `toy_universe_v2_main`, `cascade_pure4pairs`, `planar_bigbang_L16`, `d1_skeleton_atom_spin_clocks_L160` |

**Newest modules** (tag `new`; each entry's `status` field gives its evidence label):

* `d1_local_atom_L100` / `d1_local_atom_L200` — a **locally created atom
  candidate**. One seed glider passes a class-2 junction and emits light. The light
  crosses a class-0 junction and creates a glider pair. That created glider passes
  a trapped class-2 junction, and a packet stays bound with period 20 = 2d+4 from
  t = 80. The L and 2L boards give the same birth (box check on both).
  `d1_control_no_seed_L100` is the silent control.
* `d1_skeleton_atom_spin_clocks_L160` — one seed creates light, a glider pair,
  that atom candidate and a spinor-class light ring. The ring equals its 360°
  image after each 18-update lap; 7 laps are checked. Four dark clocks record the
  emitted packet without disturbing it.
* `spin_module_pure4pairs_L80` — created spin fed by the first glider of a local
  cascade: one clean 720° double lap.
* `einstein_created_instruments_L240` — two atom clocks created after t = 0,
  joined by light. One packet's round trip gives Einstein's midpoint exactly
  (t_B = (t1 + t2)/2). The clocks' periodicity is checked here; the station passages
  are documented in the catalog.

## Checks performed on replay

For every block `verify.py`:

1. checks the init file's SHA-256 against `catalog.json`;
2. loads the file with the official loader `universe24.experiments.from_dict`;
3. runs the native Engine for the declared horizon, checking the exact inverse at every update;
4. compares the complete final state with the recorded SHA-256;
5. re-checks the generic signature fields with the native click classifier:
   first exact return (period), translation, silence, clicks and kinds per period,
   first-update clicks, and a no-return bound;
6. re-checks local **box checks**, where declared: a set of sites that is exactly
   P-periodic on a window (an atom candidate in its trap), or that equals its
   360-degree image C (every channel g → z·g, z = 14) after each lap (a spinor-class ring).

The `custom` checks named in a signature (for example `r06_cascade`,
`r08_einstein`) are researcher-specific. They were run by the source library when
the block was registered and are listed for reference; `verify.py` does not re-run them.
For 103 blocks the signature holds only `custom` checks or a prose `words` field and no
box check: for them `verify.py` re-checks the exact replay (init file hash, inverse at
every update, complete final-state hash), not the described behaviour. 30 of these have
horizon 0, so only their init file hash is checked.

## Limits and caveats

* **Prepared media.** Fibres, junctions, cores, crystals and rings are prepared hardware (data at t = 0).
* **Creation needs prepared media.** In a uniform vacuum a compact seed creates light only. A planar seed creates moving matter sheets only.
* **Torus effects.** In r06's uniform-phase networks (`toy_universe_v2_*`, the R7 recombination blocks) several created gliders and atoms exist only because the seed's own light meets itself across the torus. The `d1_*` blocks are the local alternative.
* **Not included.** Five crystal Big-Bang seeds (526,848 cells each) and other blocks over 50,000 cells are left out of this set; they stay in the program's research record.
* **Scope.** Each block's `limits` field states its domain.
* **Repeated preparations.** 21 entries form 10 groups with identical complete initial
  states (for example `light_glider_r06`, `MV_glider_alone` and `W2_fast_glider_control`);
  there are 327 distinct preparations. A name records a role in a study, not a new object.

## Provenance

`build_from_library.py` produced `blocks/` and `catalog.json` from the program's
source library (`research/matter_light_v1/blocks`) and from the researchers' init
files, recorded in each entry's `origin`. That folder is the program's local working
tree and is not part of this repository: `origin` is a provenance string, and re-running
the build needs that folder. `verify.py` does not.

## Catalog fields

| field | meaning |
|---|---|
| `name`, `group`, `file`, `file_sha256` | identifier, table group, init file and its SHA-256 |
| `what`, `limits`, `controls`, `tags` | declared behaviour, stated domain, control blocks, labels such as `new` |
| `source`, `origin`, `status`, `library_verified` | researcher, provenance string, evidence label, registered by the source library |
| `signs`, `background`, `side`, `steps`, `cells` | coupling triple, uniform background, board side, horizon, stored cells |
| `signature`, `box_checks` | declared readouts re-checked by `verify.py` (`custom` and `words` are not) |
| `final_state_sha256`, `measured` | complete final state hash; first return and native click totals |
| `composable` | `false` for board-spanning media and sheets (not placeable as a local patch) |
| `heavy` | large native cost; skipped by `--quick` |

Block names are the source researchers' identifiers and are kept unchanged. The catalog records the build time, and each
entry's `status` and `source` give the evidence label and the responsible researcher.
