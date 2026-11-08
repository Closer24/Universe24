# Conditional carrier and downstream clock: finite composition result

The 32 registered runs completed and passed independent replay. None of the eight geometry groups produced the required terminal record distinguishing the joint input `11` from **all** `00`, `10` and `01` controls. Every terminal receiver was nevertheless a quiet, isolated unit clock during states 96–112. A weaker, reproducible phase rewrite survives for receiver preparation phase 0: the joint input differs from the writer-only control but equals the null and probe-only controls.

This is a useful limit on composition. A valid conditional packet and a valid phase-writing clock do not automatically form a terminal detector with a distinct recorded outcome. No engine rule, tensor, click definition or runtime operation was changed.

## Registered preparation and observations

The complete V2 writer/probe/controller assembly was reused with controller phase 0, writer delay 2 and packet gap 38. A second complete `ClockGuideInterface` was composed at `(c+20,c+1,c)`, channel 2, where `c=L//2`. Its entire 336-triple region and guide contact were assigned through an explicit compatible socket. Both clocks were already rotating. Receiver phases 0, 1, 2 and 3, both sides 393 and 425, and all four complete source masks were fixed before execution: 32 runs of 120 updates.

A source mask removes or includes the complete packet preparation, including its remainder footprint. The source controls are initial states, not runtime switches. The tensor is fixed `+++`; Rule3 with `num=den=1` remains the only evolution rule.

The early writer and later probe were observed separately. Complete, unmasked packet boxes had origins `c+10..c+13` at states 28–31 and 66–69. All raw C at fixed `(c+12,c,c,0)` were retained in windows 27–34 and 65–72. A present epoch required the complete packet and its exact two-event C word. An absent epoch required every packet match to fail and the entire fixed-port C window to be empty. Thus another C word was never filtered into silence.

The full receiver region had a pre-late hold at states 52–60 and a terminal hold at 96–112. A quiet hold required all 336 triples to recur after four updates, a unit center with remainder 0 and exact quarter turns, all other region counters zero, center input and quotient zero, and every individual external donor term zero. The finite hold does not prove permanent retention.

## Independently verified results

All 32 source input checks, early carrier/C contracts, controller holds, pre-late receiver holds and terminal receiver holds passed. Both complete null clocks followed their prepared orbit. All 32 complete rewinds passed. There was no active boundary contact, and every initial active counter was farther than 120 spatial steps from a periodic boundary.

The table gives the effective receiver phase in source-mask order **00, 10, 01, 11**. Effective phase is the index in `(0,1), (1,0), (0,-1), (-1,0)` minus board time modulo four. Both registered sizes gave the same table.

| Initial receiver phase | Pre-late phases, states 52–60 | Terminal phases, states 96–112 | Joint late input | Strong terminal record |
|---|---|---|---|---|
| 0 | 0, 2, 0, 2 | 0, 2, 0, 0 | Exact packet; C2 at 65, C1 at 69 | Fails: joint equals null and probe-only |
| 1 | 1, 2, 1, 2 | 1, 2, 1, 1 | No registered packet; seven raw C in the fixed window | Fails: input contract and terminal alias |
| 2 | 2, 2, 2, 2 | 2, 2, 2, 2 | No registered packet; one raw C in the fixed window | Fails: input contract and terminal alias |
| 3 | 3, 2, 3, 2 | 3, 2, 3, 3 | No registered packet; six raw C in the fixed window | Fails: input contract and terminal alias |

The terminal equality is stronger than matching center phases: `11` equals both `00` and `01` on **every one of the 336 receiver triples at every terminal-hold state**, in all eight groups. Initial phase 2 was the strongest prospective AND-record prediction; it failed. That prediction remains in the frozen protocol.

For phases 1–3, all four registered joint packet frames fail the exact carrier template. Their nonempty raw C words are retained. The failure is not a claim that no influence propagated. The complete native runs show preparation-dependent interactions, but these observations alone do not isolate which returning disturbance causes the late waveform change.

## What the clocks actually do

For phase 0 and joint sources, the early writer leaves the receiver in effective phase 2. The later clean carrier changes it to phase 0. The exact late encounter is the following, on both sizes:

