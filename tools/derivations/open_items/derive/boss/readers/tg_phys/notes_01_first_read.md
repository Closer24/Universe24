# Notes 01: first read of TIMEGEAR.md, notes_01, notes_02, mc_phys/REPORT.md, EDGE3.md

## The claim, as I read it
- 00 row: the gear whose count IS the clock. Its dial D = W(before) + W(now) on the edge; the out edge needs W(next),
  which it has not made yet (the fixed point).
- Symmetric root law: D_in^2 + D_out^2 = 8 W(a)^2 + 4 push + s - s+, with D_in = W(b) + W(a), D_out = W(a) + W(a+).
  Act: M = 8 W(a)^2 - D_in^2 + s + 4 push; D_out = u nearest sqrt(M) (cells [u(u-1), u(u+1)-1]); s+ = M - u^2;
  W(next) = u - W(a).
- Physics claimed: 4 W (q - v) + q^2 + v^2 = 4 push + s - s+  ==> W dv/dt + v^2/2 = F with dW/dt = v.
  Claimed to be sqrt(W) d_t (sqrt(W) d_t a) = F: "the lapse's own equation". sqrt(W) v kept on a free course.

## First suspicions (to be measured)
S1. "W dv/dt + v^2/2 = F" with W' = v  IS  d_t(W v) - v^2/2 = F ... let me check: d_t(W v) = W' v + W v' = v^2 + W v'.
    So W v' + v^2/2 = d_t(W v) - v^2/2. Hmm. And sqrt(W) d_t(sqrt(W) v) = sqrt(W) [ W'/(2 sqrt W) v + sqrt(W) v' ]
    = W' v / 2 + W v' = v^2/2 + W v' when W' = v. OK so the continuum identification is right IF W' = v, i.e. the
    00 row's own velocity is dW/dt, which it is (W = rest + a, v = a - b). Fine on paper.
    BUT the physicist's "nature" in mc_phys item 1 was derived for a FIELD a under a lapse N(t) with
    1/N = sqrt(W/rest): sqrt(W) d_t(sqrt(W) d_t a) = F. That is the equation for every OTHER row (matter under the
    lapse). Is the same equation nature's for the LAPSE ITSELF? The lapse in GR has no own kinetic term (it is a
    Lagrange multiplier); the "00 row" dynamics in this engine is a scalar wave of W. Claimed in TIMEGEAR s.4:
    "the clock's own gear must run on light's cone" and "sqrt(W) d_t(sqrt(W) d_t a) = F, the lapse's own equation".
    Need to ask: is a self-coupled W dv/dt + v^2/2 = F the equation of the 00 component under its own lapse? The term
    v^2/2 = (dW/dt)^2 / 2 is a self-interaction (nonlinear). For a wave of W on light's cone with c^2 = grip/W, what
    does the free (push = 0) course mean? sqrt(W) v kept means W grows as sqrt: W(t) ~ (3/2 K t)^(2/3). Hmm, with
    W' = K / sqrt(W), W^(1/2) dW = K dt, (2/3) W^(3/2) = K t, W ~ t^(2/3). Compare the text's "nature: W about
    26,600 at the end" with rest 10,000, v0 = 1, 30,000 rounds: sqrt(W) v = 100 => W^(3/2) = 10^6 + 150 * 30000
    = 10^6 + 4.5 x 10^6 = 5.5 x 10^6 => W = 5.5e6^(2/3) = 31,200?? Let me recompute: (2/3) W^(3/2) = K t + (2/3) W0^(3/2),
    W0^(3/2) = 10^6, K = 100. (2/3) W^(3/2) = 3000000 + 666,667 = 3,666,667 => W^(3/2) = 5,500,000 => W = 5.5e6^(2/3).
    ln(5.5e6) = 15.52; * 2/3 = 10.35; e^10.35 = 31,200. The text says "about 26,600". That differs. CHECK with whole
    numbers (cube root search). Actually: maybe the text's nature has W' = v and W v' + v^2/2 = 0 => v = C / sqrt(W)
    => dW/dt = C/sqrt(W) => my integration. Let me recheck: W0 = 10000, v0 = 1, C = 100. W^(3/2) = 10^6 + 1.5 * 100 * 30000
    = 10^6 + 4.5e6 = 5.5e6. W = 5.5e6^(2/3). 5.5e6^(1/3) = 176.5; squared = 31,150. So nature gives ~31,150, not 26,600.
    And "W v kept: 26,458": W dW/dt = 10^4 => W^2 = 10^8 + 2e4 * 3e4 = 10^8 + 6e8 = 7e8 => W = 26,458. OK that matches.
    So who is 26,600? Perhaps a mislabel. MEASURE.
