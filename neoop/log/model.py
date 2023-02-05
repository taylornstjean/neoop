import os
from datetime import datetime as dt

from config import LOG_DIR

neocp_log_path = os.path.join(LOG_DIR, "neocp.log")


def neocp_last_save():
    """Check when last neocp file pull occurred. If no data saved, returns None."""

    try:
        with open(neocp_log_path, "rb") as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            try:
                return float(f.readline().decode())
            except ValueError:
                return None
    except FileNotFoundError:
        with open(neocp_log_path, "w") as f:
            pass
        return None


def neocp_log_save():
    """Log neocp file pull."""

    with open(neocp_log_path, "a") as f:
        entry = f"{dt.utcnow().timestamp()}\n"
        f.write(entry)
