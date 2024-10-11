from pathlib import Path
import sys

from factory.random import reseed_random

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, root_dir.as_posix())
sys.path.insert(1, (root_dir / "app").as_posix())

reseed_random(0)


if __name__ == "__main__":
    from scripts.seed_data import seed_auth
