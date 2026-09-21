# Precedents: how the great papers state a new formula, recover the old ones, mark their inputs and meet experiment

Research note for the model owner's order of 2026-09-21. Repository unchanged. Paper read: paper/general_formula/main.tex (3316 lines at HEAD d663b2e3) and
PLAN.md.

## Scope and method

- The egress proxy blocks fourmilab.ch, wikisource, archive.org, arxiv, gutenberg, the Royal Society, plato.stanford and every university host tried. Primary
  texts were read from GitHub-hosted transcriptions (raw.githubusercontent.com is open) and are saved beside this note.
- Quotations are verbatim from the text read (typographic quotes and dashes made ASCII; a formula the transcription lost is in [brackets]). Where only a
  search snippet was readable the block says SECONDARY and its wording is a paraphrase unless quoted from the snippet. jundalisay/sp ("Superphysics") is
  verbatim for Newton's Phenomena and Scholium, Maxwell, Planck, Boltzmann and Schrodinger; its Newton "Rules" and Poincare files are edited renderings,
  marked so.

## PART A: the papers

Each block: (1) the new formula and how newness is said; (2) known formulas recovered and the words; (3) inputs and how marked; (4) any claim of a known
formula as own; (5) experiment.

### A1. Newton 1687, Principia Book III (Motte 1846 text; newton_phenomena.md, newton_scholium.md)
(1) Universal gravitation from the Phenomena by the Rules; newness is not proclaimed. The Scholium: "Hitherto we have explained the phenomena of the heavens
    and of our sea by the power of gravity, but have not yet assigned the cause of this power."
(2) Kepler's third law enters as Phenomenon IV, an input: "the periodic times of the five primary planets ... are in the sesquiplicate proportion of their
    mean distances from the sun." The credit form: "This proportion, first observed by Kepler, is now received by all astronomers". (Orbits from the inverse
    square are Book I, not read here.)
