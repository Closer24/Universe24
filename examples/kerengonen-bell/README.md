# Bell test on the phased-ray field: a local classical wave against the quantum owner

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1),
`kerengonen-ray-field-v1`; no other engine rule is involved. It runs the
Clauser-Horne-Shimony-Holt form of Bell's test on the classical phased field
with the same four settings the finite quantum owner uses in the
[two-wing Bell experiment](../quantum/bell_chsh.md), and asks whether a local
field of whole quanta with a phase can reach the value 14/5 that the quantum
owner records. It cannot: the field measures 1.40 and the plain field 2, both
inside the bound of 2 that every local model obeys. Every number is a read-only
world audit at host lattice coordinates. No wavelength, constant or species is
identified; the phase steps and the settings are configured integers.

```sh
PYTHONPATH=src python examples/kerengonen-bell/run_experiments.py --output artifacts/kerengonen-bell
```

## Mechanism

A funded source at the centre of a 15 x 7 x 3 open world fires one ray toward
each wing every tick, 1024 quanta per ray, on a 360-step phase circle with one
step of advance per link. Both rays leave with the same phase, the hidden
variable of the run. Three links from the source on each side stands an
analyzer, a record that absorbs the field, and three links below each analyzer
a reference lamp fires across it with the wing's setting as its phase. At the
analyzer Node the source ray and the lamp ray meet after the same number of
links, so their phase difference is the hidden phase minus the setting. The
analyzer takes the coherent share `(1 + cos d) / 2` of each ray, exact on the
field's fixed-point cosine table; the absorbed part of the source ray is the
outcome +1, the part that passes through and leaves the world is -1. Because the
source ray heads along x and the lamp ray along y, the analyzer's momentum
counts the two absorbed rays separately. Nothing travels between the wings: a
lamp's rays leave through the boundary, and the source is the only thing both
wings share.

The settings are the quantum experiment's, read as phases: Alice `a0 = 0` and
`a1 = 90` degrees for Z and X, Bob `b0 = 53` and `b1 = 307` degrees for
`(3Z + 4X) / 5` and `(3Z - 4X) / 5`, whose angle is `arctan(4/3) = 53.13`
degrees. The combination is the quantum report's,
`S = E(a0 b0) + E(a0 b1) + E(a1 b0) - E(a1 b1)`. For one hidden phase the two
wings are independent, so the correlation is the product of the two outcome
expectations, and the reported correlation is its average over the hidden phase.

Three measurements are taken.

- **Share rule.** One world per hidden phase on a five-step grid (72 per
  setting pair, 288 worlds) and 24 ticks each. The outcome expectation of a wing
  is `2 x share - 1`, the table cosine of the phase difference, so every
  correlation is an exact fraction.
- **Lottery rule.** Single quanta, `"capture": "lottery"`: each tick the source
  sends one whole quantum to each wing, and each analyzer takes it or leaves it
  by a local ticket at the coherent rate. One pair per tick, 93 pairs per world
  on a fifteen-step grid of the hidden phase, 2232 pairs per setting; the
  correlation is the mean of the products of the two clicks, +1 and -1, as a
  coincidence counter reports it.
- **Plain field.** The same worlds without the key: every ray is absorbed whole,
  every outcome is +1.

The local model's own prediction, computed independently of the update code
from the cosine table, is `E(a, b) = mean over the hidden phase of cos(phase - a) cos(phase - b)`,
which is `cos(a - b) / 2` up to the table's rounding: one half of the quantum
owner's `cos(a - b)`.

## Observed outcomes on 2026-09-14

Runtime source SHA-256
`ae732df611ba461d40f355e13f4d335fcc82203bbfb760f43c77614bc777bc2f`, Python
3.14, headless; the share and plain rows are unchanged from the first run under
`f12f349495c0bfd156390a79a7f49fc5df9c368117b25604e212fe68798e676a`, and the
lottery row was re-measured after the lottery draw changed to the square of
the ticket state (it read 397/279 = 1.423 under the earlier draw). `tests/test_kerengonen_bell.py` checks the shares at four
hidden phases, the share rule against the model on a coarse grid, the model's
bound, the plain field and a short lottery.

| Setting pair | Local model | Share rule, measured | Lottery clicks, 2232 pairs | Plain field | Quantum owner |
| --- | --- | --- | --- | --- | --- |
| a0 b0 | 118351/393216 = 0.3010 | 118351/393216 | 325/1116 = 0.291 | 1 | 3/5 |
| a0 b1 | 118351/393216 = 0.3010 | 118351/393216 | 17/62 = 0.274 | 1 | 3/5 |
| a1 b0 | 117781/294912 = 0.3994 | 117781/294912 | 7/18 = 0.389 | 1 | 4/5 |
| a1 b1 | -117781/294912 = -0.3994 | -117781/294912 | -479/1116 = -0.429 | 1 | -4/5 |
| S | 826177/589824 = 1.4007 | 826177/589824 = 1.4007 | 386/279 = 1.384 | 2 | 14/5 = 2.8 |

The share rule equals the local model exactly in all four pairs: every
absorbed share is an integer because 1024 is a multiple of the table scale
256, and the average over 72 hidden phases is the same rational number. On the
full 360-step circle the model gives 1.4001, and with exact cosines it would be
7/5, one half of the quantum owner's 14/5 at the same settings. The lottery
estimate, 1.384 from 8928 single-quantum pairs, is consistent with 1.40 and
its statistical spread of about 0.04. The plain field reaches the bound and
no further: with every outcome +1, three correlations of 1 minus one of 1 give
exactly 2. In every world the quanta in records, in flight and escaped equal
the initial stock; the audited world closes with 21504 source and 21504 lamp
quanta absorbed at each analyzer.

## What this does and does not show

- It shows that the phased-ray candidate, run through the same local ray
  owners as the double-slit and de Broglie probes, gives correlations that are
  half the quantum owner's at every setting pair and a CHSH value inside the
  local bound, while the [finite quantum owner](../quantum/bell_chsh.md) gives
  14/5 with the same settings and the same combination. The two candidates are
  distinguished by this measurement, not by interpretation.
- It shows that the classical value is the model's prediction and not a loss
  of visibility: the share rule reproduces `cos(a - b) / 2` exactly, which is
  the Malus-law correlation of a wave with a shared phase.
- It does not show that the classical field could not be extended to reach 2.
  It shows that this candidate, with a phase as its only hidden variable and
  local absorption as its only instrument, does not; that is what a local
  model must do, and it is the reason the quantum owner exists as a separate
  finite state rather than as a phased field.
- The lottery estimate is a counting experiment with a seeded local ticket,
  not an independent random source; other seeds give other counts around the
  same mean.
