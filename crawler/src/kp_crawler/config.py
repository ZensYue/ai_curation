from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = PACKAGE_ROOT / "data" / "runs"
DEFAULT_AUTH_FILE = PACKAGE_ROOT / "config" / "auth_profiles.json"


def get_data_root() -> Path:
    raw = os.environ.get("KP_CRAWLER_DATA_ROOT")
    return Path(raw).expanduser().resolve() if raw else DEFAULT_DATA_ROOT


def get_auth_file() -> Path:
    raw = os.environ.get("KP_CRAWLER_AUTH_FILE")
    return Path(raw).expanduser().resolve() if raw else DEFAULT_AUTH_FILE


def load_json_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)
