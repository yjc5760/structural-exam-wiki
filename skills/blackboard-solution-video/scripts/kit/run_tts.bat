@echo off
chcp 65001 >nul
REM 配音：讀本資料夾 segments.py → audio\*.wav、durations.json
REM 只重配某幾段：run_tts.bat --only s05,s12
REM 改用 Azure：把下一行的 tts_gemini.py 改成 tts_azure.py
cd /d "%~dp0"
python tts_gemini.py %*
pause
