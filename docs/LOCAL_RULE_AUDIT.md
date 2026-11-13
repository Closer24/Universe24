# One local rule: capacity, clocks and transport

This audit uses the unchanged capacity-scatter48 tensor at main revision
04269704b2856f6e281b538a312e7880bc76ff27. It tests a proposed extension; it does
not replace the active law or establish a gravity model.

The unifying operational form is a local reversible collision followed by
counted internal channel turning, F=O E. The same Rule3 polynomial executes
both. Node occupancy Q is bounded by 48, and changes only by signed neighbor
currents. Internal cycles are possible clock candidates, not calibrated proper
clocks. Edge holding and transport are measurable; geometric length must not
be equated to either before a common clock calibration is established.

## Exhaustive obstruction for the existing edge quartet

An edge quartet has two bits at each endpoint. Consider every Boolean gate
that preserves total occupation, is bijective, and commutes with cyclic
relabeling of the quartet. Exhaustive enumeration gives 1,4,8,4,1 gates in the
five occupation sectors: 128 complete gates. Every gate preserves
q_left^2+q_right^2 on each input word.

The reason is visible at occupation two. Alternating words (1010,0101) have
cyclic orbit length two and endpoint loads 2|0. Adjacent occupied words have
orbit length four and endpoint loads 1|1. An equivariant bijection cannot map
between these orbits. The other occupation sectors already have fixed endpoint
concentration. Thus no gate in this precise class can implement instantaneous
2|0 to 1|1 equalization. This is NOT a no-go theorem for all 48-channel laws,
clock-conditioned routing, or finite-time spreading after onsite turning.

A greedy rule that maps 1010 to 1100 and leaves 1100 unchanged has two inputs
for the same output. It loses reversibility. A reversible replacement must
preserve the routing history in counted internal state, and also demonstrate
cubic degree, face locality and exact 2O covariance. Merely adding an external
load-balancing controller would violate the state budget.

The classification can be reproduced independently:

```python
from itertools import product, permutations
words = list(product((0, 1), repeat=4))
rot = lambda w: w[-1:] + w[:-1]
s2 = lambda w: (w[0]+w[2])**2 + (w[1]+w[3])**2
counts = []
for weight in range(5):
    domain = [w for w in words if sum(w) == weight]
    count = 0
    for outputs in permutations(domain):
        gate = dict(zip(domain, outputs))
        if all(gate[rot(w)] == rot(gate[w]) for w in domain):
            count += 1
            assert all(s2(gate[w]) == s2(w) for w in domain)
    counts.append(count)
assert counts == [1, 4, 8, 4, 1]
```

## Actual Engine runs

Two size-7 radius-1 preparations were evolved for 24 updates. Both preserved
positive retained values, exact total occupancy, node continuity at every
transition and exact rewind. These have DIFFERENT totals and are not an
apples-to-apples performance comparison.

| Preparation | Q | Occupied nodes t=0 | t=5 | t=12 | t=24 |
| --- | --- | --- | --- | --- | --- |
| Symmetric core | 336 | 7 | 116 | 32 | 44 |
| Core plus declared asymmetric halo | 366 | 25 | 137 | 32 | 61 |

The symmetric run activated no three-occupation blocks. Halo run blocked
quartet counts at the same times were 30,0,6,0. Spreading and reconcentration
both occur; neither establishes a monotonic optimization principle.

A second matched-pair test added one occupied channel at the cube center in
vacuum and in a Bernoulli-1/4 background (NumPy default_rng seed 20261113).
For six updates, the total occupation difference stayed one and every
state difference stayed inside the one-edge-per-update causal cone from the
COMPLETE initial (a,b,r) difference. Inverse-history preparation initially
changes two nodes, which are both included as cone origins. These tests
establish causal perturbation transport in those preparations, not wave
polarization, Maxwell equations or gravitational waves.

## What remains missing

Numerical encoding does not identify a physical species. Moving disturbance,
stable localized composite and optically weak but gravitating composite are
separate operational tests. The present audit identifies none as established
light, matter or dark matter. Likewise a distribution score is not a physical
energy or a proper clock rate.

A richer candidate would let the counted internal phase participate in
neighbor-sensitive routing, retaining information when load spreads and
allowing later reconcentration. That is a design direction, not a completed
polynomial construction. Before promoting it, require the same Engine
contracts, independent timing/dispersion tests and a conserved stress-energy
account with common clock/metric calibration. See PHYSICS.md and
LOAD_DISTRIBUTION.md for the remaining Einstein criteria and primary sources.

Backpressure provides a congestion-gradient comparison:
https://ee.usc.edu/stochastic-nets/docs/backpressure.pdf
Jacobson's derivation uses horizon entropy and energy-flux assumptions, not
queue balancing alone: https://arxiv.org/abs/gr-qc/9504004
