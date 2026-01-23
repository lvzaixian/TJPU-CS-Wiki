from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# 项目根目录 = src 上一级目录
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_PATH = CONFIG_DIR / "sorting_rules.json"


DEFAULT_CONFIG: Dict[str, Any] = {
    "target_directory": "~/Downloads",
    "rules": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi", ".dmg"],
    },
}


def _ensure_config_dir() -> None:
    """确保配置目录存在。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """加载配置文件。

    如果配置文件不存在，则创建并写入默认配置。
    返回配置字典，调用方可以直接使用/修改后再通过 save_config 持久化。
    """
    _ensure_config_dir()

    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 简单兜底：缺失字段时填充默认值
    if "target_directory" not in data:
        data["target_directory"] = DEFAULT_CONFIG["target_directory"]
    if "rules" not in data:
        data["rules"] = DEFAULT_CONFIG["rules"]

    return data


def save_config(new_config: Dict[str, Any]) -> None:
    """保存配置到 sorting_rules.json。

    调用方负责保证 new_config 的结构正确（包含 target_directory 与 rules）。
    """
    _ensure_config_dir()

    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_config, f, ensure_ascii=False, indent=2)
