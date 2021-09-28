pyinstaller loglab/cli.py --onefile --name loglab --icon images/loglab.ico
coverage run --source loglab --parallel-mode --module pytest tests
