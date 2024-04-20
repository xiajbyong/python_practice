@echo off
cd /d "你的当前目录路径"
updatereg.exe
if %errorlevel% equ 0 (
    regedit /s add_mouse_right_func.reg
) else (
    echo updatereg.exe运行失败，add_mouse_right_func.reg未被执行。
)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
echo 长路径支持已启用，请按任意键退出。
pause