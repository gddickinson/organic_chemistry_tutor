"""Cross-platform paths for data, config, logs, and cache.

Uses ``platformdirs`` so the application lands in
``~/Library/Application Support/OrgChem`` on macOS,
``~/.local/share/OrgChem`` on Linux,
and ``%APPDATA%\\OrgChem`` on Windows.
"""
from __future__ import annotations
from pathlib import Path
from platformdirs import user_data_dir, user_config_dir, user_log_dir, user_cache_dir

_APP_NAME = "OrgChem"
_APP_AUTHOR = "OrgChem"


def data_dir() -> Path:
    p = Path(user_data_dir(_APP_NAME, _APP_AUTHOR))
    p.mkdir(parents=True, exist_ok=True)
    return p


def config_path() -> Path:
    p = Path(user_config_dir(_APP_NAME, _APP_AUTHOR))
    p.mkdir(parents=True, exist_ok=True)
    return p / "config.yaml"


def log_dir() -> Path:
    p = Path(user_log_dir(_APP_NAME, _APP_AUTHOR))
    p.mkdir(parents=True, exist_ok=True)
    return p


def cache_dir() -> Path:
    p = Path(user_cache_dir(_APP_NAME, _APP_AUTHOR))
    p.mkdir(parents=True, exist_ok=True)
    return p


def sessions_dir() -> Path:
    """Directory that holds saved session-state YAML files (Phase 20d)."""
    p = Path(user_config_dir(_APP_NAME, _APP_AUTHOR)) / "sessions"
    p.mkdir(parents=True, exist_ok=True)
    return p
