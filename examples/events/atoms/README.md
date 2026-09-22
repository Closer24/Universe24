# The atoms series: hydrogen at r = 12 and helium under form B

Two worlds of series H's base, written by `make_worlds.py` (which imports
series H's fan, flux count and orbit arithmetic from
[bohr/make_worlds.py](../bohr/make_worlds.py)), on the model owner's word
of 2026-09-21 (record 333, "it is important to show one atom or two, to
close all the corners"). The pins before the runs, every number labelled by
its kind, are in [docs/designs/atoms/PINS.md](../../../docs/designs/atoms/PINS.md),
printed by its host map; the runs come after form B lands, by an
experimenter, registered as rows of series H.

- `hydrogen_r12.json` (`rays-atoms-hydrogen-r12-form-b-v1`): series H's
  `r12` with the electron's momentum derived for the circular orbit under
  form B's drive (293783192 in place of 288249497), the action re-fixed
  by series H's rule under the same drive (h = 16 p(8) = 5536242544), a
  `wave` detector `at_proton` on the proton's Node, 7500 intervals.
- `helium_r12.json` (`rays-atoms-helium-r12-form-b-v1`): binding-v1's
  square ([binding/alpha_square_bond.json](../binding/alpha_square_bond.json):
  `p` of charge 4 and `n`, each with its held `nuclear` and `bond`) fixed
  at the four Nodes about the centre, two electrons of the register's
  electron point-symmetric about it at r = 12.51 with opposite tangential
  momenta, each releasing on the fan's band |c| <= 2 and the four in-plane
  headings so that the partner's rays push it, a `wave` detector
  `at_nucleus` on the four nucleons' Nodes, 3700 intervals.

```bash
python examples/events/atoms/make_worlds.py
PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/atoms examples/events/atoms/*.json
PYTHONPATH=src python tools/click_readings/bohr.py artifacts/atoms
```
