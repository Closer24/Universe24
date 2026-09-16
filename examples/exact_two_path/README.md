# Exact finite two-path benchmark

This configuration exercises the active engine's ordinary whole-record transport
and local atomic interactions. It is an analytical interference benchmark, not an
electron, a Detector, a Bell experiment or empirical confirmation of nature. It
uses the existing Node scheduler; it does not implement per-Port Register queues.

The separate [Port execution comparison](PORT_EXECUTION.md) uses this fixture as
an unchanged acceptance workload for an interim host scheduler. That adapter does
not implement the proposed 24 internal single-input/single-output Registers.

Two preallocated mode records carry `(real, imaginary, 0)` amplitude numerators.
The declared amplitude scale is 25 and never changes. The records are two modes,
not two particles. There is no duplicated particle, charge, mass or energy
inventory. The amplitude norm is a separate quadratic quantity; the runner's
empty additive-conservation totals do not establish its conservation.

The initialization JSON contains all local laws. The preparation script only
chooses a fixed quarter-turn matrix before execution and changes the optional
initial numerator for the negative control. Engine code never branches on these
mode names. The existing payload codec stores nonnegative mathematical values
as `2*v+1` and negative values as `-2*v`; zero is encoded as 1. Signed temporary
arithmetic remains bounded by the existing core contract.

At the origin, the configured local interaction applies
`C = [[3,-4],[4,3]] / 5`, taking `(25,0)` to `(15,20)`. Both modes then move four
nearest-neighbor hops on a periodic `6 x 6 x 6` board. Mode A takes XXYY and
mode B takes YYXX from `(0,0,0)` to `(2,2,0)`. The configured phase operation
occurs on the second local route stage. `C^T` recombines the co-located modes.
Both outputs travel through +Z to the passive output position `(2,2,1)`.

| Relative phase | Output A | Output B | Squared weights |
| --- | --- | --- | --- |
| 0 | 25 | 0 | 625, 0 |
| pi/2 | 9 + 16i | -12 + 12i | 337, 288 |
| pi | -7 | -24 | 49, 576 |

The squared norm remains 625 across every resident and in-flight ownership
snapshot. Quarter turns use exact integer sign/permutation operations; division
by 5 must be exact. Initial numerator 1 is rejected at tick 0 before the local
proposal commits, rather than rounded. Pair invariants guard both matrix
interactions atomically. Metadata and whole-record slots preserve zero-amplitude
mode readiness and prevent coalescence or deletion.

Timing is an explicit benchmark control: `normal_budget=100000`, commit cost
100000 and every other primitive cost 1. Actual nonempty cycle costs range from
100070 to 100195, so the existing cost law gives one tick of local waiting and
one tick of Link transit. Splitter commit is tick 1, path receipts are ticks
2/4/6/8, recombiner commit is tick 9, and output receipt is tick 10. This tariff
does not identify mass, physical action, proper time or a universal delay law.

From the repository root, using the configured Python 3.14 environment:

```sh
PYTHONPATH=src python examples/exact_two_path/run.py --phase zero --output artifacts/exact-zero
PYTHONPATH=src python examples/exact_two_path/run.py --phase quarter --output artifacts/exact-quarter
PYTHONPATH=src python examples/exact_two_path/run.py --phase half --output artifacts/exact-half
PYTHONPATH=src python examples/exact_two_path/run.py --amplitude 1 --output artifacts/exact-nonexact
python -m pytest tests/test_exact_two_path.py -q
```

Use a fresh output directory for each command. Every explicit run creates its
input, events, metadata, final state and canonical HTML with the existing renderer.
The negative-control command intentionally exits with `ValueError` and retains
failed-run HTML. Automated tests are headless.

The first execution used main `e5b5911ab13373e08345cf971a6ae8d7e9cb462e`, active
source fingerprint
`4e0c9eeffd4a1ce1bb832c0687913c71a8c44dd4d79d100296c42e9238f50c36`, and Python
3.14.7. All three phase runs completed 12 ticks and matched the independent table;
the negative control rejected before mutation. Four focused tests and Ruff passed.
The canonical HTML contains the actual recorded frames; no browser interaction
or visual layout verification is claimed.

This finite integer lattice is not closed under arbitrary repeated `/5`
operations. The route and apparatus are prescribed, with no apparatus recoil,
general wave dispersion, particle creation or joint physical-energy closure.
The result validates only this finite configured transfer and interference map.
