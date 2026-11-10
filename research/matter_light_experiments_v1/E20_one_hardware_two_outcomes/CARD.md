# E20 — One hardware, two outcomes: on identical hardware, two prepared initial states differing only in escort B's starting end h light only exit B (h = 0, exact cycle 90) or only exit C (h = 1, 320)

## On the event board
- coupling +++ (reference), vacuum (0,0,2), L = 256 and 2L = 512; builder D's device CC7-M as ONE registered guide_net@1
  placement (select.escort_end_junction@1): a junction X, an input line A, exits B (+x) and C (+y) behind doors, each
  door an X-gate on a private escort line bent away 4 nodes from it; three fibre-light packets (r04 guide packets,
  speed 1) of profile C = (1,−1,0), each 6 nodes before a bare end: the quantum on A, escorts B and C (candidate names)
- one hardware: identical guide paths; two prepared initial states differing in 14 cells, all on escort B's line or its
  face neighbours; the one initial datum, escort B's starting end h = 0 (lower arm) or 1 (upper arm), is a part of the
  prepared state, not of the hardware; the members equal builder D's init files exactly; nothing acts after t = 0
- [THEOREM] JR∘F∘JR = F⁻¹, JR(a, b, r) = (−b, −a, r): the click record is mirrored about an integer moment (a = −b
  everywhere; u ↔ 2τ + 1 − u, kind → −kind, q → −q), and two moments τ1 < τ2 make the period divide 2(τ2 − τ1) (r36)
- [SIMULATION, R10R-2..4] integer moments 9 + 45ℤ (h = 0), 9 + 160ℤ (h = 1) (R4's profile A = (1,0,−1), which contains
  both phases, gave half moments); exact returns at 90 and 320; over 3 cycles the unrealized exit's line sites keep ONE
  complete state (with the door sites, their face neighbourhood takes 4 or 5); runs forward only, the inverse an audit

## In the clicks (decoder 1.0 and its released layer log_symmetry_v1, official click logs)
- h shows from update 1: escort B's 4 clicks then are on its lower (h = 0) or upper arm (h = 1); first exit click 23 / 53
- h = 0, per cycle: exit B 132 clicks, its detector D_B 32 records, clock B 8 ticks; exit C, D_C and clock C 0; the
  decoder reads the lit clock as a period-16 source on exit B's five sites, beside the device's period 90
- h = 1, per cycle: exit C 524, D_C 104, clock C 26 ticks; exit B, D_B and clock B 0 (decoder 1.0 reads no source here,
  a disclosed limit); only one detector ever clicks in a cycle (record counts, not single clicks)
- no C0 click in either run (0 repaid, 0 unrepaid; unit-quantum regime, |b| ≤ 1)
- log_symmetry_v1: 3 byte-identical cycles (880 and 3,160 records), mirrored about all 6 moments; L = 2L: same records
- controls, no quantum (h = 0, 1) and no escorts: both exits click-free, exact cycles 90, 2880, 30; all clicks on guides;
  the no-quantum controls show that the exit and detector clicks need the quantum: without it no exit fires

## Claim
- in plain words: for an observer who reads only the declared detectors D_B, D_C, the outcome is known only through the
  detector click; in the full official log the datum h is visible from update 1 (R10R). One device, prepared twice with
  escort B starting at one end of its line or the other, lights exit B or exit C, never both, in every cycle of both
  prepared members (3 cycles each); the click-free exit has 0 records. Which exit clicks is fixed by the initial data;
  nothing on the board is erased; the unlit exit is the untouched prepared fibre, not a dark travelling branch
- [SIMULATION, exact; THEOREM: the mirror and the period bound] one hardware, two prepared states, two exact cycles
- not claimed: that the quantum or the device makes the outcome; a selection law (C2 is an arithmetic class); ensemble
  probabilities; other sign triples standalone; more than 3 cycles; the meshing argument (R10R-11; see E20b)
- referee: local referee r10r, R10R-0..13: 13 CONFIRMED, R10R-11 PARTLY (meshing proof wording; not claimed); re-runs
  confirmatory (R5-1) except the blind no-quantum h = 1 period and E20b; R4: FRESH 19; this package: fresh machine 2

Reproduce: python -m research.matter_light_experiments_v1.verify E20_one_hardware_two_outcomes
