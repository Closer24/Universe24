# Detector-owned sampling

The canonical contract is `detector-only-v1`, the only sampling profile. Only a
Node whose Detector bit is set may draw ([Highlights](HIGHLIGHTS.md) 3.19):
creation, propagation, ordinary contacts, phase changes, field emission,
strong/weak coupling and absorption do not authorize a draw. An entity name,
diagnostic observer, seed or supplied ticket does not establish a Detector.

This supersedes autonomous sampling as a universal interpretation of
[postulate 22](../POSTULATES.md#22-historical-autonomous-sampling-candidates).
The earlier local-lottery and bond laws and the `historical-autonomous-v1`
research profile that selected them were deleted on 2026-09-17 (issue #164,
bucket B.5), after the native-contact laws and the shared quantum resource
(buckets B.1 and B.2). Their dated measurements stay in
[validation](VALIDATION.md) and do not establish compliance with this contract.

## Configuration and admission

`sampling_profile` is immutable initialization metadata with one accepted
value, `detector-only-v1` (the default). Any other value, including
`historical-autonomous-v1`, fails admission before a world is constructed or a
ticket is consumed. The keys of the deleted samplers (`"capture": "lottery"`,
`capture_seed`, `capture_salt`, `bond`, `bond_field`, `bond_setting`) are
unknown to the parser, and a typed `SpatialFieldDefinition` whose `capture` is
`"lottery"` is rejected by `validate_spatial_sampling` at `InitialState` and
`SpatialLaw` construction. The deterministic `share` and `threshold` captures
remain and draw nothing. Preflight and run metadata record the profile. No
model ID, entity label or observation callback changes admission.

Validate both the parsed immutable initial state and the responsible local law;
direct typed construction must not bypass the same boundary. The bounded ticket
sequence (`TICKET_MODULUS`, `next_ticket`, `ticket_draw` and the phase tables
in `core/spatial_state.py`) stays as the local draw a marked Node will own; no
ordinary owner calls it. The native program admission, resolver construction
and resolver ticket gates were deleted on 2026-09-17 with the integration
layer, and the bond-registry gate with the registry itself.

No physical probability, transport, conserved quantity, ownership layout, phase
rule or timing law is changed by this admission boundary. The full external
Detector exchange remains unimplemented.

## External exchange implementation boundary

The adopted exchange is the Detector of [Highlights](HIGHLIGHTS.md) sections
3.19, 3.20 and 5.4: a marked Node draws 1 or 0 for each arriving transfer,
`1 = PASS` (ordinary behavior for that arrival) and `0 = RETURN` (the same
wave ray reversed on its line, unchanged, walking back the number of steps it
has made since its event and performing the inverse split at its birth event).
A repeated committed decision reuses its immutable result without another
draw, output or inventory charge. The historical quantum instrument that
earlier revisions of this section compared against was deleted on 2026-09-17
with the shared quantum resource.

The following definitions are still open before an implementation:

| Owner | Missing definition | Acceptance after closure |
| --- | --- | --- |
| Physics | Action-bit distribution and allowed dependence on causal settings/input; the distribution is not assumed 50/50 | Predetermined action counts and probabilities; no implicit fair coin or deterministic replacement |
| Physics and architecture | Repeat and simultaneous encounters (up to six arrivals in one interval, one independent draw each) and the mark's ticket seed | Symmetric Detector identities, declared retries/conflicts and unchanged returned content |
| Architecture, then field developer | The carried step count, the inverse split at the birth event and the cancellation arithmetic where the returning ray meets the delayed share | One-Link-at-a-time return; no remote/global erase; complete retained/transferred amounts and remainders |
| Architecture, then engine developer | Detector/model clock mapping, bounded transaction capacity and output-clock composition | Fixed neighbor transit H plus defined output delay, atomic once-only publication and rejected overflow |

An opposite-going ray alone does not define cancellation. An ordinary absorber
cannot be renamed a Detector to fill these gaps. A minimal PASS/RETURN stub
would leave the required behavior undefined, so it is not published as
physical support.


## Required evidence

1. The lottery capture, the bond-registry and claim-gather keys and any
   sampling profile other than `detector-only-v1` are rejected before any
   draw; adding an observer or naming an absorber Detector cannot authorize
   them.
2. Direct immutable-state/local-law construction rejects the same samplers.
3. Deterministic ordinary controls consume zero tickets and preserve their
   exact traces. Every actual simulation run retains its canonical HTML.
4. The dated results of the deleted samplers stay in the validation log under
   their historical profile; they are not canonical acceptance results.
5. PASS/RETURN, causal branch cancellation, real Detector authorization
   and output-clock composition remain separately blocked until their contracts
   and implementation meet the table above.
