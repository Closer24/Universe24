"""Compatibility entry point; implementation is part of Universe24."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from universe24.runtime import *  # noqa: F401,F403

if __name__ == "__main__":
    main()
