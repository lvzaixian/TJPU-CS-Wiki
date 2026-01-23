from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from . import config_manager
from . import file_utils

# 项目根目录 = src 上一级目录
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_PATH = LOG_DIR / "operation.log"


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _append_log(message: str) -> None:
    """将一条日志写入 operation.log。"""
    _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)


class FileSorterHandler(FileSystemEventHandler):
    """基于配置的文件整理事件处理器。"""

    def __init__(
        self,
        config_loader: Callable[[], Dict[str, Any]] | None = None,
        log_callback: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__()
        self._config_loader = config_loader or config_manager.load_config
        # 可选日志回调（例如写入队列），注意：不要在回调里直接操作 Streamlit 组件
        self._log_callback = log_callback
        # 记录正在处理的文件，避免重复整理
        self._processing_files: set[str] = set()

    def on_created(self, event: FileSystemEvent) -> None:  # type: ignore[override]
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        
        # 避免重复处理同一个文件
        file_key = str(src_path.resolve())
        if file_key in self._processing_files:
            return
        
        if not src_path.exists() or not src_path.is_file():
            return

        # 标记为正在处理
        self._processing_files.add(file_key)

        config = self._config_loader()
        rules: Dict[str, Any] = config.get("rules", {})

        suffix = src_path.suffix.lower()
        target_category: Optional[str] = None
        for category, exts in rules.items():
            if isinstance(exts, (list, tuple)) and suffix in [str(e).lower() for e in exts]:
                target_category = category
                break

        # 未匹配到则归类为 Others
        if target_category is None:
            target_category = "Others"

        target_root = Path(config.get("target_directory", src_path.parent))
        target_dir = target_root.expanduser() / target_category

        try:
            # 等待文件写入完成（简单延迟）
            import time
            time.sleep(0.5)
            
            # 再次检查文件是否存在（可能已被其他进程处理）
            if not src_path.exists():
                self._processing_files.discard(file_key)
                return
            
            final_path = file_utils.move_file(src_path, target_dir)
            # 简洁日志：只显示文件名和目标分类
            msg = f"✅ {src_path.name} → {target_category}"
            _append_log(msg)
            if self._log_callback is not None:
                try:
                    self._log_callback(msg)
                except Exception:
                    pass
        except PermissionError:
            # 权限错误静默跳过，不记录日志
            pass
        except Exception as exc:  # noqa: BLE001
            # 所有错误都静默处理，保持日志整洁
            pass
        finally:
            # 处理完成后移除标记
            self._processing_files.discard(file_key)


def start_watching(path: str | Path) -> Observer: # type: ignore
    """在后台启动目录监听，返回 Observer 实例。

    调用方负责保存返回的 observer 引用，并在需要时调用 stop_watching 停止监听。
    """
    watch_path = Path(path).expanduser()
    if not watch_path.exists() or not watch_path.is_dir():
        raise NotADirectoryError(f"监控目录不存在或不是目录: {watch_path}")

    event_handler = FileSorterHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)

    # 使用单独线程启动 observer，避免阻塞调用方
    thread = threading.Thread(target=observer.start, daemon=True)
    thread.start()

    return observer


def stop_watching(observer: Optional[Observer], timeout: float = 5.0) -> None: # type: ignore
    """停止给定的 Observer。"""
    if observer is None:
        return

    observer.stop()
    observer.join(timeout)
