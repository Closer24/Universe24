# Born's square as an input (P10): what the six verbs select, what the register selects, and the one axiom that would make the selection the law's own (the open-problems physicist, read-only, 2026-09-21)

Problem (5) of the seven (record 393 of the log of 2026-09-20, on the
Boss's branch at the time of writing): "Born's square is an input (P10):
the quadratic-form classification needs added measurement axioms; no
derivation from the verbs". The order: can the six verbs select the
square, or only the classification under added axioms. Read against
`main` at be194aca: DERIVATIONS 6.2, 6.5 (the lattice Gleason), 6.7 (the
click without amplitudes), 24.1 row 12 and 24.3 rows 4 and 20, the
paper's postulate P10 ("one imported member of a derived family"), the
register's two-slit bands (record 156), Malus at 22.5 degrees (record
395, the engine's 219 / 256 and 187 / 256 exactly as pinned) and the
pair's 27, 5, 5, 27. Every number is from born_map.py (`docs/designs/open_problems/born/born_map.py`, deleted 2026-09-26)
beside this note (host arithmetic on the exact cosines at N = 64; the
built tables round at 1 / 256) and its output [born_map.out](born_map.out);
no run, nothing registered, nothing decided. Notation: **f** the
record's phase-count vector, `sigma_j(f)` its j-th Galois evaluation,
`c_j` the harmonic constants, **G** the click's Gram matrix, K(D) the
kernel for two rows at the phase difference D.

## 0. The verdicts, stated at the top

| Question | Verdict |
| --- | --- |
| Do the six verbs select the square's FORM (a positive quadratic form, the power 2, the multiplicity rule)? | **DERIVED** (6.5): the rotation, the balanced splitter's conservation for every two inputs and the counts force it; nothing added here |
| Do the six verbs select Born's MEMBER (`c_1 = 1`, the other `c_j = 0`) within the family? | **NOT REACHABLE from the verbs**: the family's constants are Gleason's free state, commuting with the rotation; the verbs are blind to them (6.5, confirmed here) |
| Is "which harmonic" a physical choice? | **NO**: for j coprime to N the map `p -> j p` is an automorphism of `Z_N`, so the j-th member is Born's under a relabelled phase rate; the physical content of P10 is "one harmonic, not a mixture" (section 2) |
| What selects one harmonic over a mixture? | **THE REGISTER** (the two-slit bands pin the fringe period `23.5 / j` to j = 1; Malus at 22.5 degrees, 219 / 256 and 187 / 256 engine-exact, excludes every mixture with weight off `j = +-1 mod 8`), and ONE AXIOM of the law's own kind, least cost: the click keeps one pointer per set, the Gram matrix of rank 2 (section 3) |
| So is P10 an import from quantum mechanics? | **ADMISSIBLE WITH CORRECTIONS**: it can be restated as the least-cost click (the minimal-rank admissible form), an axiom of the apparatus's storage of the same kind as the grains, not a law imported; the paper's sentence changes, the physics does not |

## 1. The pins, before any number

- **The theorem** (6.5): on `Z[zeta_N]` with N a power of two, under the
  phase rotation, the balanced splitter's conservation and the counts,
  `R(f) = sum over odd j < N / 2 of c_j |sigma_j(f)|^2`, `c_j >= 0`: at N =
  64 sixteen free constants (the map's section A). Born's member is `c_1
  = 1`, the rest 0. The flat mixture (every `c_j` equal) is `sum f_p^2`
  on the reduced basis, phase-blind.
- **The register.** The two-slit bands of record 156: the kernel `cos(2
  pi D / 64)` at 64 steps per 23.5 pixels, the bands at y = 35 .. 38,
  59 .. 61, 82 .. 85 (a GameBoard reading of the crowd form, kept as the
  pin of the harmonics, 6.5). Malus at 22.5 degrees (record 395, the
  auditor's round 10 on the shipped worlds, DETECTOR): one polariser 219
  / 256 = 0.8555 (nature's `cos^2` 0.8536), the chain 187 / 256 = 0.7305
  (0.7286): 24.3 row 4's numbers, the engine's exactly. Every
  Mach-Zehnder and pair world: blind to the harmonics (D in {0, 16, 32}).
- **What must not move.** The theorem's hypotheses (a) to (e) and the
  registered integers.

## 2. Theorem: the verbs classify; the member is a relabelling; the mixture is the physical alternative

**On the GameBoard.** A record's rows at one Node and label are the
integer vector **f** (the amount at each phase of the circle `Z_N`).
The click's weight is one bilinear form `f^T G f` (note 37 (xii)); the
theorem says which **G** are admissible: those commuting with the
rotation (the shift of the phases), positive, and zero on the antipodal
pairs. Such a **G** is diagonal on the Galois planes (the pairs of
Fourier modes `+-j`), with one non-negative constant per odd j: the
family. The verbs, as declared, never read the constants: the evaluation
verb evaluates at the declared root of unity (the tables C and S), the
tables are declared at the scale 256, and nothing on the GameBoard forms
a product across phases (record 170: "the merge adds only identical
rows"); so no verb prefers j = 1 to j = 3, or one harmonic to two. This
is 6.5's "not reached from the algebra", and the map's section A shows
the members side by side: each single member is a cosine kernel of a
different period, the flat mixture the comb `[D = 0] - [D = 32]`.

**The relabelling** (section C of the map). For j coprime to N (every
odd j at N a power of two), `p -> j p mod N` is a bijection of `Z_N`;
under it the j-th member reads exactly as Born's reads under the
declared rate `n / d` replaced by `j n / d`. A world declared with the
member j and the rate `n / d` is a world declared with Born's member
and the rate `j n / d`: the same law, one declaration relabelled. So the
choice of j is not physics; what is physics is whether the click's form
has ONE Galois plane or several. Two rows at a phase difference D then
read `2 a b K(D)` with K a single cosine (one plane) or a sum of cosines
(several): the visibility of every fringe and the cross term of every
pair are the sum's shape. The flat mixture, all planes at one weight,
is the reading that squares each phase's amount and never crosses
phases: no fringe, no pair correlation above the classical, the
classical mixture. Born's member is the maximally coherent extreme of
the cone; the mixtures interpolate to the classical.

**What the register says of the mixture** (section B of the map). Malus
at 22.5 degrees: a member j reads `cos^2(j pi / 8)`, 0.8536 for `j = +-1
mod 8` and 0.1464 for `j = +-3 mod 8`, the flat mixture 1 / 2; the
registered 219 / 256 = 0.8555 admits j = 1, 7, 9, 15 and excludes j = 3,
5 and every mixture with a visible weight on them; at 45 and 90 degrees
every member reads 1 / 2 and 0 (NATURE row 9 tests nothing of the
harmonics). The two slits: the member j has the fringe period `23.5 / j`
pixels, 7.8 at j = 3 and below a pixel from j = 9; the registered bands
at 23.5 pixels admit j = 1 alone among the single members and exclude
every mixture with a visible second period. Together the register
pins one plane, the fundamental, to its brackets, which is what 6.5
says and what the paper's P10 imports.

## 3. Theorem: the least-cost admissible click is one harmonic

**On the GameBoard.** The click without amplitudes keeps the count
vector **f** and evaluates `f^T G f` through **G**'s factorisation `E^T
E`, the pointer **E f** a 2-vector per set (X, Y). A member j alone has
`G_j = E_j^T E_j` of rank 2 (the map's section D: rank 2 for j = 1 and
for j = 3); k members have rank `2 k`; the flat mixture has rank N / 2 =
32 (the projector on the odd subspace). The cost of the click is the
rank: 2 k products per row and 2 k integers of pointer per set
(LOCALITY-1's fixed storage, section 13's count K). So among the
admissible forms the least computation is one Galois plane, rank 2, one
pointer: the click as built, Born's member up to the relabelling of
section 2. The statement "the click keeps one pointer per set" is an
axiom of the apparatus of the same kind as the grains (P7: the circle,
the tables' scale, the wheel): a declared bound on the detector's
storage, not a law of nature imported. Under it Born's rule follows from
6.5's theorem with no free constant left: the form from the verbs and
the splitter, the member from the least storage.

**What this does and does not give.** It gives the paper a sentence in
which P10 is not an import: "the click's weight is the least-rank
positive form commuting with the rotation (one pointer per set), which
by Theorem (6.5) is one harmonic; which harmonic is a relabelling of the
declared rate". It does not make Born's rule a theorem of the six verbs
alone: the least-cost axiom is added, and it is of the same standing as
the other grains. It is, however, the axiom the law already lives by
(the three tests give the least computation, the workflow's own
statement, record 206): the click with one pointer is what every
registered world runs.

## 4. What each reading gives for the register, and a pin

| Reading | Born's member (one plane, as built) | a mixture (two or more planes) | the flat mixture |
| --- | --- | --- | --- |
| the two-slit bands (record 156) | the period 23.5 pixels, registered | a second period `23.5 / j` visible in the bands: excluded | no bands: excluded |
| Malus at 22.5 degrees (record 395) | 219 / 256 and 187 / 256, engine-exact against `cos^2` and `cos^4` | between 0.15 and 0.85 by the weights: excluded above the bracket | 128 / 256: excluded |
| the pair at the CHSH settings (D = 16) and every Mach-Zehnder (D in {0, 16, 32}) | 27, 5, 5, 27; 64 / 0; 32 / 32 | the same: blind | the same: blind |
| the pair at a setting pair OFF the grid (D = 4, say) | `E = cos(2 pi D / N)` to the rung | `sum c_j cos(2 pi j D / N)`: a different E | 0 |

**The pin that would test a mixture where the register is blind** (for
the Boss, if a reading beyond the two slits and Malus is wanted; no run
is needed for this note's verdicts): the Bell pair at the settings (0,
4) and (0, 2) on the 64-circle (D = 4 and 2), DETECTOR: the counts by the
rungs of `cos^2(pi D / 64)`: at D = 4, `E = cos(pi / 8) = 0.924`, the
cells 31, 1, 1, 31 (E = 60 / 64 = 0.9375); at D = 2, `E = cos(pi / 16) =
0.981`, the cells 32, 0, 0, 32 (E = 1 by the rung); a member j = 3 would
read `cos(3 pi / 8) = 0.383` and `cos(3 pi / 16) = 0.831` at the same
settings. The pair worlds exist (`examples/events/bell/`), the settings a
declaration; a run of seconds.

## 5. The owner's question on the conditional derivations, for this problem

- **Is Born's rule derivable from the six verbs?** Its form, yes (6.5,
  a theorem, unconditional). Its member, no: the verbs are blind to the
  harmonic constants, proved by the theorem's own freedom; what selects
  the member is the register (two readings, both registered) or the
  least-cost axiom (section 3), which is the law's own kind of axiom.
- **What a derivation of the member would take**: a rule of the six that
  reads a product across phases at the GameBoard, which record 170
  forbids (the merge adds only identical rows), or a principle of the
  apparatus (the least-cost click). The second exists and is stated
  here; the first would change the law.
- **Can the paper stand with P10 as an input?** Yes, as it stands; and
  better with the restatement: "the one imported member" becomes "the
  least-rank member, one pointer per set, an axiom of the apparatus like
  the grains; which harmonic is a relabelling". Both are honest; the
  second says what the import is.

## 6. Proposed lines for the documents I do not write

- **The paper, P10** (the coordinator): "The click's weight is forced to
  the family `sum_j c_j |sigma_j(f)|^2` (Theorem); the member with one
  Galois plane (one pointer per set, the least rank) is the click as
  built, Born's; which plane is a relabelling of the declared rate; the
  register pins the fundamental by the two-slit bands and Malus at 22.5
  degrees. The one axiom beyond the theorem is the least-rank click, of
  the grains' kind."
- **DERIVATIONS_BEAM 6.5, the verdict** (the mathematician): after "not
  reached from the algebra: the harmonic constants": "a single harmonic
  is Born's member under the relabelling `p -> j p`; a mixture is the
  physical alternative, excluded by the register; the least-rank
  admissible form is one plane (the open-problems note on Born, section
  3)".
- **DERIVATIONS_BEAM 24.1 row 12** (the same): the label "`c_1 = 1` a
  POSTULATE" to read "one Galois plane a POSTULATE of the apparatus's
  storage (the least-rank click); `c_1` against `c_j` a relabelling".
- **NATURE.md row 9** (the physicist): "Malus at 22.5 degrees, run
  (record 395): 219 / 256 against `cos^2` 0.8536, PASS at the tables'
  scale; it pins the click's harmonic to `j = +-1 mod 8`".
- **HIGHLIGHTS 5.4**: nothing.

## 7. Questions, through the Boss

1. **For the owner (substantive)**: whether the paper's P10 is restated
   as section 6's sentence (an axiom of the apparatus's storage in place
   of an import). The physics does not change; the claim's standing does.
2. **For the Boss**: the off-grid pair pin of section 4 is available if
   a third reading of the harmonics is wanted; not needed.

## 8. Links

[DERIVATIONS_BEAM 6.5](../../../DERIVATIONS_BEAM.md#65-the-uniqueness-of-the-clicks-square-a-lattice-gleason),
[6.7](../../../DERIVATIONS_BEAM.md#67-the-click-without-amplitudes-one-bilinear-form-on-the-records-integer-vector),
[24.1](../../../DERIVATIONS_BEAM.md#241-the-inputs-ledger-every-place-physics-enters-the-law) row 12,
[24.3](../../../DERIVATIONS_BEAM.md#243-the-delta-p-table-every-computable-difference-from-quantum-mechanics-or-relativity-as-the-law-is-declared) rows 4 and 20;
[BEAM_LAW note 37](../../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) (xii);
[the Malus note](../../malus/NOTE.md); [NATURE](../../../NATURE.md) rows 2c and 9;
[the three tests](../../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).

> The scripts of this folder (`born_map.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/open_problems/born/<script>`).
