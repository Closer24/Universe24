# The families in the paper: the tables of masses, groups, sets and vectors, audited against the register

The model owner, 2026-09-21 (translated): "make sure that the tables of
the masses, the groups, the sets, the vectors of all, all, all the
families we have are in the paper in the form they should be there;
clarify it with the paper's writer." Written by the mathematician,
read-only, on the paper as it stands on `main`
(`paper/general_formula/main.tex`) and on the register's one source of
the families (`examples/events/entities/families.json` and the worlds
under `examples/events/`), compiled by the host script
[family_table.py](family_table.py) with its output
[family_table.out](family_table.out): no run, nothing here is a rule.
The paper's writer owns the manuscript; this note is the audit and the
material, not an edit of the paper.

**The finding in one line.** The paper carries the family table's
SCHEMA (postulate P8: per family the content, the cost h per phase
step, the charge per unit of content, the strong column, the lifetime,
the phase rate and the hand), the groups in prose and in one figure (the
48 signed axis permutations, its 24 rotations and 24 reflections, the
circle `Z_N`, the permutations of the families, the label bits), and the
state vector's fields in prose (a row's and a body's), but NOT the
table's INSTANCE: no table in the paper lists the register's families
with their declared integers, their contents (the masses as declared),
the sets they are grouped in, or the group each declared quantity lives
on; "the family table" is cited to the Highlights and named as an
input (Table 1, the row "the masses and charges of the families:
input, the family table") without appearing. Four tables would close
the gap; their content is section 3, from the one source.

## 1. What the paper has, where

| the owner's word | what the paper carries | where |
| --- | --- | --- |
| the masses | the contents as inputs (P8; Table 1's INPUT row "the masses and charges of the families"); the minimal mass and the floors per kind (16.2, one unit; the floors 1, 1, 3, 3); a bound set's mass as its total content, `m_n - m_p` 2.54 and 1.51 against 1.29 (19); the neutrino's mass 0 refuted (row 8c) | Section 2 (P8), Table 1, Appendix tables recorda and recordc, Table tab:differs row 16 |
| the groups | the 48 signed permutations of the axes, `3! x 2^3`, the hyperoctahedral group `B_3`, its 24 rotations and 24 reflections told apart by the hand; the circle `Z_N`; the translations of the box and the interval; the permutations of the families with their columns; a boost not among them; the label bits and the group ring `Z[Z_N]` at the click | "The symmetries" paragraph of Section 2; the figure of the 48; Sections on the click model and the Gleason theorem |
| the sets | the state as the multiset of rows and bodies; a detector set of Nodes; a body on a set of Nodes (`span`) | Section 2 ("The state"), the click model |
| the vectors | a row's fields (Node, direction, age, phase, number, amount, content; under a record its identity, label, multiplicity, birth phase); a body's (Node, content, momentum, table of counts); the state vector **s** with its rate and wall per component; the six verbs | Section 2 ("The state", "The components"); the glossary table |

## 2. What the paper lacks

1. **The family table's instance.** The 75 families of the shipped
   definitions in their 27 entities (the sets), each with its quantum,
   charge, columns, lifetime, phase circle and hand; and the 23
   declarations the worlds make inline beyond them (the nucleus's proton
   at the charge 4; the quarks' `d` at -272; the coupling series'
   charges `[±2, 1]`, `[1, 2]`, `[0, 1]`; `nuclear` at the strong value
   7000 for the threshold's control; `glue` at `[10000, 606]`; the
   lamps' `phase_per_link` pairs; the W and the neutrino with a hand).
   The paper names the table's columns and never its rows.
2. **The masses as declared.** The contents the families carry on the
   worlds' measured events: the electron 1836 (series H and the atoms;
   1 in the gallery), the proton 1836 and 1834 (with `nuclear` 1 and
   `bond` 2 held), the neutron 1839 and 1837, the quarks 4 (`u`) and 9
   (`d`) with `glue` 1 held (606 and 607 dressed), the neutrino 4096,
   the W as a paid family of charge -7344, the free masses `m`, `mass`,
   `probe` from 1 to `2^26`, the sources' contents. These are the
   initialisation the paper calls an input (record 106, PREDICTIONS
   26); a reader of the paper cannot find one of them.
3. **The group per declared quantity, per family.** PREDICTIONS 26
   states the rule (what lives on a compact group is quantised, what
   lives on the scale is free), and the paper carries it in words; the
   table that applies it family by family (the content on the scale; the
   charge a winding on the circle, `Z`; the phase on `Z_N`; the strong
   column a signed scalar per unit; the lifetime in Links, `Z`; the
   hand in `Z_2`; the directions on the fan under the 48) is not there.
4. **The sets.** The entities of the definitions (a photon, an electron,
   a proton, a neutron, the strong family, the bond family, the up
   quark, the glue family, the neutrino and the antineutrino, the W, the
   apparatus materials, the masses, the sources, the choosers, the 24
   thrown sources, the 24 Hubble stars) are the sets the register
   declares its families in; the paper does not list them.
5. **The vectors per family.** The paper gives a row's and a body's
   fields once, for every family alike; what differs per family (a
   phase circle or none, a charge line or none, a column, a hand, a
   lifetime, a quantum or the content) is the family table's instance
   again (item 1).

## 3. The tables, from the one source (for the writer)

The script prints them; the writer takes what the paper needs.

- **Table F1, the family table's instance**: [family_table.out](family_table.out)
  section A (the shipped definitions: 75 families in 27 entities, every
  declared key) and section B (the 23 inline declarations with their
  worlds).
- **Table F2, the masses as declared**: section C (the content every
  family carries on the worlds' measured events, per series, with the
  held content beside).
- **Table F3, the group per declared quantity**: section D (per family
  of the physics: the content on the scale, the charge on `Z`, the
  phase on `Z_N`, the column, the lifetime, the hand on `Z_2`, the
  directions on the fan under the 48).
- **Table F4, the state vector per kind**: section E (a row's fields, a
  body's fields, the six verbs on them; the per-family differences by
  F1).

Where the paper cites "the family table" (P8; Table 1's INPUT row; the
"What is put in" paragraph), the citation should point at F1 and F2 in
the paper itself (an appendix table or two), with F3 beside the
symmetries paragraph and F4 beside "The state". Every number in F1 to
F4 is a declaration of the register (an input), labelled so; none is a
measurement.

## 4. Questions for the paper's writer

1. Does the paper carry the family table's instance (F1) and the
   declared contents (F2) as an appendix, or only the physics' families
   (the 17 of section D) with the apparatus materials and the sources
   named once? The owner asks for all of them.
2. The inline declarations that differ from the shipped ones (the
   nucleus's proton at the charge 4 against the shipped `[1, 1]`; the
   quarks' `d` at -272 against the shipped `d` a paid detector material
   of the same name; `nuclear` at 7000 as the threshold's control): the
   paper should say once that a world may declare a family beyond the
   definitions and that these are the register's declared variants, not
   a second law.
3. The masses row of Table 1 (INPUT, "the masses and charges of the
   families: input, the family table") should cite F2 in the paper,
   not the Highlights alone.
4. F3's rule (PREDICTIONS 26) is in the paper's words already; the
   table applying it per family is one appendix table, and the writer
   decides whether the symmetries paragraph carries it or the glossary.

## 5. Links

- The paper: `paper/general_formula/main.tex` (Section 2: P8, "The state", "The components", "The symmetries"; Table 1; the glossary); its plan `paper/general_formula/PLAN.md`.
- The one source: `examples/events/entities/families.json` (the definitions), the worlds under `examples/events/` (the inline declarations and the contents); [ENGINE.md](../../ENGINE.md) (the family keys); [PREDICTIONS.md](../../PREDICTIONS.md) entry 26 (what is quantised and what is free); [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) sections 16.2 and 19 (the minimal mass, the masses); [LAW.md](../vector_form/LAW.md) section 1 (the state: three vectors).
- The script and its output: [family_table.py](family_table.py), [family_table.out](family_table.out).
