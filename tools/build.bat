echo off
pytest tests

for /F "tokens=* USEBACKQ" %%F IN (`type loglab\version.py`) DO (
set ver=%%F
)
set version=%ver:~9,5%
echo -- Build version %version% --
pyinstaller loglab\cli.py --name loglab --hidden-import=click --icon image/loglab.ico --onefile --noconfirm ^
    --add-data="schema/lab.schema.json;schema" ^
    --add-data="template/tmpl_doc.html.jinja;template" ^
    --add-data="template/tmpl_obj.cs.jinja;template" ^
    --add-data="template/tmpl_obj.py.jinja;template" ^
    | rem
timeout 3
set wver="%version%.0"
tools\verpatch.exe dist\loglab.exe %wver% /va /pv %wver% /s description "Design & Validate Log Files." /s product "LogLab" /s copyright "(c) 2025"
