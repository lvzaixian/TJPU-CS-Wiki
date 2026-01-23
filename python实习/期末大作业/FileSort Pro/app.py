from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import json
import altair as alt
import pandas as pd
import streamlit as st

from src import config_manager
from src import file_utils
from src import organizer


st.set_page_config(page_title="FileSort Pro", layout="wide")


def get_project_root() -> Path:
    return Path(__file__).resolve().parent


def load_runtime_config() -> Dict[str, Any]:
    if "config" not in st.session_state:
        st.session_state["config"] = config_manager.load_config()
    return st.session_state["config"]


def save_runtime_config(cfg: Dict[str, Any]) -> None:
    st.session_state["config"] = cfg
    config_manager.save_config(cfg)


def init_session_state() -> None:
    cfg = load_runtime_config()
    st.session_state.setdefault("monitor_path", cfg.get("target_directory", ""))
    st.session_state.setdefault("watching", False)
    st.session_state.setdefault("observer", None)
    st.session_state.setdefault("favorite_dirs", cfg.get("favorite_dirs", []))


def sidebar_controls() -> None:
    st.sidebar.title("⚙️ 配置与控制")

    cfg = load_runtime_config()

    # 监控目录设置
    st.sidebar.markdown("**监控目录**")
    monitor_path = st.session_state.get("monitor_path", cfg.get("target_directory", ""))

    # 1. 常用目录管理（增删改）
    favorite_dirs = st.session_state.get("favorite_dirs", [])
    if not favorite_dirs:
        home = Path.home()
        favorite_dirs = [
            str(home / "Downloads"),
            str(home / "Desktop"),
        ]
        st.session_state["favorite_dirs"] = favorite_dirs

    st.sidebar.markdown("📚 **常用目录管理**")
    
    # 增加新常用目录
    with st.sidebar.expander("➕ 添加新常用目录"):
        # 使用独立变量控制输入框初始值
        input_key = "new_favorite_input"
        if "clear_input_trigger" not in st.session_state:
            st.session_state["clear_input_trigger"] = 0
        
        new_fav = st.text_input(
            "输入路径",
            value="",
            key=f"{input_key}_{st.session_state['clear_input_trigger']}",
            placeholder="例: D:\\MyFolder",
        )
        
        if st.button("添加", key="add_new_fav_btn"):
            if new_fav and Path(new_fav).exists():
                if new_fav not in favorite_dirs:
                    favorite_dirs.append(new_fav)
                    st.session_state["favorite_dirs"] = favorite_dirs
                    cfg["favorite_dirs"] = favorite_dirs
                    save_runtime_config(cfg)
                    # 触发清空输入框（通过改变key）
                    st.session_state["clear_input_trigger"] += 1
                    st.success(f"✅ 已添加: {new_fav}")
                    st.rerun()
                else:
                    st.info("该目录已存在")
            else:
                st.error("路径不存在或为空")
    
    # 编辑/删除现有常用目录
    if favorite_dirs:
        for idx, fav in enumerate(favorite_dirs):
            with st.sidebar.expander(f"📁 {Path(fav).name or fav}"):
                edited_path = st.text_input("路径", value=fav, key=f"edit_fav_{idx}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("保存修改", key=f"save_fav_{idx}"):
                        if edited_path and Path(edited_path).exists():
                            favorite_dirs[idx] = edited_path
                            st.session_state["favorite_dirs"] = favorite_dirs
                            cfg["favorite_dirs"] = favorite_dirs
                            save_runtime_config(cfg)
                            st.success("✅ 已更新")
                            st.rerun()
                        else:
                            st.error("路径无效")
                with col2:
                    if st.button("✖ 删除", key=f"del_fav_{idx}"):
                        favorite_dirs.pop(idx)
                        st.session_state["favorite_dirs"] = favorite_dirs
                        cfg["favorite_dirs"] = favorite_dirs
                        save_runtime_config(cfg)
                        st.success("✅ 已删除")
                        st.rerun()

    st.sidebar.markdown("---")

    # 2. 快速选择常用目录
    quick_options = ["手动输入"] + favorite_dirs
    quick_choice = st.sidebar.selectbox(
        "📌 快速选择常用目录",
        quick_options,
        index=0,
        help="从常用目录中选择，或选择'手动输入'后在下方输入任意路径。",
    )
    if quick_choice != "手动输入":
        monitor_path = quick_choice

    # 3. 监控路径输入框（可随意输入）
    monitor_path = st.sidebar.text_input(
        "📂 当前监控路径",
        value=monitor_path,
        help="可以手动输入/粘贴任意路径，也可以从上方常用目录中选择。",
    )

    # 保存监控路径到 session_state 和配置
    st.session_state["monitor_path"] = monitor_path
    cfg["target_directory"] = monitor_path
    save_runtime_config(cfg)

    # 规则编辑（简单用文本区展示 JSON，可按需要换成 data_editor）
    st.sidebar.subheader("整理规则 (JSON)")
    rules_json = st.sidebar.text_area("rules", value=json.dumps(cfg.get("rules", {}), ensure_ascii=False, indent=2))

    if st.sidebar.button("保存配置"):
        try:
            rules = json.loads(rules_json)
            cfg["rules"] = rules
            save_runtime_config(cfg)
            st.sidebar.success("配置已保存")
        except Exception as exc:  # noqa: BLE001
            st.sidebar.error(f"保存配置失败: {exc}")

    st.sidebar.markdown("---")

    # 启动 / 停止监控
    watching = st.session_state.get("watching", False)
    status_text = "🔴 已停止" if not watching else "🟢 运行中"
    st.sidebar.markdown(f"**当前状态：{status_text}**")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("启动整理", disabled=watching, key="start_btn"):
            try:
                observer = organizer.start_watching(monitor_path)
                st.session_state["observer"] = observer
                st.session_state["watching"] = True
                st.rerun()
            except Exception as exc:  # noqa: BLE001
                st.sidebar.error(f"启动失败: {exc}")
    with col2:
        if st.button("停止整理", disabled=not watching, key="stop_btn"):
            try:
                organizer.stop_watching(st.session_state.get("observer"))
            finally:
                st.session_state["watching"] = False
                st.session_state["observer"] = None
                st.rerun()


def read_logs(max_lines: int = 100) -> str:
    project_root = get_project_root()
    log_path = project_root / "logs" / "operation.log"
    if not log_path.exists():
        return "暂无日志记录。"

    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-max_lines:]
        return "".join(lines) or "暂无日志记录。"
    except Exception:
        return "暂无日志记录。"


