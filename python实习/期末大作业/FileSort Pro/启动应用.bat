@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo =====================================
echo   FileSort Pro 启动脚本
echo =====================================
echo.

echo [准备] 正在清理旧进程...
taskkill /F /IM python.exe >nul 2>&1
echo.

echo [启动中] 正在启动应用...
echo 应用将在浏览器中自动打开
echo 按 Ctrl+C 可停止应用
echo.

python -m streamlit run app.py

pause
