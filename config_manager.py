"""Config and key storage for GrokBot Free."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_FILE = HERE / "user_config.json"

DEFAULT_CONFIG = {
    "api_provider": "openrouter",  # openrouter or grok_xai
    "api_key": "",
    "model": "nvidia/nemotron-3.5-lightning:free",
    "base_url": "https://openrouter.ai/api/v1",
}


def load_config() -> dict:
    if CONFIG_FILE.is_file():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            merged = dict(DEFAULT_CONFIG)
            merged.update(data)
            return merged
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_config(data: dict):
    try:
        CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass
