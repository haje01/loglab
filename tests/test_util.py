import os

import pytest

from loglab.util import download, request_imp_dir, test_reset


@pytest.fixture
def clear():
    test_reset()


def test_download(clear):
    edir = request_imp_dir()
    assert '.loglab/import' in edir
    path = os.path.join(edir, 'foo.lab.json')
    download(
        'https://raw.githubusercontent.com/haje01/loglab/master/tests/files/foo.lab.json',
        path
    )
    assert os.path.isfile(path)
