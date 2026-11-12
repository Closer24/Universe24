# Same-law Einstein constraint audit

The shared massive 45-channel construction closes the previous source-identity gap: its geometric frame, scalar source and board diagnostics use one tensor. It does **not** close the nonlinear Einstein constraint gate. The new exact counterexample locates an obstruction in the temporal encoding even before spatial derivatives matter.

## Independent reduction and exact counterexample

Use units `c = 8πG = 1`, lapse one, zero shift, a spatially homogeneous isotropic inverse triad `B_a^i = B δ_a^i`, `K_ab = k δ_ab`, real scalar `φ`, momentum `π`, and signed dust amplitude `d`. All charged, magnetic, connection and spatial-gradient components vanish. The independently written homogeneous equations are

\[
\dot B=kB,\quad \dot k=3k^2-\tfrac12(m^2\phi^2+d^2),\quad
\dot\phi=\pi,\quad\dot\pi=3k\pi-m^2\phi,\quad\dot d=\tfrac32kd.
\]

The Hamiltonian defect is `C = 6 k² − π² − m² φ² − 2 d²`. Direct differentiation gives the exact identity `Ċ = 6 k C`. Consequently constrained initial data stay constrained under the continuum equations. This identity is checked symbolically without calling the production equation builder.

Take `B=1, k=-1, φ=2, π=0, d=1, m²=1`. Every initial constraint vanishes, with `ρ=3` and scalar pressure `p=-2`. The projective preparation has its old numerator and denominator registers zero, so its first physical update is exactly Euler. After a step `h`, independent algebra gives

\[
B'=1-h,\quad k'=-1+h/2,\quad\phi'=2,\quad\pi'=-2h,\quad d'=1-3h/2,
\qquad C'=-7h^2.
\]

The actual shared Engine/tensor is required to reproduce this identity exactly. The massless control `(φ,π,m²)=(0,2,0)` instead gives `C'=-3h²`. Flat empty data give zero. All carries and complete inverse states are checked, so the violation cannot be dismissed as floating-point error or lost reversible state.

**A constraint-added RHS that vanishes on this initial constraint surface cannot change this first step.** Therefore adding more vanishing continuum constraint terms, including the flat-symbol repair in PR #50, cannot by itself cure this defect while keeping this preparation and Euler first-step encoding. This is a narrow algebraic obstruction, not a proof that every possible integer/local encoding is impossible.

The audit compares every homogeneous physical field with an independently written reduced projective recurrence, retaining the exact denominator-memory correction after the first step. It must use the off-constraint `k̇` above. Substituting `k̇=(π²+d²)/2` from the constraint surface after the defect appears would silently evolve a different system and hide the failure.

## Reproduction and interpretation

```bash
python -m validation.geodesic_board.constraint_audit
```

Results go to `runs/geodesic-board/constraint-audit.json`. Controls and temporal refinements use 27 physical nodes. The latter run 2/4/8 steps at fixed final proper time `1/8` and report constraint defects and retained bit sizes. It is a temporal refinement diagnostic only. It does not test spatial convergence, transverse perturbations, generic nonlinear constraint propagation, or physical clock apparatus. A decreasing short-run defect does not turn the exact-preservation failure into a pass.

The next temporal proposal should carry this exact counterexample as a mandatory test, together with field error, full-state reversal and the channel ledger. A constraint-compatible discrete identity must be derived jointly for gravity and matter; runtime projection, clipped densities or an external implicit solver remain prohibited by the current system contract. Changing the physical encoding or using additional retained arithmetic phases is a research possibility, but requires a new explicit proof of locality, inverse and total allocation before integration. No such compiler is supplied by this audit.

## Primary-source context

- [Gourgoulhon, 3+1 Formalism and Bases of Numerical Relativity (2007)](https://arxiv.org/abs/gr-qc/0703035), especially the constraint propagation discussion in chapter 10: continuum propagation is tied to the Einstein evolution equations and Bianchi identities. It is not a finite-difference preservation theorem.
- [Sarbach and Tiglio, Exploiting gauge and constraint freedom in hyperbolic formulations of Einstein's equations (2002)](https://arxiv.org/abs/gr-qc/0205086): constraint additions can alter hyperbolicity while agreeing on the constrained continuum sector. That motivates the formulation repair, but does not validate this project's discrete temporal map.
- [Calabrese, Pullin, Sarbach and Tiglio, Convergence and stability in numerical relativity (2002)](https://arxiv.org/abs/gr-qc/0207018): unstable or weakly hyperbolic formulations can escape limited convergence tests. The board therefore must expose the constraint residual and reserve claims about general convergence for held-out spatial/directional controls.

These sources motivate the checks. The `−7h²` and `−3h²` defects and the source-specific first-step obstruction are derived here, rather than attributed to those papers.
