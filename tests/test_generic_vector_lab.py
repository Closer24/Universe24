"""Run the opt-in lab contract suite through the repository's normal gate."""

import subprocess
import sys
from pathlib import Path


def test_standalone_vector_lab_contracts():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "-m", "pytest", "tools/generic_vector_lab", "-q"],
        cwd=root,
        check=True,
    )
