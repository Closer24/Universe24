# Worlds of the law of the shadow (field-only-v1)

Four world files for the field-only engine of feature 20
([the law of the shadow](../../docs/SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1);
[Highlights](../../docs/HIGHLIGHTS.md) 5.4, the model owner's decision of
2026-09-18, the evening: "No real and shadow. There is only shadow. There are
events, which are a whole quantum."). Every world declares `"law": "shadow"`
and is refused by the old engine; the old worlds are refused by this one. The
numbers follow DERIVATIONS.md round 7 (sections 46 to 50): a held content of
2^24 quanta releasing 1/128 of its content per Port heading per interval
(q = 786 432 quanta per interval, the wave regime q >= 1740 r^2 out to r = 20),
its clock four phase steps per interval (K = 2^22 at N = 64, the period 16),
on an open board. Each runs in under a minute on one core:

```bash
PYTHONPATH=src python -m event_universe --init examples/shadow/one_content.json --output artifacts/shadow/one_content
PYTHONPATH=src python tools/run_series.py --out artifacts/shadow/series examples/shadow/one_content.json examples/shadow/two_contents.json
```

- `one_content.json`: one held content at rest at the centre of an open 25^3
  board, 200 intervals. What to read in `run.json`: the shadows' line of `m`
  per tick (`audit`: `released`, `current`, `escaped`, `absorbed`, balanced
  at every tick with the held line constant), the escape per interval
  approaching the emission (0.98 q by tick 200 at N = 64, the rest shed into
  standing content, round 7 section 47 (ii)), and the field's readings by
  `ShadowSimulation.shell_readings` and `cube_flux` in a script (the count
  0.147 q/r^2 rising with the standing residue, the push q/(4 pi r^2), the
  size 3 x 0.2143 sqrt(q)/r in the shell means).
- `two_contents.json`: two held contents at rest, 8 Links apart, symmetric
  about the centre, each held in place (`fixed`), no wait, 200 intervals.
  Each absorbs the other's quanta and is pushed toward it by amount x
  content per quantum (the gravity reading), re-releasing them as its own
  field with the push inverted; `run.json` lists each content's `pushed`
  (the cumulative push) and the momentum books (`held` + `in_flight` +
  `escaped` = 0 at every tick): the two pushes are equal and opposite by
  symmetry, and each is M_B rho M_A/(4 pi d^2) per interval within the
  per-Node ripple (round 7 section 48 (iii)).
- `two_slits.json`: a lamp of light (a paid family, 2^36 quanta, spending
  2^22 per interval on every heading, its clock four steps per interval, the
  period 16 and the wavelength 16 / sqrt 3 = 9.2 Links) at x = 2, an
  absorbing wall at x = 8 of held contents of the paid family `wall`
  (content 1, `hold` for light: they count what they absorb) with two slits
  14 apart, openings of 3 x 3 Nodes in the wall (an opening of one Node is
  far below the wavelength and transmits almost nothing), and a screen of
  marks at x = 17, nine Links behind the wall, on a 23 x 41 x 9 board, 200
  intervals; `one_slit.json` the control with one opening on the axis. What
  to read:
  each mark's `absorbed` `hold` count in `run.json`'s `contents`, by the
  mark's y: with two slits the counts have a minimum near 4 from the axis
  and a maximum near 8.5 beyond it, where the one-slit control falls away
  from the axis without them (a reading, not a law; the light in flight
  reads no wait here, `wait_per_quantum` 0). The slits are openings and not
  held contents that `transmit`: a quantum absorbed and released again
  carries the holder's number, and two numbers are two fields that never
  interfere (Highlights 5.4, point 24), so re-emitting slits give two
  humps and no fringes; the reading was made both ways on 2026-09-18.

The worlds are data for the engine; none of them pins a number, and their
readings are made by a script over the run's record or the Python API
(`event_universe.shadow.ShadowSimulation`), as the tests of
`tests/test_field_only.py` make theirs on smaller boards
([expectations](../../docs/TEST_EXPECTATIONS.md#the-law-of-the-shadow)).
