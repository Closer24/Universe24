# Experimental bounded matter transport

This unit-link candidate follows Highlights sections 3.3.3 and 3.5.3.
It fixes receiver contention feeding back to a remote sender in one tick.
It does not fix isolated self-response or prove a gravity law.

## Local law and ownership

- A source launches only if its own outgoing link slot is free.
- Launch removes the particle from source occupancy immediately.
- Each directed face has K fixed outbound slots, addressed by departure slot.
- A packet crosses one unit link in one elementary tick.
- The destination admits completed packets into its own available local slots.
- An unaccepted packet stays link-owned with unchanged mass and momentum.
- Acceptance transfers ownership to the destination exactly once.
- A release acknowledgement takes one further link tick to reach the source.
- A source cannot use receiver acceptance in the departure tick.
- Link-owned particles do not emit from the departure cell or receive cell forces.
- The registry stores each particle payload once; occupancy or a packet owns it.
- A source reservation and its acknowledgement are references, not more mass.

The engine collects outgoing transfers before receiver admission. A newly
admitted particle cannot leave that destination in the same elementary tick.
A lone particle can still move one cell every tick: a fresh cell has free outgoing
slots even while the previous cell awaits its acknowledgement.

## State and bounds

Each cell has six K-slot outbound credit records. Each occupied credit is backed
by either one particle packet or one release acknowledgement. Thus at most 6K
packets/acknowledgements coexist per source; they are not unbounded source histories.
Each destination receives at most 6K completed link slots. The host groups and
visits these records across the world; total host cost is not constant.
Packet routing metadata is departure address, direction, local slot and arrival
tick. The existing particle payload supplies mass, momentum and exact residuals.
The existing signed/zero particle and index encoding remains a documented migration
gap; this change does not claim global positive-integer schema compliance.

## Arbitration and boundaries

Simultaneous completed packets use ascending incoming face ID, then source slot.
This is a local deterministic capacity policy, with no particle-ID or insertion-order
priority. It distinguishes face directions during contention, so rotational symmetry
of contested admission is not established. Continuous preferred-face input can
starve a lower-priority incoming face; fairness is not established. Free movement through available links retains one hop per tick. A one-cell
periodic self-loop can reuse the same outbound slot before its acknowledgement
returns and therefore wait; general periodic free-motion equivalence is not claimed.
Collision-enabled self-loops preserve the existing no-new-encounter rule.

FaceScalarSimulation and FaceStreamSimulation use version 2 buffered-matter model
identities. GenericFaceSimulation uses version 3. Frozen baseline models retain
their historical schedule. FaceLinkedSimulation retains its historical variable-link
transit and is not covered by this unit-link ownership correction. Generalizing the
same packet and acknowledgement mechanism to variable travel times remains work.

## Acceptance

The existing competing-sender intervention compares a sender with and without a
competitor two edges away. Its departure and source credits must agree after one
tick. Every particle must have exactly one owner in cell occupancy or link inventory;
capacity never exceeds K and in-flight records retain their mass and momentum.
Tests additionally retain the source-to-target whole-tick causal comparison and the
existing generic-field integration run. Independent review covers acknowledgement
provenance and the bounded ownership graph, rather than only a green occupancy test.
