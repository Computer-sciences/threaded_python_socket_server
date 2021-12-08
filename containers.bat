@echo off

:docker:
set /p COMMAND=Build or run? { b, or r }: 

echo %COMMAND%

if "%COMMAND%"=="b" (
	echo build was b
	echo Please wait while Docker boots..
	docker build ./ -t server
	pause
) else if "%COMMAND%"=="r" (
	echo build was r
	echo Please wait while Docker boots..
	powershell -command docker run -p 127.0.0.1:10000:10000 -p 127.0.0.1:10001:10001 --user=root -it -v "${pwd}:/root/env" --rm server
	pause
) else (
	echo no command found
	pause
	exit
)