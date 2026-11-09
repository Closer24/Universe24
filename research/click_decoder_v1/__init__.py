"""Generic click decoder: physics read only from Universe24 click logs (see README.md).

Two frozen versions live side by side: v1.0 (``decoder.py``, the reference for every claim made
with it) and v1.1 (``decoder_v11.py``). ``decode`` is v1.0; ``decode_v11`` is v1.1.

    from research.click_decoder_v1 import read_log, decode, decode_v11
    events, info = read_log("runs/my_run.events.jsonl")
    report = decode(events, side=48, horizon=36, log_info=info)          # v1.0
    report = decode_v11(events, side=48, horizon=36, c=None)              # v1.1
"""
from .correlate import chsh, correlations
from .decoder import NAME, VERSION, decode, load_config, read_log
from .decoder_v11 import decode as decode_v11, read_log as read_log_v11
from .layers import diff, peak_arrival

DECODERS = {"1.0": decode, "1.1": decode_v11}

__all__ = ["DECODERS", "NAME", "VERSION", "chsh", "correlations", "decode", "decode_v11", "diff", "load_config",
           "peak_arrival", "read_log", "read_log_v11"]