(3) Rules and Phenomena stand before any proposition, the observers named and their numbers tabled: "Cassini from his own observations has determined",
    "Kepler and Bullialdus, above all others, have determined them from observations with the greatest accuracy". Rule I (SECONDARY, Wikipedia "General
    Scholium"): "We are to admit no more causes of natural things than such as are both true and sufficient to explain their appearances."
(4) Never; a name plus "first observed by" plus "received by all astronomers". (5) A table of observations per phenomenon; the gap admitted in the same book
    (SECONDARY wording): "I have not been able to discover the cause of those properties of gravity from phenomena, and I frame no hypotheses".

### A2. Maxwell 1865, A Dynamical Theory of the Electromagnetic Field (maxwell/part-*.md, paragraphs numbered)
(1) "(3) I propose a dynamical theory of the Electromagnetic Field." The light conclusion hedged: "This velocity is so nearly that of light, that it seems we
    have strong reason to conclude that light itself ... is an electromagnetic disturbance ... propagated through the electromagnetic field according to
    electromagnetic laws." (para 20)
(2) "the laws of Ampere relating to the attraction of conductors carrying currents, as well as those of Faraday about the mutual induction of currents, might
    be deduced by mechanical reasoning."
(3) Rivals judged by name (Weber and Neumann's theory "is ingenious and comprehensive"); his own quantity identified with Faraday's: "What I have called
    electromagnetic momentum is the same quantity which is called by Faraday[4] the electrotonic state"; inputs listed: "(75) The conclusions arrived at in
    the present paper are independent of this hypothesis, being deduced from experimental facts of three kinds:"; "(73) ... In the present paper I avoid any
    hypothesis of this kind". (4) Never.
(5) Numbers with their authors: Weber and Kohlrausch v = 310,740,000 m/s; "The velocity of light in air, by M. Fizeau's[2] experiments, is V = 314,858,000;
    according to the more accurate experiments of M. Foucault[3] V = 298,000,000"; "(97) Hence the velocity of light deduced from experiment agrees
    sufficiently well with the value of v deduced from the only set of experiments we as yet possess."

### A3. Boltzmann 1877 (Sharp and Matschinsky translation, transcribed in boltzmann_ch01.md; opening part)
(1) "the number P ... is the desired measure of the permutability of the corresponding distribution of states." Newness placed as continuity with his own
    work, cited by title: "The relationship between the second fundamental theorem and calculations of probability became clear for the first time when I
    demonstrated that ... (I refer to my publication 'Analytical proof of the second fundamental theorem ...')".
(2) SECONDARY: Maxwell's distribution returns as the most probable one. (3) The discretisation declared a device: "This assumption does not correspond to any
    realistic mechanical model, but it is easier to handle"; borrowed steps: "The total number of permutations is well known". (4) Never. (5) No number in the
    part read.

### A4. Planck, 14 Dec 1900 (planck_p1-3.md; the 1901 Annalen paper repeats the derivation and the constants)
(1) "The whole deduction is based upon the single theorem that the entropy of a system of resonators with given energy is proportional to the logarithm of the
    total number of possible complexions"; "We use the constant of nature h = 6.55 x 10^-27 erg sec." His own earlier idea is "my hypothesis of natural
    radiation".
(2) "the extremely important so called Wien displacement law" used; Wien's formula "not confirmed by experiment". (The Wien-limit sentence of the 1901 paper
    was not readable here.)
(3) By name: "Boltzmann* has shown that the entropy of a monatomic gas in equilibrium is equal to omega R ln P0"; "The importance of this for the second law
    of thermodynamics* was originally discovered by Mr. L. Boltzmann."; "R is the well known gas constant". (4) Never.
(5) Constants fitted from named measurements with journal and page: "F. Kurlbaum (Ann. Phys. 65 [= 301], 759 (1898)) gives S100 - S0 = 0.0731 Watt cm^-2,
    while O. Lummer and E. Pringsheim (Verh. Deutsch. Physik Ges. 2, 176 (1900)) give lambda_m T = 2940 mu degree." Derived numbers set beside others': e =
    4.69 x 10^-10 e.s.u. against "Mr. F. Richarz finds 1.29 x 10^-10 and Mr. J. J. Thomson recently 6.5 x 10^-10"; the standard: "If the theory is at all
    correct, all these relations should be not approximately, but absolutely valid."; the weakest link named: "the relatively worst known, the radiation
    constant k".

### A5. Lorentz 1904 (SECONDARY: primary blocked; search snippets; Poincare 1906's introduction in an edited rendering)
(1) The transformation and the deformable electron with two masses (paraphrase). (2) Michelson's null result via the contraction (paraphrase); Poincare's
    rendering: "My results are in agreement with those of Lorentz on all important points." and "Is there a law which satisfies the condition imposed by
    Lorentz, and which at the same time is reduced to Newton's law when the speeds of the stars are slow?" (3) Hypotheses stated as such. (4) Never
    (SECONDARY).
(5) Kaufmann's data, the incompleteness admitted (snippet, Wikipedia "Kaufmann-Bucherer-Neumann experiments"): "I have not found time for calculating the
    other tables in Kaufmann's paper." and "We may expect a satisfactory agreement with my formulae." Poincare's rendering: "These 2 hypothesis are in
    agreement with the experiments of Kaufmann, as well as the original hypothesis of Abraham".

### A6. Einstein 1905a, On the Electrodynamics of Moving Bodies (1923 translation; einstein1905_sr.txt)
(1) "We will raise this conjecture (the purport of which will hereafter be called the 'Principle of Relativity') to the status of a postulate, and also
    introduce another postulate ... that light is always propagated in empty space with a definite velocity c which is independent of the state of motion of
    the emitting body. These two postulates suffice for the attainment of a simple and consistent theory of the electrodynamics of moving bodies based on
    Maxwell's theory for stationary bodies." The own result is "by the theory here advanced"; W = mc^2(1/sqrt(1 - v^2/c^2) - 1).
(2) Section 7 "Theory of Doppler's Principle and of Aberration" (derived, named); section 8: "In agreement with experiment and with other theories, we obtain
    to a first approximation P = ..."; section 9: "the electrodynamic foundation of Lorentz's theory of the electrodynamics of moving bodies is in agreement
    with the principle of relativity." NOTE: section 10 does not say the kinetic energy "reduces to" the classical one; it says "Thus, when v = c, W becomes
    infinite. Velocities greater than that of light have - as in our previous results - no possibility of existence." and "these results as to the mass are
    also valid for ponderable material points"; the low-speed comparison is in A7. Footnote 9 carries a later admission: "The definition of force here given
    is not advantageous, as was first shown by M. Planck."
(3) "the same laws of electrodynamics and optics will be valid for all frames of reference for which the equations of mechanics hold good"; "Maxwell's
    electrodynamics - as usually understood at the present time". No bibliography; names only (Maxwell, Hertz, Lorentz, Doppler, Newtonian). Editorial
    footnote: "The preceding memoir by Lorentz was not at this time known to the author."
(4) Never. (5) No measured number; predictions offered: "the properties of the motion of the electron which result from the system of equations (A), and are
    accessible to experiment"; Besso thanked for "several valuable suggestions".

### A7. Einstein 1905b, Does the Inertia of a Body Depend Upon Its Energy-Content? (einstein1905_emc2.txt)
(1) "If a body gives off the energy L in the form of radiation, its mass diminishes by L/c^2." and "The mass of a body is a measure of its energy-content";
    introduced as "a very interesting conclusion, which is here to be deduced" from "the previous investigation".
(2) The classical form at low speed, the "reduces to" step: "Neglecting magnitudes of fourth and higher orders we may place K0 - K1 = (1/2)(L/c^2) v^2."
(3) "I based that investigation on the Maxwell-Hertz equations for empty space, together with the Maxwellian expression for the electromagnetic energy of
    space, and in addition the principle that ... (principle of relativity)."; footnote: "The principle of the constancy of the velocity of light is of course
    contained in Maxwell's equations."; own earlier result cited by section, "(section 8)".
(4) Never. (5) A test proposed, no number: "It is not impossible that with bodies whose energy-content is variable to a high degree (e.g. with radium salts)
    the theory may be successfully put to the test."; the conditional close: "If the theory corresponds to the facts, radiation conveys inertia between the
    emitting and absorbing bodies."

### A8. Bohr 1913, On the Constitution of Atoms and Molecules, Part I (bohr1913.txt)
(1) "The principal assumptions used are: (1) That the dynamical equilibrium of the systems in the stationary states can be discussed by help of the ordinary
    mechanics, while the passing of the systems between different stationary states cannot be treated on that basis. (2) That the latter process is followed
    by the emission of a homogeneous radiation, for which the relation between the frequency and the amount of energy emitted is the one given by Planck's
    theory." Hedge: "The preliminary and hypothetical character of the above considerations needs not to be emphasized."
(2) "We see that this expression accounts for the law connecting the lines in the spectrum of hydrogen. If we put [tau2 = 2] ... we get the ordinary Balmer
    series. If we put [tau2 = 3], we get the series in the ultra-red observed by Paschen[11] and previously suspected by Ritz."; Rydberg's constant "a
    universal constant, equal to the factor outside the bracket in the formula (4)".
(3) Numbered references; "Prof. Rutherford[2] has given a theory of the structure of atoms"; "Planck's constant, or as it often is called the elementary
    quantum of action"; thanks to Rutherford. (4) Never.
(5) "The agreement in question is quantitative as well as qualitative. Putting [e = 4.7 x 10^-10, e/m, h] we get [3.1 x 10^15]. The observed value for the
    factor outside the bracket in the formula (4) is [3.290 x 10^15]." then "The agreement between the theoretical and observed values is inside the
    uncertainty due to experimental errors in the constants entering in the expression for the theoretical value." The miss in the same section: "It will be
    observed that we in the above way do not obtain other series of lines, generally ascribed to hydrogen; for instance, the series first observed by
    Pickering[12] ... and the set of series recently found by Fowler[13]".

### A9. Einstein 1916, The Foundation of the General Theory of Relativity (Bose 1920 translation; einstein1916.wiki)
(1) "The theory which is sketched in the following pages forms the most wide-going generalization conceivable of what is at present known as 'the theory of
    Relativity'".
(2) Sec. 21 "Newton's Theory as a First Approximation": "This is the equation of motion of a material point according to Newton's theory, where g44/2 plays
    the part of gravitational potential."; "The equations (67) and (68) together, are equivalent to Newton's law of gravitation."; "the special relativity
    theory is to be looked upon as a special case of the general, in which g_mu_nu have constant values"; sec. 14: the equations "give us the Newtonian law of
    attraction as a first approximation, and lead in the second approximation to the explanation of the perihelion-motion of mercury discovered by Leverrier".
(3) Minkowski "was the first to recognize clearly the formal equivalence of the space like and time-like co-ordinates"; the calculus "based on the researches
    of Gauss, Riemann and Christoffel ... shaped into a system by Ricci and Levi-Civita"; "the well-known law of Determinants"; footnote "That the
    gravitational field has this property with great accuracy, was confirmed by Eotvos by experiment."; Grossmann thanked. (4) Never.
(5) "The calculation gives for the planet Mercury, a rotation of path of amount 43'' per century, corresponding sufficiently to what has been found by
    astronomers (Leverrier). They found a residual perihelion motion of this planet of the given magnitude which can not be explained by the perturbation of
    the other planets."; "A ray of light just grazing the sun would suffer a bending of 1,7''"; the red shift with its gap in a footnote: "In support of the
    existence of such an effect we can allude to the spectral observations on fix-stars according to E. Freundlich. However, a concluding examination of that
    consequence is still missing." The popular book, Appendix 3 (rendering): "If the displacement of spectral lines towards the red by the gravitational
    potential does not exist, then the general theory of relativity will be untenable."

### A10. de Broglie 1924, thesis (SECONDARY: PDF blocked; snippets; Schrodinger 1926's words are primary)
(1) The phase wave (paraphrase). (2) Bohr's condition as resonance; snippet: "the motion (of an electron) can only be stable if the phase wave is tuned with
    the length of the path". (3) Planck, Einstein, Bohr, Sommerfeld by name (paraphrase). (4) Never. (5) No measurement then. Schrodinger 1926 on him: "I owe
    the stimulation to these reflections in the first place to the brilliant thesis of Mr. Louis de Broglie20) ... for which he has shown that always an
    integer number of them, measured along the trajectory, are allotted to each period or quasiperiod of the electron."

