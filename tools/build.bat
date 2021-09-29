echo off
for /F "tokens=* USEBACKQ" %%F IN (`type loglab\version.py`) DO (
set ver=%%F
)
set version=%ver:~9,5%
echo -- Build version %version% --
pyinstaller loglab\cli.py --name loglab --icon image/loglab.ico --onefile --noconfirm --add-data="schema/lab.schema.json;schema"
set wver="%version%.0"
rem pyinstaller loglab.spec --name loglab --icon image/loglab.ico
tools\verpatch.exe dist\loglab\loglab.exe %wver% /va /pv %wver% /s description "LogLab - Design & Validate Log Files." /s product "LogLab"
