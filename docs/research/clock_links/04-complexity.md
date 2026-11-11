# Phase-link structure and the unchanged growth gate

The preregistered protocol is [issue #45 comment 6804437312](https://github.com/Closer24/Universe24/issues/45#issuecomment-6804437312).
The implementation is `validation/clock_links/complexity_audit.py`; it observes
saved complete states and canonical arithmetic records, adds no state and
cannot control evolution. The carrier ports are the existing `field.phi` and
`field.chi`, with the preparation's common-sign convention. Their phase is not
yet an operational proper clock or a local-gauge-invariant measurement.

## A precise finite proxy

Write each nonzero carrier as an integer pair `v_x=(phi_x,chi_x)`. For every
directed face edge define

```text
L_xy = (sign(phi_x phi_y + chi_x chi_y),
        sign(phi_x chi_y - chi_x phi_y)).
```

A zero endpoint receives a distinct inactive symbol. A site's motif is its
ordered six-face list in the lattice's `+x,-x,+y,-y,+z,-z` convention. At each
complete saved checkpoint, compare with the preceding complete checkpoint.
Count the distinct nonuniform motifs that remain identical at the same sites,
occur at at least two such sites, and contain no inactive face. This count is
the **current persistent organization proxy**. It is not accumulated novelty.

The definition is unchanged by independent positive integer amplitude scaling
at each node, or by multiplication of every carrier by the same nonzero complex
integer: both dot and cross products acquire only a positive scale. Relabelling
nodes and their adjacency together only permutes the motif list. The statistic
contains no elapsed-time input, numeric magnitude, message count or externally
selected threshold. Negative endpoint rescaling changes relative phase, as it
should; independent local complex rotations are not a symmetry of this reader.

## Predeclared apparatus episodes

For each complete runtime step, count all canonical records from the four
appended apparatus channels. Include empty windows. An arithmetic episode is
a strict interior local maximum of that count, at least one event. Endpoints
and plateaus do not qualify. This does **not** identify a physical cosmological
burst, collapse or detection.

The finite growth gate requires at least four such episodes and a strictly
increasing current organization proxy at every consecutive episode. Fewer
episodes means `blocked`, never success. A repeated pattern at a later episode
cannot be credited simply because more time or larger amplitudes elapsed.
Separate causal selection requires retained history to affect future carrier
phase-link structure with a disconnected control. The four-channel intensity
recorder has no apparatus-to-carrier terms; it therefore cannot pass that
selection gate by construction.

## Falsifying controls

Eight focused tests pass, including exact large-integer transformations and
malformed-input rejection. On a 7-cube:

| Control | Result |
| --- | --- |
| Nodewise positive amplitude scaling | Identical complete phase-link motifs |
| Common nonzero complex multiplication | Identical complete phase-link motifs |
| Node labels and adjacency permuted together | Identical motif multiset |
| Zero source and uniform phase | Organization proxy zero |
| Four periodic arithmetic peaks with common-phase rotation | Score `3,3,3,3`; strict growth fails |
| Fresh random phases at every checkpoint, seeds 101/509/2027 | All eight checkpoint scores zero |
| Frozen random phases, same three seeds | Scores **13,15,5** |

The last control is an explicit limitation: accidental repeated motifs in a
frozen random field can score above the ordered stripe's three motifs. This
proxy measures persistent phase-sign structure, not a universal distinction
between meaningful organization and random information. It was not retuned
after observing this counterexample. A physical complexity-selection proposal
must justify the selected statistic and show causal predictive utility, not
merely increase this observer's count.

## Actual 48-channel trace

The saved three-step run uses tensor
`094bb4edbe243e4f7654073e64688ebc7b56d951724a21a0f3af1526153df611`
and bundle
`f15c3c342d4a9ee807640fcd6357996a1c878cb43e448f8371e3a6b6b662fad9`.
The organization proxy is `0,0,0,0` from seed through all three updates.
The four detector channels produce complete step counts `100,107,107`.
There are no strict interior maxima, so the four-episode growth gate is
**blocked**. Maximum retained bit sizes are `3,6,12,25` including the seed.
Complete saved replay passes. No long-horizon physical stability claim is made.

The immutable tensor has zero apparatus-to-base monomials. This gives an exact
induction: for any apparatus-history preparation with the same original 44
complete channels, all future original channels coincide. Hence the apparatus
cannot select a more complex future carrier structure under this law. The
phase audit's matched histories can change arithmetic-event presence, but not
the carrier or its driving intensity. This distinction is a constructive
boundary for the next model change, not a successful feedback mechanism.

For a fixed board of `N` sites the proxy is at most `floor(N/2)`, because every
counted motif occupies at least two sites. Strict indefinite growth of this
particular observable is impossible even if integer magnitudes are unbounded.
Further claims must specify a finite horizon, an ensemble, or additional
spatial/temporal scales instead of treating this bounded count as unlimited
complexity.

## Reproduction and scope

```bash
python -m unittest universe24.tests.test_clock_link_complexity -v
python -m validation.clock_links.complexity_audit --out runs/clock_links/complexity
python -m validation.clock_links.complexity_audit --run PATH_TO_VERIFIED_48_CHANNEL_RUN --out runs/clock_links/complexity-board
```

Every supplied run is reverified through the existing runtime before it is
read. Evidence includes bundle/tensor/run identity, all checkpoint scores,
complete detector event counts, bit growth and explicit passed/failed/blocked
gates. Original [PR #43](https://github.com/Closer24/Universe24/pull/43) growth
and persistence failures in all 16 cases remain unchanged; this audit does not
rerun or relabel them. Neither Born probabilities, Bell violation, proper time
nor indefinite structural growth follows from these checks.
