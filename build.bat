@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if not defined PY (
  if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)
if not defined PY (
  echo Python 3 not found. Install Python 3.10 or newer and tick "Add Python to PATH".
  pause
  exit /b 1
)

%PY% -c "import markdown, pymupdf, matplotlib, numpy, PIL" >nul 2>nul
if errorlevel 1 (
  echo Installing dependencies ...
  %PY% -m pip install -q markdown pymupdf matplotlib numpy pillow
)

if "%~1"=="" goto :all
if /i "%~1"=="figures" goto :figures
if /i "%~1"=="sidebar" goto :sidebar
if /i "%~1"=="all" goto :all
call :one %~1
if errorlevel 1 goto :err
echo Done.
exit /b 0

:one
echo.
echo ===== building %1 =====
%PY% "books\build\build.py" --book %1
exit /b %errorlevel%

:figures
%PY% "books\code\make_figures.py"
if errorlevel 1 goto :err
echo Done.
exit /b 0

:sidebar
%PY% "books\build\make_sidebar.py"
if errorlevel 1 goto :err
echo Done.
exit /b 0

:all
%PY% "books\code\make_figures.py"
if errorlevel 1 goto :err
for %%B in (beginner cloth hair sss spectral aniso-metal voxel wave-optics reservoir sdf physics) do (
  if exist "books\%%B\structure.json" (
    call :one %%B
    if errorlevel 1 goto :err
  )
)
%PY% "books\build\make_sidebar.py"
if errorlevel 1 goto :err
echo.
echo All books built.
exit /b 0

:err
echo.
echo *** Build failed, see the message above ***
pause
exit /b 1
