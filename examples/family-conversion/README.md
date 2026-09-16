# Energy-dependent conversion between particle families

Five configuration-only candidates in which a declared coupling between catalog
families, together with the participants' energies, decides what happens when
records meet. They are declared on the generic
[N-to-M family conversion](../../docs/LOCAL_CONVERSIONS.md#n-to-m-family-conversion)
(`participants` -> `outputs`, one to six each); no physical name in engine code.
Every rule is a supplied discrete kinematics. Exact accounting of the declared
totals is a software correctness result, not evidence of quantum electrodynamics.

| Part | Selection |
| --- | --- |
| Units | Energy in keV, momentum in keV/c with one integer unit per keV/c (a photon has `energy == |momentum|`), charge in thirds of the positive elementary charge |
| Families | `electron`, `positron`, `photon`, with charge and rest energy derived from the [catalog](../known-entities/catalog.json) by the reference-unit adapter (`encode_components`, mass to the nearest keV/c2 with an explicit error budget, identified with keV through c = 1); [bindings.json](bindings.json) records the entity ids, encodings and errors. All three own the same layout `energy`, `momentum`, `charge`; the photon's zero charge is a stored value. Rest energy 511 keV is a declared parameter of each coupling, not a stored field, because the runner's accounting treats every field total as balanced |
| Catalog families | Each rule is bound in `bindings.json` to a catalog `interaction_families` id and, where the catalog lists it, a representative channel: `pair_creation_annihilation` for annihilation (`electron_positron_two_photon_annihilation`), pair production (`two_photon_pair_creation`) and the three-photon candidate (no catalog channel); `electromagnetic_scattering` (`compton_scattering`) for the Compton-like exchange |
| Family checks | Electron and positron: `energy >= 511`; muon (spectator family of one test): `energy >= 105658`; photons: `energy + 1 > |momentum|` (local `checks`, validated on every proposal) |
| Transport | One Link per tick along the reduced lattice direction of the momentum (`rational_direction`), so an axis-aligned momentum has unit port weights and a zero cyclic routing phase; a zero momentum holds. This is a declared transport rule, not the physical speed `|p| / E` |
| Guards | Each rule's `when` reads only the frozen inputs (`participant: i`): axis alignment, head-on geometry, rest condition and energy thresholds |
| Invariants | Per-record readouts `energy`, `momentum`, `charge` summed over all inputs and all outputs; the same fields are declared `conserved`, so the engine also compares their sums without a declaration |
| Audit | The optional [local conservation audit](../../docs/LOCAL_CONSERVATION.md) with energy and momentum read from the records |

## The five supplied laws

**Annihilation** `family-conversion-annihilation-v1`: electron + positron ->
photon + photon, no threshold. With `E` the total energy, `P` the total momentum
and `u` the unit lattice vector along `p_electron - p_positron` (+X when both
are at rest), photon a carries `E_a = whole((E + P.u) / 2)` along `+u` and photon
b carries `E_b = E - E_a`, `p_b = P - p_a`. `whole` truncates toward zero, so
`E_a = |p_a|` exactly. When `E + P.u` is odd, the indivisible keV stays as
energy of photon b, whose energy then exceeds `|p_b|` by one unit: the remainder
is owned, never dropped. The guard requires both momenta on one common axis.

**Pair production** `family-conversion-pair-production-v1`: photon + photon ->
electron + positron only when the total energy is at least 1022 keV. The guard
also requires head-on photons on one axis, each on shell, and
`E_1 * E_2 >= 511^2`, the invariant-mass condition for head-on photons (equal to
the total-energy threshold when the energies are equal). The pair shares the
totals equally, `E_e = floor(E / 2)`, `p_e = whole(P / 2)`, and the positron owns
any odd unit. The pair is exactly on shell at threshold; above it the excess is
lepton energy at rest in the pair frame, where a physical pair would carry
`|p| = sqrt(E_e^2 - m^2)`. Physical pair production also happens on a nucleus as
one photon to two leptons in a field; the lattice candidate uses the two-photon
channel because the engine's conversion is two-to-two. Below the threshold the
guard is zero and the photons cross the shared Node without reacting.

**Compton-like exchange** `family-conversion-compton-v1`: photon + electron at
rest -> photon' + electron', same families out, so it is an energy-dependent
exchange rather than a family change and needs no `output_types`. The scattered
energy is `E' = floor(E m / (m + E (1 - cos theta)))` with `m` read as the resting
target's energy and `cos theta` taken from the lattice cosine table: relative to
the incoming direction the six ports have exact cosines +1 (forward), 0 (four
transverse directions) and -1 (backward); the fixture selects the transverse row,
the right-hand cyclic successor of the incoming axis (+X -> +Y). The photon
leaves with `p' = E'` along that direction; the electron owns the division
remainder as recoil energy, `E_e' = E + m - E'`, `p_e' = p - p'`. The meeting is
one joint transaction at the Node where both records are resident in the same
tick; there is no Node-owned intermediate hold, so a moving electron can never
strand quanta. Energy dependence at `cos theta = 0`: 100 -> 83, 511 -> 255,
1022 -> 340, 10,000,000 -> 510 keV (the transverse Compton edge approaches `m`).

**Three-photon annihilation** `family-conversion-three-photon-v1` (2 -> 3, the
M > N case): electron + positron with net momentum `P` -> photon c along `P`
with `E_c = |P|`, `p_c = P`, plus a back-to-back transverse pair along `v`, the
right-hand successor of the axis: `E_t = floor((E - |P|) / 2)`, `p_a = +v E_t`,
`p_b = -v E_t`, `E_b = E_t`, and photon a owns any odd unit as energy above
`|p_a|`. Three distinct Ports. The guard requires momenta on one axis, `|P| > 0`
and `E - |P| >= 2`: three axis-aligned photons with zero total momentum always
share a Port on the cubic lattice, so the symmetric head-on pair is left to the
two-photon rule. Physical three-photon annihilation has a continuous spectrum;
this is a supplied lattice kinematics.

**Four-body joint conversion** `family-conversion-four-body-v1` (4 -> 4):
electron + positron + photon + photon, four rays arriving through four different
Ports in the same tick, -> four photons in one joint transaction. The guard
requires the leptons to cancel each other's momentum and the photons theirs,
both pairs on perpendicular lattice axes `u` (leptons) and `w` (photons), so the
total momentum is zero. The four energies pool into `Q`; `H = floor(Q / 2)`,
`E_x = floor(H / 2)`, `E_y = H - E_x`; photons leave along `+u` and `-u` with
`E_x` and along `+w` and `-w` with `E_y`; the photon on `+u` owns the odd unit
`Q - 2H` as energy above `|p|`. Every output depends on all four inputs, so the
rule is not a product of two 2 -> 2 rules. The fixture also declares the 2 -> 2
annihilation after it as the fallback for fewer than four rays. The catalog has
no four-body channel; this is a supplied joint kinematics.

## Fixtures and independent expectations

[expectations.json](expectations.json) was written before the first run. All
fixtures use an open 17 x 7 x 7 world, seeds at x = 2 and x = 14 on the line
y = z = 3, and one Link per tick, so the records meet at (8, 3, 3) at tick 6 and
converted moving outputs are `sent` at tick 6 with arrival at tick 7.

| Fixture | Inputs | Recorded at tick 6 | Afterwards |
| --- | --- | --- | --- |
| [annihilation.json](annihilation.json) | e- E 1825, p (+1752, 0, 0); e+ E 1825, p (-1752, 0, 0); both exactly on shell (1825^2 - 1752^2 = 511^2) | photon 1825 keV along +X and photon 1825 keV along -X, charge 0 | both escape the open boundary at tick 15; escaped energy 3650, momentum 0, charge 0 |
| [pair-production.json](pair-production.json) | photons 511 + 511 head-on: exactly the threshold | electron (511, 0, -3) and positron (511, 0, +3) at rest | the pair stays at (8, 3, 3); 12 `sent` events in total, all photons before the meeting |
| [pair-production-control.json](pair-production-control.json) | photons 500 + 500 head-on: total 1000 | no conversion; the photons continue | both escape at tick 15; escaped energy 1000; only photon records ever exist |
| [compton.json](compton.json) | photon 511 along +X; electron at rest at (8, 3, 3) | photon' 255 keV along +Y; electron' E 767, p (511, -255, 0) | photon' escapes at tick 10; the electron follows the cyclic router (511 hops +X first) and escapes at tick 15; escaped energy 1022, momentum (511, 0, 0), charge -3 |
| [three-photon.json](three-photon.json) | e- E 1825, p (+1752, 0, 0) from x = 2; e+ at rest at (8, 3, 3) | photons 1752 keV along +X, 292 keV along +Y and 292 keV along -Y (Ports 0, 2, 3) | transverse pair escapes at tick 10, forward photon at tick 15; escaped energy 2336, momentum (1752, 0, 0), charge 0 |
| [three-photon-capacity-control.json](three-photon-capacity-control.json) | as above with `slots_per_node` 2 | the third photon has no free slot: the cycle fails before commit with `conversion outputs exceed the free resident slots` | run status `failed`; electron and positron remain resident at (8, 3, 3) with unchanged values, no pending plan |
| [three-photon-port-control.json](three-photon-port-control.json) | the same inputs under the collinear variant `family-conversion-three-photon-collinear-v1`, whose kinematics send two forward photons (1022 and 1022) on +X and one (292) on -X | two products would use +X: the cycle fails before commit with `conversion departures must use distinct Ports` | run status `failed`; electron and positron remain resident, unchanged. A spectator photon leaving on a product's Port in the same tick does not fail the cycle (tested): only products are vetoed |
| [four-body.json](four-body.json) | on 17 x 13 x 7: e- (1825, +1752) from (2, 6, 3), e+ (1825, -1752) from (14, 6, 3), photons (300, +Y) from (8, 0, 3) and (300, -Y) from (8, 12, 3); all four arrive at (8, 6, 3) at tick 6 through Ports 0..3 | Q = 4250: photons 1062 along +X and -X, 1063 along +Y and -Y (Ports 0, 1, 2, 3) | Y photons escape at tick 13, X photons at tick 15; escaped energy 4250, momentum 0, charge 0 |
| [four-body-three-arrive-control.json](four-body-three-arrive-control.json) | as above without the -Y photon | the 4 -> 4 rule has no fourth role and stays silent; the declared 2 -> 2 annihilation gives photons 1825 along +X and -X while the +Y photon continues | escapes at ticks 13, 15, 15; escaped energy 3950, momentum (0, 300, 0) |
| [four-body-port-control.json](four-body-port-control.json) | the same four rays under the collinear variant `family-conversion-four-body-collinear-v1`, whose kinematics send 1062 and 1063 on +X and 1062 and 1063 on -X | two products per Port: the cycle fails before commit with `conversion departures must use distinct Ports` | run status `failed`; the four records remain resident, unchanged. A catalog muon spectator (E 105658 keV, p (-100, 0, 0)) leaving on -X beside a product keeps ordinary transport (tested) |

Totals plus escaped quantity equal the initial totals at every tick and the
local audit passes in every run. The runner's `conserved_at_every_completed_tick`
flag compares world totals with the initial totals without escaped quantity, so
it is true until the first escape and false afterwards in any open-boundary run
(`examples/open_world.json` shows the same); `accounting_balanced_at_every_completed_tick`,
which includes escapes, is true throughout. The conversion cycle at tick 6 has
`ready_tick == 6`: the rational-projection tariff (65536 `evaluate` charges per
rational node, about 11 million for annihilation) stays below `normal_budget`
and adds no delay.

```sh
python examples/family-conversion/build.py --write
python -m event_universe.configuration_validation examples/family-conversion/annihilation.json --json
python -m event_universe --init examples/family-conversion/annihilation.json --output artifacts/family-conversion/annihilation
python examples/family-conversion/build.py --scale annihilation --pairs 16 --energy 10000000 --size 48 --ticks 64 --output artifacts/family-scale
```

## Scale: larger board, larger energies

`build.py --scale` places distinct head-on pairs on separate (y, z) lines with
energies stepping up to the requested maximum. Measured with the canonical
runner (host wall time from `run.json`, Focus enabled, one worker):

| Law | Board | Pairs | Largest energy | Ticks | Seconds per tick | Result |
| --- | --- | --- | --- | --- | --- | --- |
| annihilation | 48^3 | 16 | 10 GeV (10,000,000 keV) | 72 | 0.104 | 16 conversions at tick 21, 32 photons up to 10 GeV, all escaped by tick 46, audit 1,561,592 Node events |
| pair production | 48^3 | 16 | 5 GeV + 5 GeV per pair | 72 | 0.070 | 16 pairs at tick 21, 16 Nodes stay awake with resting pairs |
| Compton | 48^3 | 16 | 10 GeV photons | 72 | 0.096 | 16 exchanges at tick 21, recoil electrons up to 10,000,001 keV, scattered photons 510 keV, all escaped by tick 66 |
| three-photon (2 -> 3) | 48^3 | 16 | 10 GeV | 72 | 0.108 | 16 conversions at tick 21, 48 photons on three Ports each, all escaped by tick 66, audit 1,611,557 Node events |
| four-body (4 -> 4) | 48^3 | 16 quadruples (64 rays) | 10 GeV | 72 | 0.424 | 16 joint conversions at tick 21, 64 photons on four distinct Ports per Node, all escaped by tick 46, exact totals of 212,500,000 keV, audit 6,173,680 Node events |
| annihilation | 64^3 | 64 | 10 GeV | 80 | 2.92 | 64 conversions, 128 photons escaped by tick 62, exact totals of 650,000,000 keV, audit 45,821,920 Node events |

Every accounting flag except the open-boundary `conserved` flag discussed above
is true, and the audit passes. Wall time is host work, and almost all of it is
the passive conservation audit visiting Node events, not the local physics.
Stepping the same annihilation worlds in-process for 24 ticks, with and without
the `conservation` member:

| Board | Pairs | Seconds per tick with audit | Seconds per tick without audit |
| --- | --- | --- | --- |
| 48^3 | 16 | 0.122 | 0.004 |
| 48^3 | 64 | not measured | 0.016 |
| 64^3 | 16 | not measured | 0.003 |
| 64^3 | 64 | 2.13 | 0.012 |

The first thing that breaks with scale is therefore this host diagnostic's
cost, which grows with the board volume and the run length; the physics cost
grows only with the number of occupied Nodes, as Focus intends. The integer bound is the stored component bound
`MAX_VALUE = 1,073,741,823` (about 1.07 TeV per record in keV units), not the
64-bit working register: annihilation and pair production run at exactly
`MAX_VALUE` per record, and the first thing that breaks beyond it is a seed
component of `MAX_VALUE + 1`, rejected at initialization. Compton's bound is
one unit lower, `MAX_VALUE - 1` for the photon, because the recoil electron
carries `E + 1` keV at the transverse edge; at `MAX_VALUE` the proposal is
rejected explicitly with no partial commit. Sixteen pairs at `MAX_VALUE` keep
exact totals of 34,359,738,336 keV. Choosing keV as the unit therefore covers
the requested 10 GeV with a factor of about 100 in reserve.

## Limitations

- The conversion contract rejects any carried fractional routing state, so
  converting records must move at one Link per tick with unit port weights. A
  physical pace `|p| / E` (fractional `rate`) would carry credit state and be
  rejected at the meeting; the smallest contract change that would allow it is
  an explicit rule for who owns the fractional credit at conversion.
- Above the pair threshold the leptons are at rest in the pair frame; the mass
  shell is a supplied property, not enforced. Integer keV kinematics cannot be
  on shell in general, and the remainder ownership above states where each
  indivisible unit goes.
- The pair guard `E_1 * E_2 >= 511^2` is the physical invariant-mass condition
  for head-on photons; oblique geometries are not lattice directions and are
  not admitted. An asymmetric pair whose two leptons would leave on the same
  Port in one tick (49 + 5329 keV, exactly on shell) is rejected before commit
  by the one-departure-per-Port rule; co-moving products need a later cycle or
  a retained record, which this candidate does not supply.
- The recoil electron's zigzag follows the cyclic router's block order, not an
  interleaved ratio; balanced routing would carry counters the conversion
  contract rejects.
- Lepton number is not a declared invariant: it is conserved here only as a
  consequence of the explicit output families and of charge; a follow-up may
  add a conserved `lepton` field to the shared layout.
- An N-to-M rule may re-fire on its own products in a later cycle when they stay
  co-resident and its guard admits them; here every product either leaves at once
  or is a family the rule does not select.
- The candidates carry photons as whole records. The related
  [radiation-scattering](../radiation-scattering/README.md) candidate uses field
  streams with a Node-owned hold; its two-phase meeting can strand held quanta
  when the carrier moves between the phases. The fixtures here avoid that by
  construction. Note also that outward-field `decay` exists only in schema 2,
  and schema 2 rejects `field_rules`, so a charged ray's halo cannot attenuate
  in a run that also uses field rules; these fixtures use no spatial fields and
  did not hit that limit.

Tests: [test_family_conversion.py](../../tests/test_family_conversion.py).