### A11. Heisenberg 1925 (SECONDARY: snippets quoting the paper; APS News, Europhysics News)
(1) Abstract: "The present paper seeks to establish a basis for theoretical quantum mechanics founded exclusively upon relationships between quantities which
    in principle are observable". (2) The anharmonic oscillator and the rotator recomputed. (3) Kramers, Born, Bohr's correspondence principle by name. (4)
    Never. (5) The closing admission: "Whether a method to determine quantum-theoretical data using relations between observable quantities, such as that
    proposed here, can be regarded as satisfactory in principle, or whether this method after all represents far too rough an approach ..., can be decided
    only by a more intensive mathematical investigation of the method which has been superficially employed here."

### A12. Schrodinger 1926, Quantisation as an eigenvalue problem, first communication (schrodinger/part-1*.md)
(1) "In this communication I would like first to show, in the simplest case of the (non-relativistic and unperturbed) hydrogen atom, that the usual
    prescription for quantisation can be substituted by another requirement in which no word about 'integer numbers' occurs anymore. Rather, the integerness
    emerges in the same natural way as, for example, the integerness of the number of knots of a vibrating string. The new interpretation is generalisable and
    touches, as I believe, very deeply the true essence of the quantisation prescription."
(2) "The discrete spectrum corresponds to the Balmer terms"; "Therefore, the well-known Bohr energy levels, which correspond to the Balmer terms, arise when
    one assign to the constant K, which we had to introduce in (2) for dimensional reasons, the value ..."; "It provides an understanding for Bohr's condition
    on the frequency."
