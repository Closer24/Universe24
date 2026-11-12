# Held-out sourced spatial audit

The unchanged PR47 41-channel projective law fails the preregistered
all-residual decrease gate on a new two-harmonic initial preparation. Field
error, Hamiltonian residual and metric/connection discrepancy improve, but
momentum is nonmonotone and scalar-gradient discrepancy increases. Exact
arithmetic and reversal pass. This is a useful counterexample to promoting
the prior exploratory spatial sequence to general acceptance.

## Frozen protocol

Source pin: `621fc1f55800e50e1db5f6a30ce24bb83716a49a`.
The complete protocol was posted to
[issue40 before execution](https://github.com/Closer24/Universe24/issues/40#issuecomment-6804502332).
There were no parameter or acceptance changes after seeing results.

The periodic physical domain is `[0,1)` and final coordinate/proper time of
the lapse-one reference is `T=1/32`. The three joint levels are
`(n,updates)=(8,2),(12,3),(16,4)`, hence `h=1/64,1/96,1/128`.
All fundamental states are exact integers, with preparation denominator
`2^24`, all six legal carries, unchanged 41 retained channels, degree two,
506 monomials and the existing single-face support rules.

The new continuum profile is

```
phi = sin(2*pi*x)/32 + cos(4*pi*x)/64
Pi = 3/2,  B = I,  K = diag(0,l,l),  l = 2+3*phi/4
psi = D_h(phi),  d^2 = l^2 - Pi^2/2 - psi^2/2.
```

Preparation uses exact rational Taylor sine evaluation, rounds each phi
numerator to the nearest multiple of four, and takes an integer square root
for the dust amplitude. This rounding happens only before execution. The
discrete momentum and scalar-gradient constraints initially vanish exactly;
the Hamiltonian defect from dust rounding is at most `3.72e-7` in these cases.
The two-harmonic profile and scalar momentum differ from the original
single-sine, `Pi=2` exploratory fixture. The same function is sampled at
every level; this is not an ensemble of unrelated seeds.

The gate requires strict decrease at both adjacent comparisons of all four
unscaled final H, M, gradient and metric/connection residuals, and the
independent RK4 field error. Mechanical checks also must pass. Floating
diagnostics and a separately coded planar RHS/RK4 reference never feed the
Engine. The reference uses 384 points/1024 steps, compared with 192/512;
their nested maximum field difference is `4.62731685245e-5`.

## Results

| n / updates | H | M | Gradient | Metric/connection | RK4 field error | Maximum retained bits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 / 2 | 0.0287419011 | 0.00367901860 | 9.89437410e-7 | 0.000191755962 | 0.0698413350 | 119 |
| 12 / 3 | 0.0287336431 | 0.00407137284 | 1.88077256e-6 | 0.000159468180 | 0.0379083288 | 247 |
| 16 / 4 | 0.0249293657 | 0.00248823497 | 2.21968352e-6 | 0.000126076087 | 0.0239814819 | 506 |

**Preregistered acceptance: failed.** Momentum fails the first comparison;
gradient fails both. Every step inverts, full final states rewind, all carries
stay unchanged, positive uniform denominators persist, and strict face
support passes. The independent first-step Euler comparison differs by at
most `1.735e-18` in passive float conversion. All three metric diagonals
remain positive for the completed horizon. Initial/final complete-state
binary hashes, tensor hashes and source hashes are in the JSON evidence.

This finite short-horizon failure does not prove that asymptotic refinement
is impossible, and the decreasing field error does not prove general
Einstein convergence. No finer sequence was selected to replace these rows.
The charged/Maxwell sectors, nonplanar data, operational apparatus and
long-time stability were not tested here.

## Concrete algebraic follow-up

For the isolated reduced Euler update, set `C=psi-b*D(phi)` and use
`b'=b+h*k*b`, `phi'=phi+h*pi`, `psi'=psi+h*(b*D(pi)+k*psi)`.
Direct expansion gives the exact identity

```
C' = (1+h*k)*C - h^2*k*b*D(pi).
```

Thus an initially zero constraint need not stay zero even though its
continuous derivative is `k*C`. The executable exact Fraction control
`h=1/4,b=k=D(pi)=1,C=0` returns `C'=-1/16`. A candidate reduced correction
`+h^2*k*b*D(pi)` is cubic and single-face supported, so this one Euler
product defect has an algebraically concrete repair target. It is **not
implemented** in the law here. The projective retained-history term adds
further factors; general 3D compatible derivatives, support and full
constraint propagation still require a derivation. This isolated identity
is not a claim that it completely explains the measured nonmonotonicity.

## Literature and scope

[Calabrese, Pullin, Sarbach and Tiglio (2002)](https://arxiv.org/pdf/gr-qc/0207018)
prove instability for specified discretizations of linear weakly hyperbolic
systems and show numerical relativity examples in which short or low-frequency
tests conceal nonconvergence. Their equation7/Jordan-block argument and
Fourier-mode discussion motivate a separately fixed profile and future
high-frequency/long-time tests. Their theorem does not directly classify
this nonlinear projective map. The new protocol and Euler product identity
above are local audit work, not results attributed to that paper.

## Reproduction

```bash
python -m validation.synthesis.heldout_geometry --out runs/synthesis/heldout_geometry.json
```

The runner saves the protocol before execution, incremental rows, and a final
report with actual source/seed/tensor hashes. A `.json` destination receives
the aggregate report, with its sibling directory holding protocol/progress.
An exit without assertion failure means the audit executed; consult
`preregistered_acceptance` for its physical comparison result.
