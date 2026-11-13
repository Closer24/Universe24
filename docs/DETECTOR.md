# Retained light-to-memory exchange

`universe24/detection.py` is an installed component. Its complete schema-3
preparation runs through the existing Engine, `run`, and `verify`. The `detect`
command replays the saved run and observes retained memory transfers. It does
not advance state or replace the canonical arithmetic click stream.

```bash
python -m universe24 prepare-detector --out runs/detector-input
python -m universe24 run --bundle runs/detector-input --steps 18 --out runs/detector-main
python -m universe24 verify --run runs/detector-main
python -m universe24 detect --run runs/detector-main --out runs/detector-observations.json
```

Use new output paths. `--amplitude 0` prepares a no-light control; `--unarmed`
keeps the same tensor and removes the arming pulse. `--root 0..47` rotates the
body-frame preparation. Positions are lattice coordinates along the selected
axis; changing orientation does not change the tensor. `prepare-light` retains
the previously installed free-wave preparation. This new shared light/memory
law has a different tensor hash and its results must not be assigned to old runs.

## Complete allocation and polynomial

The tensor has exactly 48 dynamical node channels, 144 retained integers, 624
monomials, degree at most two and no old-a reads. Every monomial has support
on the target and at most one face edge. All 48 target polynomials satisfy the
exact joint regular-label/cube 2O action; no channel is appended or padded.

Right ports use the repository's fixed group enumeration: memory q=1, arming
r=6, and selector s=2. The arming port reverses the body x direction. For a
prepared root g, the four nonzero-capable rows are

| Role | Channel | Preparation |
| --- | --- | --- |
| Light p | g | Integer planar amplitude |
| Memory m | gq | Zero initially; complete histories retained |
| Arming c | gr | Boolean plane moving opposite to light |
| Selector | gqs | Uniform one, retained in a,b and not an external switch |

All other complete rows start at zero; their polynomials still have dynamics.
Roles are defined by the preparation and transform together under 2O. They
are not fixed physical species selected by channel names inside the Engine.

For every label h let n_h=R_h e_x. The base tensor input is

    3[b_h(x-n_h)+b_h(x+n_h)]
      + 3 b_(hs)(x)[2b_h(x)-b_h(x-n_h)-b_h(x+n_h)].

Add the following terms for every h, with j=hq and c=hr:

    to u_h: 3 b_c(x)[b_j(x)-b_h(x-n_h)]
            +3 b_c(x)[b_j(x+n_h)-b_h(x+n_h)]
    to u_j: 3 b_c(x)[b_h(x-n_h)-b_j(x)]
            +3 b_c(x-n_h)[b_h(x)-b_j(x)].

These are construction formulas for one fixed tensor. At runtime every term
reads the same complete old snapshot; there is no staged collision callback.
Multiplication on the right commutes with the left label action and offsets
rotate with n_h, giving coefficient-level covariance. The finite port table
also ensures the four-role sector is closed: other triggered pairs have zero
inputs; only the memory's selector equals one on a nonuniform active row.

## Exact prepared dynamics and account

Let n be the light direction, p_in(x)=p(x-n). On the declared sector the
independent first-order map F is

    p'(x) = p_in(x) + c(x)[m(x)-p_in(x)]
    m'(x) = m(x) + c(x)[p_in(x)-m(x)]
    c'(x) = c(x+n).

For c=0 the pulse passes. For c=1 the incoming amplitude and stored amplitude
exchange. The arming pulse moves away; the memory remains local. The inverse is

    p_old(x) = p'(x+n) + c'(x)[m'(x+n)-p'(x+n)]
    m_old(x) = m'(x) + c'(x-n)[p'(x)-m'(x)]
    c_old(x) = c'(x-n).

The tensor evaluates u=3(F(b)+F_inverse(b)) on this sector. Preparing the full
old history a=F_inverse(b) makes unchanged Rule3 give b_next=F(b), a_next=b
and r_next=r. This relation is invariant, with arbitrary legal remainders.
`sector_map` supplies only the initial history and an independent validation
oracle; the Engine performs every actual tick.

Each local exchange is a permutation, and transport is a lattice permutation.
Therefore sum(p²+m²) is exactly conserved. The separate arming and selector
squared norms are also conserved; all resources are counted. The complete
prepared integer amplitudes remain bounded by their initial maximum. This is
a dimensionless excitation account, not a demonstrated material Hamiltonian,
photon energy calibration or relativistic stress-energy conservation law.

For the default 13³ preparation, the light plane starts at x=2 and the arming
plane at x=7. Capture occurs at x=5 on tick 3: light account 169→0, memory
0→169. Memory is unchanged through tick 15. Periodic return of the arming
pulse releases it at tick 16. This is finite retention with endogenous release,
not irreversible absorption or an indefinitely ready apparatus. A larger
lattice postpones the same periodic return; no output filtering hides it.

## Observation contract and physical limits

`detect` first verifies complete canonical replay, then matches the entire
bundle to the declared preparation, checks the independent exchange map and
the conserved accounts, and records every arming opportunity. Output includes
capture, release, exchange and no-transfer totals; capture/release records
carry incoming/outgoing amplitudes and the signed transfer to memory. Persistent
memory is not counted again at each tick. Where present, the corresponding
canonical arithmetic event ID is retained. All arithmetic C0/C1/C2 records
remain unchanged. Photon number is explicitly null.

No-light runs can have arithmetic arming clicks while producing no capture.
Doubling amplitude quadruples transferred quadratic account, without doubling
the number of occupied memory cells. These are essential limits on interpreting
the events as photons. All tensor coefficients are divisible by three, so its
arithmetic clicks remain C0; C0 is not a particle identity.

Still open: an energy-frequency relation hbar*omega, single-photon preparation,
a justified Born ensemble, two-detector anticorrelation, efficiency/noise
calibration, material clocks, recoil and an interacting Maxwell/Einstein limit.
The arming pulse is a prepared counterpropagating resource. It is not a derived
massive detector, thermal reservoir or external power supply. Neither this
component nor `detect` grants general physical acceptance; `--require-physics`
continues to fail. No stochastic sampler or forced outcome is added.

Core tests cover the polynomial and runtime contracts, all 48 orientations,
random signed amplitudes above 64 bits, Boolean arming, scalar-oracle equality,
exact rewind, capture/retention/release, no-light/unarmed controls and rejection
of mismatched interpretation metadata. Fresh saved evidence belongs in `runs/`.

The committed [18-tick main run](../runs/light-memory-main-v1) contains all
complete states, arithmetic clicks and observed transfers: 169 captures on
tick 3, 169 releases on tick 16, and 2,704 arming opportunities without transfer.
The 8,450 arithmetic clicks are a different observable. The [matched controls](../runs/light-memory-controls-v1)
use the same tensor: no light gives no capture despite arming activity; no
arming gives uninterrupted light transport; doubled amplitude stores 676
account units instead of 169 in the same 169 memory cells. All 123 active tests,
generic replay and installed-wheel execution passed; component source hashes
and the test log accompany the main run.
