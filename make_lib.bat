@echo off
choice /c yn /m "��ȷ���Ƿ���붯̬���ӿ�"
if %errorlevel% == 1 (
	gcc -shared -fPIC -o lib/libpathfinder.dll c_src/path_finder.c
) else (
	echo ��ȡ��
)
pause