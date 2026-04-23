"""Application configuration, persisted as YAML via platformdirs."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
import logging
from typing import Any, Dict

import yaml

from orgchem.utils.paths import data_dir, config_path, log_dir, cache_dir

log = logging.getLogger(__name__)


@dataclass
class AppConfig:
    db_path: Path = field(default_factory=lambda: data_dir() / "orgchem.sqlite")
    log_dir: Path = field(default_factory=log_dir)
    cache_dir: Path = field(default_factory=cache_dir)
    theme: str = "light"
    log_level: str = "INFO"
    default_3d_style: str = "stick"
    default_3d_backend: str = "3Dmol"   # "3Dmol" | "matplotlib"
    autogen_3d_on_import: bool = True
    online_sources_enabled: bool = True

    @classmethod
    def load(cls) -> "AppConfig":
        cfg_path = config_path()
        if not cfg_path.exists():
            log.info("No config file at %s — using defaults", cfg_path)
            return cls()
        try:
            with open(cfg_path) as f:
                raw: Dict[str, Any] = yaml.safe_load(f) or {}
        except Exception as e:
            log.warning("Could not read %s (%s) — using defaults", cfg_path, e)
            return cls()
        defaults = cls()
        return cls(
            db_path=Path(raw.get("db_path", defaults.db_path)),
            log_dir=Path(raw.get("log_dir", defaults.log_dir)),
            cache_dir=Path(raw.get("cache_dir", defaults.cache_dir)),
            theme=raw.get("theme", defaults.theme),
            log_level=raw.get("log_level", defaults.log_level),
            default_3d_style=raw.get("default_3d_style", defaults.default_3d_style),
            default_3d_backend=raw.get("default_3d_backend", defaults.default_3d_backend),
            autogen_3d_on_import=raw.get("autogen_3d_on_import", defaults.autogen_3d_on_import),
            online_sources_enabled=raw.get("online_sources_enabled", defaults.online_sources_enabled),
        )

    def save(self) -> None:
        cfg_path = config_path()
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        data = {k: (str(v) if isinstance(v, Path) else v) for k, v in asdict(self).items()}
        with open(cfg_path, "w") as f:
            yaml.safe_dump(data, f)
        log.info("Config saved to %s", cfg_path)
