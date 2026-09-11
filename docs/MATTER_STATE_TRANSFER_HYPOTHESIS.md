# Matter-state transfer and self-response

Status: exact state-transfer and local arithmetic checks pass. A replacement
long-range interaction law is unverified; the existing self-response failures
are not resolved by these checks. Reviewed production: `d7fcc0e`.

The current [Highlights](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit)
sections 3.1, 3.3.2, 3.3.3 and 3.5 require separate moving mass records, exact
vector components, unique ownership and explicit interaction balances.

## Hypothesis and condition

The user's proposal is to receive the particle's own mass and momentum as its
transported state, instead of interpreting that reception as an extra force.
Transferring a record from source to link to destination preserves its velocity
if mass, momentum, scales and residuals remain unchanged and are counted once.
The source must relinquish the transferred inventory.

If a local record `(M, P)` actually merges with a payload `(m, q)`, its resulting
velocity is `(P + q) / (M + m)`. It retains `P / M` precisely when
`M*q = m*P`, component by component. Unchanged velocity alone does not establish
mass or momentum conservation: adding a duplicate doubles both and keeps the ratio.

When a moving record is split, mass and momentum portions must be coupled so each
portion has the original velocity. Separate conservative integer divisions can
change each portion's velocity despite conserving the global totals. Exact
integer-ratio momentum descriptors or retention of indivisible joint bundles
can represent this; an arbitrary rounding rule cannot silently replace it.

| Check | Exact result | Meaning |
| --- | --- | --- |
| Encode and restore `m=7, p=(14,-7,21)` | Components unchanged | Velocity `(2,-1,3)` is restored without impulse |
| Joint six-way split of that record | Six `m=1, p=(2,-1,3)` portions and one retained identical portion | Mass, momentum and each portion's velocity are preserved |
| Independently split `m=8, px=4` six ways | Each sent portion has `m=1, px=0`; retained `m=2, px=4` | Total balances pass, but outgoing speed becomes zero and retained speed becomes two instead of one-half |
| Add a copy of `m=2, px=6` | `m=4, px=12`, same speed three | Velocity preservation hides duplicate inventory |
| Split one integer mass unit equally six ways | Nothing sent; one unit retained | An indivisible unit cannot be emitted on all six faces at once |
| Existing elastic contact: masses `2,1`, momenta `6,-1` | Outgoing momenta `2/3,13/3`; velocities `1/3,13/3` | A separately defined local interaction preserves total momentum five and kinetic energy |

These are pure component and arithmetic checks, not a new world simulation or a
new physical law. In particular, splitting a localized particle into multiple
mass portions would need its own spatial and record-identity definition.

## Relationship to the current implementation

`MatterTransport` and `Engine._receive_matter` already transfer ownership of the
particle record and change its location without applying an arrival impulse.
The existing free-motion and ownership experiments verify this scheduling.

`GenericEngine._field_step` separately supplies occupancy counts to field
definitions. Those definitions create scalar or octant signal amounts; they do
not debit or transport the particle's mass and momentum. Descriptive information
about an emitter's mass is not additional transported matter. The force adapter
still responds to field-face imbalance, including an emitter's own co-arrival.

An actual replacement requires typed mass/momentum payloads, exact shared vector
storage and a receive operation that restores the appropriate bounded record.
It must define which outward messages transfer matter and which carry other field
quantities. A separate local interaction rule must explain changes caused by
another record or field. Averaging records with different velocities cannot erase
them in free motion, and overwriting another record is not state restoration.

This supports the proposal's state-transfer principle. It does not yet establish
gravity or cancellation of the existing seven self-response failures. See the
[earlier self-response counterexamples](SELF_RESPONSE_BLOCKER.md).

## Reproduce the pure checks

Run from the repository root. No floating-point arithmetic or world is used.

```sh
PYTHONPATH=src python - <<'PY'
from event_universe.fields.encoding import encode_values, decode_values
from event_universe.fields.conservation import split_ratio
from event_universe.dynamics.collision import CollisionBody, elastic_backscatter

state = (7, 14, -7, 21)
encoded = encode_values(state)
assert all(n > 0 for n in encoded)
assert decode_values(encoded) == state

parts, retained = split_ratio(7, (1,) * 6)
velocity = (2, -1, 3)
momenta = tuple(tuple(m * v for v in velocity) for m in parts)
rest_p = tuple(retained * v for v in velocity)
assert parts == (1,) * 6 and retained == 1
assert sum(parts) + retained == 7
assert tuple(sum(p[a] for p in momenta) + rest_p[a] for a in range(3)) == state[1:]
assert all(tuple(m * v for v in velocity) == p for m, p in zip(parts, momenta))

mass_parts, mass_rest = split_ratio(8, (1,) * 6)
p_parts, p_rest = split_ratio(4, (1,) * 6)
assert (mass_parts, mass_rest) == ((1,) * 6, 2)
assert (p_parts, p_rest) == ((0,) * 6, 4)
assert sum(mass_parts) + mass_rest == 8 and sum(p_parts) + p_rest == 4
assert p_parts[0] * 8 != mass_parts[0] * 4
assert 12 * 2 == 6 * 4  # Duplicating m=2,p=6 preserves velocity, not inventory.
assert split_ratio(1, (1,) * 6) == ((0,) * 6, 1)

result = elastic_backscatter(CollisionBody((6, 0, 0), 2), CollisionBody((-1, 0, 0), 1))
assert result.first == CollisionBody((2, 0, 0), 2, 3)
assert result.second == CollisionBody((13, 0, 0), 1, 3)
assert 2 + 13 == 5 * 3  # Total momentum five in denominator-three units.
assert 4 + 2 * 169 == 19 * 18  # Twice kinetic energy in denominator-eighteen units.
print('Six hypothesis checks passed; long-range interaction remains undefined.')
PY
```
