# QuietClock: a reusable prepared-clock component

`QuietClock` is a research-only factory returning an immutable initial Patch.
It adds no runtime method, force, gate or update stage. The unchanged generic
composer and Rule3 engine perform all subsequent assembly and evolution.

```python
from research.components import BoardSpec, TensorSpec, finalize, place
from research.clock_selection.quiet_clock import QuietClock

tensor = TensorSpec.from_signs((1, -1, 1))
clock = QuietClock(channel=17, a=1, b=1, r=3,
                   halo_parity=1, tensor=tensor)
prepared = finalize(BoardSpec(7, tensor=tensor), [
    place(clock, at=(3, 3, 3), name="clock"),
])
```

The initial center pair may be any nonzero integers with `|a|+|b|<=2`, including
unit counters, amplitude2 axes and diagonal pairs(+/-1,+/-1). The center
remainder may be any integer0..5. All48 channel labels and all eight currently
allowed TensorSpec sign families are supported. A chosen `halo_remainders`
tuple supplies six exact residues, or the factory chooses admissible residues
near the stationary background, optionally with `halo_parity=0` or1.

The returned Patch explicitly assigns all336 triples on the center and its
six neighboring nodes. Its ports expose `center`, `center_node`,
`outgoing_recipients` and `region`; its data-only contract records each
recipient, signed weight, valid remainder interval, fixed tensor and environment
requirements. Outgoing recipients are derived by inverting the opposite
direction's incoming map, rather than assuming a table direction convention.
Conflicting shared assignments are rejected by the existing composer.

## Proven behavior and scope

With no additional input to this protected center/halo and zero other counters,
the center follows `(a,b)->(b,-a)`, while each halo remainder follows its signed
cumulative input. The prefix values are `0,b,b-a,-a`, whose span is
`|a|+|b|`. Choosing each recipient's initial residue in
`[-2*min(prefix), 5-2*max(prefix)]` keeps all halo quotients zero. A valid choice
exists exactly when the integer L1 amplitude is at most2. The complete isolated
state therefore has minimal period4, and no guarded C occurs.

This is a preparation theorem, not a promise under arbitrary external input.
It does not establish signal activation, a driven detector, physical time or
mass. Joining another component requires agreement of every shared triple and
a new behavioral test; passing initial composition alone cannot certify that
interaction. The factory leaves the core component library and engine unchanged.

## Registered validation

The [protocol](quiet_clock_protocol.json) has SHA256
`a0198c4f4e79c1c1afe6ecd34620ec49615e338152038d9cb8f16610ab04d7af`.
Before evolution, independent exact4x4-matrix routing checked all384
channel/sign combinations, and384 full initial-state comparisons checked all48
proper orientations for all eight sign families. Four contract tests cover
amplitude rejection, residue/parity bounds, independently reconstructed outgoing
ports and conflict rejection. The separate
[preflight review](evidence/independent_audit/quiet_clock_preflight_review.json)
reconstructed all48 registered full preparations and every outgoing map.

All48 native cases then passed: eight fixed sign tensors, three amplitude
orbits `(0,1)`, `(0,2)`, `(1,1)`, and two remainder parities, with explicitly
registered representative channel labels. The two sizes are5 and7 and the
horizon is8. The [complete result](evidence/quiet_clock_v1/result.json) retains
432 full states,384 transitions and all full-state inverse checks. Every saved
state equals the complete analytic formula; every minimal period is4; no
guarded C occurs anywhere; and only the center has nonzero counters. All24
parity pairs have identical counter traces and seven remainder offsets of+1.
Producer source verification passed. The separate
[independent full replay](evidence/independent_audit/quiet_clock_v1.json) also
passed:432 full states,384 forward/inverse transitions, complete rewinds, every
analytic whole-state phase, no guarded C, minimal period4 and all24 parity
pairs. The independent audit used2.16 CPU seconds.

The complete output initially occupied1,500,724 bytes. External whole-process
measurement of capture, analysis and export was7.643893 CPU seconds. The prior
preflight section measured9.009289 CPU seconds in another process, excluding
that process's startup. Therefore a complete whole-session60-second CPU budget
certificate is unavailable; this limitation is retained explicitly in the
[measurement receipt](evidence/quiet_clock_v1/capture_process_time.json).

## View and reproduce

[The Presenter](evidence/quiet_clock_v1/The_Presenter.html) contains six fixed
examples covering all three amplitudes and both parities under+++. It reads
complete native records; viewing or rotating the cube does not affect evolution.
All48 complete records remain in the evidence folder, including other signs.

```sh
python -m unittest tests.test_quiet_clock -v
python -m research.clock_selection.quiet_clock --prepare --output new-quiet-clock-run
python -m research.clock_selection.quiet_clock --run --output new-quiet-clock-run
```

The preparation command does not evolve the board. Review its registration
before the execution command. A registered run cannot be overwritten or
restarted, and source changes after registration are rejected.
