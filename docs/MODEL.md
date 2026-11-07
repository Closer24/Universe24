# Algebraic specification

## Geometry and state

The only spatial parameter is the periodic cube's side `L >= 3`:

`Lambda_L = (Z/LZ)^3`, with six distinct face-neighbor sites per node.

Channels are indexed by the 48 elements of `G = 2O`. Every channel `(x,g)` stores `(a,b,r)` with `a,b` arbitrary-precision signed integers and `r in {0,1,2,3,4,5}`. There are 96 integer counters and 48 six-valued remainders per node.

## Unified signed coupling

Let `D=(+x,-x,+y,-y,+z,-z)`, `R(g)` be the spatial cube rotation of group element `g`, and `u=R(g)^(-1)d`. Fix body actions

`B_(+x)=B_(-x)=1; B_(+y)=qy, B_(-y)=qy^(-1); B_(+z)=qz^3, B_(-z)=qz^(-3)`.

Choose three signs `s_x,s_y,s_z in {-1,+1}` before any execution, applying the same sign to both orientations of each body axis. The coupling function is

`C(g,d)=(g B_u, s_u)`.

Its fixed tensor has entries `P[d,g,h] = s_u` if `h=g B_u`, and `0` otherwise. All six matrices are signed permutations: each row/column has one nonzero entry and `P[-d]=P[d]^T`. Under proper cube rotations, the channel labels and spatial directions covary.

## Unique forward law

```text
u[x,g]   = sum over d in D of s(R(g)^(-1)d) * b[x+d, g B_(R(g)^(-1)d)]
ell,r'   = divmod(2*u[x,g] + r[x,g], 6)
a'       = b
b'       = ell - a
```

All positions are modulo `L`, and every channel reads the same old snapshot. No on-site links, hidden stored board, adaptive tensor, external clock gate, or click-triggered update is permitted.

The full state is invertible: from new state `(a',b',r')`, reconstruct old `b=a'` everywhere, form the old neighbor sum `u_old` from these old b values, then `r=(r'-2*u_old) mod 6` and `a=(2*u_old+r-r')/6-b'`. This reconstruction is an audit, not a forward-time procedure.

## External readout

For a completed transition define `ell=b'+a`; an illustrative arithmetic event is declared if `ell != 0` and the local triple changed. With `r=2*theta+epsilon`, `epsilon=r mod 2` is invariant; `theta'=(theta+u) mod 3`. Thus the three arithmetic event classes are `C_0,C_1,C_2` according to `u mod 3`. This passive observation **does not perform physical selection** and never writes to the automaton state.

## Scientific status

Mathematical inversion and discrete symmetry are established by the construction. The existing signed account `Q=sum(6(b-a)+r-background.r)` is generally not conserved by frustrated signed connections; local residual identities remain valid. This is not physical energy. Nor are physical clicks, electromagnetism, angular momentum, the Born rule, exclusivity, autonomous time, or gravity derived.

## Combined spatial reflections

The same fixed coupling also admits all 24 orientation-reversing cubic maps when accompanied by a signed permutation of the 48 channels and the exact remainder map `J(a,b,r)=(-a,-b,4-r+2*(r mod 2))`. With directional matrices `P[d]` and signed channel matrix `F_M`, the condition is `P[M*d] F_M = F_M P[d]`; it implies `W T_M = T_M W` for the complete state.

For the selected x-plane lift and signs `(1,-1,1)`, `T_M^2=J_all Z` and `T_M^4=I`, where `Z` permutes channels by the central element of `2O`. This is not an order-two full-state mirror or an established physical parity representation. The 48 labels still cover 24 proper rotations, not 24 rotations plus 24 mirrors. See [the exact proof, scope and reproduction commands](REFLECTION_AUDIT.md). The transformation compares preparations; it adds no evolution step.
