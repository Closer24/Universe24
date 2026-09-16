# Mass-coupled computation-field experiments

These probes use the ordinary `event_universe.runner` and its existing standalone
HTML renderer. Observations are read-only world/event audits: they cannot alter
the field, routing, clocks or source values. Every run keeps the exact input,
source fingerprint, event stream, final state, accounting and recorded playback.

## Scope

The first integrated candidate contains a held mass source and nonemitting
probes. Mass selects the amount of a configured computation field, which travels
as ordinary causal rays. The timing response is the explicitly named engineering
law in the candidate contract, not an independently derived gravitational law.
Energy and momentum retain their configured family definitions.

The source Node's clock response and a free ray's response to its own emitted
field are different questions. Existing free-ray self-exclusion remains binding.
This experiment must not make every moving emitter respond to its own field,
and must not claim that a nonemitting-probe result validates that composition.

## Acceptance matrix

| Probe | Predeclared acceptance |
| --- | --- |
| Zero clock coupling | The source still emits its funded computation tokens; only the extra output wait vanishes |
| Zero source mass | No computation-field pulse is emitted and the unused reserve remains owned by the source |
| Mass variation | The frozen mass values produce the independently declared source amounts and output-ready times |
| Remote arrival | The remote Node's prefix matches its control until the first actual field arrival; there is no effect from an unarrived source |
| Source locality | A held mass Node uses the same eligible local-field rule as an otherwise identical Node |
| Six output faces | Distinct frozen local loads can give distinct release times; an occupied output clock does not postpone input receipt |
| Link timing | Every sent packet's actual arrival is exactly the declared fixed Link duration after actual departure |
| Equal field | Equal eligible local inputs and otherwise equal local state give equal output delays at separate Nodes |
| Unchanged free ray | Existing isolated rest, straight-motion and external-field controls keep their established self-field behavior |

Readiness and conservation concern actual ownership at the current Node or
Link, not a future timestamp assigned to inventory that was already removed.
Changing playback speed never changes any expected tick.

## Reproduction

Select the project Python interpreter and this checkout's `src` explicitly.
Pass a new output directory. The authoring adapter writes complete candidate
inputs and the normal runner validates each one before execution:

```text
python examples/mass_computation/run_experiments.py --output artifacts/mass-field-check
```

Select one fixture with `--case M1` (repeat the option for several fixtures).
The frozen numerical expectations are in `expectations.json`; they precede runs
and reference the candidate design commit. `configuration.py` defines reusable
family data and each fixture's initial placements. C1/C2 receive their probes
through ordinary causal Links, without external scheduled injection.

The command prints each generated `run.html` path. `summary.json` records the
ordinary runner's completion, integer accounting and source identity. A completed
process and balanced configured quantities do not establish agreement with
experimental gravity, a strong/weak interaction law or emergent spacetime.
