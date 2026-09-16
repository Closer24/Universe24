# Private36 two-detector experiment

This integrates the existing one-number shared-pair law with the private cubic
Register scheduler. The [published design](../../docs/PRIVATE_REGISTER_CONTACTS.md)
was committed before implementation as
`df1de27c67dbe94cc1ac020ad4ea812bf49a78c1`.

Use Python 3.14 and the selected checkout explicitly:

```sh
PYTHONPATH=/absolute/checkout/src python /absolute/checkout/examples/private_bell/run.py \
  --source /absolute/checkout \
  --input /absolute/checkout/examples/private_bell/input.json \
  --output /absolute/output/private36-bell --samples 64
```

The example supplies all 36 directed routes per Node. Two initial endpoint tokens
travel three one-tick Links from one source to distinct detectors six Links apart.
Each detector retains its token and outcome at tick 3; the final tick-4 snapshot
contains two terminal owners and no traveling copies. There is no implicit split
or new particle-generation rule. The renderer keeps ordinary cubic lattice Nodes;
Register addresses and retained outcomes are readouts. `detector_binding` markers
show configured locations and are not extra token inventory.

Each setting/number configuration runs both dense and sparse scheduling. Complete
physical and quantum state hashes must match at every recorded tick. Each actual
run emits the existing renderer's `run.html`, input, events, hashes and metadata.
The quantum counter must show one number and two endpoint requests per pair.

The default CHSH probe uses 64 deterministic midpoint numbers over the bounded
number interval for each of four settings `(0,8)`, `(0,24)`, `(16,8)`, `(16,24)`.
This finite quadrature is distinct from a random sample or confidence interval.
The independent negative control makes the first detector return +1 and the second
-1 from its local end definition, with no quantum owner. Both controls still
require actual token arrival and terminal private retention. Its CHSH value is 2.

The shared resource explicitly uses both detector settings. A CHSH value above 2
therefore checks integration of the existing quantum model, not emergence from
Bell-local hidden variables. This experiment does not migrate all catalog entities
and couplings, add generic beam splitting, or replace the native two-draw program.
The [acceptance tests](../../tests/test_private_bell.py) also cover delayed ordering,
completed replay, stream exhaustion and atomic failures.