(3) "the Hamiltonian function of the Keplerian motion"; de Broglie (A10) and "Einstein's theory of gas" by name with references; "as it is well-known" twice.
    (4) Never. (5) The constant fixed to the data: "In order for numerical agreement to exist, K ..."; the weak step admitted: "It might raise concerns that
    these conclusions are based on the relation (22) in its approximated form ... However, that is only apparent".

### A13. Dirac 1928, The Quantum Theory of the Electron (dirac1928.txt; the transcription ends after sec. 4)
(1) "It appears that the simplest Hamiltonian for a point-charge electron satisfying the requirements of both relativity and the general transformation theory
    leads to an explanation of all duplexity phenomena without further assumption."
(2) "The electron will therefore behave as though it has a magnetic moment (eh/2mc) sigma ... This magnetic moment is just that assumed in the spinning
    electron model."; "All the same there is a great deal of truth in the spinning electron model, at least as a first approximation."; "This model for the
    electron has been fitted into the new mechanics by Pauli, and Darwin, working with an equivalent theory, has shown that it gives results in agreement with
    experiment for hydrogen-like spectra to the first order of accuracy."
(3) "It has been suggested by Gordon that the operator of the wave equation ..."; "Gordon, and also independently Klein"; the matrices "which Pauli
    introduced"; references by journal, volume and page. (4) Never.
