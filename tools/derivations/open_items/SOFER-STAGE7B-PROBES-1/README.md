# Sofer's probes of stage 7b's design (tensor24-review 06c823ca2)

One file, run on the repo's Python with `python -I`, its output beside it.

- **chain_rule.py** `<runs> <seed>`: the Boss's fourth question of 2026-10-29, 02:30 UTC (the composition test of Postulate 6, thread comment
  6486246054), answered for the time gear in the ruler's form. The push per notch of a field Y on the torus is, by the six neighbours' second
  difference D and the three centred differences G the act already reads, p(Y) = sum over the axes of D Y / Y - (G Y / Y)^2, which is
  Y lap(ln Y) / Y. For a product P = Y1 Y2 the chain rule is exact on the lattice, with a remainder E written from the factors' own readings
  (a = D Y1 / Y1, u = G Y1 / Y1 and b, v for Y2, per axis, c = u b + v a): p(P) = p(Y1) + p(Y2) + E with E = sum of a b / 2 - (u + v) c -
  c^2 / 4. The head's law, q(Y) = sum of D Y / Y + 3 (G Y / Y)^2, misses the same sum by H = sum of 8 u v + a b / 2 + 3 (u + v) c +
  3 c^2 / 4, so it fails on every pair of fields whose gradients cross, whatever the lattice. The test therefore needs no lattice spacing, no
  bound and no smooth field: the act's numerator over the gear's value in fractions, set against the factors' pushes plus E computed in the
  test, and the head's law as the mutant.
- **chain_rule.txt**, its run (40 pairs of random whole-number fields, values to 10^6, a 3 by 4 by 5 torus, seed 20261029): both identities
  hold exactly at 2,400 of 2,400 sites, and the two mutants of E (the c^2 / 4 term dropped, the middle term's sign turned) fail at 2,400 of
  2,400.

## What it does not cover

- Uniform grips and the space part of the push alone; a metric that varies adds the grips' terms (7c), and the strides' term in time stands
  apart.
- The count form of the time gear (David's p17, toys-5 1b6a92195), where the law is the plain act on the count and the composition is the
  addition of strides: its test is his.

---
Sofer.
