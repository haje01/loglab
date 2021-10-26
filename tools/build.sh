pytest tests
pyinstaller loglab/cli.py --name loglab --icon image/loglab.ico --onefile --noconfirm --add-data="schema/lab.schema.json:schema"
