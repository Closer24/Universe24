# Installed 48-channel light component

The current light implementation is **`universe24/light.py` in the installed
main package**. It is not the earlier source-only optical experiment.
`python -m universe24 prepare-light` seals its complete inputs; the existing
`run` and `verify` commands execute and replay the unchanged Rule3 Engine.

```bash
python -m universe24 prepare-light --out runs/light-bundle
python -m universe24 run --bundle runs/light-bundle --steps 6 --out runs/light-main
python -m universe24 verify --run runs/light-main
```

Defaults are L=13, a binomial pulse of order 4 centered at x=4, propagation +x
and electric polarization +y. Use `--axis y --polarization x`, `--sign -1`,
or the size/center/order/amplitude preparation flags for another complete seed.
The same immutable tensor is used in every case. Output directories must be
new. No callback, reference solver or detector changes the evolution.

## Algebra and physical domain

| Item | Implemented contract |
| --- | --- |
| Retained channels | Exactly 48, all with dynamical transport; no idle padding |
| Retained integers per node | 144: all a,b,r values |
| Input | u_g(x)=3[b_g(x−n_g)+b_g(x+n_g)], n_g=R_g e_x |
| Scalar update | Unchanged fixed-six Rule3 |
| Tensor | 96 linear integer monomials; one face per term; no old-a reads |
| Candidate symmetry | Exact `2O-left-regular-cube/1`, passed for the entire polynomial |
| Model role | `universe-candidate`; algebraic acceptance, not full physics |
| Complete preparation | a_g(x)=b_g(x+n_g), arbitrary retained carries in 0…5 |
| Prepared evolution | b_next,g(x)=b_g(x−n_g), r_next=r, for every tick |
| Coordinate metric | Flat −dt²+dx²+dy²+dz²; one edge and time unit per tick |
| Tensor SHA-256 | `a3b4ab5293de5ca5ce143bf86c17bbe908277ea4ad7fdceeaa8bf86d39129be6` |

All 48 channel polynomials obey the action, including the central quaternion
lift. The two physical transverse basis polarizations occur for each signed
cube axis. The proof and non-injective vector readout are documented in
[MODEL.md](../../MODEL.md#native-48-channel-2o-light-streams).

The exact prepared shift has no denominator scale or finite precision horizon.
For the declared single-plane packet, the transverse electric and magnetic
fields translate at exactly unit speed, are orthogonal with equal magnitude,
and conserve their global electromagnetic energy. Every update still saves
all channels, old histories, carries and canonical arithmetic records.

The supported physical domain is **flat, axis-aligned transverse plane waves**.
There are six discrete propagation directions. This does not establish general
arbitrary-direction Maxwell convergence, dynamic Einstein backreaction,
operational proper clocks or quantum photon detection. `--require-physics`
continues to reject a full physical acceptance claim. Clicks remain arithmetic
events and cannot become photon counts merely by naming a channel.

## Verification

Installed-component tests check polynomial symmetry, forward/inverse complete
states, all six directions and both polarizations, the independent scalar
oracle, and main CLI preparation/replay:

```bash
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/new-smoke
python -m universe24 verify --run runs/new-smoke/run
```

The passive observer `validation/light_runtime.py` inspects saved native light
runs. Its `collect` function runs the x/y/z preparations through the same main
runtime. The archived central research collector is not a supported schema-3
execution path. Different gravity and light tensors are not one physical law.

Saved schema-3 evidence is in [`runs/native-light-main-v3`](../../../runs/native-light-main-v3)
and [`runs/native-light-axes-v3`](../../../runs/native-light-axes-v3). The main
13³, six-tick run retains its complete seed, tensor, trace and all 7,098 C0
clicks. Its center advances 5,6,7,8,9,10; twice the plane-field energy remains
23,660. All 117 active tests passed, as did generic replay and prepare/run/verify
from the built wheel without the source-only validation package. Source hashes
and exact check scope are recorded in `integration_checks.json` beside the run.

## Original optical experiment, preserved separately

The earlier 18-channel static optical tensor is a different law, with hash
`256db395ebfd0456d72fb6bd7c65754896f984c3b4724f5462d6ac0dce96b177`, executed against
Engine source `e582960f6c9d2d134d3d6b28c08494e8bfafa86a`.
Its four original scripts are in `original_source/`; its full lossless
plane-compressed states and clicks remain in `runs/light-packet-clicks-v2/`.
Every original byte is preserved. These traces are not evidence for the new
native tensor or the new bundle schema.

| Original background | Target speed | Measured centroid speed | Raw clicks |
| --- | ---: | ---: | ---: |
| q=1 | 1 | 0.928285 | 2,649,256, all C0 |
| q=2 | 2 | 1.893229 | 2,649,256, all C0 |
| q=1→2 | 2 after transition | 1.884710, late fit | 2,649,256, all C0 |

That tensor's finite-grid tails, identical count/location/class maps across
three backgrounds and amplitude/count mismatch remain reported. Padding it
with 30 zeros does not satisfy the specified regular 2O candidate action, so
the native component above uses a new covariant law instead. Its simpler flat
domain does not inherit the old model's variable optical-background response.

[Original Hebrew report](Universe24_light_clicks_report_he.html) ·
[Original animation](Universe24_light_clicks.gif) ·
[Original spacetime figure](Universe24_light_clicks.png)
