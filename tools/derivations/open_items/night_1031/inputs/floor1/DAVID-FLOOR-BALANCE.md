# The floor's balance: masses against bands

David, 2026-10-31, 10:4x UTC, on the owner's order to David of 10:3x UTC (in Hebrew; in translation): "Search for all
the solutions in these balances, and pass the above law to the writer." The law above is the line he answered in
David's answer to him and named "the breakthrough" (10:21 to the Boss, 10:28 to David): "No floor is laid, and no law
line sets one. It comes out by itself when the structure gives two clocks joined by a band each a mass of at least half
the band. If the algebra gives exactly half, the floor comes with nothing added." It stands among his words of the same
hour: "There is no floor in the law." (10:11), "The floor comes out by itself.." (10:14), the masses "come out of the
structure in the clicks" (10:18), "From the structure only." (10:21), "The miracle... requires a certain mass number for
the spring." (10:2x) and "In my opinion everything is from the structure.." (10:26). Posted on #2187 as 6542240895 and
6542281701. Status: **for its hostile pair** (a mathematician and a physicist, each new to it).

Letters, as on Big Pic's equil.py (bigpic-3clicks 9771a49a4, the click world's own numbers): W the rest teeth, s a
clock's own spring (its mass), t the two-leg band between two clocks (the hands' tie, TIE2 = 96,000), c the four-leg
tie's factor (TIE4 = 60,000), S the held hand's spring, h the held hand's count. A clock's potential terms are s x^2,
t x_i x_j and c x_i^2 x_j^2, as his pushes -2 s a_i, -t a_j and -2 c a_i a_j^2 say.

