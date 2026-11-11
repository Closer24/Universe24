# Tensor, seed and click contract

A reproducible run consists of the exact integer tensor, complete initial
`a,b,r` arrays, the storage graph and the fixed-six engine version. Neither a
picture nor a list of selected event counts specifies the full construction.

## Locality and evolution

Each input polynomial has integer coefficients, at most three factors and
strict target-plus-one-face support. Old-history dependencies must be acyclic.
Every forward update reads one old snapshot and applies
`divmod(2*u+r,6)`, retaining the remainder. No detector or callback changes
that forward evolution.

## Official observations

An official record requires a nonzero quotient and a changed complete local
triple, together with its observation label. Readout labels do not influence
the dynamics. A missing row may mean a zero quotient or an unchanged triple;
therefore it does not generally determine the local update by itself.

A decoder must state the initial information and invariants it uses. The
[prepared geodesic example](PPWAVE_OPERATIONAL_ROUTE.md) supplies a narrow
successful decoder and an explicit failed naive decoder. Distinct complete
states can still produce the same official record stream.

## Reproduce an audit

```bash
python -m universe24.tools.audit_contract --L 4 --steps 120 --out runs/contract
python -m universe24.tools.audit_contract --replay runs/contract
```

Check the completed horizon, full-state hashes, exact inverse, support audit
and exported event stream. The old nonunit-divisor law must be rejected by a
current replay reader rather than silently reinterpreted.

The previous assembly's numerical inventory and replay records are
[historical](archive/pre-fixed-six/docs/CLICK_CONTRACT_AUDIT.md).
Their pass counts and physical limitations must not be reassigned to the new
default. Current checks establish implementation properties, not quantum
collapse, an Einstein spacetime or a maximum-complexity choice law.

## C2 and the event cone

The [joint audit](CLICK_CAUSALITY.md) proves the modular C0/C1/C2 classification,
checks differences in official C2 records against the complete initial causal
footprint, and separates message-driven C2 activity from structural growth.
A repeated C2 label does not itself implement a complexity preference.
