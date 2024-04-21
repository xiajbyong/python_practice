@echo off
set "currentPath=%~dp0"
echo %currentPath%
set "sourcePath="

:: 检查当前路径下是否存在source文件夹
if exist "%currentPath%source\" (
    set "sourcePath=%currentPath%source"
	echo %sourcePath%
) else (
    echo "source" folder does not exist in the current path.
    pause
    exit /b 1
)
if exist "%sourcePath%\updatereg.exe" (
    "%sourcePath%\updatereg.exe"
) else (
    echo "updatereg.exe" does not exist
    pause
    exit /b 1
)

regedit /s "%sourcePath%\add_mouse_right_func.reg"
if %errorlevel% equ 0 (
    echo add reg info successful!
) else (
    echo add reg info failed
    pause
    exit /b 1
)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
if %errorlevel% equ 0 (
    echo enable LongPathsEnabled successful!
) else (
    echo enable LongPathsEnabled failed
	pause
    exit /b 1
)
pause
exit /b 1