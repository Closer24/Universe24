# Universe24 development constraints

- One board, 48 channels, complete integer (a,b,r) state per channel.
- Periodic cubic lattice (Z/LZ)^3, L >= 3, exactly six spatial neighbors per channel.
- Fixed group-derived 2O coupling, body actions (0,1,3), optional fixed +/- sign per body axis.
- No on-site links, second board, discarded remainders, runtime coupling changes, or floating counters.
- core/rule3.py:forward is the ONLY scalar forward state-changing operation.
- Every new state is computed solely from the same previous state and six spatial inputs.
- No detector, atom, click, veto, reset, time-reversal, or experiment-specific state-changing gates.
- Observation is external and read-only; C2 is NOT a proven physical selection mechanism.
- Inverse methods are for auditing, not part of forward simulation.
- Seeds/configuration are data, never injected after the run starts.
- Q is an algebraic signed account, not established physical energy.
- Use python -m unittest discover -s tests -v; tests do not establish a physical theory.
