# Configured BCC vector encounter

[bcc_vectors.json](bcc_vectors.json) is a complete runtime input. The simulator
reads it directly; no code generation or compilation is required for edits.
The [topology contract](../../docs/CONFIGURED_TOPOLOGY.md) explains the optional
environment schema and the independent 2/4/6/8/12/18/26-port checks.

The example selects an even periodic 8 by 8 by 8 coordinate box and the BCC
same-parity sites: 128 nodes, eight reciprocal body-diagonal links per node.
Each link takes one tick. Forward and backward three-component amplitudes start
at (2,2,2) and (6,6,6) and propagate along opposite diagonal links.

When both arrive at one node, a JSON `transform` permutes each amplitude's
components from (x,y,z) to (y,z,x). This is a signed-integer-compatible 120-degree
rotation around the (1,1,1) axis. Separate configured guards preserve each squared
norm and its transverse condition. This is a supplied candidate encounter law,
not the old cardinal cross-product quarter-turn and not a derived Maxwell law.
No simulator code branches on the mode names or candidate identity.

For these two isolated modes, including actual in-flight owners, the independent
test verifies normalized diagnostics at every recorded tick:

- Forward squared norm: 18; backward squared norm: 8.
- Candidate energy U = 18 + 8 = 26.
- Direction-weighted norm Q = 18(1,1,1) + 8(-1,-1,-1) = (10,10,10).
- Both amplitudes remain transverse; their sums of components remain zero.

The rotations appear after co-locations at ticks 2 and 6. Periodic wrapping is
active and does not rotate the carried amplitudes. These normalized U and Q
definitions are not SI energy or momentum. Multiple packets of the same mode
superposing need separate interference accounting; this example does not prove
global squared-norm conservation for every possible initialization. Component
vectors themselves rotate, so their fields are not marked linearly conserved.

From the repository root with the project Python environment:

```powershell
$env:PYTHONPATH = (Resolve-Path src).Path
python -m event_universe --init examples/topology/bcc_vectors.json --output artifacts/bcc-vector-run --visualize
python -m pytest tests/test_topology_example.py tests/test_topology_invariants.py tests/test_configured_topology.py -q
```

Use a new output directory per run. The saved input and topology metadata are
authoritative for replay. The headless path is the same command without
`--visualize`; display never changes physical state.