S2. The "second cone" argument: the 00 row's own wave. For a WAVE of W on a board (not one gear), the symmetric form's
    speed was measured 1008, 1006 permille. The text says "the wave's mean drifts: nature's v^2/2 term". A v^2/2 term
    in a wave equation is a nonlinearity that will steepen waves -- in a lapse that is a time reparametrization,
    is there any such nonlinearity? For a pure lapse (uniform), nature says nothing is observable. For the 00 wave:
    the text treats W as a dynamical scalar field with its own wave equation. Nature (GR) has no propagating scalar
    lapse mode. So "one cone" is a necessary but not sufficient condition. Note that.
S3. Uniform rate change: if W -> every clock's W changes uniformly, two clocks at one site see nothing. Under the
    symmetric form, the 00 gear's OWN course is not uniform in time: the quirk at |v| = 1 -- linear growth of W.
    This means a uniform lapse drift of 1 count/round is NOT the same as 2 counts/round scaled... Measure: does a free
    00 gear at v0 = 1 vs v0 = 2 give the same physics under a rescale? Under nature (sqrt W v kept) both decelerate.
    Under the symmetric form at v = 1 W grows linearly for ever: a sub-notch artefact. Does this matter where the lapse
    moves slowly (sub-notch)? At the real calibre W ~ 10^23 and the lapse moves by << 1 count a round, so v = 0 mostly
    with a tooth drifting: "at v = 0 every form freezes a sub-half-count momentum". Need to measure the sub-notch
    regime: v0 < 1 i.e. a tooth of momentum s0 with v = 0. Does the symmetric form move at all? Under the act, M =
    8W^2 - D_in^2 + s + 4 push with D_in = 2W (v = 0): M = 4 W^2 + s. u nearest sqrt(4W^2 + s) = 2W if |s| <= 2W. So
    s+ = s, W(next) = W. The tooth is frozen for ever at v = 0: no motion below one count. And with push: M = 4W^2 +
    s + 4 push; the quotient changes when s + 4 push crosses +-2W. Hmm, for u = 2W+1: u(u-1) = (2W+1)(2W) = 4W^2 + 2W.
    So s + 4 push >= 2W needed. So the threshold for a move is 2W = D (the dial) just like the carry. Fine: same
    quantization. But at v = 1: D_in = 2W - 1, M = 8W^2 - (2W-1)^2 + s = 4W^2 + 4W - 1 + s. u = 2W + 1 has cell
    [4W^2 + 2W, 4W^2 + 6W + 1]. So M in cell iff s in [-2W + 1, 2W + 2]... s in [-D_in, D_in - 1] = [-2W+1, 2W-2].
    So ALWAYS u = 2W+1, q = 1, s+ = M - u^2 = 4W^2 + 4W - 1 + s - 4W^2 - 4W - 1 = s - 2. Tooth drifts -2 a round;
    the dial D_out = 2W+1 grows by 2 a round (W by 1). s must stay >= -D_out = -(2W+1)... s decreases 2 a round, the
    dial's lower bound decreases 2 a round: s - 2 >= -(2W + 1) iff s >= -2W + 1 ... hmm s_t = s_0 - 2t, lower bound
    -(2 W_t + 1) = -(2 W_0 + 2t + 1). So s_t - lower = s_0 + 2 W_0 + 1 - 2t + 2t... = const. The tooth never falls
    out. CONFIRMED on paper: at v = 1 the quotient is 1 for ever. That's the "quirk". At v = 2: D_in = 2W-2, M =
    8W^2 - 4W^2 + 8W - 4 + s = 4W^2 + 8W - 4 + s. u = 2W+2: cell [(2W+2)(2W+1), (2W+2)(2W+3) - 1] = [4W^2 + 6W + 2,
    4W^2 + 10W + 5]. M in cell iff s in [-2W + 6, 2W + 9]. s in [-2W+2, 2W-3]: for s in [-2W+2, -2W+5] (4 values) u
    = 2W+1 (q = 1): "the tooth overflows and the quotient falls". s+ = M - u^2 = 4W^2 + 8W - 4 + s - 4W^2 - 4W - 1 =
    4W - 5 + s when q = 1... = 4W - 5 + s in [2W - 3, 2W] -- hmm, needs s+ <= D_out - 1 = 2W + 1 - 1 = 2W. OK in
    range. Otherwise s+ = M - (2W+2)^2 = 4W^2 + 8W - 4 + s - 4W^2 - 8W - 4 = s - 8. Tooth drifts -8 a round at v = 2,
    and the lower bound moves -4 a round (W by 2). So it falls out in ~ (s0 + 2W0 - 2)/4 rounds, and then q = 1 ...
    then at v = 1 it stays for ever. So nature's deceleration is coarse: v = 2 -> 1 then stuck at 1 for ever!
    Nature: v would decrease continuously as 1/sqrt(W). The symmetric form at the integer level: v: 100 -> ... -> 2 ->
    1 -> 1 for ever. The "sqrt(W) v kept within 1.5 percent" is measured at v0 = 100 over W x 3 (v ~ 100 -> 58). Not at
    small v. So "nature's form" is a claim about the large-|v| regime only; at |v| <= 1 the form is NOT nature's
    (a linear clock, v kept: the as-built physics). Where does the lapse actually sit at the calibre? W ~ 10^23 and the
    velocity of the 00 slot... the text itself says "its share of the dial is 2 counts a round against 2 W ~ 10^23".
    So the 00 slot moves a count or so a round at most -- the regime where the symmetric form is the as-built
    form, not nature's. Potential BLOCKING: nature's form is claimed where it is not measured, and in the regime
    the engine runs (|v| <= 1) the form is not nature's.
    However: what does "nature" even mean at |v| ~ 1 count/round for the 00 slot? The deceleration of W is
    v^2/(2W) per round = 1/(2 x 10^4) per round at v = 1: it takes 2W rounds to lose one count of velocity: 20,000
    rounds at W = 10^4. The symmetric form should lose one count of velocity after 2W rounds (when the tooth has
    drifted a full dial) -- but it never does because the dial grows as fast as the tooth drifts. The tooth drift 2
    per round comes from q^2 + v^2 = 2 at q = v = 1, and the dial growth 2 per round comes from 2 x (W growth 1).
    In nature at v = 1: W v' = -v^2/2 = -1/2 per round: after 2W rounds, v = 0. Under the form: never.
    The condition for the quotient to fall to 0 at v = 1: s + 4 push drops below the cell u = 2W+1's lower end
    minus... M = 4W^2 + 4W - 1 + s < 4W^2 + 2W iff s < -2W + 1 = -D_in -- impossible since s >= -D_in. So the quotient
    can NEVER fall from 1 to 0 by the free drift, only by a push. The claim "at |v| = 1 ... the quotient never falls"
    is thus exact: an unphysical fixed velocity. It is physics-breaking when the lapse's own sqrt(W) v should decay.
    But hold on -- is the deceleration of the 00 gear "nature"? There is no "nature" for a free lapse: a uniform
    lapse drift is pure gauge. The deceleration W v' + v^2/2 = 0 for the lapse itself is an artefact of giving the
    lapse a kinetic term. Hmm, but the engine does that in every form. The question the task asks: "Ask whether the
    symmetric root law is nature's clock where nature's clocks sit". Where nature's clocks sit: the lapse moves slowly,
    sub-notch, in proper time nothing happens to a uniform lapse. The symmetric root law at v = 0 is frozen like
    every form; at v = 1 is linear; both are consistent with "a uniform lapse is unobservable" ONLY IF the other
    rows see it as a time reparametrization. For other rows, the form is the edge (W v kept) or whatever the fwdback
    deriver finds -- not this page's. OK.
