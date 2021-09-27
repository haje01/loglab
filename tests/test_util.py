import os

import pytest

from loglab.util import download, request_ext_dir, test_clear


@pytest.fixture
def clear():
    test_reset()


def test_download(clear):
    edir = request_ext_dir()
    assert '.loglab/extern' in edir
    path = os.path.join(edir, 'foo.lab.json')
    download(
        'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/foo.lab.json',
        path
    )
    assert os.path.isfile(path)
