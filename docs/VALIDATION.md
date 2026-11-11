# Fixed-six implementation validation

The default now uses local message transport and reception, with 54 channels
and 306 linear terms. [Local communication](LOCAL_COMMUNICATION.md) gives the
proof and controls. Fresh results and source hashes are recorded separately in
[local_communication.json](evidence/local_communication.json). The 48-channel
checks below belong to the explicit `--model reference` construction.


The common scalar divisor is now six. Validation must identify the current
tensor and complete initial state; old variable-divisor hashes or physical
calibrations are not acceptable substitutes. The migration intentionally
retires the earlier 382-channel assembly and its dependent research presets.

## Local communication validation

At the communication change, the complete suite passed **125 tests**, including
seven transport and reception checks. The size-three, 20-update communication pulse records
**120 edge messages** and **11685 official clicks**, and rewinds the
complete seed exactly. The independent scalar oracle checks **324** transitions
without mismatch; strict support has zero violations, and the saved 12-update
run replays exactly. Both message and official-click logs are passive.

The new tensor fingerprint is
`fc3076f34ff0240e5069ae786b745c3a33c0c528867d0b20ef4ceff46b72f0ce`.
The [evidence record](evidence/local_communication.json) includes source hashes,
commands, complete seed metadata and the explicit prior-reference comparison.

## Recurrent-burst audit validation

The complete suite now passes **134 tests**, including nine
[burst-audit checks](../universe24/tests/test_recurrent_bursts.py). All 25
experimental histories rewind exactly; the independent scalar oracle checks
**5,832 transitions** across 18 feedback tensors with zero mismatches. The
[report](RECURRENT_BURSTS.md) and [evidence](evidence/recurrent_bursts.json)
record the failed physical target separately from successful software checks.
No case demonstrates stagnation-driven recurrent bursts with growing structure.

## Verified earlier fixed-six migration results

The migrated full suite completed **118 tests** successfully. All 74 non-test
modules imported and all 33 exported layer names resolved. The explicit reference mode
uses 48 channels, 288 linear terms, actual tensor order two, and fingerprint
`b84ddee525ad22ce903b6183fd9b9bf88a754d0c967a1d3af58f7d840f46941b`.

The [migration evidence record](evidence/fixed_divisor_repository_migration.json)
includes the tested source hashes, commands and current default census.

A size-three reference pulse run completed 20 updates with 75 official records
and exact rewind. The independent scalar oracle checked 288 transitions with
no mismatch; the support audit found no strict-locality violations, and a
12-update saved-input replay matched exactly. These are reproducible software
and arithmetic checks, not evidence of general relativity or quantum theory.

The bounded-circuit evidence was regenerated at divisor six: all three
24-update histories have 48 C0 records, exact rewind, legal remainders and
proved prepared-sector periods 12, 24 and 4. Its new tensor and state hashes
are not asserted equal to the retired records.

## Required checks

| Check | What a passing result establishes |
|---|---|
| Independent scalar oracle | Agreement with the fixed `divmod(2*u+r,6)` operation |
| Full-state forward and inverse | Recovery of every retained `a,b,r` value |
| Integer overflow guard | Exact fallback to arbitrary-precision arithmetic |
| Tensor support and dependency validation | Declared locality and staged inverse assumptions |
| Official-event replay | Agreement with the specified passive event definition |
| Reference-group checks | The stated finite-group identities and matrix relations |
| Fixed-six migration fixtures | The current declared construction's complete traces |
| Prepared-sector examples | Their stated invariants and explicit negative controls |
| CLI and installed-package smoke runs | The public run/replay paths execute successfully |

The checks do not prove physical interpretation. A test deliberately verifying
an instability, failed constraint or missing signal response is a successful
software test of a negative scientific result.

## Reproduction

```bash
python -m pip install '.[validation]'
python -m unittest universe24.tests.test_communication universe24.tests.test_one universe24.tests.test_migration -v
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m unittest discover -s universe24/tests -t . -v
python -m universe24 --L 3 --tmax 20 --budget 120 --out runs/demo --tag demo --rewind
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

Fresh records belong under `runs/`. The fixture for the migrated default is a
new fixed-six record; it is not asserted equal to the retired assembly.
Legacy serialized laws with a nonunit divisor scale must be rejected clearly.
A legacy record with the same divisor may be accepted only by an explicit
compatibility reader that preserves the integer law.

## Optional geometry checks

```bash
python experiments/geometry/reciprocal_metric_candidate.py
python experiments/geometry/metric_transport_candidate.py
python experiments/geometry/linear_spin2_check.py
python experiments/geometry/retimed_tensor_wave.py
python experiments/geometry/ppwave_palatini_local.py
python experiments/geometry/ppwave_geodesic_clock.py
python experiments/geometry/ppwave_geodesic_audit.py
```

Their [index](../experiments/geometry/README.md), algebra notes and fresh JSON
records specify each seed, tensor, completed horizon, exact checks and failed
physical conditions. The last command is an independent optional symbolic
audit of a restricted continuum geodesic, not a second evolution algorithm.

## Historical results

The [pre-fixed-six archive](archive/pre-fixed-six/README.md) contains old
validation tables and evidence under their original assumptions. Counts such
as an earlier complete suite size, a long large-divisor run or a former
clock-rate result do not establish the corresponding property of the new
model. Historical results are retained for comparison, not silently updated
by textual substitution.
