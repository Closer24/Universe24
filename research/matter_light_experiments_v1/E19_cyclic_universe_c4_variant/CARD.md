# E19 — VARIANT chiral-011-mpp@190301d802c5: C4, seven prepared, non-interacting sectors on one board, sharing one bang and turnaround schedule (period 320), with the weak-like and EM-like signatures

## On the event board
- EXPLICITLY SEPARATE CANDIDATE VARIANT (AGENTS.md), not the reference model: axial m = (0,1,1), signs (−,+,+) (only
  the ±z body actions differ from (−,+,+)), fixed before t = 0; table reviewed clean by r16 and valid for FRESH 11; every
  run is the variant runner's audited run (VariantEngine, exact inverse at every update)
- board: L = 320 and 2L = 640, 960 updates (3 cycles), vacuum (0,0,2); r36b's variant init files byte for byte; the seed
  has b = 0 on every channel and is the disjoint union of seven parts, each at its own half moment: the C2′ light and
  matter segments, the spin box loop, the lamp ring and tap fibre, the ring clock, the free line, the twin-cavity module
  and r30's forces sector (two mirror-geometry skew rings on a bang line, a like and an unlike M4r_η charge pair)
- [THEOREM] JR∘F∘JR = F⁻¹, JR(a, b, r) = (−b, −a, r): half moments at ½ + 160ℤ give period 320; the board equals the
  union of its parts at every update, in state and in clicks (R10G-119, FRESH 11; not re-run here)
- runs: C4 on L and 2L, its expansion (160) and contraction (rewound 160, then 160), the free ring-clock calibration

## In the clicks (decoder 1.0 and its released layer log_symmetry_v1)
- log_symmetry_v1: 3 byte-identical cycles of 23,480 records; 2L gives the same 70,440 records; each contraction is the
  click mirror of its expansion about the half moment 160.5 (n ↔ 322 − n: 319/319, silent update 161); the whole log
  mirrored about 480.5, unique, 0 unpaired; the spin ring's C-image after 32 updates on 288/288
- expansion ("created" by the decoder's positional rule, inside prepared modules): created light at exact −1 (born 84),
  a created glider pair at exact (0, ∓1/3, 0) born at 89, and both twin atoms read while forming (period 20, born 23)
- weak-like: the bang light (exact ∓1) reaches the skew rings at 59; decay light leaves the mirror-geometry ring
  (x = 217) at 91 (exact −1) and the other (x = 103) at 115 (exact +1): lifetimes 32 and 56; both end at x = 148 = O − 12
- EM-like: the like charge pair is a period-10 source (3 sites); the unlike pair gives 0 clicks in 960 updates
- contraction: both atoms over [1, 138] (un-forming), the matter tracks converging at exact 1/3, the decay light back on
  O = 160; whole log: network 160, ring clock 20 (one free packet 12: N = 12/20 = 3/5), lamp period 32 on [24, 122],
  spin ring 64 on 28 sites with channel-free period 32 (720°), atoms 20 over [24, 298]

## Claim
- [THEOREM + SIMULATION] under the variant: seven prepared, non-interacting sectors (the board equals the union of its
  parts at every update, in state and in clicks), sharing one bang and turnaround schedule: light, matter (exact ∓1/3)
  and twin cavity atom candidates created by the decoder's positional rule inside prepared modules (the atoms from the
  bang's packet pair, in prepared zero-counter cavities with prepared escorts), a 720° spin ring, a ring clock at
  N = 3/5, and r30's weak-like and EM-like signatures; the charges are prepared, the rule acts at contact only
- not claimed here: the α_in = 1 instrument pair (the probe needs a difference layer); context only: R10G-118 and FRESH 11
  (PARTLY), v_in = 3/5 per two-crossing period (steps 8/12), a1v.json reads 21/34
- reference beside it: C3c under (−,+,+) has the six other sectors (E18, FRESH 8); r30's rings synchronise (R10G-105)
- referee: remote fresh-machine referee FRESH11-C4 CONFIRMED in every core claim; r10g R10G-111..117 and 119 CONFIRMED,
  R10G-120 PARTLY (wording, applied above); nothing emerges from a uniform vacuum; no statement about the reference model

Reproduce: python -m research.matter_light_experiments_v1.verify E19_cyclic_universe_c4_variant