(5) The opening is a measured failure of the old theory: "The new quantum mechanics, when applied to the problem of the structure of the atom with
    point-charge electrons, does not give results in agreement with experiment." The own gap: "The wave equation thus refers equally well to an electron with
    charge e as to one with charge -e." ... "The resulting theory is therefore still only an approximation, but it appears to be good enough to account for
    all the duplexity phenomena without arbitrary assumptions."

### A14. Feynman 1948, Space-Time Approach to Non-Relativistic Quantum Mechanics (SECONDARY: snippets)
(1) Abstract: "Non-relativistic quantum mechanics is formulated here in a different way. It is, however, mathematically equivalent to the familiar
    formulation." (2) Schrodinger's equation and the classical limit recovered; "There is a pleasure in recognizing old things from a new point of view." (3)
    Dirac's exp(iS/hbar) remark credited by name. (4) Never. (5) No measurement; equivalence is the claim.

## PART B: the pattern the great papers share

1. The inputs are written first and are few: two postulates (Einstein 1905a), two assumptions (Bohr), Rules and Phenomena with the observers' tables (Newton),
   "experimental facts of three kinds" (Maxwell).
2. The new law is stated in the author's voice and hedged in the same breath: "I propose", "the theory here advanced", "In the present paper it is shown", "it
   seems ... strong reason", "as I believe".
3. The old laws follow, each named with its author and a plain verb: "first approximation", "equivalent to Newton's law", "accounts for the law connecting the
   lines", "the well-known Bohr energy levels ... arise", "just that assumed in the spinning electron model", "Neglecting magnitudes of fourth and higher
   orders", "first observed by Kepler", "agrees sufficiently well".
4. Borrowed steps carry a name, usually with journal and page (Bohr, Dirac, Planck), or "as is well known" / "the well-known" for textbook facts (Einstein
   1916, Planck, Boltzmann, Schrodinger).
