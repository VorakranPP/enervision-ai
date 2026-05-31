# db_paths.py
# Centralized database path constants for dashboard

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

DB_ENERGY = _ROOT / "backend" / "energy_data.db"
DB_EV     = _ROOT / "backend" / "ev_data.db"
