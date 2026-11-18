@echo off
chcp 65001 >nul
cd /d "%~dp0"
call build.bat cloth
if errorlevel 1 (
  pause
  exit /b 1
)
if exist "output\" (
  for %%F in ("output\*.pdf") do echo PDF: %%~fF
)
exit /b 0
