"""Include the same-run evidence boundary tests in normal repository CI."""
from pathlib import Path


def load_tests(loader, tests, pattern):
    root = Path(__file__).resolve().parents[2]
    return loader.discover(str(root / 'validation/geodesic_board'),
                           pattern='test_*.py', top_level_dir=str(root))
