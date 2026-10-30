# Notes 03: probe A (two clocks on a uniformly deepening clock) -- the decisive physics numbers

File: probe_a_two_clocks.py -> probe_a_two_clocks.txt (whole numbers; edge_lib.split and tensor24 carry only).
Harness checked against the real act through edge_lib's board (12 rows x 27 sites, uniform light row on a spring,
00 slot rising 1/round): 0 misses in 400 rounds for the edge (cut) and for the act as built (loader's lay).

## A. Free gear, v0 = 1e6 notches/round, W 10,000 -> 40,000 (x4, 1 count a round)
            v at W=4e4   v^2 W / start (permille)   P = 2 D v + s
as built    1,000,000    4000                        grows (39,998e6 -> 159,998e6)
edge          249,991     249                        kept to the bit (39,998,000,000 at every mark)
half-tooth  1,000,000    4000                        grows
nature      500,000 (v ~ W^-1/2)  1000 (proper velocity v/N constant: a uniform lapse is a change of time coordinate)

## B. Hairspring, g = 100, A0 = 1e7, same clock (base = the mark at W 17,500; W x2.17 to 38,000)
            A/A0 at W=38,000   A^4 W (permille)   T^2/W
as built    1212               4699               989   (A ~ W^(+1/4): the WKB invariant A^2 omega of W a_tt = -g a)
edge         824               1002               989   (A ~ W^(-1/4): E/omega kept to 0.3 percent)
half-tooth  1212               4699               989
nature      1000               (A constant)       (the beat omega = sqrt(g/W) in every form: T^2/W the same)
2.17^(1/4) = 1.214, 2.17^(-1/4) = 0.824: the measured values ARE the quarter powers.

## C. Notches per beat v T (two clocks at one site), W 10,000 -> 38,000 (x3.8)
as built/half-tooth  1932 permille  (3.8^(+1/2) = 1.949)
edge                  508 permille  (3.8^(-1/2) = 0.513)
nature               1000           (all clocks slow alike: local position invariance)
=> The edge and the act as built sit symmetrically about nature, each off by sqrt(W_out/W_in) in a free gear's
   proper velocity. Nature's equation is W d_t v + (1/2)(d_t W) v = F, i.e. sqrt(W) d_t (sqrt(W) d_t a) = F; the edge
   keeps the whole (d_t W) v, the others none of it.

## E. Term 9's notch: one swing W 10,000 -> 20,000 -> 10,000 (1 count a round each way)
Free gear:  edge v 1e6 -> 499,987 at the top -> 999,900 back (P kept to the bit; the 100-notch loss is the tooth's
            re-split rounding); as built v constant throughout.
Hairspring: edge A 930 permille at the top (W x1.33: 1.33^(-1/4) = 0.930), back to 998 at W 15,000; as built 1075
            at the top (1.33^(+1/4) = 1.075), back to 1001. Both return over a full swing (adiabatic invariants);
            within the swing both breathe, oppositely. Nature: no breathing at all.
Half-tooth on the falling half: ran here without its promise (the carry takes a negative tooth) and gave the
            as-built numbers; CLICK25 itself says its run back fails there (probe D to confirm).

## What this means for the owner's rule
The edge conserves P = SUM(2 D v + s) as a board invariant, exactly. In the clicks' spacetime (proper time) the free
gear's momentum m v / N and the hairspring's energy both fall as W^(-1/2) under the edge on a uniformly deepening
clock, where nature keeps them. So the edge conserves precisely the kind of quantity the owner said not to ask for,
and loses the kind he asked for. The as-built/half-tooth lose it the other way (W^(+1/2)).
