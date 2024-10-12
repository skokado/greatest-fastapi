from pathlib import Path
import sys

app_root_dir = Path(__file__).resolve().parent
sys.path.insert(0, app_root_dir.as_posix())
