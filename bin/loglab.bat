 @echo off
 title loglab

 REM 설치된 도구 환경의 Python 직접 실행
 if exist "%USERPROFILE%\AppData\Roaming\uv\tools\loglab\Scripts\python.exe" (
     "%USERPROFILE%\AppData\Roaming\uv\tools\loglab\Scripts\python.exe" -m loglab.cli %*
     goto :end
 )

 echo Error: loglab is not properly installed. Please reinstall with uv.
 exit /b 1

 :end