S4. The twin: is parting really unstable, or is the measured parting the same |v| = 1 artefact (one half's momentum
    meets the half count first)? The text: "A frozen at 19,999, B at 40,000". Both halves started at v = 1; A drops
    to 0 (W v kept gives v -> 0 when P reaches half count...). Under W v kept: P = 2 D v + s constant = 2 x 20000 x 1
    + s0 ~ 40,000; D grows to 40,000 => v falls to 1/2 => quotient jitter 1,0,1,0 for the carried dial; for the twin,
    A's dial is B's 2W: when A's v falls to 0 (q = 0), A freezes, its W(A) stands, and B's dial 2 W(A) stands, so B
    with momentum P_B = 2 D_B v_B + s_B constant and D_B constant: v_B = 1 for ever. YES the parting is the |v| = 1
    quirk in another guise: P/2D = 1/2 exactly at the half count. Would it also happen at the real calibre? Yes
    whenever v passes through 1/2 in units of counts/round: every free decelerating clock passes through v = 1/2.
    Hmm, but in which direction... the carried dial: when v crosses 1/2 the quotient jitters 1,0,1,0 - a Nyquist
    drive. It's the discreteness of the quotient. At the real calibre the jitter is of 1 count on W ~ 10^23 -- the
    departure grows 2 counts a round. In 10^23 rounds it matters. In 10^10 rounds (the universe), 2 x 10^10 on 10^23
    is 2 x 10^-13. The text says "growing without bound where the jitter's spacing is even". So is the register's
    pump a real cost? Its linear growth needs the strict alternation 1,0,1,0 - which needs v = 1/2 EXACTLY and a
    standing W... but W grows by 1 every 2 rounds, so v drifts. Measure: how long does the alternation last, and is
    the growth linear for ever or does it saturate when the pattern changes (e.g., 1,0,0,1,0,0 at v = 1/3)?
    The text claims "20,001 of a dial 60,000 at round 30,000": with the pump growing the dial, the velocity v = P/(2D)
    falls below 1/2 -> pattern changes -> less pumping? Actually the quotient pattern follows the tooth's drift... Need
    to trace. MEASURE with the text's probe_tg9 and my own.
