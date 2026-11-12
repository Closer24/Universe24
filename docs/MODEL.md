# Fixed Rule3 algebra and physical interpretation

This is the current algebra of the supported bundle-driven execution system. Historical variable-divisor and oversized default constructions are retained only as research history. There is no accepted default physical universe.

## Central postulate: one local integer universe

The research starts from this assumption: the whole universe is one network,
and the same fixed local rule acts at every node. A node can read its own
retained integers and those of its immediate face neighbors. It cannot read a
distant node directly. A signal must cross the intervening edges, one update
at a time. Fields, links, matter, clocks and memory must all live in that same
counted state; there is no external controller that chooses the next outcome.

This is a research postulate, not a consequence already proved by quantum
mechanics. The project must still derive the relevant quantum observations,
including interference, outcome probabilities and Bell correlations with their
stated preparation assumptions. Integer state, reversible evolution and local
communication alone do not establish those results.

The current cubic lattice is the implemented version of this postulate. Its
six face neighbors define the communication graph, not an already derived
physical spacetime metric. Prepared distant correlations do not permit a
distant input to change a node in one update.

## State, tensor and budget

On a periodic cubic lattice of side L at least three, each node stores G at most 48 channels. Every channel has two signed integer histories a,b and one remainder r in 0..5. All matter, geometry, apparatus, clocks, workspace and schedules count in G. Integer precision is unbounded and its cost must be measured.

A fixed integer polynomial supplies each local input:

    u[x,i] = sum_m c[m] product_f z[x+offset[f], gear[f], bank[f]]

Each bank is old a or old b. There are at most three nonconstant factors per term. The complete physical support, including endpoints of link channels, is the target and at most one face edge. The old-a dependency graph is acyclic. Static matrix or quaternion data may generate coefficients before preparation; no algebra solver runs during evolution.

The polynomial coupling tensor is not a spacetime metric. A rank-four coefficient notation counts the output index and up to three input factors, not spacetime tensor rank. The binary octahedral group's 48 elements do not require a 48-channel matter inventory or prove particle content.

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

For a saved transition, ell=b_next+a. A canonical arithmetic event requires ell nonzero and a changed complete triple. Its remainder displacement is delta=(r_next-r) mod 6. Classes are C0 for delta 0/3, C1 for 1/2 and C2 for 4/5. Legal Rule3 transitions preserve remainder parity, so their emitted class is C_(u mod 3). A retained oscillator can evolve while emitting no such events.

The decoder is passive and versioned. Tensor labels identify an observation convention; they do not turn an arithmetic event into a physical detector outcome. A material record and its backreaction require counted retained channels and source terms.

Writing r=2*s+epsilon, with s in {0,1,2} and epsilon in {0,1}, makes the
retained remainder explicit:

    ell=floor((u+s)/3), s_next=(u+s) mod 3, epsilon_next=epsilon.
    (r_next-r) mod 6=2*(u mod 3).

C2 is the name of a class, not every third event and not an active choice.
No event count or comparison of possible futures is hidden in the decoder.

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

## Native anisotropic extension and source clock

The separate eight-channel diagonal Bianchi I candidate adds two frozen shear charges S1,S2, with S3=-S1-S2, to the native massless state. The same linear volume recurrence preserves

    J*J-12*D*W-24*N*N*(P*P+sum_i(S_i*S_i))=0.

The common source and metric obey

    H_i=U/(3*V)+S_i/V, I_dot=1/V,
    A_i=V^(1/3)*exp(S_i*I), phi=phi_ref+P*I,
    ds²=-dt²+sum_i(A_i*A_i*dx_i*dx_i).

The anchored integral I is a passive logarithm of actual U and retained Uref. All sixteen Einstein components match the declared homogeneous massless scalar and comoving dust source. The exact source clock is tau_source=(J-Jref)/(6*D*N); J-Jref-6*D*T is invariant when the retained marker T advances by one. The source clock does not read that marker. It is a comoving proper-time diagnostic, not an autonomous emitter, receiver or record.

More explicitly, K_flow=U^2-3*D*V is constant. For q=sqrt(K_flow)>0
and the declared positive chart U,Uref>q,

    I=(1/q)*log(((U-q)*(Uref+q))/((U+q)*(Uref-q))).

This makes I=0 at the retained reference Uref and gives I_dot=1/V.
The implementation evaluates an equivalent stable logarithm. It uses the
actual flow constant rather than replacing it with a desired constraint;
the passive reader must not repair an incorrect source state.

Conserved probe covectors give E²=m²+sum_i(p_i²/A_i²), dx_i/dt=p_i/(A_i²*E), and d(tau_probe)/dt=m/E. These are passive geodesic diagnostics, not retained particle evolution. Spatially varying shear can keep the pointwise Hamiltonian constraint zero while violating momentum constraints; the homogeneous reader rejects that preparation. Thus the added shear charges do not establish a spatial Einstein law.

