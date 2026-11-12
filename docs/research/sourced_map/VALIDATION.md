# Final local validation ledger

Baseline: central integration `f4f64e062f07b3ca119eccf655df746be206908b`.
The final research source, tests and saved-run evidence passed the checks below.

| Check | Executed result |
| --- | --- |
| Full `unittest` discovery | **405 tests passed in 246.164 seconds** |
| New sourced-map regression module | 14 tests passed, including complete-history, source removal, near-branch bigint decoding and shifted runtime origin |
| `python -m validation.sourced_map.run_all` | All eight audits passed on the final sources |
| Source/evidence integrity | All ten package source hashes and eight committed evidence hashes matched; compressed trace round-trip passed |
| Generic runtime smoke and CLI verification | Passed at `runs/sourced-map/local-smoke` |
| Independent review | All 16 Einstein components, actual native endpoints, phase quadrature and adversarial controls passed |
| `git diff --check` | Passed |

The complete unit-test log is `runs/sourced-map/logs/unit-tests.txt`.
The collector at `runs/sourced-map/collection.json` identifies each exact
module, source hash, execution log and evidence artifact. The large native
trace is committed as deterministic `runs/sourced_map/native.json.gz`; its raw
JSON hash is recorded separately. All five saved-run directories referenced
by `runs/sourced-map/runtime.json` are included with their complete bundles,
traces, canonical clicks and generic verification reports.

## What the passing checks establish

The unchanged Rule3 Engine, with one immutable six-channel linear tensor,
exactly samples the declared massless scalar/dust FLRW flow. The proof uses
the complete history invariant, and the physical reconstruction satisfies the
Einstein and matter equations in that homogeneous expanding chart. The
independent physical reference executes twelve source/resolution runs; the
native scalar audit contains eleven cases and 26,244 integer comparisons.
The saved-runtime audit contains five runs and 13,122 scalar comparisons.
These totals overlap and are not summed into a larger independent experiment count.

The ordinary native fixtures peak at 18 bits per retained integer. Separate
large-integer review/regression controls deliberately exceed that size. The
proof of logarithmic growth is for fixed preparation, not a uniform bit bound
over all possible initial integers or near-singularity calibrations.

## Corrections and retained failures

Independent review found a real numerical cancellation in the passive scalar
phase near its branch boundary. Exact rational differences and branch products,
followed by `log1p`, now preserve both zero and nonzero phases. An actual native
Pell-family step agrees with a separate 400-digit direct evaluation to about
`2.22e-82`. The runtime reader also now permits a shifted coordinate-time origin
consistently with its constructor, and rejects equal-resolution comparisons
mislabelled as different resolutions.

The original massive first-step and tick-two history failures remain present.
The new massless map rejects a massive interpretation. Removing its actual dust
response or starting off the constraint does not become physical success merely
because inversion works. Positive endpoint volumes do not establish a physical
path through an intervening singularity. Pure-source and contracting charts are
not silently admitted by this decoder.

The separate massive-method analysis supplies exact rejection results and an
approximate second-order target, not a massive native implementation. General
spatial Einstein dynamics, operational clocks, apparatus and physical click
interpretations remain unestablished; generic runtime physical gates remain
`not_tested`.

`.github/workflows/sourced-map.yml` repeats full discovery, the eight audits and
fresh generic smoke/replay on Python 3.11 and 3.12. Remote CI results belong to
their published exact commit and are reported on the pull request separately.
