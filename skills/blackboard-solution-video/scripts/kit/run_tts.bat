@echo off
chcp 65001 >nul
REM 配音：讀本資料夾 segments.py → audio\*.wav、durations.json
REM 只重配某幾段：run_tts.bat --only s05,s12
REM 預設用 Azure（zh-TW-HsiaoChenNeural）；要改回 Gemini 把下一行改成 tts_gemini.py
cd /d "%~dp0"
python tts_azure.py %*
pause