The exact generic carry-aware momentum identity is pi=6*(b-a)+r and Delta pi=2*(u-6*b). Suitable reciprocal, shift-invariant face potentials can therefore conserve a contracted charge. The separate face control proves local transport, not a stress-complete coupling to this Bianchi source or automatic energy stability.

## Constrained massive homogeneous coordinates

A distinct six-channel candidate stores one projective denominator and numerators for four coordinates x,y,z,w and log-frame beta. Define

    sigma=(x*x+3*y*y)/2, q=z*z+3*w*w,
    p=x*z+3*y*w, eta=y*z-x*w,
    k=-sigma-q/12, phi=2*sigma-q/6-eta, d=sigma-q/12+eta.

Then 6*k*k-p*p-phi*phi-2*d*d is identically zero. This identity is accompanied by an independently checked cubic coordinate force whose pushforward is

    k_dot=3*k*k-(phi*phi+d*d)/2,
    p_dot=3*k*p-phi, phi_dot=p, d_dot=3*k*d/2, beta_dot=k.

The coordinate force itself uses A=d-phi and B=d+2*phi:

    x_dot=3*x*k/2+x*B/4+y/2+z/6-w*A/4,
    y_dot=-x/6+3*y*k/2+y*B/4+z*A/12+w/6,
    z_dot=-x+3*y*A/2+3*z*k/2-z*B/4-w/2,
    w_dot=-x*A/2-y+z/6+3*w*k/2-w*B/4,
    beta_dot=k.

Here the scalar mass squared is one, lapse is one and shift is zero. With
X=(x,y,z,w,beta), numerator vector P, retained denominator Q and X=P/Q,
let F_hom(P,Q)=Q^3*F(P/Q). A fixed integer M clears the rational
coefficients of h*F. The actual compiled integer recurrence is

    Q_next=M*Q^3-Q_old,
    P_next=M*(Q^2*P+h*F_hom(P,Q))-P_old,
    r_next=r.

Every product has degree at most three. M is part of the fixed tensor;
Rule3 still divides by six. The old numerators and denominator are retained,
so this is not an ordinary Euler step. Preparation sets Q_old=P_old=0;
only the first decoded step is exactly Euler. These older registers are a
memory boundary, not another physical state obtained by dividing by zero.
The stated convergence proof concerns the seed X=(1,0,0,0,0),
Q_initial at least 2, this complete older history, and h=1/m with m at
least 16, over time at most 1/8. It is not a
proof for arbitrary constrained initial data.

The same beta defines ds²=-dt²+exp(-2beta)(dx²+dy²+dz²). Exponentiation is passive and absent from the homogeneous polynomial force. The actual retained-history recurrence, not an assumed Euler surrogate, has a first-order finite-time convergence proof on its stated prepared expanding family. Constraint-only wrong-force and wrong-metric controls are rejected.

The old-history subtraction acts in coordinate space, so the earlier obstruction for separately null physical vectors does not prohibit this law. This is a changed physical encoding, not a repair or equivalence claim for old massive45 traces. Exact finite-step dust-mass conservation still fails, scalar phase divided by mass is not universal proper time, and projective integer growth prevents efficient long-time refinement.

## Reversible local records and their source

The bounded collision uses four Boolean rails (p,q,x,y): a record moving in
the positive direction, a record moving in the negative direction, and the
two corresponding carrier rails. It exchanges 1001 and 0110 and leaves the
other fourteen Boolean inputs unchanged. Its integer polynomial is

    delta=p*y*(1-q-x)-q*x*(1-p-y),
    G(p,q,x,y)=(p-delta,q+delta,x+delta,y-delta).

The quartic terms cancel, leaving degree three. On the Boolean domain G is
an involution. It preserves n_plus=p+x, n_minus=q+y, n_record=p+q and
n_carrier=x+y. The packet accounts E=n_plus+n_minus and
P=n_plus-n_minus therefore balance exactly; record recoil is opposite to
carrier recoil. A ready record can route a carrier while retaining its origin.
The ready record supply is part of the initial state and is finite.

Two counted groups A and B each hold these four rails. Let S move positive
rails one edge forward and negative rails one edge backward. Define

    F(A,B)=(G(B),S(A)), F_inverse(A,B)=(S_inverse(B),G(A)),
    u=3*(F(b)+F_inverse(b)), a=F_inverse(b) at preparation.

Then Rule3 gives b_next=F(b), a_next=b and r_next=r. The prepared relation
is preserved at every step. This uses eight channels and 24 integers per node.
The groups A and B are channel groups within the existing state, not extra
history banks. Each polynomial term is onsite or on one face edge. Two
updates give F^2(A,B)=(G S(A),S G(B)). Their phase is a computational
ordering, not an operational proper-time clock.

The source extension adds four retained profiles A_plus,A_minus,B_plus,B_minus,
for twelve channels and 36 integers per node. For the plus profiles the inputs
are

    u_Aplus=3*(3*B_plus(x)-B_plus(x-e)-n_Bplus(x)),
    u_Bplus=3*(3*A_plus(x)-A_plus(x+e)-n_Aplus(x)).

