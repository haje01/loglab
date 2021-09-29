echo off
for /F "tokens=* USEBACKQ" %%F IN (`type loglab\version.py`) DO (
set ver=%%F
)
set version=%ver:~9,5%
echo -- Build version %version% --
set VERSION="%version%.0"
rem pyinstaller loglab\cli.py --onefile --name loglab --icon images/loglab.ico
pyinstaller loglab.spec --name loglab --icon images/loglab.ico
tools\verpatch.exe dist\loglab.exe %VERSION% /va /pv %VERSION% /s description "LogLab - Design & Validate Log Files." /s product "LogLab"
coverage run --source loglab --parallel-mode --module pytest tests