5. Experiment is whose measurement, which number, with the uncertainty; agreement is said in measured words ("inside the uncertainty", "agrees sufficiently
   well", "corresponding sufficiently").
6. The miss and the untested consequence stand in the same paper, in one or two sentences with the cause named (Bohr's Pickering lines, Einstein's red shift
   "still missing", Dirac's second difficulty, Lorentz's "not found time", Planck's spread of e, Heisenberg's closing doubt).
7. No great claims a known formula; the novelty claimed is the mechanism, and a reformulation says so ("mathematically equivalent").
8. Own earlier work is cited by section or paper; helpers are thanked by name (Besso, Grossmann, Rutherford).

## PART C: our paper against the pattern

(a) Derived and marked. The standing column (DERIVED / HYPOTHESIS / POSTULATE / INPUT / DIFFERENT / NOT REACHED / OPEN) of Table tab:consequences, the four
    labels (measured, proved, assumed, open) per claim, the Method paragraph and the appendix record mark what is derived from Eq. (1) and what is not: the
    pattern's items 1 and 3 made explicit; nothing in the greats contradicts it.

(b) Known formulas and their credit. The paper credits textbook laws by eponym without a citation (Newton, Coulomb, Gauss, Poisson, Doppler, Kepler, Young,
    Malus, Compton, Bradley, Hubble, Milne, Fraunhofer, Fresnel) and the founders by name, year and bibitem (Planck 1901, Einstein 1905, Bohr 1913, de Broglie
    1924, Heisenberg 1925, Born-Jordan 1925, Schrodinger 1926, Born 1926, Heisenberg 1927 with Kennard 1927, Dirac 1928, Bell 1964, Tsirelson 1980, Gleason
    1957, Jordan-von Neumann 1935, Donoho-Stark 1989, Maassen-Uffink 1988, Weyl 1931, Schwinger 1960, CFL 1928): the greats' two registers (Einstein 1905a
    names without pages; Bohr and Dirac cite pages). Places to fix:
  1. Figure fig:square (sec:lorentz), "Einstein, 1905: E^2 = E_0^2 + p^2c^2". Neither 1905 paper contains that equation: 1905a gives W = mc^2(1/sqrt(1
     - v^2/c^2) - 1) and the two masses, 1905b gives L/c^2. Write "the energy-momentum relation of special relativity" (no year), or credit the quadratic form
       to the four-vector formulation with a source the paper has read.
  2. The same caption's "the continuum form is a corollary of the integer one" can be heard as priority over the known relation; the greats' verb is "gives
     ... exactly" / "is equivalent to" (see (c)).
  3. Eponyms with no source a referee may not know: "Jefimenko's retarded fields" (tab:recordc), "the Bresenham deficits" (tab:recorda), "Landauer's bound",
     "Shannon's H". The greats leave textbook names uncited, but the paper's own standard (a bibitem for every founder) makes the asymmetry visible: add
     one-line bibitems (Shannon 1948, Landauer 1961, Bresenham 1965, Jefimenko 1966) or drop the eponym.
  4. Nothing else reads as a claim of a known formula: the abstract's "From this law ... follow: Gauss's law exactly, Newton's and Coulomb's inverse square
     ..." is Einstein 1916 sec. 14's form; "Newton and Coulomb from the bilinear coupling" is "Newton's Theory as a First Approximation"; sec:qm's "Nothing
     here claims that the law is quantum mechanics" is Feynman's form; the lattice Gleason says what Gleason's theorem needs and this one does not (line
     1241), Dirac's form.