Reverse e for the minus profiles. The n terms are the corresponding record
plus carrier occupancy in the opposite group. There is no runtime solve.
Preparation imposes the interior difference constraints

    Delta^2 A_plus=-n_Aplus, Delta^2 A_minus=-n_Aminus,
    Delta^2 B_plus=-n_Bplus, Delta^2 B_minus=-n_Bminus,
    Delta^2 f(x)=f(x+e)-2*f(x)+f(x-e).

They are preserved on the stated finite causal interior. At even updates,
cubic cardinal B-spline interpolation gives characteristic profiles f(u),g(v)
with f''=-sum_j(n_plus[j]*B1(u-j)) and
g''=-sum_j(n_minus[j]*B1(v-j)); B1 is the linear hat function. For
u=t-x, v=t+x and R=f(u)+g(v)>0, the passive metric is

    ds^2=-2*R^(-1/2)*du*dv+R*(dy^2+dz^2),
    G_uu=-f''/R, G_vv=-g''/R,
    other Einstein components=0.

In units 8*pi*G=c=1 these components give the two null source streams from
the same retained run. The finite causal margin and spline support must be
checked before reading the metric. Summing a periodic second difference
gives zero, so a globally periodic profile with a nonzero nonnegative source
cannot satisfy this chart. The seam remains in the invertible board and is
excluded from the physical chart, not deleted. Repeated finite encounters
are established; massive bound bodies, material clocks and sustained growth
are not established by this construction.

## Finite gauge links and interference

The static control has seven channels: complex matter psi=phi+i*chi,
complex links on the positive x and y edges, and one neutral reader. The
stored U_k(x) transports the neighbor at x+e_k to x. Define

    (H_U*psi)(x)=sum_k[U_k(x)*psi(x+e_k)
                       +conj(U_k(x-e_k))*psi(x-e_k)].
    u_matter=3*H_U*b, u_link=6*b_link,
    u_reader=3*(phi^2+chi^2).

The resulting exact recurrences are

    psi_next=H_U*psi-psi_old,
    U_next=2*U-U_old,
    ell_reader=|psi|^2, reader_next=|psi|^2-reader_old,
    r_next=r.

Equal link histories with U in {1,i,-1,-i} remain stationary. A local
time-independent phase g_x in this finite group acts by psi_x -> g_x*psi_x
and U_xy -> g_x*U_xy*g_y^-1. Apply its signed permutation to both histories.
A negative component also sends r -> 5-r. The identity

    -2*u+5-r=6*(-ell)+(5-r_next)

proves that this action respects the complete update. The passive loop

    W(x)=U_x(x)*U_y(x+e_x)*conj(U_x(x+e_y))*conj(U_y(x))

is gauge invariant. It is a readout across several edges, never a multi-edge
input term. In the prepared two-path experiment, flux w=+1 or -1 gives
amplitude 1+w after two updates, hence intensity 4 or 0; the reader quotient
reports it one update later. The uniform matter mode instead obeys
q_next=4*q-q_old and grows 1,3,11,41. Thus this law does not supply stable
wave propagation or a conserved probability norm.

A separate ten-channel dynamic control retains a charged sign y and three
registers (chi,eta,U) for each positive spatial edge. With Y=y(x+e),

    F(chi,eta,U)=(eta,U*Y,chi*Y),
    F_inverse(chi,eta,U)=(U*Y,chi,eta*Y), y_next=y.

For signs in {-1,+1}, the tuple (chi,eta,U*Y) has a three-cycle. The same
prepared-history compilation u=3*(F+F_inverse) gives exact period dividing
three, including all carries. Under local Z2 signs g_x, the charged values
transform by g_x and U_xy by g_x*g_y. Links and invariant loops can change,
and charged-register changes feed back through a link. Evolving information
nevertheless stays within each edge triplet. There is no propagated signal
through successive edges, electric Gauss law, shared stress source or
operational detector. The static and dynamic controls are distinct tensors;
their successful parts do not constitute one physical gauge field theory.

## Compatibility and acceptance

Equal decoded fields do not imply equal complete states. The two six-channel restrictions of full45 use different default omitted carries and reduced labels. Their common evolution polynomial does not authorize cross-default projection. A separately prepared compatible embedding can be checked without modifying an existing trajectory.

A complete certificate joins tensor, full seed, interpretation, protocol, horizon, trace and current source. Different candidates or timestep laws retain separate identities. A native compiler's successful workspace proof cannot certify a different physical tensor.

Source locations: `validation/sourced_map/`, `validation/conservation_closure/`,
`validation/unified_law/`, `validation/local_unification/`,
`validation/gauge_loop/`, `validation/integration_contract/` and
`validation/system_acceptance/`. The one installed implementation is
`universe24/system/`; the source-only acceptance command reports both positive
scoped results and rejected/blocked physical claims. This document collects
the common algebra and the integrated constructions; detailed proofs and
historical counterexamples remain in their respective research reports.
