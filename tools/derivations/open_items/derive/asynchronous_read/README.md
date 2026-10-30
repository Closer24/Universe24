# Item (u), the asynchronous read: past against lin, on the stage 3 engine

The question (TENSOR24_PLAN.md, section 14, item 21; the ruling's line 5 and its note on lin): a Node-clock reads a neighbour as of its own count c. **past** reads the neighbour's now slot where its tn is at most c, else its before slot. **lin** reads the straight line between the two slots by the local times, one carry by tn - tb, at least 1 since the before slot is older. The plan recommends lin, as David and Sofer recommend, and its formula is owed before stage 3.

**The finding (CHECKED, probe.py on the stage 3 engine; its output probe_out.txt):**
- In the synchronous main run no neighbour stands ahead of its reader, so every read is its now slot, and past and lin agree.
- Under the runner's masks a neighbour stands at most one count ahead (the due beat waits for every neighbour at the reader's count). Its now slot then holds its next tick, written at tn = c + 1.
- past reads the before slot there, which is the neighbour's state as of c: forty random schedules equal the synchronous pass in 40 of 40, with the rates and the teeth parted and one clock stopped.
- lin reads the line toward that next tick, which the synchronous pass cannot see at the count c: 0 of 40.

So lin as one carry by tn - tb breaks the order test, the stage 3 test that can fail. It can hold only with a synchronous pass that reads at the half tick too, which is David's to give.

**In the engine:** stage 3 reads by past (engine/mesh.py, seen), the ruling's line 5.

**Words:** David's, past (6478324607): in the ruling's beat no neighbour stands more than one count ahead, so its state as of c is one of its two slots, and past reads it exactly; lin inside the beat engine is the line toward a slot written a count ahead, breaking the order test and the cone in counts (1,851 of 6,724 reached sites early, against 0 of 6,563 under past); it gains nothing for the reversal. Its price, for the owner: where the dials part, the gears' run back after the turnover is not the forward run's mirror, while the rewind stays exact through the outs. Sofer's, past (6476698665). The owner's word on the change from the plan's lin is asked.
