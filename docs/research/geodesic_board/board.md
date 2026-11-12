# One saved-run event board

`validation/geodesic_board/board.py` is a passive HTML renderer. It takes the
same report emitted by `validation.geodesic_board.run`, embeds that report as
escaped JSON, and writes a self-contained page with no third-party scripts,
network requests or alternate evolution engine.

The page shows the saved node-event slice at y=z=0 and the null/timelike
readout paths lying in that slice. The +y null control remains in the full
report but is excluded from this x-t section, rather than misleadingly
projected into it. Horizontal positions use physical distance
`sqrt(gamma_xx(t))*x`; the full spatial metric is displayed alongside it.
The interpolation of gamma used for drawing paths matches the readout's
piecewise-linear gamma convention. Saved time controls select recorded
slices and never advance the retained state.

The sidebar reports energy, scalar/dust contributions, charge and signed
Hamiltonian residual from the same saved run. Status rows are read from the
report's actual acceptance gates. General Einstein convergence and quantum
physics are not asserted. The board explicitly distinguishes saved
computational events, passive test paths, and physical detector outcomes.

## Reproduction

```bash
python -m validation.geodesic_board.run --out runs/geodesic-board
# Or render an already-produced report without rerunning dynamics:
python -m validation.geodesic_board.board runs/geodesic-board/board_data.json
```

Open `runs/geodesic-board/board.html`. The renderer does not modify its input
report. It rejects empty snapshots and JSON nonfinite numbers, and escapes
less-than signs before embedding data so labels cannot close the script tag.

## Verification performed

An actual four-update massive corrected45 run rendered successfully: 45
channels, 889 monomials, 27 nodes, peak 186 retained bits. The embedded
JavaScript executed against a DOM/canvas test harness across all five saved
slices and the play control, with finite drawing coordinates and source-based
status rows. These are JavaScript/data checks, not a browser visual check.

A real Chromium launch was attempted using Playwright and `/usr/bin/chromium`.
The managed process sandbox rejected Chromium's singleton `socket()` call
with `Operation not permitted`. Therefore this run did not produce a browser
screenshot or establish responsive visual QA; that limitation is explicit.

## Offline report trust boundary

Before rendering, `validate_report` rejects unknown schemas, inconsistent
run/bundle/tensor/trace identities, count or bit-cost discrepancies, missing
node snapshots, diagnostic alias disagreements, unsupported promoted gate
statuses and missing runtime checks. It recomputes the passive geodesics from
the supplied metric snapshots and rejects stale or forged path arrays.

These are report-consistency checks. A malicious author could construct a
self-consistent false report; an offline JSON renderer cannot prove the
provenance of hidden Engine states. Re-run the unified `verify` path on the
saved bundle and complete trace to establish execution provenance. The page
states that boundary and does not label its own consistency checks an
independent physical validation.

The reproducible JavaScript audit used by CI is:

```bash
node validation/geodesic_board/check_board.cjs runs/geodesic-board/board.html
```

It parses the embedded report, executes the actual embedded script against a
minimal DOM/canvas harness, visits every saved slice, checks displayed source
energy/constraint values and the replay status, and exercises playback start,
pause and completion. It rejects nonfinite canvas coordinates and reports
script/harness SHA-256 identities plus run/bundle/tensor identities. It does
not claim browser layout or screenshot verification.