def main_panel() -> None:
    st.title("📂 FileSort Pro — 智能文件整理机器人")

    cfg = load_runtime_config()
    target_dir = Path(cfg.get("target_directory", "")).expanduser()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 文件类型分布")
        if target_dir.exists() and target_dir.is_dir():
            try:
                df_stats = file_utils.scan_directory_stats(target_dir)
                if not df_stats.empty:
                    chart = (
                        alt.Chart(df_stats)
                        .mark_arc()
                        .encode(theta="count", color="extension", tooltip=["extension", "count"])
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("当前目录下没有可统计的文件。")
            except Exception as exc:  # noqa: BLE001
                st.error(f"统计文件分布时出错: {exc}")
        else:
            st.warning("目标监控目录不存在或不可访问，请在侧边栏中重新配置。")

    with col_right:
        st.subheader("📈 今日整理概览")
        logs_text = read_logs(max_lines=1000)
        log_lines = [line for line in logs_text.splitlines() if "✅" in line]
        total_files = len(log_lines)
        
        # 主指标
        st.metric("📄 今日整理文件数", value=total_files)
        
        # 预估节省时间（按每个文件手动整理需要5秒计算）
        saved_seconds = total_files * 5
        if saved_seconds >= 60:
            saved_time = f"{saved_seconds // 60} 分 {saved_seconds % 60} 秒"
        else:
            saved_time = f"{saved_seconds} 秒"
        st.metric("⏱️ 预估节省时间", value=saved_time)
        
        # 各分类统计
        if log_lines:
            st.markdown("**📊 分类统计**")
            category_counts = {}
            for line in log_lines:
                # 解析日志格式: ✅ 文件名 → 分类
                if "→" in line:
                    category = line.split("→")[-1].strip()
                    category_counts[category] = category_counts.get(category, 0) + 1
            
            for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
                st.text(f"  {cat}: {count} 个文件")
        
        # 最近整理时间
        if log_lines:
            last_line = log_lines[-1]
            # 提取时间戳
            if "[" in last_line and "]" in last_line:
                last_time = last_line.split("]")[0].replace("[", "").strip()
                st.caption(f"🕒 最近整理: {last_time}")

    st.markdown("---")

    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.subheader("🧾 实时日志控制台")
    with col_btn:
        if st.button("🔄 刷新", key="refresh_btn"):
            st.cache_data.clear()
            st.toast("已刷新")
            st.rerun()
    
    log_text = read_logs(max_lines=200)
    st.code(log_text, language=None)


def main() -> None:
    init_session_state()
    sidebar_controls()
    main_panel()


if __name__ == "__main__":
    main()