(c) "Contains and extends": the precedents and their words, for W_E = E'_0^2 + 3 p.p against E^2 = E_0^2 + p^2c^2.
  - Einstein 1916 over Newton: "give us the Newtonian law of attraction as a first approximation"; "This is the equation of motion of a material point
    according to Newton's theory"; "equivalent to Newton's law of gravitation"; the old theory "a special case of the general".
  - Einstein 1905b over Newton's kinetic energy: "Neglecting magnitudes of fourth and higher orders we may place K0 - K1 = (1/2)(L/c^2) v^2".
  - Dirac over Pauli: "This magnetic moment is just that assumed in the spinning electron model."; "a great deal of truth in the spinning electron model, at
    least as a first approximation."
  - Schrodinger over Bohr: "the well-known Bohr energy levels ... arise when one assign to the constant K ... the value"; "It provides an understanding for
    Bohr's condition on the frequency."
  - Bohr over Balmer and Rydberg: "this expression accounts for the law connecting the lines in the spectrum of hydrogen"; de Broglie over Bohr (SECONDARY):
    the stability condition is the resonance condition.
  The form of words for fig:square, in that pattern: "In the units c^2 = 1/3 the exact square gives the energy-momentum relation of special relativity, E^2 =
  E_0^2 + p^2c^2, exactly, E' being its integer root to the remainder; the relation is not new, and the identity's own content is the integer form, in which
  the departure from the known relation is the rounding of E', one part in E'_0, a row a measurement can refute." The status sentence already there ("a
  hypothesis, not built") is Dirac's "still only an approximation" and stays.

