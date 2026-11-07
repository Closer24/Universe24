"""Report a runtime-dependent JSON I/O limit without changing the engine or guard.

Run from the repository root: python -m research.reliability.known_limits.serialization_probe
The integer is specified by an exact generator to avoid serializing the failing
5001-digit value in this diagnostic's own output. This is outside the bounded
100-digit checkpoint acceptance domain, not a failed Rule3 inverse.
"""
import hashlib
import json
from pathlib import Path
import platform
import sys
from universe24 import Channel, Cube, Engine, State
from universe24.experiments import checkpoint_data


def probe():
    root = Path(__file__).resolve().parents[3]
    initial = State(Cube(3), cells={(0,0,0,0): Channel(10**5000,0,2)})
    engine = Engine()
    final = engine.advance(initial)
    error = None
    try:
        json.dumps(checkpoint_data(initial, engine, 0))
        serialized = True
    except ValueError as failure:
        serialized = False
        error = str(failure)
    return {'case': '5001_decimal_digit_counter', 'python': platform.python_version(),
            'integer_string_limit': sys.get_int_max_str_digits(),
            'source_engine_commit': 'ed1556e202eb0f3cc60342c75d44012c2eeb71c3',
            'probe_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'source_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted((root/'universe24').rglob('*.py'))},
            'preparation': {'side':3,'signs':[1,1,1],'background':[0,0,2],
                            'address':[0,0,0,0],'a_generator':'10**5000','b':0,'r':2},
            'forward_inverse':engine.rewind(final)==initial,
            'checkpoint_json_serialization':serialized,'error':error,
            'scope':'Runtime-dependent serialization limitation; no guard or core change applied.'}


if __name__ == '__main__':
    print(json.dumps(probe(), indent=2))
