echo off
for /F "tokens=* USEBACKQ" %%F IN (`type loglab\version.py`) DO (
set ver=%%F
)
set version=%ver:~11,5%
echo -- Build version %version% --
pyinstaller loglab\cli.py --name loglab --icon image/loglab.ico --noconfirm
set wver="%version%.0"
rem pyinstaller loglab.spec --name loglab --icon image/loglab.ico
tools\verpatch.exe dist\loglab.exe %wver% /va /pv %wver% /s description "LogLab : Design & Validate Log Files." /s product "LogLab"
coverage run --source loglab --parallel-mode --module pytest tests
