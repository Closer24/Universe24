"""The algebra of the frozen mark against the cycle lay's content (sb1): the law's own integers through the engine's readers, no hand-written number."""
import sys
from event_universe.core import paces
from event_universe.features import volume

gamma = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
frozen = paces.certified(gamma)
print("gamma", gamma)
print("frozen content (least content with the Link pace 0)", frozen)
print("clock at the frozen content", paces.clock(gamma, frozen))
print("clock at the content before it", paces.clock(gamma, frozen - 1))
print("link pace at the content before it", paces.link_pace(gamma, frozen - 1))
print("half the wall", gamma // 2)
xf = int(volume.volume_of(gamma, [frozen])[0])
print("X at the frozen content", xf, "bits", xf.bit_length())
for a in (0, 771, 1047, 2157, 2518, 3793):
    x = int(volume.volume_of(gamma, [a])[0])
    print("content", a, "X", x, "bits", x.bit_length())
for x in (1000, 2070, 21888, 3886000000, 4268834097):
    print("X", x, "content", int(volume.level_of(gamma, [x])[0]))
