"""
psql interpreter to the database.
psql -h localhost -U postgres -d {DATABASE_NAME}
"""
import os
from pathlib import Path
import signal
import subprocess
import sys

sys.path.insert(0, Path(__file__).resolve().parent.parent.as_posix())

from app.config import settings

os.environ.setdefault("PGPASSWORD", settings.DATABASE_PASSWORD)


def preexec_function():
    # https://stackoverflow.com/a/5050521
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.
    signal.signal(signal.SIGINT, signal.SIG_IGN)


subprocess.run(
    [
        "psql",
        "-h",
        settings.DATABASE_HOST,
        "-U",
        settings.DATABASE_USER,
        "-d",
        settings.DATABASE_NAME,
    ],
    # preexec_fn=preexec_function,
)