| Update | Center before `(a,b,r)` | Actual input `u` | Quotient `ell` | Center after `(a,b,r)` | Native C |
|---|---|---:|---:|---|---|
| 73 | `(0,-1,0)` | 0 | 0 | `(-1,0,0)` | None |
| 74 | `(-1,0,0)` | -1 | -1 | `(0,0,4)` | C2 |
| 75 | `(0,0,4)` | 0 | 0 | `(0,0,4)` | None |
| 76 | `(0,0,4)` | 1 | 1 | `(0,1,0)` | C1 |
| 77 | `(0,1,0)` | 0 | 0 | `(1,0,0)` | None |
| 78 | `(1,0,0)` | 0 | 0 | `(0,-1,0)` | None |

The negative lobe makes the two center counters zero; the positive lobe restarts their rotation two updates later. Both operations are native Rule3 updates. There is no approval function, waiting gate or external restart. The entire receiver region is quiet from state 77 through 112 in this recorded example; the registered acceptance interval remains 96–112. This earliest trailing-quiet time is a passive illustration computed after capture, not a new success criterion.

The late native events are **C2 followed by C1**, not one unique approval click. At the final receiver, `11` and the null control are indistinguishable over the registered hold, while the complete reversible board retains their different histories elsewhere. No wavefunction collapse, unique physical route, autonomous selection or loss of full-state information follows from the clock rewrite.

## Evidence and reproduction

- Frozen protocol: [`carrier_memory_protocol.json`](carrier_memory_protocol.json), SHA-256 `6309eea6e455a533258d235e884d835bb0759302f455d98659e77b035721c1ce`.
- Executed producer: [`carrier_memory.py`](carrier_memory.py), SHA-256 `899cc00bb1bd1b9b8b3e891555a164139b9086cb0b21eefbdf18787320ea6c18`.
- Whole-process budget wrapper: [`carrier_memory_budget.py`](carrier_memory_budget.py), SHA-256 `fa02185c1c424dd687a920238a7df89c4a336c6ce4c05133c28e27aa6a2495d5`.
- All captures, source snapshots, assessments and archive hashes: [`evidence/carrier_memory_v1/`](evidence/carrier_memory_v1/).
- Independent preflight: [`carrier_memory_preflight.json`](evidence/independent_audit/carrier_memory_preflight.json) and [`wording supplement`](evidence/independent_audit/carrier_memory_preflight_wording_supplement.json).
- Independent full replay: [`carrier_memory_v1.json`](evidence/independent_audit/carrier_memory_v1.json), **3,872 complete states, 3,840 transitions and inverses, 32 full rewinds**, all raw C, six donor terms and registered verdicts matched; 56.063 audit CPU seconds.
- Complete prospectively selected Presenter examples: [`experiments.json`](evidence/carrier_memory_v1/experiments.json), all four masks for side 393, initial receiver phase 2, including their failures.
- Passive exact clock illustration for every case: [`illustration.json`](evidence/carrier_memory_v1_illustration/illustration.json), produced by [`carrier_memory_illustration.py`](carrier_memory_illustration.py). It retains updates 70–82 with all six donor terms, pre-late/terminal phases and complete-region equivalences. It changes no capture or acceptance result.

The timed producer used **98.219 whole-workflow CPU seconds**, 98.139 wall seconds and approximately 15.79 MB before the final receipt, within the registered 240 CPU-second / 96 MiB limits. This includes startup, preflight, source preservation, capture, inverses, passive analysis, compression, Presenter export and archive hashing. No case was skipped or left unobserved. Independent audit and the separately requested passive illustration are separately accounted follow-up analysis.

```bash
python -m research.clock_selection.carrier_memory --preflight-output NEW_PREFLIGHT.json
python -m research.clock_selection.carrier_memory_budget --output NEW_EVIDENCE_DIRECTORY
python -m unittest discover -s tests -p test_clock_selection_carrier_memory.py -v
```

The two observer regression tests reject a writer-only distinction that aliases null/probe-only, and reject a mere halo difference without the required nonzero center phase distinction. Both pass.

## Decision

The clean phase-0 chain can be reused as a **prepared conditional phase rewrite and reversible pause/resume demonstration**, with the null-alias limitation stated. It is not a strong terminal detector. The phase-2 AND-record candidate cannot be promoted after its input and record failures.

The next decisive question is the complete scattering and memory map of the first encounter: which part of the retained outgoing state carries the receiver's original phase, and how does it affect the later probe? A causal comparison must preserve complete states and use a separately frozen preparation family. No additional geometry or longer trajectory was added after this batch, and no negative criterion was relaxed to create a positive result.
