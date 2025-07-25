@echo off
title loglab

REM uvx가 PATH에 있으면 사용
uvx --from loglab loglab %* 2>nul && goto :end

REM uvx가 없으면 uv tool run 사용
uv tool run --from loglab loglab %* 2>nul && goto :end

REM 로컬 설치된 uv 시도
"%USERPROFILE%\.local\bin\uv.exe" tool run --from loglab loglab %* 2>nul && goto :end

REM 모두 실패하면 에러
echo Error: uv is not found. Please install uv and try again.
exit /b 1

:end