(d) What none of the greats did, the nearest precedent, the verdict.
  - A ledger of inputs (P1 to P10, "What is not in this list is not assumed"). Precedent in kind, not in length: two postulates, two assumptions, Rules plus
    Phenomena, three kinds of facts. Strength; keep, and say in one sentence before the list which four do the work (P1, P4, P6, P10).
  - A confrontation table with FAIL rows (twelve of twenty-one). Precedent for admitting a miss in the paper: Bohr, Einstein 1916, Dirac, Lorentz, Planck,
    Heisenberg, each one or two misses in prose with the cause; no great tabulated failures. Strength for candour, a deviation in proportion: the abstract's
    "four pass, twelve fail" without the cause reads as a refuted theory, where sec:nature's prose sorts the twelve by cause (the law, a declared input, a
    hypothesis). Carry that sorting into the abstract in one clause.
  - A table of refutable predictions with today's bounding experiment (tab:differs) and "the one prediction" (181/64). Precedent: Einstein 1916 sec. 22 (three
    numbers, the astronomers named), 1905a's "accessible to experiment", 1905b's radium salts, the popular book's "will be untenable". Strength; the greats
    give one to three, so the one prediction stays first.
  - A derivation record with commit SHAs and fingerprints. No precedent among the greats; the nearest is Planck's citation of each measurement by journal and
    page, Newton's observers and instruments, Einstein's footnote to his own 1915 paper and Schwarzschild. Keep the record; soften its placement: SHAs belong
    in Reproducibility and the appendix, not in captions (tab:nature's caption carries five) or in Part II's running text.

(e) What the greats did that the paper does not yet.
  - One sentence in the author's voice that names the newness and hedges it ("the theory here advanced", "it seems", "as I believe"); the Introduction has
    "One law" and "Method" but no such sentence.
  - Where a known formula is reached in prose (sec:newton, sec:delay, sec:gleason, sec:qm), the greats end with the measured number and the experimenter's
    name, then the gap; the paper puts its numbers in register series and the nature number only in tab:nature. Give one nature number with its author in each
    such section (Bohr's 3.1 against 3.290; Maxwell's four velocities).
  - "As is well known" for a borrowed textbook step (the Courant bound, the Fraunhofer constant, Kennard's form): the paper never uses the phrase; the greats
    use it to mark the step as not theirs.
  - The admitted gap as one sentence at the end of the section that reaches the formula (Einstein's red-shift footnote, Bohr's "we do not obtain"); the
    paper's gaps sit in tables and its prose sections end on the result.

## PART D: verdict

1. KEEP the ledger of inputs (sec:law), the standing column and four labels (sec:table), the one prediction (sec:differs) and the not-claimed list
   (sec:notclaimed): they are the greats' items 1, 3, 5 and 6 made explicit, and no great contradicts them.
2. CHANGE fig:square (sec:lorentz): "Einstein, 1905: E^2 = E_0^2 + p^2c^2" is not in either 1905 paper; write "the energy-momentum relation of special
   relativity", and replace "the continuum form is a corollary of the integer one" by the greats' form, "gives ... exactly; the relation is not new".
3. CHANGE the abstract's "four pass, twelve fail" to carry the cause of the twelve in one clause (the law, a declared input, a hypothesis), as sec:nature's
   prose already sorts them.
4. ADOPT, at the end of sec:newton, sec:delay, sec:gleason and sec:qm, one closing sentence in the greats' form: the author of the known law, the verb
   ("accounts for", "is equivalent to", "reduces to at first order"), one measured number with the experimenter's name, and the gap admitted.
5. ADOPT: move commit SHAs out of captions and Part II's text into Reproducibility and the appendix; add one-line bibitems for Shannon, Landauer, Bresenham
   and Jefimenko or drop the eponyms.

## URLs read (through the session's proxy; the raw files are saved beside this note)

Primary (RAW = https://raw.githubusercontent.com; SP = RAW/jundalisay/sp/master/content/en/research):
- RAW/borb-pdf/borb-pdf-corpus/master/txt/0370.txt (Einstein 1905a, fourmilab 1923 text) and .../txt/0124.txt (Einstein 1905b);
  RAW/superlinear-ai/wtpsplit-lite/main/tests/specrel.md (Einstein 1905a, second copy); SP/einstein/electrodynamics/part-10.md; SP/einstein/inertia.md
  (annotated) -
  RAW/rwong26/is310-coding-assignments/main/is310-coding-assignments/week1-cli-assignment/Maze/Entrance/On_the_constitution_of_atoms_and_molecules.txt (Bohr
  1913)
- RAW/SengerM/html-academic-publishing/main/examples/1928_Dirac/1928_Dirac_The_Quantum_Theory_of_the_Electron.html (Dirac 1928, partial)
- RAW/cccbook/py2cs/master/01-%E7%A8%8B%E5%BC%8F%E8%88%87%E6%95%B8%E5%AD%B8/%E6%9B%B8%E7%B1%8D/gemini3/dgeom/paper/1916-grel_english.wiki (Einstein 1916, Bose
  translation)
- SP/newton/principia/book-3/{1-introduction,2-phenomena,scholium}.md; SP/planck/spectrum/part-0{1,2,3}.md; SP/maxwell/dynamical/part-*.md;
  SP/boltzmann/chapter-01.md; SP/schrodinger/quantization/part-1*.md; SP/poincare/electron/introduction.md; SP/einstein/relativity/appendix-3{,b}.md;
  SP/whittaker/aether/chapter-08c.md; RAW/nelsonco/phys_categorizer/master/physics/physics.hist-ph/0405066v1.txt (Sauer on Einstein 1916)
Secondary (search snippets only; the pages were blocked): en.wikipedia.org/wiki/Kaufmann%E2%80%93Bucherer%E2%80%93Neumann_experiments (Lorentz on Kaufmann);
en.wikipedia.org/wiki/General_Scholium and plato.stanford.edu/entries/newton-principia/ (Rule I, hypotheses non fingo);
royalsocietypublishing.org/rspa/article/117/778/610/2242/ (Dirac abstract); aps.org/apsnews/2025/07/werner-heisenberg-pioneers-quantum-mechanics and
europhysicsnews.org/articles/epn/full_html/2025/02/epn2025562p15/epn2025562p15.html (Heisenberg 1925); link.aps.org/doi/10.1103/RevModPhys.20.367 and
thenewatlantis.com/publications/richard-feynman-and-the-pleasure-principle (Feynman 1948); fondationlouisdebroglie.org/LDB-oeuvres/De_Broglie_Kracklauer.pdf
and galileo-unbound.blog/2024/02/14/100-years-of-quantum-physics-de-broglies-wave-1924/ (de Broglie); mdpi.com/1099-4300/17/4/1971/htm (Sharp and Matschinsky
2015).