**The finding in one line:** on the click world's triangle the giver and the taker swing together or opposite; the
band adds t/2 to the together swing and takes t/2 from the opposite one, and the held hand lends both c h^2, so the
potential is bounded below at every h exactly when s >= t/2 (for unequal masses s_1 s_2 >= (t/2)^2). The floor comes
out of the masses and the band alone, or not at all; the smallest mass that gives it is half the band, and at that
balance the opposite swing keeps no spring of its own and is held by the held hand's lend alone. On a pair the
whole-number balances are the divisor pairs of (t/2)^2 (315 on the click world's band). For equal masses and bands on
any network the balance is s = -lambda_min(A) t/2: half the band exactly on networks of complete groups, the whole band
on the line networks and the exceptional ones of E8.

## 1. In clocks

- **Two clocks on one band.** If they swing together, the band pulls each back by half its strength more; if they swing
  opposite, it pushes each on by half its strength. A clock's own spring s is its mass.
- **The held hand lends a spring.** Through its four-leg tie with each of them it lends c h^2 to the giver and to the
  taker alike, more when it swings wide, nothing when it passes 0.
- **The opposite swing keeps s - t/2 + c h^2.** When the held hand passes 0, only s - t/2 is left. Below half the band
  the opposite swing then runs downhill and the pair runs away: the shipped click world's fall, where the giver and the
  taker hold no spring of their own (s = 0, Big Pic's 6541977181 item 2).
- **At exactly half the band** the opposite swing keeps no spring of its own and is held by the lend alone; above half
  it holds with room. Nothing is laid for the floor: it is the masses against the band.

## 2. In the algebra

### 2.1 The pair

- The click world's triangle with an own spring s on the giver (g) and the taker (u):
  V(g, u, h) = s g^2 + s u^2 + t g u + c h^2 (g^2 + u^2) + S h^2 = [g u] M(h) [g u]^T + S h^2, with
  M(h) = [[s + c h^2, t/2], [t/2, s + c h^2]] = M(0) + c h^2 I.
- M(h) = (s + c h^2) I + (t/2) X, X the swap of the two clocks. Its parts are the swap's even direction (1, 1), holding
  s + c h^2 + t/2, and its odd direction (1, -1), holding s + c h^2 - t/2.
- **The floor (DERIVED):** with c >= 0 and S >= 0, if M(0) is non-negative then every M(h) is, and V >= 0. If M(0) has
  a negative direction v, then V(r v, 0) = r^2 v^T M(0) v runs to minus infinity with r. So V is bounded below exactly
  when M(0) is non-negative: s >= t/2, and for unequal masses s_1 >= 0, s_2 >= 0, s_1 s_2 >= (t/2)^2 (its determinant).
- **The balance** is the floor's edge, det M(0) = 0 with M(0) non-negative. Its equilibria are exactly the kernel's
  directions: at s_1 s_2 = (t/2)^2 the kernel of M(0) is spanned by (t/2, -s_1), since s_1 (t/2) - (t/2) s_1 = 0 and
  (t/2)^2 - s_2 s_1 = 0. At equal masses it is the opposite swing (1, -1). Displaced along it with h = 0, the pair rests
  with V = 0.

### 2.2 The whole-number balances on a pair

- With t = 2m the balances are s_1 s_2 = m^2. In whole numbers they are the divisor pairs (d, m^2 / d), and at each the
  free swing (m, -s_1) is a whole-number direction: no root enters.
- On the click world's band m = 48,000 = 2^7 x 3 x 5^3, so m^2 = 2^14 x 3^2 x 5^6 has (14 + 1)(2 + 1)(6 + 1) = 315
  divisors: 315 ordered balances, 158 unordered (m^2 is a square, so one divisor is its own partner), and one equal
  pair, 48,000 each.
- The giver and the taker carry the same couplings in the file, and the triangle keeps their swap (Big Pic's
  equil_5000.txt: the round turned alike in 2 of the 6 turns and flips). A structure that keeps the swap gives them one
  mass, and then the balance is the one number s = t/2.

### 2.3 Every network of clocks, equal masses and equal bands

- **Scope:** networks whose terms beyond the quadratic ones are the held hands' lends, each a held value's square times
  a clock's square with a factor c >= 0, as on the click world's triangle. Then the reading of 2.1 holds word for word:
  the floor is the quadratic form at zero lend, non-negative.
- With equal masses s and equal bands t on the edges of a network with adjacency A, that form is s I + (t/2) A. The
  floor asks s >= -lambda_min(A) t/2, and the balance's equilibria are the directions of lambda_min(A).
- A is a whole-number matrix, so a rational eigenvalue of it is a whole number. So the balance is a whole-number
  relation between the mass and the band exactly when lambda_min(A) is a whole number.
- **lambda_min = -1, the balance at half the band:** exactly the networks whose connected groups are complete, every
  clock banded to every other: the pair, the triangle, the tetrahedron and on. A complete group of n clocks has the
  eigenvalues n - 1 and -1, the -1 on the swings that sum to 0. Any connected group that is not complete holds an open
  path of three clocks, two of them not banded, whose lowest eigenvalue is minus the root of two, and by Cauchy's
  interlacing the group sits at or below it.
- **lambda_min = -2, the balance at the whole band (s = t):** within the networks whose lowest eigenvalue is at least
  -2, which are the line networks, their generalized kin, and the exceptional ones represented in the E8 root system
  (P. J. Cameron, J.-M. Goethals, J. J. Seidel and E. E. Shult, J. Algebra 43 (1976) 305-327). Every even ring is one;
  its balance's equilibrium is the alternating swing.
- An odd ring of five or more clocks has no whole-number balance: the ring of five sits at minus the golden ratio, and
  every odd ring longer than three sits at an irrational number.
- **On the equilateral triangle of two-leg bands,** where Big Pic found the floor (6541977181 item 4), the form is
  s I + (t/2)(J - I): the common swing (S_3's trivial part) holds s + t and the two swings summing to 0 (its
  two-dimensional part) hold s - t/2, so the floor asks s >= t/2, the same number as the pair. At s = t/2 those two hold
  no spring at all there, since no held hand lends one.

## 3. On the board

- Big Pic's round keeps E32 to the teeth's share in every round (his identity, read every round here too), and an own
  spring is a degree-2 term, which adds no residual (ALG3's M8, the Boss's 6542202933 item 3). So the exact step and its
  books stand at every s read.
- The floor of section 2 is the potential's. That the round's E32, the kinetic with each term polarized at the edge, is
  bounded below exactly when the potential is, at the click world's steps (the held clock's 2 S / W = 1/3), is the
  standard reading of a polarized step; this text reads it as no fall, measured, and does not derive it for every grain.

## 4. In the clicks

- The masses are read only in the clicks (the owner's word of 10:18). What the board shows here is what the clicks will
  read: at the balance and above, no count runs away and the taker takes the giver's whole swing, so the first click's
  passing goes on with a floor under it.
- **Below the balance the pair holds only while the held hand swings wide enough.** The held hand swings fast beside the
  pair, so the pair feels the mean of the lend, c times the held square's mean, half its largest for a plain swing A:
  it needs s + c A^2 / 2 > t/2. At the shipped swing (A = 1) that is s > t/2 - c/2 = 3/8 of t/2, and the measured edge
  sits there (section 5). The edge moves with the swing, which the run itself changes, and wider swings pump the pair at
  windows (section 5's last rows): a hold, not a floor. A reading, not derived.

## 5. Measured (node/floor_balance.txt)

floor_balance.py on node-all 9d75a4904's src and Big Pic's equil.py of 9771a49a4, his World and round unchanged, his
grain recipe; 5,000 rounds; a fall is a count 20 bits past the giver's lay.

- **The control, as shipped (s = 0), lambda 100:** the largest held square per 250 rounds 12,996, 8,464 and 33,489
  counts^2 (1.2996, 0.8464 and 3.3489 of the unit), then the fall at round 827: Big Pic's whole click world's walk
  (split_bedge_x100_5000.txt), read on his triangle alone.
- **At the balance, s = t/2:** no fall at lambda 1, 10, 100 and 1000; the identity in 5,000 of 5,000 rounds and the run
  back exact at each; the giver's and the taker's largest swings 46 and 46 of the unit at lambda 100, 39 and 40 at
  lambda 1000.
- **Above it** (11/10 and 2 times t/2, lambda 100): the same.
- **Below it, lambda 100:** 1/4, 3/10 and 3/8 of t/2 fall, at rounds 2,813, 4,841 and 4,136; 2/5, 9/20, 1/2, 9/10 and
  99/100 hold over the run (9/10 also at lambda 1000), each with the identity exact and the run back exact.
- **The swing alone (s = 0), the held hand laid wider, lambda 100:** 1.20 of the shipped lay falls at round 1,702; 1.25,
  1.28 and 1.30 hold; 1.35 and 1.50 fall at rounds 3,535 and 4,227; 2.00 holds.

## 6. What stands, and OPEN

- **DERIVED here, for the pair:** the floor on the click world's triangle exactly when the masses meet the band (2.1);
  the balance's equilibria, the kernel (t/2, -s_1); the whole-number balances as the divisor pairs of (t/2)^2, 315 on
  the file's band (2.2); for equal masses and bands, the balance at -lambda_min(A) t/2 with the classes of 2.3, two of
  them cited.
- **MEASURED:** section 5, on Big Pic's triangle; scratch readings first posted in 6542212052 and 6542160901.
- **OPEN:**
  - whether the one algebra gives the masses and the bands, and which balance they meet: Big Pic's search, by the
    owner's order of 10:3x and the Boss's 6542181017;
  - the books in the clicks on the whole click world at the balance: Big Pic's;
  - the polarized step's floor at every grain (section 3);
  - the strengths law's second clause under "everything is from the structure": the Boss's with the owner;
  - any mass of nature, and any physics from these board readings.

## 7. How this text checked itself

- 2.1 by substitution: (1, 1) and (1, -1) in M(h); the kernel (t/2, -s_1) at four balances of the click world's band,
  (1, m^2), (2^14, 3^2 5^6), (m, m) and (3^2 5^6, 2^14), each giving (0, 0).
- 2.2 by the exponents of m = 48,000 = 128 x 3 x 125; nothing searched.
- 2.3 by the cited theorems and the eigenvalues of the complete group, the open path and the even ring, written out.
- Section 5 by the probe, whose control reproduces Big Pic's three held squares and his round of the fall exactly.
