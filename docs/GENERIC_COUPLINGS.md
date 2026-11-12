# Generic couplings and an exact restricted sector

The seven-specialist findings from [issue #40](https://github.com/Closer24/Universe24/issues/40#issuecomment-6811093154)
are executable source code in `validation/generic_couplings/`, covered by the
repository unittest suite and reliability CI. They use the same `Tensor`,
`Engine`, sealed bundles, canonical decoder and saved-run verifier as the
supported system. They add no runtime mode or default physical model.

```bash
python -m validation.generic_couplings --out runs/generic-couplings
python -m universe24 verify --run runs/generic-couplings/runtime/full
python -m universe24 verify --run runs/generic-couplings/runtime/reduced
```

Choose a new output directory for each run. `evidence.json` records actual
source hashes, tensor/bundle/run identities, counts and scope. Both runtime
directories contain complete input bundles, traces, clicks and verification
reports. All physical acceptance gates remain unestablished; adding
`--require-physics` to verification must still fail.

## What is generic

The coefficient tensor is a local polynomial interaction table. Channels own
complete `(a,b,r)` state; a clock is a property of a particular trajectory and
observable, with physical calibration still to be supplied. Degree at most
three and exact reversibility do not select a physical spacetime tensor,
conserved energy, stable dynamics or Einstein equations.

For every legal transition, write `r=2s+epsilon`, with `s` in 0..2 and `epsilon`
in 0..1. Then `ell,s_next=divmod(u+s,3)` and `epsilon_next=epsilon`.
For every emitted canonical click the class is `C_(u mod3)`. The separate
emission predicate is still required. In particular `u=0` gives the nontrivial
period-four orbit `(1,0,r)->(0,-1,r)->(-1,0,r)->(0,1,r)->(1,0,r)`, with no
canonical clicks. A mechanical cycle, a physical tick and a recorded click
cannot be equated from these arithmetic definitions.

The passive coordinates `position=b`, `momentum=6(b-a)+r` are bijective, with
`r=momentum mod6`, `a=position-floor(momentum/6)`. The exact update identity is
`momentum_next=momentum+2u-12position`,
`position_next=position+floor(momentum_next/6)`. Packing saves zero channels
under the current contract. Old-a dependence introduces floor functions into
the transformed drive; this is not a general degree-three compiler or
symplecticity theorem. The original Engine and inverse remain authoritative.

## Exact full45 to six-channel restriction

`sector.build_reduction()` consumes the existing parameterized full45 builder
`validation.geodesic_board.run.build_program` at h=1/64, dx=1/4 and mass²=1.
The full tensor fingerprint is
`6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0`.
Coefficient restriction is compared with an independently declared onsite
six-channel tensor, fingerprint
`6e00a1bb2dd7f7f9ddf5c1bd66b31e5bafc450fff12d98515367368e1e0d2c3a`:

```text
u_D   = 768 D²
u_B   = 768 D B + 12 K B
u_K   = 768 D K + 36 K² - 6 phi² - 6 d²
u_phi = 768 D phi + 12 D Pi
u_Pi  = 768 D Pi + 36 K Pi - 12 D phi
u_d   = 768 D d + 18 K d
```

All RHS values are current retained b values. There are six complete channels,
18 retained integers per node and 14 monomials. Ordinary fixed-six Rule3
performs the update and retains every remainder.

The embedding requires homogeneous old/current histories, equal diagonal B
triples, equal diagonal K triples and zero omitted triples. It keeps denominator,
common frame diagonal, common K diagonal, real scalar value/momentum and signed
dust amplitude. Its six legal carries are retained and copied to each duplicated
field; omitted full45 carries are zero. Carries may vary by node because these
coefficients freeze them. No independent discarded carry is silently removed.

`embed_state` and `project_state` reject data outside this complete-state domain.
The polynomial closure proof establishes `F_full(H(s))=H(F_small(s))` and the
inverse relation. A custom source tensor is accepted by the restriction API only
if its restricted polynomials still agree; its full fingerprint remains distinct.
The default saved-runtime audit additionally requires the exact fingerprints
above. The runtime reconstructs every full before/after snapshot and then
redecodes the **full** canonical click stream. The raw six-channel click stream
has different field identities and is not itself the full45 stream.

This is a homogeneous isotropic neutral scalar/comoving-dust invariant sector.
It excludes spatial packets, anisotropy, charged phase and Maxwell excitations.
It inherits the full proposal's physical constraint and time-stability failures;
the strong seed still has first-step Hamiltonian defect `-7h²`. The eight-step
fixture reaches 3,742-bit retained integers. Fewer channels do not remove
projective integer growth. General physical model gates are unchanged.

## Reciprocal ports and clocks

One local polynomial interaction can generate all reciprocal responses:
`Phi_e=-h_e²*|psi_y-psi_x|²/2`, with two node fields `psi=(X,Y)` and one face-link
weight, gives 14 cubic terms. `geometry.build_reciprocal_edge(axis)` constructs
this mechanical example; it is not attached to full45. Deleting the link's
reaction fails reciprocity. Oracle/remainder/rewind checks establish execution;
the audit reports integer growth rather than claiming stability.

The module also retains free-oscillator and non-synchronization controls.
Reciprocal influence alone does not imply synchronization. The covector test
uses `ell=dt-dz`: rest and transverse speed3/5 have equal phase per coordinate
time, but proper-time rates1 and4/5. Conformally related metrics can have the
same null cones and different proper-clock rates/curvature. A covector is not
an operational clock or a complete connection law.

The next physical test still requires one identified law, actual transported
matter/signals and independent clock records, one calibration, complete source
stress accounting and refinement in a declared regime. See #41 for apparatus
and #45 for retained selection. This integration supplies executable controls
and exact restricted reconstruction, not Einstein/Born/complexity acceptance.