S5. "Nature has one cone for every field" vs "the lapse's own wave on light's cone" -- in GR the lapse has no wave.
    The engine's 00 row IS a dynamical field with grip (it's "the metric's time component"). The test the task sets:
    does the lapse's own wave sit on light's cone? Measured 1008, 1006 under the symmetric form (vs 1000 for the carried
    forms). The text explains the 8 permille by "the wave's mean drifts: nature's v^2/2 term". Hmm: a v^2/2 term in
    a wave of amplitude A = grip/1000 of W: the drift of the mean is a second-order effect: v^2/(2W) ~ (A omega)^2 /
    (2 W). Is 8 permille consistent? Measure: run the symmetric form's wave probe at half the amplitude: if the
    departure from 1000 falls 4x, it's the nonlinearity; if it stays, it's a dispersion/stride artefact. Also measure
    the cone with a different stride (the window). The text says "T_light^2/T_00^2" - the period ratio squared. 1008
    permille = 0.8% in c^2.
S6. Energy books by windows: "the round's identity 0 misses" for the symmetric form -- what identity? D_in^2 + D_out^2
    = 8W^2 + 4 push + s - s+ IS the law, so "0 misses" of the law is a tautology, not a book. For the carry forms, P =
    2 D v + s obeys P+ - P = 4 SUM push: a conservation law. For the symmetric form what is the conserved momentum?
    It is sqrt(W) v (the continuum), with no integer form -> no exact book. The energy of the other rows under the
    00 row's law: do windows show conservation? MEASURE: a hairspring on the 00 gear under the symmetric form: is its
    amplitude constant (books by windows)? The text measured (probe_tg3) "0.5 grip under a mode of a grip on the 00
    row" departures for the carried dial... I need to see what probe_tg7/tg9 did.
S7. probe_tg9: "sqrt(W) v kept within 1.5 percent at v0 = 100 (W 3,115,855 against nature 1000, against W v kept
    1386)" -- what's 3,115,855? W from 10^6 after 30,000 rounds at v0 = 100: nature sqrt(W) v = 10^5: W^(3/2) = 10^9 +
    1.5 x 10^5 x 3 x 10^4 = 10^9 + 4.5 x 10^9 = 5.5 x 10^9; W = 5.5e9^(2/3) = (1.7652e3)^2 = 3.116e6. OK so 3,115,855
    matches nature's W to 1000 permille. Good. And W v kept: W^2 = 10^12 + 2 x 10^8 x 3 x 10^4 = 10^12 + 6 x 10^12 =
    7e12, W = 2.6458e6; 3115855/2645751 = 1.178, hmm "1386"? Maybe they measure v^2 W: nature's v^2 W = 10^10 /
    ... whatever. Will check in the .txt.
    So in the text's "rest 10,000, v0 = 1 ... nature: W about 26,600 at the end" -- my calc gives 31,150. Check.

## Stride: every measure I make states its stride (the sampling interval in rounds) and reads means by windows.
