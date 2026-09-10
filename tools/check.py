"""Run the project's required local gates from any working directory."""

import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
commands = [
    ["ruff", "check", "."],
    ["ruff", "format", "--check", "."],
    ["mypy", "--python-version", f"{sys.version_info.major}.{sys.version_info.minor}"],
    ["pytest", "--junitxml=artifacts/junit.xml"],
]
for command in commands:
    subprocess.run([sys.executable, "-m", *command], cwd=root, check=True)
