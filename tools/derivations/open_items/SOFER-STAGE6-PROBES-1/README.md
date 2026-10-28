# Sofer's probes of stage 6 (tensor24-review 83a0b214a)

Four files, each run on the repo's Python with `python -I`, the outputs beside them.

- **channels_check.py** (no worktree): the 24, the five kinds as matrices and the channels C[i, k -> m] made from the
  groups' definitions alone, not from the build. Each kind is a representation on all 576 pairs (2,880 products); the
  characters on the five classes (sizes 1, 8, 3, 6 and 6) are the table of SOFER-KINDS-REFERENCE-1; the six Spokes are
  A1 + E + T1 and the three axes A1 + E; there are 43 channels, each of multiplicity 1; the first nonzero seed's group sum
  is kept by all 24 at every channel; one seed of all ones loses 20 of the 43; every nonzero seed of a channel gives its
  primitive tensor up to sign, with a content of 4, 8, 12 or 24 (the first seed's: 4 on 19 channels, 8 on 17, 12 on 3,
  24 on 4), and 9 channels give two contents by seed.
- **signs.py** `<worktree>`: the sign of each table as the build makes it. The tables are primitive (the build divides
  out the content), and their sign is the first nonzero seed's: the first nonzero entry is positive on 37 channels and
  negative on 6, all six with E (A2 x E -> E, E x A2 -> E, E x T1 -> T2, E x T2 -> T1, T1 x E -> T2, T2 x E -> T1).
  The tests pin the sign of the dot, the cross and A2 x T1 -> T2 alone.
- **fuzz_files.py** `<worktree> <variants> <seed>`: the three files mutated at random (a value replaced by one of 27
  hostile values, a key or a row dropped, one added or doubled, the text cut, made no JSON, nested 100,000 deep or holding
  a number of 5,000 digits), each variant through the checker and, where it holds, through the load and the contraction.
  A raise anywhere is a finding.

## What they found at 83a0b214a

- **The checker raised in 0 of 23,000 variants, and the contraction in 0 of the 1,716 that loaded.**
- **The load raised on files the checker holds:** 14 of 264 variants in the first run and 77 of 1,701 in the second.
  - `KeyError: 'gears'`: a setting with no gears key (the checker reads it as no gears, `setting.get("gears", [])`;
    the load reads `setting["gears"]`).
  - `KeyError: 'couplings'`: a universe with no couplings key, the same (`universe.get("couplings", [])` against
    `universe["couplings"]`).
  - `ValueError: Maximum allowed dimension exceeded`: a piece whose sides multiply past what an array holds
    (runner/load.py, lay); the checker bounds no side, so the load names none.
- **The sign convention** is the order the seeds are tried in. It stays silent while no train holds E (stage 6 refuses
  one); before stage 7 puts E beside A1 in the tensions, a sign by rule (the first nonzero entry positive) keeps the
  tables whatever the order.

## What they give at 927071a14 (the Boss's 91226e796 and the eighth review's changes)

- **The load raises on none of 43,000 variants** (3,000 at seed 20261028, 20,000 at seed 7 and 20,000 at seed 11): the checker, the
  load and the contraction each raise none. The `.get` for gears and couplings and the board's size named in lay() are in.
- **signs.py gives 43 of 43 positive:** each table is primitive with its first entry positive.
- The harness drew its hostile values from one pool of objects, which made a circular document in one configuration;
  each value drawn is now a copy.

---
Sofer, scribe-5.
