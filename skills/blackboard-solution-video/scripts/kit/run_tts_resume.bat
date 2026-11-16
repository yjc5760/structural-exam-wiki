@echo off
chcp 65001 >nul
REM 配音中斷後續跑：已用同一聲音配好的段落會略過
cd /d "%~dp0"
python tts_azure.py --resume %*
pause
