# Native integer shears before projective homogenization

Researcher 1 of the eight-researcher review, 11 November 2026. Coordination:
[issue 40](https://github.com/Closer24/Universe24/issues/40). Code inspected:
local integration commit `613ea1b`; published projective proposal
[#47](https://github.com/Closer24/Universe24/pull/47) at
`621fc1f55800e50e1db5f6a30ce24bb83716a49a`. This report changes no Engine,
runtime interface, supported physical model, or acceptance status.

## Result and recommendation

**The existing Rule3 is already an exact integer kick--drift map.** The
projective denominator is therefore not an unavoidable cost of the core law.
Use that native algebra to derive a local action and compatible conserved
quantities before reintroducing a general field integrator. This is a concrete
research route; it is not a replacement Einstein tensor ready for promotion.

The denominator-free controls below run 600--1,000 actual Engine steps with
bounded integers and exact rewind. A cubic counterexample still grows to
6,785 bits in eight steps. Stability and continuum refinement remain separate
requirements even after eliminating the projective denominator.

## Primary literature actually inspected

| Paper and inspected part | Relevant result | Universe24 boundary |
| --- | --- | --- |
| [Earn & Tremaine, *Exact numerical studies of Hamiltonian maps* (1992)](https://ms.mcmaster.ca/earn/pdfs/EarnTrem1992_PhysicaD_ExactHamiltonianMaps.pdf), section 5, pp.17--19, equations 11--13 and shear theorem | Lattice maps formed by two invertible shears can be related to symplectic maps under stated derivative-symmetry assumptions. | Supplies the correct interpretation of integer shears; does not identify our retained variables with a GR canonical pair or prove energy preservation. |
| [Rein & Tamayo, *JANUS* (2017)](https://arxiv.org/pdf/1704.07715), sections 2.1--2.4, especially equations 3 and 5 | Integer position/velocity additions make rounded-force leapfrog exactly reversible when the force is recomputed identically in both directions. | Their force evaluation uses floating arithmetic and arbitrary rounding; neither is an allowed runtime callback here. Their implementation cannot be copied into Rule3 as a solution. |
| [Stam, *An Exact Bitwise Reversible Integrator* (2022)](https://arxiv.org/pdf/2207.07695), sections 2.3--4, equations 8--10 and source code | Symmetric splitting with fixed-point additions provides another practical reversible construction. | Its floating force routine and external step size also violate our fundamental-law contract. Reversibility alone does not establish the broad energy/stability language sometimes attached to these methods. |
| [Brunton et al., *Koopman invariant subspaces...* (2016)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0150171), finite-observable construction and sections on continuous/discrete closure | Finite linear descriptions require a closed observable subspace; differentiation can introduce new observables and destroy closure. | Useful when searching for small exact sectors. It does not justify assuming the full nonlinear Einstein system is a finite collection of independent rotations. No global no-go theorem for Universe24 is inferred. |

These sources motivated the comparison. All Rule3 identities and measurements
below are independently derived and checked here.

## Exact change of coordinates, with no new channel

For a retained triple with `0 <= r < 6`, define

```text
q = b
p = 6(b-a) + r
```

This is a bijection between `Z x Z x {0,...,5}` and `Z x Z`. Its inverse is

```text
b = q
a = q - floor(p/6)
r = p mod 6
```

It is only a mathematical reparametrization: the runtime retains every
original `a,b,r`, so this does not change the budget convention.

For a tensor whose input is `u = 6q + F(q)` and has no old-a dependence,
substitution into the unchanged Rule3 gives the exact identities

```text
p_next = p + 2 F(q)
q_next = q + floor(p_next/6)
r_next = p_next mod 6.
```

The inverse first recovers `q = q_next-floor(p_next/6)`, then
`p=p_next-2F(q)`. Recomputing the force from recovered q loses no information.
Every sign and all six carry classes are included. The parity of p, equivalently
the parity of r, is invariant. A force that is degree <=3 and single-face-local
retains those properties after adding `6q`; it adds no scheduling state.

There is a discrete kinetic primitive. For `p=6m+s`, `0<=s<6`, set

```text
K(p) = 3m(m-1) + ms.
K(p+1)-K(p) = floor(p/6).
```

This holds for negative p too. It is a finite-difference identity, not an
assertion that this K plus an arbitrary potential is exactly conserved.

If F is the negative gradient of one smooth potential, its Jacobian is
symmetric. The kick is then a canonical shear. The componentwise integer
drift can be extended by smooth interpolation through its integer samples,
giving a separable canonical shear on real phase space. Their composition has
the lattice-map symplectic interpretation discussed by Earn--Tremaine.
The literal floor map is discontinuous on real arguments; calling that map a
smooth symplectomorphism would be incorrect. Neither this interpretation nor
the inverse proves conservation of a prescribed Hamiltonian or GR constraints.

## Reproducible bounded and failing controls

Run from the repository root:

```bash
python -m validation.research_eight.01_native_lattice_audit
```

The program writes `runs/research_eight/01_native_lattice_audit.json` with its
source hash. It uses the actual unchanged Engine and an independent scalar
identity/closed-form transport oracle.

| Check | Exact result |
| --- | --- |
| Signed scalar identity and bijection | 26,250 cases, all six remainders |
| Integer kinetic difference | 20,001 signed p values |
| `u=3b`, one onsite channel | 600 steps, 27 nodes, at most 11 retained bits; period divides six; `a²-ab+b²` invariant |
| `u=3(q[x+1]+q[x-1])`, one channel | 1,000 steps on 125 nodes, at most 21 retained bits; exact independent `f(x+n)+g(x-n)` trajectory |
| Wave with incompatible zero-mode history | `q=-n`; boundedness fails as expected despite exact rewind |
| `u=5q-q³`, one onsite channel | Bit counts `3,4,11,29,85,253,755,2263,6785`; exact rewind, failed boundedness |

All complete inverse checks pass. The wave is one-dimensional transport on the
cubic lattice, not isotropic 3D Einstein propagation. The oscillator is a
computational period, not a calibrated proper clock. Both use fixed state
allocation without a projective denominator. They are validation controls and
are not appended to the existing 44-channel law as an independent metric.

## Why arbitrary refinement is still blocked in the direct encoding

Let a physical scalar be `x=q/S`, with physical time step h. Ignoring the
explicit carry error for a moment, the native second difference gives

```text
x[n+1]-2x[n]+x[n-1] = F(q[n])/(3S) + (r[n]-r[n+1])/(6S).
```

To approximate `x'' = c_d*x^d` directly, the required coefficient of `q^d`
in F is `k_d=3 h² c_d / S^(d-1)`. For fixed nonzero c_d, h tending to zero
and S tending to infinity makes this coefficient nonzero but smaller than one
in magnitude. It cannot remain an integer. The audit explicitly checks the
failed integrality for degrees 1--3 at `S=2,4,8,16,32`, `h=1/S`.

This obstructs the **single-microtick, common-scale direct polynomial-force
ansatz**. It does not rule out a different representation, weak-field or
long-wave limits, exact invariant sectors, or a counted multi-tick arithmetic
circuit. In particular, spatial/time joint refinement can keep a wave's
Courant ratio fixed: small lattice differences provide the small physical
increment, without a small onsite coefficient. Calling the same fixed-period
oscillator a slower physical clock does not solve the onsite nonlinear problem.

## Concrete next construction and falsifying milestones

1. **Native action before arbitrary RHS.** Seek one local potential/action with
   at most quartic terms, so its reciprocal force fits cubic Rule3. Verify the
   exact discrete symmetry and its actual conserved quantity. For an edge
   potential depending on `q_y-q_x`, conservation of sum p is a uniform-field
   shift charge; it is not automatically physical spatial momentum.
2. **Canonical state interpretation.** One channel can mathematically hold one
   pair q,p, so artificial leapfrog history need not consume a second physical
   bank. But the existing 40 first-order frame/matter fields are not supplied
   in canonical pairs. ADM's metric-dependent DeWitt kinetic term is
   nonseparable. Identifying p with K would not derive its equations. A claimed
   channel reduction requires an explicit canonical transformation, reality/
   gauge constraints, and one shared matter/geometry action.
3. **Small-step arithmetic as a counted compiler problem.** JANUS suggests
   recompute/uncompute for rounded forces, avoiding a growing history. The
   current tensor cannot evaluate `floor(P/3^k)` in one step for arbitrary k.
   A serial base-three quotient circuit is a possible use of microticks, but
   must supply a static cubic local schedule, restored workspace and exact
   inverse. The four unallocated slots in protected44 are only a proposed
   workspace budget; no such four-slot circuit is implemented or proved here.
4. **Reject by actual failure.** Before any GR promotion, require a fixed-time
   nonlinear coupled matter test with separate time/space/seed refinement,
   metric positivity, H/M/torsion defects, held-out initial data and integer
   bit budgets. If native scaling cannot resolve nonlinear forces or the
   schedule exceeds 48, this route is blocked rather than rescued by an
   external force evaluation or denominator reset.

The most defensible immediate direction is to retain the native integer
shears, derive discrete constraints from the same local action, and prove a
small-step representation for that particular action. The literature gives
pieces of this construction, not a ready-made 48-channel general Einstein
solution. All general physical gates remain open.
