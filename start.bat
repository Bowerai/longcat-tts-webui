@echo off
chcp 65001 >nul
echo 🚀 启动 LongCat-AudioDiT WebUI...
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
    echo.
)

REM 激活虚拟环境
echo ✅ 激活虚拟环境...
call venv\Scripts\activate.bat
echo.

REM 检查依赖
echo 📥 检查依赖...
pip install -r requirements.txt -q
echo.

REM 启动 WebUI
echo 🎤 启动 WebUI 服务...
echo 📱 访问地址：http://localhost:7860
echo 💡 按 Ctrl+C 停止服务
echo.
python app.py

pause
