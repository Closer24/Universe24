"""Generic, data-only assembly for the unchanged Universe24 reference engine."""
from .spec import BoardSpec, TensorSpec, Patch, Socket, Placement, place, plain
from .recipes import SignalSource, GuideSegment, Receiver, PairedArm, GuidedPacketSource
from .compose import PreparedBoard, finalize
from .clocks import LocalizedSixClock, CompactFiveClock, CooperativeClockPair
from .packets import EvenPacketSource, RemainderTarget, RegisterWriter, SourceOverlapRegister
from .assemblies import assemble_scatterer, assemble_remainder_register

__all__ = ['BoardSpec', 'TensorSpec', 'Patch', 'Socket', 'Placement', 'place', 'plain',
           'SignalSource', 'GuideSegment', 'Receiver', 'PairedArm', 'GuidedPacketSource', 'PreparedBoard', 'finalize',
           'LocalizedSixClock', 'CompactFiveClock', 'CooperativeClockPair', 'EvenPacketSource',
           'RemainderTarget', 'RegisterWriter', 'SourceOverlapRegister',
           'assemble_scatterer', 'assemble_remainder_register']
