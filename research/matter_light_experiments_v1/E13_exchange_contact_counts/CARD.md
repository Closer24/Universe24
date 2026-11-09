# E13 — exchange contact counts on prescribed field lines: a fixed-area probe meets the prepared geometric count (192/r)²

## On the event board
- coupling +++ (reference), quiet vacuum (0,0,2), side 200; two compositions, each ONE placement of the registered
  generator field_line_bundle@1: 64 open gauged staircases from O = (0,100,100) toward (8, 2j+1, 2k+1), j, k = −4…3,
  from x = 16 to x = 100 (the +x bundle of a 384-line cube-gnomonic source); no junction; r04's halo condition is
  checked (no shortcut, no shared halo channel)
- prescribed_flux: one outward (1,0,−1) quantum per line at its root; created_flux: no quantum in flight, but 64
  prepared, in-phase one-shot emitter cores (−1,0,0), one in the −x halo slot of every root
- probe surface S(r): |y|, |z| ≤ 24 on the plane x = r (fixed area 48 × 48), r = 24, 32, 48, 96; probe: one inward
  (1,0,−1) quantum on every line crossing S(r); station: node 1 of every line
- runs, packet masks: the probe at each r without flux, with the prescribed flux and with the created front; two
  flux quanta per line at r = 48; flux only; front only; dark; 31–111 updates. E13b's no-core runs are the no-flux
  runs here (identical initial states). After t = 0 only Rule3 acts; nothing is injected or read back
- algebra: guide lemma (r04, THEOREM): one node per update; a head-on contact delays both quanta by exactly 4 (r04,
  r22, r23); a probe crossing the created front is delayed by exactly 2; co-moving quanta never meet. Central
  projection: (2·24·4/r)² = (192/r)² lines cross S(r), and each crossing line gives exactly one contact
- clocks: line nodes are gears at θ = 2; a passing quantum turns one 2→0 (C1, q = +1) and 0→2 four updates later
  (C2, q = −1); the lines alone are dark; each core fires its root once (t = 2) and starts a front

## In the clicks (decoder 1.0; the stations through its own correlations over the declared window [8, 111])
- no flux: each crossing line's station first clicks at its free arrival; prescribed flux: exactly 4 later on 64, 36,
  16, 4 lines at r = 24, 32, 48, 96, i.e. (192/r)²; two quanta per line at r = 48: 8 later on its 16 lines
- created front: exactly 2 later on the same 64, 36, 16, 4 lines; the stations of the lines outside S(r) stay silent
  in all three; flux only and front only (from t = 8): no station clicks; dark: 0 clicks

## Claim
- [THEOREM (count) + SIMULATION (clicks)] (r33, declared 03:40 and 04:11 UTC): the contact count of a fixed-area probe
  equals the prepared geometric count (192/r)²; the delay per probe quantum is 4 (prescribed flux) or 2 (created
  front) at every r, so there is no fall-off per probe; r²·delay = 4·192² (and 2·192²) is an identity by
  construction: geometric bookkeeping, consistent with contact-only interaction (r18 T2), not a force law
- created means the front only, from 64 prepared, in-phase one-shot cores on 64 prepared lines; it leaves a dark
  rotating wake (behind it the probe's clicks begin with C2)
- no sign, for the 74 clean contacts only [EXHAUSTIVE r33, 1,296 head-on contacts]: 68 delay both quanta by 4, 6 pass
  unchanged, none advances or reflects a quantum; the other 1,222 are not classified (R10G-50). Magnitude only
- limits: prepared lines (their geometry puts the count in); no recoil; static charges (r18 T4); contact only (T2)
- referee: r10g R10G-46, 47, 49, 78, 79 CONFIRMED; R10G-48, 50, 80, 81 PARTLY (their wording is used here);
  R10G-82, 83 NOT CHECKED (r33's one-lamp bound and coincidence receipts; neither is claimed here)

Reproduce: python -m research.matter_light_experiments_v1.verify E13_exchange_contact_counts
