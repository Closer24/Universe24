# Fixed Rule3 algebra and physical interpretation

This is the current algebra of the supported bundle-driven execution system. Historical variable-divisor and oversized default constructions are retained only as research history. There is no accepted default physical universe.

## State, tensor and budget

On a periodic cubic lattice of side L at least three, each node stores G at most48 channels. Every channel has two signed integer histories a,b and one remainder r in0..5. All matter, geometry, apparatus, clocks, workspace and schedules count in G. Integer precision is unbounded and its cost must be measured.

A fixed integer polynomial supplies each local input:

    u[x,i] = sum_m c[m] product_f z[x+offset[f], gear[f], bank[f]]

Each bank is old a or old b. There are at most three nonconstant factors per term. The complete physical support, including endpoints of link channels, is the target and at most one face edge. The old-a dependency graph is acyclic. Static matrix or quaternion data may generate coefficients before preparation; no algebra solver runs during evolution.

The polynomial coupling tensor is not a spacetime metric. A rank-four coefficient notation counts the output index and up to three input factors, not spacetime tensor rank. The binary octahedral group's48 elements do not require a48-channel matter inventory or prove particle content.

## One forward map and its inverse

All targets use the same old snapshot:

    ell, r_next = divmod(2*u + r, 6)
    a_next = b
    b_next = ell - a

The denominator is always six. A retained projective denominator used by a research decoder is an ordinary counted channel, not a replacement for this divisor. A static timestep used to compile coefficients is fixed before a run.

The exact identity is

    6*(b_next + a) = 2*u + r - r_next.

From the new state, old b is a_next. Recover old-a inputs in the validated dependency order, then compute

    r = (r_next - 2*u) mod 6
    a = (2*u + r - r_next)//6 - b_next.

The division is exact. This recovers both histories and every remainder. Inversion is not a physical time-reversal or CPT theorem. No reset, projection, normalization, future-state lookup or click callback is permitted.

The integer pair q=a+b, p=6*a+r is an alternative lossless encoding: a,r=divmod(p,6) and b=q-a. This coordinate identity is not itself a physical canonical-momentum or Hamiltonian derivation.

## Readout, clocks and conservation

For a saved transition, ell=b_next+a. A canonical arithmetic event requires ell nonzero and a changed complete triple. Its remainder displacement is delta=(r_next-r) mod6. Classes are C0 for delta0/3, C1 for1/2 and C2 for4/5. Legal Rule3 transitions preserve remainder parity, so their emitted class is C_(u mod3). A retained oscillator can evolve while emitting no such events.

The decoder is passive and versioned. Tensor labels identify an observation convention; they do not turn an arithmetic event into a physical detector outcome. A material record and its backreaction require counted retained channels and source terms.

Summing the recurrence gives

    6*sum(ell) = 2*sum(u) + r_initial - r_final.

This is an exact integer ledger, not a physical energy law. Reciprocal force derivatives can establish a common potential under their stated assumptions; they do not automatically bound discrete trajectories or conserve physical stress. Conditional uniform-remainder counts do not establish a preparation measure or the Born rule.

## Exact native homogeneous massless source

A six-channel construction stores volume W, dust charge D, scalar charge P, reference velocity, scalar offset and a coordinate-time counter. Its unchanged Engine input is u_W=6W+18D and u_i=6b_i for the other channels. Prepared source/reference histories are equal; all carries remain explicit.

For a positive integer calibration N, define

    h=1/N, V=W/(4*N*N), J=W-W_old+3*D, U=J/(4*N).
    W_next=2*W-W_old+6*D.

The full-history invariant is

    J*J - 12*D*W - 24*N*N*P*P = 0.

It gives the exact physical flow

    V_next=V+h*U+3*D*h*h/4, U_next=U+3*D*h/2,
    U*U-3*D*V-3*P*P/2=0.

On the declared expanding chart, scale factor A=V^(1/3), k=-U/(3V), scalar velocity=P/V and dust density=D/V reconstruct the sourced flat homogeneous Einstein solution. Roots and anchored logarithms are passive readouts; they do not feed the Engine. The counter calibrates coordinate proper time, not an operational material clock.

The source has rho=P*P/(2*V*V)+D/V and fluid pressure=P*P/(2*V*V). With H=U/(3V),

    H_dot=-D/(2V)-P*P/(2*V*V),
    A_ddot/A=-D/(6V)-P*P/(3*V*V).

For positive D and the expanding chart, density decreases and no bounce or repeated homogeneous density burst occurs. The long-time integer cost is logarithmic in update count for this exact native recurrence. Spatial modes and a mass term are outside this construction.

## Constrained massive homogeneous coordinates

A distinct six-channel candidate stores one projective denominator and numerators for four coordinates x,y,z,w and log-frame beta. Define

    sigma=(x*x+3*y*y)/2, q=z*z+3*w*w,
    p=x*z+3*y*w, eta=y*z-x*w,
    k=-sigma-q/12, phi=2*sigma-q/6-eta, d=sigma-q/12+eta.

Then 6*k*k-p*p-phi*phi-2*d*d is identically zero. This identity is accompanied by an independently checked cubic coordinate force whose pushforward is

    k_dot=3*k*k-(phi*phi+d*d)/2,
    p_dot=3*k*p-phi, phi_dot=p, d_dot=3*k*d/2, beta_dot=k.

The same beta defines ds²=-dt²+exp(-2beta)(dx²+dy²+dz²). Exponentiation is passive and absent from the homogeneous polynomial force. The actual retained-history recurrence, not an assumed Euler surrogate, has a first-order finite-time convergence proof on its stated prepared expanding family. Constraint-only wrong-force and wrong-metric controls are rejected.

The old-history subtraction acts in coordinate space, so the earlier obstruction for separately null physical vectors does not prohibit this law. This is a changed physical encoding, not a repair or equivalence claim for old massive45 traces. Exact finite-step dust-mass conservation still fails, scalar phase divided by mass is not universal proper time, and projective integer growth prevents efficient long-time refinement.

## Compatibility and acceptance

Equal decoded fields do not imply equal complete states. The two six-channel restrictions of full45 use different default omitted carries and reduced labels. Their common evolution polynomial does not authorize cross-default projection. A separately prepared compatible embedding can be checked without modifying an existing trajectory.

A complete certificate joins tensor, full seed, interpretation, protocol, horizon, trace and current source. Different candidates or timestep laws retain separate identities. A native compiler's successful workspace proof cannot certify a different physical tensor.

Source locations: `validation/sourced_map/`, `validation/unified_law/`, `validation/integration_contract/`, `validation/system_acceptance/`. The one installed implementation is `universe24/system/`; the source-only acceptance command reports both positive scoped results and rejected/blocked physical claims.
