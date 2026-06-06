@echo off
set /p RESOLVE_PATH="Enter the path to DaVinci Resolve (enter for C:\Program Files\Blackmagic Design\DaVinci Resolve): "
if "%RESOLVE_PATH%"=="" (
    set RESOLVE_PATH=C:\Program Files\Blackmagic Design\DaVinci Resolve
)
if not exist "%RESOLVE_PATH%\fusionscript.dll" (
    echo The specified path does not contain fusionscript.dll. Please check the path and try again.
    pause
    exit /b
)

net session >nul 2>&1
if %errorlevel% neq 0 (
    setx RESOLVE_SCRIPT_API "%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    setx RESOLVE_SCRIPT_LIB  "%RESOLVE_PATH%\fusionscript.dll"
    setx PYTHONPATH "%%PYTHONPATH%%;%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules\"
    echo User environment variables for DaVinci Resolve scripting have been added.
) else (
    setx /M RESOLVE_SCRIPT_API "%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    setx /M RESOLVE_SCRIPT_LIB  "%RESOLVE_PATH%\fusionscript.dll"
    setx /M PYTHONPATH "%%PYTHONPATH%%;%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules\"
    echo System environment variables for DaVinci Resolve scripting have been added.
)
pause