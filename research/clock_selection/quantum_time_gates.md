# Bell, click records and operational time: required gates

Status: mathematical constraint and prospective observation requirements.
No new trajectories, quantum measurement rule or clock update is introduced.
Existing route exclusivity, phase writing, wave comparisons and reversibility
do not by themselves establish quantum entanglement or a physical time arrow.

## A conditional Bell obstruction

Bell's original paper isolates the problem of reproducing quantum correlations
with local hidden-variable responses [1]. CHSH makes a related correlation test
explicit for two settings at each apparatus [2]. For Universe24, state the
following assumptions before interpreting any statistic:

- Each registered trial has local settings i,j in{0,1} and local outcomes
  A_i,B_j in{-1,+1}, obtained with one frozen observation map.
- The relevant hidden-variable preparation has the same distribution rho(lambda)
  for all four setting pairs. Define the source, apparatus and setting registers
  explicitly; independent-looking pseudorandom seeds do not prove this condition.
- The outcome at A depends on i and lambda, but not j; B depends on j and lambda,
  but not i. Any setting-independent auxiliary variables can be included in
  lambda. This is a statement about observed responses, not merely nearby lattice
  edges in the implementation.
- Every registered trial contributes. Outcome-based rejection, missing-click
  deletion and setting-dependent coincidence pairing are not allowed.

For a deterministic realization at fixed lambda,

`s=A_0*(B_0+B_1)+A_1*(B_0-B_1)`.

One bracket is zero and the other is +2 or-2, so |s|=2. Averaging with the same
rho gives

`|E_00+E_01+E_10-E_11| <= 2`.

This short derivation applies to any reversible or irreversible board satisfying
the stated assumptions. It constrains ensemble correlations; a finite-sample
estimate needs its preregistered uncertainty analysis. Reversibility, many
hidden updates and visible branch cancellation do not invalidate the bound.
An apparent violation must first identify which assumption or implementation
check failed, rather than being labeled entanglement automatically.

## Missing outcomes and board locality must be explicit

Freeze trial identifiers, setting assignments, detector regions, time windows,
and the handling of empty or multiple detection records before running. One
valid binary convention is to assign an empty or ambiguous local record `-1`;
another requires its own declared outcome analysis. Preserve the raw records
and all such assignments. C0/C1/C2 are not automatically the binary outcomes;
their detector mapping must also be fixed. A truncated or corrupt capture is
incomplete computation, not a physical no-click result. A result computed only from surviving paired clicks
can have a different hidden-variable ensemble for each setting pair and does
not test the bound above. The original CHSH paper explicitly discusses the
additional detection assumption needed for its proposed inefficient optical
implementation [2]; it must not be silently supplied here.

Construct lambda and the setting-preparation ensemble honestly. Lambda must
retain relevant common causes; dropping a correlated apparatus field does not
make settings independent. Conversely, defining lambda as the entire universe
including the setting registers makes the desired independence assumption
inapplicable. The model must specify a meaningful partition and justify the
factorization used in the test.

Board locality means one update propagates influence at most one graph edge.
Operational spacelike separation needs a separate mapping from board states to
detector positions, local times and a calibrated signal speed. Audit the full
causal cones from the earliest setting-dependent board state, not merely from
the click at which a setting is displayed. A setting encoded initially may
have time to influence a remote apparatus before its recorded “choice.”

If many unrecorded updates allow an acknowledgment or cancellation signal to
travel between the apparatuses before their outputs, the model may remain
board-local while failing observed Bell locality. That is a specific model
choice to analyze, not a free derivation of quantum correlations. It must also
predict stable local marginal statistics under remote setting changes and a
whole family of joint correlations. A single exclusive route, matched pair of
clicks or common clock phase does not supply those predictions or a Born rule.

## Board updates, event counts and physical elapsed time

Let `N_C(t)` count registered raw C events through board update t. An interval
with no C events has `Delta N_C=0`. It can still contain many board updates and
different complete states. Calling this interval zero physical elapsed time
requires a separately derived clock/readout law; it does not follow from the
absence of an event.

The analyst's accumulated count is not automatically a native stored record.
On an exact full-board periodic orbit, the board state can repeat while an
external counter of its events keeps increasing. Therefore that unbounded count
is not a function of the current board state alone. An internal cycle count
needs actual counter/remainder degrees of freedom that preserve it, with stated
capacity and readout behavior.

Similarly, the increasing ordering of a saved event list is imposed by the
forward recording procedure. A physical arrow requires persistent internal
records, their preparation and stability conditions, and a quantitative account
of information remaining elsewhere under reversal. The audited
[phase-record comparison](evidence/phase_record_information_location.json)
illustrates the distinction:after a probe, local clock histories coincide while
external counter/remainder differences remain. It is not an irreversible
microscopic collapse or a permanent local measurement record.

An invariant observed light speed would require calibrated signal exchanges
between moving emitters, receivers and clocks, predicting the same operational
speed across declared preparations with errors. The lattice causal bound and
an individual packet velocity are insufficient. Camera rotation does not move
the apparatus. A native clock's phase, raw C event count and a detector's stored
elapsed-time record are three different observables until their relation is
derived and tested.

## Next acceptance gates

1. Realize two independently readable local settings and detector records,
   including no-click and multiple-click outcomes, under unchanged Rule3.
2. Freeze the preparation ensemble, trial pairing, outcome map and causal-cone
   audit. State exactly which locality and setting-independence assumptions hold.
3. Predict and test all four correlation tables plus local marginals, with every
   registered trial retained and an uncertainty rule fixed before validation.
4. Separately test moving-clock calibration and internally retained event counts.
   A success in a correlation test does not establish a clock law, or conversely.

These are prerequisites for a quantum/time claim, not newly implemented gates
in the engine. Neither an observer nor an approval algorithm may change a state,
select an outcome or erase a history during a run.

## Primary sources

Checked2026-11-08. The sources support the Bell/CHSH context; the board mapping,
counting distinction and proposed acceptance gates are the analysis above.

1. J. S. Bell, *On the Einstein Podolsky Rosen paradox*, Physics Physique
   Fizika1,195–200(1964). Publisher's complete six-page PDF inspected:
   <https://journals.aps.org/ppf/pdf/10.1103/PhysicsPhysiqueFizika.1.195>.
   The CERN copy was blocked by a browser-verification page; the publisher copy
   supplied the primary text.
2. J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt, *Proposed Experiment
   to Test Local Hidden-Variable Theories*, Physical Review Letters23,880–884
   (1969), DOI<https://doi.org/10.1103/PhysRevLett.23.880>. Complete original
   five-page paper scan inspected, including locality, setting independence
   and the detection discussion:
   <https://www.informationphilosopher.com/solutions/scientists/bell/CHSH.pdf>.
