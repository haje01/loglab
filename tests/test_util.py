import os
from shutil import rmtree

import pytest

from loglab.util import download, request_ext_dir


@pytest.fixture
def clear():
    _clear()


def _clear():
    # 결과 디렉토리 삭제
    if os.path.isdir('.loglab'):
        rmtree(".loglab")


def test_download(clear):
    edir = request_ext_dir()
    assert '.loglab/extern' in edir
    path = os.path.join(edir, 'sample.lab.json')
    download(
        'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/sample.lab.json',
        path
    )
    assert os.path.isfile(path)
