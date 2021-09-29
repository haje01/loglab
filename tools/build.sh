pyinstaller loglab/cli.py --name loglab --icon image/loglab.ico --noconfirm
coverage run --source loglab --parallel-mode --module pytest tests
