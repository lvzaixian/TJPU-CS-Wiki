from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd


def move_file(src: Path | str, dst_dir: Path | str) -> Path:
    """将文件移动到目标文件夹，并在重名时自动追加后缀避免覆盖。

    返回最终文件路径。
    """
    src_path = Path(src)
    dst_dir_path = Path(dst_dir)

    # 检查源文件是否存在
    if not src_path.exists():
        raise FileNotFoundError(f"源文件不存在: {src_path}")
    
    if not src_path.is_file():
        raise ValueError(f"源路径不是文件: {src_path}")

    dst_dir_path.mkdir(parents=True, exist_ok=True)

    target_path = dst_dir_path / src_path.name
    if not target_path.exists():
        target_path = src_path.rename(target_path)
        return target_path

    # 处理重名: xxx.ext -> xxx_copy1.ext / xxx_copy2.ext ...
    stem = src_path.stem
    suffix = src_path.suffix
    index = 1
    while True:
        candidate = dst_dir_path / f"{stem}_copy{index}{suffix}"
        if not candidate.exists():
            target_path = src_path.rename(candidate)
            return target_path
        index += 1


def scan_directory_stats(path: Path | str) -> pd.DataFrame:
    """扫描目录下文件的类型分布，返回用于可视化的 DataFrame。

    当前实现按照文件后缀统计数量，返回列：
    - extension: 扩展名（如 .pdf / .jpg）
    - count: 数量
    """
    root = Path(path)
    if not root.exists() or not root.is_dir():
        raise NotADirectoryError(f"目录不存在或不是目录: {root}")

    extensions: List[str] = []

    for item in root.iterdir():
        if item.is_file():
            extensions.append(item.suffix.lower() or "<no_ext>")

    if not extensions:
        return pd.DataFrame({"extension": [], "count": []})

    series = pd.Series(extensions, name="extension")
    counts = series.value_counts().reset_index()
    counts.columns = ["extension", "count"]
    return counts
