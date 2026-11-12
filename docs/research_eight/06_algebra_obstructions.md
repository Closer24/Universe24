# Researcher 6: exact obstructions and admissible algebraic escapes

Scope: research toward the fixed-six, cubic, one-face, at-most-48-channel contract. This report changes neither the Engine nor an accepted physical model. The inspected local base is `613ea1b`; the remote research baseline is PR #47, `621fc1f55800e50e1db5f6a30ce24bb83716a49a`. Current issue #40 and its PR #47 evidence were read. The findings below are targeted mathematical statements, **not a no-go theorem for Universe24 or discrete Einstein gravity**.

## What the literature establishes

| Primary source and inspected sections | Established result | Consequence and limit here |
| --- | --- | --- |
| Kato, Sakamoto and So, [No-Go Theorem of Leibniz Rule and Supersymmetry on the Lattice](https://arxiv.org/pdf/0810.2360), section 2, equations (2.1)–(2.7); companion [finite-volume analysis](https://arxiv.org/pdf/1212.1533), sections 2–3 | In the stated translationally invariant lattice setting, nontrivial local products and local difference operators cannot obey the ordinary Leibniz identity. The Fourier relation becomes a functional equation whose nonzero derivative solution is nonlocal. The finite-volume paper specifies locality across increasing lattice sizes. | Replacing continuum derivatives by local differences while retaining all continuum product manipulations is unsupported. Shifted identities and different discrete products are alternatives. The theorem does not rule out convergence, weakened identities, discrete gauge constructions, or all finite channel systems. |
| Bahr and Dittrich, [(Broken) Gauge Symmetries and Constraints in Regge Calculus](https://arxiv.org/pdf/0905.1670), introduction, section 7, section 8 | Their curved four-dimensional Regge examples break exact gauge symmetry; canonical equations have pseudo-constraints. Their Hessian analysis relates null directions to genuine constraints. They explicitly leave open other symmetry-preserving actions. Exact mechanical actions obtained from boundary-value solutions illustrate a special alternative; field-theory perfect actions can require nonlocal couplings. | A geometric action or a holonomy loop is not itself a proof of exact Einstein constraint propagation. A proposal must state its discrete symmetry and actual local implementation. Importing a continuum boundary solve or nonlocal perfect action violates this runtime contract unless replaced by a proved local construction. |
| Rein and Tamayo, [JANUS: A bit-wise reversible integrator for N-body dynamics](https://arxiv.org/pdf/1704.07715), section 2.1, equations (3)–(4), and section 2.4 | A position-Verlet form can be bit reversible although force evaluation and rounding are not individually invertible: identical retained current positions reproduce the identical rounded force in both directions. JANUS uses mixed integer/floating arithmetic and discusses formal symplecticity separately from its exact bijection. | Reversible dynamics need not carry a growing common projective denominator. JANUS is inspiration, not a compliant import: its floating-point force and rounding are outside the fixed integer polynomial law. Reversibility does not imply exact physical energy conservation. |

These are original papers, with the cited equations/sections inspected; no abstract-only inference is used.

## 1. Finite pointwise functions have no nonzero ordinary derivation

Here is a short independent proof specific to the ordinary sampled algebra. Let `D` be linear over the scalar field on `A = R^N` (or `Q^N`) with pointwise multiplication and suppose

`D(f g) = (Df) g + f (Dg)` for every `f,g`.

For the site basis idempotent `e_j`, `e_j^2=e_j`, so

`D e_j = 2 e_j D e_j`.

Component `i` gives `(1-2 delta_ij) D_ij = 0`. Every coefficient is either +1 or -1. Thus every matrix entry is zero. No assumptions of translation invariance or nearest-neighbor support are needed for this *pointwise finite algebra* result. It is not the more general theorem for arbitrary products discussed in the papers.

Therefore no adjustment of the central-difference stencil can make a nonzero derivative obey the continuum product rule for **all** sampled fields with the same ordinary product. Refinement of a smooth family can still make the defect tend to zero.

There is an exact local replacement on an oriented face. With `E f_i=f_(i+1)` and `Delta=E-1`,

`Delta(fg) = (E f) Delta g + g Delta f`,

and equivalently

`2 Delta(fg) = (E f+f) Delta g + (E g+g) Delta f`.

Both expressions use one edge only. The second identity is written without a new division. Cubic products similarly obey

`Delta(fgh) = (E f)(E g) Delta h + (E f)h Delta g + gh Delta f`.

These identities suggest deriving geometric/source fluxes together using their discrete product algebra. They do not prove that the full Einstein constraints close. Researcher 2 supplies the separate flux and Einstein-specific review.

## 2. PR #47 denominator bit growth is intrinsic to that recurrence

The compiler uses `C >= 2`, degree `d in {2,3}`, `D_-1=0`, and `D_0>=2`:

`D_(n+1) = C D_n^d - D_(n-1)`.

Inductively, `0 <= D_(n-1) < D_n` and

`D_(n+1) >= D_n^d`.

Consequently

`D_n >= D_0^(d^n)`,

so its bit length is at least `floor(d^n log2(D_0))+1`. This is a proof for the implemented positive denominator sector, not merely a fit to eight updates. Reducing field amplitudes or changing diagnostics does not alter this lower bound. Delaying the same macro-update with a scheduler only reduces its rate per microtick; the bound remains per completed macro-update.

The recurrence must change to solve this cost problem. That means a new encoded physical integrator and a new convergence proof, rather than a behavior-preserving optimization of the existing retained integers.

## 3. The protecting Wronskian limits common-factor cancellation

Consider a protected pair governed by the same integer coefficient at each step:

`p_(n+1) = A_n p_n - p_(n-1)`,

`q_(n+1) = A_n q_n - q_(n-1)`.

Direct substitution proves that

`W_n = p_n q_(n-1) - p_(n-1) q_n`

is constant. For each time slice, `gcd(p_n,q_n)` divides `W_n`, because it divides both summands defining `W_n`. If the nonzero preparation invariant is `W_0`, every simultaneous divisor of the current protected pair is at most `abs(W_0)`. This also bounds a common divisor shared with other current numerators or the denominator. If `W_0=1`, no nontrivial current-pair gcd exists.

Thus the very invariant that prevents degeneration also prevents arbitrarily large common factors in that pair. One cannot presume that the enormous retained integers are merely redundant digits removable by a shared gcd. This does not forbid a different reversible representation, nor does it rule out special-sector normalization for which an explicit inverse is separately proved.

Unrecorded gcd normalization is noninjective on general legal state: `(a,b,r)=(2,4,0)` and `(4,8,0)` both become `(1,2,0)`. Retaining the lost scale can restore information in principle, but it must count toward the allocation and obey the same polynomial evolution. A passive reduced ratio is allowed and does not reduce the Engine's state cost.

## 4. A clock does not make arbitrary cubic gating free

Multiplying an arbitrary cubic force term `x*y*z` by a retained gate variable gives `gate*x*y*z`, of degree four. It violates the present degree-three contract. This excludes only the naive gate multiplication. It does **not** exclude a compiled clock using a different invariant encoding, factored intermediate channels or a longer algebraic schedule. Such a proposal needs a complete count and proof for its intermediate states.

The constructive candidate from researcher 1 is the existing Engine's exact native coordinate change:

`q=b`, `p=6(b-a)+r`.

For an admissible `b`-only force polynomial and `u=6q+F(q)`, direct algebra gives

`p_next=p+2F(q)`, `q_next=q+floor(p_next/6)`.

This has no extra retained coordinate: `(q,p)` determines `r=p mod 6` and `a=q-(p-r)/6`. It is a useful search space for a new integer local lift. It does not by itself solve arbitrary rational refinement, slow physical clocks, geometry positivity or Einstein constraints. Researcher 1 independently audits the identity and its integrality obstacles.

## Reproducible exact audit

Run:

```bash
python validation/research_eight/06_algebra_obstructions.py
```

The source-hashed output is `runs/research_eight/06_algebra_obstructions.json`.

| Control | Result | Scope |
| --- | --- | --- |
| Finite pointwise derivation equations for N=1,2,3,7,12 | Nullity zero in every case | Illustrates the proof; not numerical evidence substituted for a theorem |
| Shifted and polarized edge products on signed integer random fixtures | 2,200 exact checks; 2,078 matched ordinary-product failures | Exact algebraic positive/negative control |
| Eight genuine Engine cases: degrees 2/3, C=2/3, D0=2/5, eight updates each, 27 nodes | Independent scalar recurrence agrees; all six remainder classes retained; every inverse and full rewind exact | Three-channel denominator plus protected-pair toy; not coupled matter or GR |
| Denominator lower bound and pair Wronskian/gcd bound | Passed at every saved step; maximum retained size 20,433 bits | Demonstrates growth even when the decoded physical pair is simple |
| Unrecorded gcd collision | Found exactly | Refutes generic state normalization |
| Direct clock-gated cubic | Degree four | Fails that naive implementation; alternate compilations untested |

The toy tensor has three channels, nine retained integers per node, degree at most three, onsite support, no old-`a` inputs, and the original fixed-six Engine. It audits the cost obstruction; it is not appended to the 44-channel model.

## Recommendation and decisive next test

Develop a new denominator-free native local lift and a shift-compatible geometric/source flux algebra together. Keep their tests separate: the first must demonstrate long-duration bit cost and physical step refinement; the second must demonstrate a discrete constraint identity on arbitrary local data and convergence to the intended continuum equations. Then compile their composition with an exhaustive 48-channel schedule/ownership ledger.

Reject a candidate before broad physical tests if it relies on discarded scale, a runtime solve, diagonal reads, a quartic gated cubic, or an uncounted intermediate bank. Accepting the edge identities or the reversible lift is only an ingredient. General Einstein constraints, shared-metric apparatus and physical detector gates remain open.
