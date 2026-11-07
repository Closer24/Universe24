"""Generic, data-only assembly for the unchanged Universe24 reference engine."""
from .spec import BoardSpec, TensorSpec, Patch, Socket, Placement, place, plain
from .recipes import SignalSource, GuideSegment, Receiver, PairedArm, GuidedPacketSource
from .compose import PreparedBoard, finalize

__all__ = ['BoardSpec', 'TensorSpec', 'Patch', 'Socket', 'Placement', 'place', 'plain',
           'SignalSource', 'GuideSegment', 'Receiver', 'PairedArm', 'GuidedPacketSource', 'PreparedBoard', 'finalize']
