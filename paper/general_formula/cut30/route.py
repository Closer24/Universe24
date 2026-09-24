"""The opening of the section on how the algebra was reached (the Boss's order
of 2026-09-24, 01:00Z: the old-law sections to history, each replaced by
docs/ALGEBRA.md chapters 1 to 3 and 8 in the owner's order): the paper's
statement of ALGEBRA.md chapter 7, items (i), (ii) and (v) (the one choice
and the seven Nodes; what the choice forces, the 48 and the 24 within them;
the owner's sentence), placed by cut30/records.py before the paragraph "From
the operations to the group" (chapter 1.3, already in the paper). The two
direction tables, the simulator's part and the old dictionary of the rows
that hop, as the paper carried them, move whole to the records file. Nothing
here is written anew; every sentence is the algebra document's.
"""

OPENING = r"""\paragraph{The one choice, and the seven Nodes.} The one choice of the model is the six Ports of a Node, $P = \{\pm x, \pm y, \pm z\}$ with the opposite involution, the $L^1$ neighbourhood of the cubic lattice: a Node and its six neighbours, the seven Nodes of the causal front, one message per Link per interval in each direction (Section~\ref{sec:algebra}). Two more choices, and no fourth: the phase circle $\Z_{\Nphi}$, $\Nphi$ per world, and the translation group of the torus, $\Z_X \times \Z_Y \times \Z_Z$, each factor a circle or a segment; the point group is then forced and is already the largest, the translation group is the board, and the only freedom that changes the physics is the neighbourhood, through the front, $c$ and the tables \cite[chapter 7]{algebra}.

\paragraph{What the choice forces: the $48$, and the $24$ within them.} What is not chosen is the group of $48$: every map that preserves the six Ports as a set and the lattice's Links is one of the signed permutations of the three axes, $3! \times 2^3 = 48$, and every one of them does; no three-dimensional lattice has a point group of order above $48$ \cite[chapter 7]{algebra}, and the cubic lattice's is the full octahedral group of that order, so this lattice keeps the $48$ and no more. Nothing was added to it: the mass, the charge and the other contents of the family table live on the amounts, on which the $48$ act trivially. The only $\Z$-linear bijections that preserve the cone of one Link per interval are these $48$; a boost is not $\Z$-linear, so no boost is among them, and Lorentz's form is reached Outside from the clicks (Section~\ref{sec:click}) and not as a symmetry of the lattice. The determinant splits the $48$: the $24$ rotations, the group of order $24$, isomorphic to $S_4$ on the cube's four body diagonals, and the $24$ reflections; the hand, needed to carry spin and polarisation, is the pseudoscalar that tells them apart, $h \mapsto \det(g)\,h$ (Theorem~\ref{th:group}); the $24$ are the octahedron's rotations, not a numeral chosen. The GameBoard showed that everything converges to this group and this ring, and what did not converge was not put in (the author's sentence, record 1109 \cite{log}).

"""
