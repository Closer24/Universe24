# Directional radiation quanta scattered by a charge

`directional-quanta-charge-scattering-v1` is a configuration-only candidate in
which the wave itself pays for the momentum a charged carrier receives. It uses
the existing [local field rules](../../docs/LOCAL_FIELD_RULES.md) and
[joint field/carrier transactions](../../docs/LOCAL_FIELD_RULES.md#joint-fieldcarrier-transactions);
no engine change and no physical name in engine code.

| Part | Selection |
| --- | --- |
| Wave | Six scalar local fields `rad_px` .. `rad_mz`, one integer quantum stream per cardinal travel direction; each quantum carries one momentum unit along its direction |
| Carrier | `scatterer` with configured `charge`, held in place; emits a `presence` marker equal to charge squared each interval |
| Field phase | `hold_scattered_quanta` moves `min(rad_px, presence * 2)` into `held_px`; `stream_quanta` sends every stream one link along its port; `clear_presence` resets the marker |
| Carrier phase | `scatter_held_quanta` turns `held_px` into `rad_mx` and adds twice that amount along +X to the carrier momentum |
| Invariants | `quanta` (all streams, held stock and outgoing payloads) and `total_momentum` (carrier momentum plus the direction-weighted quanta), checked on every rule |

With six pulses of ten quanta passing a charge of either sign, two quanta per
interval are held, the forward stream continues with eight, a back stream of
two per interval appears one interval later, and the carrier gains four
momentum units per scattered batch: 24 after six batches. Quanta stay at 60 and
carrier-plus-wave momentum stays at 60 until streams leave the open boundary.
A neutral carrier changes nothing; charge 2 holds eight of ten and gains 96.

```powershell
python examples/radiation-scattering/build.py --charge -1 --output artifacts/radiation-scattering
```

Carrier momentum is declared nonconserved on its own because it is conserved
only jointly with the radiation; the named invariant enforces that exactly per
transaction. The scattering fraction `presence * 2` is a supplied selection
rule, not a derived cross section; the transverse impulse of a pulse remains
the separate [local Lorentz example](../local_lorentz_field.json). Tests:
[test_radiation_scattering.py](../../tests/test_radiation_scattering.py).
