# Temporal accuracy and integer cost of the shared massive45 run

## Result

The same corrected massive45 law used by the event board approaches an independent homogeneous continuum reference over the declared short interval, with observed first-order temporal accuracy. Its exact reversibility does not make the temporal discretization constraint preserving or affordable at long horizons.

This audit uses the shared `build_program` and `prepare_seed`; the three refinement tensors differ only through the declared physical time step. All runs use 45 channels, 27 nodes, all six retained remainder classes, the actual fixed-six Engine and complete rewind. No reference result is fed into evolution.

Reproduce:

```bash
python -m validation.geodesic_board.time_cost_audit
```

Fresh output is `runs/geodesic-board/time-cost-audit.json`. The aggregate runner can call `audit()` directly.

## Independent continuum oracle

Use the spatially flat homogeneous metric, lapse one, shift zero, and units `c=8*pi*G=m=1`. Instead of calling the production frame RHS, integrate the continuum equations in the different variables `(a,H,phi,pi,rho_d)`:

\[
\dot a=Ha,\quad \dot H=-\tfrac12(\pi^2+\rho_d),\quad
\dot\phi=\pi,\quad \dot\pi=-3H\pi-\phi,\quad
\dot\rho_d=-3H\rho_d.
\]

The initial values are `(1,1,2,0,1)`. They satisfy
`3 H² = rho_d + (pi²+phi²)/2` exactly. The comparison outputs are
`B=1/a`, `k=-H`, `phi`, `pi`, `dust_amplitude=sqrt(rho_d)`.

The Raychaudhuri equation here is the on-constraint continuum equation; it is not the production off-constraint `dot k=3k²-(phi²+dust_amplitude²)/2`. The two are equivalent on the continuum constraint surface. This distinction lets the reference expose the production trajectory's finite-step error without replacing the production dynamics.

The external oracle uses 60-digit Decimal RK4 at 1,024 and 2,048 steps over final proper time `T=1/8`. Their maximum endpoint difference is `2.23762e-17`; the finer Friedmann residual is `1.63204e-18`. This is a numerical reference self-consistency check, not a certified interval enclosure or proof of continuum uniqueness. Its error is negligible relative to the observed Engine differences.

## Actual integer results

| Engine updates | Physical dt | Max field error against reference | Absolute Hamiltonian defect | Largest retained integer (bits) |
| --- | --- | --- | --- | --- |
| 2 | 1/16 | 0.0179896959643 | 0.0376438312386 | 39 |
| 4 | 1/32 | 0.00851264848019 | 0.0162753464348 | 186 |
| 8 | 1/64 | 0.00414655051734 | 0.00761621104416 | 3,321 |

All five field errors decrease. The successive maximum-norm temporal orders are `1.07949` and `1.03770`. The default four-update board uses tensor
`fbbf8f9b4128563e786ff0b57069fe18320698451c0ac9acb0c947c568cfc617`, matching this middle row.

The constrained seed and short time series do not test spatial convergence, oblique modes, generic nonlinear stability or a nondegenerate metric for all valid states. The positive-definite metric and rewind statements are finite-run checks. The exact first-step constraint failure remains as documented in `constraints.md`.

## Exact cost obstruction

The retained common denominator satisfies

\[
D_{n+1}=C D_n^2-D_{n-1},\qquad D_{-1}=0,\quad D_0=32,\quad C\ge2.
\]

Inductively `0 <= D_(n-1) <= D_n²`, so `D_(n+1) >= D_n²`; hence
`D_n >= 32^(2^n)`. The actual audit checks the bound after every step. At eight updates the proof already requires at least 1,281 denominator bits; the actual denominator has 3,320 bits. The 48-channel budget bounds the number of retained integers, not their size or the memory and arithmetic work required for them. A common-divisor reduction would need a reversible representation and cannot be inserted as a lossy runtime normalization.

## Next implementable research gate

The next compiler change should target a counted reversible temporal composition in native Rule3 coordinates, with a declared discrete gravity/matter constraint identity. Before replacing the projective compiler it must provide: exact integer inverse including carry; face-edge support and degree bound at every microtick; all scheduler and arithmetic workspace within 48; a derivation of its physical-time map; nontrivial constraint and source-work tests; and held-out time/space refinement.

Symmetric splitting or a variational method is a candidate design principle, not an established fix. The general gravity/matter Hamiltonian is not already a separable potential-kick problem. Ordinary implicit midpoint would require an undeclared runtime solve, and a projection would violate complete-state reversibility. Neither is silently inserted here. The native representation already investigated in `validation/research_eight/01_native_lattice_audit.py` offers a starting point, but its successful restricted controls do not establish a full Einstein compiler.

## Primary source ledger

- Éric Gourgoulhon, *3+1 Formalism and Bases of Numerical Relativity* (2007), [arXiv:gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035). Background for the geometric/source split and its separate constraints. The FLRW equations and independent finite-time audit above are explicitly derived for this fixture; no paper theorem is transferred to Rule3.
- Ernst Hairer, *Geometric Numerical Integration, Lecture 2: Symplectic integrators* (2010), [author-hosted notes](https://www.unige.ch/~hairer/poly_geoint/week2.pdf), §1 and §§3–5. The notes distinguish symmetry, symplecticity, composition and general implicitness; separable Hamiltonians admit special explicit cases. They motivate the proposed temporal-design search but do not prove Einstein constraint preservation, bounded integer cost or a 48-channel implementation.

Status: **finite homogeneous temporal convergence evidence passed; exact discrete constraints failed; efficient long-horizon projective evolution failed; general Einstein convergence not established.**
