@echo off
choice /c yn /m "请确认是否编译动态链接库"
if %errorlevel% == 1 (
	gcc -shared -fPIC -o lib/libpathfinder.dll c_src/path_finder.c
) else (
	echo 已取消
)
pause