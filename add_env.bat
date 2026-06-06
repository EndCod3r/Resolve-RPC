@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    setx RESOLVE_SCRIPT_API "%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    setx RESOLVE_SCRIPT_LIB  "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    setx PYTHONPATH "%%PYTHONPATH%%;%%RESOLVE_SCRIPT_API%%\Modules\"
) else (
    setx /M RESOLVE_SCRIPT_API "%%PROGRAMDATA%%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    setx /M RESOLVE_SCRIPT_LIB  "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    setx /M PYTHONPATH "%%PYTHONPATH%%;%%RESOLVE_SCRIPT_API%%\Modules\"
)
echo Environment variables for DaVinci Resolve scripting have been added.
pause